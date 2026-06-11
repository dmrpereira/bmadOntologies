---
name: Validate Update Consistency
code: validate-update
description: Checks model updates with configured automated reasoning.
---

# Validate Update Consistency

## Outcome

Validate a proposed or committed model update against the current canonical model using the strongest configured automated checks available for the relevant logic family.

## What Success Looks Like

- Accepted assertions are checked according to lifecycle-stage strictness.
- Provisional and candidate assertions receive compatibility checks without creating false contradictions among alternatives.
- Missing optional tools are recorded as degraded checks only when at least one supported automated reasoning backend is available.
- Contradictions are reported as blockers unless the user explicitly overrides continuation.
- Validation records are suitable for later readiness and verification reports.

## Validation Targets

- Description logic ontology commitments.
- First-order specification assertions.
- Temporal lifecycle, ordering, state, or behavior properties.
- Higher-order/meta assertions only when the model genuinely requires them.

## Outputs

Produce a validation result with:

- status: `passed`, `blocked`, `degraded`, or `inconsistent`;
- checked assertions and skipped/degraded checks;
- tool views or tool-run references when available;
- contradictions, ambiguities, and missing coverage;
- repair proposals with affected source artifacts and expected consequences.
