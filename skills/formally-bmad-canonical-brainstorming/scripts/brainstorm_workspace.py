#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Create a canonical-surface brainstorming workspace."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


STARTER_FILES = {
    "brainstorm.md": "# Brainstorm\n\n",
    "canonical-surface.md": (
        "# Canonical Surface\n\n"
        "## Scope\n\n"
        "## Concepts\n\n"
        "| Concept | Kind | State | Definition | Notes |\n"
        "| ------- | ---- | ----- | ---------- | ----- |\n\n"
        "## Relations\n\n"
        "| Subject | Relation | Object | Cardinality | State | Notes |\n"
        "| ------- | -------- | ------ | ----------- | ----- | ----- |\n\n"
        "## States\n\n"
        "| State | Parent State | Entry Condition | Exit Condition | Notes |\n"
        "| ----- | ------------ | --------------- | -------------- | ----- |\n\n"
        "## Events And Actions\n\n"
        "| Event / Action | Trigger | Effect | State | Notes |\n"
        "| -------------- | ------- | ------ | ----- | ----- |\n\n"
        "## Constraints And Invariants\n\n"
        "| Constraint / Invariant | Kind | State | Notes |\n"
        "| ---------------------- | ---- | ----- | ----- |\n\n"
        "## Assumptions\n\n"
        "| Assumption | State | Notes |\n"
        "| ---------- | ----- | ----- |\n\n"
        "## Alternatives\n\n"
        "| Alternative | Implication | Excludes | Promotion Condition | State |\n"
        "| ----------- | ----------- | -------- | ------------------- | ----- |\n\n"
        "## Open Questions\n\n"
        "| Question | Blocking Layer | Next Step |\n"
        "| -------- | -------------- | --------- |\n"
    ),
    "ontology-projection.md": (
        "# Ontology Projection\n\n"
        "Target language: OWL 2 DL\n\n"
        "## Classes\n\n"
        "| Class | Parent | State | Notes |\n"
        "| ----- | ------ | ----- | ----- |\n\n"
        "## Properties\n\n"
        "| Property | Kind | Domain | Range | State | Notes |\n"
        "| -------- | ---- | ------ | ----- | ----- | ----- |\n\n"
        "## Semantic Constraints\n\n"
        "| Constraint | OWL Shape | State | Notes |\n"
        "| ---------- | --------- | ----- | ----- |\n\n"
        "## Manchester Fragments\n\n"
    ),
    "system-model.md": (
        "# System Model\n\n"
        "Target semantics: restricted hierarchical typed EFSM\n\n"
        "## Control States\n\n"
        "| State | Parent | Kind | Invariant | Notes |\n"
        "| ----- | ------ | ---- | --------- | ----- |\n\n"
        "## Variables\n\n"
        "| Variable | Type | Initial Value | State | Notes |\n"
        "| -------- | ---- | ------------- | ----- | ----- |\n\n"
        "## Events\n\n"
        "| Event | Parameters | Source | Notes |\n"
        "| ----- | ---------- | ------ | ----- |\n\n"
        "## Transitions\n\n"
        "| From | Event | Guard | Effect | To | State | Notes |\n"
        "| ---- | ----- | ----- | ------ | -- | ----- | ----- |\n\n"
        "## Excluded Semantics\n\n"
        "- Unrestricted orthogonal concurrency\n"
        "- History pseudostates\n"
        "- Rich UML pseudostate machinery\n"
    ),
    "candidate-delta.md": "# Candidate Canonical Delta\n\n",
    "provenance.md": "# Provenance\n\n| Source Idea | Canonical Entry | Projection Impact | State | Notes |\n| ----------- | --------------- | ----------------- | ----- | ----- |\n",
    "local-validation.md": (
        "# Local Validation\n\n"
        "## Projection Drift Checks\n\n"
        "- Canonical surface updated:\n"
        "- Ontology projection synchronized:\n"
        "- System model synchronized:\n\n"
        "## Blockers\n\n"
    ),
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def resolve_path(raw: str, project_root: Path) -> Path:
    return Path(raw.replace("{project-root}", str(project_root))).expanduser().resolve()


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip().lower()).strip("-")
    return slug or "brainstorm"


def create_workspace(module_root: Path, topic: str) -> dict[str, object]:
    safe_topic = slugify(topic)
    workspace = module_root / "artifacts" / "brainstorming" / safe_topic
    workspace.mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    for name, content in STARTER_FILES.items():
        path = workspace / name
        if not path.exists():
            path.write_text(content, encoding="utf-8")
            created.append(str(path))
    manifest = {
        "generated_at": utc_now(),
        "topic": topic,
        "safe_topic": safe_topic,
        "workspace": str(workspace),
        "files": sorted(str(path) for path in workspace.iterdir() if path.is_file()),
    }
    (workspace / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest["created"] = created
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a canonical-surface brainstorming workspace.")
    parser.add_argument("--project-root", required=True, help="Project root directory.")
    parser.add_argument("--module-root", required=True, help="Formally BMAD project state directory.")
    parser.add_argument("--topic", required=True, help="Brainstorming topic or slug.")
    parser.add_argument("-o", "--output", help="Write JSON result to file instead of stdout.")
    args = parser.parse_args()

    project_root = resolve_path(args.project_root, Path.cwd())
    module_root = resolve_path(args.module_root, project_root)
    if not project_root.exists():
        print(f"Project root does not exist: {project_root}", file=sys.stderr)
        return 2
    if not module_root.exists():
        print(f"Module root does not exist: {module_root}", file=sys.stderr)
        return 2

    result = create_workspace(module_root, args.topic)
    output = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
