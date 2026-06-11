---
title: 'Module Plan'
status: 'complete'
module_name: 'Formally BMAD'
module_code: 'formally-bmad'
module_description: 'Extends BMad artifacts with formal specifications, ontologies, traceability, readiness checks, and verification reports.'
architecture: 'hybrid: steward agent plus formalized lifecycle workflows'
standalone: true
expands_module: 'BMad ecosystem'
skills_planned:
  - formally-bmad-setup
  - formally-bmad-agent-steward
  - formally-bmad-formal-brainstorming
  - formally-bmad-formal-prd
  - formally-bmad-formal-architecture
  - formally-bmad-formal-epics
  - formally-bmad-formal-stories
  - formally-bmad-formal-import
  - formally-bmad-ontology-alignment
  - formally-bmad-formal-verification
config_variables:
  - formally_bmad_project_root
  - formally_bmad_canonical_model_path
  - formally_bmad_validation_strictness
  - formally_bmad_auto_apply_repairs
  - formally_bmad_tool_profile
  - formally_bmad_min_required_tools
  - formally_bmad_export_only_fallback
  - formally_bmad_report_format
created: '2026-05-30T14:03:54Z'
updated: '2026-05-30T16:14:00Z'
---

# Module Plan

## Vision

Formally BMAD extends the BMad lifecycle with an evolving formal model that is built incrementally as project artifacts are created. It keeps the familiar BMad user experience while adding formal specifications, ontology grounding, automated validation, traceability, readiness checks, and verification reports.

The module covers brainstorming, PRD, architecture, epics, stories, implementation readiness checks, and verification reports. UX specification is explicitly out of scope. For each covered artifact, Formally BMAD preserves the normal Markdown artifact style and creates source-artifact-oriented formal companions containing rigorous English explanations, formal deltas, exports, provenance, and validation results.

The formal layer targets logic families before tool syntaxes: description logic for ontology representation, first-order logic as the default specification foundation, temporal logic for lifecycle and behavioral properties, and higher-order logic only where strictly needed. Automated checking is prioritized over maximal expressiveness. Proof assistants are not primary targets; automated provers, model finders, SMT solvers, temporal model checkers, and ontology reasoners are preferred.

## Architecture

The recommended architecture is a hybrid module: one dedicated steward agent owns the canonical formal model, while separate formalized lifecycle workflows create and refine BMad artifacts with formalization built in.

This avoids making every workflow independently responsible for model evolution, validation semantics, provenance, stale-state detection, and contradiction handling. The lifecycle workflows remain artifact-oriented and BMad-like; the steward provides the shared formal service behind them.

The architecture has four layers:

1. Lifecycle workflows create familiar BMad artifacts: formal brainstorming, formal PRD, formal architecture, formal epics/stories, formal readiness checks, and formal verification reports.
2. The canonical model steward receives proposed model deltas from those workflows, validates each update, manages provenance, and maintains consistency status.
3. Automated reasoning adapters invoke configured tools against exported views of the canonical model or artifact-specific deltas.
4. Formal companion artifacts expose rigorous English explanations, generated exports, validation results, repair proposals, and provenance links by source artifact.

Every update to the canonical model triggers automatic consistency validation. Explicit checkpoint verification commands remain available for larger lifecycle gates, but they are not the only validation mechanism.

Contradictions block the active artifact workflow until resolved, unless the user explicitly orders continuation. If the user overrides the block, the canonical model is marked inconsistent and the override, contradiction, affected artifacts, and downstream risks are recorded.

Validation outputs include repair proposals. Accepted repairs should update BMad source artifacts directly and update the canonical model accordingly.

Validation strictness increases across the lifecycle. Brainstorming and early PRD work can tolerate provisional uncertainty and competing alternatives. Architecture, epics, stories, readiness checks, and verification reports apply stricter validation to accepted implementation-facing commitments.

### Memory Architecture

Formally BMAD should use a module-owned persistent project model rather than ordinary per-agent conversational memory as its primary state. The canonical representation is a durable project artifact that evolves over time and is stored under a module-owned folder, likely `_bmad/formally-bmad/`.

The canonical representation should be logic-native at the mathematical level. Human-readable summaries, structured interchange files, and tool-specific exports can be generated from it, but the canonical model itself must preserve formal semantics directly.

Recommended project state structure:

```text
_bmad/formally-bmad/
  canonical/
    model/
    ontology/
    temporal/
    meta/
    versions/
    status.md
  artifacts/
    brainstorming/
    prd/
    architecture/
    epics/
    stories/
  exports/
  reports/
  provenance/
  indexes/
  tool-runs/
```

The primary navigation model for formal companions is by source artifact. Shared canonical files, indexes, and global reports still exist, but users should be able to start from a BMad artifact and find its companion formalization, delta, exports, validation result, and provenance.

The model must track assertion states such as `provisional`, `candidate`, `accepted`, `rejected`, `superseded`, `open-question`, and `assumption`. Validation semantics depend on those states: accepted assertions receive full consistency checks; provisional and candidate assertions receive softer compatibility checks; rejected and superseded assertions remain in provenance but are excluded from active reasoning.

### Memory Contract

The steward owns the module state contract.

