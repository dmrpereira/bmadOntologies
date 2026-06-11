---
name: formally-bmad-formal-contracts
description: Derives code contracts from formal obligations. Use when the user requests to 'create formal contracts', 'derive code contracts', or 'map formal requirements into contracts'.
---

# formally-bmad-formal-contracts

## Overview

This workflow derives language-aware code contracts from accepted PRD requirements, architecture constraints, epic/story obligations, and the evolving Formally BMAD canonical model. Act as a contract refinement engineer: translate implementation-facing obligations into explicit contract surfaces, contract notations, exportable tool views, and honest evidence expectations without pretending that comments or pseudocode are already checkable contracts.

## Conventions

- Bare paths (e.g. `scripts/contracts_workspace.py`) resolve from the skill root.
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

If `--headless` or `-H` is invoked, require accepted requirements or story criteria plus a target language and a target code surface. Without those, create only the workspace and report that contract derivation needs implementation-facing obligations and a language target.

## Workflow

### Establish Contract Scope

Load or ask for:

- accepted PRD requirements and their verification obligations;
- architecture constraints and interface commitments;
- epic/story obligations and acceptance criteria;
- target language: `python`, `c`, or `rust`;
- target code surfaces: module, file, type, function, method, API boundary, or protocol;
- existing implementation artifact if refining brownfield code.

Do not proceed if the target language or contract surface is unclear enough that a contract notation choice would be speculative.

### Initialize Workspace

Run the deterministic workspace helper once the target language and scope are known:

```bash
python3 scripts/contracts_workspace.py --project-root {project-root} --module-root "{formally_bmad_project_root}" --target "{target-language-and-scope}"
```

The helper creates `{formally_bmad_project_root}/artifacts/contracts/<safe-target>/` with starter files for the contract inventory, language profile, contract formalization, implementation mapping, exported views, provenance, and local validation.

### Choose Contract Surfaces

Map implementation-facing obligations into explicit contract locations:

- function or method preconditions;
- postconditions and result properties;
- data invariants and representation invariants;
- frame or side-effect constraints;
- error and exceptional-behavior contracts;
- protocol, sequencing, or temporal usage rules;
- ownership, aliasing, mutability, or resource constraints when relevant.

If a requirement is too large or mixed to produce a faithful contract, split it before assigning notation.

### Choose Language-Aware Contract Notation

For each contract, choose a notation and record why it fits:

- Python: prefer `deal`-style or `icontract`-style contracts for preconditions, postconditions, invariants, and side effects; use CrossHair-friendly expression subsets when symbolic checking is intended; plain `assert` is runtime-only and must be marked degraded.
- C: prefer ACSL for function/module contracts and Frama-C-oriented proof obligations; use executable assertions or CBMC harness assertions only as bounded or runtime-oriented fallbacks, not as equivalent replacements for ACSL.
- Rust: prefer Kani-friendly assertions, proof harnesses, and function-contract style obligations when model checking is intended; use Prusti or Creusot style specification surfaces when the target code and ownership model fit those tools; plain `assert!` or `debug_assert!` is runtime-only unless a verifier actually consumes it.

Do not emit a contract notation merely because it looks familiar. Emit only notations that are plausible for the selected language and verification path.

### Classify Faithfulness and Evidence

For every derived contract, record:

- `contract_kind`: precondition, postcondition, invariant, frame, effect, temporal-usage, ownership, or error-behavior;
- `notation_family`: python-decorator, acsl, rust-contract, runtime-assertion, harness, or mixed;
- `faithfulness`: `exact`, `conservative-approximation`, `partial-translation`, or `not-faithfully-expressible`;
- `verification_mode`: `symbolic`, `bounded-model-checking`, `deductive`, `runtime`, `test`, `manual-review`, or `mixed`;
- `claim_strength`: `contract-written`, `tool-view-exported`, or `tool-backed-validated`.

If the contract is only a runtime guard, comment, or docstring, say so plainly. Do not imply solver-backed enforceability.

### Generate Tool-Facing Views

For each contract that is more than documentation-only, define the tool-facing export path:

- Python: CrossHair-oriented checks, `deal` lint/test/formal-verification surface, or runtime-only decorator/assertion use;
- C: ACSL plus Frama-C WP/E-ACSL path, or CBMC harness/assertion path;
- Rust: Kani proof harness or contract path, Prusti path, Creusot path, or runtime-only assertion path.

Where export is not yet faithful, record the missing model detail rather than fabricating a stronger contract view.

### Submit to Steward

Submit accepted contract mappings and implementation-facing obligations to `formally-bmad-agent-steward` through `Accept Canonical Delta` and `Validate Update Consistency` when they refine accepted upstream commitments.

The steward should treat contract artifacts as downstream refinements of accepted requirements, not as independent replacements for them.

### Produce Companions

Maintain the companion folder with:

- `contracts.md` — contract summary and formal status block;
- `contract-inventory.md` — contract IDs, target surfaces, kinds, notation family, faithfulness, verification mode, and claim strength;
- `language-profile.md` — selected language, supported notation choices, selected tool paths, and known limits;
- `formalization.md` — rigorous English plus code-contract notation sketches or exact snippets when available;
- `implementation-mapping.md` — requirement/story-to-code-surface mapping;
- `exported-views.md` — tool-facing export plan and artifact paths;
- `provenance.md` — source requirement/story to contract mapping;
- `local-validation.md` — ambiguity, downgrade reasons, missing model detail, steward responses, and repair proposals.

### Handoff

End with:

- contract workspace path;
- target language and target code surfaces;
- contract coverage summary by kind and notation family;
- contracts that remain runtime-only, test-backed, or review-backed, with reasons;
- steward validation status;
- recommended next workflow: `formally-bmad-contract-stubs`.
