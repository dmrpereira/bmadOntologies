#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Create a DSL-branch brainstorming workspace."""

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
        "## Namespaces\n\n"
        "Prefix ex: https://example.org/domain#\n\n"
        "## Scope\n\n"
        "## Concepts\n\n"
        "Concept C-001: ExampleConcept as Entity\n"
        "LifecycleStatus: provisional\n"
        "KnowledgeStatus: asserted\n"
        "VerificationStatus: not_mapped\n"
        "  Definition: Replace with the canonical concept definition.\n\n"
        "## Relations\n\n"
        "Relation R-001: ExampleConcept relatesTo optional AnotherConcept\n"
        "LifecycleStatus: provisional\n"
        "KnowledgeStatus: asserted\n"
        "VerificationStatus: not_mapped\n"
        "  Notes: Replace with a real semantic relation.\n\n"
        "## States\n\n"
        "State S-001: ExampleState = Draft | Active | Closed\n"
        "LifecycleStatus: provisional\n"
        "KnowledgeStatus: asserted\n"
        "VerificationStatus: not_mapped\n"
        "  Notes: Replace with actual state family members.\n\n"
        "## Events And Actions\n\n"
        "Event E-001: ExampleEvent(exampleId: ExampleConcept)\n"
        "LifecycleStatus: provisional\n"
        "KnowledgeStatus: asserted\n"
        "VerificationStatus: not_mapped\n"
        "  Notes: Replace with a real event trigger.\n\n"
        "## Assertion Catalog\n\n"
        "Assertion A-001: EventDriven\n"
        "Statement: \"When an example trigger occurs, the system shall perform an example response.\"\n"
        "Trigger: \"an example trigger occurs\"\n"
        "Response: \"the system performs an example response\"\n"
        "OntologyTerms: ExampleConcept\n"
        "BehaviorTerms: ExampleEvent\n"
        "LifecycleStatus: provisional\n"
        "KnowledgeStatus: asserted\n"
        "VerificationStatus: not_mapped\n"
        "Notes: Replace with a real normalized behavioral assertion.\n\n"
        "## Scenarios\n\n"
        "Scenario SC-001: GherkinLike\n"
        "LifecycleStatus: provisional\n"
        "KnowledgeStatus: asserted\n"
        "VerificationStatus: not_mapped\n"
        "Given an example precondition holds\n"
        "When the example event occurs\n"
        "Then the example response is observed\n"
        "References: A-001\n\n"
        "## Assumptions\n\n"
        "Assumption AS-001: \"Replace with an explicit modeling assumption.\"\n"
        "LifecycleStatus: provisional\n"
        "KnowledgeStatus: assumption\n"
        "VerificationStatus: not_mapped\n\n"
        "## Alternatives\n\n"
        "Alternative ALT-001: \"Replace with a competing design direction.\"\n"
        "LifecycleStatus: provisional\n"
        "KnowledgeStatus: asserted\n"
        "VerificationStatus: not_mapped\n"
        "  Implication: Replace with what this alternative would imply.\n\n"
        "## Open Questions\n\n"
        "Question Q-001: \"Replace with an unresolved formal question.\" [Canonical]\n"
        "LifecycleStatus: provisional\n"
        "KnowledgeStatus: open_question\n"
        "VerificationStatus: not_mapped\n"
    ),
    "ontology-projection.md": (
        "# Ontology Projection\n\n"
        "Target language: OWL 2 DL\n\n"
        "## Classes\n\n"
        "| Class | Parent | Qualified Name | Source IDs | LifecycleStatus | Notes |\n"
        "| ----- | ------ | -------------- | ---------- | --------------- | ----- |\n\n"
        "## Properties\n\n"
        "| Property | Kind | Domain | Range | Qualified Name | Source IDs | LifecycleStatus | Notes |\n"
        "| -------- | ---- | ------ | ----- | -------------- | ---------- | --------------- | ----- |\n\n"
        "## Semantic Constraints\n\n"
        "| Constraint | OWL Shape | Source IDs | LifecycleStatus | Notes |\n"
        "| ---------- | --------- | ---------- | --------------- | ----- |\n\n"
        "## Manchester Fragments\n\n"
    ),
    "asm-model.md": (
        "# ASM Model\n\n"
        "Target semantics: disciplined ASM ground model\n\n"
        "## Domains\n\n"
        "| Domain | Kind | Source IDs | LifecycleStatus | Notes |\n"
        "| ------ | ---- | ---------- | --------------- | ----- |\n\n"
        "## Controlled Functions\n\n"
        "| Function | Type | Source IDs | LifecycleStatus | Notes |\n"
        "| -------- | ---- | ---------- | --------------- | ----- |\n\n"
        "## Monitored Functions\n\n"
        "| Function | Type | Source IDs | LifecycleStatus | Notes |\n"
        "| -------- | ---- | ---------- | --------------- | ----- |\n\n"
        "## Derived Predicates\n\n"
        "| Predicate | Meaning | Source IDs | LifecycleStatus | Notes |\n"
        "| --------- | ------- | ---------- | --------------- | ----- |\n\n"
        "## Rules\n\n"
        "| Rule | Trigger | Guard | Update Summary | Source IDs | LifecycleStatus | Notes |\n"
        "| ---- | ------- | ----- | -------------- | ---------- | --------------- | ----- |\n\n"
        "## Invariants\n\n"
        "| Invariant ID | Statement | Source IDs | LifecycleStatus | Notes |\n"
        "| ------------ | --------- | ---------- | --------------- | ----- |\n\n"
        "## Modeling Conventions\n\n"
    ),
    "proposed-deltas.md": (
        "# Proposed Deltas\n\n"
        "| Delta ID | Source Brainstorm Outcome | Source Assertion IDs | Change Kind | Target Layer(s) | Summary | Affected Existing IDs | DeltaLifecycleStatus | DeltaValidationStatus | Disposition | Notes |\n"
        "| -------- | ------------------------ | -------------------- | ----------- | --------------- | ------- | --------------------- | -------------------- | --------------------- | ----------- | ----- |\n"
    ),
    "increment-validation.md": (
        "# Increment Validation\n\n"
        "| Delta ID | Affected Ontology Elements | Affected ASM Elements | Affected Property IDs | New Property IDs | Obsolete Property IDs | Recheck Property IDs | Ontology Increment Result | ASM Increment Result | Property Impact Result | Backend Check Result | Overall Increment Result | Counterexample / Conflict Reference | Notes |\n"
        "| -------- | -------------------------- | --------------------- | --------------------- | ---------------- | --------------------- | -------------------- | ------------------------- | -------------------- | ---------------------- | -------------------- | ------------------------ | ----------------------------------- | ----- |\n"
    ),
    "generated-properties.md": (
        "# Generated Properties\n\n"
        "| Property ID | Kind | Source Assertion IDs | Origin Delta ID | Informal Meaning | Target Backend Form | Status |\n"
        "| ----------- | ---- | -------------------- | --------------- | ---------------- | ------------------- | ------ |\n"
    ),
    "verification-traceability.md": (
        "# Verification Traceability\n\n"
        "| Brainstorm Outcome | Canonical Source ID(s) | Delta ID | Ontology Element(s) | ASM Element(s) | Property ID(s) | Increment Validation Result | Backend Check Result | Disposition | Notes |\n"
        "| ------------------ | ---------------------- | -------- | ------------------- | -------------- | -------------- | --------------------------- | -------------------- | ----------- | ----- |\n"
    ),
    "backend-checks.md": (
        "# Backend Checks\n\n"
        "| Check ID | Backend | Model Artifact | Property IDs | Triggered By Delta ID | Result | Counterexample / Witness | Notes |\n"
        "| -------- | ------- | -------------- | ------------ | --------------------- | ------ | ------------------------ | ----- |\n"
    ),
    "candidate-delta.md": "# Candidate Canonical Delta\n\n",
    "provenance.md": (
        "# Provenance\n\n"
        "| Source Idea | Canonical Source ID(s) | Delta ID | Ontology Impact | ASM Impact | Property Impact | State | Notes |\n"
        "| ----------- | ---------------------- | -------- | --------------- | ---------- | --------------- | ----- | ----- |\n"
    ),
    "local-validation.md": (
        "# Local Validation\n\n"
        "## Baseline Drift Checks\n\n"
        "- Canonical surface updated:\n"
        "- Ontology projection synchronized:\n"
        "- ASM model synchronized:\n"
        "- Proposed deltas reviewed:\n"
        "- Increment validation reviewed:\n"
        "- Generated properties synchronized:\n"
        "- Backend checks refreshed:\n\n"
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
    workspace = module_root / "artifacts" / "dsl-brainstorming" / safe_topic
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
    parser = argparse.ArgumentParser(description="Create a DSL-branch brainstorming workspace.")
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
