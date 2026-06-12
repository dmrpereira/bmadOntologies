---
name: formally-bmad-dsl-prd
description: Creates PRDs grounded in the DSL branch's accepted baseline, deltas, and validation state. Use when the user requests to 'create DSL PRD', 'formalize PRD with the DSL workflow', or 'write a PRD from the delta-validated brainstorming baseline'.
---

# formally-bmad-dsl-prd

## Overview

This workflow creates or formalizes a BMad-style PRD for the parallel DSL branch while preserving the formal meaning of the upstream baseline. Act as a product requirements facilitator with a formal baseline layer underneath: keep the PRD readable, but make every accepted requirement traceable to accepted canonical assertions, accepted deltas, validation state, and backend evidence posture.

This workflow must not treat brainstorming output as a loose idea dump or a single static formal model. It consumes:

- an evolving canonical baseline;
- accepted canonical assertions;
- accepted deltas;
- increment-validation outcomes;
- ontology and ASM projection context;
- backend evidence state.

The PRD must distinguish between:

- accepted baseline commitments;
- accepted commitments with deferred verification;
- deferred or contested formal commitments;
- asserted commitments and explicit assumptions.

Never flatten those into a single undifferentiated requirement list.

Never end the session silently. Before any pause, stop, or handoff, explicitly tell the user what PRD formalization work was completed, what evidence posture the result has, what blockers remain, and the next concrete step.

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

If `--headless` or `-H` is invoked, require source material such as a DSL-branch brainstorming workspace, an existing PRD path, or a product brief. Without source material, stop after creating the workspace and report that DSL PRD formalization needs a source baseline.

## Workflow

### Establish PRD Intent

Gather or load product intent, stakeholders, goals, non-goals, constraints, assumptions, success criteria, and source artifacts. Prefer an existing `formally-bmad-dsl-brainstorming` workspace when available.

The PRD skill must consume the accepted current baseline, not the full undifferentiated brainstorming history. Use this authority order:

1. accepted canonical assertions;
2. accepted deltas and their validation records;
3. current ontology and ASM projections;
4. generated properties and backend evidence;
5. brainstorm narrative and provenance.

If lower-authority artifacts conflict with higher-authority ones, higher-authority artifacts win unless the user explicitly proposes a new downstream delta.

### Initialize Workspace

Run the deterministic workspace helper once the PRD title or source path is known:

```bash
python3 scripts/prd_workspace.py --project-root {project-root} --module-root "{formally_bmad_dsl_project_root}" --title "{prd-title-or-source-slug}"
```

The helper creates `{formally_bmad_dsl_project_root}/artifacts/dsl-prd/<safe-title>/` with starter files for the PRD artifact, requirement inventory, formalization, accepted delta view, validation status, verification obligations, provenance, and local validation.

### Filter Eligible Source Material

Only treat upstream material as accepted requirement input when it satisfies the DSL branch contract.

Eligible canonical assertions:

- `LifecycleStatus = accepted`
- `KnowledgeStatus = asserted` or `assumption`

Eligible deltas:

- `DeltaLifecycleStatus = accepted`

Deferred deltas may inform PRD risks, deferred scope notes, and unresolved tensions, but must not become accepted requirement commitments.

Rejected deltas must not become accepted requirements except as provenance for rejected alternatives.

### Build A Requirement Evidence Model

Do not flatten all accepted assertions into equal-strength requirements. Each requirement must carry an evidence interpretation derived from the upstream validation state.

Use evidence classes such as:

- `baseline-accepted`
- `baseline-accepted-with-backend-evidence`
- `baseline-accepted-with-deferred-verification`
- `deferred-formal-commitment`
- `formally-contested`

Do not upgrade confidence downstream. If brainstorming only established an accepted delta with deferred backend checking, the PRD must not present it as if it were backend-validated.

### Draft Or Formalize The PRD

Produce or update the source PRD as normal Markdown. Include a concise formal status block that states:

