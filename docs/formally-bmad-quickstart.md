# Formally BMAD Quickstart

## What This Repository Is

This repository contains the Formally BMAD module source. It is not a standalone installer.

The module is packaged as a set of skill folders under `skills/`. To use it in a target project, copy those skill folders into the active BMad skill location for that target project and then run the setup skill from inside the target project.

## What This Module Adds

Formally BMAD extends BMad artifacts with a project-level canonical model and automated consistency/verification hooks.

Default on-disk state lives under:

- DSL branch state root: `{project-root}/_bmad/formally-bmad-dsl/`
- DSL canonical model: `{project-root}/_bmad/formally-bmad-dsl/canonical/`

## Prerequisite

The target project must already have BMad installed.

To create a fresh local BMad project in a target folder, run one of these commands from inside that folder:

```bash
npx bmad-method install
```

or:

```bash
npx bmad-method@next install
```

Formally BMAD expects:

- an existing `_bmad/` directory in the target project
- BMad configuration files or normal BMad project state
- an active skill installation location, commonly `.claude/skills/`

Formally BMAD does not bootstrap core BMad into an empty folder.

## Install The Module

Install the Formally BMAD skill folders into the target project's active BMad skill location.

For the DSL parallel branch, the supported agent-specific installed locations are:

```text
{project-root}/.claude/skills/
{project-root}/.codex/skills/
{project-root}/.pi/skills/
```

You can install the DSL branch payload automatically with:

```bash
./scripts/install_formally_bmad_dsl_branch.sh --target-project <target-project>
```

The required runtime skills are:

- `formally-bmad-dsl-setup`
- `formally-bmad-dsl-agent-steward`
- `formally-bmad-formal-brainstorming`
- `formally-bmad-dsl-brainstorming`
- `formally-bmad-formal-import`
- `formally-bmad-ontology-alignment`
- `formally-bmad-formal-prd`
- `formally-bmad-dsl-prd`
- `formally-bmad-formal-architecture`
- `formally-bmad-dsl-architecture`
- `formally-bmad-formal-epics`
- `formally-bmad-dsl-epics`
- `formally-bmad-formal-stories`
- `formally-bmad-dsl-stories`
- `formally-bmad-dsl-contracts`
- `formally-bmad-dsl-contract-stubs`
- `formally-bmad-implementation-contracts`
- `formally-bmad-code-verification`
- `formally-bmad-formal-verification`
- `formally-bmad-dsl-verification`

Copy those exact directories from this repository's `skills/` folder into the active skills directory for the agent you plan to use, for example:

```text
<target-project>/.claude/skills/
```

Each skill directory must become a direct child of the chosen `skills/` directory.

Correct examples:

```text
<target-project>/.claude/skills/formally-bmad-dsl-setup
<target-project>/.claude/skills/formally-bmad-dsl-agent-steward
<target-project>/.claude/skills/formally-bmad-dsl-prd
<target-project>/.claude/skills/formally-bmad-dsl-architecture
<target-project>/.claude/skills/formally-bmad-dsl-verification
```

Wrong example:

```text
<target-project>/.claude/skills/skills/formally-bmad-dsl-setup
```

You may obtain those skills by cloning this repository, copying them from a local checkout, or downloading and uncompressing a ZIP. The ZIP is only a transport format; the actual install step is copying the skill directories into the target project's active skills location.

## Setup

Run the setup capability:

- Skill: `formally-bmad-dsl-setup`

DSL setup does two things:

1. Registers the isolated DSL branch help/config surface in `{project-root}/_bmad/config.yaml` and `{project-root}/_bmad/module-help.csv`
2. Initializes the module state and validates at least one supported automated reasoning tool is available

## Tool Requirement (Hard Gate)

Setup is blocked unless the baseline validation gate is satisfied:

- at least one supported SMT solver
- at least one supported first-order or SAT solver

Supported families (examples):

- SMT: `z3`, `cvc5`, `cvc4`
- First-order: `vampire`, `eprover`, `prover9`, `mace4`
- SAT: `kissat`, `cadical`, `minisat`, `glucose`
- Temporal: `tlc`, `apalache`, `alloy`
- Ontology/DL: `robot`, `hermit`, `elk`, `pellet`
- Python contract verification: `pyveritas`, `deal`, `crosshair`, `nagini`, `esbmc`
- C contract verification: `frama-c`, `cbmc`, `esbmc`, `verifast`
- Rust contract verification: `cargo-kani`, `prusti-rustc`, `cargo-prusti`, `cargo-creusot`, `verus`, `flux`, `verifast`, `esbmc`

Additional tooling such as `black` and proof assistants may be detected and reported, but they do not replace the baseline gate.

If the baseline gate is not satisfied, setup must not proceed.

## Verify Setup Output

After setup completes, expect:

- `{project-root}/_bmad/formally-bmad-dsl/reports/setup-report.md`
- `{project-root}/_bmad/formally-bmad-dsl/canonical/status.md`
- Canonical folders under `{project-root}/_bmad/formally-bmad-dsl/canonical/`:
  - `model/`, `ontology/`, `temporal/`, `meta/`, `versions/`

## Notes

- Proof assistants are not primary targets; automated provers/solvers are preferred.
- `black` and `robot` may be installed outside the normal `PATH`; the current setup helper also checks known session-local install paths.
- Human-readable specs remain BMad-style Markdown, with logic-native companions produced alongside them.
- Two workflow branches may coexist:
  - the original `formally-bmad-formal-*` branch;
  - the parallel experimental `formally-bmad-dsl-*` branch built around a canonical DSL, ontology/ASM projections, and delta validation.
- The DSL implementation path is now: `formally-bmad-dsl-stories` -> `formally-bmad-dsl-contracts` -> `formally-bmad-dsl-contract-stubs` -> explicit scaffold approval -> `formally-bmad-implementation-contracts` -> `formally-bmad-code-verification` -> `formally-bmad-dsl-verification`.
- DSL contract scaffolds default to `{project-root}/scaffold/{story-id}/`.
- For Rust in the DSL path, `Kani` is the default canonical verification target unless the project config overrides it.
- If the selected target language lacks a compatible verification backend, those implementation-facing workflows should offer installation before falling back to degraded behavior.
