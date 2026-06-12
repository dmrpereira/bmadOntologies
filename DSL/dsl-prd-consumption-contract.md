# DSL PRD Consumption Contract

## Purpose

This note defines how the proposed `formally-bmad-dsl-prd` skill should consume outputs from `formally-bmad-dsl-brainstorming`.

This contract is specific to the new parallel `formally-bmad-dsl-*` branch and must not be assumed to apply to the existing `formally-bmad-formal-*` branch.

## Design Goal

The DSL PRD skill should not consume brainstorming output as a loose idea dump or a single static formal model.

It should consume:

- an evolving canonical baseline;
- accepted assertions;
- accepted deltas;
- current increment-validation outcomes;
- current backend evidence state.

That means the PRD is grounded not only in what the team wants the system to do, but also in what the current formal baseline can already justify or what it still leaves unresolved.

## Upstream Source Artifacts

`formally-bmad-dsl-prd` should consume the following upstream artifacts when available:

### Required primary artifacts

- `canonical-surface.md`
- `proposed-deltas.md`
- `increment-validation.md`

### Required projection context

- `ontology-projection.md`
- `asm-model.md`

### Required verification context

- `generated-properties.md`
- `verification-traceability.md`
- `backend-checks.md`

### Optional supporting context

- `brainstorm.md`
- `provenance.md`
- `local-validation.md`

## Consumption Principle

The PRD skill must consume the **accepted current baseline**, not the full undifferentiated history.

So it should treat source material in this order of authority:

1. accepted canonical assertions
2. accepted deltas and their validation records
3. currently valid ontology and ASM projections
4. generated properties and backend evidence
5. brainstorm narrative and provenance

If lower-authority artifacts conflict with higher-authority ones, higher-authority artifacts win.

## Eligibility Rules

The PRD skill must decide which upstream items are eligible to shape the PRD.

### 1. Eligible canonical assertions

Canonical assertions are eligible PRD inputs when:

- `LifecycleStatus = accepted`
- `KnowledgeStatus = asserted` or `assumption`

Additional rule:

- `open_question` items are not PRD commitments, but may become explicit PRD open issues.

### 2. Eligible deltas

Deltas are eligible when:

- `DeltaLifecycleStatus = accepted`

or, if the workflow wants to surface risk explicitly:

- `DeltaLifecycleStatus = deferred`

Deferred deltas must not be treated as accepted requirement commitments, but they may inform:

- PRD risks;
- unresolved design tensions;
- deferred scope notes;
- formalization gaps.

Rejected deltas must not be treated as source requirements except as provenance or rejected alternatives.

### 3. Eligible validation state

Increment validation outcomes are consumed as requirement-confidence evidence.

The PRD skill should consume:

- ontology increment result;
- ASM increment result;
- property impact result;
- backend check result;
- overall increment result.

These values should affect how strongly the PRD presents a requirement.

## Requirement Confidence Model

The PRD skill should not flatten all accepted assertions into equal-strength requirements.

Instead, each requirement should carry a confidence and evidence interpretation derived from upstream validation state.

## Proposed requirement evidence classes

### `baseline-accepted`

Use when:

- the source assertion is accepted;
- the source delta is accepted;
- increment validation is at least structurally acceptable;
- backend checking may still be deferred.

Interpretation:

- valid formal baseline increment;
- not necessarily mechanized strongly yet.

### `baseline-accepted-with-backend-evidence`

Use when:

- the source assertion is accepted;
- the source delta is accepted;
- backend checks relevant to that increment have passed.

Interpretation:

- strongest PRD confidence class available from brainstorming-stage material.

### `baseline-accepted-with-deferred-verification`

Use when:

- the source assertion is accepted;
- the source delta is accepted;
- backend checks are deferred or not run;
- no failing result exists.

Interpretation:

- requirement is part of the accepted baseline, but stronger mechanized evidence is still pending.

### `deferred-formal-commitment`

Use when:

- the source delta is deferred;
- the requirement is important enough to mention;
- it should not yet be presented as an accepted commitment.

Interpretation:

- unresolved candidate material, not accepted PRD commitment.

### `formally-contested`

Use when:

- increment validation or backend results expose conflict or failure;
- the requirement remains relevant but is not cleanly accepted.

Interpretation:

- should appear in PRD only as a blocker, conflict, or explicit risk.

## What The PRD Skill Must Extract

From the upstream artifacts, the PRD skill should extract:

### 1. Requirement candidates

From:

- accepted behavioral assertions;
- accepted structural assertions that imply product commitments;
- accepted deltas that introduce or modify obligations.

### 2. Domain vocabulary

From:

