"""
SQLAlchemy ORM models for C-A-D-E.

Tables
------
agents          – agent catalog (manifest + user-created)
projects        – project containers
project_agents  – many-to-many membership
executions      – every agent run, with status + captured logs
"""
from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class AgentRow(Base):
    __tablename__ = "agents"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    category: Mapped[str] = mapped_column(String, nullable=False)
    framework: Mapped[str] = mapped_column(String, nullable=False)
    language: Mapped[str] = mapped_column(String, nullable=False)
    code: Mapped[str] = mapped_column(Text, default="")
    # Manifest-backed fields
    docker_image: Mapped[str] = mapped_column(String, default="")
    local_image: Mapped[str] = mapped_column(String, default="")
    local_path: Mapped[str] = mapped_column(String, default="")
    available: Mapped[bool] = mapped_column(default=False)
    source: Mapped[str] = mapped_column(String, default="user")  # "manifest" | "user"
    skills: Mapped[str] = mapped_column(Text, default="")  # JSON-serialised list
    capabilities: Mapped[str] = mapped_column(Text, default="")  # JSON-serialised list
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    executions: Mapped[List["ExecutionRow"]] = relationship(
        "ExecutionRow", back_populates="agent", cascade="all, delete-orphan"
    )
    project_memberships: Mapped[List["ProjectAgentRow"]] = relationship(
        "ProjectAgentRow", back_populates="agent", cascade="all, delete-orphan"
    )


class ProjectRow(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    project_agents: Mapped[List["ProjectAgentRow"]] = relationship(
        "ProjectAgentRow", back_populates="project", cascade="all, delete-orphan"
    )


class ProjectAgentRow(Base):
    __tablename__ = "project_agents"

    project_id: Mapped[str] = mapped_column(
        String, ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True
    )
    agent_id: Mapped[str] = mapped_column(
        String, ForeignKey("agents.id", ondelete="CASCADE"), primary_key=True
    )

    project: Mapped["ProjectRow"] = relationship("ProjectRow", back_populates="project_agents")
    agent: Mapped["AgentRow"] = relationship("AgentRow", back_populates="project_memberships")


class ExecutionRow(Base):
    __tablename__ = "executions"

    id: Mapped[str] = mapped_column(String, primary_key=True)  # UUID, doubles as task_id
    agent_id: Mapped[str] = mapped_column(
        String, ForeignKey("agents.id", ondelete="CASCADE"), nullable=False
    )
    agent_name: Mapped[str] = mapped_column(String, default="")
    input_data: Mapped[dict] = mapped_column(JSONB, default=dict)
    status: Mapped[str] = mapped_column(String, default="pending")
    # "pending" | "running" | "completed" | "failed" | "simulated"
    logs: Mapped[str] = mapped_column(Text, default="")
    exit_code: Mapped[int] = mapped_column(Integer, default=-1)
    container_id: Mapped[str] = mapped_column(String, default="")
    orchestrator_result: Mapped[str] = mapped_column(Text, default="")
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    agent: Mapped["AgentRow"] = relationship("AgentRow", back_populates="executions")
