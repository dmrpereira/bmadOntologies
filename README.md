# Formally BMAD MVP

This repository contains an MVP Formally BMAD module: a BMad extension for turning product and delivery artifacts into a formalized, traceable, verification-oriented project model.

The current module is ready to use for a simple project workflow. It supports:

- setup and tool detection
- formal brainstorming and import
- PRD, architecture, epics, and stories with formal companions
- language-aware code contract derivation for Python, C, and Rust
- contract-bearing stub generation for review before implementation
- implementation verification against generated contracts
- checkpoint verification, readiness review, contradiction analysis, and traceability review

## What This MVP Covers

The current module is designed for a practical first adoption, not full formal-methods automation.

It already gives you:

- a setup workflow with enforced validation baseline
- a canonical project structure under `_bmad/formally-bmad`
- a formal artifact flow from idea to stories
- a contract refinement flow from accepted obligations into code-level contracts
- a review gate that turns accepted contracts into code skeletons before full generation
- explicit verification routing for the currently supported toolchain
- clear degraded-check behavior when a backend is missing

It does not yet give you:

- full automatic end-to-end solver orchestration for every workflow
- permanent system installation for every optional tool
- mature multi-backend cross-checking by default

## Installation Model

This repository is the module source bundle. It is not a standalone executable installer.

Formally BMAD is packaged as a set of BMad skill folders under [skills](/Users/dmrpereira/Propostas/bmadOntologies/skills:1). To use it in another project, you install those skill folders into the skill location used by that target project and then run the setup skill from inside the target project.

You do not need a special archive format. A ZIP file is only a transport mechanism. You can:

- clone this repository and copy the skill folders
- download a ZIP and uncompress it, then copy the skill folders
- copy the `skills/` subtree directly from a local checkout

The important point is not the transport format. The important point is that the target project ends up with the Formally BMAD skill directories installed in its active BMad skill location.

## Prerequisite: BMad Must Already Exist In The Target Project

Yes, the target project must already have BMad installed before you install Formally BMAD.

Why:

- `formally-bmad-setup` writes into `{project-root}/_bmad/config.yaml`
- it merges entries into `{project-root}/_bmad/module-help.csv`
- it assumes the target project already has a working `_bmad/` structure
- cleanup logic assumes skills are installed in `.claude/skills/` or an equivalent active skills location

Formally BMAD does not currently bootstrap core BMad into an empty non-BMad folder. It is a BMad module, not a replacement for the core BMad installation.

Before installing Formally BMAD into a target project, verify that the target project already has:

- an `_bmad/` directory
- core BMad config files or the normal BMad project structure
- an active BMad skill installation location, commonly `.claude/skills/` or equivalent

## How To Start A BMad Project Before Installing Formally BMAD

To create a fresh local BMad project in a target folder, run one of:

```bash
npx bmad-method install
```

or:

```bash
npx bmad-method@next install
```

Run that command from inside the target project folder where you want BMad installed.

After that, the correct sequence is:

1. create or choose a normal project folder
2. run `npx bmad-method install` or `npx bmad-method@next install` in that folder
3. verify that the folder is now a real BMad project
4. install the Formally BMAD skills into that BMad project

### Minimum Checklist For “This Is A BMad Project”

Treat a target folder as ready for Formally BMAD only if all of these are true:

- the folder contains `_bmad/`
- the folder contains BMad config state such as `_bmad/config.yaml` or the normal BMad project structure
- the folder has access to the installed BMad skills, commonly under `.claude/skills/`
- the BMad runtime can already resolve normal core skills before Formally BMAD is added

If those conditions are not true yet, you do not have a usable BMad project for this module.

### Practical Start-From-Scratch Flow

If you are starting from a completely empty project:

1. make the project folder
2. run `npx bmad-method install` or `npx bmad-method@next install`
3. confirm the BMad project structure exists
4. confirm the active BMad skills location exists
5. copy the Formally BMAD skill directories from this repository's `skills/` folder into the target folder's `.claude/skills/` directory
6. run `formally-bmad-setup`

