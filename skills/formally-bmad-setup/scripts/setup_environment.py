#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Initialize Formally BMAD project state and detect reasoning tools."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


SUPPORTED_TOOLS = {
    "smt": ["z3", "cvc5", "cvc4"],
    "first_order": ["vampire", "eprover", "prover9", "mace4"],
    "sat": ["kissat", "cadical", "minisat", "glucose"],
    "temporal": ["tlc", "apalache", "alloy"],
    "ontology": ["robot", "hermit", "elk", "jfact", "factplusplus", "pellet"],
}

PROOF_ASSISTANTS = ["coqc", "rocq", "lean", "lake", "isabelle"]

SPECIALIZED_TOOLS = {
    "temporal_satisfiability": ["black"],
    "ontology_workbench": ["robot"],
    "python_contract_verification": ["crosshair"],
    "c_contract_verification": ["frama-c", "cbmc"],
    "rust_contract_verification": ["cargo-kani", "prusti-rustc", "cargo-creusot"],
}

DEFAULT_EXTRA_TOOL_DIRS = [
    "/private/tmp/black-install/bin",
    "/private/tmp/robot/bin",
]

BMAD_ARTIFACT_PATTERNS = [
    "*brainstorm*.md",
    "*prd*.md",
    "*architecture*.md",
    "*epic*.md",
    "*story*.md",
    "*readiness*.md",
    "*verification*.md",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def resolve_path(raw: str, project_root: Path) -> Path:
    return Path(raw.replace("{project-root}", str(project_root))).expanduser().resolve()


def resolve_tool_search_dirs() -> list[str]:
    configured = os.environ.get("FORMALLY_BMAD_EXTRA_TOOL_DIRS", "")
    configured_dirs = [part for part in configured.split(os.pathsep) if part]
    candidate_dirs = configured_dirs + DEFAULT_EXTRA_TOOL_DIRS
    return [directory for directory in candidate_dirs if Path(directory).is_dir()]


def build_tool_search_path(extra_dirs: list[str]) -> str:
    path_parts = extra_dirs + [os.environ.get("PATH", "")]
    return os.pathsep.join(part for part in path_parts if part)


def detect_tool(name: str, search_path: str | None = None) -> dict[str, object]:
    path = shutil.which(name, path=search_path)
    result: dict[str, object] = {"name": name, "available": bool(path), "path": path}
    if not path:
        return result

    version_args = ([path, "--version"], [path, "-version"], [path, "-h"])
    for args in version_args:
        try:
            completed = subprocess.run(args, capture_output=True, text=True, timeout=5, check=False)
        except (OSError, subprocess.TimeoutExpired):
            continue
        output = (completed.stdout or completed.stderr).strip().splitlines()
        result["version_probe"] = " ".join(args[1:])
        result["version"] = output[0] if output else ""
        result["smoke_exit_code"] = completed.returncode
        return result
    result["version"] = ""
    result["smoke_exit_code"] = None
    return result


def discover_artifacts(project_root: Path) -> list[dict[str, str]]:
    seen: set[Path] = set()
    artifacts: list[dict[str, str]] = []
    ignored_parts = {".git", ".agents", ".claude", "node_modules", ".venv", "__pycache__"}
    for pattern in BMAD_ARTIFACT_PATTERNS:
        for path in project_root.rglob(pattern):
            if any(part in ignored_parts for part in path.parts):
                continue
            if path in seen or not path.is_file():
                continue
            seen.add(path)
            artifacts.append({"path": str(path.relative_to(project_root)), "kind_hint": pattern})
    return sorted(artifacts, key=lambda item: item["path"])


def ensure_structure(module_root: Path, canonical_path: Path) -> list[str]:
    folders = [
        canonical_path / "model",
        canonical_path / "ontology",
        canonical_path / "temporal",
        canonical_path / "meta",
        canonical_path / "versions",
        module_root / "artifacts" / "brainstorming",
        module_root / "artifacts" / "prd",
        module_root / "artifacts" / "architecture",
        module_root / "artifacts" / "epics",
        module_root / "artifacts" / "stories",
        module_root / "artifacts" / "contracts",
        module_root / "artifacts" / "stubs",
        module_root / "exports",
        module_root / "reports",
        module_root / "provenance",
        module_root / "indexes",
        module_root / "tool-runs",
    ]
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)

    created = [str(folder) for folder in folders]
    status = canonical_path / "status.md"
    if not status.exists():
        status.write_text(
            "---\n"
            "status: initialized\n"
            f"updated: {utc_now()}\n"
            "---\n\n"
            "# Formally BMAD Canonical Model Status\n\n"
            "Setup initialized the canonical model structure. Validation is not active until at least one supported automated reasoning tool is confirmed.\n",
            encoding="utf-8",
        )
    override_ledger = module_root / "provenance" / "contradiction-override-ledger.md"
    if not override_ledger.exists():
        override_ledger.write_text("# Contradiction and Override Ledger\n\nNo overrides recorded.\n", encoding="utf-8")
    index = module_root / "indexes" / "index.md"
    if not index.exists():
        index.write_text("# Formally BMAD Index\n\nInitialized by setup.\n", encoding="utf-8")
    return created


