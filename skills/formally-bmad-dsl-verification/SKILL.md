---
name: formally-bmad-dsl-verification
description: Verifies the DSL branch baseline, deltas, coverage, and readiness. Use when the user requests to 'run DSL verification', 'check the DSL baseline', or 'audit delta validation and readiness'.
---

# formally-bmad-dsl-verification

## Overview

This workflow runs checkpoint verification, increment-validation review, readiness checks, traceability audits, contradiction analysis, evidence review, and repair reporting over the evolving `formally-bmad-dsl-*` branch. Act as a formal verification reporter: make accepted baselines, deltas, degraded checks, contradictions, recheck obligations, and repair decisions easy to inspect.

This branch is delta-aware. The verification target is not only isolated generated properties, but the evolving validated baseline and the proposed increments applied to it.

Earlier DSL workflows may produce canonical assertions, ontology and ASM projections, generated properties, accepted deltas, and partial backend evidence. This workflow is the place where that material is systematically audited, rechecked, and turned into explicit verification reporting.

Never end the session silently. Before any pause, stop, or handoff, explicitly tell the user what was verified, what was only structurally prepared, what failed or was skipped, and the next concrete action.

This branch is sequential. Do not suggest bypassing verification in favor of direct implementation. Implementation work belongs only after verification has been executed and its outcome has been reported explicitly.

## Conventions

- Bare paths (e.g. `scripts/verification_workspace.py`) resolve from the skill root.
- `{skill-root}` resolves from this skill's installed directory.
- `{project-root}`-prefixed paths resolve from the project working directory.
- `{skill-name}` resolves to the skill directory's basename.

## On Activation

Load available config from `{project-root}/_bmad/config.yaml` and `{project-root}/_bmad/config.user.yaml` (root level and `formally-bmad-dsl` section). Resolve these values, using setup defaults only when config is absent:

- `formally_bmad_dsl_project_root`: `{project-root}/_bmad/formally-bmad-dsl`
- `formally_bmad_dsl_canonical_model_path`: `{project-root}/_bmad/formally-bmad-dsl/canonical`
- `formally_bmad_dsl_validation_strictness`: `stage-aware`
- `formally_bmad_dsl_report_format`: `markdown,html`

If `{formally_bmad_dsl_project_root}` or `{formally_bmad_dsl_canonical_model_path}/status.md` is missing, stop and direct the user to run `formally-bmad-dsl-setup`.

If `--headless` or `-H` is invoked, run a verification checkpoint over the current DSL branch state and always produce Markdown reporting.

## Workflow

### Prepare Verification Workspace

Run the deterministic workspace helper:

```bash
python3 scripts/verification_workspace.py --project-root {project-root} --module-root "{formally_bmad_dsl_project_root}" --scope "{scope}"
```

The helper creates a timestamped DSL verification report workspace under `{formally_bmad_dsl_project_root}/reports/dsl-verification/`, indexes known companion artifacts, and writes starter report files.

### Determine Verification Scope

Confirm scope unless running headless:

- whole DSL branch baseline;
- a selected artifact family such as brainstorming, PRD, architecture, epics, or stories;
- a selected delta or increment-validation set;
- a readiness audit for implementation planning;
- a contradiction or recheck review only;
- a traceability or coverage audit only.

Scope determines which companions, delta ledgers, validation ledgers, provenance files, and tool-run references to inspect.

### Audit The Accepted Baseline

Review the currently accepted baseline across the DSL branch:

- canonical assertions;
- accepted deltas;
- ontology and ASM projections;
- generated properties;
- backend checks;
- downstream PRD, architecture, epic, and story artifacts where in scope.

Distinguish clearly between:

- accepted baseline elements;
- deferred or rejected deltas;
- contested requirements or design commitments;
- unchecked but accepted increments;
- backend-evidenced increments.

### Check Increment Validation Quality

Review whether each significant accepted or proposed delta has:

- explicit source assertion IDs;
- explicit target layers;
- explicit affected ontology/ASM/property sets;
- explicit increment-validation result;
- explicit backend evidence state or explicit deferral.

