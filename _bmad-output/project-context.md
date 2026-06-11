---
project_name: "bmadOntologies"
user_name: "David"
date: "2026-06-11"
sections_completed:
  - technology_stack
  - language_specific_rules
  - framework_specific_rules
  - testing_rules
  - code_quality_style_rules
  - development_workflow_rules
  - critical_dont_miss_rules
existing_patterns_found: 8
status: "complete"
rule_count: 60
optimized_for_llm: true
---

# Project Context for AI Agents

_This file contains critical rules and patterns that AI agents must follow when implementing code in this project. Focus on unobvious details that agents might otherwise miss._

---

## Technology Stack & Versions

- BMad/BMM module repository centered on skill authoring rather than application delivery
- BMM configuration version: `6.8.1-next.0` from `_bmad/bmm/config.yaml`
- Primary artifact formats: Markdown, YAML, TOML, CSV
- Automation language: Python `>=3.10` in helper scripts; one legacy-compatible helper declares `>=3.9`
- Repository structure assumes BMAD skill packaging: `SKILL.md` plus optional `assets/`, `references/`, and `scripts/` per skill
- Formal-methods extension is first-class: Formally BMAD skills define canonical-model conventions and automated-reasoning integration points
- Current repository evidence does not establish a JavaScript, TypeScript, Rust, or Python application runtime stack; agents must not invent one

## Critical Implementation Rules

### Language-Specific Rules

- Treat Python in this repo as helper-script infrastructure, not as an application framework layer
- Keep helper scripts directly executable with a shebang and inline script metadata when they are intended to run standalone
- Prefer `pathlib.Path` for filesystem work; do not reintroduce string-concatenated path handling
- Preserve `{project-root}` placeholders in config-facing values until a script explicitly resolves them to concrete paths
- Use UTF-8 for all file reads and writes, and write deterministic text artifacts with trailing newlines
- Prefer JSON for machine-readable outputs between scripts and workflows; print structured results to stdout and reserve stderr for operational errors
- Use explicit numeric exit codes for CLI scripts so success, validation failure, and runtime failure stay distinguishable
- Keep functions small and purpose-specific; current scripts separate path resolution, discovery, serialization, and report-writing concerns
- Prefer standard-library implementations unless a dependency is already justified; `pyyaml` appears only where YAML parsing is required
- Do not invent async patterns, web servers, or package-level abstractions that the repo does not use

### Framework-Specific Rules

- Treat BMAD skills as the primary framework unit; each skill should define behavior in `SKILL.md` and keep auxiliary logic in `scripts/`, `references/`, and `assets/` only when needed
- Follow the activation contract in each skill exactly: load required config first, enforce prerequisite checks, and stop early when setup state or source inputs are missing
- Prefer deterministic workspace helpers for artifact creation instead of ad hoc file creation inside conversational flows
- Keep BMAD artifacts readable and user-facing; formal or machine-oriented detail belongs in companion files, reports, or canonical-model state
- For Formally BMAD workflows, never write canonical truth directly from a lifecycle workflow when the steward is the declared authority
- Treat `_bmad/formally-bmad/` as the durable formal state boundary; workflows may read from it, but ownership of consistency, provenance, and status remains centralized
- When a skill says a contradiction or missing prerequisite must block progress, do not soften that rule in implementation
- Use stage-aware validation semantics where the workflow defines them; early artifacts may tolerate uncertainty, but implementation-facing artifacts should tighten validation
- External ontology or reasoning-tool integrations must degrade explicitly when unavailable; agents must not fabricate successful tool access or repository results
- Preserve the BMad-style user experience even when adding formal-methods behavior: concise conversational guidance, artifact-oriented outputs, and clear handoff to the next skill

### Testing Rules

- Use `unittest` for helper-script tests unless the repository establishes a different test framework in the same area
- Keep tests close to the scripts they validate under `scripts/tests/` within the owning skill or module directory
- Match test filenames to the script or behavior under test; current patterns include both underscore and hyphen legacy variants, so prefer the active canonical name but preserve compatibility when touching older areas
- Prioritize deterministic tests for workspace creation, config merging, path resolution, artifact discovery, and report generation
- Validate CLI behavior explicitly: stdout structure, created files, and exit codes are part of the contract
- Treat setup smoke tests and validation checks as first-class behavior, not incidental logging
- When a workflow distinguishes `complete`, `blocked`, `accepted_for_validation`, or degraded states, tests should assert those state transitions directly
- Avoid tests that depend on live external ontology repositories or installed reasoning tools unless the test is explicitly designed as an environment-dependent smoke check
- Prefer temporary directories and isolated fixture trees over real project-state mutation
- When changing artifact templates or workspace helpers, update tests to verify the expected starter-file set and companion-folder structure

