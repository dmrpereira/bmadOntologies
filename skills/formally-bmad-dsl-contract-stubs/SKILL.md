---
name: formally-bmad-dsl-contract-stubs
description: Generates DSL reviewable code scaffolds enriched with formal contracts. Use when the user requests to 'generate DSL contract stubs', 'create scaffold code from DSL contracts', or 'prepare contract-bearing scaffolds before implementation'.
---

# formally-bmad-dsl-contract-stubs

## Overview

This workflow projects one story's accepted DSL contracts into reviewable source-tree scaffolding before implementation begins. Act as an implementation-shaping engineer for the `formally-bmad-dsl-*` branch: infer file, module, type, and signature layout from story and architecture artifacts, place the accepted contracts directly on those surfaces, and generate scaffold code under the project tree without filling in business logic.

This stage is mandatory after `formally-bmad-dsl-contracts`. Its purpose is to make the future implementation boundary explicit and reviewable before `bmad-dev` or a human starts writing bodies.

The default scaffold root is `{formally_bmad_dsl_scaffold_root}`, which should resolve to `{project-root}/scaffold` unless the user configured a different project-local staging area.

Never end the session silently. Before any pause, stop, or handoff, explicitly tell the user what scaffold files were planned or generated, what contract placements remain blocked, whether user approval is still required, and the exact next workflow.

## Conventions

- Bare paths (e.g. `scripts/contract_stubs_workspace.py`) resolve from the skill root.
- `{skill-root}` resolves to this skill's installed directory.
- `{project-root}`-prefixed paths resolve from the project working directory.
- `{skill-name}` resolves to the skill directory's basename.

## On Activation

Load available config from `{project-root}/_bmad/config.yaml` and `{project-root}/_bmad/config.user.yaml` (root level and `formally-bmad-dsl` section). Resolve these values, using setup defaults only when config is absent:

- `formally_bmad_dsl_project_root`: `{project-root}/_bmad/formally-bmad-dsl`
- `formally_bmad_dsl_canonical_model_path`: `{project-root}/_bmad/formally-bmad-dsl/canonical`
- `formally_bmad_dsl_report_format`: `markdown,html`
- `formally_bmad_dsl_scaffold_root`: `{project-root}/scaffold`

If `{formally_bmad_dsl_project_root}` or `{formally_bmad_dsl_canonical_model_path}/status.md` is missing, stop and direct the user to run `formally-bmad-dsl-setup`.

If `--headless` or `-H` is invoked, require a DSL contract workspace or accepted contract inventory plus a target language. Without those, create only the workspace and report that scaffold generation needs explicit contracts and a language target.

## Workflow

### Establish Stub Scope

Load or ask for:

- contract workspace or accepted contract inventory from `formally-bmad-dsl-contracts`;
- target language: `python`, `c`, or `rust`;
- story artifact and relevant architecture companions;
- project naming or layering constraints if the user supplied any.

This stage is per-story only. Keep the scaffold tied to one story identifier and one chosen language profile.

### Initialize Workspace

Run the deterministic workspace helper once the language and scope are known:

```bash
python3 scripts/contract_stubs_workspace.py --project-root {project-root} --module-root "{formally_bmad_dsl_project_root}" --target "{story-id-and-language}"
```

The helper creates `{formally_bmad_dsl_project_root}/artifacts/dsl-contract-stubs/<safe-target>/` with starter files for the stub plan, contract surface summary, scaffold plan, review checklist, provenance, and local validation.

### Infer Code Shape Conservatively

Infer the file, module, type, and signature layout from story plus architecture artifacts.

If the layout is underdetermined:

- propose the minimal code shape that best satisfies the accepted architecture and story obligations;
- write that proposal into the stub workspace;
- stop and require explicit user approval before writing scaffold files.

Do not silently guess a layout that materially affects interface or verification structure.

### Generate Source-Tree Scaffolding

When the layout is sufficiently grounded and approved, write scaffold files under:

`{formally_bmad_dsl_scaffold_root}/{story-id}/`

Generate only:

- file/module boundaries;
- public and internal signatures;
- types, structs, records, traits, interfaces, or headers as appropriate;
- accepted contract annotations, decorators, specification blocks, or canonical specification comments in the chosen notation family;
- placeholder bodies only.

Do not implement business logic.

### Keep Contract Placement Explicit

For each generated scaffold element, record:

- which contract IDs it implements;
- where each precondition, postcondition, invariant, frame/effect rule, or error contract is attached;
- which later body-level proof obligations remain for implementation;
- whether the placement is exact, approximate, or still blocked.

If a contract cannot yet be placed cleanly, surface that as a review blocker rather than burying it.

### Tailor Scaffold Style By Language

Use language-appropriate skeletons:

- Python: typed functions/classes with `pyveritas`-oriented or `deal`-oriented contract placement and placeholder bodies such as `raise NotImplementedError`;
- C: header/source or API skeletons with ACSL blocks and explicit placeholder bodies;
- Rust: Kani-oriented module, trait, impl, or function skeletons using placeholder bodies such as `todo!()` only when clearly marked as unimplemented.

Keep the generated style compatible with the selected canonical verification target from the contract stage.

### Require User Review

This workflow is a hard review gate.

The output must make it easy for the user to validate:

- names and boundaries;
- inferred layout choices;
- signatures and data shapes;
- contract placement;
- whether the scaffold is acceptable as the implementation starting point.

Do not recommend implementation until the user explicitly approves the scaffold.

### Produce Companions

Maintain the companion folder with:

- `stubs.md` — scaffold summary and formal status block;
- `contract-surface.md` — mapping from contracts to signatures/types/modules;
- `file-plan.md` — expected file/module layout and ownership;
- `scaffold-plan.md` — source-tree scaffold targets under `{formally_bmad_dsl_scaffold_root}/{story-id}/`;
- `review-checklist.md` — what the user must validate before implementation begins;
- `provenance.md` — contract-to-scaffold mapping;
- `local-validation.md` — missing placements, blocked decisions, approval state, naming conflicts, and repair proposals.

### Handoff

End with:

- stub workspace path;
- generated or proposed scaffold root;
- target language and code surface summary;
- generated scaffold scope and review issues;
- contracts that could not yet be placed cleanly;
- explicit approval status;
- mandatory next workflow after approval: `formally-bmad-implementation-contracts`.

If approval is still pending, say plainly that implementation is blocked until the scaffold is approved.
