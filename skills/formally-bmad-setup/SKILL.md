---
name: formally-bmad-setup
description: Configures Formally BMAD project state. Use when the user requests to 'setup Formally BMAD', 'configure formally-bmad', or 'install formally-bmad module'.
---

# formally-bmad-setup

## Overview

This skill configures Formally BMAD by registering the module, collecting module settings, creating durable project state, detecting BMad artifacts, verifying automated reasoning capability, and producing a setup report. Act as a formal methods aware setup engineer: keep the interaction BMad-like, but do not allow installation to complete unless at least one supported automated reasoning tool is executable.

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
- whether at least one automated reasoning tool is required; this must stay at `1` or higher unless the user explicitly accepts an unsupported non-validating fork;
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

If a config value is not yet physically written, substitute the default resolved path. The helper creates the module folder structure, detects BMad artifacts, detects supported automated reasoning tools, runs lightweight smoke tests, writes setup state files, and emits JSON.

If the script cannot run, perform the same checks manually and explain that script automation was unavailable. Do not mark setup complete without verifying at least one supported automated reasoning tool.

### Supported Tool Families

Accept any detected executable from these automated reasoning families as satisfying the minimum tool requirement:

- SMT solvers: `z3`, `cvc5`, `cvc4`;
- first-order provers/model finders: `vampire`, `eprover`, `prover9`, `mace4`;
- temporal/model checking tools: `tlc`, `apalache`, `alloy`;
- ontology reasoners/tools: `robot`, `hermit`, `elk`, `jfact`, `factplusplus`, `pellet`.

Proof assistants such as Coq/Rocq, Lean, Isabelle, or HOL tools do not satisfy the minimum requirement by themselves. They may be optional advanced export targets later.

### Interpret Results

If the helper reports zero supported automated reasoning tools, stop setup. Produce a blocking installation guidance message using the helper report. Do not create a success narrative around export-only mode.

If at least one supported tool is available:

- confirm the initialized project structure;
- summarize detected BMad artifacts;
- summarize available and missing optional reasoning tools;
- note any degraded optional checks;
- point to the generated setup report under `{formally_bmad_project_root}/reports/`.

### Cleanup Legacy Installer Files

After config and help registration succeed, run:

```bash
python3 scripts/cleanup-legacy.py --bmad-dir "{project-root}/_bmad" --module-code formally-bmad --also-remove _config --skills-dir "{project-root}/.claude/skills"
```

If cleanup reports that installed skills cannot be verified, surface the warning and continue; the Formally BMAD project state and module registration are the critical setup outcomes.

### Handoff

Finish with the current setup status and the next recommended skill: `formally-bmad-agent-steward`. If setup is blocked, the next step is installing at least one supported automated reasoning tool and rerunning this setup workflow.
