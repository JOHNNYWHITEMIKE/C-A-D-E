"""
Docker Agent Orchestrator
Manages Docker containers for AI agents
"""
import docker
from docker.errors import DockerException, NotFound, APIError
from typing import Dict, List, Optional
import logging
import time
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DockerOrchestrator:
    """Orchestrates Docker containers for AI agents"""
    
    def __init__(self, docker_host: str = "unix:///var/run/docker.sock"):
        """
        Initialize Docker orchestrator
        
        Args:
            docker_host: Docker daemon socket path
        """
        try:
            self.client = docker.DockerClient(base_url=docker_host)
            self.api_client = docker.APIClient(base_url=docker_host)
            # Test connection
            self.client.ping()
            logger.info("Docker connection established successfully")
        except DockerException as e:
            logger.error(f"Failed to connect to Docker: {e}")
            raise
    
    def start_agent(
        self,
        agent_id: str,
        docker_image: str,
        task_data: Dict,
        environment: Optional[Dict[str, str]] = None,
        volumes: Optional[Dict[str, Dict]] = None,
        resource_limits: Optional[Dict] = None
    ) -> Dict[str, str]:
        """
        Start a Docker container for an agent
        
        Args:
            agent_id: Unique identifier for the agent
            docker_image: Docker image to use
            task_data: Input data for the task
            environment: Environment variables
            volumes: Volume mounts
            resource_limits: CPU/memory limits
            
        Returns:
            Dictionary with container_id and status
        """
        container_name = f"agent_{agent_id}_{int(time.time())}"
        
        # Prepare environment variables
        env = environment or {}
        env['TASK_DATA'] = json.dumps(task_data)
        env['AGENT_ID'] = agent_id
        
        # Prepare volume mounts
        if volumes is None:
            volumes = {
                # Mount output directory for results
                f"/tmp/agent_output_{agent_id}": {
                    'bind': '/output',
                    'mode': 'rw'
                }
            }
        
        # Resource limits
        limits = resource_limits or {
            'mem_limit': '1g',
            'cpu_quota': 50000,  # 0.5 CPU
        }
        
        try:
            # Pull image if not present
            logger.info(f"Pulling Docker image: {docker_image}")
            try:
                self.client.images.pull(docker_image)
            except Exception as e:
                logger.warning(f"Could not pull image {docker_image}: {e}")
                # Continue anyway in case image exists locally
            
            # Create and start container
            logger.info(f"Starting container: {container_name}")
            container = self.client.containers.run(
                image=docker_image,
                name=container_name,
                environment=env,
                volumes=volumes,
                detach=True,
                remove=False,  # Keep container for log inspection
                **limits
            )
            
            logger.info(f"Container {container.id[:12]} started successfully")
            
            return {
                'container_id': container.id,
                'container_name': container_name,
                'status': 'running',
                'started_at': time.time()
            }
            
        except APIError as e:
            logger.error(f"Failed to start container: {e}")
            return {
                'container_id': None,
                'status': 'failed',
                'error': str(e)
            }
    
    def stop_agent(self, container_id: str, timeout: int = 10) -> Dict[str, str]:
        """
        Stop a running agent container
        
        Args:
            container_id: ID of the container to stop
            timeout: Timeout in seconds before force kill
            
        Returns:
            Status dictionary
        """
        try:
            container = self.client.containers.get(container_id)
            logger.info(f"Stopping container {container_id[:12]}")
            
            container.stop(timeout=timeout)
            
            return {
                'status': 'stopped',
                'container_id': container_id
            }
        except NotFound:
            logger.warning(f"Container {container_id[:12]} not found")
            return {
                'status': 'not_found',
                'container_id': container_id
            }
        except APIError as e:
            logger.error(f"Error stopping container: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def get_container_status(self, container_id: str) -> Dict:
        """
        Get current status of a container
        
        Args:
            container_id: ID of the container
            
        Returns:
            Status dictionary with details
        """
        try:
            container = self.client.containers.get(container_id)
            container.reload()  # Refresh container info
            
            stats = container.stats(stream=False)
            
            # Parse resource usage
            cpu_percent = self._calculate_cpu_percent(stats)
            memory_usage = self._calculate_memory_usage(stats)
            
            return {
                'container_id': container.id,
                'status': container.status,
                'name': container.name,
                'image': container.image.tags[0] if container.image.tags else 'unknown',
                'created': container.attrs['Created'],
                'started': container.attrs['State'].get('StartedAt', ''),
                'cpu_percent': cpu_percent,
                'memory_usage': memory_usage,
                'health': self._check_health(container)
            }
        except NotFound:
            return {
                'container_id': container_id,
                'status': 'not_found'
            }
        except Exception as e:
            logger.error(f"Error getting container status: {e}")
            return {
                'container_id': container_id,
                'status': 'error',
                'error': str(e)
            }
    
    def _calculate_cpu_percent(self, stats: Dict) -> float:
        """Calculate CPU usage percentage from stats"""
        try:
            cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - \
                       stats['precpu_stats']['cpu_usage']['total_usage']
            system_delta = stats['cpu_stats']['system_cpu_usage'] - \
                          stats['precpu_stats']['system_cpu_usage']
            cpu_count = stats['cpu_stats'].get('online_cpus', 1)
            
            if system_delta > 0:
                cpu_percent = (cpu_delta / system_delta) * cpu_count * 100.0
                return round(cpu_percent, 2)
        except (KeyError, ZeroDivisionError):
            pass
        return 0.0
    
    def _calculate_memory_usage(self, stats: Dict) -> Dict[str, float]:
        """Calculate memory usage from stats"""
        try:
            usage = stats['memory_stats']['usage']
            limit = stats['memory_stats']['limit']
            percent = (usage / limit) * 100.0
            
            return {
                'usage_mb': round(usage / (1024 * 1024), 2),
                'limit_mb': round(limit / (1024 * 1024), 2),
                'percent': round(percent, 2)
            }
        except (KeyError, ZeroDivisionError):
            return {
                'usage_mb': 0,
                'limit_mb': 0,
                'percent': 0
            }
    
    def _check_health(self, container) -> str:
        """Check container health status"""
        try:
            health = container.attrs['State'].get('Health', {})
            return health.get('Status', 'unknown')
        except:
            return 'unknown'
    
    def get_container_logs(
        self,
        container_id: str,
        tail: int = 100,
        follow: bool = False
    ) -> str:
        """
        Get logs from a container
        
        Args:
            container_id: ID of the container
            tail: Number of lines to return from end
            follow: Stream logs in real-time
            
        Returns:
            Log output as string
        """
        try:
            container = self.client.containers.get(container_id)
            logs = container.logs(
                tail=tail,
                follow=follow,
                timestamps=True
            )
            
            if isinstance(logs, bytes):
                return logs.decode('utf-8')
            return logs
        except NotFound:
            return f"Container {container_id[:12]} not found"
        except Exception as e:
            logger.error(f"Error getting logs: {e}")
            return f"Error: {str(e)}"
    
    def cleanup_container(self, container_id: str, force: bool = False) -> Dict[str, str]:
        """
        Remove a container
        
        Args:
            container_id: ID of the container
            force: Force removal even if running
            
        Returns:
            Status dictionary
        """
        try:
            container = self.client.containers.get(container_id)
            
            if container.status == 'running' and not force:
                return {
                    'status': 'error',
                    'message': 'Container is still running. Use force=True to remove.'
                }
            
            logger.info(f"Removing container {container_id[:12]}")
            container.remove(force=force)
            
            return {
                'status': 'removed',
                'container_id': container_id
            }
        except NotFound:
            return {
                'status': 'not_found',
                'container_id': container_id
            }
        except APIError as e:
            logger.error(f"Error removing container: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def list_agent_containers(self, all_containers: bool = False) -> List[Dict]:
        """
        List all agent containers
        
        Args:
            all_containers: Include stopped containers
            
        Returns:
            List of container information
        """
        try:
            containers = self.client.containers.list(
                all=all_containers,
                filters={'name': 'agent_'}
            )
            
            result = []
            for container in containers:
                result.append({
                    'container_id': container.id,
                    'name': container.name,
                    'status': container.status,
                    'image': container.image.tags[0] if container.image.tags else 'unknown',
                    'created': container.attrs['Created']
                })
            
            return result
        except Exception as e:
            logger.error(f"Error listing containers: {e}")
            return []
    
    def monitor_container(
        self,
        container_id: str,
        check_interval: int = 5,
        max_checks: int = 120
    ) -> Dict:
        """
        Monitor container until completion or timeout
        
        Args:
            container_id: ID of container to monitor
            check_interval: Seconds between status checks
            max_checks: Maximum number of checks before timeout
            
        Returns:
            Final status and results
        """
        logger.info(f"Monitoring container {container_id[:12]}")
        checks = 0
        
        while checks < max_checks:
            status = self.get_container_status(container_id)
            
            if status['status'] in ['exited', 'dead', 'not_found']:
                # Container has stopped
                logs = self.get_container_logs(container_id)
                
                # Check exit code
                try:
                    container = self.client.containers.get(container_id)
                    exit_code = container.attrs['State']['ExitCode']
                    
                    return {
                        'status': 'completed' if exit_code == 0 else 'failed',
                        'exit_code': exit_code,
                        'logs': logs,
                        'checks': checks
                    }
                except:
                    return {
                        'status': 'unknown',
                        'logs': logs,
                        'checks': checks
                    }
            
            time.sleep(check_interval)
            checks += 1
        
        # Timeout
        logger.warning(f"Container monitoring timed out after {max_checks} checks")
        return {
            'status': 'timeout',
            'checks': checks
        }
    
    def get_docker_info(self) -> Dict:
        """Get Docker system information"""
        try:
            info = self.client.info()
            return {
                'containers': info.get('Containers', 0),
                'containers_running': info.get('ContainersRunning', 0),
                'containers_paused': info.get('ContainersPaused', 0),
                'containers_stopped': info.get('ContainersStopped', 0),
                'images': info.get('Images', 0),
                'driver': info.get('Driver', 'unknown'),
                'memory_total': round(info.get('MemTotal', 0) / (1024**3), 2),  # GB
                'cpus': info.get('NCPU', 0)
            }
        except Exception as e:
            logger.error(f"Error getting Docker info: {e}")
            return {}


# Example usage
if __name__ == "__main__":
    # Initialize orchestrator
    orchestrator = DockerOrchestrator()
    
    # Get Docker system info
    docker_info = orchestrator.get_docker_info()
    print("Docker System Info:")
    print(json.dumps(docker_info, indent=2))
    
    # Example: Start an agent container
    task_data = {
        "task_id": "task_12345",
        "type": "web_scraping",
        "target_url": "https://example.com",
        "output_format": "csv"
    }
    
    # Note: This would use an actual agent image in production
    # result = orchestrator.start_agent(
    #     agent_id="web-scraper-01",
    #     docker_image="python:3.11-slim",  # Example image
    #     task_data=task_data
    # )
    # 
    # if result['status'] == 'running':
    #     container_id = result['container_id']
    #     print(f"Container started: {container_id}")
    #     
    #     # Monitor the container
    #     final_status = orchestrator.monitor_container(container_id)
    #     print(f"Final status: {final_status['status']}")
    #     
    #     # Cleanup
    #     orchestrator.cleanup_container(container_id, force=True)
    
    # List all agent containers
    containers = orchestrator.list_agent_containers(all_containers=True)
    print(f"\nAgent containers: {len(containers)}")
    for container in containers:
        print(f"  - {container['name']}: {container['status']}")
