---
name: Export Tool Views
code: export-tool-views
description: Generates check-specific views for automated reasoning tools.
---

# Export Tool Views

## Outcome

Create tool-specific views of the canonical model without letting concrete tool syntax become the canonical representation.

For the MVP, generate only the views that correspond to currently supported installed backends and to obligations that can be translated faithfully without inventing semantics.

## What Success Looks Like

- The logic-native canonical model remains authoritative.
- Exports are scoped to the check being run and include enough metadata to trace results back to canonical assertions.
- Tool views prefer automated checking targets over proof-assistant workflows.
- Missing optional export backends are reported as degraded checks, not silently ignored.

## Preferred Target Families

- Description logic / OWL-DL style ontology views.
- First-order prover or model finder views, such as TPTP-like representations.
- SMT views for decidable fragments and practical constraints.
- Temporal model checking views for lifecycle, ordering, state, and behavior.
- Temporal satisfiability views for finite-trace or requirement-consistency checking.

Proof-assistant exports are advanced fallback targets only and do not satisfy minimum automated validation capability by themselves.

## MVP Backend Preferences

Prefer these concrete targets when available:

- SMT views: `z3`, then `cvc5`, then `cvc4`
- first-order views: `vampire`, then `eprover`, then `prover9`; `mace4` for finite-model-oriented exports
- SAT-style Boolean views: `kissat`, `cadical`, `minisat`, `glucose`
- temporal satisfiability views: `black`
- executable temporal/state-machine views: `tlc`, then `apalache`, then `alloy`
- ontology views: `robot`, then ontology reasoners/tools such as `hermit`, `elk`, `jfact`, `factplusplus`, or `pellet`

If a backend is missing or the translation would be misleading, emit a degraded export record instead of fabricating a stronger view.

## Outputs

Produce export records with:

- target family and tool/backend;
- source canonical assertions;
- generated artifact paths;
- tool-run input references;
- whether the export is authoritative, degraded, or suggestive only;
- limitations or degraded-check notes.
