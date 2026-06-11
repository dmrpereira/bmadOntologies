---
name: Handle Contradictions and Overrides
code: contradictions-overrides
description: Blocks, resolves, or records inconsistent model states.
---

# Handle Contradictions and Overrides

## Outcome

Ensure contradictions block progress unless resolved or explicitly overridden, and make any inconsistent model state deliberate and visible.

## What Success Looks Like

- The contradiction is explained in source-artifact language before formal notation.
- Affected assertions, artifacts, tool checks, and downstream risks are identified.
- Repair proposals are concrete enough for a lifecycle workflow to present or apply after confirmation.
- If the user overrides the contradiction, the canonical model status becomes inconsistent and the override ledger records the decision.

## Repair Proposal Quality

Useful repairs may include:

- editing a source requirement or architecture decision;
- splitting an overloaded concept;
- marking a claim as an assumption;
- choosing between alternatives;
- weakening or strengthening a constraint;
- superseding stale canonical assertions.

## Outputs

Produce either:

- a resolved contradiction record with accepted repairs and updated status, or
- an override record containing the contradiction, user decision, affected artifacts, downstream risk, and inconsistent model status.
