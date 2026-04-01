from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Optional
from uuid import uuid4

from .models import AgentRole, AgentSpec


class AgentRegistry:
    """Tracks agent lifecycle and specialization metadata."""

    def __init__(self) -> None:
        self._agents: Dict[str, AgentSpec] = {}
        self._role_counts: Dict[AgentRole, int] = defaultdict(int)

    def register(self, role: AgentRole, skills: List[str]) -> AgentSpec:
        agent_id = f"{role.value}-{uuid4()}"
        agent = AgentSpec(id=agent_id, role=role, skills=skills)
        self._agents[agent_id] = agent
        self._role_counts[role] += 1
        return agent

    def update_status(self, agent_id: str, status: str) -> None:
        if agent_id in self._agents:
            self._agents[agent_id].status = status

    def get_idle(self, role: AgentRole) -> List[AgentSpec]:
        return [agent for agent in self._agents.values() if agent.role == role and agent.status == "idle"]

    def count(self, role: Optional[AgentRole] = None) -> int:
        if role is None:
            return len(self._agents)
        return self._role_counts[role]

    def list_all(self) -> List[AgentSpec]:
        return list(self._agents.values())
