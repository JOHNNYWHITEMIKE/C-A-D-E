# C-A-D-E - Community of Autonomous AI Agent Development Environment

<div align="center">

[![License](https://img.shields.io/badge/License-GPL%203.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18.0+-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)](https://fastapi.tiangolo.com/)

**Autonomous Agent Studio + Infrastructure Layer**

*Your orchestration platform for building, testing, deploying, and networking AI agents*

</div>

## 🌟 What is C-A-D-E?

C-A-D-E is an **open-source orchestration platform** — essentially a **DevOps + IDE + agent-hub** designed for collaborative creation and management of **autonomous AI agents**.

It's your complete "Autonomous Agent Studio + Infrastructure Layer" where you can create, test, deploy, and network AI agents from a single unified environment.

### The Platform Blends:

🧠 **AI Agent Frameworks** (LangChain, AutoGPT, CrewAI, etc.)  
⚙️ **Developer Tools** (FastAPI backend, React frontend, Monaco code editor)  
🧰 **Automation Layer** (CLI + Dockerized environment)  
☁️ **Remote Integration** (GitHub syncing + API endpoints)

## 🧱 Core Components

### 1. Backend (FastAPI)
- Runs the API for creating, managing, and executing agents
- Stores metadata and configuration for all agents/projects
- Handles agent execution, logging, and results storage
- RESTful endpoints for complete agent lifecycle management

### 2. Frontend (React)
- Dashboard with analytics and management panels
- Monaco editor for direct in-browser code editing
- Visual interfaces for projects, agents, logs, and system health
- Real-time monitoring and statistics

### 3. CLI (Node.js / cade.js)
- Manage projects and agents from the terminal
- Automate build, deployment, and runtime tasks
- Integrates tightly with Docker and GitHub
- Command-line interface for power users

### 4. Dockerized Runtime
- Spin up the entire stack with `docker-compose up`
- Provides reproducible local or remote environments
- Enables container-based agent isolation
- Easy deployment and scaling

## 🚀 What You Can Do With C-A-D-E

### 🧠 Build & Test Agents
- Scaffold agents with built-in templates
- Develop using your preferred framework (LangChain, CrewAI, OpenAI SDK, etc.)
- Test agents locally or in Dockerized sandboxes
- Use the Monaco code editor for professional development experience

### 🧩 Orchestrate Multi-Agent Systems
- Combine multiple agents into one project
- Use C-A-D-E as a controller layer for local and remote execution
- Define communication protocols between agents via REST/WebSocket
- Coordinate complex multi-agent workflows

### ☁️ Sync & Deploy via GitHub
- Automatically discover agents in your repos
- Deploy remotely to GitHub runners or any Docker host
- Use Actions or your orchestrator agent to manage agent lifecycles
- Version control your agent ecosystem

### 📊 Visualize & Manage
- **Dashboard**: agent usage, runtime logs, error tracking
- **Project view**: versioned groups of agents
- **Documentation panel**: live API and quickstart references
- **Analytics**: monitor performance and system health

### 🧰 Extend and Integrate
- Expose custom API routes in FastAPI backend
- Add custom front-end components for agent visualization
- Connect CADE to any LLM API, vector DB, or data source
- Plugin-ready architecture for extensibility

## Architecture

C-A-D-E is built with a modern, scalable architecture:

- **Frontend**: React 18 + Vite + Monaco Editor
- **Backend**: FastAPI (Python)
- **CLI**: Node.js command-line tools
- **Styling**: Custom CSS with dark cyberpunk theme
- **Deployment**: Docker & Docker Compose

## Quick Start

### Prerequisites

- Docker and Docker Compose (recommended)
- OR Python 3.11+ and Node.js 18+

### 🚀 Launch the Stack

#### Option 1: Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/JOHNNYWHITEMIKE/C-A-D-E.git
cd C-A-D-E
```

2. Start the application:
```bash
docker-compose up -d
```

3. Access the platform:
   - **Frontend**: http://localhost:5173
   - **Backend API**: http://localhost:8000
   - **API Docs**: http://localhost:8000/docs

#### Option 2: Manual Setup

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

### 🎯 Using the CLI

The C-A-D-E CLI provides command-line access to manage projects and agents:

```bash
# Initialize C-A-D-E environment
node bin/cade.js init

# Create a new project
node bin/cade.js create my-agent-project

# List available modules
node bin/cade.js list

# Check system status
node bin/cade.js status
```

For more CLI commands, run:
```bash
node bin/cade.js help
```

## Usage

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
5. Run and manage your multi-agent application

### Browsing Agents

- View all created agents in the **Agents** page
- Filter by category or search by name
- Run, view, or edit existing agents
- Execute agents with custom input data

### Orchestrating Multi-Agent Systems

C-A-D-E excels at coordinating multiple agents:

1. Create individual agents for specific tasks
2. Group them into a project
3. Define communication protocols via the API
4. Execute coordinated workflows
5. Monitor results in the dashboard

## 💡 In Short

**C-A-D-E is a self-contained ecosystem for AI agents:**

✅ **Dev platform** for building and debugging  
✅ **Orchestrator** for running and networking agents  
✅ **Community hub** for sharing and deploying them  
✅ **Automation backbone** for scaling your agent infrastructure

## API Documentation

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

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Roadmap

### Current Features ✅
- Visual agent builder with Monaco editor
- Multi-framework support (LangChain, AutoGPT, CrewAI, etc.)
- Project management system
- RESTful API with FastAPI
- Docker deployment
- CLI tool for automation
- Dashboard with analytics

### Upcoming Features 🚧
- [ ] **Database integration** (PostgreSQL/MongoDB)
- [ ] **User authentication** and authorization
- [ ] **Agent marketplace** for sharing
- [ ] **Real-time collaboration** features
- [ ] **Advanced agent monitoring** and logging
- [ ] **WebSocket support** for agent communication
- [ ] **Plugin system** for extensibility
- [ ] **Cloud deployment** templates
- [ ] **Agent chaining** and workflow builder
- [ ] **GitHub Actions** integration for CI/CD

## 🙏 Acknowledgments

- Inspired by [awesome_ai_agents](https://github.com/jim-schwoebel/awesome_ai_agents) repository
- Built with modern web technologies and AI frameworks
- Community-driven and open-source

## 📜 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Awesome AI Agents Repository](https://github.com/jim-schwoebel/awesome_ai_agents)
- [Issue Tracker](https://github.com/JOHNNYWHITEMIKE/C-A-D-E/issues)
- [Discussions](https://github.com/JOHNNYWHITEMIKE/C-A-D-E/discussions)

---

<div align="center">

**Made with ❤️ by the C-A-D-E Community**

*Your Autonomous Agent Studio + Infrastructure Layer*

⭐ Star this repository if you find it helpful!

</div>

