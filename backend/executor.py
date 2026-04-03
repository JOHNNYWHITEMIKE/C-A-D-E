"""
Agent execution engine for C-A-D-E.

Wraps ``freelance_agent.orchestration.docker_manager.DockerOrchestrator``
and adds graceful fallback when Docker is not available.

The ``TaskRouter`` skill-matching algorithm from
``freelance_agent.routing.router`` is reused here without importing the
heavy spaCy / sentence-transformers dependencies (those were loaded in
``__init__`` but never called during actual scoring).
"""
from __future__ import annotations

import json
import logging
import os
import re
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Docker orchestrator – import defensively so the app starts even without
# the docker daemon or docker SDK installed.
# ---------------------------------------------------------------------------
try:
    from freelance_agent.orchestration.docker_manager import DockerOrchestrator

    _docker_orch = DockerOrchestrator()
    DOCKER_AVAILABLE = True
    logger.info("Docker daemon connected – real execution enabled")
except (ImportError, ModuleNotFoundError, Exception) as exc:  # noqa: BLE001
    # Exception covers docker.errors.DockerException (daemon not running) as well as
    # missing docker SDK; all produce a graceful simulated-execution fallback.
    _docker_orch = None  # type: ignore[assignment]
    DOCKER_AVAILABLE = False
    logger.warning("Docker not available (%s) – executions will be simulated", exc)


# ---------------------------------------------------------------------------
# Lightweight agent router
# Reuses the Jaccard-based skill matching from TaskRouter without importing
# the ML dependencies that are loaded-but-never-called in that class.
# ---------------------------------------------------------------------------

_SKILL_CATEGORIES: Dict[str, List[str]] = {
    "web_development": [
        "react", "vue", "angular", "html", "css", "javascript",
        "typescript", "node.js", "express", "django", "flask",
        "fastapi", "php", "laravel", "wordpress", "frontend", "backend",
    ],
    "data_science": [
        "python", "pandas", "numpy", "scikit-learn", "tensorflow",
        "pytorch", "machine learning", "ml", "ai", "data analysis",
        "visualization", "matplotlib", "seaborn", "jupyter",
    ],
    "devops": [
        "docker", "kubernetes", "k8s", "ci/cd", "jenkins",
        "github actions", "aws", "azure", "gcp", "terraform",
        "ansible", "linux", "bash", "deployment",
    ],
    "api_development": [
        "rest", "api", "graphql", "websocket", "microservices",
        "postman", "swagger", "openapi",
    ],
    "database": [
        "postgresql", "mysql", "mongodb", "redis", "sql",
        "database", "orm", "sqlalchemy",
    ],
    "automation": [
        "selenium", "puppeteer", "playwright", "web scraping",
        "automation", "testing", "pytest", "jest",
    ],
}


def _extract_skills(text: str) -> List[str]:
    skills: set[str] = set()
    for skill_list in _SKILL_CATEGORIES.values():
        for skill in skill_list:
            if re.search(r"\b" + re.escape(skill.lower()) + r"\b", text.lower()):
                skills.add(skill)
    return list(skills)


def _jaccard(a: List[str], b: List[str]) -> float:
    sa, sb = {x.lower() for x in a}, {x.lower() for x in b}
    union = sa | sb
    return len(sa & sb) / len(union) if union else 0.0


def find_best_agent(
    agents: List[Dict[str, Any]],
    job_description: str,
) -> Tuple[Optional[Dict[str, Any]], float]:
    """
    Return (best_agent_dict, confidence) using the same Jaccard-based scoring
    as ``TaskRouter._score_agent`` / ``_calculate_skill_match``.

    Only considers agents where ``available == True``.
    """
    required_skills = _extract_skills(job_description)
    scored = []
    for agent in agents:
        if not agent.get("available"):
            continue
        agent_skills = agent.get("skills", [])
        if isinstance(agent_skills, str):
            try:
                agent_skills = json.loads(agent_skills)
            except Exception:
                agent_skills = []
        skill_score = _jaccard(agent_skills, required_skills) if required_skills else 0.5
        perf = agent.get("performance_score", 0.5)
        total = skill_score * 0.70 + perf * 0.30
        scored.append((agent, total))

    scored.sort(key=lambda x: x[1], reverse=True)
    return (scored[0][0], scored[0][1]) if scored else (None, 0.0)


# ---------------------------------------------------------------------------
# Execution engine
# ---------------------------------------------------------------------------


def run_agent_sync(
    agent: Dict[str, Any],
    task_data: Dict[str, Any],
    execution_id: str,
) -> Dict[str, Any]:
    """
    Run the agent container synchronously (called from a thread via
    ``asyncio.to_thread``).

    Returns a dict::

        {
            "status": "completed" | "failed" | "simulated",
            "logs": str,
            "exit_code": int,
            "container_id": str,
        }
    """
    docker_image = agent.get("docker_image", "")
    local_image = agent.get("local_image", "")
    image = local_image or docker_image

    if not DOCKER_AVAILABLE or not image:
        return _simulated_result(agent, task_data, execution_id)

    task_data = {**task_data, "task_id": execution_id}

    try:
        result = _docker_orch.start_agent(  # type: ignore[union-attr]
            agent_id=execution_id[:12],
            docker_image=image,
            task_data=task_data,
        )
    except Exception as exc:
        return {
            "status": "failed",
            "logs": f"Failed to start container: {exc}",
            "exit_code": -1,
            "container_id": "",
        }

    if result.get("status") != "running":
        return {
            "status": "failed",
            "logs": result.get("error", "Container did not start"),
            "exit_code": -1,
            "container_id": "",
        }

    container_id: str = result["container_id"]
    final = _docker_orch.monitor_container(  # type: ignore[union-attr]
        container_id, check_interval=2, max_checks=300
    )
    logs = _docker_orch.get_container_logs(container_id)  # type: ignore[union-attr]
    _docker_orch.cleanup_container(container_id, force=True)  # type: ignore[union-attr]

    docker_status = final.get("status", "unknown")
    status = "completed" if docker_status == "completed" else "failed"
    return {
        "status": status,
        "logs": logs,
        "exit_code": final.get("exit_code", -1),
        "container_id": container_id,
    }


def _simulated_result(
    agent: Dict[str, Any],
    task_data: Dict[str, Any],
    execution_id: str,
) -> Dict[str, Any]:
    """Return a clearly-labelled simulated result when Docker is unavailable."""
    logs = (
        f"[SIMULATED] Docker not available on this host.\n"
        f"Agent   : {agent.get('name', agent.get('id'))}\n"
        f"Image   : {agent.get('local_image') or agent.get('docker_image') or 'none'}\n"
        f"Task ID : {execution_id}\n"
        f"Input   : {json.dumps(task_data, indent=2)}\n\n"
        f"In a Docker-enabled environment this would run the container and\n"
        f"return real output here."
    )
    return {
        "status": "simulated",
        "logs": logs,
        "exit_code": 0,
        "container_id": "",
    }
