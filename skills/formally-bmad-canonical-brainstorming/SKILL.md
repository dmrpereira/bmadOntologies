---
name: formally-bmad-canonical-brainstorming
description: Brainstorms through a canonical DSL while maintaining ontology and system-model projections. Use when the user requests to 'run canonical formal brainstorming', 'brainstorm into a DSL with ontology and system model', or 'create a formal specification model from brainstorming'.
---

# formally-bmad-canonical-brainstorming

## Overview

This workflow helps you run interactive brainstorming as formal specification drafting without exposing raw formal logic as the primary user surface. Act as a BMad brainstorming facilitator whose authoritative artifact is a controlled conceptual DSL in Markdown, while a formal ontology and a formal system model are continuously maintained from that same surface.

The three layers are asymmetric:

- the canonical DSL is the only authoritative user-facing artifact;
- the ontology is a maintained projection for concept grounding and semantic constraints;
- the system model is a maintained projection for behavior, state, and evolution.

Do not treat these as three peer artifacts. The ontology and system model must stay subordinate to the canonical DSL, and must be revised when the canonical surface changes.

This workflow does not itself claim mechanized verification. Its outputs are structured formalization artifacts prepared for later export, checking, and refinement.

## Conventions

- Bare paths resolve from the skill root.
- `{project-root}`-prefixed paths resolve from the project working directory.
- `{skill-name}` resolves to the skill directory basename.

## On Activation

Load available config from `{project-root}/_bmad/config.yaml` and `{project-root}/_bmad/config.user.yaml` (root level and `formally-bmad` section). Resolve these values, using setup defaults only when config is absent:

- `formally_bmad_project_root`: `{project-root}/_bmad/formally-bmad`
- `formally_bmad_canonical_model_path`: `{project-root}/_bmad/formally-bmad/canonical`
- `formally_bmad_validation_strictness`: `stage-aware`
- `formally_bmad_report_format`: `markdown,html`

If `{formally_bmad_project_root}` or `{formally_bmad_canonical_model_path}/status.md` is missing, stop and direct the user to run `formally-bmad-setup`.

If `--headless` or `-H` is invoked, require an input brief or source artifact path. Without one, create the workspace and stop with a report saying interactive brainstorming needs user input.

## Workflow

### Open the Modeling Conversation

Invite the user to share goals, actors, resources, lifecycle expectations, rules, exceptions, uncertainties, and competing ideas. Keep the live conversation readable and generative. The user should not need to speak in OWL, EFSM, Alloy, or TLA+ terms to make progress.

### Initialize Workspace

Once the topic is known, run:

```bash
python3 scripts/brainstorm_workspace.py --project-root {project-root} --module-root "{formally_bmad_project_root}" --topic "{topic-slug}"
```

The helper creates a companion folder under `{formally_bmad_project_root}/artifacts/brainstorming/` with a canonical surface, two formal projections, and supporting provenance and validation files.

### Maintain the Canonical Surface

Treat `canonical-surface.md` as the authoritative artifact produced during the session. Keep it in structured Markdown with constrained sections and tables, not free-form prose only.

The canonical surface should normally maintain:

- scope and modeling intent;
- concepts, actors, resources, and roles;
- relations and cardinalities;
- states and substates;
- events and actions;
- guards, effects, and invariants;
- goals, non-goals, assumptions, alternatives, and open questions.

Prefer one stable vocabulary. If the user says the same idea in multiple ways, normalize it in the canonical surface and preserve informal wording only in provenance or brainstorming notes.

### Maintain the Ontology Projection

Treat `ontology-projection.md` as a projection from the canonical surface, not as an independent source of truth.

The ontology projection should reflect:

- concept classes and subclasses;
- object and data properties;
- domain/range expectations;
- class disjointness where the user is confident;
- cardinality-style semantic constraints;
- candidate mappings to external ontologies when relevant.

Use OWL 2 DL as the target ontology language. When a human-readable ontology rendering is useful, prefer Manchester-style expressions or disciplined structured English rather than raw RDF serialization.

Do not force behavioral details into the ontology projection when they belong in the system model.

### Maintain the System-Model Projection

Treat `system-model.md` as a projection from the canonical surface for behavior and evolution.

The system-model projection should reflect a restricted hierarchical typed EFSM:

- finite control states;
- optional state hierarchy;
- typed variables or data state;
- events and triggers;
- guards;
- transition effects;
- state invariants;
- explicit notes on excluded semantics.

Prefer a deliberately restricted semantics over full UML state-machine expressiveness. Avoid introducing rich pseudostates, history, unrestricted orthogonal concurrency, or other semantics-heavy features unless the user explicitly needs them and the skill records the added complexity.

### Keep Alternatives Structured

When the user explores competing designs, preserve them as alternatives with explicit implications and decision conditions. Represent unresolved differences as alternatives or open questions, not as silent contradictions across artifacts.

### Clarify Only When Projection Quality Depends On It

Ask concise follow-up questions when a missing distinction blocks one of these outcomes:

- stable concept grounding in the ontology;
- a coherent state or transition structure in the system model;
- safe promotion of a decision into the canonical model.

Explain which layer the ambiguity is blocking.

### Promote Converged Decisions

When the user converges, convert stable canonical surface elements into candidate or accepted-for-validation deltas. Cite the relevant canonical surface section and identify which ontology and system-model projections were updated as a consequence.

Submit promoted deltas to `formally-bmad-agent-steward` through `Accept Canonical Delta`. Keep unaccepted decisions in the brainstorming companion until conflicts are resolved.

### Produce Companions

Maintain the companion folder with:

- `brainstorm.md` for readable conversational capture;
- `canonical-surface.md` for the authoritative structured DSL;
- `ontology-projection.md` for the OWL 2 DL-oriented projection;
- `system-model.md` for the restricted hierarchical typed EFSM projection;
- `candidate-delta.md` for steward-facing promoted assertions;
- `provenance.md` for source-to-model traceability;
- `local-validation.md` for ambiguity, projection drift, blockers, and next steps.

### Handoff

End with:

- the brainstorming artifact path;
- the canonical surface path;
- the ontology projection path;
- the system-model path;
- the companion folder path;
- promoted decisions and still-open questions;
- an explicit note stating whether mechanized verification has or has not occurred;
- a note that downstream workflows must refine from the canonical surface, not fork disconnected formal drafts;
- recommended next workflow: `formally-bmad-ontology-alignment` for concept grounding, `formally-bmad-formal-prd` for requirements, or `formally-bmad-formal-verification` for tool-backed checking and export planning.
