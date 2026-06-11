#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Create Formally BMAD architecture companion workspace."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


STARTER_FILES = {
    "architecture.md": "# Architecture\n\n## Formal Status\n\n",
    "decisions.md": "# Architecture Decisions\n\n| ID | Decision | State | Source Section | Notes |\n| -- | -------- | ----- | -------------- | ----- |\n",
    "components.md": "# Components\n\n| Component | Responsibility | Constraints | Notes |\n| --------- | -------------- | ----------- | ----- |\n",
    "interfaces.md": "# Interfaces\n\n| Interface | Provider | Consumer | Contract | Notes |\n| --------- | -------- | -------- | -------- | ----- |\n",
    "constraints.md": "# Constraints and Invariants\n\n",
    "temporal-properties.md": "# Temporal Properties\n\n",
    "prd-alignment.md": "# PRD Alignment\n\n| Requirement | Architecture Support | Status | Notes |\n| ----------- | -------------------- | ------ | ----- |\n",
    "candidate-delta.md": "# Candidate Canonical Delta\n\n",
    "implementation-constraints.md": "# Implementation Constraints\n\n| Constraint | Applies To | Source Decision | Status |\n| ---------- | ---------- | --------------- | ------ |\n",
    "provenance.md": "# Provenance\n\n| Architecture Section | Assertion / Decision | State | Notes |\n| -------------------- | -------------------- | ----- | ----- |\n",
    "local-validation.md": "# Local Validation\n\n",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def resolve_path(raw: str, project_root: Path) -> Path:
    return Path(raw.replace("{project-root}", str(project_root))).expanduser().resolve()


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip().lower()).strip("-")
    return slug or "architecture"


def create_workspace(module_root: Path, title: str) -> dict[str, object]:
    safe_title = slugify(title)
    workspace = module_root / "artifacts" / "architecture" / safe_title
    workspace.mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    for name, content in STARTER_FILES.items():
        path = workspace / name
        if not path.exists():
            path.write_text(content, encoding="utf-8")
            created.append(str(path))
    manifest = {
        "generated_at": utc_now(),
        "title": title,
        "safe_title": safe_title,
        "workspace": str(workspace),
        "files": sorted(str(path) for path in workspace.iterdir() if path.is_file()),
    }
    (workspace / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest["created"] = created
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Formally BMAD architecture companion workspace.")
    parser.add_argument("--project-root", required=True, help="Project root directory.")
    parser.add_argument("--module-root", required=True, help="Formally BMAD project state directory.")
    parser.add_argument("--title", required=True, help="Architecture title or source slug.")
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

    result = create_workspace(module_root, args.title)
    output = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
