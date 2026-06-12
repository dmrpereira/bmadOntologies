# Delta-Based Validation Workflow

## Purpose

This note revises the workflow model for `formally-bmad-canonical-brainstorming`.

The earlier design emphasized property generation and property checking for individual assertions. That is necessary, but it is not sufficient for the real goal of the workflow.

The stronger goal is:

- when a new brainstormed idea is stabilized,
- treat it as a proposed increment to the current formal baseline,
- and verify whether that increment is acceptable with respect to the evolving ontology and ASM model.

So the workflow must be **delta-based**, not only **assertion-based**.

## Core Reframing

The formal object being managed is not a disconnected set of individual assertions.

It is an evolving baseline made of:

- the canonical DSL baseline;
- the ontology projection baseline;
- the ASM projection baseline;
- the generated property baseline;
- the mechanized evidence baseline.

A newly stabilized idea is therefore not just:

- “one more assertion”

It is:

- “a proposed delta to the current formal baseline”

## Verification Objective

The workflow must answer this question for every significant new stable idea:

> If this delta is applied to the current baseline, does the resulting formal state remain acceptable?

This is stronger than asking:

> Does this one generated property pass?

Both are needed, but the second is subordinate to the first.

## Delta Lifecycle

Each significant stable brainstormed idea should move through this lifecycle:

1. **Idea captured**
2. **Canonical assertion(s) normalized**
3. **Delta extracted**
4. **Impact set identified**
5. **Ontology increment checked**
6. **ASM increment checked**
7. **Affected properties regenerated or marked for recheck**
8. **Backend verification run on impacted obligations**
9. **Delta accepted, rejected, or deferred**
10. **Baseline updated only if accepted**

This means the workflow becomes baseline-aware and change-aware.

## What A Delta Is

A delta is the formal change induced by one or more new canonical assertions.

Each delta should identify:

- the source brainstorm outcome(s);
- the source canonical assertion ID(s);
- the structural changes introduced;
- the behavioral changes introduced;
- the ontology elements added, modified, or superseded;
- the ASM elements added, modified, or superseded;
- the generated properties added, modified, invalidated, or requiring recheck.

## Delta Validity Dimensions

Delta validation should happen on four dimensions.

### 1. Ontology Increment Validity

Questions:

- does the delta introduce semantic contradiction?
- does it violate existing cardinality commitments?
- does it create unsatisfiable concept structure?
- does it misuse existing vocabulary?
- does it require superseding older ontology commitments?

Success condition:

- the ontology baseline remains semantically acceptable after the increment.

### 2. ASM Increment Validity

Questions:

- does the delta introduce rule conflicts?
- does it break existing invariants?
- does it enable forbidden states?
- does it make required states unreachable?
- does it silently change the meaning of existing behavioral elements?

Success condition:

- the ASM baseline remains behaviorally acceptable after the increment.

### 3. Property Impact Validity

Questions:

- which existing properties are affected by the delta?
- which properties must be regenerated?
- which properties become obsolete?
- which properties must be rechecked?

Success condition:

- the property baseline accurately reflects the changed model.

### 4. Traceability Validity

Questions:

- is the delta explicit rather than implicit?
- are all impacted artifacts identified?
- are supersessions and conflicts recorded?
- can later reviewers reconstruct what changed and why?

Success condition:

- the increment is auditable.

## Revised Workflow Chain

The earlier chain:

1. brainstorm outcome
2. canonical assertion
3. ontology element(s)
4. ASM element(s)
5. generated property
6. backend check result

is too weak on its own.

The revised chain should be:

1. brainstorm outcome
2. canonical assertion(s)
3. proposed delta
4. affected ontology element(s)
5. affected ASM element(s)
6. impacted property set
7. increment validation checks
8. backend check results
9. delta disposition

## Required Artifact Additions

The current artifact set should be extended with explicit delta tracking.

### New artifact: `proposed-deltas.md`

Purpose:

- ledger of proposed increments before they are accepted into the formal baseline.

Recommended fields:

- `Delta ID`
- `Source Brainstorm Outcome`
- `Source Assertion IDs`
- `Change Kind`
- `Summary`
- `LifecycleStatus`
- `ValidationStatus`
- `Disposition`

Where `Change Kind` may be:

- `add`
- `modify`
- `supersede`
- `remove`

And `Disposition` may be:

- `proposed`
- `accepted`
- `rejected`
- `deferred`

