#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Create ontology alignment workspace scaffolding for Formally BMAD."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_REPOSITORIES = [
    {
        "code": "bioportal",
        "name": "BioPortal",
        "url": "https://bioportal.bioontology.org/",
        "purpose": "Broad ontology repository, especially biomedical ontologies.",
        "license_note": "Repository is open to users; individual ontology licenses may vary.",
    },
    {
        "code": "obo-foundry",
        "name": "OBO Foundry",
        "url": "https://obofoundry.org/",
        "purpose": "Interoperable open biomedical and biological ontologies.",
        "license_note": "Check each ontology's declared license.",
    },
    {
        "code": "lov",
        "name": "Linked Open Vocabularies",
        "url": "https://lov.linkeddata.es/",
        "purpose": "RDF/OWL vocabulary discovery for linked-data contexts.",
        "license_note": "Check each vocabulary's declared license.",
    },
    {
        "code": "wikidata",
        "name": "Wikidata",
        "url": "https://www.wikidata.org/",
        "purpose": "Open identifiers, cross-links, and term grounding.",
        "license_note": "Wikidata content licensing applies; verify downstream use.",
    },
    {
        "code": "ontohub",
        "name": "Ontohub",
        "url": "https://ontohub.org/",
        "purpose": "Heterogeneous formal ontology and logic resources where relevant.",
        "license_note": "Check each ontology's declared license.",
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def resolve_path(raw: str, project_root: Path) -> Path:
    return Path(raw.replace("{project-root}", str(project_root))).expanduser().resolve()


def write_registry(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"repositories": DEFAULT_REPOSITORIES}, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_mapping_skeleton(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "# Ontology Candidate Mappings\n\n"
        "| Project Concept | External Label | External URI | Repository | Mapping | Status | Rationale |\n"
        "| --------------- | -------------- | ------------ | ---------- | ------- | ------ | --------- |\n",
        encoding="utf-8",
    )


def write_report(path: Path, generated_at: str, alignment_root: Path, registry_path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "# Ontology Alignment Report\n\n"
        f"- Generated: `{generated_at}`\n"
        f"- Alignment workspace: `{alignment_root}`\n"
        f"- Repository registry: `{registry_path}`\n\n"
        "## Project Concepts\n\n"
        "To be completed by the workflow.\n\n"
        "## Repository Searches\n\n"
        "To be completed by the workflow with query provenance and retrieval dates.\n\n"
        "## Candidate Mappings\n\n"
        "To be completed by the workflow.\n\n"
        "## Controlled Imports and Steward Validation\n\n"
        "To be completed by the workflow.\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Create Formally BMAD ontology alignment workspace scaffolding.")
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

    generated_at = utc_now()
    alignment_root = module_root / "artifacts" / "ontology-alignment"
    reports_root = module_root / "reports"
    alignment_root.mkdir(parents=True, exist_ok=True)
    reports_root.mkdir(parents=True, exist_ok=True)

    registry_path = alignment_root / "repository-registry.json"
    mappings_path = alignment_root / "candidate-mappings.md"
    report_path = reports_root / "ontology-alignment-report.md"

    if not registry_path.exists():
        write_registry(registry_path)
    if not mappings_path.exists():
        write_mapping_skeleton(mappings_path)
    write_report(report_path, generated_at, alignment_root, registry_path)

    result: dict[str, object] = {
        "generated_at": generated_at,
        "status": "complete",
        "project_root": str(project_root),
        "module_root": str(module_root),
        "alignment_root": str(alignment_root),
        "repository_registry": str(registry_path),
        "candidate_mappings": str(mappings_path),
        "report_path": str(report_path),
        "repositories": DEFAULT_REPOSITORIES,
    }

    output = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
