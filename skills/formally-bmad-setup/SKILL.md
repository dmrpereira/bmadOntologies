---
name: formally-bmad-setup
description: Configures Formally BMAD project state. Use when the user requests to 'setup Formally BMAD', 'configure formally-bmad', or 'install formally-bmad module'.
---

# formally-bmad-setup

## Overview

This skill configures Formally BMAD by registering the module, collecting module settings, creating durable project state, detecting BMad artifacts, verifying automated reasoning capability, and producing a setup report. Act as a formal methods aware setup engineer: keep the interaction BMad-like, but do not allow installation to complete unless the baseline validation toolchain is executable: at least one supported SMT solver and at least one supported first-order or SAT solver.

## Conventions

- Bare paths (e.g. `scripts/setup_environment.py`) resolve from the skill root.
- `{skill-root}` resolves to this skill's installed directory.
- `{project-root}`-prefixed paths resolve from the project working directory.
- `{skill-name}` resolves to the skill directory's basename.

## On Activation

Read `assets/module.yaml` for module metadata, configuration variables, post-install notes, and agent roster. Load available config from `{project-root}/_bmad/config.yaml` and `{project-root}/_bmad/config.user.yaml` (root level and `formally-bmad` section). If neither exists, use these defaults and tell the user setup will create module-specific configuration:

- `formally_bmad_project_root`: `{project-root}/_bmad/formally-bmad`
- `formally_bmad_canonical_model_path`: `{project-root}/_bmad/formally-bmad/canonical`
- `formally_bmad_validation_strictness`: `stage-aware`
- `formally_bmad_auto_apply_repairs`: `confirm-before-edit`
- `formally_bmad_tool_profile`: `auto-detect`
- `formally_bmad_min_required_tools`: `1`
- `formally_bmad_export_only_fallback`: `true`
- `formally_bmad_report_format`: `markdown,html`

If the user invoked headless mode (`--headless` or `-H`), apply defaults and inferred config without interactive questions. Record assumptions in `.decision-log.md` if you change this skill.

## Workflow

### Confirm Configuration and Registration

Confirm or collect only the values that matter for this project:

- where Formally BMAD should store project state;
- whether validation strictness should remain `stage-aware`;
- whether accepted repairs should remain `confirm-before-edit`;
- whether the total supported tool count should remain `1` or higher; this does not replace the mandatory baseline validation toolchain of at least one SMT solver plus at least one first-order or SAT solver unless the user explicitly accepts an unsupported non-validating fork;
- whether missing optional backends may degrade to export-only checks after the minimum tool requirement passes.

Default to the module plan values unless the user asks for changes.

The module registration assets are:

- `assets/module.yaml` — module identity, config variables, and agent roster;
- `assets/module-help.csv` — capability registry for BMad help.

### Register Module

Write a temp JSON file with collected answers shaped as `{"core": {...}, "module": {...}}`. Omit `core` if the project already has core config. Run:

```bash
uv run scripts/merge-config.py --config-path "{project-root}/_bmad/config.yaml" --user-config-path "{project-root}/_bmad/config.user.yaml" --module-yaml assets/module.yaml --answers {temp-file} --legacy-dir "{project-root}/_bmad"
python3 scripts/merge-help-csv.py --target "{project-root}/_bmad/module-help.csv" --source assets/module-help.csv --legacy-dir "{project-root}/_bmad" --module-code formally-bmad
```

If either script exits non-zero, surface the JSON error and stop. Config values stored in files must keep the literal `{project-root}` token; only filesystem creation resolves it to the actual project path.

### Run Formally BMAD Setup Helper

Run the deterministic setup helper from the skill root:

```bash
python3 scripts/setup_environment.py --project-root {project-root} --module-root "{formally_bmad_project_root}" --canonical-path "{formally_bmad_canonical_model_path}" --min-tools "{formally_bmad_min_required_tools}"
```

If a config value is not yet physically written, substitute the default resolved path. The helper creates the module folder structure, detects BMad artifacts, detects supported automated reasoning tools, checks whether the baseline validation gate is satisfied, runs lightweight smoke tests, writes setup state files, and emits JSON.

If the script cannot run, perform the same checks manually and explain that script automation was unavailable. Do not mark setup complete without verifying at least one supported SMT solver and at least one supported first-order or SAT solver.

### Supported Tool Families

Track detected executables from these automated reasoning families:

- SMT solvers: `z3`, `cvc5`, `cvc4`;
- first-order provers/model finders: `vampire`, `eprover`, `prover9`, `mace4`;
- SAT solvers: `kissat`, `cadical`, `minisat`, `glucose`;
- temporal/model checking tools: `tlc`, `apalache`, `alloy`;
- ontology reasoners/tools: `robot`, `hermit`, `elk`, `jfact`, `factplusplus`, `pellet`.

Also report specialized supporting tools when available:

- temporal satisfiability tooling: `black`;
- ontology workflow tooling: `robot` as a CLI ontology workbench in addition to its role in the ontology tool family;
- proof assistants: `coqc`, `rocq`, `lean`, `lake`, `isabelle`.

The setup helper searches the normal `PATH`. If session-local tools are installed outside `PATH`, provide extra directories through `FORMALLY_BMAD_EXTRA_TOOL_DIRS` or rely on known local install paths such as `/private/tmp/black-install/bin` and `/private/tmp/robot/bin`.

The baseline validation requirement is stricter than the total tool count:

- at least one SMT solver must be detected and usable;
- at least one first-order or SAT solver must also be detected and usable;
- temporal/model-checking tools, specialized temporal satisfiability tooling, ontology reasoners/tools, and proof assistants are relevant and should be reported, but they do not satisfy the baseline by themselves.

Proof assistants such as Coq/Rocq, Lean, Isabelle, or HOL tools count as relevant formal tooling, but they cannot replace the baseline SMT plus first-order-or-SAT requirement.

### Interpret Results

If the helper reports that the baseline validation gate is not satisfied, stop setup. Produce a blocking installation guidance message using the helper report. Do not create a success narrative around export-only mode or proof-assistant-only availability.

If the baseline validation gate is satisfied:

- confirm the initialized project structure;
- summarize detected BMad artifacts;
- summarize baseline validation availability, plus available and missing optional reasoning tools, specialized temporal tooling, ontology workbench tooling, and proof assistants;
- note any degraded optional checks;
- point to the generated setup report under `{formally_bmad_project_root}/reports/`.

### Cleanup Legacy Installer Files

After config and help registration succeed, run:

```bash
python3 scripts/cleanup-legacy.py --bmad-dir "{project-root}/_bmad" --module-code formally-bmad --also-remove _config --skills-dir "{project-root}/.claude/skills"
```

If cleanup reports that installed skills cannot be verified, surface the warning and continue; the Formally BMAD project state and module registration are the critical setup outcomes.

### Handoff

Finish with the current setup status and the next recommended skill: `formally-bmad-agent-steward`. If setup is blocked, the next step is installing at least one supported SMT solver and at least one supported first-order or SAT solver, then rerunning this setup workflow.