| File or Folder | Purpose | Read By | Written By |
| -------------- | ------- | ------- | ---------- |
| `canonical/model/` | Logic-native canonical specification model, including FOL-level assertions and active commitments. | Steward, lifecycle workflows, verification workflows, export adapters | Steward |
| `canonical/ontology/` | Description-logic ontology of artifact types, concepts, relationships, roles, and constraints. | Steward, lifecycle workflows, ontology reasoner adapters | Steward |
| `canonical/temporal/` | Temporal properties for lifecycle, ordering, state transitions, workflow gates, and behavior. | Steward, architecture/story/readiness workflows, model checker adapters | Steward |
| `canonical/meta/` | Higher-order or meta-level specifications used only when needed for transformations, refinement, proof obligations, or reusable specification schemas. | Steward, advanced verification workflows | Steward |
| `canonical/versions/` | Versioned snapshots, migrations, and delta history for the evolving canonical model. | Steward, reports, verification workflows | Steward |
| `canonical/status.md` | Current model status: consistent, inconsistent, stale, blocked, overridden, or degraded due to missing tools. | All Formally BMAD skills | Steward |
| `artifacts/<source>/` | Source-artifact formal companions: rigorous English formalization, local delta, local validation result, exports, and provenance links. | Lifecycle workflows, users, reports | Lifecycle workflows and steward |
| `provenance/` | Cross-artifact traceability from source sections to canonical assertions, tool runs, reports, and repairs. | All Formally BMAD skills | Steward |
| `tool-runs/` | Inputs, outputs, logs, and summaries from invoked automated reasoning tools. | Steward, verification reports | Tool adapters and steward |
| `reports/` | Integrated verification and readiness reports with issues, evidence, repairs, and decisions. | Users, lifecycle workflows | Verification workflows |
| `indexes/` | Human-readable and machine-readable indexes for model contents, artifacts, reports, and open issues. | All Formally BMAD skills | Steward |

### Cross-Agent Patterns

The lifecycle workflows are user-facing. They preserve BMad style and ask artifact-oriented questions. When formal ambiguity blocks sound formalization, they ask concise clarification questions tied to the current artifact rather than exposing unnecessary formal-methods detail.

The steward acts as a shared formal service. Workflows hand it proposed canonical deltas; the steward validates the delta, records provenance, updates model status, invokes reasoning tools through adapters, and returns either acceptance, blocking issues, repair proposals, or explicit inconsistency status.

Cross-agent interaction pattern:

1. A lifecycle workflow creates or edits a source artifact.
2. The workflow proposes a formal delta and rigorous English companion text.
3. The steward validates the delta against the current canonical model.
4. If validation passes, the steward commits the delta, updates provenance, and writes formal status back to the source artifact.
5. If validation finds ambiguity or contradiction, the workflow asks the user targeted clarification questions or presents repair proposals.
6. If the user accepts repairs, Formally BMAD edits the affected BMad artifacts and updates the canonical model.
7. If the user explicitly overrides a contradiction, the steward marks the model inconsistent and records the override.

The user remains the final decision-maker for ambiguity resolution, repair acceptance, and contradiction overrides. The module should automate checking and propose repairs, but it should not silently reinterpret project intent.

## Skills

### formally-bmad-setup

**Type:** workflow

**Purpose:** Configure Formally BMAD, initialize durable project state, verify automated reasoning capability, and produce a setup report.

**Capabilities:**

| Capability | Outcome | Inputs | Outputs |
| ---------- | ------- | ------ | ------- |
| Collect configuration | Captures storage paths, validation strictness, repair behavior, tool profile, minimum tool count, fallback policy, and report formats. | User setup answers, project defaults | Module configuration values |
| Initialize project structure | Creates the module-owned folder hierarchy and initial state files. | Project root, configuration | `_bmad/formally-bmad/` structure or configured equivalent |
| Detect BMad artifacts | Finds existing BMad artifact locations for future import or formalized workflows. | Project root, BMad config | Artifact location inventory |
| Detect reasoning tools | Finds supported automated reasoning tools and records versions/capabilities. | Tool profile, local environment | Tool capability inventory |
| Enforce minimum tool availability | Stops setup if no supported automated reasoning tool is available. | Tool detection result, `formally_bmad_min_required_tools` | Success or blocking installation guidance report |
| Run smoke tests | Confirms configured tools can execute simple checks. | Detected tools | Smoke-test results and degraded capability notes |
| Generate setup report | Explains configured paths, enabled checks, missing optional tools, and next steps. | Configuration and detection results | Markdown/HTML setup report |

**Design Notes:** This custom setup skill is required because Formally BMAD cannot be considered installed without at least one executable automated reasoning backend. Export-only behavior is a fallback for optional missing tools, not for a tool-less setup.

**Relationships:** Runs before all other skills. Initializes the state consumed by the steward and lifecycle workflows.

---

### formally-bmad-agent-steward

**Type:** agent

**Persona:** A precise, quiet formal model steward. It communicates in BMad-friendly language when surfaced, explains formal issues without unnecessary jargon, and treats source intent as authoritative. It is rigorous about consistency, provenance, model state, and automated validation.

**Core Outcome:** Maintain the evolving logic-native canonical model, validate every proposed update, preserve provenance, invoke automated reasoning tools, and keep the project formal status trustworthy.

**The Non-Negotiable:** Never silently accept a contradictory or provenance-free canonical model update.

**Capabilities:**

