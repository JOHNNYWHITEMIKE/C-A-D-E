# AI Freelance Agent System

**An intelligent system for creating optimized freelance profiles and orchestrating AI-powered task delegation for dropservice businesses.**

## Overview

This system enables you to operate as a highly effective freelancer on platforms like Fiverr and Upwork by:

1. **Automatically generating** professional, AI-optimized freelance profiles and resumes
2. **Intelligently routing** incoming jobs to specialized AI agents based on skills and requirements
3. **Managing Docker containers** that run autonomous AI agents for different tasks
4. **Tracking and optimizing** project progress, agent performance, and earnings
5. **Presenting a unified front** as a single freelancer while distributing work internally

## Architecture

```
Freelance Platform → Central AI Hub → Task Router → Docker Agents → Completed Work
                           ↓
                     Dashboard & Monitoring
```

See [Architecture Documentation](../docs/freelance-ai-agent-architecture.md) for detailed diagrams and flows.

## Features

### 🎯 Dynamic Profile Generation
- AI-powered resume and profile creation
- Platform-specific optimization (Upwork, Fiverr, Freelancer)
- Keyword optimization for discoverability
- Portfolio generation from past projects
- Multiple niche support

### 🧠 Intelligent Task Routing
- NLP-based job requirement analysis
- Semantic skill matching
- Automated agent selection
- Load balancing across agents
- Confidence scoring and fallback options

### 🐳 Docker Agent Orchestration
- Containerized AI agents from GitHub repository
- Automatic container lifecycle management
- Resource monitoring and optimization
- Health checking and auto-recovery
- Isolated execution environments

### 📊 Comprehensive Dashboard
- Real-time project tracking
- Agent utilization metrics
- Earnings analytics
- Performance monitoring
- Alert system for issues

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 15+
- Redis 7+
- OpenAI API key (or Anthropic Claude)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/JOHNNYWHITEMIKE/C-A-D-E.git
   cd C-A-D-E/backend/freelance_agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and settings
   ```

4. **Start the system**
   ```bash
   docker-compose up -d
   ```

## Usage Examples

### Generate a Freelance Profile

```python
from profile.generator import ProfileGenerator

# Initialize generator
generator = ProfileGenerator()

# Generate profile
profile = generator.generate_profile(
    niche="Python Web Development",
    skills=["Python", "Django", "FastAPI", "PostgreSQL", "Docker"],
    platform="upwork",
    experience_level="expert",
    previous_projects=[
        {
            "title": "E-commerce Platform",
            "description": "Built scalable platform handling 10k+ daily transactions"
        }
    ]
)

# Export for platform
upwork_profile = generator.export_for_platform(profile, "upwork")
print(upwork_profile)
```

### Route a Job to an Agent

```python
from routing.router import TaskRouter

# Initialize router
router = TaskRouter()

# Analyze a job posting
job_description = """
Need experienced Python developer to build web scraping tool.
Requirements: Selenium, BeautifulSoup, CSV export
Budget: $300-$500
Timeline: 1 week
"""

requirements = router.analyze_job(job_description, "Python Web Scraper")

# Find best agent
best_agent, confidence = router.find_best_agent(requirements)

print(f"Best Agent: {best_agent['name']}")
print(f"Confidence: {confidence:.2%}")

# Estimate duration and cost
duration = router.estimate_task_duration(requirements, best_agent)
cost = router.estimate_cost(duration, best_agent)

print(f"Estimated Duration: {duration} hours")
print(f"Estimated Cost: ${cost}")
```

### Orchestrate Docker Agents

```python
from orchestration.docker_manager import DockerOrchestrator

# Initialize orchestrator
orchestrator = DockerOrchestrator()

# Start an agent
task_data = {
    "task_id": "task_12345",
    "target_urls": ["https://example.com"],
    "data_fields": ["name", "price", "rating"],
    "output_format": "csv"
}

result = orchestrator.start_agent(
    agent_id="web-scraper-01",
    docker_image="ghcr.io/johnnywhitemike/agents/web-scraper:latest",
    task_data=task_data
)

if result['status'] == 'running':
    container_id = result['container_id']
    
    # Monitor container
    final_status = orchestrator.monitor_container(container_id)
    
    # Get logs
    logs = orchestrator.get_container_logs(container_id)
    
    # Cleanup
    orchestrator.cleanup_container(container_id)
```

## Project Structure

```
backend/freelance_agent/
├── profile/
│   ├── generator.py         # Profile generation
│   └── optimizer.py         # Profile optimization
├── routing/
│   ├── router.py            # Task routing engine
│   ├── analyzer.py          # Job analysis
│   └── matcher.py           # Skill matching
├── orchestration/
│   ├── docker_manager.py    # Docker operations
│   ├── agent_manager.py     # Agent lifecycle
│   └── monitor.py           # Health monitoring
├── dashboard/
│   └── analytics.py         # Analytics & metrics
├── requirements.txt
└── main.py

agents/
├── web-scraper/
│   ├── Dockerfile
│   ├── scraper.py
│   └── requirements.txt
├── python-web-dev/
├── data-analyst/
└── agents.yaml              # Agent manifest

