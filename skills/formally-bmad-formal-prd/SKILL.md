---
name: formally-bmad-formal-prd
description: Creates PRDs with formal grounding. Use when the user requests to 'create formal PRD', 'formalize PRD', or 'write PRD with formally-bmad'.
---

# formally-bmad-formal-prd

## Overview

This workflow creates or formalizes a BMad-style PRD while incrementally updating Formally BMAD with rigorous English formalization, candidate/accepted requirements, provenance, validation findings, and downstream verification obligations. Act as a product requirements facilitator with a formal specification layer: keep the PRD readable, but make each accepted requirement traceable, explicit about its verification path, and honest about what is or is not mechanized yet.

## Conventions

- Bare paths (e.g. `scripts/prd_workspace.py`) resolve from the skill root.
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

If `--headless` or `-H` is invoked, require source material such as brainstorming output, an existing PRD path, or a product brief. Without source material, stop after creating the workspace and report that PRD formalization needs product intent.

## Workflow

### Establish PRD Intent

Gather or load the product intent, stakeholders, goals, non-goals, constraints, assumptions, success criteria, and source artifacts. Prefer existing Formally BMAD brainstorming outputs and ontology-aligned concepts when available.

Keep the PRD BMad-style and readable. Formal details belong in the companion files and formal status block.

### Initialize Workspace

Run the deterministic workspace helper once the PRD title or source path is known:

```bash
python3 scripts/prd_workspace.py --project-root {project-root} --module-root "{formally_bmad_project_root}" --title "{prd-title-or-source-slug}"
```

The helper creates `{formally_bmad_project_root}/artifacts/prd/<safe-title>/` with starter files for the PRD companion, requirements, formalization, candidate delta, verification obligations, provenance, and local validation.

### Draft or Formalize the PRD

Produce or update the source PRD as normal Markdown. Include a concise formal status block:

- canonical model version or pending delta;
- consistency status;
- last formalization timestamp;
- open ambiguities/blockers;
- companion folder link.

If formalizing an existing PRD, preserve source meaning and avoid rewriting requirements unless the user accepts a repair proposal.

### Extract Requirements

Map PRD content into formalizable units:

- goals and non-goals;
- functional requirements;
- non-functional requirements;
- constraints;
- assumptions;
- domain concepts;
- stakeholder commitments;
- exclusions and deferred scope.

Use `candidate` for draft requirements and `accepted` only when the user clearly confirms the requirement as a commitment. Use `open-question` when sound formalization is blocked.

For every requirement, record these classifications explicitly rather than inferring them silently:

- `formalization_status`: `not-yet-formalized`, `rigorous-english`, `logic-shaped`, or `logic-native`;
- `mechanization_class`: `direct-tool-checkable`, `requires-additional-modeling`, `not-mechanized-in-mvp`, or `blocked-by-ambiguity`;
- `verification_mode`: one or more of `smt`, `fol`, `sat`, `temporal`, `ontology`, `proof-assistant`, `test`, `manual-review`, or `mixed`;
- `claim_strength`: `structured-only`, `planned-for-tool-check`, or `tool-backed-validated`.

Do not decide privately that a requirement "is really a test requirement" or "cannot be formalized" without writing that classification and the reason into the companion artifacts.

### Formalize and Check Ambiguity

For each requirement, write rigorous English that identifies:

- subject and predicate;
- preconditions and scope;
- obligation, permission, or prohibition;
- measurable success condition if available;
- dependency on assumptions or external concepts;
- likely logic family: FOL, description logic, temporal logic, or meta/HOL only when needed.

Ask clarifying questions only when ambiguity blocks useful formalization or validation. PRD-stage tolerance is moderate: unresolved questions may remain, but accepted requirements must be coherent.

Where a requirement is not directly tool-checkable with the currently installed MVP toolchain, say which of these is true:

- the requirement is still formalizable, but needs a richer model or translation than the current artifact provides;
- the requirement is formalizable only after architecture/story refinement;
- the requirement is presently represented as a test or review obligation for MVP reasons;
- the requirement is blocked by ambiguity and cannot yet be soundly classified.

Do not claim or imply that a requirement has been formally verified merely because you can imagine a possible future encoding in FOL, SMT, temporal logic, or a proof assistant.

### Define Verification Obligations

Create initial downstream verification obligations for accepted requirements:

- what must later be shown by architecture;
- what must later be covered by epics/stories;
- what automated checks or model properties may be needed;
- formal coverage status.

Every accepted requirement must also get:

- a named primary verification path for this stage;
- a fallback path if the preferred mechanized check is not available yet;
- the concrete reason when the current stage uses `test` or `manual-review` instead of a tool-backed check;
- the additional artifact, translation, or model detail required to upgrade it later to a stronger mechanized check, if such an upgrade is plausible.

If you downgrade a requirement from a possible mechanized check to a test-backed or review-backed obligation for MVP reasons, state that downgrade explicitly in user-visible output.

### Submit to Steward

Submit PRD deltas to `formally-bmad-agent-steward` through `Accept Canonical Delta` and, for accepted requirements, `Validate Update Consistency`.

If the steward reports a contradiction, block promotion of the affected accepted requirement until resolved or explicitly overridden. If the user overrides, the model must be marked inconsistent by the steward.

### Produce Companions

Maintain the companion folder with:

- `prd.md` — PRD artifact or source link and formal status block;
- `requirements.md` — requirement inventory, states, mechanization class, verification mode, and current claim strength;
- `formalization.md` — rigorous English formalization plus any logic-family placement and explicit non-mechanization rationale;
- `candidate-delta.md` — canonical assertions and logic-family placement;
- `verification-obligations.md` — downstream coverage and check obligations, including why each obligation is tool-backed, degraded, test-backed, review-backed, or blocked;
- `provenance.md` — PRD section to assertion mapping;
- `local-validation.md` — ambiguity, blockers, steward responses, and repair proposals.

### Handoff

End with:

- PRD path and companion folder;
- accepted, candidate, and open-question requirements;
- steward validation status;
- formal coverage baseline, including counts by mechanization class and verification mode;
- any accepted requirements that are not yet directly tool-checkable, with the written reason for each;
- recommended next workflow: `formally-bmad-formal-architecture`, or `formally-bmad-ontology-alignment` if domain concepts need grounding first.