| Capability | Outcome | Inputs | Outputs |
| ---------- | ------- | ------ | ------- |
| Initialize formal project state | Creates the module-owned canonical folders, status files, indexes, provenance ledger, and first model version. | Project root, setup configuration, detected BMad artifact locations | Initialized `_bmad/formally-bmad/` structure, setup/status report |
| Accept canonical deltas | Reviews proposed formal model changes from lifecycle workflows before commit. | Source artifact reference, proposed logic-native delta, rigorous English explanation, assertion states | Accepted delta, rejected delta, or blocking issue list |
| Validate update consistency | Runs automatic consistency checks on each accepted delta using configured automated tools. | Current canonical model, proposed delta, validation strictness, tool profile | Validation result, tool-run records, contradiction/blocker list |
| Manage assertion lifecycle | Tracks assertion states and transitions such as provisional, candidate, accepted, rejected, superseded, open-question, and assumption. | Assertion changes, user decisions, lifecycle stage | Updated canonical model and provenance records |
| Handle contradictions and overrides | Blocks workflows on contradictions unless the user explicitly overrides continuation. | Contradiction report, user resolution or override decision | Resolved model state or inconsistent status with override ledger entry |
| Produce repair proposals | Suggests concrete source-artifact and canonical-model repairs for contradictions, ambiguity, incompleteness, or misalignment. | Validation findings, provenance, affected artifacts | Repair proposal set suitable for Markdown/HTML reports |
| Maintain provenance and status | Keeps traceability from source sections to formal assertions, tool runs, reports, and accepted repairs. | Source references, model deltas, tool outputs, report IDs | Provenance index, model status, artifact formal status blocks |
| Export tool views | Generates tool-specific representations from the canonical model for configured automated reasoning backends. | Canonical model, target backend profile | Export files, execution inputs, degraded-check notes |

**Memory:** Reads all module state under `_bmad/formally-bmad/`, especially canonical, provenance, status, indexes, and tool-runs. Writes canonical model versions, status, provenance, contradiction/override ledger, indexes, and tool-run summaries.

**Init Responsibility:** On first run, verify module structure exists; if not, guide setup. Confirm at least one supported automated reasoning tool is executable before allowing full installation.

**Activation Modes:** Primarily internal/headless, invoked by lifecycle workflows. Direct interactive use should be reserved for maintenance, debugging, forced validation, model-status inspection, contradiction/override review, and advanced troubleshooting.

**Tool Dependencies:** Automated reasoning tool adapters selected later. Must support at least one executable automated reasoning backend. Proof assistants are optional advanced exports only.

**Design Notes:** This is the shared service/agent. Lifecycle workflows should not duplicate stewardship logic. Users should interact with it minimally; the normal experience should be through the artifact lifecycle workflows.

---

### formally-bmad-formal-brainstorming

**Type:** workflow

**Purpose:** Run BMad-style brainstorming while capturing provisional formal concepts, alternatives, assumptions, and open questions in a way that can later be promoted into accepted requirements.

**Capabilities:**

| Capability | Outcome | Inputs | Outputs |
| ---------- | ------- | ------ | ------- |
| Capture exploratory concepts | Preserves raw ideas as provisional formal knowledge without treating them as commitments. | User brainstorming input, existing project context | Brainstorming Markdown, rigorous English exploratory formalization, provisional canonical delta |
| Model alternatives | Represents competing options without producing false contradictions. | Alternative ideas, tradeoffs, exclusions | Candidate assertions, alternative sets, open decision records |
| Promote decisions | Converts converged ideas into accepted or assumption-marked assertions. | User decisions, selected concepts, rejected alternatives | Accepted canonical delta, rejected/superseded provenance |
| Ask formalization clarifications | Surfaces ambiguity only when it blocks useful formal capture. | Ambiguous concept, dependency, or constraint | Concise clarification question and resulting assertion update |
| Create brainstorming companions | Writes companion files organized by source artifact. | Brainstorming artifact path, formalization results | Companion formalization, local validation summary, provenance links |

**Design Notes:** Early validation should be tolerant. Competing alternatives should be modeled as alternatives, not contradictions, until promoted.

**Relationships:** Sends deltas to `formally-bmad-agent-steward`. Feeds PRD formalization with accepted goals, assumptions, open questions, and rejected alternatives.

---

### formally-bmad-formal-prd

**Type:** workflow

**Purpose:** Create or formalize a BMad-style PRD while incrementally updating the canonical model with accepted goals, requirements, constraints, assumptions, and verification obligations.

**Capabilities:**

| Capability | Outcome | Inputs | Outputs |
| ---------- | ------- | ------ | ------- |
| Create formalized PRD | Produces a readable PRD plus formal companions and status block. | Product intent, brainstorming outputs, stakeholder constraints | PRD Markdown, formal status block, rigorous English formalization |
| Extract requirements as assertions | Maps PRD requirements into FOL-oriented accepted or candidate assertions. | PRD sections, requirement statements | Canonical requirement delta, provenance map |
| Detect ambiguity and incompleteness | Finds requirements that cannot be formalized soundly. | Draft PRD, current canonical model | Clarification questions, open-question assertions, blocker list |
| Validate PRD consistency | Checks PRD requirements against accepted canonical assertions and ontology constraints. | Proposed PRD delta, canonical model | Validation result, repair proposals, local report |
| Define readiness obligations | Creates initial verification conditions and formal coverage expectations for downstream architecture/stories. | Accepted PRD requirements | Verification obligation list and coverage baseline |

**Design Notes:** PRD tolerance is moderate: unresolved questions can remain, but accepted requirements must be coherent.

**Relationships:** Uses brainstorming accepted assertions; sends deltas to the steward; feeds architecture and epics/stories workflows.

---

### formally-bmad-formal-architecture

**Type:** workflow

**Purpose:** Create or formalize BMad architecture artifacts with explicit alignment to accepted PRD requirements and formal constraints.

**Capabilities:**

