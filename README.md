# 🤖 C-A-D-E - Community Application Development Environment

<div align="center">

[![License](https://img.shields.io/badge/License-GPL%203.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18.0+-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)](https://fastapi.tiangolo.com/)

**A comprehensive platform for building, testing, and deploying AI agents**

</div>

## 📖 Overview

C-A-D-E (Community Application Development Environment) is an open-source, full-stack platform designed to empower developers to create, manage, and deploy AI agents with ease. Inspired by the [awesome_ai_agents](https://github.com/jim-schwoebel/awesome_ai_agents) repository, C-A-D-E provides a visual interface and powerful tools for working with various AI frameworks and models.

## ✨ Features

- 🎨 **Visual Agent Builder**: Create AI agents with an intuitive interface and built-in code editor
- 🔧 **Multi-Framework Support**: Works with LangChain, AutoGPT, CrewAI, OpenAI, Anthropic Claude, and more
- 📁 **Project Management**: Organize multiple agents into cohesive projects
- 🚀 **Execution Environment**: Test and run agents in a secure, isolated environment
- 📊 **Dashboard**: Monitor agent statistics and system health
- 📚 **Comprehensive Documentation**: Built-in guides and best practices
- 🌐 **RESTful API**: Backend API for programmatic access
- 🐳 **Docker Support**: Easy deployment with Docker Compose

## 🏗️ Architecture

C-A-D-E is built with a modern, scalable architecture:

- **Frontend**: React 18 + Vite + Monaco Editor
- **Backend**: FastAPI (Python)
- **Styling**: Custom CSS with dark theme
- **Deployment**: Docker & Docker Compose

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose (recommended)
- OR Python 3.11+ and Node.js 18+

### Option 1: Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/JOHNNYWHITEMIKE/C-A-D-E.git
cd C-A-D-E
```

2. Start the application:
```bash
docker-compose up -d
```

3. Access the application:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

#### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file (optional):
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. Run the backend server:
```bash
python main.py
```

The API will be available at http://localhost:8000

#### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at http://localhost:5173

## 📚 Usage

### Creating Your First Agent

1. Navigate to the **Agent Builder** from the sidebar
2. Fill in the agent details:
   - Name: Give your agent a descriptive name
   - Description: Explain what your agent does
   - Category: Select from available categories
   - Framework: Choose your AI framework
3. Write your agent code in the Monaco editor
4. Click **Create Agent** to save

### Managing Projects

1. Go to the **Projects** page
2. Click **+ New Project**
3. Enter project details
4. Add agents to your project
5. Run and manage your AI application

### Browsing Agents

- View all created agents in the **Agents** page
- Filter by category or search by name
- Run, view, or edit existing agents

## 🛠️ API Documentation

The backend provides a RESTful API with the following endpoints:

- `GET /` - API information
- `GET /health` - Health check
- `GET /agents` - List all agents
- `POST /agents` - Create a new agent
- `GET /agents/{agent_id}` - Get agent details
- `PUT /agents/{agent_id}` - Update an agent
- `DELETE /agents/{agent_id}` - Delete an agent
- `POST /agents/execute` - Execute an agent
- `GET /projects` - List all projects
- `POST /projects` - Create a new project
- `GET /categories` - Get available categories
- `GET /frameworks` - Get supported frameworks

Full API documentation is available at http://localhost:8000/docs

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📋 Roadmap

- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] User authentication and authorization
- [ ] Agent marketplace for sharing
- [ ] Real-time collaboration features
- [ ] Advanced agent monitoring and logging
- [ ] Integration with more AI frameworks
- [ ] Plugin system for extensibility
- [ ] Cloud deployment templates

## 🙏 Acknowledgments

- Inspired by [awesome_ai_agents](https://github.com/jim-schwoebel/awesome_ai_agents) repository
- Built with modern web technologies and AI frameworks
- Community-driven and open-source

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Awesome AI Agents Repository](https://github.com/jim-schwoebel/awesome_ai_agents)
- [Issue Tracker](https://github.com/JOHNNYWHITEMIKE/C-A-D-E/issues)
- [Discussions](https://github.com/JOHNNYWHITEMIKE/C-A-D-E/discussions)

---

<div align="center">

**Made with ❤️ by the C-A-D-E Community**

⭐ Star this repository if you find it helpful!

</div>
# C.A.D.E.

**Community Application Development Environment**

A collaborative development platform designed to streamline the application development process for teams and communities.

## Features

- 🚀 **Modular Architecture**: Extensible module system for different development needs
- 🛠️ **Project Management**: Easy project creation and configuration
- 🤝 **Collaboration-First**: Built with team development in mind
- 📦 **Built-in Modules**: Web development, API building, testing, and more
- 💻 **CLI & API**: Use via command line or as a library
- 🎨 **Developer-Friendly**: Colored logging and intuitive interface

## Quick Start

### Run the Environment

```bash
node src/index.js
```

### Use the CLI

```bash
# Initialize C.A.D.E.
node bin/cade.js init

# Create a new project
node bin/cade.js create my-app

# List available modules
node bin/cade.js list

# Check status
node bin/cade.js status
```

### Use as a Library

```javascript
import { CADECore } from './src/core/cade-core.js';

const cade = new CADECore();
await cade.initialize();

const project = await cade.createProject('my-app');
```

## Available Modules

- **web-dev**: Web development tools and templates
- **api-builder**: REST API scaffolding and tools
- **collaboration**: Team collaboration features
- **testing**: Testing framework integration

## Documentation

- [Getting Started](docs/getting-started.md)
- [API Documentation](docs/api.md)
- [Architecture](docs/architecture.md)

## Examples

Check out the `examples/` directory for usage examples:

```bash
node examples/hello-world.js
```

## Requirements

- Node.js >= 16.0.0

## License

GPL-3.0 - See [LICENSE](LICENSE) file for details

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## Author

JOHNNYWHITEMIKE
# C-A-D-E
COMMUNITY APPLICATION DEVELOPMENT ENVIRONMENT

## Overview

C-A-D-E is a comprehensive resource for application development, providing detailed documentation on:
- Job roles and descriptions in software development
- AI agent employees for virtual teams
- Complete blueprint for application creation from start to finish

## Documentation

### ⚡ [Quick Reference Guide](./QUICK_REFERENCE.md)
Fast overview with visual diagrams, decision matrices, and reading guides:
- Documentation overview and structure
- Team composition recommendations
- Quick start workflow (week-by-week)
- Decision matrix (human vs AI for each task)
- Success metrics and technology recommendations
- Common use cases and pro tips

### 📋 [Job Descriptions](./JOB_DESCRIPTIONS.md)
Complete guide to all roles involved in application development, from design to development:
- Product Management (CEO, Product Owner, Product Manager)
- Technical Leadership (CTO, Technical Architect, Technical Lead)
- Research (UX Researcher)
- Design (UI/UX Designer, Product Designer)
- Development (Frontend, Backend, Full-Stack, Mobile Developers)
- Quality Assurance (QA Engineer, Tester, Code Reviewer)
- DevOps & Infrastructure (DevOps Engineer)
- Security (Security Engineer)
- Documentation (Technical Writer)

Each role includes:
- Overview and responsibilities
- Key skills required
- How they fit in the development process

### 🤖 [AI Agent Employee List](./EMPLOYEE_LIST.md)
Curated list of 50+ AI agents from the [awesome_ai_agents](https://github.com/jim-schwoebel/awesome_ai_agents) repository that can serve as virtual team members:
- Executive & Product Management Agents
- Technical Architecture & Leadership Agents
- Research & Analysis Agents
- Design & UI/UX Agents
- Development & Programming Agents
- Testing & QA Agents
- DevOps & Infrastructure Agents
- Sales & Business Development Agents
- Customer Support Agents
- Multi-Agent Frameworks & Orchestration Tools

Includes practical guidance on:
- Building virtual teams with AI agents
- Framework recommendations
- Best practices for agent collaboration

### 🎯 [App Creation Blueprint](./APP_CREATION_BLUEPRINT.md)
Step-by-step guide for creating applications from concept to deployment:

**7 Phases of Development:**
1. **Pre-Planning & Discovery** - Problem identification and validation
2. **Requirements & Planning** - Requirements definition and project planning
3. **Design & Architecture** - UX research, UI design, and technical architecture
4. **Development Setup** - Environment and project scaffolding
5. **Implementation** - Feature development and integration
6. **Testing & QA** - Comprehensive testing strategy
7. **Deployment & Release** - Launch and go-live
8. **Maintenance & Iteration** - Ongoing support and enhancement

**Also Includes:**
- Best practices for development and team collaboration
- Agile/Scrum framework guidance
- Technology stack recommendations
- Timeline estimates (6-12 months for MVP)
- Risk management strategies
- Success metrics and KPIs

## Quick Start

1. **Understand the Roles**: Start with [JOB_DESCRIPTIONS.md](./JOB_DESCRIPTIONS.md) to understand what roles are needed
2. **Build Your Team**: Check [EMPLOYEE_LIST.md](./EMPLOYEE_LIST.md) for AI agents that can fill these roles
3. **Follow the Blueprint**: Use [APP_CREATION_BLUEPRINT.md](./APP_CREATION_BLUEPRINT.md) as your roadmap

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to improve the documentation.

## Use Cases

- **Startups**: Build your first application with limited resources
- **Development Teams**: Standardize processes and roles
- **Students**: Learn about professional software development
- **AI Enthusiasts**: Explore AI agent capabilities in software development
- **Project Managers**: Understand the complete development lifecycle

## Resources

- [awesome_ai_agents Repository](https://github.com/jim-schwoebel/awesome_ai_agents) - Source of AI agent information
- [ChatDev](https://github.com/OpenBMB/ChatDev) - Virtual software company with AI agents
- [crewAI](https://github.com/joaomdmoura/crewai) - Framework for orchestrating AI agents
- [Agency Swarm](https://github.com/VRSEN/agency-swarm) - Multi-agent collaboration framework

## License

See [LICENSE](./LICENSE) file for details.

---

*Built with ❤️ for the software development community*
## CityHall

CityHall is the central hub for community governance and administration in C-A-D-E.

### Features

- **Member Management**: Add and remove community members
- **Announcements**: Make community-wide announcements
- **Proposals**: Submit and vote on community proposals
- **Community Information**: Track community statistics

### Usage

Run the demo:
```bash
python3 cityhall.py
```

Run tests:
```bash
python3 test_cityhall.py
```

### Example

```python
from cityhall import CityHall

# Create a CityHall instance
city_hall = CityHall("My Community")

# Add members
city_hall.add_member("Alice")
city_hall.add_member("Bob")

# Make an announcement
city_hall.make_announcement("Welcome everyone!")

# Submit and vote on a proposal
proposal_id = city_hall.submit_proposal("Should we add feature X?")
city_hall.vote_on_proposal(proposal_id, vote_for=True)

# Get community info
info = city_hall.get_info()
print(f"Community: {info['name']}, Members: {info['member_count']}")
```
