# DSL Contracts Consumption Contract

## Purpose

This note defines how the new `formally-bmad-dsl-contracts` and `formally-bmad-dsl-contract-stubs` skills should consume the upstream DSL branch after `formally-bmad-dsl-stories`.

This contract belongs to the parallel `formally-bmad-dsl-*` workflow family and must not be assumed to apply to the original `formally-bmad-formal-*` branch.

## Design Goal

The DSL branch should not jump from implementation stories directly into body implementation.

Instead, after stories are accepted:

1. derive explicit Hoare-style implementation contracts from accepted upstream formal artifacts;
2. project those contracts into reviewable source-tree scaffolds;
3. require user approval of the scaffold before implementation begins;
4. only then allow implementation to add code bodies plus body-level proof artifacts.

## Required Upstream Inputs

`formally-bmad-dsl-contracts` must consume:

- canonical DSL baseline and current steward-promoted status;
- PRD formalization and accepted requirements;
- architecture formalization and recheck obligations;
- epic obligations;
- story artifact and story companions from `formally-bmad-dsl-stories`.

The contract stage must block when any of those inputs are missing, stale, contradictory, or only implied by unsynchronized summaries.

## Authority Order

1. accepted canonical DSL baseline and promoted deltas
2. accepted PRD requirements and formalization
3. accepted architecture formalization and recheck obligations
4. accepted epic and story obligations
5. prose-only supporting narrative

If prose and the accepted formal baseline disagree, the accepted formal baseline wins unless a new repair or delta workflow explicitly changes it.

## Contract Derivation Rules

Per story, the contract stage must:

- select exactly one target language;
- select exactly one canonical verification-oriented contract profile for that story;
- derive preconditions, postconditions, invariants, frame/effect constraints, error contracts, and other implementation-facing obligations that are already justified by the upstream formal artifacts;
- record body-level proof obligations that must be added during implementation, such as loop invariants, loop variants, helper lemmas/specs, and local assertions/assumptions.

It must not:

- generate multiple parallel notation families for the same story;
- continue past missing formal grounding;
- pretend that body-level proof obligations are already discharged before implementation exists.

## Stub Generation Rules

`formally-bmad-dsl-contract-stubs` must:

- infer file/module/type/signature layout from story plus architecture artifacts;
- write scaffolds under `{project-root}/scaffold/{story-id}/` by default;
- attach the accepted contracts to the generated code surfaces;
- require explicit user approval before implementation begins.

If the layout is materially underdetermined, the stub stage must propose a layout and stop for approval rather than silently guessing.

## Downstream Handoff

After scaffold approval, the implementation stage must preserve the approved contract surface and add body-level proof artifacts. The intended downstream flow is:

`formally-bmad-dsl-stories` -> `formally-bmad-dsl-contracts` -> `formally-bmad-dsl-contract-stubs` -> scaffold approval -> `formally-bmad-implementation-contracts` -> `formally-bmad-code-verification` -> `formally-bmad-dsl-verification`
