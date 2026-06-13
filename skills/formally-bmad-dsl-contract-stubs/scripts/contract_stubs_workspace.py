#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Create Formally BMAD DSL contract-stub companion workspace."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


STARTER_FILES = {
    "stubs.md": "# DSL Contract-Bearing Scaffolds\n\n## Formal Status\n\n",
    "contract-surface.md": "# Contract Surface Mapping\n\n| Contract ID | Target Scaffold Element | Placement | Fidelity | Notes |\n| ----------- | ----------------------- | --------- | -------- | ----- |\n",
    "file-plan.md": "# File and Module Plan\n\n| File / Module | Responsibility | Scaffold Elements | Notes |\n| ------------- | -------------- | ----------------- | ----- |\n",
    "scaffold-plan.md": "# Source-Tree Scaffold Plan\n\n| Target Path | Role | Status | Notes |\n| ----------- | ---- | ------ | ----- |\n",
    "review-checklist.md": "# Scaffold Review Checklist\n\n- [ ] Inferred layout is acceptable\n- [ ] Signatures match accepted obligations\n- [ ] Contract placement is correct\n- [ ] No business logic was filled in prematurely\n- [ ] Scaffold is approved for implementation\n",
    "provenance.md": "# Provenance\n\n| Source Contract | Scaffold Element | Notes |\n| --------------- | ---------------- | ----- |\n",
    "local-validation.md": "# Local Validation\n\n",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def resolve_path(raw: str, project_root: Path) -> Path:
    return Path(raw.replace("{project-root}", str(project_root))).expanduser().resolve()


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip().lower()).strip("-")
    return slug or "dsl-contract-stubs"


def create_workspace(module_root: Path, target: str) -> dict[str, object]:
    safe_target = slugify(target)
    workspace = module_root / "artifacts" / "dsl-contract-stubs" / safe_target
    workspace.mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    for name, content in STARTER_FILES.items():
        path = workspace / name
        if not path.exists():
            path.write_text(content, encoding="utf-8")
            created.append(str(path))
    manifest = {
        "generated_at": utc_now(),
        "target": target,
        "safe_target": safe_target,
        "workspace": str(workspace),
        "files": sorted(str(path) for path in workspace.iterdir() if path.is_file()),
    }
    (workspace / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest["created"] = created
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Formally BMAD DSL contract-stub companion workspace.")
    parser.add_argument("--project-root", required=True, help="Project root directory.")
    parser.add_argument("--module-root", required=True, help="Formally BMAD DSL project state directory.")
    parser.add_argument("--target", required=True, help="Story ID and language target.")
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

    result = create_workspace(module_root, args.target)
    output = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
