---
name: Maintain Provenance and Status
code: provenance-status
description: Keeps traceability, indexes, versions, and status current.
---

# Maintain Provenance and Status

## Outcome

Keep the canonical model auditable by maintaining traceability, status, indexes, version history, and stale-state signals.

## What Success Looks Like

- Every active accepted assertion can be traced to a source artifact section or explicit user decision.
- Formal companions link back to their source artifacts and forward to validation/tool-run evidence.
- Model status accurately reflects consistency, degraded checks, stale artifacts, blockers, and overrides.
- Verification workflows can build reports from the provenance records without reconstructing history from conversation.

## Status Vocabulary

Use these statuses consistently when applicable:

- `consistent`
- `inconsistent`
- `stale`
- `blocked`
- `overridden`
- `degraded`
- `initialized`

## Outputs

Maintain or update:

- `canonical/status.md`;
- provenance records;
- contradiction/override ledger;
- model version metadata;
- artifact formal status block data;
- indexes for artifacts, assertions, reports, and open issues.