| Capability | Outcome | Inputs | Outputs |
| ---------- | ------- | ------ | ------- |
| Create formalized architecture | Produces BMad-style architecture with formal status and companions. | PRD, constraints, technology choices, current canonical model | Architecture Markdown, rigorous English formalization, canonical delta |
| Formalize architecture decisions | Represents components, interfaces, dependencies, constraints, and invariants. | Architecture decisions and diagrams/text | FOL/DL assertions, temporal properties where relevant |
| Check PRD alignment | Validates that architecture decisions satisfy, refine, or explicitly constrain accepted requirements. | Architecture delta, PRD assertions, verification obligations | Alignment report, contradictions, repair proposals |
| Model lifecycle/behavior | Captures state, ordering, workflow, and temporal properties when architecture implies behavior. | Architecture flows, stateful components, process rules | Temporal logic companion assertions and exports |
| Tighten implementation constraints | Converts architecture commitments into downstream constraints for epics and stories. | Accepted architecture assertions | Story/epic constraint set and provenance links |

**Design Notes:** Architecture validation should be stricter than PRD validation because it starts constraining implementation.

**Relationships:** Consumes accepted PRD assertions; sends deltas to the steward; supplies constraints for epics/stories and readiness checks.

---

### formally-bmad-formal-epics

**Type:** workflow

**Purpose:** Create or formalize epics as implementation planning structures with formal traceability to PRD requirements, architecture constraints, assumptions, and verification obligations.

**Capabilities:**

| Capability | Outcome | Inputs | Outputs |
| ---------- | ------- | ------ | ------- |
| Create formalized epics | Groups implementation work while preserving requirement and architecture traceability. | PRD, architecture, current canonical model | Epic Markdown, formal companions, canonical epic assertions |
| Map requirements to epics | Ensures accepted PRD requirements are covered by one or more epics or intentionally deferred. | Accepted PRD assertions, architecture constraints | Requirement-to-epic coverage map, gaps, repair proposals |
| Check epic coherence | Validates that each epic has a coherent purpose, scope, dependencies, and formal relation to architecture constraints. | Epic draft, canonical model | Epic validation result, blockers, repair proposals |
| Define story obligations | Derives story-level obligations, constraints, and coverage expectations from each epic. | Epic assertions, PRD obligations, architecture constraints | Story obligation set and provenance links |
| Track epic readiness | Marks whether an epic is ready to be decomposed into stories. | Epic assertions, validation results, coverage map | Epic readiness status and local report |

**Design Notes:** Epic validation is stricter than architecture planning but less granular than story readiness. Epics should expose coverage gaps before story writing begins.

**Relationships:** Consumes PRD and architecture model state; sends deltas to the steward; feeds formal story creation and readiness reports.

---

### formally-bmad-formal-stories

**Type:** workflow

**Purpose:** Create or formalize implementation stories with formal acceptance criteria, traceability, consistency checks, and readiness status.

**Capabilities:**

| Capability | Outcome | Inputs | Outputs |
| ---------- | ------- | ------ | ------- |
| Create formalized stories | Produces story files with acceptance criteria that are formally grounded and checkable. | Epic context, target requirement, architecture constraints | Story Markdown, formal status block, story formalization |
| Formalize acceptance criteria | Converts acceptance criteria into checkable assertions and verification conditions. | Story acceptance criteria | Formal criteria delta, coverage links |
| Check story alignment | Validates story consistency with PRD, architecture, assumptions, epics, and prior stories. | Story delta, canonical model | Alignment result, blockers, repair proposals |
| Detect implementation blockers | Finds contradictions, missing formal coverage, unresolved assumptions, or stale source dependencies that block implementation. | Story formalization, current model status | Blocking issue list, repair proposals, readiness status |
| Track story readiness | Marks whether a story has sufficient formal coverage and no unresolved blocking contradictions. | Story assertions, tool results, open issues | Story readiness status and local report |

**Design Notes:** Story validation should be strict for accepted implementation commitments. A story should not be ready if accepted requirements lack formal coverage or if blocking contradictions remain.

**Relationships:** Consumes PRD, architecture, and epic model state; sends deltas to the steward; feeds readiness and verification reports.

---

### formally-bmad-formal-import

**Type:** workflow

**Purpose:** Formalize existing BMad Markdown artifacts into the Formally BMAD canonical model, creating source-artifact companions, provenance links, ambiguity records, and initial validation results.

**Capabilities:**

| Capability | Outcome | Inputs | Outputs |
| ---------- | ------- | ------ | ------- |
| Discover existing artifacts | Finds BMad artifacts that can be imported into the formal model. | Project root, configured artifact paths | Artifact inventory and classification |
| Classify artifact types | Determines whether each artifact is brainstorming, PRD, architecture, epic, story, readiness report, verification report, or unsupported content. | Artifact inventory, file contents | Classified import plan |
| Extract candidate assertions | Converts existing Markdown content into candidate formal assertions without overcommitting ambiguous text. | Source artifact sections | Candidate canonical deltas, ambiguity list |
| Create formal companions | Writes rigorous English formalizations and local validation summaries by source artifact. | Source artifact, extracted assertions, steward feedback | Companion folder contents and status block suggestions |
| Build provenance links | Maps source sections to formal assertions, assumptions, open questions, and skipped content. | Source artifact structure, candidate deltas | Provenance records and missing-link findings |
| Submit import deltas | Sends candidate deltas to the steward for validation before commit. | Candidate deltas, assertion states, import scope | Accepted/rejected deltas, blockers, repair proposals |
| Produce import report | Summarizes what was imported, skipped, blocked, contradicted, or left ambiguous. | Import run results, tool outputs, steward status | Markdown/HTML import report |