def write_report(module_root: Path, result: dict[str, object]) -> Path:
    report_path = module_root / "reports" / "setup-report.md"
    tools = result["tools"]
    specialized_tools = result["specialized_tools"]
    proof_assistants = result["proof_assistants_detected"]
    available = [
        f"- `{tool['name']}` ({family}) at `{tool['path']}`"
        for family, entries in tools.items()
        for tool in entries
        if tool["available"]
    ]
    missing = [
        f"- `{tool['name']}` ({family})"
        for family, entries in tools.items()
        for tool in entries
        if not tool["available"]
    ]
    available_specialized = [
        f"- `{tool['name']}` ({family}) at `{tool['path']}`"
        for family, entries in specialized_tools.items()
        for tool in entries
        if tool["available"]
    ]
    available_proof_assistants = [
        f"- `{tool['name']}` at `{tool['path']}`"
        for tool in proof_assistants
        if tool["available"]
    ]
    report_path.write_text(
        "# Formally BMAD Setup Report\n\n"
        f"- Generated: `{result['generated_at']}`\n"
        f"- Status: `{result['status']}`\n"
        f"- Project root: `{result['project_root']}`\n"
        f"- Module root: `{result['module_root']}`\n"
        f"- Canonical path: `{result['canonical_path']}`\n"
        f"- Supported tools available: `{result['available_tool_count']}`\n\n"
        "## Tool Search Paths\n\n"
        + (
            "\n".join(f"- `{directory}`" for directory in result["tool_search_dirs"])
            if result["tool_search_dirs"]
            else "No extra tool directories configured."
        )
        + "\n\n"
        "## Baseline Validation Gate\n\n"
        f"- SMT solver available: `{result['baseline_validation']['has_smt']}`\n"
        f"- First-order or SAT solver available: `{result['baseline_validation']['has_first_order_or_sat']}`\n"
        f"- Baseline satisfied: `{result['baseline_validation']['baseline_satisfied']}`\n\n"
        "## Available Tools\n\n"
        + ("\n".join(available) if available else "None detected.")
        + "\n\n## Specialized Tooling\n\n"
        + ("\n".join(available_specialized) if available_specialized else "No specialized tools detected.")
        + "\n\n## Proof Assistants\n\n"
        + ("\n".join(available_proof_assistants) if available_proof_assistants else "No proof assistants detected.")
        + "\n\n## Missing Supported Tools\n\n"
        + ("\n".join(missing) if missing else "No supported tools missing from the known list.")
        + "\n\n## BMad Artifact Candidates\n\n"
        + (
            "\n".join(f"- `{item['path']}` ({item['kind_hint']})" for item in result["artifacts"])
            if result["artifacts"]
            else "No candidate BMad artifacts detected."
        )
        + "\n\n## Setup Guidance\n\n"
        + str(result["guidance"])
        + "\n",
        encoding="utf-8",
    )
    return report_path


def has_available_tool(entries: list[dict[str, object]]) -> bool:
    return any(bool(tool["available"]) for tool in entries)


