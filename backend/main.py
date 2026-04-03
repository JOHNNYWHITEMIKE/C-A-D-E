"""
C-A-D-E Backend API Server
Community Application Development Environment
"""
from __future__ import annotations

import asyncio
import json
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from cade_v3.models import Task, TaskPriority, TaskType
from cade_v3.orchestrator import Orchestrator
from cityhall import CityHall
from crud import (
    count_agents,
    count_executions,
    count_projects,
    create_execution,
    create_project,
    delete_agent,
    delete_project,
    distinct_categories,
    get_agent,
    get_execution,
    list_agents,
    list_executions,
    list_projects,
    update_execution,
    update_project_agents,
    upsert_agent,
)
from database import AsyncSessionLocal, engine, get_db
from db_models import Base
from executor import DOCKER_AVAILABLE, find_best_agent, run_agent_sync
from manifest import load_manifest, manifest_agent_to_db

import os
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Subsystem singletons
# ---------------------------------------------------------------------------
orchestrator = Orchestrator()
city_hall = CityHall("C-A-D-E Community")

_PRIORITY_MAP: Dict[str, TaskPriority] = {
    "low": TaskPriority.LOW,
    "normal": TaskPriority.NORMAL,
    "high": TaskPriority.HIGH,
    "critical": TaskPriority.CRITICAL,
}
_TYPE_MAP: Dict[str, TaskType] = {t.value: t for t in TaskType}


# ---------------------------------------------------------------------------
# Startup / shutdown
# ---------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables (idempotent)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Sync manifest agents into DB
    async with AsyncSessionLocal() as db:
        manifest = load_manifest()
        for entry in manifest:
            await upsert_agent(db, manifest_agent_to_db(entry))
        print(f"Synced {len(manifest)} manifest agents into DB")

    print("Orchestrator initialised with foundation agents")
    print("CityHall initialised for community governance")
    print(f"Docker available: {DOCKER_AVAILABLE}")
    yield
    await engine.dispose()


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="C-A-D-E API",
    description="Community Application Development Environment – AI Agent Platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Pydantic request / response models
# ---------------------------------------------------------------------------


