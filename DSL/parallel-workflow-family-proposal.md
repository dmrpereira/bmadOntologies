# Parallel Workflow Family Proposal

## Purpose

This note proposes a new parallel workflow family for the DSL + ontology + ASM + delta-validation approach.

The goal is to:

- preserve the existing Formally BMAD extension unchanged;
- create a new experimental branch of skills and artifacts;
- allow side-by-side evaluation between the original formal extension and the new canonical-DSL workflow;
- avoid contaminating the current pet-project baseline with premature redesign.

## Design Principle

Do not retrofit the existing workflow family.

Instead:

- keep the original workflow as one branch;
- create a second, parallel workflow family for the new experiment;
- let both branches coexist until the new branch proves its value.

This is the right move both technically and experimentally.

Technically:

- it avoids breaking the existing pipeline;
- it avoids ambiguous artifact contracts;
- it avoids retrofitting old skills around assumptions they were not designed for.

Experimentally:

- it gives a clean comparison point;
- it lets you test the original extension as a control branch;
- it lets the new workflow evolve aggressively without invalidating earlier work.

## Existing Branch

The existing branch remains unchanged:

- `formally-bmad-formal-brainstorming`
- `formally-bmad-formal-prd`
- `formally-bmad-formal-architecture`
- `formally-bmad-formal-epics`
- `formally-bmad-formal-stories`
- `formally-bmad-formal-verification`
- related support skills

This branch should continue to use its current assumptions and artifact chain.

## New Branch Goal

The new branch should test a different formalization philosophy:

- canonical DSL as authoritative surface;
- ontology as semantic projection;
- ASM as behavioral projection;
- delta-based validation over an evolving formal baseline;
- backend verification interpreted as increment validation, not only isolated property checking.

## Proposed Workflow Family

I recommend naming the new branch explicitly so it is clearly separate from the original “formal” branch.

The cleanest naming pattern is:

- `formally-bmad-dsl-*`

Reason:

- it identifies the canonical DSL as the defining feature;
- it avoids collision with the existing `formally-bmad-formal-*` family;
- it remains short and readable.

## Proposed Skill Chain

### 1. `formally-bmad-dsl-brainstorming`

Role:

- canonical entrypoint for the new branch;
- produces the authoritative DSL;
- produces ontology and ASM projections;
- manages proposed deltas and increment validation state;
- records verification traceability and backend evidence status.

Primary artifacts:

- `canonical-surface.md`
- `ontology-projection.md`
- `asm-model.md`
- `generated-properties.md`
- `verification-traceability.md`
- `backend-checks.md`
- `proposed-deltas.md`
- `increment-validation.md`

### 2. `formally-bmad-dsl-prd`

Role:

- consumes accepted canonical assertions and accepted deltas from the DSL brainstorming branch;
- turns them into a readable PRD plus requirement inventory;
- preserves validation state and evidence state rather than flattening them away;
- identifies which requirements inherit strong support, weak support, or unresolved increment risk.

Primary input:

- accepted canonical assertions;
- accepted deltas;
- increment validation state;
- backend evidence state.

Primary output:

- PRD artifacts that remain anchored to the validated evolving baseline.

### 3. `formally-bmad-dsl-architecture`

Role:

- refines accepted PRD requirements into architectural structures while preserving ontology and ASM continuity;
- adds architectural deltas to the same style of formal baseline;
- identifies architecture-level impacts on ontology, ASM, and verification obligations.

Primary output:

- architecture artifacts plus architectural deltas and validation implications.

### 4. `formally-bmad-dsl-epics`

Role:

- derives epic-level increments from accepted PRD and architecture baselines;
- keeps requirements and implementation planning tied to validated formal increments.

### 5. `formally-bmad-dsl-stories`

Role:

- derives story-level increments and implementation-facing obligations;
- preserves traceability back to canonical assertions and accepted deltas.

### 6. `formally-bmad-dsl-verification`

Role:

- owns deeper backend-oriented checking for the new branch;
- performs systematic rechecks after accepted deltas;
- produces consolidated evidence and counterexample interpretation.

This skill should be the heavy verification engine for the new branch, not the only place where formal awareness first appears.

## Proposed Handoff Order

Recommended sequence:

1. `formally-bmad-dsl-brainstorming`
2. `formally-bmad-dsl-prd`
3. `formally-bmad-dsl-architecture`
4. `formally-bmad-dsl-epics`
5. `formally-bmad-dsl-stories`
6. `formally-bmad-dsl-verification`

This mirrors the broad BMad lifecycle while preserving the experimental formalism branch.

## Branch Separation Rules

To keep the comparison clean, I recommend these rules.

### Rule 1. Separate skill names

Do not reuse `formally-bmad-formal-*` names for the new branch.

### Rule 2. Separate artifact roots if possible

Prefer a distinct artifact subtree for the new branch, for example:

- `{formally_bmad_project_root}/artifacts/dsl-brainstorming/`
- `{formally_bmad_project_root}/artifacts/dsl-prd/`

or a separate branch root such as:

- `{formally_bmad_project_root}/dsl-artifacts/`

This avoids confusion with the existing branch artifacts.

### Rule 3. Separate module-help entries

The new branch should appear as a separate workflow family, not as silent replacements for existing steps.

### Rule 4. No silent contract sharing

Do not assume the old PRD, architecture, or verification skills can consume the new artifacts without explicit design work.

### Rule 5. Comparison should be deliberate

Any later convergence between the old and new branches should happen only after explicit review.

## Minimal New Branch To Build First

Do not try to build the entire branch immediately.

The minimum rational parallel branch is:

1. `formally-bmad-dsl-brainstorming`
2. `formally-bmad-dsl-prd`

Reason:

- this gives you a complete first downstream handoff;
- it is enough to test whether the new DSL/delta-validation model actually improves the requirements pipeline;
- it keeps the scope manageable.

Only after those two are coherent should you proceed to:

- `formally-bmad-dsl-architecture`
- and later downstream skills.

## Immediate Next Design Task

The most sensible next step is:

- define the consumption contract for `formally-bmad-dsl-prd`

That contract should answer:

- what exact artifacts it reads from DSL brainstorming;
- what it treats as eligible source material;
- how it handles accepted vs deferred vs rejected deltas;
- how it carries validation confidence and backend evidence into the PRD.

## Recommendation

Proceed with the new branch using this naming and sequencing strategy:

1. keep the original `formally-bmad-formal-*` branch unchanged;
2. treat the new branch as `formally-bmad-dsl-*`;
3. build `formally-bmad-dsl-brainstorming` and `formally-bmad-dsl-prd` first;
4. evaluate them against the original branch before expanding further.
