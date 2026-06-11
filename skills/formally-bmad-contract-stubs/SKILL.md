---
name: formally-bmad-contract-stubs
description: Generates contract-bearing code skeletons. Use when the user requests to 'generate contract stubs', 'create code skeletons with contracts', or 'preview contract-bearing signatures'.
---

# formally-bmad-contract-stubs

## Overview

This workflow generates reviewable code skeletons from accepted code contracts before full implementation begins. Act as an implementation-shaping engineer: project requirements and accepted contracts into signatures, types, modules, interfaces, and contract annotations for the target language without filling in business logic or pretending the stubs are already implemented.

## Conventions

- Bare paths (e.g. `scripts/contract_stubs_workspace.py`) resolve from the skill root.
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

If `--headless` or `-H` is invoked, require a contract workspace or accepted contract inventory plus a target language and target code surface. Without those, create only the workspace and report that stub generation needs explicit contracts and a language target.

## Workflow

### Establish Stub Scope

Load or ask for:

- contract workspace or accepted contract inventory;
- target language: `python`, `c`, or `rust`;
- intended package/module/file layout;
- target code surfaces: functions, methods, types, interfaces, traits, headers, or modules;
- any user-imposed naming or layering constraints.

Do not begin if the contracts are still unstable enough that signatures or module boundaries would be guesswork.

### Initialize Workspace

Run the deterministic workspace helper once the language and scope are known:

```bash
python3 scripts/contract_stubs_workspace.py --project-root {project-root} --module-root "{formally_bmad_project_root}" --target "{target-language-and-scope}"
```

The helper creates `{formally_bmad_project_root}/artifacts/stubs/<safe-target>/` with starter files for the stub plan, contract surface summary, review checklist, provenance, and local validation.

### Check Contract Tool Readiness

Stub generation may continue without an installed verifier, but it must not hide the gap.

Check whether the selected language has at least one compatible backend:

- Python: `crosshair`, `deal`, `nagini`, or `esbmc`
- C: `frama-c`, `cbmc`, `esbmc`, or `verifast`
- Rust: `cargo-kani`, `prusti-rustc`, `cargo-prusti`, `cargo-creusot`, `verus`, `flux`, `verifast`, or `esbmc`

If no compatible backend is available:

- warn the user that the stubs can still be reviewed for code shape, but the chosen contract notation is not yet backed by an available verifier;
- if a plausible installer path is known in the current environment, ask whether the user wants to install the backend now;
- continue with stub generation even if the user declines, but record the missing backend in `local-validation.md` and `review-checklist.md`.

### Project Contracts Into Code Shape

Generate only the code shape implied by accepted contracts:

- file/module boundaries;
- public and internal signatures;
- types, structs, records, traits, interfaces, or headers as appropriate;
- contract annotations, decorators, comments, or specification blocks in the selected contract notation;
- placeholders for bodies, not full logic.

Do not fill in business logic beyond the minimum placeholder structure required by the target language.

### Keep Contract Placement Explicit

For each generated stub, record:

- which contract IDs it implements;
- where each precondition, postcondition, invariant, or effect rule is attached;
- whether the contract is rendered directly in code, adjacent specification syntax, or companion comments only;
- whether the current stub shape is exact, approximate, or still blocked by missing type/interface decisions.

If a contract cannot yet be placed cleanly, surface that as a review issue rather than burying it in the stub.

### Tailor Stub Style By Language

Use language-appropriate skeletons:

- Python: function/class skeletons with `deal`, `icontract`, or other accepted contract markers, typed signatures, and placeholder bodies such as `raise NotImplementedError`;
- C: header/source or API skeletons with ACSL blocks, CBMC/ESBMC harness hooks where appropriate, or VeriFast-friendly specification placement, with empty or explicit placeholder bodies;
- Rust: module, trait, impl, or function skeletons with Kani, Prusti, Creusot, Verus, Flux, or VeriFast oriented annotations or placeholders, using `todo!()` or equivalent only when clearly marked as unimplemented.

If the chosen contract notation has tool-specific syntax limits, keep the skeleton compatible with that path and note any compromises.

### Require Review Before Full Implementation

Treat this workflow as a review gate, not code completion.

The output must make it easy for the user to validate:

- names and boundaries;
- signatures and data shapes;
- contract placement;
- whether the code shape faithfully reflects the accepted obligations.

Do not recommend full implementation until the stub review issues are either accepted or repaired.
If the verifier backend is still missing, include that as a review item rather than burying it.

### Produce Companions

Maintain the companion folder with:

- `stubs.md` — stub-generation summary and formal status block;
- `contract-surface.md` — mapping from contracts to signatures/types/modules;
- `file-plan.md` — expected file/module layout and ownership;
- `review-checklist.md` — what the user should validate before implementation begins;
- `provenance.md` — contract-to-stub mapping;
- `local-validation.md` — missing placements, blocked decisions, naming conflicts, and repair proposals.

### Handoff

End with:

- stub workspace path;
- target language and code surface summary;
- generated stub scope and review issues;
- contracts that could not yet be placed cleanly;
- recommended next workflow: user review/approval, then `formally-bmad-code-verification` once real implementation exists.
