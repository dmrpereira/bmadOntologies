---
name: Manage Assertion Lifecycle
code: assertion-lifecycle
description: Maintains assertion states across artifact evolution.
---

# Manage Assertion Lifecycle

## Outcome

Keep assertion states accurate as BMad artifacts evolve from exploratory ideas into implementation-facing commitments.

## What Success Looks Like

- Assertion states reflect project intent, not just text presence.
- State transitions preserve history instead of overwriting it.
- Rejected and superseded assertions remain in provenance but are excluded from active reasoning.
- Open questions become blockers only when downstream accepted work depends on them.
- Accepted assertions have enough formal coverage and provenance to support readiness checks.

## State Model

Use these states consistently:

- `provisional`
- `candidate`
- `accepted`
- `rejected`
- `superseded`
- `open-question`
- `assumption`

## Outputs

Record state changes with:

- previous and new state;
- source artifact and section;
- user decision or workflow reason;
- impact on active reasoning;
- downstream artifacts that may become stale or blocked.
