---
name: formally-bmad-formal-architecture
description: Creates architecture with formal alignment. Use when the user requests to 'create formal architecture', 'formalize architecture', or 'check architecture against formal PRD'.
---

# formally-bmad-formal-architecture

## Overview

This workflow creates or formalizes BMad architecture artifacts with explicit alignment to accepted PRD requirements and the evolving Formally BMAD canonical model. It keeps architecture readable while producing rigorous English formalization, component/interface constraints, temporal properties where relevant, PRD alignment evidence, and downstream implementation constraints.

## Conventions

- Bare paths (e.g. `scripts/architecture_workspace.py`) resolve from the skill root.
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

If `--headless` or `-H` is invoked, require a PRD, accepted requirement set, existing architecture artifact, or architecture brief. Without that source material, create only the workspace and report that formal architecture needs accepted requirements or architecture intent.

## Workflow

### Establish Architecture Context

Load or ask for:

- accepted PRD requirements and verification obligations;
- current canonical model status;
- known constraints, assumptions, and ontology-aligned concepts;
- technology choices, components, interfaces, data flows, lifecycle states, and deployment constraints;
- existing architecture artifact if formalizing brownfield work.

Architecture validation is stricter than PRD validation because architecture starts constraining implementation.

### Initialize Workspace

Run the deterministic workspace helper once the architecture title or source path is known:

```bash
python3 scripts/architecture_workspace.py --project-root {project-root} --module-root "{formally_bmad_project_root}" --title "{architecture-title-or-source-slug}"
```

The helper creates `{formally_bmad_project_root}/artifacts/architecture/<safe-title>/` with starter files for architecture, decisions, components, interfaces, constraints, temporal properties, PRD alignment, candidate delta, provenance, and local validation.

### Create or Formalize Architecture

Produce or update a BMad-style architecture document. Include a concise formal status block:

- canonical model version or pending delta;
- consistency/alignment status;
- last formalization timestamp;
- open ambiguities/blockers;
- companion folder link.

If formalizing an existing architecture, preserve source meaning and avoid rewriting decisions unless the user accepts a repair proposal.

### Formalize Architecture Decisions

Represent architecture commitments as formalizable units:

- components and responsibilities;
- interfaces and contracts;
- dependencies and ordering constraints;
- data ownership and flow constraints;
- deployment/runtime assumptions;
- invariants and forbidden states;
- lifecycle or behavioral properties.

Prefer FOL/DL for structural commitments and temporal logic for lifecycle, ordering, state, and behavior. Use meta/HOL only when strictly needed.

### Check PRD Alignment

For each accepted PRD requirement or verification obligation, classify architecture support:

- `satisfies`;
- `partially-satisfies`;
- `constrains`;
- `defers`;
- `conflicts`;
- `unmapped`.

Conflicts against accepted PRD requirements block promotion of the affected architecture decision unless resolved or explicitly overridden through the steward.

### Tighten Implementation Constraints

Create downstream constraints for epics and stories:

- architectural rules stories must obey;
- acceptance criteria implications;
- required verification conditions;
- unresolved assumptions or blockers that must not be hidden during implementation planning.

### Submit to Steward

Submit architecture deltas to `formally-bmad-agent-steward` through `Accept Canonical Delta` and `Validate Update Consistency`.

Accepted implementation-facing architecture decisions should receive stricter validation than PRD candidates. If validation reports contradiction, block workflow progress until resolved or explicitly overridden.

### Produce Companions

Maintain the companion folder with:

- `architecture.md` — architecture artifact or source link and formal status block;
- `decisions.md` — architecture decision inventory and states;
- `components.md` — component responsibilities and constraints;
- `interfaces.md` — interface contracts and dependencies;
- `constraints.md` — invariants, assumptions, and forbidden states;
- `temporal-properties.md` — lifecycle/order/state behavior when relevant;
- `prd-alignment.md` — requirement-to-architecture alignment;
- `candidate-delta.md` — canonical assertions and logic-family placement;
- `implementation-constraints.md` — downstream epic/story obligations;
- `provenance.md` — architecture section to assertion mapping;
- `local-validation.md` — ambiguity, blockers, steward responses, and repair proposals.

### Handoff

End with:

- architecture artifact path and companion folder;
- PRD alignment summary;
- accepted architecture constraints and open blockers;
- steward validation status;
- downstream implementation constraints;
- recommended next workflow: `formally-bmad-formal-epics`.