class AgentCreate(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    category: str
    framework: str
    language: str
    code: Optional[str] = ""
    docker_image: Optional[str] = ""


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    framework: Optional[str] = None
    language: Optional[str] = None
    code: Optional[str] = None
    docker_image: Optional[str] = None


class AgentExecution(BaseModel):
    agent_id: str
    input_data: Dict[str, Any] = {}


class ProjectCreate(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    agents: List[str] = []


class ProjectUpdate(BaseModel):
    agents: List[str]


class TaskSubmission(BaseModel):
    type: str
    payload: Dict[str, Any]
    priority: str = "normal"
    approved_by: Optional[str] = None


class MemberBody(BaseModel):
    name: str


class AnnouncementBody(BaseModel):
    text: str


class ProposalBody(BaseModel):
    description: str


class VoteBody(BaseModel):
    vote_for: bool = True


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------


@app.get("/")
async def root():
    return {
        "name": "C-A-D-E API",
        "version": "1.0.0",
        "description": "Community Application Development Environment",
        "status": "operational",
        "docker_available": DOCKER_AVAILABLE,
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------


@app.get("/dashboard/stats")
async def dashboard_stats(db: AsyncSession = Depends(get_db)):
    """Aggregate statistics from all subsystems."""
    total_agents = await count_agents(db)
    total_projects = await count_projects(db)
    total_executions = await count_executions(db)
    completed = await count_executions(db, status="completed")
    failed = await count_executions(db, status="failed")
    simulated = await count_executions(db, status="simulated")
    recent = await list_executions(db, limit=5)
    registry_agents = orchestrator.registry.list_all()
    return {
        "agents": {
            "total": total_agents,
            "categories": await distinct_categories(db),
        },
        "projects": {"total": total_projects},
        "executions": {
            "total": total_executions,
            "completed": completed,
            "failed": failed,
            "simulated": simulated,
            "recent": recent,
        },
        "orchestrator": {
            "foundation_agents": len(registry_agents),
            "agents_by_role": {
                role.value: orchestrator.registry.count(role)
                for role in orchestrator.registry._role_counts
            },
            "task_counts": dict(orchestrator._task_counter),
            "memory_topics": orchestrator.memory.snapshot(),
            "monetization_recommendation": orchestrator.monetization_summary(),
        },
        "community": city_hall.get_info(),
        "docker_available": DOCKER_AVAILABLE,
    }


# ---------------------------------------------------------------------------
# Agents
# ---------------------------------------------------------------------------


@app.get("/agents")
async def list_agents_ep(db: AsyncSession = Depends(get_db)):
    return {"agents": await list_agents(db)}


@app.post("/agents", status_code=201)
async def create_agent_ep(body: AgentCreate, db: AsyncSession = Depends(get_db)):
    agent_id = body.id or f"agent_{uuid.uuid4().hex[:12]}"
    existing = await get_agent(db, agent_id)
    if existing:
        raise HTTPException(status_code=409, detail="Agent ID already exists")
    row = await upsert_agent(db, {
        "id": agent_id,
        "name": body.name,
        "description": body.description,
        "category": body.category,
        "framework": body.framework,
        "language": body.language,
        "code": body.code or "",
        "docker_image": body.docker_image or "",
        "source": "user",
        "available": False,
    })
    from crud import _row_to_agent_dict
    return {"message": "Agent created", "agent": _row_to_agent_dict(row)}


@app.get("/agents/{agent_id}")
async def get_agent_ep(agent_id: str, db: AsyncSession = Depends(get_db)):
    row = await get_agent(db, agent_id)
    if not row:
        raise HTTPException(status_code=404, detail="Agent not found")
    from crud import _row_to_agent_dict
    return {"agent": _row_to_agent_dict(row)}


@app.put("/agents/{agent_id}")
async def update_agent_ep(
    agent_id: str, body: AgentUpdate, db: AsyncSession = Depends(get_db)
):
    row = await get_agent(db, agent_id)
    if not row:
        raise HTTPException(status_code=404, detail="Agent not found")
    update: Dict[str, Any] = {"id": agent_id}
    for field in ("name", "description", "category", "framework", "language", "code", "docker_image"):
        v = getattr(body, field, None)
        if v is not None:
            update[field] = v
    updated = await upsert_agent(db, update)
    from crud import _row_to_agent_dict
    return {"message": "Agent updated", "agent": _row_to_agent_dict(updated)}


@app.delete("/agents/{agent_id}", status_code=204)
async def delete_agent_ep(agent_id: str, db: AsyncSession = Depends(get_db)):
    removed = await delete_agent(db, agent_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Agent not found")


# ---------------------------------------------------------------------------
# Agent execution
# ---------------------------------------------------------------------------


async def _run_execution_background(
    execution_id: str,
    agent_dict: Dict[str, Any],
    input_data: Dict[str, Any],
) -> None:
    """Background task: runs the Docker container and updates the execution row."""
    async with AsyncSessionLocal() as db:
        await update_execution(db, execution_id, status="running")

    result = await asyncio.to_thread(
        run_agent_sync, agent_dict, input_data, execution_id
    )

    async with AsyncSessionLocal() as db:
        await update_execution(
            db,
            execution_id,
            status=result["status"],
            logs=result["logs"],
            exit_code=result["exit_code"],
            container_id=result.get("container_id", ""),
            finished_at=datetime.now(timezone.utc),
        )


@app.post("/agents/execute")
async def execute_agent(
    execution: AgentExecution,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """
    Submit an agent execution.  Returns immediately with an execution_id;
    the container runs in the background.  Poll GET /executions/{id}.
    """
    row = await get_agent(db, execution.agent_id)
    if not row:
        raise HTTPException(status_code=404, detail="Agent not found")

    from crud import _row_to_agent_dict
    agent_dict = _row_to_agent_dict(row)

    # Also route through cade_v3 orchestrator for task tracking
    task = Task(
        type=TaskType.CODE,
        payload={"agent_id": execution.agent_id, "agent_name": row.name},
        priority=TaskPriority.NORMAL,
    )
    orchestrator.submit(task)
    orch_result = orchestrator.process_next()

    execution_id = str(uuid.uuid4())
    await create_execution(
        db,
        execution_id=execution_id,
        agent_id=execution.agent_id,
        agent_name=row.name,
        input_data=execution.input_data,
        orchestrator_result=orch_result,
    )

    background_tasks.add_task(
        _run_execution_background,
        execution_id,
        agent_dict,
        execution.input_data,
    )

    return {
        "execution_id": execution_id,
        "agent_id": execution.agent_id,
        "status": "pending",
        "message": "Execution started – poll GET /executions/{execution_id} for results",
        "orchestrator_result": orch_result,
    }


# ---------------------------------------------------------------------------
# Executions
# ---------------------------------------------------------------------------


@app.get("/executions")
async def list_executions_ep(
    agent_id: Optional[str] = None,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    return {"executions": await list_executions(db, agent_id=agent_id, limit=limit)}


@app.get("/executions/{execution_id}")
async def get_execution_ep(execution_id: str, db: AsyncSession = Depends(get_db)):
    exc = await get_execution(db, execution_id)
    if not exc:
        raise HTTPException(status_code=404, detail="Execution not found")
    return {"execution": exc}


# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------


@app.get("/projects")
async def list_projects_ep(db: AsyncSession = Depends(get_db)):
    return {"projects": await list_projects(db)}


@app.post("/projects", status_code=201)
async def create_project_ep(body: ProjectCreate, db: AsyncSession = Depends(get_db)):
    project_id = body.id or f"project_{uuid.uuid4().hex[:12]}"
    project = await create_project(
        db,
        project_id=project_id,
        name=body.name,
        description=body.description,
        agent_ids=body.agents,
    )
    return {"message": "Project created", "project": project}


@app.get("/projects/{project_id}")
async def get_project_ep(project_id: str, db: AsyncSession = Depends(get_db)):
    row = await get_project_by_id(db, project_id)
    if not row:
        raise HTTPException(status_code=404, detail="Project not found")
    from crud import _row_to_project_dict
    return {"project": _row_to_project_dict(row)}


@app.put("/projects/{project_id}/agents")
async def update_project_agents_ep(
    project_id: str, body: ProjectUpdate, db: AsyncSession = Depends(get_db)
):
    updated = await update_project_agents(db, project_id, body.agents)
    if not updated:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project agents updated", "project": updated}


@app.delete("/projects/{project_id}", status_code=204)
async def delete_project_ep(project_id: str, db: AsyncSession = Depends(get_db)):
    removed = await delete_project(db, project_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Project not found")


# helper not in crud yet
async def get_project_by_id(db, project_id):
    from crud import get_project
    return await get_project(db, project_id)


# ---------------------------------------------------------------------------
# Agent routing
# ---------------------------------------------------------------------------


@app.get("/agents/route/best")
async def route_best_agent(job: str, db: AsyncSession = Depends(get_db)):
    """Return the best available agent for a job description."""
    agents = await list_agents(db)
    best, confidence = find_best_agent(agents, job)
    if not best:
        raise HTTPException(status_code=404, detail="No available agents found")
    return {"agent": best, "confidence": round(confidence, 3)}


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


@app.get("/orchestrator/status")
async def orchestrator_status():
    agents = [
        {
            "id": a.id,
            "role": a.role.value,
            "skills": a.skills,
            "status": a.status,
            "created_at": a.created_at.isoformat(),
        }
        for a in orchestrator.registry.list_all()
    ]
    return {
        "agents": agents,
        "task_counts": dict(orchestrator._task_counter),
        "memory_snapshot": orchestrator.memory.snapshot(),
        "monetization_recommendation": orchestrator.monetization_summary(),
    }


@app.post("/orchestrator/tasks")
async def submit_task(submission: TaskSubmission):
    task_type = _TYPE_MAP.get(submission.type.lower())
    if task_type is None:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown task type. Valid: {list(_TYPE_MAP.keys())}",
        )
    priority = _PRIORITY_MAP.get(submission.priority.lower(), TaskPriority.NORMAL)
    task = Task(type=task_type, payload=submission.payload, priority=priority)
    orchestrator.submit(task)
    ctx: Dict[str, str] = {}
    if submission.approved_by:
        ctx["approved_by"] = submission.approved_by
    result = orchestrator.process_next(ctx)
    return {
        "task_id": task.id,
        "type": task_type.value,
        "priority": priority.name.lower(),
        "orchestrator_result": result,
        "status": "blocked" if result.startswith("blocked") else "queued_and_processed",
    }


@app.get("/orchestrator/memory")
async def orchestrator_memory(topic: Optional[str] = None, limit: int = 10):
    entries = orchestrator.memory.query(topic or "", limit=limit)
    return {
        "entries": [
            {
                "topic": e.topic,
                "content": e.content,
                "confidence": e.confidence,
                "created_at": e.created_at.isoformat(),
            }
            for e in entries
        ]
    }


# ---------------------------------------------------------------------------
# Community (CityHall)
# ---------------------------------------------------------------------------


@app.get("/community/info")
async def community_info():
    return city_hall.get_info()


@app.get("/community/members")
async def list_members():
    return {"members": city_hall.get_members()}


@app.post("/community/members")
async def add_member(body: MemberBody):
    if not city_hall.add_member(body.name):
        raise HTTPException(status_code=409, detail=f"Member '{body.name}' already exists")
    return {"message": f"Member '{body.name}' added", "members": city_hall.get_members()}


@app.delete("/community/members/{name}")
async def remove_member(name: str):
    if not city_hall.remove_member(name):
        raise HTTPException(status_code=404, detail=f"Member '{name}' not found")
    return {"message": f"Member '{name}' removed", "members": city_hall.get_members()}


@app.get("/community/announcements")
async def list_announcements():
    return {"announcements": city_hall.get_announcements()}


@app.post("/community/announcements")
async def make_announcement(body: AnnouncementBody):
    city_hall.make_announcement(body.text)
    return {"message": "Announcement posted", "announcements": city_hall.get_announcements()}


@app.get("/community/proposals")
async def list_proposals():
    return {"proposals": city_hall.get_proposals()}


@app.post("/community/proposals")
async def submit_proposal(body: ProposalBody):
    proposal_id = city_hall.submit_proposal(body.description)
    return {"message": "Proposal submitted", "proposal_id": proposal_id}


@app.post("/community/proposals/{proposal_id}/vote")
async def vote_on_proposal(proposal_id: int, body: VoteBody):
    if not city_hall.vote_on_proposal(proposal_id, vote_for=body.vote_for):
        raise HTTPException(status_code=404, detail=f"Proposal {proposal_id} not found")
    proposals = city_hall.get_proposals()
    return {"message": "Vote recorded", "proposal": proposals[proposal_id]}


# ---------------------------------------------------------------------------
# Categories / frameworks (static lists)
# ---------------------------------------------------------------------------


@app.get("/categories")
async def get_categories():
    return {
        "categories": [
            "Autonomous Agents",
            "Code Generation",
            "Data Analysis",
            "Web Automation",
            "NLP & Chat",
            "Workflow Automation",
            "Research & Development",
            "Testing & QA",
        ]
    }


@app.get("/frameworks")
async def get_frameworks():
    return {
        "frameworks": [
            "LangChain",
            "AutoGPT",
            "CrewAI",
            "OpenAI",
            "Anthropic Claude",
            "HuggingFace",
            "Custom",
        ]
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from sample_data import get_sample_agents, get_sample_projects
from cade_v3.orchestrator import Orchestrator
from cade_v3.models import Task, TaskType, TaskPriority
from cityhall import CityHall

load_dotenv()

# Subsystem singletons – shared across all requests
orchestrator = Orchestrator()
city_hall = CityHall("C-A-D-E Community")

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

class TaskSubmission(BaseModel):
    type: str  # plan | code | review | deploy | maintenance
    payload: Dict[str, Any]
    priority: str = "normal"  # low | normal | high | critical
    approved_by: Optional[str] = None  # required for deploy tasks

class MemberBody(BaseModel):
    name: str

class AnnouncementBody(BaseModel):
    text: str

class ProposalBody(BaseModel):
    description: str

class VoteBody(BaseModel):
    vote_for: bool = True

# In-memory storage (would be database in production)
# TODO: Replace with persistent database (PostgreSQL/MongoDB) for production use
# This in-memory storage is suitable for development and testing only
agents_db: Dict[str, Agent] = {}
projects_db: Dict[str, Project] = {}

_PRIORITY_MAP: Dict[str, TaskPriority] = {
    "low": TaskPriority.LOW,
    "normal": TaskPriority.NORMAL,
    "high": TaskPriority.HIGH,
    "critical": TaskPriority.CRITICAL,
}

_TYPE_MAP: Dict[str, TaskType] = {t.value: t for t in TaskType}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load sample data on application startup"""
    for agent_data in get_sample_agents():
        agents_db[agent_data["id"]] = Agent(**agent_data)

    for project_data in get_sample_projects():
        projects_db[project_data["id"]] = Project(**project_data)

    print(f"Loaded {len(agents_db)} sample agents")
    print(f"Loaded {len(projects_db)} sample projects")
    print("Orchestrator initialised with foundation agents")
    print("CityHall initialised for community governance")
    yield
    # Shutdown: cleanup resources like database connections, file handles, etc.

app = FastAPI(
    title="C-A-D-E API",
    description="Community Application Development Environment - AI Agent Platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------

@app.get("/")
async def root():
    return {
        "name": "C-A-D-E API",
        "version": "1.0.0",
        "description": "Community Application Development Environment",
        "status": "operational"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

# ---------------------------------------------------------------------------
# Dashboard stats – aggregates from all subsystems
# ---------------------------------------------------------------------------

@app.get("/dashboard/stats")
async def dashboard_stats():
    """Aggregate statistics from agents, projects, orchestrator, and community."""
    registry_agents = orchestrator.registry.list_all()
    memory_snap = orchestrator.memory.snapshot()
    return {
        "agents": {
            "total": len(agents_db),
            "categories": list({a.category for a in agents_db.values()}),
        },
        "projects": {
            "total": len(projects_db),
        },
        "orchestrator": {
            "foundation_agents": len(registry_agents),
            "agents_by_role": {
                role.value: orchestrator.registry.count(role)
                for role in orchestrator.registry._role_counts
            },
            "task_counts": dict(orchestrator._task_counter),
            "memory_topics": memory_snap,
            "monetization_recommendation": orchestrator.monetization_summary(),
        },
        "community": city_hall.get_info(),
    }

# ---------------------------------------------------------------------------
# Agent endpoints
# ---------------------------------------------------------------------------

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
    """Execute an agent by routing it through the CADE v3 orchestrator."""
    if execution.agent_id not in agents_db:
        raise HTTPException(status_code=404, detail="Agent not found")

    agent = agents_db[execution.agent_id]

    task = Task(
        type=TaskType.CODE,
        payload={"agent_id": execution.agent_id, "agent_name": agent.name, **execution.input_data},
        priority=TaskPriority.NORMAL,
    )
    orchestrator.submit(task)
    result = orchestrator.process_next()

    return {
        "message": "Agent executed via orchestrator",
        "agent_id": execution.agent_id,
        "task_id": task.id,
        "orchestrator_result": result,
        "status": "blocked" if result.startswith("blocked") else "success",
    }

# ---------------------------------------------------------------------------
# Project endpoints
# ---------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------
# Orchestrator endpoints
# ---------------------------------------------------------------------------

@app.get("/orchestrator/status")
async def orchestrator_status():
    """Return full orchestrator runtime state."""
    agents = [
        {
            "id": a.id,
            "role": a.role.value,
            "skills": a.skills,
            "status": a.status,
            "created_at": a.created_at.isoformat(),
        }
        for a in orchestrator.registry.list_all()
    ]
    return {
        "agents": agents,
        "task_counts": dict(orchestrator._task_counter),
        "memory_snapshot": orchestrator.memory.snapshot(),
        "monetization_recommendation": orchestrator.monetization_summary(),
    }

@app.post("/orchestrator/tasks")
async def submit_task(submission: TaskSubmission):
    """Submit a task to the orchestrator queue and process the next item."""
    task_type = _TYPE_MAP.get(submission.type.lower())
    if task_type is None:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown task type '{submission.type}'. Valid types: {list(_TYPE_MAP.keys())}"
        )
    priority = _PRIORITY_MAP.get(submission.priority.lower(), TaskPriority.NORMAL)

    task = Task(type=task_type, payload=submission.payload, priority=priority)
    orchestrator.submit(task)

    approval_context: Dict[str, str] = {}
    if submission.approved_by:
        approval_context["approved_by"] = submission.approved_by

    result = orchestrator.process_next(approval_context)
    return {
        "task_id": task.id,
        "type": task_type.value,
        "priority": priority.name.lower(),
        "orchestrator_result": result,
        "status": "blocked" if result.startswith("blocked") else "queued_and_processed",
    }

@app.get("/orchestrator/memory")
async def orchestrator_memory(topic: Optional[str] = None, limit: int = 10):
    """Query the orchestrator's shared memory."""
    if topic:
        entries = orchestrator.memory.query(topic, limit=limit)
    else:
        entries = orchestrator.memory.query("", limit=limit)
    return {
        "entries": [
            {
                "topic": e.topic,
                "content": e.content,
                "confidence": e.confidence,
                "created_at": e.created_at.isoformat(),
            }
            for e in entries
        ]
    }

# ---------------------------------------------------------------------------
# Community (CityHall) endpoints
# ---------------------------------------------------------------------------

@app.get("/community/info")
async def community_info():
    """Get community overview."""
    return city_hall.get_info()

@app.get("/community/members")
async def list_members():
    return {"members": city_hall.get_members()}

@app.post("/community/members")
async def add_member(body: MemberBody):
    added = city_hall.add_member(body.name)
    if not added:
        raise HTTPException(status_code=409, detail=f"Member '{body.name}' already exists")
    return {"message": f"Member '{body.name}' added", "members": city_hall.get_members()}

@app.delete("/community/members/{name}")
async def remove_member(name: str):
    removed = city_hall.remove_member(name)
    if not removed:
        raise HTTPException(status_code=404, detail=f"Member '{name}' not found")
    return {"message": f"Member '{name}' removed", "members": city_hall.get_members()}

@app.get("/community/announcements")
async def list_announcements():
    return {"announcements": city_hall.get_announcements()}

@app.post("/community/announcements")
async def make_announcement(body: AnnouncementBody):
    city_hall.make_announcement(body.text)
    return {"message": "Announcement posted", "announcements": city_hall.get_announcements()}

@app.get("/community/proposals")
async def list_proposals():
    return {"proposals": city_hall.get_proposals()}

@app.post("/community/proposals")
async def submit_proposal(body: ProposalBody):
    proposal_id = city_hall.submit_proposal(body.description)
    return {"message": "Proposal submitted", "proposal_id": proposal_id}

@app.post("/community/proposals/{proposal_id}/vote")
async def vote_on_proposal(proposal_id: int, body: VoteBody):
    success = city_hall.vote_on_proposal(proposal_id, vote_for=body.vote_for)
    if not success:
        raise HTTPException(status_code=404, detail=f"Proposal {proposal_id} not found")
    proposals = city_hall.get_proposals()
    return {"message": "Vote recorded", "proposal": proposals[proposal_id]}

# ---------------------------------------------------------------------------
# Categories and frameworks
# ---------------------------------------------------------------------------

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
