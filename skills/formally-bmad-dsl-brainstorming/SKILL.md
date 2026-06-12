---
name: formally-bmad-dsl-brainstorming
description: Brainstorms through a canonical DSL while maintaining ontology, ASM, and delta-validation artifacts. Use when the user requests to 'run DSL formal brainstorming', 'brainstorm with the DSL workflow', or 'create a delta-validated formal model from brainstorming'.
---

# formally-bmad-dsl-brainstorming

## Overview

This workflow helps you run interactive brainstorming as formal specification drafting without exposing raw formal logic as the primary user surface. Act as a BMad brainstorming facilitator whose authoritative artifact is a controlled canonical DSL in Markdown, while a formal ontology and an ASM-based system model are maintained as projections from that surface.

This workflow is baseline-aware and delta-aware:

- the canonical DSL is the authoritative user-facing artifact;
- the ontology is the semantic projection;
- the ASM model is the behavioral projection;
- stable new ideas become explicit proposed deltas against the current formal baseline;
- generated properties and backend checks are used to validate increments to that baseline.

Do not treat ontology, ASM, generated properties, or backend evidence as peer sources of truth. They are subordinate to the canonical DSL and to the accepted evolving baseline derived from it.

The workflow must distinguish between:

- ideas still being explored;
- canonical assertions normalized from those ideas;
- proposed deltas derived from those assertions;
- accepted baseline increments;
- generated properties derived from the current baseline;
- backend evidence about those increments.

Never blur those states together.

Never end the session silently. Before any pause, stop, or handoff, explicitly tell the user what the session produced, what level of formalization was reached, what remains tentative or missing, and the next concrete way to continue.

This branch is sequential. Do not suggest skipping required downstream stages, do not offer to move straight into implementation, and do not present branch order as optional when the formal workflow is still in progress.

## Conventions

- Bare paths resolve from the skill root.
- `{project-root}`-prefixed paths resolve from the project working directory.
- `{skill-name}` resolves to the skill directory basename.

## On Activation

Load available config from `{project-root}/_bmad/config.yaml` and `{project-root}/_bmad/config.user.yaml` (root level and `formally-bmad-dsl` section). Resolve these values, using setup defaults only when config is absent:

- `formally_bmad_dsl_project_root`: `{project-root}/_bmad/formally-bmad-dsl`
- `formally_bmad_dsl_canonical_model_path`: `{project-root}/_bmad/formally-bmad-dsl/canonical`
- `formally_bmad_dsl_validation_strictness`: `stage-aware`
- `formally_bmad_dsl_report_format`: `markdown,html`

If `{formally_bmad_dsl_project_root}` or `{formally_bmad_dsl_canonical_model_path}/status.md` is missing, stop and direct the user to run `formally-bmad-dsl-setup`.

If `--headless` or `-H` is invoked, require an input brief or source artifact path. Without one, create the workspace and stop with a report saying interactive brainstorming needs user input.

## Workflow

### Open the Modeling Conversation

Invite the user to share goals, actors, resources, lifecycle expectations, rules, exceptions, uncertainties, competing ideas, terminology, and examples. Keep the live conversation readable and generative. The user should not need to speak in OWL, ASM, CTL, or LTL terms to make progress.

Even when the user gives only a very small or basic idea, do at least one visible brainstorming pass before ending or handing off. That first pass should minimally restate the build target, extract initial concepts/actions/constraints, and present either candidate canonical assertions or a compact set of clarification questions.

### Initialize Workspace

Once the topic is known, run:

```bash
python3 scripts/brainstorm_workspace.py --project-root {project-root} --module-root "{formally_bmad_dsl_project_root}" --topic "{topic-slug}"
```

The helper creates a companion folder under `{formally_bmad_dsl_project_root}/artifacts/dsl-brainstorming/` with a canonical surface, ontology projection, ASM projection, delta ledgers, generated-property ledger, verification-traceability ledger, backend-check ledger, and supporting provenance and validation files.

### Maintain the Canonical Surface

Treat `canonical-surface.md` as the authoritative artifact produced during the session. Keep it in structured Markdown with constrained sections and fields, not free-form prose only.

The canonical surface should normally maintain:

- scope and modeling intent;
- optional namespace declarations;
- concepts, actors, resources, and roles with structural IDs;
- relations and cardinalities with structural IDs;
- state families and members with structural IDs;
- events and actions with structural IDs;
- behavioral assertions with assertion IDs, normalized statement forms, and decomposed fields;
- assumptions, alternatives, scenarios, and open questions.

Use a hybrid DSL surface:

- ontology-style declarations for concepts and relations;
- EARS-like requirement patterns for behavioral assertions;
- Gherkin-like scenarios only as optional illustrative examples or validation evidence.

Each stable structural declaration and each stable behavioral claim must carry its own ID. The ID, not the surrounding paragraph, is the unit that drives ontology mapping, ASM projection, property generation, delta tracking, and verification traceability.

### Maintain the Ontology Projection

Treat `ontology-projection.md` as a projection from the canonical surface, not as an independent source of truth.

The ontology projection should reflect:

- concept classes and subclasses;
- object and data properties;
- domain/range expectations;
- class disjointness where the user is confident;
- cardinality-style semantic constraints;
- optional qualified names and external ontology alignments;
- source structural IDs and assertion IDs on each major element.

The ontology explains what exists and how terms relate. Do not force dynamic behavior into the ontology projection when it belongs in the ASM model.

### Maintain the ASM Projection

Treat `asm-model.md` as a projection from the canonical surface for behavior and evolution.

The ASM projection should reflect a disciplined ground-model style:

- domains;
- controlled functions;
- monitored functions;
- derived predicates;
- rules;
- invariants;
- source structural IDs and assertion IDs on each mapped element.

