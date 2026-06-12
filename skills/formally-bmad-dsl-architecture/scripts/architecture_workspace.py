#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Create a DSL-branch architecture companion workspace."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


STARTER_FILES = {
    "architecture.md": (
        "# Architecture\n\n"
        "## Formal Status\n\n"
        "- Inherited baseline scope:\n"
        "- Inherited evidence posture:\n"
        "- New architecture-level deltas:\n"
        "- Recheck obligations:\n"
        "- Companion folder:\n\n"
    ),
    "design-decisions.md": (
        "# Design Decisions\n\n"
        "| Decision ID | Decision | Classification | Source Requirement IDs | Source Delta IDs | Validation Posture | Notes |\n"
        "| ----------- | -------- | -------------- | ---------------------- | ---------------- | ------------------ | ----- |\n"
    ),
    "architecture-deltas.md": (
        "# Architecture Deltas\n\n"
        "| Delta ID | Summary | Source Requirement IDs | Source Upstream Delta IDs | Ontology Impact | ASM Impact | Property Impact | Recheck Obligations | Validation Posture | Notes |\n"
        "| -------- | ------- | ---------------------- | ------------------------- | --------------- | ---------- | --------------- | ------------------- | ------------------ | ----- |\n"
    ),
    "architecture-validation-status.md": (
        "# Architecture Validation Status\n\n"
        "| Decision / Delta ID | Inherited Evidence Posture | New Validation Need | Backend Evidence Status | Risk Posture | Notes |\n"
        "| ------------------- | ------------------------- | ------------------- | ----------------------- | ------------ | ----- |\n"
    ),
    "ontology-refinement.md": (
        "# Ontology Refinement\n\n"
        "| Element | Refinement Type | Source Requirement IDs | Source Delta IDs | Status | Notes |\n"
        "| ------- | --------------- | ---------------------- | ---------------- | ------ | ----- |\n"
    ),
    "asm-refinement.md": (
        "# ASM Refinement\n\n"
        "| Element | Refinement Type | Source Requirement IDs | Source Delta IDs | Recheck Needed | Status | Notes |\n"
        "| ------- | --------------- | ---------------------- | ---------------- | -------------- | ------ | ----- |\n"
    ),
    "verification-obligations.md": (
        "# Verification Obligations\n\n"
        "| Obligation ID | Obligation | Inherited Or New | Triggered By | Recheck Needed | Downstream Artifact | Status | Notes |\n"
        "| ------------- | ---------- | ---------------- | ------------ | -------------- | ------------------- | ------ | ----- |\n"
    ),
    "provenance.md": (
        "# Provenance\n\n"
        "| Architecture Section | Decision / Delta ID | Source Requirement IDs | Source Upstream Delta IDs | Notes |\n"
        "| -------------------- | ------------------- | ---------------------- | ------------------------- | ----- |\n"
    ),
    "local-validation.md": (
        "# Local Validation\n\n"
        "## Baseline Intake Checks\n\n"
        "- Accepted PRD requirements loaded:\n"
        "- Accepted upstream deltas loaded:\n"
        "- Inherited ontology and ASM baseline references loaded:\n"
        "- Architecture-level recheck set identified:\n\n"
        "## Blockers And Repair Proposals\n\n"
    ),
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
    workspace = module_root / "artifacts" / "dsl-architecture" / safe_title
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
    parser = argparse.ArgumentParser(description="Create a DSL-branch architecture companion workspace.")
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
