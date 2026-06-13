# DSL Architecture Consumption Contract

## Purpose

This note defines how `formally-bmad-dsl-architecture` should consume outputs from the upstream DSL branch, especially:

- `formally-bmad-dsl-prd`
- and, where needed for grounding, `formally-bmad-dsl-brainstorming`

## Design Goal

The architecture skill in this branch should not treat the PRD as a plain prose requirements document.

It should consume:

- accepted PRD requirements;
- accepted upstream deltas;
- inherited increment-validation state;
- inherited ontology and ASM baseline context;
- inherited backend evidence status;
- new architecture-level deltas introduced by structural design choices.

So architecture becomes:

- a refinement of an evolving validated baseline,
- not a disconnected redesign stage.

## Upstream Source Artifacts

`formally-bmad-dsl-architecture` should consume the following artifacts when available.

### Required from `formally-bmad-dsl-prd`

- `prd.md`
- `requirements.md`
- `formalization.md`
- `accepted-deltas.md`
- `validation-status.md`
- `verification-obligations.md`
- `provenance.md`

### Required inherited baseline context

Either directly from PRD artifacts or, if needed, by following their references:

- `canonical-surface.md`
- `ontology-projection.md`
- `asm-model.md`
- `generated-properties.md`
- `proposed-deltas.md`
- `increment-validation.md`
- `backend-checks.md`

### Optional supporting context

- `brainstorm.md`
- `local-validation.md`

## Consumption Principle

The architecture skill must design against the **currently accepted validated baseline**, not against every brainstormed possibility.

Authority order:

1. accepted PRD requirements
2. accepted deltas and validation records
3. inherited ontology and ASM baseline
4. verification obligations and backend evidence
5. earlier brainstorming narrative

If prose and formal baseline disagree, the accepted validated baseline wins unless architecture explicitly proposes a new delta.

## What Architecture Is Allowed To Do

The architecture skill may:

- refine accepted requirements into components, boundaries, interactions, and architectural constraints;
- introduce architecture-level deltas;
- tighten ontology structure for design purposes;
- refine the ASM baseline where architectural decisions affect behavior or coordination;
- introduce new verification obligations driven by architectural commitments.

It may not:

- silently redefine accepted upstream requirements;
- silently ignore failed or deferred validation states;
- present unsupported architecture assumptions as if they were validated inherited facts.

## Eligible Upstream Inputs

### 1. Requirements eligible for architectural commitment

Requirements are eligible as architecture-driving inputs when they are:

- accepted PRD requirements;
- tied to accepted deltas;
- not currently marked as formally contested.

Requirements with weaker evidence may still be used, but only with explicit uncertainty markers.

### 2. Deferred and contested material

The architecture skill may consume:

- deferred deltas;
- contested requirements;
- assumptions;

but only as:

- risks;
- architecture alternatives;
- unresolved constraints;
- triggers for architecture-level validation needs.

They must not become silently accepted architectural facts.

## Architecture-Level Refinement Model

Architecture in this branch is not only a structural document. It is a refinement layer that may itself create new formal increments.

That means architecture output should include:

1. architectural decisions derived from accepted baseline material;
2. architecture-level deltas;
3. architecture-level impacts on ontology;
4. architecture-level impacts on ASM behavior;
5. architecture-level impacts on generated properties and recheck obligations.

## Required Output Semantics

The architecture skill should produce outputs that distinguish:

- inherited validated commitments;
- architecture interpretations of those commitments;
- new architectural commitments;
- new architectural deltas requiring validation.

This distinction is critical.

Otherwise architecture will blur:

- what was already accepted upstream;
- what is newly introduced by design.

## Required Architecture Artifacts

I recommend the new architecture branch produce at least:

- `architecture.md`
- `design-decisions.md`
- `architecture-deltas.md`
- `architecture-validation-status.md`
- `ontology-refinement.md`
- `asm-refinement.md`
- `verification-obligations.md`
- `provenance.md`
- `local-validation.md`

## Recommended File Roles

### architecture.md

Human-facing architecture document with:

- architectural overview;
- major components and boundaries;
- interaction structure;
- architecture status block with baseline/evidence posture.

### design-decisions.md

Explicit record of:

- major architectural choices;
- what upstream requirement or delta drove them;
- whether each decision is inherited, interpretive, or newly introduced.

### architecture-deltas.md

Ledger of architecture-level changes proposed against the accepted upstream baseline.

