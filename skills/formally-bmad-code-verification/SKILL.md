---
name: formally-bmad-code-verification
description: Verifies implementation against generated contracts. Use when the user requests to 'verify code contracts', 'check implementation against contracts', or 'run code verification'.
---

# formally-bmad-code-verification

## Overview

This workflow verifies implementation artifacts against generated code contracts and their upstream formal obligations. Act as an implementation verification engineer: collect tool-backed evidence where the language/toolchain allows it, distinguish bounded or degraded evidence from stronger proofs, and refuse to equate comments or unchecked assertions with verified conformance.

## Conventions

- Bare paths (e.g. `scripts/code_verification_workspace.py`) resolve from the skill root.
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

If `--headless` or `-H` is invoked, require a contract workspace or explicit implementation-facing contract set plus a target code scope. Without that, create only the workspace and report that code verification needs generated contracts and implementation targets.

## Workflow

### Establish Verification Scope

Load or ask for:

- contract workspace or contract inventory;
- target language: `python`, `c`, or `rust`;
- implementation paths, crates, modules, or files to verify;
- relevant upstream requirements, architecture constraints, and story criteria;
- available toolchain backends detected by setup or known in the environment.

If the selected code lacks explicit contracts and only has comments or pseudocode, stop short of strong verification claims and report that contract generation is incomplete.

### Initialize Workspace

Run the deterministic workspace helper once the verification scope is known:

```bash
python3 scripts/code_verification_workspace.py --project-root {project-root} --module-root "{formally_bmad_project_root}" --target "{target-language-and-scope}"
```

The helper creates `{formally_bmad_project_root}/reports/code-verification/<safe-target>/` with starter files for scope, tool runs, findings, coverage, counterexamples, readiness, and summary.

### Select Verification Path Conservatively

Choose only backends that fit the actual contract notation and implementation language:

- Python: prefer CrossHair when contracts are written in a symbolic-friendly subset; use `deal` checking modes when `deal` contracts exist; runtime assertions or tests are degraded evidence only unless tied to an explicit contract surface.
- C: prefer Frama-C WP for ACSL deductive obligations, E-ACSL for executable runtime checking of ACSL, and CBMC for bounded assertion or harness-based checking.
- Rust: prefer Kani for proof harnesses, assertions, and function-contract style checks; use Prusti or Creusot when the code and annotations fit those tools; plain `assert!` or `debug_assert!` without a verifier remains runtime-only evidence.

Do not switch languages, contract styles, or proof models mid-report without saying that the evidence is mixed and potentially non-equivalent.

### Run and Classify Evidence

For each checked contract or contract group, record:

- chosen backend;
- source contract IDs and implementation paths;
- outcome: `passed`, `failed`, `counterexample`, `degraded`, `skipped`, `not-applicable`, or `unchecked`;
- evidence class: `deductive`, `symbolic`, `bounded`, `runtime`, `test`, or `manual-review`;
- whether the result is faithful to the written contract or only to a weaker approximation.

Timeouts, unsupported language fragments, missing annotations, or harness-only checks are degraded evidence, not proof of correctness.

### Check Upstream Contract Coverage

Audit whether the implementation evidence actually covers the generated contracts:

- which requirements have contract-backed implementation evidence;
- which contracts were only exported but not checked;
- which contracts were weakened during translation;
- which obligations still rely only on runtime checks, tests, or manual review.

Implementation readiness is blocked if strong claims are made without matching tool evidence.

### Produce Reports

Maintain the report workspace with:

- `scope.md` — verification scope and target language;
- `tool-runs.md` — executed or planned backend runs and outcomes;
- `coverage.md` — contract-to-code coverage and evidence class;
- `counterexamples.md` — failing cases, traces, or missing-proof notes;
- `readiness.md` — implementation conformance status and rationale;
- `summary.md` — concise verdict and next actions;
- `manifest.json`.

Where concrete tool runs exist, also record lightweight references under `{formally_bmad_project_root}/tool-runs/`.

### Handoff

End with:

- code-verification report workspace;
- target language and implementation scope;
- passed, failed, degraded, and unchecked contract counts;
- contracts lacking faithful implementation evidence;
- recommended next workflow: `formally-bmad-formal-verification` for project-level readiness and traceability review.
