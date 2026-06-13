# Formally BMAD DSL Quickstart

## What This Repository Is

This repository contains the active Formally BMAD DSL module source. It is not a standalone installer.

The module is packaged as skill folders under `skills/`. Install those folders into an existing BMad project and then run the DSL setup skill from inside that target project.

## State Layout

Default DSL state lives under:

- `{project-root}/_bmad/formally-bmad-dsl/`
- `{project-root}/_bmad/formally-bmad-dsl/canonical/`

Default pre-implementation scaffold output lives under:

- `{project-root}/scaffold/{story-id}/`

## Prerequisite

The target project must already have BMad installed.

Typical bootstrap commands:

```bash
npx bmad-method install
```

or:

```bash
npx bmad-method@next install
```

## Install The Module

Install the Formally BMAD DSL skill folders into the target project's active skills directory, or use:

```bash
./scripts/install_formally_bmad_dsl_branch.sh --target-project <target-project>
```

Supported install locations:

```text
{project-root}/.claude/skills/
{project-root}/.codex/skills/
{project-root}/.pi/skills/
```

Required runtime skills:

- `formally-bmad-dsl-setup`
- `formally-bmad-dsl-agent-steward`
- `formally-bmad-dsl-brainstorming`
- `formally-bmad-dsl-prd`
- `formally-bmad-dsl-architecture`
- `formally-bmad-dsl-epics`
- `formally-bmad-dsl-stories`
- `formally-bmad-dsl-contracts`
- `formally-bmad-dsl-contract-stubs`
- `formally-bmad-implementation-contracts`
- `formally-bmad-code-verification`
- `formally-bmad-dsl-verification`

Correct example:

```text
<target-project>/.claude/skills/formally-bmad-dsl-setup
```

Wrong example:

```text
<target-project>/.claude/skills/skills/formally-bmad-dsl-setup
```

## Setup

Run:

- `formally-bmad-dsl-setup`

Setup:

1. registers DSL config/help into `_bmad/`
2. creates the DSL project state
3. validates the baseline automated reasoning gate

## Tool Requirement

Setup is blocked unless both are available:

- at least one supported SMT solver
- at least one supported first-order or SAT solver

Implementation-facing tool families include:

- Python: `pyveritas`, `deal`, `crosshair`, `nagini`, `esbmc`
- C: `frama-c`, `cbmc`, `esbmc`, `verifast`
- Rust: `cargo-kani`, `prusti-rustc`, `cargo-prusti`, `cargo-creusot`, `verus`, `flux`, `verifast`, `esbmc`

## Expected Setup Output

After setup completes, expect:

- `{project-root}/_bmad/formally-bmad-dsl/reports/setup-report.md`
- `{project-root}/_bmad/formally-bmad-dsl/canonical/status.md`
- canonical folders under `{project-root}/_bmad/formally-bmad-dsl/canonical/`:
  - `model/`
  - `ontology/`
  - `temporal/`
  - `meta/`
  - `versions/`

## Workflow

Use this order:

1. `formally-bmad-dsl-agent-steward`
2. `formally-bmad-dsl-brainstorming`
3. `formally-bmad-dsl-prd`
4. `formally-bmad-dsl-architecture`
5. `formally-bmad-dsl-epics`
6. `formally-bmad-dsl-stories`
7. `formally-bmad-dsl-contracts`
8. `formally-bmad-dsl-contract-stubs`
9. explicit scaffold approval
10. `formally-bmad-implementation-contracts`
11. `formally-bmad-code-verification`
12. `formally-bmad-dsl-verification`

## Notes

- The DSL path is the supported Formally BMAD workflow in this repository.
- Rust defaults to `Kani` as the canonical verification target unless config overrides it.
- Implementation should not start until the scaffold has been generated and approved.
