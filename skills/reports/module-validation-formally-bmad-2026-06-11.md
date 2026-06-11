# Module Validation Report: Formally BMAD

- Date: 2026-06-11
- Module code: `formally-bmad`
- Module name: `Formally BMAD`
- Target: `skills/`
- Validator: `.agents/skills/bmad-module-builder/scripts/validate-module.py`

## Result

Status: `pass`

Structural validation passed with 0 findings.

## Fixes Applied Before Final Assessment

Patched agent roster metadata so the agent code matches the skill directory basename:

- [skills/formally-bmad-setup/assets/module.yaml](/Users/dmrpereira/Propostas/bmadOntologies/skills/formally-bmad-setup/assets/module.yaml:10)
- [skills/formally-bmad-agent-steward/customize.toml](/Users/dmrpereira/Propostas/bmadOntologies/skills/formally-bmad-agent-steward/customize.toml:9)

Updated value:

- from: `agent-steward`
- to: `formally-bmad-agent-steward`

Patched setup policy enforcement and contract alignment for the baseline validation gate:

- baseline now requires at least one supported SMT solver
- baseline also requires at least one supported first-order or SAT solver
- SAT family added to the detected tool families: `kissat`, `cadical`, `minisat`, `glucose`
- proof assistants remain relevant and reported, but do not satisfy the baseline by themselves

Patched files:

- [skills/formally-bmad-setup/scripts/setup_environment.py](/Users/dmrpereira/Propostas/bmadOntologies/skills/formally-bmad-setup/scripts/setup_environment.py:18)
- [skills/formally-bmad-setup/SKILL.md](/Users/dmrpereira/Propostas/bmadOntologies/skills/formally-bmad-setup/SKILL.md:10)
- [skills/formally-bmad-setup/assets/module.yaml](/Users/dmrpereira/Propostas/bmadOntologies/skills/formally-bmad-setup/assets/module.yaml:58)
- [skills/formally-bmad-setup/scripts/tests/test_setup_environment.py](/Users/dmrpereira/Propostas/bmadOntologies/skills/formally-bmad-setup/scripts/tests/test_setup_environment.py:1)

Patched setup detection and reporting so advanced-but-non-baseline tooling is surfaced explicitly:

- added explicit reporting for specialized temporal satisfiability tooling: `black`
- added explicit reporting for ontology workbench tooling: `robot`
- added explicit reporting for proof assistants in setup results
- added extra tool search directory support, including session-local installs under `/private/tmp/black-install/bin` and `/private/tmp/robot/bin`

Patched files:

- [skills/formally-bmad-setup/scripts/setup_environment.py](/Users/dmrpereira/Propostas/bmadOntologies/skills/formally-bmad-setup/scripts/setup_environment.py:18)
- [skills/formally-bmad-setup/SKILL.md](/Users/dmrpereira/Propostas/bmadOntologies/skills/formally-bmad-setup/SKILL.md:78)
- [skills/formally-bmad-setup/scripts/tests/test_setup_environment.py](/Users/dmrpereira/Propostas/bmadOntologies/skills/formally-bmad-setup/scripts/tests/test_setup_environment.py:1)

Patched MVP verification routing so downstream verification now names the currently supported toolchain explicitly:

- SMT: `z3`, then `cvc5`, then `cvc4`
- first-order: `vampire`, then `eprover`, then `prover9`; `mace4` for finite countermodels
- SAT: `kissat`, then `cadical`, then `minisat`, then `glucose`
- temporal satisfiability: `black`
- temporal/state-model checking: `tlc`, then `apalache`, then `alloy`
- ontology validation/export: `robot`, then ontology reasoners/tools
- proof assistants remain support-only for the MVP

Patched files:

- [skills/formally-bmad-formal-verification/SKILL.md](/Users/dmrpereira/Propostas/bmadOntologies/skills/formally-bmad-formal-verification/SKILL.md:10)
- [skills/formally-bmad-agent-steward/references/validate-update-consistency.md](/Users/dmrpereira/Propostas/bmadOntologies/skills/formally-bmad-agent-steward/references/validate-update-consistency.md:11)
- [skills/formally-bmad-agent-steward/references/export-tool-views.md](/Users/dmrpereira/Propostas/bmadOntologies/skills/formally-bmad-agent-steward/references/export-tool-views.md:11)

Expanded the module with an explicit implementation-facing contract and code-verification layer:

- added `formally-bmad-formal-contracts` to derive language-aware code contracts from accepted requirements and story obligations
- added `formally-bmad-code-verification` to collect implementation evidence against generated contracts
- supported MVP contract/verification guidance for Python, C, and Rust
- added deterministic workspace helpers and unit tests for both new skills
- updated setup reporting to surface contract-oriented executable backends: `crosshair`, `frama-c`, `cbmc`, `cargo-kani`, `prusti-rustc`, `cargo-creusot`
- updated module help and documentation so the lifecycle now includes stories -> contracts -> code verification -> final verification

Patched files:

- [skills/formally-bmad-formal-contracts/SKILL.md](/Users/dmrpereira/Propostas/bmadOntologies/skills/formally-bmad-formal-contracts/SKILL.md:1)
- [skills/formally-bmad-formal-contracts/scripts/contracts_workspace.py](/Users/dmrpereira/Propostas/bmadOntologies/skills/formally-bmad-formal-contracts/scripts/contracts_workspace.py:1)
- [skills/formally-bmad-code-verification/SKILL.md](/Users/dmrpereira/Propostas/bmadOntologies/skills/formally-bmad-code-verification/SKILL.md:1)
- [skills/formally-bmad-code-verification/scripts/code_verification_workspace.py](/Users/dmrpereira/Propostas/bmadOntologies/skills/formally-bmad-code-verification/scripts/code_verification_workspace.py:1)
- [skills/formally-bmad-setup/assets/module-help.csv](/Users/dmrpereira/Propostas/bmadOntologies/skills/formally-bmad-setup/assets/module-help.csv:1)
- [README.md](/Users/dmrpereira/Propostas/bmadOntologies/README.md:1)
- [docs/formally-bmad-quickstart.md](/Users/dmrpereira/Propostas/bmadOntologies/docs/formally-bmad-quickstart.md:1)

