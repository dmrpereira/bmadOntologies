---
name: formally-bmad-formal-import
description: Imports existing BMad artifacts formally. Use when the user requests to 'formalize existing BMad artifacts', 'import BMad artifacts into formally-bmad', or 'run formal import'.
---

# formally-bmad-formal-import

## Overview

This workflow imports existing BMad Markdown artifacts into Formally BMAD by discovering candidate files, classifying artifact types, extracting candidate formal assertions, creating source-artifact companions, building provenance, submitting deltas to the steward, and producing an import report. Act as a formalization migration specialist: preserve source intent, avoid overcommitting ambiguous text, and make every imported assertion traceable.

## Conventions

- Bare paths (e.g. `scripts/import_inventory.py`) resolve from the skill root.
- `{skill-root}` resolves to this skill's installed directory.
- `{project-root}`-prefixed paths resolve from the project working directory.
- `{skill-name}` resolves to the skill directory's basename.

## On Activation

Load available config from `{project-root}/_bmad/config.yaml` and `{project-root}/_bmad/config.user.yaml` (root level and `formally-bmad` section). Resolve these values, using setup defaults only when config is absent:

- `formally_bmad_project_root`: `{project-root}/_bmad/formally-bmad`
- `formally_bmad_canonical_model_path`: `{project-root}/_bmad/formally-bmad/canonical`
- `formally_bmad_validation_strictness`: `stage-aware`
- `formally_bmad_report_format`: `markdown,html`

If `{formally_bmad_project_root}` or `{formally_bmad_canonical_model_path}/status.md` is missing, stop and direct the user to run `formally-bmad-setup` before import. Do not create an import model outside the setup-managed project structure.

If the user invokes `--headless` or `-H`, run the import with inferred defaults: project-wide scope, no source edits, candidate/provisional assertion states only, and a Markdown import report.

## Workflow

### Inventory

Run the deterministic inventory helper:

```bash
python3 scripts/import_inventory.py --project-root {project-root} --module-root "{formally_bmad_project_root}"
```

The helper discovers candidate Markdown artifacts, applies filename/path heuristics, creates the import workspace under `{formally_bmad_project_root}/artifacts/import/`, and writes an inventory JSON plus a Markdown skeleton report.

Use the helper output as inventory, not as semantic truth. It can suggest artifact kinds, but final classification is a workflow judgment.

### Classify Scope

Confirm the import scope unless running headless:

- all discovered BMad artifacts;
- selected artifact families: brainstorming, PRD, architecture, epics, stories, readiness reports, verification reports;
- selected files only.

Exclude generated Formally BMAD companions, reports, exports, memory, and tool-run files from source import. They are outputs, not source artifacts.

### Extract Candidate Formalization

For each selected source artifact, produce a source-artifact companion folder under `{formally_bmad_project_root}/artifacts/<kind>/<safe-source-id>/` containing:

- `source-summary.md` — source path, artifact kind, sections, and import notes;
- `formalization.md` — rigorous English formalization;
- `candidate-delta.md` — candidate/provisional canonical assertions and logic-family placement;
- `provenance.md` — source section to assertion mapping;
- `local-validation.md` — import-time findings, ambiguity, skipped content, and steward response.

Use assertion states conservatively:

- `candidate` for likely project concepts or requirements;
- `provisional` for uncertain ideas and partial interpretations;
- `open-question` when a statement cannot be formalized without clarification;
- `assumption` only when the source text explicitly supports an assumption;
- do not mark imported assertions `accepted` unless the user explicitly confirms promotion.

### Submit to Steward

For every artifact delta, invoke the steward conceptually through `formally-bmad-agent-steward` capability `Accept Canonical Delta`. The steward must validate the delta contract before any import commit.

Expected steward result categories:

- `accepted_for_validation` — write candidate delta and provenance; status remains candidate/provisional until promoted;
- `needs_clarification` — record open questions and blockers in the local validation file and import report;
- `rejected` — record unsupported or unsafe formalization with rationale.

If a steward validation detects contradiction in an imported candidate, treat it as an import blocker, not as a source edit request. Existing artifacts must not be rewritten during import unless the user explicitly accepts a later repair workflow.

### Produce Import Report

Create `{formally_bmad_project_root}/reports/import-report.md` summarizing:

- files discovered, selected, skipped, and unsupported;
- classification decisions;
- candidate/provisional assertions created;
- open questions and ambiguities;
- contradictions or steward blockers;
- provenance coverage;
- suggested next steps, including ontology alignment or verification where relevant.

HTML may be produced later by reporting workflows; this import workflow must always produce Markdown.

### Handoff

If import produced candidate formalization, recommend `formally-bmad-ontology-alignment` next when domain concepts would benefit from external ontology grounding. Otherwise recommend `formally-bmad-formal-verification` for a checkpoint report or the relevant lifecycle workflow for continued authoring.