def evaluate_baseline_validation(tools: dict[str, list[dict[str, object]]]) -> dict[str, bool]:
    has_smt = has_available_tool(tools["smt"])
    has_first_order_or_sat = has_available_tool(tools["first_order"]) or has_available_tool(tools["sat"])
    return {
        "has_smt": has_smt,
        "has_first_order_or_sat": has_first_order_or_sat,
        "baseline_satisfied": has_smt and has_first_order_or_sat,
    }


def build_guidance(
    baseline_validation: dict[str, bool],
    available_tool_count: int,
    min_required_tools: int,
) -> str:
    if not baseline_validation["has_smt"] and not baseline_validation["has_first_order_or_sat"]:
        return (
            "Install at least one SMT solver and at least one first-order or SAT solver, then rerun setup. "
            "Supported examples include z3 or cvc5 for SMT, and vampire, eprover, kissat, or minisat for the second baseline class."
        )
    if not baseline_validation["has_smt"]:
        return (
            "Install at least one SMT solver, then rerun setup. "
            "Supported examples include z3, cvc5, and cvc4."
        )
    if not baseline_validation["has_first_order_or_sat"]:
        return (
            "Install at least one first-order or SAT solver, then rerun setup. "
            "Supported examples include vampire, eprover, prover9, kissat, cadical, minisat, and glucose."
        )
    if available_tool_count < min_required_tools:
        return (
            f"Baseline validation tooling is available, but setup requires at least {min_required_tools} supported tools in total. "
            "Install more supported tools, then rerun setup."
        )
    return (
        "Setup can proceed. Baseline validation tooling is available: at least one SMT solver and at least one first-order or SAT solver were detected."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize Formally BMAD state and detect automated reasoning tools.")
    parser.add_argument("--project-root", required=True, help="Project root directory.")
    parser.add_argument("--module-root", required=True, help="Formally BMAD module state directory.")
    parser.add_argument("--canonical-path", required=True, help="Canonical model directory.")
    parser.add_argument("--min-tools", type=int, default=1, help="Minimum supported automated reasoning tools required.")
    parser.add_argument("-o", "--output", help="Write JSON result to file instead of stdout.")
    parser.add_argument("--verbose", action="store_true", help="Emit progress diagnostics to stderr.")
    args = parser.parse_args()

    project_root = resolve_path(args.project_root, Path.cwd())
    module_root = resolve_path(args.module_root, project_root)
    canonical_path = resolve_path(args.canonical_path, project_root)

    if not project_root.exists():
        print(f"Project root does not exist: {project_root}", file=sys.stderr)
        return 2

    created = ensure_structure(module_root, canonical_path)
    artifacts = discover_artifacts(project_root)
    tool_search_dirs = resolve_tool_search_dirs()
    search_path = build_tool_search_path(tool_search_dirs)
    tools = {family: [detect_tool(tool, search_path=search_path) for tool in names] for family, names in SUPPORTED_TOOLS.items()}
    specialized_tools = {
        family: [detect_tool(tool, search_path=search_path) for tool in names]
        for family, names in SPECIALIZED_TOOLS.items()
    }
    proof_assistants = [detect_tool(tool, search_path=search_path) for tool in PROOF_ASSISTANTS]
    available_tool_count = sum(1 for entries in tools.values() for tool in entries if tool["available"])
    baseline_validation = evaluate_baseline_validation(tools)
    status = (
        "complete"
        if baseline_validation["baseline_satisfied"] and available_tool_count >= args.min_tools
        else "blocked"
    )
    guidance = build_guidance(baseline_validation, available_tool_count, args.min_tools)

    result: dict[str, object] = {
        "generated_at": utc_now(),
        "status": status,
        "project_root": str(project_root),
        "module_root": str(module_root),
        "canonical_path": str(canonical_path),
        "created_or_verified_folders": created,
        "artifacts": artifacts,
        "tool_search_dirs": tool_search_dirs,
        "tools": tools,
        "specialized_tools": specialized_tools,
        "proof_assistants_detected": proof_assistants,
        "baseline_validation": baseline_validation,
        "available_tool_count": available_tool_count,
        "min_required_tools": args.min_tools,
        "guidance": guidance,
    }
    report_path = write_report(module_root, result)
    result["report_path"] = str(report_path)

    output = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0 if status == "complete" else 1


if __name__ == "__main__":
    sys.exit(main())