docs/
├── freelance-ai-agent-architecture.md
├── freelance-ai-agent-implementation-plan.md
├── compliance-and-anti-detection.md
└── README.md
```

## Agent Development

### Creating a New Agent

1. **Create agent directory**
   ```bash
   mkdir agents/my-agent
   cd agents/my-agent
   ```

2. **Create Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY agent.py .
   CMD ["python", "agent.py"]
   ```

3. **Implement agent script**
   ```python
   # agent.py
   import os
   import json
   
   def main():
       task_data = json.loads(os.getenv('TASK_DATA', '{}'))
       # Process task
       # Save results to /output
   
   if __name__ == "__main__":
       main()
   ```

4. **Add to agents.yaml**
   ```yaml
   - id: "my-agent-01"
     name: "My Agent"
     skills: ["skill1", "skill2"]
     docker_image: "ghcr.io/username/my-agent:latest"
   ```

5. **Build and push**
   ```bash
   docker build -t ghcr.io/username/my-agent:latest .
   docker push ghcr.io/username/my-agent:latest
   ```

## Configuration

### Environment Variables

```bash
# API Keys
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/freelance_ai
REDIS_URL=redis://localhost:6379

# Docker
DOCKER_HOST=unix:///var/run/docker.sock
AGENT_REGISTRY=ghcr.io/yourusername

# Application
SECRET_KEY=your_secret_key
DEBUG=False
LOG_LEVEL=INFO
```

## Compliance & Ethics

**IMPORTANT**: Read the [Compliance and Anti-Detection Guidelines](../docs/compliance-and-anti-detection.md) before using this system on freelance platforms.

### Recommended Approach

1. **Full Disclosure** (Safest): State in your profile that you use AI tools
2. **Agency Model** (Recommended for Scale): Register as a company/agency
3. **Tool-Assisted** (Gray Area): Position AI as your development toolkit

### Key Principles

- ✅ Deliver high-quality work
- ✅ Be honest about capabilities
- ✅ Follow platform Terms of Service
- ✅ Maintain human oversight
- ✅ Provide excellent customer service
- ❌ Don't deceive clients
- ❌ Don't game the system
- ❌ Don't sacrifice quality for automation

## Documentation

- **[Architecture](../docs/freelance-ai-agent-architecture.md)** - System design and data flows
- **[Implementation Plan](../docs/freelance-ai-agent-implementation-plan.md)** - Step-by-step development guide
- **[Compliance Guidelines](../docs/compliance-and-anti-detection.md)** - Legal and ethical considerations
- **[App Creation Blueprint](../APP_CREATION_BLUEPRINT.md)** - General development methodology

## API Reference

### Profile Generation Endpoints

```
POST   /api/profiles/generate
GET    /api/profiles/{profile_id}
PUT    /api/profiles/{profile_id}
POST   /api/profiles/{profile_id}/export
```

### Task Routing Endpoints

```
POST   /api/jobs/analyze
POST   /api/jobs/assign
GET    /api/jobs/{job_id}/status
```

### Agent Orchestration Endpoints

```
GET    /api/agents
POST   /api/agents/{agent_id}/start
POST   /api/agents/{agent_id}/stop
GET    /api/agents/{agent_id}/health
GET    /api/agents/{agent_id}/logs
```

### Dashboard Endpoints

```
GET    /api/dashboard/stats
GET    /api/dashboard/projects
GET    /api/dashboard/earnings
```

## Testing

```bash
# Run tests
pytest tests/

# With coverage
pytest --cov=. tests/

# Specific test
pytest tests/test_profile_generator.py
```

## Deployment

### Docker Compose (Development)

```bash
docker-compose up -d
```

### Production Deployment

See [Implementation Plan](../docs/freelance-ai-agent-implementation-plan.md#phase-6-deployment-week-12) for detailed production deployment instructions.

## Performance Metrics

- **Job Analysis**: < 5 seconds
- **Agent Selection**: < 2 seconds
- **Container Startup**: < 30 seconds
- **Dashboard Load**: < 2 seconds
- **Concurrent Agents**: 10+
- **Success Rate**: > 95%

## Troubleshooting

### Docker Issues

```bash
# Check Docker status
docker ps

# View agent logs
docker logs <container_id>

# Restart orchestrator
docker-compose restart backend
```

### Database Issues

```bash
# Connect to database
psql $DATABASE_URL

# Check tables
\dt

# Reset database (development only)
alembic downgrade base
alembic upgrade head
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

GPL-3.0 - See [LICENSE](../LICENSE) for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/JOHNNYWHITEMIKE/C-A-D-E/issues)
- **Discussions**: [GitHub Discussions](https://github.com/JOHNNYWHITEMIKE/C-A-D-E/discussions)

## Acknowledgments

- Built following the [App Creation Blueprint](../APP_CREATION_BLUEPRINT.md)
- Inspired by the needs of solo entrepreneurs and dropservice businesses
- Powered by OpenAI, Docker, and the Python ecosystem

---

**⚠️ Legal Disclaimer**: This system is provided for educational purposes. Users are responsible for ensuring their use complies with all applicable laws and platform Terms of Service. Always prioritize ethical operation and client satisfaction.