### What This README Can And Cannot Tell You

This README can tell you how Formally BMAD is installed into a BMad project.

It cannot give you the authoritative core-BMad bootstrap command unless that command is documented by the BMad distribution you are using. Different BMad environments may install core skills differently, but for Formally BMAD the required end state is always the same:

- `_bmad/` exists
- core BMad is already working
- the active BMad skills location exists
- Formally BMAD skills are copied into that location

## What To Copy Into A Target Project

Install these skill directories from [skills](/Users/dmrpereira/Propostas/bmadOntologies/skills:1):

- `formally-bmad-setup`
- `formally-bmad-agent-steward`
- `formally-bmad-formal-brainstorming`
- `formally-bmad-formal-import`
- `formally-bmad-ontology-alignment`
- `formally-bmad-formal-prd`
- `formally-bmad-formal-architecture`
- `formally-bmad-formal-epics`
- `formally-bmad-formal-stories`
- `formally-bmad-formal-contracts`
- `formally-bmad-contract-stubs`
- `formally-bmad-code-verification`
- `formally-bmad-formal-verification`

Do not copy `skills/reports/`. That folder is project documentation for this module repository, not a runtime dependency of the target project.

## Where To Copy The Skills

Copy the directories above into the active BMad skills location used by the target project.

In the current module scripts, the assumed installed location is:

```text
{project-root}/.claude/skills/
```

The cleanup safety logic explicitly refers to `.claude/skills/` as the installed location. If your BMad environment uses a different active skill path, use that equivalent location instead, but the skills must be installed where your agent runtime will actually discover them.

## Installation Steps For A New Target Project

Use this sequence:

1. Start with a project that already has BMad installed.
2. Copy these directories from this repository's `skills/` folder:
   - `skills/formally-bmad-setup`
   - `skills/formally-bmad-agent-steward`
   - `skills/formally-bmad-formal-brainstorming`
   - `skills/formally-bmad-formal-import`
   - `skills/formally-bmad-ontology-alignment`
   - `skills/formally-bmad-formal-prd`
   - `skills/formally-bmad-formal-architecture`
   - `skills/formally-bmad-formal-epics`
   - `skills/formally-bmad-formal-stories`
   - `skills/formally-bmad-formal-contracts`
   - `skills/formally-bmad-contract-stubs`
   - `skills/formally-bmad-code-verification`
   - `skills/formally-bmad-formal-verification`
3. Copy them into the target project's active BMad skills location:

```text
<target-project>/.claude/skills/
```

Each copied directory should land directly under `.claude/skills/`, for example:

```text
<target-project>/.claude/skills/formally-bmad-setup
<target-project>/.claude/skills/formally-bmad-agent-steward
<target-project>/.claude/skills/formally-bmad-formal-contracts
<target-project>/.claude/skills/formally-bmad-contract-stubs
<target-project>/.claude/skills/formally-bmad-formal-verification
```

Do not create an extra nesting layer such as:

```text
<target-project>/.claude/skills/skills/formally-bmad-setup
```

That layout is wrong.
4. Open the target project root, not this repository root.
5. Run `formally-bmad-setup` inside the target project.
6. Confirm that setup creates and updates:
   - `{project-root}/_bmad/config.yaml`
   - `{project-root}/_bmad/config.user.yaml`
   - `{project-root}/_bmad/module-help.csv`
   - `{project-root}/_bmad/formally-bmad/`
7. Only after setup succeeds, begin the formal workflow.

## Minimal Example Install Procedure

If you already have a BMad-enabled target project and want the simplest install path:

1. clone or download this repository
2. from this repository, copy these directories:
   - `skills/formally-bmad-setup`
   - `skills/formally-bmad-agent-steward`
   - `skills/formally-bmad-formal-brainstorming`
   - `skills/formally-bmad-formal-import`
   - `skills/formally-bmad-ontology-alignment`
   - `skills/formally-bmad-formal-prd`
   - `skills/formally-bmad-formal-architecture`
   - `skills/formally-bmad-formal-epics`
   - `skills/formally-bmad-formal-stories`
   - `skills/formally-bmad-formal-contracts`
   - `skills/formally-bmad-contract-stubs`
   - `skills/formally-bmad-code-verification`
   - `skills/formally-bmad-formal-verification`
