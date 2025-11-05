# C-A-D-E Setup Guide

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker & Docker Compose** (Recommended)
  - Docker: https://docs.docker.com/get-docker/
  - Docker Compose: https://docs.docker.com/compose/install/

OR

- **Python 3.11+**
  - Download from: https://www.python.org/downloads/
- **Node.js 18+**
  - Download from: https://nodejs.org/
- **npm** (comes with Node.js)

## Quick Start with Docker

The easiest way to run C-A-D-E is using Docker Compose:

```bash
# Clone the repository
git clone https://github.com/JOHNNYWHITEMIKE/C-A-D-E.git
cd C-A-D-E

# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop all services
docker-compose down
```

Access the application at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Manual Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
# On Linux/Mac
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. Start the backend server:
```bash
python main.py
```

The backend API will be available at http://localhost:8000

### Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
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

The frontend will be available at http://localhost:5173

## Development

### Backend Development

- The backend uses FastAPI with hot-reload enabled
- Edit files in `/backend`
- API documentation is automatically available at http://localhost:8000/docs

### Frontend Development

- The frontend uses Vite with hot-reload enabled
- Edit files in `/frontend/src`
- Changes will automatically reflect in the browser

### Environment Variables

Backend environment variables (optional):

```env
# .env file
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
HOST=0.0.0.0
PORT=8000
```

## Troubleshooting

### Port Already in Use

If ports 8000 or 5173 are already in use:

**Backend:**
```bash
# Change port in backend/main.py or use environment variable
PORT=8001 python main.py
```

**Frontend:**
```bash
# Change port in vite.config.js or use CLI flag
npm run dev -- --port 5174
```

### Dependencies Installation Issues

If you encounter dependency conflicts:

```bash
# Backend
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir

# Frontend
rm -rf node_modules package-lock.json
npm install
```

### CORS Issues

If you experience CORS errors, ensure:
1. Backend is running on http://localhost:8000
2. Frontend is configured to connect to the correct backend URL
3. CORS middleware is properly configured in backend/main.py

## Production Deployment

### Using Docker Compose (Recommended)

1. Update docker-compose.yml for production settings
2. Use production-ready environment variables
3. Configure reverse proxy (nginx/traefik)
4. Enable HTTPS with SSL certificates

### Manual Deployment

**Backend:**
```bash
# Use production-ready ASGI server
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Frontend:**
```bash
# Build for production
npm run build

# Serve with any static file server
# e.g., nginx, serve, etc.
npx serve -s dist -l 3000
```

## Next Steps

After setup:

1. Explore the Dashboard
2. Try creating your first agent in the Agent Builder
3. Browse the documentation for best practices
4. Check out the API documentation at http://localhost:8000/docs

## Getting Help

- Check the [main README](../README.md)
- Review the [Documentation](http://localhost:5173/docs) (when app is running)
- Open an issue on GitHub
- Join our community discussions

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vite.dev/)
- [Docker Documentation](https://docs.docker.com/)
