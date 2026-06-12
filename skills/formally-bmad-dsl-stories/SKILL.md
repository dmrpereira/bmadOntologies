---
name: formally-bmad-dsl-stories
description: Creates stories grounded in the DSL branch's accepted baseline, epic planning, and evidence posture. Use when the user requests to 'create DSL stories', 'formalize implementation stories with the DSL workflow', or 'check story readiness from the validated DSL baseline'.
---

# formally-bmad-dsl-stories

## Overview

This workflow creates or formalizes implementation stories for the parallel DSL branch while preserving the formal meaning of the upstream validated baseline. Act as an implementation-readiness facilitator with a formal baseline underneath: keep the story readable, but make every accepted criterion traceable to accepted requirements, accepted deltas, architecture decisions, epic obligations, and inherited evidence posture.

This workflow must not treat PRD, architecture, and epic outputs as plain prose. It consumes:

- accepted PRD requirements;
- accepted upstream and architecture-level deltas;
- inherited validation posture and backend evidence state;
- architecture constraints and recheck obligations;
- epic coverage and story obligations.

The stories skill must distinguish between:

- inherited validated commitments;
- implementation-facing acceptance criteria derived from them;
- deferred or contested upstream commitments;
- blockers that prevent a story from being truly ready.

Never flatten those distinctions into a superficial “ready” label.

Never end the session silently. Before any pause, stop, or handoff, explicitly tell the user what story formalization work was completed, what readiness level was actually reached, what remains blocked, and the next concrete step.

This branch is sequential. Do not suggest skipping required downstream stages, do not offer to move straight into implementation, and do not present branch order as optional while the DSL workflow is incomplete.

## Conventions

- Bare paths resolve from the skill root.
- `{skill-root}` resolves from this skill's installed directory.
- `{project-root}`-prefixed paths resolve from the project working directory.
- `{skill-name}` resolves to the skill directory's basename.

## On Activation

Load available config from `{project-root}/_bmad/config.yaml` and `{project-root}/_bmad/config.user.yaml` (root level and `formally-bmad-dsl` section). Resolve these values, using setup defaults only when config is absent:

- `formally_bmad_dsl_project_root`: `{project-root}/_bmad/formally-bmad-dsl`
- `formally_bmad_dsl_canonical_model_path`: `{project-root}/_bmad/formally-bmad-dsl/canonical`
- `formally_bmad_dsl_validation_strictness`: `stage-aware`
- `formally_bmad_dsl_report_format`: `markdown,html`

If `{formally_bmad_dsl_project_root}` or `{formally_bmad_dsl_canonical_model_path}/status.md` is missing, stop and direct the user to run `formally-bmad-dsl-setup`.

If `--headless` or `-H` is invoked, require epic context, story obligations, an existing story artifact, or a target requirement. Without source material, create only the workspace and report that DSL stories need epic and implementation context.

## Workflow

### Establish Story Context

Load or ask for:

- target epic and story obligations;
- accepted PRD requirements and evidence classes;
- accepted upstream and architecture-level deltas;
- architecture constraints, refinements, and recheck obligations;
- relevant assumptions, unresolved blockers, and current validation posture;
- existing story artifact if formalizing brownfield work.

Story validation in this branch is strict: a story should not be ready if inherited validated commitments lack implementation-facing coverage, alignment is unresolved, deferred or contested commitments are being treated as accepted facts, or blocker status is hidden.

### Initialize Workspace

Run the deterministic workspace helper once the story title, ID, or source path is known:

```bash
python3 scripts/stories_workspace.py --project-root {project-root} --module-root "{formally_bmad_dsl_project_root}" --story-id "{story-id-or-title}"
```

The helper creates `{formally_bmad_dsl_project_root}/artifacts/dsl-stories/<safe-story-id>/` with starter files for story content, acceptance criteria, formalization, alignment, blockers, readiness, delta lineage, provenance, and local validation.

### Create Or Formalize Story

Produce or update a readable BMad-style story. Include a concise formal status block that states:

- inherited baseline scope for the story;
- inherited evidence posture;
- architecture and epic obligations in scope;
- deferred or contested commitments affecting readiness;
- companion folder link.

If formalizing an existing story, preserve source meaning and avoid rewriting acceptance criteria unless the user accepts a repair proposal.

### Formalize Acceptance Criteria Conservatively

Convert acceptance criteria into implementation-facing formal obligations that preserve upstream evidence meaning.

For each accepted criterion, explicitly record:

- criterion ID;
- criterion text;
- evidence class;
- source requirement IDs;
- source delta IDs;
- architecture or epic obligations it satisfies;
- implementation-facing verification condition or review/test obligation;
- readiness impact.

If a criterion is represented only as a test obligation or manual review obligation, say so plainly. Do not imply that every acceptance criterion is solver-ready merely because it has rigorous English.

### Check Alignment

Validate the story against:

- PRD requirements and their evidence classes;
- architecture decisions, refinements, and recheck obligations;
- epic coverage and story obligations;
- prior stories where dependency or ordering matters;
- active assumptions, deferred deltas, contested commitments, and blockers.

Classify each alignment result as:

- `satisfies`
- `partially-satisfies`
- `depends-on`
- `conflicts`
- `unmapped`
- `blocked`

### Detect Implementation Blockers

Block readiness for:

- contradictions with inherited accepted commitments;
- missing implementation-facing coverage for accepted requirements;
- unresolved architecture or epic constraints;
- stale upstream dependencies;
- hidden dependence on deferred or contested formal commitments;
- missing evidence classification for accepted criteria;
- open questions required for implementation.

Produce repair proposals rather than only issue lists.

### Preserve Delta And Evidence Lineage

Every criterion and every readiness claim should remain linked to:

- source requirement IDs;
- source upstream delta IDs;
- source architecture delta IDs when relevant;
- epic obligation lineage;
- inherited evidence posture.

### Produce Companions

Maintain the companion folder with:

- `story.md` — story artifact with formal status block;
- `acceptance-criteria.md` — criteria inventory with evidence class, source lineage, and implementation-facing verification or review/test posture;
- `formalization.md` — rigorous English formalization and any non-mechanization rationale;
- `alignment.md` — PRD, architecture, epic, and prior-story alignment;
- `blockers.md` — contradictions, hidden uncertainty, missing coverage, stale dependencies, and repair proposals;
- `readiness.md` — story readiness status and rationale, including deferred or contested commitments affecting implementation;
- `delta-lineage.md` — source delta lineage relevant to the story;
- `provenance.md` — story section to requirement, criterion, and delta mapping;
- `local-validation.md` — local validation notes and unresolved issues.

### Handoff

End with:

- story artifact path and companion folder;
- readiness status;
- accepted criteria grouped by evidence posture;
- alignment summary;
- blockers and repair proposals;
- deferred or contested commitments affecting implementation;
- mandatory next workflow when the stories stage is complete: `formally-bmad-dsl-verification` before any implementation work.