3. copy them into:

```text
<target-project>/.claude/skills/
```

4. in the target project, run:

```text
formally-bmad-setup
```

That is the install procedure for the MVP.

## Current Tooling Model

### Baseline Validation Gate

Setup requires:

- at least one SMT solver
- at least one first-order or SAT solver

In practice, the current environment already supports this baseline with:

- `z3`
- `vampire`
- `eprover`
- `kissat`

### Additional Supported Tools

The module can also detect and report:

- proof assistants: `rocq`, `coqc`, `lean`, `lake`, `isabelle`
- temporal satisfiability tooling: `black`
- ontology tooling: `robot`
- temporal/model-checking tooling: `tlc`, `apalache`, `alloy`
- Python contract verification tooling: `crosshair`
- C contract verification tooling: `frama-c`, `cbmc`
- Rust contract verification tooling: `cargo-kani`, `prusti-rustc`, `cargo-creusot`
- additional ontology reasoners: `hermit`, `elk`, `jfact`, `factplusplus`, `pellet`

### Important Environment Note

Some tools are currently installed session-locally rather than globally:

- `black`: `/private/tmp/black-install/bin/black`
- `robot`: `/private/tmp/robot/bin/robot`

The setup helper already knows to search those directories. If you move to another machine or a new environment, either reinstall those tools or provide extra tool directories through:

```bash
FORMALLY_BMAD_EXTRA_TOOL_DIRS=/path/to/tools1:/path/to/tools2
```

## How Verification Currently Uses Tools

The MVP verification workflow routes checks conservatively by logic family:

- SMT obligations: `z3`, then `cvc5`, then `cvc4`
- first-order obligations: `vampire`, then `eprover`, then `prover9`
- finite countermodel attempts: `mace4`
- SAT-oriented reductions: `kissat`, then `cadical`, then `minisat`, then `glucose`
- temporal satisfiability and finite-trace consistency: `black`
- executable temporal/state-model views: `tlc`, then `apalache`, then `alloy`
- ontology validation and export: `robot`, then `hermit`, `elk`, `jfact`, `factplusplus`, `pellet`

Proof assistants are support-only in the MVP. They are informative, but they are not the primary validation backend.

For implementation-facing verification, the current MVP also supports this contract/tool split:

- Python contracts: prefer `deal` or `icontract` style notation, with `crosshair` as the primary executable verifier
- C contracts: prefer `ACSL`, with `frama-c` or `cbmc` as executable verification backends
- Rust contracts: prefer Kani-oriented assertions or proof harnesses, or Prusti/Creusot style specifications, with `cargo-kani`, `prusti-rustc`, or `cargo-creusot` as backends

## Recommended Starting Workflow

For a new simple project, use this sequence:

1. Run `formally-bmad-setup`
2. Start with either:
   - `formally-bmad-formal-brainstorming` for a greenfield idea
   - `formally-bmad-formal-import` if you already have BMad artifacts
3. Run `formally-bmad-formal-prd`
4. Run `formally-bmad-formal-architecture`
5. Run `formally-bmad-formal-epics`
6. Run `formally-bmad-formal-stories`
7. Run `formally-bmad-formal-contracts` when implementation-facing contracts are needed
8. Run `formally-bmad-contract-stubs` to generate reviewable skeletons before implementation
9. Run `formally-bmad-code-verification` when code exists
10. Run `formally-bmad-formal-verification` at checkpoints and at the end

The intended call order is strictly sequential once you are in the planning-to-implementation part of the lifecycle:

1. `formally-bmad-formal-prd`
2. `formally-bmad-formal-architecture`
3. `formally-bmad-formal-epics`
4. `formally-bmad-formal-stories`
5. `formally-bmad-formal-contracts`
6. `formally-bmad-contract-stubs`
7. `formally-bmad-code-verification`
8. `formally-bmad-formal-verification`

