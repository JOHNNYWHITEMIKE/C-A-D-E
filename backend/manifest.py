"""
Manifest loader – reads agents/agents.yaml and upserts into the database.

The manifest path is read from the AGENTS_MANIFEST_PATH env var so it can
be overridden when running inside Docker (where the repo root is mounted
at /agents or similar).
"""
from __future__ import annotations

import os
import pathlib
from typing import Any, Dict, List

import yaml

_DEFAULT_PATH = pathlib.Path(__file__).parent.parent / "agents" / "agents.yaml"
MANIFEST_PATH = pathlib.Path(os.getenv("AGENTS_MANIFEST_PATH", str(_DEFAULT_PATH)))


def load_manifest() -> List[Dict[str, Any]]:
    """Return the raw list of agent dicts from agents.yaml."""
    if not MANIFEST_PATH.exists():
        print(f"WARNING: agents manifest not found at {MANIFEST_PATH}")
        return []
    with open(MANIFEST_PATH) as fh:
        data = yaml.safe_load(fh)
    return data.get("agents", [])


def manifest_agent_to_db(entry: Dict[str, Any]) -> Dict[str, Any]:
    """Normalise a manifest agent entry into the shape expected by crud.upsert_agent."""
    skills = entry.get("skills", [])
    caps = entry.get("capabilities", [])
    categories = entry.get("categories", [])

    # Map manifest categories to a single UI-facing category string
    cat_map = {
        "automation": "Web Automation",
        "data_science": "Data Analysis",
        "web_development": "Code Generation",
        "api_development": "Code Generation",
        "database": "Data Analysis",
        "devops": "Workflow Automation",
    }
    category = "Autonomous Agents"
    for c in categories:
        if c in cat_map:
            category = cat_map[c]
            break

    return {
        "id": entry["id"],
        "name": entry.get("name", entry["id"]),
        "description": entry.get("description", ""),
        "category": category,
        "framework": "Custom",
        "language": "Python",
        "code": "",
        "docker_image": entry.get("docker_image", ""),
        "local_image": entry.get("local_image", ""),
        "local_path": entry.get("local_path", ""),
        "available": entry.get("available", False),
        "source": "manifest",
        "skills": skills,
        "capabilities": caps,
    }