- concepts;
- relations;
- ontology projection terms;
- optional qualified names if grounding matters.

### 3. Validation-backed constraints

From:

- accepted negative assertions;
- accepted state-driven or conditional constraints;
- ontology semantic constraints;
- validated ASM invariants and property outcomes.

### 4. Unresolved formal risks

From:

- deferred deltas;
- failing increment validation rows;
- failing backend checks;
- open questions with architecture or verification consequences.

## What The PRD Skill Must Preserve

The PRD skill must preserve these distinctions in user-visible output:

- accepted requirement vs deferred idea;
- accepted baseline vs contested baseline;
- backend-evidenced requirement vs deferred-verification requirement;
- asserted requirement vs explicit assumption.

If those distinctions disappear, the PRD corrupts the epistemic meaning of the upstream formal artifacts.

## PRD Artifact Requirements

The new `formally-bmad-dsl-prd` skill should produce a PRD companion set that carries this branch’s stronger upstream semantics.

Recommended artifacts:

- `prd.md`
- `requirements.md`
- `formalization.md`
- `accepted-deltas.md`
- `validation-status.md`
- `verification-obligations.md`
- `provenance.md`
- `local-validation.md`

## Recommended file roles

### prd.md

Human-facing PRD with:

- concise formal status block;
- explicit statement of baseline confidence;
- links to accepted delta and validation artifacts.

### requirements.md

Requirement inventory with:

- source assertion IDs;
- source delta IDs;
- evidence class;
- assumption/assertion distinction;
- validation posture.

### formalization.md

Rigorous English restatement of accepted PRD requirements and the formal interpretation carried forward from the DSL branch.

### accepted-deltas.md

Subset view of accepted deltas relevant to this PRD.

### validation-status.md

PRD-facing summary of:

- which requirements inherit backend evidence;
- which inherit only accepted-but-unchecked increments;
- which remain contested or deferred.

### verification-obligations.md

Forward-looking obligations for architecture and later verification.

This file should distinguish:

- already checked obligations;
- obligations requiring recheck because later stages will refine the model;
- obligations not yet mechanized.

## Filtering Rules

The PRD skill should apply these filters when building the requirement inventory.

### Include directly

- accepted assertions tied to accepted deltas;
- accepted constraints tied to passing or deferred-but-nonfailing validation.

### Include with caution markers

- accepted assertions tied to accepted deltas with deferred backend checks;
- accepted assertions depending on explicit assumptions.

### Include only as risks, open issues, or deferred scope

- deferred deltas;
- contested increments;
- failed backend validations unless explicitly overridden.

### Exclude from accepted requirement set

- rejected deltas;
- superseded assertions unless preserved as provenance;
- unresolved brainstorm fragments without stable assertion form.

## Confidence Propagation Rules

The PRD skill should propagate confidence conservatively.

### Rule P1

Do not upgrade confidence downstream.

If brainstorming only established:

- accepted delta + deferred backend

the PRD skill must not present that as if it were:

- backend-validated.

### Rule P2

Do not erase failure.

If increment validation failed or backend checks failed:

- the requirement may still be discussed;
- but it must be labeled contested, blocked, or deferred.

### Rule P3

Assumptions remain assumptions.

A requirement depending on an explicit assumption must preserve that dependency in PRD artifacts.

## Handoff To Later DSL Skills

`formally-bmad-dsl-prd` should itself become an upstream source for:

- `formally-bmad-dsl-architecture`
- later `formally-bmad-dsl-verification`

It should therefore emit:

- accepted PRD requirements with source assertion and delta IDs;
- PRD-stage delta additions if requirements are refined;
- PRD-stage validation posture;
- downstream verification obligations.

## Minimal Acceptance Condition For Starting PRD

The DSL PRD skill is allowed to begin when the brainstorming stage provides at least:

- accepted canonical assertions;
- accepted deltas;
- increment-validation records for those deltas;
- ontology and ASM projections that are current enough to interpret the accepted baseline.

It should not require that every accepted delta already has full backend evidence.

## Stronger Acceptance Condition For High-Risk PRDs

If the product area is safety-critical, contract-critical, or contradiction-prone, the PRD skill should recommend additional upstream checking before finalizing the PRD when:

- accepted deltas lack backend evidence for central constraints;
- increment validation is deferred on critical baseline changes;
- key negative assertions remain only property-generated and unchecked.

## Summary

The PRD in this branch is not just “requirements written after brainstorming.”

It is:

- a readable requirements artifact grounded in an accepted and increment-validated formal baseline;
- explicit about which commitments are strongly evidenced, weakly evidenced, deferred, assumed, or contested;
- conservative in how it propagates confidence from the brainstorming branch.