**Design Notes:** Import is intentionally separate from verification. It builds or extends the formal model from existing artifacts; verification judges the resulting model and lifecycle readiness.

**Relationships:** Uses the steward for validation and provenance commits. Feeds verification with an initial model, import report, and unresolved ambiguity list.

---

### formally-bmad-ontology-alignment

**Type:** workflow

**Purpose:** Discover relevant external ontology concepts, compare them with project concepts, propose controlled mappings/imports, and submit validated ontology deltas to the steward.

**Capabilities:**

| Capability | Outcome | Inputs | Outputs |
| ---------- | ------- | ------ | ------- |
| Search ontology repositories | Finds candidate concepts in configured open ontology repositories. | Project concept, artifact context, configured repositories | Candidate ontology concepts with source, URI, version, and license/status |
| Recommend ontology terms | Ranks external concepts by semantic fit and project relevance. | Candidate concepts, local canonical ontology, source artifact context | Ranked recommendation list with rationale |
| Compare concept meaning | Assesses whether an external term matches, broadens, narrows, overlaps, or conflicts with a project concept. | Project concept definition, external concept definition and axioms | Mapping proposal: exact, broader, narrower, related, conflict, or no match |
| Propose controlled imports | Prepares ontology deltas without silently accepting external commitments. | Approved candidate mappings, source ontology metadata | Candidate/provisional ontology delta with provenance |
| Validate imported commitments | Checks external ontology commitments against the current canonical model. | Ontology delta, canonical model, steward validation result | Accepted delta, blockers, semantic conflicts, repair proposals |
| Generate alignment reports | Explains candidate terms, mapping rationale, conflicts, accepted imports, and rejected options. | Search results, mapping decisions, validation findings | Markdown/HTML ontology alignment report |
| Maintain external provenance | Records source repository, ontology URI, term URI, version/date, license/status, mapping rationale, and user decision. | Accepted/rejected mappings | External ontology provenance records |

**Design Notes:** This workflow is ontology discovery, alignment, and controlled import, not unrestricted ontology generation. External concepts should enter as candidate or provisional until explicitly accepted by the user and validated by the steward.

**Relationships:** Uses the steward for ontology delta validation and provenance commits. Supports PRD, architecture, epics, stories, import, and verification by grounding project concepts in external ontologies where useful.

---

### formally-bmad-formal-verification

**Type:** workflow

**Purpose:** Run checkpoint verification, readiness checks, traceability audits, consistency reports, and repair review reports over the evolving canonical model and its source artifacts.

**Capabilities:**

| Capability | Outcome | Inputs | Outputs |
| ---------- | ------- | ------ | ------- |
| Run checkpoint verification | Validates the current canonical model and selected artifact scope on demand. | Scope, canonical model, tool profile | Markdown/HTML verification report, tool-run records |
| Check implementation readiness | Determines whether artifacts are consistent, aligned, and sufficiently formally covered. | PRD, architecture, epics/stories, canonical model | Readiness report with pass/fail, coverage thresholds, blockers |
| Audit traceability | Shows links from source text to assertions, verification conditions, tool runs, and repairs. | Artifact scope, provenance index | Traceability audit report and missing-link findings |
| Analyze contradictions | Explains contradictions with affected artifacts, formal assertions, counterexamples if available, and repair options. | Inconsistent model state, tool outputs | Contradiction report, repair proposals, override implications |
| Review formal coverage | Measures whether accepted requirements and implementation commitments have formal assertions and verification conditions. | Canonical model, source artifacts | Coverage report, gaps, recommended repairs |
| Generate repair review | Presents proposed source edits and model changes for user decision. | Repair proposals, affected files | Markdown/HTML repair review, accepted/rejected decision records |

**Design Notes:** This workflow is report-oriented. HTML output is especially useful here because verification evidence, traceability, coverage, and repairs need scanning and auditability.

**Relationships:** Uses the steward for current model status and tool execution; may trigger accepted repairs that edit BMad artifacts and update canonical state.

---

## Configuration

The setup skill should collect enough configuration to initialize durable module state and invoke automated reasoning tools. Every configuration value must have a sensible default, but setup must not complete unless at least one supported automated reasoning tool is available and passes the minimum capability check.

| Variable | Prompt | Default | Result Template | User Setting |
| -------- | ------ | ------- | --------------- | ------------ |
| `formally_bmad_project_root` | Where should Formally BMAD store its project-level formal model and reports? | `{project-root}/_bmad/formally-bmad` | `formally_bmad_project_root: "{answer}"` | Yes |
| `formally_bmad_canonical_model_path` | Where should the logic-native canonical model live? | `{formally_bmad_project_root}/canonical` | `formally_bmad_canonical_model_path: "{answer}"` | Yes |
| `formally_bmad_validation_strictness` | What default validation strictness should be used? | `stage-aware` | `formally_bmad_validation_strictness: "{answer}"` | Yes |
| `formally_bmad_auto_apply_repairs` | Should accepted repair proposals edit BMad source artifacts directly? | `confirm-before-edit` | `formally_bmad_auto_apply_repairs: "{answer}"` | Yes |
| `formally_bmad_tool_profile` | Which automated reasoning tool profile should be used? | `auto-detect` | `formally_bmad_tool_profile: "{answer}"` | Yes |
| `formally_bmad_min_required_tools` | What is the minimum number of supported automated reasoning tools required for setup to proceed? | `1` | `formally_bmad_min_required_tools: {answer}` | Yes |
| `formally_bmad_export_only_fallback` | If an optional reasoning backend is missing after at least one supported tool is available, should the module generate exports and mark those specific checks as degraded? | `true` | `formally_bmad_export_only_fallback: {answer}` | Yes |
| `formally_bmad_report_format` | Which report formats should verification and readiness reports produce? | `markdown,html` | `formally_bmad_report_format: "{answer}"` | Yes |

