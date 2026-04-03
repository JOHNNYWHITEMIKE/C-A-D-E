"""
Async CRUD helpers for C-A-D-E database operations.

All functions accept an AsyncSession and return ORM rows or plain values.
They do NOT commit on their own – callers decide when to commit.
Exception: helpers that are self-contained use an explicit commit.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db_models import AgentRow, ExecutionRow, ProjectAgentRow, ProjectRow

# ---------------------------------------------------------------------------
# Agents
# ---------------------------------------------------------------------------


def _row_to_agent_dict(row: AgentRow) -> Dict[str, Any]:
    return {
        "id": row.id,
        "name": row.name,
        "description": row.description,
        "category": row.category,
        "framework": row.framework,
        "language": row.language,
        "code": row.code,
        "docker_image": row.docker_image,
        "local_image": row.local_image,
        "local_path": row.local_path,
        "available": row.available,
        "source": row.source,
        "skills": json.loads(row.skills) if row.skills else [],
        "capabilities": json.loads(row.capabilities) if row.capabilities else [],
        "created_at": row.created_at.isoformat() if row.created_at else None,
        "updated_at": row.updated_at.isoformat() if row.updated_at else None,
    }


async def list_agents(db: AsyncSession) -> List[Dict[str, Any]]:
    result = await db.execute(select(AgentRow).order_by(AgentRow.created_at))
    return [_row_to_agent_dict(r) for r in result.scalars().all()]


async def get_agent(db: AsyncSession, agent_id: str) -> Optional[AgentRow]:
    result = await db.execute(select(AgentRow).where(AgentRow.id == agent_id))
    return result.scalar_one_or_none()


async def upsert_agent(db: AsyncSession, data: Dict[str, Any]) -> AgentRow:
    """Insert or update an agent row (used by manifest sync and user creation)."""
    existing = await get_agent(db, data["id"])
    skills_json = json.dumps(data.get("skills", []))
    caps_json = json.dumps(data.get("capabilities", []))

    if existing:
        for key, value in {
            "name": data.get("name", existing.name),
            "description": data.get("description", existing.description),
            "category": data.get("category", existing.category),
            "framework": data.get("framework", existing.framework),
            "language": data.get("language", existing.language),
            "code": data.get("code", existing.code),
            "docker_image": data.get("docker_image", existing.docker_image),
            "local_image": data.get("local_image", existing.local_image),
            "local_path": data.get("local_path", existing.local_path),
            "available": data.get("available", existing.available),
            "source": data.get("source", existing.source),
            "skills": skills_json,
            "capabilities": caps_json,
        }.items():
            setattr(existing, key, value)
        await db.commit()
        await db.refresh(existing)
        return existing

    row = AgentRow(
        id=data["id"],
        name=data.get("name", ""),
        description=data.get("description", ""),
        category=data.get("category", ""),
        framework=data.get("framework", "Custom"),
        language=data.get("language", "Python"),
        code=data.get("code", ""),
        docker_image=data.get("docker_image", ""),
        local_image=data.get("local_image", ""),
        local_path=data.get("local_path", ""),
        available=data.get("available", False),
        source=data.get("source", "user"),
        skills=skills_json,
        capabilities=caps_json,
    )
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return row


async def delete_agent(db: AsyncSession, agent_id: str) -> bool:
    row = await get_agent(db, agent_id)
    if not row:
        return False
    await db.delete(row)
    await db.commit()
    return True


async def count_agents(db: AsyncSession) -> int:
    result = await db.execute(select(func.count()).select_from(AgentRow))
    return result.scalar_one()


async def distinct_categories(db: AsyncSession) -> List[str]:
    result = await db.execute(select(AgentRow.category).distinct())
    return result.scalars().all()


# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------


def _row_to_project_dict(row: ProjectRow) -> Dict[str, Any]:
    return {
        "id": row.id,
        "name": row.name,
        "description": row.description,
        "agents": [pa.agent_id for pa in row.project_agents],
        "created_at": row.created_at.isoformat() if row.created_at else None,
    }


async def list_projects(db: AsyncSession) -> List[Dict[str, Any]]:
    result = await db.execute(
        select(ProjectRow)
        .options(selectinload(ProjectRow.project_agents))
        .order_by(ProjectRow.created_at)
    )
    return [_row_to_project_dict(r) for r in result.scalars().all()]


async def get_project(db: AsyncSession, project_id: str) -> Optional[ProjectRow]:
    result = await db.execute(
        select(ProjectRow)
        .options(selectinload(ProjectRow.project_agents))
        .where(ProjectRow.id == project_id)
    )
    return result.scalar_one_or_none()


async def create_project(
    db: AsyncSession,
    project_id: str,
    name: str,
    description: str,
    agent_ids: List[str],
) -> Dict[str, Any]:
    row = ProjectRow(id=project_id, name=name, description=description)
    db.add(row)
    for aid in agent_ids:
        db.add(ProjectAgentRow(project_id=project_id, agent_id=aid))
    await db.commit()
    refreshed = await get_project(db, project_id)
    return _row_to_project_dict(refreshed)


async def update_project_agents(
    db: AsyncSession, project_id: str, agent_ids: List[str]
) -> Optional[Dict[str, Any]]:
    row = await get_project(db, project_id)
    if not row:
        return None
    # Replace membership set
    for pa in list(row.project_agents):
        await db.delete(pa)
    await db.flush()
    for aid in agent_ids:
        db.add(ProjectAgentRow(project_id=project_id, agent_id=aid))
    await db.commit()
    refreshed = await get_project(db, project_id)
    return _row_to_project_dict(refreshed)


async def delete_project(db: AsyncSession, project_id: str) -> bool:
    row = await get_project(db, project_id)
    if not row:
        return False
    await db.delete(row)
    await db.commit()
    return True


async def count_projects(db: AsyncSession) -> int:
    result = await db.execute(select(func.count()).select_from(ProjectRow))
    return result.scalar_one()


# ---------------------------------------------------------------------------
# Executions
# ---------------------------------------------------------------------------


def _row_to_execution_dict(row: ExecutionRow) -> Dict[str, Any]:
    return {
        "id": row.id,
        "agent_id": row.agent_id,
        "agent_name": row.agent_name,
        "input_data": row.input_data,
        "status": row.status,
        "logs": row.logs,
        "exit_code": row.exit_code,
        "container_id": row.container_id,
        "orchestrator_result": row.orchestrator_result,
        "started_at": row.started_at.isoformat() if row.started_at else None,
        "finished_at": row.finished_at.isoformat() if row.finished_at else None,
    }


async def create_execution(
    db: AsyncSession,
    execution_id: str,
    agent_id: str,
    agent_name: str,
    input_data: Dict[str, Any],
    orchestrator_result: str = "",
) -> ExecutionRow:
    row = ExecutionRow(
        id=execution_id,
        agent_id=agent_id,
        agent_name=agent_name,
        input_data=input_data,
        status="pending",
        orchestrator_result=orchestrator_result,
    )
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return row


async def update_execution(
    db: AsyncSession,
    execution_id: str,
    *,
    status: Optional[str] = None,
    logs: Optional[str] = None,
    exit_code: Optional[int] = None,
    container_id: Optional[str] = None,
    orchestrator_result: Optional[str] = None,
    finished_at: Optional[datetime] = None,
) -> Optional[ExecutionRow]:
    result = await db.execute(
        select(ExecutionRow).where(ExecutionRow.id == execution_id)
    )
    row = result.scalar_one_or_none()
    if not row:
        return None
    if status is not None:
        row.status = status
    if logs is not None:
        row.logs = logs
    if exit_code is not None:
        row.exit_code = exit_code
    if container_id is not None:
        row.container_id = container_id
    if orchestrator_result is not None:
        row.orchestrator_result = orchestrator_result
    if finished_at is not None:
        row.finished_at = finished_at
    await db.commit()
    await db.refresh(row)
    return row


async def get_execution(
    db: AsyncSession, execution_id: str
) -> Optional[Dict[str, Any]]:
    result = await db.execute(
        select(ExecutionRow).where(ExecutionRow.id == execution_id)
    )
    row = result.scalar_one_or_none()
    return _row_to_execution_dict(row) if row else None


async def list_executions(
    db: AsyncSession,
    agent_id: Optional[str] = None,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    stmt = select(ExecutionRow).order_by(ExecutionRow.started_at.desc()).limit(limit)
    if agent_id:
        stmt = stmt.where(ExecutionRow.agent_id == agent_id)
    result = await db.execute(stmt)
    return [_row_to_execution_dict(r) for r in result.scalars().all()]


async def count_executions(
    db: AsyncSession, status: Optional[str] = None
) -> int:
    stmt = select(func.count()).select_from(ExecutionRow)
    if status:
        stmt = stmt.where(ExecutionRow.status == status)
    result = await db.execute(stmt)
    return result.scalar_one()
