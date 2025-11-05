"""
C-A-D-E Backend API Server
Community Application Development Environment
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv
from sample_data import get_sample_agents, get_sample_projects

load_dotenv()

app = FastAPI(
    title="C-A-D-E API",
    description="Community Application Development Environment - AI Agent Platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class Agent(BaseModel):
    id: str
    name: str
    description: str
    category: str
    framework: str
    language: str
    code: Optional[str] = ""
    
class AgentExecution(BaseModel):
    agent_id: str
    input_data: Dict[str, Any]
    
class Project(BaseModel):
    id: str
    name: str
    description: str
    agents: List[str] = []

# In-memory storage (would be database in production)
agents_db: Dict[str, Agent] = {}
projects_db: Dict[str, Project] = {}

# Load sample data on startup
@app.on_event("startup")
async def load_sample_data():
    """Load sample agents and projects"""
    # Load sample agents
    for agent_data in get_sample_agents():
        agents_db[agent_data["id"]] = Agent(**agent_data)
    
    # Load sample projects
    for project_data in get_sample_projects():
        projects_db[project_data["id"]] = Project(**project_data)
    
    print(f"✓ Loaded {len(agents_db)} sample agents")
    print(f"✓ Loaded {len(projects_db)} sample projects")

# Root endpoint
@app.get("/")
async def root():
    return {
        "name": "C-A-D-E API",
        "version": "1.0.0",
        "description": "Community Application Development Environment",
        "status": "operational"
    }

# Health check
@app.get("/health")
async def health():
    return {"status": "healthy"}

# Agent endpoints
@app.get("/agents")
async def list_agents():
    """List all available agents"""
    return {"agents": list(agents_db.values())}

@app.post("/agents")
async def create_agent(agent: Agent):
    """Create a new agent"""
    if agent.id in agents_db:
        raise HTTPException(status_code=400, detail="Agent already exists")
    agents_db[agent.id] = agent
    return {"message": "Agent created", "agent": agent}

@app.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    """Get agent details"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"agent": agents_db[agent_id]}

@app.put("/agents/{agent_id}")
async def update_agent(agent_id: str, agent: Agent):
    """Update an agent"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")
    agents_db[agent_id] = agent
    return {"message": "Agent updated", "agent": agent}

@app.delete("/agents/{agent_id}")
async def delete_agent(agent_id: str):
    """Delete an agent"""
    if agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")
    del agents_db[agent_id]
    return {"message": "Agent deleted"}

@app.post("/agents/execute")
async def execute_agent(execution: AgentExecution):
    """Execute an agent with given input"""
    if execution.agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    agent = agents_db[execution.agent_id]
    # Placeholder for execution logic
    return {
        "message": "Agent executed",
        "agent_id": execution.agent_id,
        "status": "success",
        "output": f"Executed {agent.name} with input: {execution.input_data}"
    }

# Project endpoints
@app.get("/projects")
async def list_projects():
    """List all projects"""
    return {"projects": list(projects_db.values())}

@app.post("/projects")
async def create_project(project: Project):
    """Create a new project"""
    if project.id in projects_db:
        raise HTTPException(status_code=400, detail="Project already exists")
    projects_db[project.id] = project
    return {"message": "Project created", "project": project}

@app.get("/projects/{project_id}")
async def get_project(project_id: str):
    """Get project details"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"project": projects_db[project_id]}

# Categories and frameworks
@app.get("/categories")
async def get_categories():
    """Get available agent categories"""
    return {
        "categories": [
            "Autonomous Agents",
            "Code Generation",
            "Data Analysis",
            "Web Automation",
            "NLP & Chat",
            "Workflow Automation",
            "Research & Development",
            "Testing & QA"
        ]
    }

@app.get("/frameworks")
async def get_frameworks():
    """Get available AI frameworks"""
    return {
        "frameworks": [
            "LangChain",
            "AutoGPT",
            "CrewAI",
            "OpenAI",
            "Anthropic Claude",
            "HuggingFace",
            "Custom"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
