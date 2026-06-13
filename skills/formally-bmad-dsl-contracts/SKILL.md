---
name: formally-bmad-dsl-contracts
description: Derives DSL-branch Hoare-style contracts per story before implementation begins. Use when the user requests to 'derive DSL contracts', 'formalize story contracts from the DSL branch', or 'prepare implementation contracts after DSL stories'.
---

# formally-bmad-dsl-contracts

## Overview

This workflow derives implementation-facing Hoare-style contracts from a single accepted DSL story before any business-logic implementation begins. Act as a contract refinement engineer for the `formally-bmad-dsl-*` branch: consume the accepted DSL baseline, PRD formalization, architecture formalization, epic/story obligations, and inherited evidence posture, then project that material into explicit preconditions, postconditions, invariants, frame/effect constraints, error behavior, and proof-ready assumptions for one target language.

This stage is mandatory after `formally-bmad-dsl-stories`. It exists to stop implementation from starting against under-specified story prose.

Never continue in the presence of missing formal grounding. If canonical DSL baseline, PRD formalization, architecture formalization, or story lineage is incomplete enough that the contract would be speculative, stop and report the exact missing artifacts or unresolved mappings.

Never end the session silently. Before any pause, stop, or handoff, explicitly tell the user what contract derivation work completed, what target language/tooling was fixed, what remains blocked, and the exact next workflow.

## Conventions

- Bare paths (e.g. `scripts/contracts_workspace.py`) resolve from the skill root.
- `{skill-root}` resolves to this skill's installed directory.
- `{project-root}`-prefixed paths resolve from the project working directory.
- `{skill-name}` resolves to the skill directory's basename.

## On Activation

Load available config from `{project-root}/_bmad/config.yaml` and `{project-root}/_bmad/config.user.yaml` (root level and `formally-bmad-dsl` section). Resolve these values, using setup defaults only when config is absent:

- `formally_bmad_dsl_project_root`: `{project-root}/_bmad/formally-bmad-dsl`
- `formally_bmad_dsl_canonical_model_path`: `{project-root}/_bmad/formally-bmad-dsl/canonical`
- `formally_bmad_dsl_validation_strictness`: `stage-aware`
- `formally_bmad_dsl_report_format`: `markdown,html`
- `formally_bmad_dsl_scaffold_root`: `{project-root}/scaffold`
- `formally_bmad_dsl_rust_contract_backend`: `kani`

If `{formally_bmad_dsl_project_root}` or `{formally_bmad_dsl_canonical_model_path}/status.md` is missing, stop and direct the user to run `formally-bmad-dsl-setup`.

If `--headless` or `-H` is invoked, require a story artifact or story companion folder plus a target language. Without those, create only the workspace and report that DSL contract derivation needs a formalized story and a language target.

## Workflow

### Establish Contract Scope

Load or ask for:

- one accepted DSL story artifact and its companion folder;
- target language: `python`, `c`, or `rust`;
- target code surfaces implied by the story and architecture;
- canonical requirement and delta lineage for the story;
- architecture refinements and constraints that drive type, module, or API boundaries;
- current backend/tool availability relevant to the selected language.

This stage is per-story only. Do not widen the derivation into an epic-wide batch unless the user deliberately restarts scope with a different skill invocation.

### Validate Formal Grounding

Before writing any contract, verify that the story can be traced to all of the following:

- accepted canonical DSL baseline material;
- accepted PRD requirements and formalization;
- accepted architecture formalization and recheck obligations;
- accepted epic and story obligations with evidence posture;
- current steward-promoted delta lineage.

If any of those are missing, stale, contradictory, or only implied by prose summaries, stop and report the missing formal grounding. Do not infer contracts across a gap you cannot trace.

### Fix The Verification Target

Choose exactly one canonical contract/tool profile for the selected language and record why:

- Python: prefer `pyveritas`; use `deal` only when `pyveritas` is unavailable or the story's contract surface is a poor fit for the current `pyveritas` path.
- C: use `ACSL`.
- Rust: use the backend configured by `formally_bmad_dsl_rust_contract_backend`, defaulting to `kani`.

Do not emit multiple parallel notation families for the same story. The downstream stub stage and later implementation stage need one canonical contract surface.

### Initialize Workspace

Run the deterministic workspace helper once the language and story scope are known:

```bash
python3 scripts/contracts_workspace.py --project-root {project-root} --module-root "{formally_bmad_dsl_project_root}" --target "{story-id-and-language}"
```

The helper creates `{formally_bmad_dsl_project_root}/artifacts/dsl-contracts/<safe-target>/` with starter files for the contract inventory, language profile, grounding audit, formalization, implementation mapping, exported views, provenance, and local validation.

### Derive Hoare-Style Contracts Conservatively

Translate accepted implementation-facing obligations into explicit contract units such as:

- preconditions;
- postconditions and result properties;
- data invariants and representation invariants that can be stated before implementation;
- frame or side-effect constraints;
- error and exceptional-behavior contracts;
- protocol or sequencing constraints;
- ownership, aliasing, mutability, or resource obligations when the target language requires them.

Because this stage is pre-code, do not fabricate body-level proof artifacts such as loop invariants or variants as if the loop structure already exists. Instead, record those as implementation-stage proof obligations where relevant.

### Record Faithfulness And Deferred Body Obligations

For every derived contract, record:

- `contract_kind`;
- `notation_family`;
- `faithfulness`;
- `verification_mode`;
- `claim_strength`;
- source requirement IDs;
- source delta IDs;
- source architecture obligations;
- whether the contract is directly ready for stub placement;
- whether later implementation must add body-level proof material such as loop invariants, loop variants, helper lemmas/specs, or local assertions/assumptions.

If a requirement cannot be expressed faithfully in the selected notation, say so plainly and keep the story blocked until the mismatch is resolved or accepted explicitly as a downgrade.

### Produce Tool-Facing Export Guidance

For the chosen language profile, define the exact downstream export and checking path:

- Python: `pyveritas` if available and suitable; otherwise `deal`.
- C: ACSL/Frama-C oriented output.
- Rust: Kani-oriented output unless configuration explicitly selects another backend.

Where the selected toolchain is missing, report the block and stop. This stage must fix the verification target before implementation planning continues.

### Produce Companions

Maintain the companion folder with:

- `contracts.md` — contract summary and formal status block;
- `contract-inventory.md` — contract IDs, target surfaces, kinds, notation family, faithfulness, verification mode, claim strength, and deferred body obligations;
- `language-profile.md` — selected language, chosen canonical tool profile, and rejected alternatives;
- `grounding-audit.md` — proof that the story's contracts are grounded in canonical baseline, PRD, architecture, epic, and story lineage;
- `formalization.md` — rigorous English plus exact or near-exact contract notation;
- `implementation-mapping.md` — requirement/story-to-code-surface mapping;
- `exported-views.md` — downstream tool-facing export path and artifact plan;
- `provenance.md` — source requirement/story to contract mapping;
- `local-validation.md` — ambiguity, blocked derivations, downgrade reasons, and repair proposals.

### Handoff

End with:

- contract workspace path;
- story ID and target language;
- chosen canonical verification target;
- contract coverage summary by kind;
- blocked or downgraded contracts with reasons;
- deferred implementation-stage proof obligations;
- mandatory next workflow: `formally-bmad-dsl-contract-stubs`.

Do not allow implementation to begin directly from this stage. The generated contracts must first be projected into reviewable scaffolding.
