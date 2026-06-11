---
name: formally-bmad-formal-epics
description: Creates epics with formal coverage. Use when the user requests to 'create formal epics', 'formalize epics', or 'map requirements to epics'.
---

# formally-bmad-formal-epics

## Overview

This workflow creates or formalizes BMad epics as implementation planning structures with formal traceability to accepted PRD requirements, architecture constraints, assumptions, and verification obligations. It ensures epics expose coverage gaps before story writing begins and produce story-level obligations for downstream implementation planning.

## Conventions

- Bare paths (e.g. `scripts/epics_workspace.py`) resolve from the skill root.
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

If `--headless` or `-H` is invoked, require accepted PRD requirements, architecture constraints, or an existing epic artifact. Without source material, create only the workspace and report that formal epics need requirement and architecture context.

## Workflow

### Establish Epic Context

Load or ask for:

- accepted PRD requirements and verification obligations;
- architecture decisions and implementation constraints;
- known assumptions, unresolved blockers, and current canonical model status;
- existing epics if formalizing brownfield work.

Epic validation is stricter than architecture planning but less granular than story readiness. Epics must show coverage and coherent decomposition intent before stories are created.

### Initialize Workspace

Run the deterministic workspace helper once the epic set title or source path is known:

```bash
python3 scripts/epics_workspace.py --project-root {project-root} --module-root "{formally_bmad_project_root}" --title "{epic-set-title-or-source-slug}"
```

The helper creates `{formally_bmad_project_root}/artifacts/epics/<safe-title>/` with starter files for epics, requirement coverage, epic coherence, story obligations, candidate delta, provenance, and local validation.

### Create or Formalize Epics

Produce or update readable BMad-style epics. Include a concise formal status block for the epic set:

- canonical model version or pending delta;
- coverage/alignment status;
- last formalization timestamp;
- open blockers;
- companion folder link.

If formalizing existing epics, preserve source meaning and avoid rewriting scope unless the user accepts a repair proposal.

### Map Requirements to Epics

For every accepted PRD requirement, record one coverage status:

- `covered`;
- `partially-covered`;
- `deferred`;
- `not-covered`;
- `conflict`;
- `not-applicable`.

Coverage gaps are not automatically contradictions, but implementation-facing epics should not be ready while accepted requirements are unintentionally unmapped.

### Check Epic Coherence

Assess each epic for:

- coherent purpose and bounded scope;
- relation to accepted PRD requirements;
- relation to architecture constraints;
- dependencies and ordering implications;
- assumptions or blockers that affect story decomposition;
- absence of hidden conflicts with accepted commitments.

### Define Story Obligations

Derive story-level obligations from each epic:

- required acceptance-criteria themes;
- architecture constraints stories must obey;
- verification obligations stories must cover;
- unresolved questions that must be answered before a story can be ready.

### Submit to Steward

Submit epic deltas to `formally-bmad-agent-steward` through `Accept Canonical Delta` and `Validate Update Consistency` where epic commitments are accepted.

If validation reports contradiction against accepted PRD or architecture commitments, block readiness for the affected epic until resolved or explicitly overridden.

### Produce Companions

Maintain the companion folder with:

- `epics.md` — epic set artifact or source link and formal status block;
- `requirement-coverage.md` — requirement-to-epic coverage map;
- `epic-coherence.md` — epic purpose, scope, dependencies, and blockers;
- `story-obligations.md` — obligations for story creation;
- `candidate-delta.md` — canonical assertions and logic-family placement;
- `provenance.md` — epic section to assertion/coverage mapping;
- `local-validation.md` — ambiguity, coverage gaps, blockers, steward responses, and repair proposals.

### Handoff

End with:

- epic artifact path and companion folder;
- requirement coverage summary;
- epic readiness status;
- story obligations;
- steward validation status;
- recommended next workflow: `formally-bmad-formal-stories`.
