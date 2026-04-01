from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable


@dataclass(slots=True)
class GovernancePolicy:
    allow_self_modification: bool = False
    require_human_approval_for_deploy: bool = True
    max_parallel_coders: int = 4


class PolicyEngine:
    """Guardrails for risky actions in autonomous mode."""

    def __init__(self, policy: GovernancePolicy | None = None) -> None:
        self.policy = policy or GovernancePolicy()

    def validate_action(self, action: str, context: Dict[str, str]) -> tuple[bool, str]:
        if action == "self_modify" and not self.policy.allow_self_modification:
            return False, "Self modification blocked by governance policy"
        if action == "deploy_prod" and self.policy.require_human_approval_for_deploy:
            approver = context.get("approved_by", "")
            if not approver:
                return False, "Production deploy requires explicit approval"
        return True, "allowed"

    def throttle(self, active_coders: Iterable[str]) -> bool:
        return len(list(active_coders)) <= self.policy.max_parallel_coders
