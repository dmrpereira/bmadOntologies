---
name: Export Tool Views
code: export-tool-views
description: Generates check-specific views for automated reasoning tools.
---

# Export Tool Views

## Outcome

Create tool-specific views of the canonical model without letting concrete tool syntax become the canonical representation.

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

Proof-assistant exports are advanced fallback targets only and do not satisfy minimum automated validation capability by themselves.

## Outputs

Produce export records with:

- target family and tool/backend;
- source canonical assertions;
- generated artifact paths;
- tool-run input references;
- limitations or degraded-check notes.