`formally-bmad-formal-contracts` does not run in parallel with `formally-bmad-formal-stories`.

Reason:

- `formally-bmad-formal-stories` decides the implementation-facing acceptance criteria and obligations
- `formally-bmad-formal-contracts` consumes those accepted obligations and refines them into code-level contracts
- `formally-bmad-contract-stubs` projects those contracts into signatures, types, modules, and contract placement for review
- `formally-bmad-code-verification` then checks actual code against the approved contracts and stub shape

Use this rule of thumb:

- if you are still deciding what implementation must do, stay in `formally-bmad-formal-stories`
- if you are deciding how an accepted obligation becomes a checkable Python, C, or Rust contract, move to `formally-bmad-formal-contracts`
- if you want reviewable code shape before implementation, run `formally-bmad-contract-stubs`
- if code already exists and you want evidence that it satisfies those contracts, run `formally-bmad-code-verification`

Use `formally-bmad-agent-steward` whenever you need:

- canonical model status
- contradiction review
- provenance/status maintenance
- consistency guidance across sessions

## Best First Project

Do not start with a large system. The best first adoption is a single-feature project or a single vertical slice.

A good first run is:

1. setup the module
2. brainstorm one feature
3. formalize the PRD
4. run verification immediately
5. only then continue into architecture and stories
6. add contract derivation once implementation planning begins
7. review generated contract-bearing stubs before full code generation
8. run code verification once real implementation exists

That gives you fast feedback on:

- whether the formalization style is useful
- whether the generated obligations are understandable
- whether the chosen solver/tool mix is adequate

## Step-By-Step Instructions

### 1. Prepare a Project Folder

Create or choose a working project directory.

If BMad is not installed yet in that folder, run:

```bash
npx bmad-method install
```

or:

```bash
npx bmad-method@next install
```

After BMad is installed, the module will create project state under:

```text
_bmad/formally-bmad
```

This is where canonical model state, reports, artifacts, provenance, and tool-run records will live.

### 2. Install The Skills And Run Setup

First, copy these directories from this repository:

- `skills/formally-bmad-setup`
- `skills/formally-bmad-agent-steward`
- `skills/formally-bmad-formal-brainstorming`
- `skills/formally-bmad-formal-import`
- `skills/formally-bmad-ontology-alignment`
- `skills/formally-bmad-formal-prd`
- `skills/formally-bmad-formal-architecture`
- `skills/formally-bmad-formal-epics`
- `skills/formally-bmad-formal-stories`
- `skills/formally-bmad-formal-contracts`
- `skills/formally-bmad-contract-stubs`
- `skills/formally-bmad-code-verification`
- `skills/formally-bmad-formal-verification`

Copy them into the target project's active BMad skill location, usually:

```text
{project-root}/.claude/skills/
```

Each Formally BMAD skill directory should become a direct child of `.claude/skills/`.

Then run:

```text
formally-bmad-setup
```

Setup will:

- register the module
- merge module configuration into `_bmad/config.yaml` and `_bmad/config.user.yaml`
- detect available formal tools
- verify the baseline validation gate
- create the canonical model structure
- produce a setup report

If setup blocks, fix the missing baseline tools first. Do not continue formal verification work without passing setup.

### 3. Choose an Entry Point

Use one of these:

`formally-bmad-formal-brainstorming`

- best for new ideas
- captures assumptions, alternatives, open questions, and candidate concepts
- keeps things flexible while building traceable formal companions

`formally-bmad-formal-import`

- best if you already have existing BMad Markdown artifacts
- inventories source files
- creates import companions and candidate formal deltas
- preserves source meaning rather than rewriting it prematurely

### 4. Formalize Requirements

Run:

```text
formally-bmad-formal-prd
```

This stage should produce:

- a readable PRD
- formalized requirements
- provenance links
- verification obligations
- candidate or accepted canonical deltas

