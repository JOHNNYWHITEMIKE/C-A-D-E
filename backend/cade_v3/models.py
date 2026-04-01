from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List
from uuid import uuid4


class TaskType(str, Enum):
    PLAN = "plan"
    CODE = "code"
    REVIEW = "review"
    DEPLOY = "deploy"
    MAINTENANCE = "maintenance"


class TaskPriority(int, Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class AgentRole(str, Enum):
    OVERSEER = "overseer"
    PLANNER = "planner"
    CODER = "coder"
    CRITIC = "critic"
    SECURITY = "security"
    MONETIZATION = "monetization"


@dataclass(slots=True)
class Task:
    type: TaskType
    payload: Dict[str, Any]
    priority: TaskPriority = TaskPriority.NORMAL
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(slots=True)
class AgentSpec:
    id: str
    role: AgentRole
    skills: List[str]
    status: str = "idle"
    created_at: datetime = field(default_factory=datetime.utcnow)