- accepted baseline scope;
- count or summary of accepted deltas used;
- confidence posture of the requirement set;
- known deferred or contested formal commitments;
- companion folder link.

If formalizing an existing PRD, preserve source meaning and avoid rewriting requirements unless the user accepts a repair proposal.

### Keep PRD Summaries Synchronized

Treat the PRD artifact, `requirements.md`, `accepted-deltas.md`, `validation-status.md`, and the PRD formal status block as one synchronized package.

If requirement IDs, source assertion IDs, source delta IDs, evidence classes, or accepted-delta coverage change during PRD work, update every affected summary in the same session. Do not leave the PRD body or status block naming an older accepted baseline after the requirement inventory has been revised.

At minimum, resynchronize:

- the PRD formal status block baseline scope summary;
- the accepted-delta count or summary;
- requirement references used in the PRD body;
- `requirements.md`;
- `accepted-deltas.md`;
- `validation-status.md`.

Do not hand off a PRD stage whose inventories and summary blocks disagree about the accepted baseline.

### Extract Requirements Conservatively

From the upstream DSL branch, extract:

- accepted behavioral assertions;
- accepted structural assertions that imply product commitments;
- accepted deltas that introduce or modify obligations;
- accepted negative, conditional, or state-driven constraints that shape product behavior;
- explicit assumptions that materially affect requirement meaning.

Also extract unresolved formal risks from:

- deferred deltas;
- failed increment-validation rows;
- failing backend checks;
- open questions with architecture or verification consequences.

### Formalize And Preserve Confidence

For each requirement, write rigorous English that identifies:

- subject and predicate;
- preconditions and scope;
- obligation, permission, or prohibition;
- measurable success condition if available;
- dependency on assumptions or upstream deltas;
- baseline evidence class.

The PRD must preserve, in user-visible artifacts:

- accepted requirement vs deferred idea;
- accepted baseline vs contested baseline;
- backend-evidenced requirement vs deferred-verification requirement;
- asserted requirement vs explicit assumption.

If those distinctions disappear, the PRD corrupts the epistemic meaning of the upstream formal artifacts.

### Maintain Delta-Aware Provenance

Every accepted requirement should record:

- source assertion IDs;
- source delta IDs;
- evidence class;
- validation posture;
- assumption dependencies where relevant.

### Define Downstream Verification Obligations

Create verification obligations that distinguish between:

- obligations already supported by inherited backend evidence;
- obligations accepted into the baseline but still awaiting stronger mechanized checks;
- obligations that must be rechecked after architecture or later refinements;
- obligations blocked by contested or deferred increments.

Do not pretend that PRD-stage restatement itself is formal verification.

### Produce Companions

Maintain the companion folder with:

- `prd.md` — PRD artifact with formal status block;
- `requirements.md` — requirement inventory with source assertion IDs, source delta IDs, evidence class, assumption/assertion distinction, and validation posture;
- `formalization.md` — rigorous English formalization and interpretation of accepted DSL-branch requirements;
- `accepted-deltas.md` — accepted delta subset relevant to the PRD;
- `validation-status.md` — summary of inherited validation and backend evidence posture;
- `verification-obligations.md` — downstream obligations, including recheck needs and deferred mechanization;
- `provenance.md` — PRD section to canonical assertion and delta mapping;
- `local-validation.md` — ambiguity, conflicts, deferred items, and repair proposals.

### Handoff

End with:

- PRD path and companion folder;
- accepted requirements grouped by evidence class;
- deferred and contested formal commitments that affect product scope or confidence;
- accepted delta coverage summary;
- inherited backend evidence posture;
- assumptions that materially affect accepted requirements;
- explicit confirmation that the PRD artifact, requirement inventory, accepted-delta view, and validation summary were synchronized for this handoff;
- mandatory next workflow when the PRD stage is complete: `formally-bmad-dsl-architecture` for design refinement over the accepted validated baseline.