## External Dependencies

The module depends on automated reasoning tools, but exact ecosystems will be chosen later. Setup should therefore support tool profiles rather than hard-coding one prover stack.

Preferred dependency families:

- Description logic / ontology reasoners for ontology consistency, classification, and concept/property constraints.
- First-order automated theorem provers and model finders for core specification consistency and counterexample discovery.
- SMT solvers for decidable fragments, bounded checks, arithmetic/data constraints, and practical automation.
- Temporal model checkers or temporal logic tooling for lifecycle, workflow, state, ordering, and behavioral properties.
- Export adapters for standards such as OWL/DL, TPTP, SMT-LIB, TLA+/PlusCal-style views, Alloy-style models, or other selected targets.

Proof assistants should not be required dependencies. Exports to proof assistants may be advanced optional targets only when automated checking is insufficient or explicitly requested.

Setup responsibilities:

- Detect installed reasoning tools for the selected profile.
- Require at least one supported automated reasoning tool before setup can proceed.
- Record tool versions and capabilities.
- Run a smoke test for each configured tool.
- Create export-only fallbacks only for missing optional backends after the minimum required tool availability has been satisfied.
- Mark validation as `degraded` when an optional or expected check could not be executed, but do not allow setup to complete with zero executable automated reasoning capability.
- Store tool run inputs, outputs, logs, and summaries under `tool-runs/`.

## UI and Visualization

The module does not need a full bespoke web application for the first version. It should produce high-quality Markdown and HTML reports with enough structure to support review, audit, and decision-making.

Recommended visual/reporting outputs:

- Formal status blocks embedded in BMad source artifacts.
- Source-artifact companion folders with local validation summaries.
- Integrated readiness and verification reports in Markdown and HTML.
- Traceability tables linking source artifact sections, canonical assertions, tool checks, issue IDs, and repair proposals.
- Consistency status dashboard as a generated report, not a live app initially.
- Model coverage summaries showing which accepted requirements, architecture decisions, epics, and stories have formal assertions and verification conditions.
- Contradiction and override ledger showing unresolved contradictions, explicit user overrides, affected artifacts, and downstream risks.

HTML reports are especially valuable for readiness checks, verification runs, contradiction analysis, traceability audits, coverage reports, and repair proposal reviews.

## Setup Extensions

The setup skill should do more than collect config. It should initialize the module's durable project structure and verify that the formalization environment is usable.

Setup extensions:

- Create `_bmad/formally-bmad/` or the configured project root.
- Create canonical, artifact, report, provenance, index, export, and tool-run folders.
- Initialize `canonical/status.md`.
- Initialize model version metadata.
- Create a first provenance index.
- Create an empty contradiction/override ledger.
- Detect supported BMad artifact locations in the project.
- Detect configured automated reasoning tools and record versions.
- Run tool smoke tests where possible.
- Stop setup with a clear installation guidance report if no supported automated reasoning tool is available.
- Generate a setup report summarizing active capabilities, degraded checks, missing tools, and next recommended configuration steps.

## Integration

Formally BMAD is an expansion of the BMad ecosystem, but it should provide independent value when run over existing Markdown artifacts.

It provides its own formalized lifecycle workflows rather than only wrapping existing BMad skills. Existing BMad artifacts can still be imported, formalized, checked, and repaired.

Integration principles:

- Preserve BMad-style artifact authoring and user interaction.
- Keep main artifacts readable Markdown.
- Add formal status blocks and companion artifacts.
- Edit BMad source artifacts when accepted repairs require it.
- Maintain traceability from informal artifact text to canonical formal assertions and verification reports.
- Allow explicit checkpoint verification commands at lifecycle gates.
- Automatically validate every canonical model update.

## Creative Use Cases

- Convert an existing BMad PRD and architecture into an evolving formal model, then identify contradictions before stories are written.
- Use brainstorming alternatives as provisional assertions, then promote selected decisions into accepted requirements with provenance.
- Run a readiness gate that proves every accepted requirement has formal coverage, source provenance, and at least one verification condition.
- Generate an HTML verification report that shows contradictions, counterexamples, repair proposals, and source edits needed to restore consistency.
- Compare two architecture alternatives by checking which one satisfies more accepted requirements under the current canonical model.
- Audit a story for implementation readiness by checking alignment with PRD goals, architecture constraints, accepted assumptions, and unresolved contradictions.
- Maintain a contradiction/override ledger for projects where the user intentionally continues despite known inconsistency.

## Ideas Captured