### New artifact: `increment-validation.md`

Purpose:

- record the validation of each proposed delta against the current baseline.

Recommended fields:

- `Delta ID`
- `Affected Ontology Elements`
- `Affected ASM Elements`
- `Affected Property IDs`
- `Ontology Increment Result`
- `ASM Increment Result`
- `Property Impact Result`
- `Backend Check Result`
- `Overall Increment Result`
- `Notes`

## Required Changes To Existing Artifacts

### canonical-surface.md

Should continue to hold the authoritative assertions, but accepted assertions should reference the delta they belong to when applicable.

### ontology-projection.md

Should distinguish:

- baseline elements;
- elements added or modified by a pending delta;
- elements superseded by accepted deltas.

### asm-model.md

Should distinguish:

- baseline rules/invariants/functions;
- pending delta changes;
- superseded elements.

### generated-properties.md

Should include:

- `Origin Delta ID`
- `Impact Type`

Where `Impact Type` may be:

- `new`
- `modified`
- `recheck_required`
- `obsolete`

### verification-traceability.md

Should be revised to include delta awareness.

Recommended columns:

| Brainstorm Outcome | Canonical Assertion ID(s) | Delta ID | Ontology Element(s) | ASM Element(s) | Property ID(s) | Increment Validation Result | Backend Check Result | Disposition |

This is stronger than the earlier assertion-only traceability row.

### backend-checks.md

Should distinguish:

- checks run because a property exists;
- checks rerun because a delta impacted an existing property.

## Revised Status Model

The earlier split status dimensions still help, but delta handling needs another status layer.

### For assertions

- `LifecycleStatus`
- `KnowledgeStatus`
- `VerificationStatus`

### For deltas

- `DeltaLifecycleStatus`
  - `proposed | under_review | accepted | rejected | deferred`

- `DeltaValidationStatus`
  - `not_checked | ontology_checked | asm_checked | impact_checked | backend_checked | complete`

Assertions and deltas should not share the exact same lifecycle fields, because they represent different things.

## Role Of Backend Verification In The Revised Workflow

Backend verification is not only about checking newly generated properties in isolation.

It must also support:

- rechecking previously existing properties affected by a delta;
- checking whether the merged updated model still satisfies required obligations;
- surfacing counterexamples caused by the interaction between old and new model elements.

So the proper role of backend verification is:

- verify the **incremented baseline**, not merely the newly introduced statement in isolation.

## Acceptance Rule

A stable new idea should not update the accepted formal baseline until:

1. its canonical assertion(s) are stable enough;
2. its delta is explicit;
3. ontology and ASM impacts are identified;
4. impacted properties are identified;
5. increment validation is at least partially completed;
6. any required backend checks for the intended confidence level have been run or explicitly deferred.

This does not mean every idea needs maximum verification immediately.

It means every accepted increment must have an explicit verification disposition.

## Staged Confidence Model

To keep the workflow usable during brainstorming, delta validation should support staged confidence:

### Level 1: structural mapping only

- canonical assertion normalized;
- ontology/ASM impacts identified;
- no backend evidence yet.

### Level 2: property-ready increment

- impacted properties generated or marked for recheck;
- baseline impact understood.

### Level 3: selectively checked increment

- backend checks run for high-risk or central impacts.

### Level 4: strongly checked increment

- all planned impacted checks run;
- increment accepted with stronger confidence.

This lets the workflow stay usable during ideation while still preserving formal discipline.

## Consequence For PRD Handoff

PRD should not consume only:

- accepted assertions

It should consume:

- accepted assertions;
- accepted deltas;
- their ontology and ASM impacts;
- their current increment validation status;
- their current backend evidence status.

That way PRD is grounded in the actual validated state of the evolving model, not only in decontextualized statements.

## Minimum Revision To The Current Design

Before implementation, the minimum design revision should be:

1. add explicit delta artifacts;
2. revise traceability to include delta IDs and increment validation results;
3. redefine backend checking as baseline-increment checking, not only per-property checking;
4. define acceptance/disposition rules for proposed deltas.

## Recommended Immediate Next Design Task

The next useful design task after this note is:

- define the schema for `proposed-deltas.md` and `increment-validation.md`
- and revise the mapping spec so each assertion pattern specifies:
  - what delta it creates,
  - what ontology impacts it may trigger,
  - what ASM impacts it may trigger,
  - what property recheck obligations it creates.
