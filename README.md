# Formally BMAD DSL

This repository contains the active Formally BMAD DSL module source. The older non-DSL workflow family has been removed. The supported path is the DSL-based lifecycle only.

## What It Provides

The DSL module adds:

- canonical DSL baseline management under `{project-root}/_bmad/formally-bmad-dsl/`
- DSL-first brainstorming, PRD, architecture, epics, and stories workflows
- per-story contract derivation before implementation
- contract-bearing scaffold generation under `{project-root}/scaffold/{story-id}/`
- implementation governance for preserving and extending formal contracts
- implementation verification and final DSL verification reporting

The intended workflow is:

1. `formally-bmad-dsl-setup`
2. `formally-bmad-dsl-agent-steward`
3. `formally-bmad-dsl-brainstorming`
4. `formally-bmad-dsl-prd`
5. `formally-bmad-dsl-architecture`
6. `formally-bmad-dsl-epics`
7. `formally-bmad-dsl-stories`
8. `formally-bmad-dsl-contracts`
9. `formally-bmad-dsl-contract-stubs`
10. explicit scaffold approval
11. `formally-bmad-implementation-contracts`
12. `formally-bmad-code-verification`
13. `formally-bmad-dsl-verification`

## Prerequisite

The target project must already have BMad installed. Formally BMAD DSL is a module on top of an existing BMad project; it does not bootstrap core BMad into an empty folder.

Typical bootstrap commands for a target project are:

```bash
npx bmad-method install
```

or:

```bash
npx bmad-method@next install
```

The target project must already contain:

- `_bmad/`
- core BMad config or normal BMad project state
- an active skills directory such as `.claude/skills/`, `.codex/skills/`, or `.pi/skills/`

## Install

Copy the runtime skill directories from `skills/` into the active skills location of the target project, or use the installer:

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

Each skill directory must become a direct child of the target skills directory.

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

This registers the module in the target project and initializes:

- `{project-root}/_bmad/formally-bmad-dsl/`
- `{project-root}/_bmad/formally-bmad-dsl/canonical/`
- DSL module help/config entries under `_bmad/`

Setup is blocked unless at least:

- one supported SMT solver is available
- one supported first-order or SAT solver is available

Relevant implementation-facing backend families include:

- Python: `pyveritas`, `deal`, `crosshair`, `nagini`, `esbmc`
- C: `frama-c`, `cbmc`, `esbmc`, `verifast`
- Rust: `cargo-kani`, `prusti-rustc`, `cargo-prusti`, `cargo-creusot`, `verus`, `flux`, `verifast`, `esbmc`

The default Rust verification target for the DSL implementation path is `Kani` unless the project config overrides it.

## Notes

- Human-readable artifacts remain Markdown, with formal lineage and verification posture tracked alongside them.
- Contract scaffolds default to `{project-root}/scaffold/{story-id}/`.
- Business-logic implementation is gated behind contract derivation, scaffold generation, and explicit scaffold approval.
- Final sign-off belongs to `formally-bmad-dsl-verification`, after implementation evidence has passed through `formally-bmad-code-verification`.

See [docs/formally-bmad-quickstart.md](/Users/dmrpereira/Propostas/bmadOntologies/docs/formally-bmad-quickstart.md) for the concise operator flow.
