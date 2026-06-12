#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Create a DSL-branch verification report workspace."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


STARTER_FILES = {
    "checkpoint-verification.md": "# Checkpoint Verification\n\n",
    "baseline-audit.md": "# Baseline Audit\n\n",
    "increment-validation-audit.md": "# Increment Validation Audit\n\n",
    "rechecks.md": "# Recheck Obligations Review\n\n",
    "readiness.md": "# Implementation Readiness\n\nStatus: `not-assessed`\n\n",
    "traceability-audit.md": "# Traceability Audit\n\n",
    "contradictions.md": "# Contradictions and Repair Needs\n\n",
    "coverage.md": "# Formal Coverage\n\n",
    "repair-review.md": "# Repair Review\n\n",
    "summary.md": "# Verification Summary\n\n",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def resolve_path(raw: str, project_root: Path) -> Path:
    return Path(raw.replace("{project-root}", str(project_root))).expanduser().resolve()


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip().lower()).strip("-")
    return slug or "verification"


def index_companions(module_root: Path) -> list[dict[str, str]]:
    artifacts_root = module_root / "artifacts"
    if not artifacts_root.exists():
        return []
    companions: list[dict[str, str]] = []
    for path in sorted(artifacts_root.rglob("manifest.json")):
        companions.append(
            {
                "kind": path.parent.parent.name if path.parent.parent != artifacts_root else path.parent.name,
                "workspace": str(path.parent),
                "manifest": str(path),
            }
        )
    return companions


def create_workspace(module_root: Path, scope: str) -> dict[str, object]:
    generated_at = utc_now()
    stamp = generated_at.replace(":", "").replace("-", "").replace("Z", "Z")
    safe_scope = slugify(scope)
    workspace = module_root / "reports" / "dsl-verification" / f"{stamp}-{safe_scope}"
    workspace.mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    for name, content in STARTER_FILES.items():
        path = workspace / name
        if not path.exists():
            path.write_text(content, encoding="utf-8")
            created.append(str(path))
    companions = index_companions(module_root)
    manifest = {
        "generated_at": generated_at,
        "scope": scope,
        "safe_scope": safe_scope,
        "workspace": str(workspace),
        "companions": companions,
        "files": sorted(str(path) for path in workspace.iterdir() if path.is_file()),
    }
    (workspace / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    latest = module_root / "reports" / "latest-dsl-verification-summary.md"
    latest.write_text(
        "# Latest DSL Verification Summary\n\n"
        f"- Generated: `{generated_at}`\n"
        f"- Scope: `{scope}`\n"
        f"- Report workspace: `{workspace}`\n"
        "- Status: `not-assessed`\n",
        encoding="utf-8",
    )
    manifest["created"] = created
    manifest["latest_summary"] = str(latest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a DSL-branch verification report workspace.")
    parser.add_argument("--project-root", required=True, help="Project root directory.")
    parser.add_argument("--module-root", required=True, help="Formally BMAD project state directory.")
    parser.add_argument("--scope", default="whole-dsl-branch", help="Verification scope label.")
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

    result = create_workspace(module_root, args.scope)
    output = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
