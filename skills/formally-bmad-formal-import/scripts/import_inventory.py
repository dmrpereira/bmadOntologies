#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Discover BMad Markdown artifacts for Formally BMAD import."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


KIND_PATTERNS = [
    ("brainstorming", re.compile(r"brainstorm|ideat|discovery", re.IGNORECASE)),
    ("prd", re.compile(r"\bprd\b|product[-_ ]?requirements?", re.IGNORECASE)),
    ("architecture", re.compile(r"architecture|architectural|system[-_ ]?design", re.IGNORECASE)),
    ("epic", re.compile(r"\bepic\b|epics", re.IGNORECASE)),
    ("story", re.compile(r"\bstory\b|stories|story-\d", re.IGNORECASE)),
    ("readiness", re.compile(r"readiness|implementation[-_ ]?ready", re.IGNORECASE)),
    ("verification", re.compile(r"verification|validation|formal[-_ ]?check", re.IGNORECASE)),
]

EXCLUDED_PARTS = {
    ".git",
    ".agents",
    ".claude",
    ".venv",
    "__pycache__",
    "node_modules",
    "exports",
    "tool-runs",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def resolve_path(raw: str, project_root: Path) -> Path:
    return Path(raw.replace("{project-root}", str(project_root))).expanduser().resolve()


def safe_source_id(relative_path: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9._-]+", "-", relative_path.replace("/", "__"))
    return normalized.strip("-") or "artifact"


def classify_kind(path: Path, project_root: Path) -> str:
    rel = str(path.relative_to(project_root))
    haystack = f"{rel}\n{path.name}"
    for kind, pattern in KIND_PATTERNS:
        if pattern.search(haystack):
            return kind
    return "unsupported"


def should_exclude(path: Path, project_root: Path, module_root: Path) -> bool:
    if module_root in path.parents or path == module_root:
        return True
    try:
        relative = path.relative_to(project_root)
    except ValueError:
        return True
    return any(part in EXCLUDED_PARTS for part in relative.parts)


def discover_markdown(project_root: Path, module_root: Path) -> list[dict[str, str]]:
    artifacts: list[dict[str, str]] = []
    for path in sorted(project_root.rglob("*.md")):
        if not path.is_file() or should_exclude(path, project_root, module_root):
            continue
        relative = str(path.relative_to(project_root))
        kind = classify_kind(path, project_root)
        artifacts.append({
            "path": relative,
            "kind_hint": kind,
            "safe_source_id": safe_source_id(relative),
        })
    return artifacts


def write_report(report_path: Path, result: dict[str, object]) -> None:
    artifacts = result["artifacts"]
    lines = [
        "# Formally BMAD Import Report",
        "",
        f"- Generated: `{result['generated_at']}`",
        f"- Project root: `{result['project_root']}`",
        f"- Module root: `{result['module_root']}`",
        f"- Candidate artifacts: `{len(artifacts)}`",
        "",
        "## Inventory",
        "",
        "| Source | Kind Hint | Safe Source ID |",
        "| ------ | --------- | -------------- |",
    ]
    for artifact in artifacts:
        lines.append(f"| `{artifact['path']}` | `{artifact['kind_hint']}` | `{artifact['safe_source_id']}` |")
    lines.extend([
        "",
        "## Import Findings",
        "",
        "Semantic classification, candidate assertions, provenance, steward response, and blockers are completed by the import workflow.",
    ])
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory Markdown artifacts for Formally BMAD formal import.")
    parser.add_argument("--project-root", required=True, help="Project root directory.")
    parser.add_argument("--module-root", required=True, help="Formally BMAD project state directory.")
    parser.add_argument("-o", "--output", help="Write JSON result to file instead of stdout.")
    parser.add_argument("--verbose", action="store_true", help="Emit diagnostics to stderr.")
    args = parser.parse_args()

    project_root = resolve_path(args.project_root, Path.cwd())
    module_root = resolve_path(args.module_root, project_root)

    if not project_root.exists():
        print(f"Project root does not exist: {project_root}", file=sys.stderr)
        return 2
    if not module_root.exists():
        print(f"Module root does not exist: {module_root}", file=sys.stderr)
        return 2

    import_root = module_root / "artifacts" / "import"
    reports_root = module_root / "reports"
    import_root.mkdir(parents=True, exist_ok=True)
    reports_root.mkdir(parents=True, exist_ok=True)

    artifacts = discover_markdown(project_root, module_root)
    result: dict[str, object] = {
        "generated_at": utc_now(),
        "status": "complete",
        "project_root": str(project_root),
        "module_root": str(module_root),
        "import_root": str(import_root),
        "artifacts": artifacts,
        "report_path": str(reports_root / "import-report.md"),
        "inventory_path": str(import_root / "inventory.json"),
    }

    Path(result["inventory_path"]).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_report(Path(result["report_path"]), result)

    output = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