Flag as findings:

- missing delta rows;
- missing increment-validation rows;
- accepted deltas with unclear impact sets;
- accepted deltas whose recheck obligations were not recorded;
- evidence claims stronger than the recorded backend status.

### Review Coverage And Recheck Obligations

Review whether:

- accepted behavioral assertions generated expected properties;
- accepted deltas triggered expected rechecks;
- architecture deltas triggered recheck obligations where coordination, state ownership, or event flow changed;
- epic and story stages preserved inherited evidence posture and did not silently erase deferred or contested commitments.

Missing recheck planning is a finding, not a cosmetic gap.

### Choose Tool Families Conservatively

For the MVP, continue to route checks by logic family using the currently supported backends detected by setup. Prefer the strongest currently available detected backend for each check family, record degraded checks when a backend is missing, and avoid inventing proof obligations that cannot yet be exercised by the installed toolchain.

When you invoke or conceptually invoke a backend, record:

- logic family;
- chosen backend;
- why that backend fits the artifact or obligation;
- whether the result is authoritative, degraded, or suggestive only;
- where the input/output should be stored under `{formally_bmad_dsl_project_root}/tool-runs/`.

Use backend checks both for:

- checking newly generated obligations;
- rechecking obligations affected by accepted deltas or architecture changes.

### Assess Readiness Conservatively

Readiness should be `ready`, `not-ready`, `blocked`, or `degraded`, with rationale.

Assess readiness using DSL-branch-specific thresholds:

- accepted requirements have preserved evidence class and source lineage;
- accepted deltas have increment-validation records;
- important accepted deltas have either backend evidence or explicit deferred-verification rationale;
- architecture-level deltas have explicit recheck planning;
- epic coverage is intentional and evidence-aware;
- story readiness does not ignore contested or deferred commitments;
- claim strength in downstream artifacts does not exceed recorded evidence.

If no actual tool-backed checks were run for relevant obligations, do not issue a strong readiness sign-off. At most, report that the artifact is structurally prepared for stronger verification.

### Audit Traceability

Trace links from:

- brainstorm outcomes to canonical assertions;
- canonical assertions to deltas;
- deltas to ontology and ASM impacts;
- deltas to generated properties and backend checks;
- accepted requirements to source assertions and deltas;
- architecture decisions to requirements and deltas;
- epics and stories to inherited evidence posture;
- repair proposals to affected artifacts.

Missing links are findings.

### Analyze Contradictions And Repair Needs

For contradictions, use source-artifact language before formal notation. Include:

- affected artifacts and IDs;
- delta or baseline element in conflict;
- validation/tool evidence or counterexample references when available;
- downstream risk;
- repair proposals;
- whether a contradiction is inherited, newly introduced, or still unresolved.

Contradictions and unresolved critical recheck failures block readiness unless explicitly overridden.

### Produce Reports

Maintain the report workspace with:

- `checkpoint-verification.md`;
- `baseline-audit.md`;
- `increment-validation-audit.md`;
- `rechecks.md`;
- `readiness.md`;
- `traceability-audit.md`;
- `contradictions.md`;
- `coverage.md`;
- `repair-review.md`;
- `summary.md`;
- `manifest.json`.

Also update `{formally_bmad_dsl_project_root}/reports/latest-dsl-verification-summary.md` with the current result and report workspace path.

Where tool-backed checks were run or planned, also maintain lightweight tool-run references under `{formally_bmad_dsl_project_root}/tool-runs/` so later reports can trace:

- the backend selected;
- the exported view or input artifact;
- the outcome category;
- the relevant source assertions, deltas, requirements, or decisions.

### Handoff

End with:

- verification report workspace;
- readiness status;
- blocking contradictions or failed rechecks;
- degraded or skipped checks;
- traceability and coverage gaps;
- repair proposals requiring user decision;
- mandatory next action: either perform the required repair/rework workflow for blocked findings, or if verification is complete and acceptable, explicitly report that the DSL workflow sequence has reached its verification gate and only then allow implementation planning to begin.
