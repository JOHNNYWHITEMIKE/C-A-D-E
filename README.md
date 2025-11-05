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
