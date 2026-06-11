---
name: formally-bmad-formal-stories
description: Creates stories with formal readiness. Use when the user requests to 'create formal stories', 'formalize stories', or 'check story readiness'.
---

# formally-bmad-formal-stories

## Overview

This workflow creates or formalizes implementation stories with formal acceptance criteria, traceability, consistency checks, blocker detection, and readiness status. It consumes PRD, architecture, and epic model state and applies strict validation because stories are implementation-facing commitments.

## Conventions

- Bare paths (e.g. `scripts/stories_workspace.py`) resolve from the skill root.
- `{skill-root}` resolves to this skill's installed directory.
- `{project-root}`-prefixed paths resolve from the project working directory.
- `{skill-name}` resolves to the skill directory's basename.

## On Activation

Load available config from `{project-root}/_bmad/config.yaml` and `{project-root}/_bmad/config.user.yaml` (root level and `formally-bmad` section). Resolve these values, using setup defaults only when config is absent:

- `formally_bmad_project_root`: `{project-root}/_bmad/formally-bmad`
- `formally_bmad_canonical_model_path`: `{project-root}/_bmad/formally-bmad/canonical`
- `formally_bmad_validation_strictness`: `stage-aware`
- `formally_bmad_report_format`: `markdown,html`

If `{formally_bmad_project_root}` or `{formally_bmad_canonical_model_path}/status.md` is missing, stop and direct the user to run `formally-bmad-setup`.

If `--headless` or `-H` is invoked, require epic context, story obligations, an existing story artifact, or a target requirement. Without source material, create only the workspace and report that formal stories need epic and implementation context.

## Workflow

### Establish Story Context

Load or ask for:

- target epic and story obligations;
- accepted PRD requirements and verification obligations;
- architecture constraints and implementation constraints;
- relevant assumptions, unresolved blockers, and current canonical model status;
- existing story artifact if formalizing brownfield work.

Story validation is strict: a story should not be ready if accepted requirements lack formal coverage, alignment is unresolved, or blocking contradictions remain.

### Initialize Workspace

Run the deterministic workspace helper once the story title, ID, or source path is known:

```bash
python3 scripts/stories_workspace.py --project-root {project-root} --module-root "{formally_bmad_project_root}" --story-id "{story-id-or-title}"
```

The helper creates `{formally_bmad_project_root}/artifacts/stories/<safe-story-id>/` with starter files for story content, acceptance criteria, formalization, alignment, blockers, readiness, candidate delta, provenance, and local validation.

### Create or Formalize Story

Produce or update a readable BMad-style story. Include a concise formal status block:

- canonical model version or pending delta;
- readiness status;
- consistency/alignment status;
- last formalization timestamp;
- open blockers;
- companion folder link.

If formalizing an existing story, preserve source meaning and avoid rewriting acceptance criteria unless the user accepts a repair proposal.

### Formalize Acceptance Criteria

Convert acceptance criteria into checkable formal obligations:

- actor, trigger, and expected outcome;
- preconditions and scope;
- success/failure conditions;
- data or state constraints;
- architecture constraints referenced;
- verification condition or test obligation;
- logic-family placement.

Use `accepted` only for criteria the user confirms as implementation commitments. Use `open-question` for criteria that cannot be checked without clarification.

### Check Alignment

Validate the story against:

- PRD requirements and verification obligations;
- architecture decisions and constraints;
- epic scope and story obligations;
- prior stories where ordering or dependency matters;
- active assumptions and blockers.

Classify each alignment result as `satisfies`, `partially-satisfies`, `depends-on`, `conflicts`, `unmapped`, or `blocked`.

### Detect Implementation Blockers

Block readiness for:

- contradictions with accepted canonical assertions;
- missing formal coverage for accepted requirements;
- unresolved architecture constraints;
- stale source dependencies;
- unvalidated acceptance criteria;
- open questions required for implementation.

Produce repair proposals rather than only issue lists.

### Submit to Steward

Submit story deltas to `formally-bmad-agent-steward` through `Accept Canonical Delta` and `Validate Update Consistency`.

If validation reports contradiction, block story readiness until resolved or explicitly overridden. If overridden, the steward must mark the canonical model inconsistent and record downstream risk.

### Produce Companions

Maintain the companion folder with:

- `story.md` — story artifact or source link and formal status block;
- `acceptance-criteria.md` — criteria inventory and formalization;
- `formalization.md` — rigorous English formalization;
- `alignment.md` — PRD, architecture, epic, and prior-story alignment;
- `blockers.md` — contradictions, missing coverage, stale dependencies, and open questions;
- `readiness.md` — story readiness status and rationale;
- `candidate-delta.md` — canonical assertions and logic-family placement;
- `provenance.md` — story section to assertion/criterion mapping;
- `local-validation.md` — steward responses and repair proposals.

### Handoff

End with:

- story artifact path and companion folder;
- readiness status;
- accepted criteria and unresolved open questions;
- alignment summary;
- blockers and repair proposals;
- steward validation status;
- recommended next workflow: `formally-bmad-formal-verification` for readiness or checkpoint reporting.