These are analogous to `proposed-deltas.md`, but architecture-specific.

### architecture-validation-status.md

Architecture-facing validation summary including:

- inherited validation state;
- architecture-induced recheck obligations;
- unresolved design conflicts;
- backend evidence implications.

### ontology-refinement.md

Refinement of the inherited ontology baseline where architectural concepts require:

- component-level concepts;
- interface-level relations;
- deployment or responsibility concepts;
- updated term grounding.

### asm-refinement.md

Refinement of the inherited ASM baseline where architecture decisions affect:

- concurrency or coordination;
- event structure;
- subsystem responsibilities;
- state ownership;
- rule decomposition.

### verification-obligations.md

Architecture-stage verification obligations should include:

- obligations inherited from PRD;
- new obligations introduced by architecture;
- recheck obligations triggered by architecture deltas.

## Architecture Delta Rules

Every new architectural commitment with formal significance should create an architecture-level delta.

Typical triggers:

- introducing subsystem boundaries that change responsibility allocation;
- refining state ownership or event flow;
- decomposing one requirement into distributed interactions;
- introducing new constraints such as consistency, ordering, fault handling, or synchronization.

Each architecture delta should identify:

- source requirement IDs;
- source upstream delta IDs;
- ontology impacts;
- ASM impacts;
- property impacts;
- recheck obligations.

## Confidence Propagation Rules

Architecture must propagate confidence conservatively, just as PRD does.

### Rule A1

Do not upgrade requirement confidence because of design eloquence.

If an upstream commitment is accepted but backend verification is deferred, architecture may refine it, but it must not imply stronger evidence than actually exists.

### Rule A2

New architecture commitments start weaker than inherited validated commitments.

Unless architecture-specific validation is run, new architecture-level deltas should begin as:

- proposed;
- under review;
- validation pending.

### Rule A3

Inherited failures remain failures.

If an upstream increment is contested or failed, architecture may respond to it, but must not silently erase it.

## Relationship To Ontology

Architecture should consume the ontology baseline as semantic grounding, then refine it where architecture adds:

- component concepts;
- service/interface concepts;
- dependency relations;
- ownership or allocation relations.

The architecture skill should not replace the ontology baseline. It should extend or refine it through explicit deltas.

## Relationship To ASM

Architecture should consume the ASM baseline as the inherited behavioral model, then refine it where architecture changes:

- control distribution;
- interaction order;
- responsibility for state changes;
- synchronization or coordination patterns;
- event decomposition across components.

Architecture is therefore a likely stage where the ASM model becomes more structured and where recheck obligations become more frequent.

## Recheck Obligation Rules

Architecture should trigger recheck obligations when it:

- splits one behavioral rule across components;
- introduces new coordination logic;
- changes timing/order assumptions;
- changes state ownership;
- introduces new fault-handling behavior;
- changes the interpretation of an accepted negative or safety assertion.

These recheck obligations must be explicit in architecture outputs.

## Minimal Acceptance Condition For Starting Architecture

The DSL architecture skill is allowed to begin when PRD provides at least:

- accepted requirement inventory;
- accepted deltas;
- validation status summary;
- inherited ontology and ASM baseline references.

It does not require that every requirement already has full backend evidence, but it must preserve uncertainty explicitly.

## Stronger Acceptance Condition For High-Risk Architecture

The architecture skill should recommend further upstream or immediate architecture-stage validation before finalizing if:

- central coordination requirements remain formally contested;
- negative assertions affecting safety or integrity remain unchecked;
- architecture introduces distribution/concurrency that materially changes ASM interpretation;
- major design decisions depend on deferred deltas.

## Handoff To Later DSL Skills

`formally-bmad-dsl-architecture` should become the upstream source for:

- `formally-bmad-dsl-epics`
- `formally-bmad-dsl-stories`
- `formally-bmad-dsl-verification`

It should therefore emit:

- accepted architecture decisions with source requirement and delta lineage;
- architecture-level deltas and validation status;
- ontology and ASM refinements;
- updated verification obligations and recheck sets.

## Summary

The architecture skill in this branch should act as:

- a design refinement stage over an accepted validated baseline;
- a producer of new architecture-level deltas;
- a refiner of ontology and ASM baselines;
- a trigger point for recheck obligations caused by structural design decisions.

It must preserve the distinction between inherited validated commitments and newly introduced design commitments, or the whole branch loses epistemic discipline.