### Code Quality & Style Rules

- Prefer concise, high-signal Markdown; headings, bullets, and tables should carry structure without filler prose
- Keep `SKILL.md` files explicit about activation, prerequisites, workflow steps, path conventions, and handoff behavior
- Use stable file and folder naming: skill directories in kebab-case, Python helpers in snake_case, and artifact/report files with descriptive lowercase names
- Favor deterministic templates and starter files over freeform artifact generation so outputs stay comparable across runs
- Write focused module and function docstrings that explain the script contract, especially inputs, outputs, and exit-code semantics
- Add inline comments only where behavior would otherwise be non-obvious; the repo’s current style does not use commentary to narrate trivial code
- Preserve auditability in both docs and scripts: name affected artifacts, statuses, provenance, and decision points explicitly
- Keep CSV, JSON, YAML, and Markdown outputs structurally clean and machine-safe; avoid ad hoc formatting drift
- When merging or regenerating shared registries, use anti-zombie replacement patterns rather than appending duplicate stale entries
- Do not blur operational memory, generated reports, and canonical source-of-truth state; each has a separate purpose and location

### Development Workflow Rules

- Treat `_bmad/` configuration and registry files as shared workflow infrastructure; changes there should remain schema-aware and deterministic
- Use `_bmad/custom/` for team or user behavior overrides instead of editing installed workflow logic when customization is the real goal
- Preserve the committed-vs-personal split: team customization files are intended for shared project behavior, while user-local overrides stay local
- Support headless operation where the surrounding skill or module already defines it; headless mode should skip conversational prompts but not skip validation or prerequisite checks
- Keep workflow outputs in the configured artifact locations such as `_bmad-output/`, planning artifacts, implementation artifacts, or module-owned report folders
- Respect BMAD handoff semantics: each workflow should end with status plus the next recommended skill or action when the source workflow defines one
- When updating module registration data like `config.yaml` or `module-help.csv`, use replacement or merge helpers rather than manual edits that can leave stale entries behind
- Preserve lifecycle order where the repo defines it: setup before stewarded formal work, earlier artifact stages before implementation-facing stages, and stricter validation as commitments become more concrete
- Do not assume git metadata is available from every working directory; workflow logic should not depend on branch or commit inspection unless the environment actually provides a repository
- When a workflow is blocked by missing source material, missing setup state, or failed validation, report the blocker clearly and stop instead of inventing downstream progress

### Critical Don't-Miss Rules

- Never store canonical assertions, validation status, contradictions, overrides, readiness facts, or provenance only in steward memory; anything audit-relevant belongs under `_bmad/formally-bmad/`
- Do not treat degraded, skipped, or export-only checks as equivalent to passed validation
- Never allow setup to complete with zero supported automated reasoning tools, even if export generation still works
- Do not silently promote `candidate`, `provisional`, or imported external concepts to `accepted`; promotion requires clear user confirmation where the workflow says so
- Treat competing early-stage ideas as alternatives, not contradictions, until they are actually promoted into accepted commitments
- When validation reports contradiction, block workflow progress unless the user explicitly overrides continuation; if overridden, mark the model inconsistent and record downstream risk
- Do not rewrite source artifacts during import or repair-like situations unless the workflow explicitly permits it and the user accepts the change
- If web access, ontology repositories, or optional tool backends are unavailable, produce a degraded report and say so plainly; do not fabricate successful retrievals or checks
- Keep unresolved assumptions, missing coverage, stale dependencies, and blockers visible in the local validation or blocker artifacts; do not hide them to make an artifact look ready
- Do not rely on proof assistants alone to satisfy the minimum automated-validation capability for Formally BMAD setup

---

## Usage Guidelines

**For AI Agents:**

- Read this file before implementing any code or changing workflow artifacts
- Follow all rules exactly as documented, especially blocking and provenance rules
- When in doubt, prefer the more restrictive interpretation and preserve auditability
- Update this file when repo conventions or formal-workflow boundaries materially change

**For Humans:**

- Keep this file lean and focused on non-obvious agent-facing rules
- Update it when the technology stack, workflow contracts, or formal-state boundaries change
- Remove rules that become redundant or obvious from surrounding repository structure
- Review it periodically to keep guidance accurate and compact

Last Updated: `2026-06-11`
