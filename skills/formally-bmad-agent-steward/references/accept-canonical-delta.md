---
name: Accept Canonical Delta
code: accept-delta
description: Reviews proposed canonical model deltas before validation.
---

# Accept Canonical Delta

## Outcome

Decide whether a proposed canonical model delta may be committed to the Formally BMAD project model.

## What Success Looks Like

- The source artifact and source section behind the delta are identified.
- Each proposed assertion has an assertion state, logic-family placement, and rigorous English explanation.
- The delta preserves the canonical model contract: source intent, formal assertion, provenance, validation expectation, and lifecycle stage are all connected.
- Unsupported guesses are rejected or downgraded to `candidate`, `provisional`, `open-question`, or `assumption`.
- Accepted deltas are ready for consistency validation before becoming committed model state.

## Required Inputs

- Source artifact reference and relevant excerpt or section identifier.
- Proposed logic-native delta.
- Assertion states.
- Lifecycle stage and validation strictness.
- Companion rigorous English formalization.

## Outputs

Return one of:

- `accepted_for_validation`: delta is structurally suitable and should be checked.
- `needs_clarification`: formalization is blocked by ambiguity.
- `rejected`: delta is unsupported by source intent or violates the model contract.

Include affected artifact paths, assertion identifiers, and a short reason for every non-accepted item.