Inserted a contract-stub review gate between contract derivation and implementation verification:

- added `formally-bmad-contract-stubs` to generate contract-bearing code skeletons for review before real code generation
- updated lifecycle ordering to: stories -> contracts -> contract stubs -> code verification -> final verification
- updated setup structure so `_bmad/formally-bmad/artifacts/stubs/` exists from setup onward

Patched files:

- [skills/formally-bmad-contract-stubs/SKILL.md](/Users/dmrpereira/Propostas/bmadOntologies/skills/formally-bmad-contract-stubs/SKILL.md:1)
- [skills/formally-bmad-contract-stubs/scripts/contract_stubs_workspace.py](/Users/dmrpereira/Propostas/bmadOntologies/skills/formally-bmad-contract-stubs/scripts/contract_stubs_workspace.py:1)
- [skills/formally-bmad-setup/assets/module-help.csv](/Users/dmrpereira/Propostas/bmadOntologies/skills/formally-bmad-setup/assets/module-help.csv:1)
- [skills/formally-bmad-setup/scripts/setup_environment.py](/Users/dmrpereira/Propostas/bmadOntologies/skills/formally-bmad-setup/scripts/setup_environment.py:1)
- [README.md](/Users/dmrpereira/Propostas/bmadOntologies/README.md:1)
- [docs/formally-bmad-quickstart.md](/Users/dmrpereira/Propostas/bmadOntologies/docs/formally-bmad-quickstart.md:1)

Expanded the language-specific contract/code-verification backend sets and made missing-backend behavior explicit:

- Python backends now include `crosshair`, `deal`, `nagini`, `esbmc`
- C backends now include `frama-c`, `cbmc`, `esbmc`, `verifast`
- Rust backends now include `cargo-kani`, `prusti-rustc`, `cargo-prusti`, `cargo-creusot`, `verus`, `flux`, `verifast`, `esbmc`
- `formal-contracts` now treats missing compatible backends as an explicit install/degrade/cancel decision
- `contract-stubs` warns and may offer installation, but can still proceed as a review gate
- `code-verification` treats missing compatible backends as a blocker for strong verification claims unless the user explicitly accepts degraded evidence

Patched files:

- [skills/formally-bmad-formal-contracts/SKILL.md](/Users/dmrpereira/Propostas/bmadOntologies/skills/formally-bmad-formal-contracts/SKILL.md:1)
- [skills/formally-bmad-contract-stubs/SKILL.md](/Users/dmrpereira/Propostas/bmadOntologies/skills/formally-bmad-contract-stubs/SKILL.md:1)
- [skills/formally-bmad-code-verification/SKILL.md](/Users/dmrpereira/Propostas/bmadOntologies/skills/formally-bmad-code-verification/SKILL.md:1)
- [skills/formally-bmad-setup/SKILL.md](/Users/dmrpereira/Propostas/bmadOntologies/skills/formally-bmad-setup/SKILL.md:1)
- [skills/formally-bmad-setup/scripts/setup_environment.py](/Users/dmrpereira/Propostas/bmadOntologies/skills/formally-bmad-setup/scripts/setup_environment.py:1)
- [README.md](/Users/dmrpereira/Propostas/bmadOntologies/README.md:1)
- [docs/formally-bmad-quickstart.md](/Users/dmrpereira/Propostas/bmadOntologies/docs/formally-bmad-quickstart.md:1)

## Quality Assessment

No remaining structural or quality findings after the metadata fix.

Confirmed:

- setup skill and module metadata are complete
- `module-help.csv` contains one coherent entry per registered skill
- action names, descriptions, and phase ordering align with the skill behaviors
- agent roster metadata is now consistent with the agent skill directory and `customize.toml`
- setup policy prose, module metadata, and helper enforcement now describe the same baseline rule
- setup now surfaces installed advanced tooling separately from the baseline gate without confusing those tools with mandatory setup requirements
- verification workflow and steward reference docs now agree on MVP backend routing and degraded-check behavior
- the PRD/stories/verification contract now distinguishes structured formalization, planned mechanized checks, and actual tool-backed evidence
- the module now has an explicit requirement-to-contract-to-code-evidence path for implementation-facing work
- the module now has an explicit contract-to-stub review gate before full implementation
- implementation-facing workflows now spell out language-specific backend expectations and degraded/blocking behavior when those backends are missing
- focused setup-helper tests pass for the new baseline decision logic

## Overall Assessment

The module is ready for use.

## Verification Performed

- `python3 .agents/skills/bmad-module-builder/scripts/validate-module.py skills`
  Result: `pass`, 0 findings
- `python3 -m unittest skills/formally-bmad-setup/scripts/tests/test_setup_environment.py`
  Result: `Ran 9 tests ... OK`
- `python3 -m unittest skills/formally-bmad-formal-contracts/scripts/tests/test_contracts_workspace.py`
  Result: `Ran 2 tests ... OK`
- `python3 -m unittest skills/formally-bmad-contract-stubs/scripts/tests/test_contract_stubs_workspace.py`
  Result: `Ran 2 tests ... OK`
- `python3 -m unittest skills/formally-bmad-code-verification/scripts/tests/test_code_verification_workspace.py`
  Result: `Ran 2 tests ... OK`

Validation complete.