- Initial spark: a BMad extension for formal specifications and ontologies over BMad artifacts.
- Artifact coverage should include brainstorming, PRD, architecture, epics, stories, implementation readiness checks, and verification reports. UX specification has been explicitly dropped from scope.
- The module should help turn natural-language BMad outputs into formalized, queryable, checkable artifacts.
- Module identity: "Formally BMAD" with module code `formally-bmad`.
- The existing one-line description is accepted as-is: "Extends BMad artifacts with formal specifications, ontologies, traceability, readiness checks, and verification reports."
- Ontology modeling and machine-checkable formal specification are equally important pillars, not one primary and one supporting.
- Formal targets should use standard representations, including semantic web and formal methods families such as RDF, OWL, SHACL, SPARQL, JSON/YAML schema forms, Alloy, TLA+, Coq, Lean, or comparable standards where appropriate.
- Formal artifacts must also include a human-readable explanation written in structured, rigorous English. The explanation should be precise enough for review and traceability, while remaining readable to BMad users who are not experts in a specific formal language.
- The module should likely produce paired outputs: canonical machine-readable specifications and companion English explanations. The English should explain concepts, predicates, constraints, invariants, mappings, assumptions, verification status, and unresolved ambiguities.
- User refined the formal target strategy: the module should primarily target logic families rather than concrete tool syntaxes. First-order logic, temporal logic, and higher-order logic are the main families due to generality and representability in automated reasoning tools. Ontology representation should target description logics because they are a subset/fragment of first-order logic and can facilitate unified reasoning.
- A canonical intermediate representation is mandatory. During BMad ideation and specification phases, the module will need to call formal analysis and verification tools for consistency and alignment checks. Different tools may require different concrete logic families or concrete syntaxes, so the module must preserve a stable canonical representation that can be transformed into tool-specific targets.
- Automated checking is the priority. The module should prefer decidable or practically checkable fragments when possible, even if that constrains expressiveness. Expressive targets remain useful, but they should not undermine routine automated validation.
- Proof assistants should be avoided as primary targets where possible. Ecosystem choices will be defined later, with emphasis on automated provers, model finders, SMT solvers, temporal model checkers, ontology reasoners, and similar automated tools. Proof-assistant exports may exist only as advanced or fallback targets.
- Recommended framing to revisit in architecture: logic-family canonical model first, concrete verifier/export backends second. Concrete standards and tools should be viewed as serialization/execution targets, not the top-level ontology of the module.
- The canonical intermediate representation should be a durable project artifact that evolves over time, not a temporary output regenerated from scratch for every check. This implies first-class support for synchronization with source BMad documents, provenance links, versioning/migration, stale-state detection, and controlled updates as artifacts change.
- Likely storage convention to revisit later: `_bmad/formally-bmad/` or another module-owned project folder containing the canonical model, generated exports, verification reports, provenance indexes, and synchronization metadata.
- Formalization should happen incrementally as BMad artifacts are created and refined. Explicit checkpoint commands such as "formalize PRD", "verify architecture", or "check story readiness" should still exist, but they operate on top of an evolving canonical model rather than being the only way the model is built.
- Incremental operation implies stage-specific formalization hooks for brainstorming, PRD, UX, architecture, epics, stories, readiness checks, and verification reports. Each stage should add, revise, or deprecate canonical assertions with provenance instead of overwriting the whole model.
- Checkpoint verification should be available through explicit user commands, but every update to the evolving canonical model must also trigger automatic consistency validation for that update. The module should not wait for a checkpoint to detect contradictions introduced by new formal assertions.
- Artifact creation should use active formalization-in-the-loop. When ambiguity blocks sound formalization, the module should ask clarifying questions during artifact creation rather than silently guessing or deferring all issues to later validation.
- Ambiguity handling should distinguish between tolerable underspecification, explicit assumptions, formalization blockers, and contradictions. Blockers should be surfaced as concise clarification questions tied to the affected source artifact and canonical assertion.
- User agrees with a dedicated canonical model steward agent/capability. This steward should own canonical model evolution, update validation, provenance integrity, stale-state detection, contradiction handling, and model consistency status.
- Contradiction policy: if automatic validation finds a contradiction, the module should block the artifact workflow until the contradiction is solved or the user explicitly orders continuation. If the user overrides the block, the canonical model must be marked inconsistent, with the contradiction, override decision, affected artifacts, and downstream risk recorded.
- Inconsistency must be a deliberate project state. The module should not silently continue with an inconsistent canonical model, and later verification reports should surface that status prominently.
- The module should provide its own formalized versions of BMad artifact workflows rather than merely integrating as an external check layer over existing BMad skills. Examples include "create PRD with formalization", "create architecture with formalization", "create epics/stories with formalization", and "run readiness check with formal verification".
- Existing BMad workflows may remain sources or references, but Formally BMAD should feel like a parallel formalized BMad path where canonical model updates and validation are built into artifact creation.
- The canonical model steward should not replace the formalized artifact workflows. It should act as a shared service/agent that the workflows use for canonical model updates, delta validation, ambiguity resolution, provenance recording, and consistency status.
- User-facing style should preserve the BMad experience. The module should feel like BMad with stricter formal backing, not like a formal methods tool that exposes excessive logic terminology during normal use. Formal details should be available in reports and exports, while interaction remains accessible and artifact-oriented.
- Artifact strategy: preserve familiar BMad-style Markdown artifacts and generate formal companion artifacts rather than merging everything into large combined documents. Main artifacts should include a concise formal status block with canonical model version, consistency status, last formalization timestamp, open ambiguities/blockers, and links to companion formal artifacts or reports.
- Formal companions should contain rigorous English formalizations, canonical model deltas, exported logic/tool files, validation reports, and provenance maps. These companions may live beside the source artifact or under a module-owned folder, to be decided later.
- Formal companions should be organized primarily by source artifact, not primarily by formal concern. This keeps companion materials discoverable from the BMad artifact they explain or validate. Shared/global canonical files, indexes, and reports may still exist, but source-artifact folders are the main navigation structure.
- Possible structure to revisit: `_bmad/formally-bmad/artifacts/prd/`, `_bmad/formally-bmad/artifacts/architecture/`, `_bmad/formally-bmad/artifacts/epics/`, `_bmad/formally-bmad/artifacts/stories/story-1.1/`, plus shared canonical/provenance indexes.
- Verification reports are the main exception: they may be integrated documents combining human explanation, formal claims, evidence, validation results, tool outputs, and recommended resolutions.
- Brainstorming formalization should use two layers: exploratory capture and committed decisions. Exploratory capture preserves uncertainty, alternatives, open questions, assumptions, candidate concepts, and tentative relationships as provisional knowledge. Committed decisions promote selected concepts, constraints, goals, and exclusions into stable canonical assertions once ideation converges.
- The canonical representation should support assertion states such as `provisional`, `candidate`, `accepted`, `rejected`, `superseded`, `open-question`, and `assumption`.
- Validation semantics should depend on assertion state. Full consistency checks apply to accepted assertions. Softer compatibility checks apply to candidate/provisional assertions. Rejected and superseded assertions remain in provenance but are excluded from active reasoning. Open questions become formalization blockers only when downstream artifacts depend on them.
- The purpose of early brainstorming formalization is traceability without brittleness: preserve the origin of later requirements while avoiding false contradictions among competing alternatives.
- Automated validation should include repair proposals, not only pass/fail status or issue lists. When validation finds contradictions, ambiguity, incompleteness, or misalignment, reports should propose concrete repairs such as editing a source requirement, splitting a concept, marking a claim as an assumption, resolving an alternative, weakening/strengthening a constraint, or updating canonical assertions.
- Repair proposals should be traceable to affected source artifacts and canonical assertions, and should explain expected consequences/tradeoffs. User acceptance of repairs should update both the source artifact and the canonical model where appropriate.
- Accepted repair proposals should edit the source BMad artifacts directly. The module should still make the proposed change explicit before applying it, but the intended repair path is not merely advisory.
- Validation strictness should vary by lifecycle stage. Early stages such as brainstorming and PRD can tolerate more provisional inconsistency or unresolved alternatives. Later stages such as architecture, epics, stories, readiness checks, and verification reports should become progressively stricter, especially for accepted assertions and implementation-facing commitments.
- The canonical representation should be logic-native at the mathematical level, not primarily YAML/JSON/TOML. Human-readable and machine-interchange formats may be generated around it, but the canonical representation should preserve formal semantics directly.
- The module should directly invoke configured automated reasoning and verification tools, not only generate exports and instructions. Export-only behavior may remain a fallback when tools are unavailable.
- Implementation readiness should include formal coverage thresholds, not only consistency/alignment. For example, every accepted requirement should have formal assertions, provenance, and relevant verification conditions before it is considered ready.
- It should likely preserve traceability from early ideation through verification, so every downstream claim can point back to upstream intent and constraints.
- It should probably support both ontology modeling and formal specification extraction, because the user named both domains explicitly.
- Verification reports are a first-class output, not just internal validation logs.
- Readiness checks are included in scope, which suggests the module should assess whether artifacts are sufficiently complete, consistent, and formally grounded before implementation.
- This appears to be an extension to the BMad ecosystem rather than a standalone non-BMad product, but it should still provide independent value when run against existing markdown artifacts.