Keep requirements readable. Formal detail belongs in companions, not in unreadable source documents.

### 5. Formalize Architecture

Run:

```text
formally-bmad-formal-architecture
```

This stage should align architecture with accepted requirements and produce:

- component and interface constraints
- invariants
- temporal properties where relevant
- implementation constraints for downstream epics and stories

### 6. Formalize Planning

Run:

```text
formally-bmad-formal-epics
formally-bmad-formal-stories
```

These stages should:

- map requirements to epics
- expose coverage gaps before implementation starts
- produce stories with formalized acceptance criteria
- detect readiness blockers before coding

This is the last stage where you are still defining implementation commitments. Do not start `formally-bmad-formal-contracts` until the relevant stories and acceptance criteria are accepted enough to serve as stable input.

### 7. Derive Code Contracts

Run:

```text
formally-bmad-formal-contracts
```

This stage should:

- translate accepted requirements and story criteria into code-contract surfaces
- choose language-aware notation for Python, C, or Rust
- record whether each contract is exact, conservative, partial, or not faithfully expressible
- generate tool-facing contract views rather than leaving contracts as comments only

When this stage begins:

- stories should already exist
- acceptance criteria should already be formalized
- the target language and target code surface should be known

This stage is downstream from stories, not a parallel drafting activity with them.

### 8. Generate Contract-Bearing Stubs

Run:

```text
formally-bmad-contract-stubs
```

This stage should:

- generate signatures, types, files, modules, or traits with accepted contract placement
- avoid filling in business logic
- provide a review checkpoint for names, boundaries, and contract attachment
- make the user approve code shape before full implementation begins

This is the bridge between contract refinement and full implementation.

### 9. Verify Implementation Against Contracts

Run:

```text
formally-bmad-code-verification
```

This stage should:

- check implementation against generated contracts
- record whether evidence is deductive, symbolic, bounded, runtime, test-based, or manual-review only
- report failures, degraded checks, and contracts that still lack faithful implementation evidence

Only run this stage after contract stubs have been reviewed and actual code exists. If all you have are comments, docstrings, pseudocode, or unreviewed skeletons, you are still too early for strong code-verification claims.

### 10. Run Verification at Checkpoints

Run:

```text
formally-bmad-formal-verification
```

Do not wait until the end. The recommended checkpoint cadence is:

1. after PRD
2. after architecture
3. after stories
4. after contract derivation and stub review when implementation planning becomes concrete
5. after code verification when implementation exists

This gives early signal on:

- contradictions
- missing formal coverage
- traceability gaps
- obligations that are represented structurally but not yet tool-checkable

## What Good MVP Usage Looks Like

For this version of the module, success looks like:

- setup passes
- every major artifact gets a formal companion
- implementation-facing obligations are translated into explicit contracts before strong code-level claims are made
- verification is run repeatedly, not only at the end
- degraded checks are reported honestly
- the canonical model remains the source of truth
- source artifacts stay readable

## What To Expect From Reports

Setup and verification reports should make these things explicit:

- which tools were detected
- which baseline checks passed
- which checks were degraded or skipped
- which contradictions are blocking readiness
- which obligations are tool-checkable with the current environment
- which obligations still need a better backend or a cleaner formal encoding
- which implementation contracts are only runtime/test-backed rather than tool-backed

## Suggested Workflow For Daily Use

For a small project, this is a good operating rhythm:

1. update the current artifact
2. submit the new delta through the relevant workflow
3. check steward status if needed
4. run formal verification at the end of the checkpoint
5. resolve blockers before moving to the next lifecycle stage

## Current Status

This MVP currently validates cleanly:

- module validation passes
- setup-helper tests pass
- setup detects the current solver/tool environment correctly
- verification and steward guidance are aligned with the installed toolchain

If you want to extend this later, the natural next steps are:

- permanent installation paths for `black` and `robot`
- explicit command-level integration of solver runs in verification workflows
- richer backend support such as `cvc5`, `tlc`, `apalache`, or additional ontology reasoners
