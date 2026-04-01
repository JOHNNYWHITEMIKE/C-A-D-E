from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(slots=True)
class RevenueSignal:
    feature: str
    demand_score: float
    implementation_cost: float


class MonetizationAdvisor:
    """Prioritizes tasks with best creativity-to-revenue potential."""

    def score(self, signal: RevenueSignal) -> float:
        # Higher demand and lower cost means higher score.
        return round((signal.demand_score * 2.0) - signal.implementation_cost, 3)

    def recommend(self, signals: Dict[str, RevenueSignal]) -> str:
        if not signals:
            return "No monetization opportunities detected"
        ranked = sorted(signals.values(), key=self.score, reverse=True)
        best = ranked[0]
        return f"Prioritize '{best.feature}' (score={self.score(best)})"