## Build Roadmap

Recommended build order:

1. **formally-bmad-setup**
   - Build first because all other skills depend on the module-owned folder structure, configuration contract, tool-detection policy, and minimum automated reasoning capability.
   - Must enforce that setup stops if no supported automated reasoning tool is available.

2. **formally-bmad-agent-steward**
   - Build second because all lifecycle workflows depend on canonical model updates, validation, provenance, status, contradiction handling, and tool invocation.
   - Should support mostly internal/headless use, with limited direct interaction for maintenance and debugging.

3. **formally-bmad-formal-import**
   - Build early so existing BMad artifacts can seed the canonical model and validate the setup/steward contract against real documents.
   - Useful for testing provenance, ambiguity handling, companion creation, and validation results before new formalized workflows are built.

4. **formally-bmad-ontology-alignment**
   - Build before the full lifecycle workflows so project concepts can be grounded in external ontologies when useful.
   - Must support controlled imports, mapping rationale, repository provenance, license/status capture, and steward validation.

5. **formally-bmad-formal-brainstorming**
   - Build next to support the beginning of the formalized lifecycle.
   - Establishes provisional/candidate/accepted assertion handling and alternative modeling.

6. **formally-bmad-formal-prd**
   - Builds on brainstorming outputs and creates the central requirement layer of the canonical model.
   - Introduces formal coverage expectations and verification obligations.

7. **formally-bmad-formal-architecture**
   - Builds on accepted PRD assertions and validates architecture decisions against requirements and constraints.
   - Introduces temporal properties and stricter implementation-facing constraints.

8. **formally-bmad-formal-epics**
   - Maps accepted requirements and architecture constraints into implementation planning groups.
   - Checks epic coherence and requirement coverage before story decomposition.

9. **formally-bmad-formal-stories**
   - Builds on epics to create strict implementation-facing story formalizations and readiness statuses.
   - Formalizes acceptance criteria and story-level verification conditions.

10. **formally-bmad-formal-verification**
   - Build after the main artifact workflows so reports can consume realistic model state, provenance, tool runs, readiness data, and repair proposals.
   - Produces checkpoint verification, readiness reports, traceability audits, contradiction analysis, coverage reports, and repair reviews.

This order reduces risk by establishing setup, persistence, validation, and import before building the full formalized artifact lifecycle.

**Next steps:**

1. Build each skill using **Build an Agent (BA)** or **Build a Workflow (BW)** — share this plan document as context
2. When all skills are built, return to **Create Module (CM)** to scaffold the module infrastructure
