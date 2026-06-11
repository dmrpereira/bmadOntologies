---
name: Validate Update Consistency
code: validate-update
description: Checks model updates with configured automated reasoning.
---

# Validate Update Consistency

## Outcome

Validate a proposed or committed model update against the current canonical model using the strongest configured automated checks available for the relevant logic family.

For the MVP, prefer one direct backend per logic family and record degraded checks instead of attempting speculative multi-tool orchestration.

## What Success Looks Like

- Accepted assertions are checked according to lifecycle-stage strictness.
- Provisional and candidate assertions receive compatibility checks without creating false contradictions among alternatives.
- Missing optional tools are recorded as degraded checks only when at least one supported automated reasoning backend is available.
- Contradictions are reported as blockers unless the user explicitly overrides continuation.
- Validation records are suitable for later readiness and verification reports.

## MVP Tool Routing

Use the strongest currently available backend that matches the obligation:

- SMT obligations: `z3`, then `cvc5`, then `cvc4`
- first-order obligations: `vampire`, then `eprover`, then `prover9`
- finite countermodel attempts: `mace4` when useful and available
- SAT-oriented Boolean reductions: `kissat`, then `cadical`, then `minisat`, then `glucose`
- temporal satisfiability/consistency checks: `black`
- temporal/state-model checks: `tlc`, then `apalache`, then `alloy` when a faithful executable view exists
- ontology validation: `robot`, then `hermit`, `elk`, `jfact`, `factplusplus`, or `pellet`

Proof assistants such as `rocq`, `coqc`, `lean`, `lake`, and `isabelle` are support tooling only for the MVP and should not be treated as the primary validation backend.

If no faithful translation is available, mark the check `degraded` or `not-applicable` instead of overstating the result.

## Validation Targets

- Description logic ontology commitments.
- First-order specification assertions.
- Temporal lifecycle, ordering, state, or behavior properties.
- Higher-order/meta assertions only when the model genuinely requires them.

## Outputs

Produce a validation result with:

- status: `passed`, `blocked`, `degraded`, or `inconsistent`;
- checked assertions and skipped/degraded checks;
- selected backend per checked logic family;
- tool views or tool-run references when available;
- contradictions, ambiguities, and missing coverage;
- repair proposals with affected source artifacts and expected consequences.
