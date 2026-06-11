# Formally BMAD Quickstart

## What This Module Adds

Formally BMAD extends BMad artifacts with a project-level canonical model and automated consistency/verification hooks.

Default on-disk state lives under:

- `{project-root}/_bmad/formally-bmad/`
- Canonical model: `{project-root}/_bmad/formally-bmad/canonical/`

## Setup (Install)

Run the setup capability:

- Skill: `formally-bmad-setup`

Setup does two things:

1. Registers the module in `{project-root}/_bmad/config.yaml` and `{project-root}/_bmad/module-help.csv`
2. Initializes the module state and validates at least one supported automated reasoning tool is available

## Tool Requirement (Hard Gate)

Setup is blocked unless **at least one** supported automated reasoning tool is detected on `PATH`.

Supported families (examples):

- SMT: `z3`, `cvc5`
- First-order: `vampire`, `eprover`
- Temporal: `tlc`, `apalache`, `alloy`
- Ontology/DL: `robot`, `hermit`, `elk`, `pellet`

If zero tools are detected, setup must not proceed.

## Verify Setup Output

After setup completes, expect:

- `{project-root}/_bmad/formally-bmad/reports/setup-report.md`
- `{project-root}/_bmad/formally-bmad/canonical/status.md`
- Canonical folders under `{project-root}/_bmad/formally-bmad/canonical/`:
  - `model/`, `ontology/`, `temporal/`, `meta/`, `versions/`

## Notes

- Proof assistants are not primary targets; automated provers/solvers are preferred.
- Human-readable specs remain BMad-style Markdown, with logic-native companions produced alongside them.

