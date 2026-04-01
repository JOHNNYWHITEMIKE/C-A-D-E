from __future__ import annotations

from collections import Counter
from queue import PriorityQueue
from typing import Dict, List

from .memory import SharedMemory
from .models import AgentRole, Task, TaskPriority, TaskType
from .monetization import MonetizationAdvisor, RevenueSignal
from .policies import PolicyEngine
from .registry import AgentRegistry


class Orchestrator:
    """CADE v3 core loop with scaling, guardrails, and monetization hooks."""

    def __init__(self) -> None:
        self.registry = AgentRegistry()
        self.memory = SharedMemory()
        self.policies = PolicyEngine()
        self.monetization = MonetizationAdvisor()
        self.queue: PriorityQueue[tuple[int, int, Task]] = PriorityQueue()
        self._task_counter: Counter[str] = Counter()
        self._sequence = 0

        self._bootstrap_foundation_agents()

    def _bootstrap_foundation_agents(self) -> None:
        self.registry.register(AgentRole.OVERSEER, ["routing", "governance"])
        self.registry.register(AgentRole.PLANNER, ["decomposition", "estimation"])
        self.registry.register(AgentRole.CODER, ["python", "api"])
        self.registry.register(AgentRole.CRITIC, ["quality", "tests"])
        self.registry.register(AgentRole.SECURITY, ["threat-modeling", "hardening"])
        self.registry.register(AgentRole.MONETIZATION, ["pricing", "packaging"])

    def submit(self, task: Task) -> None:
        self._sequence += 1
        self.queue.put((-int(task.priority), self._sequence, task))
        self._task_counter[task.type.value] += 1
        self._auto_specialize()

    def _auto_specialize(self) -> None:
        """Spawn additional coders or planners based on sustained load."""
        code_load = self._task_counter[TaskType.CODE.value]
        plan_load = self._task_counter[TaskType.PLAN.value]

        if code_load >= 8 and self.registry.count(AgentRole.CODER) < 3:
            self.registry.register(AgentRole.CODER, ["frontend", "rapid-prototyping"])
            self.memory.add("scaling", "Spawned specialist coder for sustained code load")

        if plan_load >= 5 and self.registry.count(AgentRole.PLANNER) < 2:
            self.registry.register(AgentRole.PLANNER, ["architecture", "backlog-prioritization"])
            self.memory.add("scaling", "Spawned planner for backlog pressure")

    def process_next(self, approval_context: Dict[str, str] | None = None) -> str:
        if self.queue.empty():
            return "idle"

        _, _, task = self.queue.get()
        approval_context = approval_context or {}

        if task.type == TaskType.DEPLOY:
            allowed, message = self.policies.validate_action("deploy_prod", approval_context)
            if not allowed:
                self.memory.add("policy", message, confidence=1.0)
                return f"blocked: {message}"

        if task.type == TaskType.MAINTENANCE and task.payload.get("action") == "self_modify":
            allowed, message = self.policies.validate_action("self_modify", approval_context)
            if not allowed:
                return f"blocked: {message}"

        self.memory.add(task.type.value, f"Completed task {task.id}")
        return f"completed:{task.type.value}:{task.id}"

    def monetization_summary(self) -> str:
        signals = {
            "plugin_marketplace": RevenueSignal("plugin marketplace", 8.4, 3.2),
            "managed_hosting": RevenueSignal("managed hosting", 7.8, 5.0),
            "template_pack": RevenueSignal("template pack", 6.9, 2.0),
        }
        return self.monetization.recommend(signals)


if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.submit(Task(type=TaskType.PLAN, payload={"goal": "build CADE v3"}, priority=TaskPriority.HIGH))
    orchestrator.submit(Task(type=TaskType.CODE, payload={"goal": "implement orchestrator"}, priority=TaskPriority.HIGH))
    orchestrator.submit(Task(type=TaskType.DEPLOY, payload={"env": "prod"}, priority=TaskPriority.CRITICAL))

    print(orchestrator.process_next())
    print(orchestrator.process_next())
    print(orchestrator.process_next())
    print(orchestrator.monetization_summary())
