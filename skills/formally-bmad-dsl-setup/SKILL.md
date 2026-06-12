---
name: formally-bmad-dsl-setup
description: Configures the Formally BMAD parallel DSL branch. Use when the user requests to 'setup DSL Formally BMAD', 'configure the formally-bmad DSL branch', or 'install the formally-bmad-dsl module'.
---

# formally-bmad-dsl-setup

## Overview

This skill configures the isolated `formally-bmad-dsl-*` branch by registering a DSL-specific module/help surface, collecting branch settings, creating durable project state, detecting BMad artifacts, verifying automated reasoning capability, and producing a DSL-branded setup report. Act as a formal-methods-aware setup engineer for the DSL branch: keep the interaction BMad-like, but do not allow installation to complete unless the baseline validation toolchain is executable: at least one supported SMT solver and at least one supported first-order or SAT solver.

This setup is intentionally separate from `formally-bmad-setup`. It uses its own module code, its own state root under `_bmad/formally-bmad-dsl/`, its own help rows, and its own local helper scripts. It should be the only setup command used before running `formally-bmad-dsl-brainstorming`.

Never end the session silently. If setup must stop, block, or pause, explicitly tell the user what completed, what failed or is still missing, where the relevant artifacts or reports were written, and the exact next step.

## Conventions

- Bare paths resolve from the skill root.
- `{skill-root}` resolves to this skill's installed directory.
- `{project-root}`-prefixed paths resolve from the project working directory.
- `{skill-name}` resolves to the skill directory's basename.

## On Activation

Read `assets/module.yaml` for module metadata, configuration variables, and post-install notes. Load available config from `{project-root}/_bmad/config.yaml` and `{project-root}/_bmad/config.user.yaml` when present; if the host BMad installation only has TOML root config such as `{project-root}/_bmad/config.toml` and `{project-root}/_bmad/config.user.toml`, treat that as a valid pre-existing BMad install and proceed. This DSL setup will create its own YAML registration files if needed under `_bmad/`, using the `formally-bmad-dsl` section.

If no DSL root YAML config exists yet, use these defaults and tell the user setup will create DSL module-specific configuration:

- `formally_bmad_dsl_project_root`: `{project-root}/_bmad/formally-bmad-dsl`
- `formally_bmad_dsl_canonical_model_path`: `{project-root}/_bmad/formally-bmad-dsl/canonical`
- `formally_bmad_dsl_validation_strictness`: `stage-aware`
- `formally_bmad_dsl_auto_apply_repairs`: `confirm-before-edit`
- `formally_bmad_dsl_tool_profile`: `auto-detect`
- `formally_bmad_dsl_min_required_tools`: `1`
- `formally_bmad_dsl_export_only_fallback`: `true`
- `formally_bmad_dsl_report_format`: `markdown,html`

If the user invoked headless mode (`--headless` or `-H`), apply defaults and inferred config without interactive questions.

## Workflow

### Confirm Configuration and Registration

Confirm or collect only the values that matter for this project:

- where the DSL branch should store project state;
- whether validation strictness should remain `stage-aware`;
- whether accepted repairs should remain `confirm-before-edit`;
- whether the total supported tool count should remain `1` or higher; this does not replace the mandatory baseline validation toolchain of at least one SMT solver plus at least one first-order or SAT solver unless the user explicitly accepts an unsupported non-validating fork;
- whether missing optional backends may degrade to export-only checks after the minimum tool requirement passes.

Default to the module plan values unless the user asks for changes.

The registration assets are:

- `assets/module.yaml` — DSL setup identity and config variables;
- `assets/module-help.csv` — DSL module capability registry for BMad help.

### Register Module

Write a temp JSON file with collected answers shaped as `{"core": {...}, "module": {...}}`. Omit `core` if the project already has core config. Run:

```bash
uv run scripts/merge-config.py --config-path "{project-root}/_bmad/config.yaml" --user-config-path "{project-root}/_bmad/config.user.yaml" --module-yaml assets/module.yaml --answers {temp-file} --legacy-dir "{project-root}/_bmad"
python3 scripts/merge-help-csv.py --target "{project-root}/_bmad/module-help.csv" --source assets/module-help.csv --legacy-dir "{project-root}/_bmad" --module-code formally-bmad-dsl
```

If either script exits non-zero, surface the JSON error and stop. Config values stored in files must keep the literal `{project-root}` token; only filesystem creation resolves it to the actual project path.

### Run DSL Setup Helper

Run the deterministic setup helper:

```bash
python3 scripts/setup_environment.py --project-root {project-root} --module-root "{formally_bmad_dsl_project_root}" --canonical-path "{formally_bmad_dsl_canonical_model_path}" --min-tools "{formally_bmad_dsl_min_required_tools}" --module-label "Formally BMAD DSL" --status-title "Formally BMAD DSL Canonical Model Status" --index-title "Formally BMAD DSL Index"
```

If the helper cannot run, perform the same checks manually and explain that script automation was unavailable. Do not mark setup complete without verifying at least one supported SMT solver and at least one supported first-order or SAT solver.

### Interpret Results

If the helper reports that the baseline validation gate is not satisfied, stop setup. Produce a blocking installation guidance message using the helper report.

If the baseline validation gate is satisfied:

- confirm the initialized project structure;
- summarize detected BMad artifacts;
- summarize baseline validation availability and optional reasoning tooling;
- point to the generated setup report under `{formally_bmad_dsl_project_root}/reports/`.

### Cleanup Legacy Installer Files

After config and help registration succeed, run:

```bash
python3 scripts/cleanup-legacy.py --bmad-dir "{project-root}/_bmad" --module-code formally-bmad-dsl --skills-dir "{project-root}/.claude/skills" --skills-dir "{project-root}/.codex/skills" --skills-dir "{project-root}/.pi/skills"
```

If cleanup reports that installed DSL skills cannot be verified, surface the warning and continue; the DSL project state and DSL branch registration are the critical setup outcomes.

### Handoff

Finish with the current setup status and the next recommended skills: `formally-bmad-dsl-agent-steward`, followed by `formally-bmad-dsl-brainstorming`.
