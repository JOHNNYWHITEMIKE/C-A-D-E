# CADE v3 Bootstrap (Local, Continuous, Open-Source)

This document defines the **implemented CADE v3 scaffold** in `backend/cade_v3/`.

## Goals

- Continuous orchestration loop with queue-based task routing
- Foundation agent community (overseer/planner/coder/critic/security/monetization)
- Policy guardrails for high-risk autonomy
- Shared memory for cross-agent learning
- Monetization advisor hook for product prioritization
- Workload-triggered specialization (spawn extra planners/coders)

## Implemented Modules

- `models.py`: Task, agent roles, and priorities.
- `registry.py`: Agent registration and status tracking.
- `memory.py`: Shared append-only memory with topic snapshots.
- `policies.py`: Governance policy checks (deploy approvals, self-modification blocks).
- `monetization.py`: Revenue scoring and recommendation helper.
- `orchestrator.py`: Main CADE v3 orchestration with auto-specialization and policy-aware execution.

## Run a Local Dry Run

From repository root:

```bash
python -m backend.cade_v3.orchestrator
```

Expected behavior:

1. Initializes foundation agents.
2. Executes high-priority planning/coding tasks.
3. Blocks deploy until approval context is provided.
4. Prints monetization recommendation.

## Next Extensions

- Replace in-memory queue with Redis/NATS.
- Route CODE tasks to Codex/local model executor.
- Add containerized worker runtime per task.
- Persist memory/metrics to vector DB + SQL.
- Add signed policy approvals for production deploys.
