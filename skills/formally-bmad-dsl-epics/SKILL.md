---
name: formally-bmad-dsl-epics
description: Creates epics grounded in the DSL branch's accepted baseline, architecture deltas, and evidence posture. Use when the user requests to 'create DSL epics', 'map validated requirements to epics', or 'plan implementation from the DSL architecture baseline'.
---

# formally-bmad-dsl-epics

## Overview

This workflow creates or formalizes BMad epics for the parallel DSL branch while preserving the formal meaning of the upstream validated baseline. Act as an implementation-planning facilitator with a formal baseline underneath: keep the epic set readable, but make every epic traceable to accepted requirements, accepted upstream deltas, architecture decisions, architecture-level deltas, and inherited evidence posture.

This workflow must not treat PRD and architecture outputs as plain prose. It consumes:

- accepted PRD requirements;
- accepted upstream and architecture-level deltas;
- inherited increment-validation and architecture-validation posture;
- inherited ontology and ASM baseline context where relevant;
- inherited backend evidence posture;
- and it may introduce epic-level coverage commitments and story obligations.

The epics skill must distinguish between:

- inherited validated commitments;
- epic planning coverage of those commitments;
- deferred or contested upstream material;
- verification gaps that stories must later close.

Never flatten those distinctions into a simple “all requirements are covered” claim without evidence.

## Conventions

- Bare paths resolve from the skill root.
- `{skill-root}` resolves from this skill's installed directory.
- `{project-root}`-prefixed paths resolve from the project working directory.
- `{skill-name}` resolves to the skill directory's basename.

## On Activation

Load available config from `{project-root}/_bmad/config.yaml` and `{project-root}/_bmad/config.user.yaml` (root level and `formally-bmad` section). Resolve these values, using setup defaults only when config is absent:

- `formally_bmad_project_root`: `{project-root}/_bmad/formally-bmad`
- `formally_bmad_canonical_model_path`: `{project-root}/_bmad/formally-bmad/canonical`
- `formally_bmad_validation_strictness`: `stage-aware`
- `formally_bmad_report_format`: `markdown,html`

If `{formally_bmad_project_root}` or `{formally_bmad_canonical_model_path}/status.md` is missing, stop and direct the user to run `formally-bmad-setup`.

If `--headless` or `-H` is invoked, require accepted DSL PRD requirements, architecture context, or an existing epic artifact. Without source material, create only the workspace and report that DSL epics need PRD and architecture context.

## Workflow

### Establish Epic Context

Load or ask for:

- accepted DSL PRD requirements and their evidence classes;
- accepted upstream and architecture-level deltas;
- architecture decisions, refinements, and recheck obligations;
- known assumptions, unresolved blockers, and contested formal commitments;
- existing epics if formalizing brownfield work.

Epic planning must respect the accepted validated baseline and the current uncertainty posture. It must not silently erase deferred, assumption-dependent, or contested commitments.

### Initialize Workspace

Run the deterministic workspace helper once the epic set title or source path is known:

```bash
python3 scripts/epics_workspace.py --project-root {project-root} --module-root "{formally_bmad_project_root}" --title "{epic-set-title-or-source-slug}"
```

The helper creates `{formally_bmad_project_root}/artifacts/dsl-epics/<safe-title>/` with starter files for epics, requirement coverage, epic coherence, story obligations, accepted delta lineage, validation posture, provenance, and local validation.

### Create Or Formalize Epics

Produce or update readable BMad-style epics. Include a concise formal status block for the epic set that states:

- inherited requirement baseline scope;
- accepted upstream and architecture delta coverage;
- evidence posture of the epic set;
- deferred or contested commitments affecting planning;
- companion folder link.

If formalizing existing epics, preserve source meaning and avoid rewriting scope unless the user accepts a repair proposal.

### Map Requirements To Epics Conservatively

For every accepted PRD requirement, record one coverage status:

- `covered`
- `partially-covered`
- `deferred`
- `not-covered`
- `conflict`
- `not-applicable`

Preserve each requirement's evidence class and inherited validation posture in the coverage map. Do not rewrite a requirement with deferred or contested status as if the epic had already resolved it unless the epic actually introduces the missing design or verification plan.

### Check Epic Coherence

Assess each epic for:

- coherent purpose and bounded scope;
- relation to accepted PRD requirements;
- relation to architecture decisions and architecture deltas;
- dependency and ordering implications;
- assumptions or blockers that affect story decomposition;
- absence of hidden conflict with inherited validated commitments.

### Define Story Obligations

Derive story-level obligations from each epic, including:

- acceptance-criteria themes;
- architecture constraints stories must obey;
- inherited or new verification obligations stories must cover;
- recheck obligations triggered by architecture decisions;
- unresolved questions that must be answered before a story is ready.

For each covered requirement, say whether story work is expected to:

- preserve an existing evidence path;
- supply missing detail needed for later mechanized checking;
- remain test-backed or review-backed for now;
- avoid implementing deferred or contested commitments as if they were accepted facts.

### Preserve Delta And Evidence Lineage

Every coverage or epic-planning commitment should remain linked to:

- source requirement IDs;
- source upstream delta IDs;
- source architecture delta IDs when relevant;
- inherited evidence class or validation posture.

### Produce Companions

Maintain the companion folder with:

- `epics.md` — epic set artifact with formal status block;
- `requirement-coverage.md` — requirement-to-epic coverage map with evidence class and inherited validation posture;
- `epic-coherence.md` — epic purpose, scope, dependencies, blockers, and conflict notes;
- `story-obligations.md` — obligations for story creation, including verification and recheck needs;
- `accepted-delta-lineage.md` — accepted upstream and architecture-level delta references relevant to the epic set;
- `validation-posture.md` — summary of inherited evidence, deferred commitments, and planning risk;
- `provenance.md` — epic section to requirement, architecture decision, and delta mapping;
- `local-validation.md` — ambiguity, coverage gaps, blockers, and repair proposals.

### Handoff

End with:

- epic artifact path and companion folder;
- requirement coverage summary grouped by evidence posture;
- epic readiness status;
- story obligations;
- deferred or contested commitments affecting implementation planning;
- recommended next workflow: `formally-bmad-dsl-stories`.
