---
name: formally-bmad-dsl-architecture
description: Creates architecture artifacts grounded in the DSL branch's accepted baseline, deltas, and evidence posture. Use when the user requests to 'create DSL architecture', 'design architecture with the DSL workflow', or 'refine the validated baseline into architecture'.
---

# formally-bmad-dsl-architecture

## Overview

This workflow creates or formalizes architecture artifacts for the parallel DSL branch while preserving the formal meaning of the upstream validated baseline. Act as a system architect with a formal baseline underneath: keep the architecture readable, but make every major design choice traceable to accepted requirements, accepted deltas, inherited validation posture, and backend evidence state.

This workflow must not treat the PRD as plain prose. It consumes:

- accepted PRD requirements;
- accepted upstream deltas;
- inherited increment-validation state;
- inherited ontology and ASM baseline context;
- inherited backend evidence posture;
- and it may introduce new architecture-level deltas.

The architecture skill must distinguish between:

- inherited validated commitments;
- architecture interpretations of those commitments;
- new architectural commitments;
- new architecture-level deltas requiring validation.

Never flatten those distinctions into a single undifferentiated design narrative.

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

If `{formally_bmad_project_root}` or `{formally_bmad_canonical_model_path}/status.md` is missing, stop and direct the user to run `formally-bmad-dsl-setup`.

If `--headless` or `-H` is invoked, require source material such as a DSL-branch PRD workspace, an existing architecture path, or a structured design brief. Without source material, stop after creating the workspace and report that DSL architecture formalization needs a source baseline.

## Workflow

### Establish Architecture Intent

Gather or load architecture goals, constraints, deployment context, interaction concerns, and source artifacts. Prefer an existing `formally-bmad-dsl-prd` workspace when available.

The architecture skill must design against the accepted validated baseline, not against every brainstormed possibility. Use this authority order:

1. accepted PRD requirements;
2. accepted deltas and validation records;
3. inherited ontology and ASM baseline;
4. verification obligations and backend evidence;
5. earlier brainstorming narrative.

If prose and the accepted validated baseline disagree, the accepted validated baseline wins unless the user explicitly proposes a new architecture-level delta.

### Initialize Workspace

Run the deterministic workspace helper once the architecture title or source path is known:

```bash
python3 scripts/architecture_workspace.py --project-root {project-root} --module-root "{formally_bmad_project_root}" --title "{architecture-title-or-source-slug}"
```

The helper creates `{formally_bmad_project_root}/artifacts/dsl-architecture/<safe-title>/` with starter files for the architecture artifact, design decisions, architecture deltas, validation status, ontology refinement, ASM refinement, verification obligations, provenance, and local validation.

### Filter Eligible Upstream Inputs

Requirements are eligible as architecture-driving commitments when they are:

- accepted PRD requirements;
- tied to accepted deltas;
- not currently marked as formally contested.

Deferred deltas, contested requirements, and assumptions may still be consumed, but only as risks, architecture alternatives, unresolved constraints, or triggers for additional validation. They must not become silently accepted architectural facts.

### Design Against The Accepted Baseline

Produce or update the architecture as normal Markdown. Include a concise architecture status block that states:

- inherited baseline scope;
- inherited evidence posture;
- architecture decisions that are interpretive versus newly introduced;
- architecture-level deltas introduced by this stage;
- companion folder link.

### Refine Architecture Conservatively

The architecture skill may:

- refine accepted requirements into components, boundaries, interactions, and architectural constraints;
- introduce architecture-level deltas;
- tighten ontology structure for design purposes;
- refine the ASM baseline where architecture decisions affect behavior, coordination, or state ownership;
- introduce new verification obligations driven by design commitments.

It may not:

- silently redefine accepted upstream requirements;
- silently ignore failed or deferred validation states;
- present unsupported architecture assumptions as if they were validated inherited facts.

### Maintain Design Decisions

Record major design choices explicitly, including:

- what upstream requirement or delta drove them;
- whether the decision is inherited, interpretive, or newly introduced;
- what ontology refinement, ASM refinement, or verification impact it causes.

### Maintain Architecture Deltas

Every new architectural commitment with formal significance should create an architecture-level delta.

Typical triggers include:

- subsystem boundaries that change responsibility allocation;
- refined state ownership or event flow;
- decomposition of one requirement into distributed interactions;
- new ordering, consistency, synchronization, or fault-handling constraints.

Each architecture delta should identify:

- source requirement IDs;
- source upstream delta IDs;
- ontology impacts;
- ASM impacts;
- property impacts;
- recheck obligations;
- validation posture.

### Refine Ontology And ASM

Maintain `ontology-refinement.md` for refinements that add or clarify:

- component-level concepts;
- interface-level relations;
- dependency relations;
- ownership or allocation relations;
- updated term grounding needed by architecture.

Maintain `asm-refinement.md` for refinements that affect:

- concurrency or coordination;
- event structure;
- subsystem responsibilities;
- state ownership;
- rule decomposition.

Architecture should extend or refine the inherited ontology and ASM baselines through explicit deltas, not replace them silently.

### Propagate Confidence Conservatively

Do not upgrade requirement confidence because of design eloquence.

If an upstream commitment is accepted but backend verification is deferred, architecture may refine it, but must not imply stronger evidence than actually exists.

New architecture commitments start weaker than inherited validated commitments unless architecture-specific validation is actually run.

Inherited failures remain failures unless explicitly repaired through a new validated delta.

### Define Architecture-Stage Verification Obligations

Create obligations that distinguish between:

- obligations inherited from PRD;
- obligations already supported by inherited backend evidence;
- obligations requiring recheck because architecture changed the formal baseline;
- obligations newly introduced by architecture;
- obligations blocked by contested or deferred upstream material.

### Produce Companions

Maintain the companion folder with:

- `architecture.md` — architecture artifact with status block;
- `design-decisions.md` — explicit major design choices with inherited/new distinction;
- `architecture-deltas.md` — architecture-level delta ledger;
- `architecture-validation-status.md` — architecture-facing validation and evidence summary;
- `ontology-refinement.md` — ontology extensions or refinements caused by architecture;
- `asm-refinement.md` — ASM refinements caused by architecture;
- `verification-obligations.md` — inherited and architecture-stage obligations, including recheck needs;
- `provenance.md` — architecture section to requirement and delta mapping;
- `local-validation.md` — unresolved conflicts, risks, and repair proposals.

### Handoff

End with:

- architecture path and companion folder;
- inherited requirement coverage summary;
- architecture-level delta summary;
- ontology and ASM refinement summary;
- recheck obligations triggered by architecture decisions;
- inherited and newly introduced uncertainty posture;
- recommended next workflow: `formally-bmad-dsl-epics` for planning refinement over the architecture-stage validated baseline.