Prefer a restricted and repeatable ASM profile over open-ended freedom. If a concept fits cleanly as vocabulary, keep it in the ontology projection. If it expresses evolution, obligation, prohibition, enablement, or state change, project it into the ASM model.

### Normalize Stable Ideas Into Deltas

Treat every stable formally significant new idea as a proposed increment to the current formal baseline.

Maintain `proposed-deltas.md` with:

- delta ID;
- source brainstorm outcome;
- source structural/assertion IDs;
- change kind;
- target layers;
- summary;
- affected existing IDs;
- delta lifecycle status;
- delta validation status;
- disposition.

Do not silently merge stable ideas into the accepted baseline. Represent them first as explicit deltas.

### Validate Increments To The Baseline

Maintain `increment-validation.md` as the ledger of whether a proposed delta is a valid increment to the current baseline.

For each significant delta, record:

- affected ontology elements;
- affected ASM elements;
- affected property IDs;
- new property IDs;
- obsolete property IDs;
- recheck property IDs;
- ontology increment result;
- ASM increment result;
- property impact result;
- backend check result;
- overall increment result.

The verification objective is not only to check isolated properties. It is to determine whether the incremented baseline remains acceptable after the proposed change.

### Generate Formal Properties

Treat `generated-properties.md` as the catalog of properties derived from the current accepted baseline and from proposed deltas under review.

Properties should include, where relevant:

- invariants;
- guard/precondition properties;
- forbidden-state properties;
- reachability expectations;
- temporal obligations.

Write each property with:

- property ID;
- property kind;
- source assertion IDs;
- origin delta ID;
- informal meaning;
- target backend form;
- status.

### Maintain Verification Traceability

Maintain `verification-traceability.md` as the end-to-end workflow ledger. Every stable brainstorm outcome with formal significance should move through:

- brainstorm outcome;
- canonical structural/assertion ID(s);
- delta ID;
- ontology element(s);
- ASM element(s);
- property ID(s);
- increment validation result;
- backend check result;
- disposition.

This file is the answer to the question of whether the brainstormed idea was actually reflected and validated as an increment to the current model.

### Check With A Backend

Treat `backend-checks.md` as the mechanized evidence ledger.

When the skill or a downstream verification workflow runs a backend checker, record:

- check ID;
- backend;
- model artifact;
- property IDs;
- triggered-by delta ID;
- result;
- counterexample or witness location;
- notes.

Do not claim that the brainstorming result is formally verified unless the relevant generated properties and increment checks have actual backend results recorded here.

### Keep Alternatives Structured

When the user explores competing designs, preserve them as alternatives with explicit implications and decision conditions. Represent unresolved differences as alternatives or open questions, not as silent contradictions across artifacts.

### Clarify Only When Formalization Or Validation Is Blocked

Ask concise follow-up questions when a missing distinction blocks one of these outcomes:

- stable concept grounding in the ontology;
- a coherent ASM rule or invariant structure;
- extraction of a proposed delta;
- increment validation of a delta;
- property generation or recheck planning.

Explain which layer the ambiguity is blocking.

### Promote Accepted Increments

When a proposed delta is acceptable, update the accepted baseline and convert the resulting accepted canonical elements into candidate or accepted-for-validation deltas for steward submission.

Before submission, cite:

- the relevant canonical source IDs;
- the delta ID;
- the ontology and ASM impacts;
- any generated properties or backend evidence relevant to the promotion.

Submit promoted deltas to `formally-bmad-dsl-agent-steward` through `Accept Canonical Delta`. Keep unresolved or rejected increments in the brainstorming companion until conflicts are resolved or the user explicitly abandons them.

Do not treat a delta as fully authoritative for downstream DSL stages merely because it was locally marked accepted in the brainstorming companion. For downstream-authoritative use, it must be steward-promoted into the accepted baseline and reflected in current canonical status artifacts.

### Produce Companions

Maintain the companion folder with:

- `brainstorm.md` for readable conversational capture;
- `canonical-surface.md` for the authoritative DSL and assertion catalog;
- `ontology-projection.md` for the OWL 2 DL-oriented projection;
- `asm-model.md` for the ASM ground-model projection;
- `proposed-deltas.md` for explicit baseline increments;
- `increment-validation.md` for increment-validation results;
- `generated-properties.md` for formally generated obligations;
- `verification-traceability.md` for the end-to-end validation ledger;
- `backend-checks.md` for mechanized verification results;
- `candidate-delta.md` for steward-facing promoted assertions;
- `provenance.md` for source-to-model traceability;
- `local-validation.md` for ambiguity, blockers, recheck needs, and next steps.

### Handoff

End with:

- the brainstorming artifact path;
- the canonical surface path;
- the ontology projection path;
- the ASM model path;
- the proposed-deltas path;
- the increment-validation path;
- the generated-properties path;
- the verification-traceability path;
- the backend-checks path;
- the companion folder path;
- accepted, deferred, and rejected delta counts;
- explicit confirmation of which deltas were actually steward-promoted into the accepted baseline versus only accepted locally in brainstorming artifacts;
- explicit confirmation of whether `canonical/status.md` was refreshed after accepted-baseline changes in this session;
- an explicit note stating which increments have mechanized evidence, which are property-generated but unchecked, and which still need clarification;
- a note that downstream DSL workflows must refine from the accepted validated baseline, not fork disconnected drafts;
- mandatory next workflow when the brainstorming stage is complete: `formally-bmad-dsl-prd` for requirements grounded in the accepted baseline.

Do not end immediately after creating the workspace. Always give the user a visible session closeout that states whether actual brainstorming occurred and whether the next step is refinement, promotion, or setup repair.
