# 🚀 C-A-D-E Quick Start Guide

Get up and running with C-A-D-E in under 5 minutes!

## 🐳 Option 1: Docker (Fastest)

**Prerequisites:** Docker and Docker Compose installed

```bash
# Clone and run
git clone https://github.com/JOHNNYWHITEMIKE/C-A-D-E.git
cd C-A-D-E
docker-compose up -d

# Open your browser
# Frontend: http://localhost:5173
# Backend:  http://localhost:8000/docs
```

That's it! 🎉

## 💻 Option 2: Local Development

**Prerequisites:** Python 3.11+, Node.js 18+

```bash
# Clone repository
git clone https://github.com/JOHNNYWHITEMIKE/C-A-D-E.git
cd C-A-D-E

# Run the start script
chmod +x start.sh
./start.sh

# Or manually:

# Terminal 1 - Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py

# Terminal 2 - Frontend
cd frontend
npm install
npm run dev
```

## 🎯 Your First Agent in 3 Steps

### Step 1: Create an Agent

1. Open http://localhost:5173
2. Click **"Agent Builder"** in the sidebar
3. Fill in the details:
   - **Name:** "Hello World Agent"
   - **Description:** "My first AI agent"
   - **Category:** Select any
   - **Framework:** Choose your preference

### Step 2: Write Code

Use the built-in code editor:

```python
# Simple example
def main():
    print("Hello from C-A-D-E!")
    return {"status": "success", "message": "Agent executed"}

if __name__ == "__main__":
    main()
```

### Step 3: Save & Run

1. Click **"Create Agent"**
2. View your agent in the **"Agents"** page
3. Click **"Run"** to execute

## 📚 Next Steps

- **Explore Documentation:** Click "Documentation" in the sidebar
- **Create Projects:** Organize multiple agents together
- **Check API Docs:** http://localhost:8000/docs
- **Browse Examples:** Visit the awesome_ai_agents repository

## 🛠️ Common Commands

```bash
# Stop services (Docker)
docker-compose down

# View logs (Docker)
docker-compose logs -f

# Rebuild (Docker)
docker-compose up -d --build

# Backend only
cd backend && python main.py

# Frontend only
cd frontend && npm run dev

# Run tests (when available)
pytest  # Backend
npm test  # Frontend
```

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Check what's using the port
lsof -i :8000  # Backend
lsof -i :5173  # Frontend

# Or use different ports
# Edit docker-compose.yml or start commands
```

### Dependencies Issues

```bash
# Backend
cd backend
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Docker Issues

```bash
# Clean everything
docker-compose down -v
docker-compose up -d --build

# Check logs
docker-compose logs backend
docker-compose logs frontend
```

## 📖 Resources

- **Main README:** [README.md](README.md)
- **Setup Guide:** [docs/SETUP.md](docs/SETUP.md)
- **API Docs:** [docs/API.md](docs/API.md)
- **Awesome AI Agents:** https://github.com/jim-schwoebel/awesome_ai_agents

## 💡 Tips

- Use the **Monaco editor** for syntax highlighting
- **Categories** help organize your agents
- **Projects** allow multi-agent applications
- Check the **Dashboard** for statistics
- API is fully RESTful - integrate with any tool

## 🤝 Getting Help

- Check documentation first
- Open an issue on GitHub
- Review existing issues
- Join community discussions

---

**Ready to build amazing AI agents? Let's go! 🚀**
