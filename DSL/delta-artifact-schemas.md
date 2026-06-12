# Delta Artifact Schemas

## Purpose

This note defines the schemas for the two delta-centered artifacts introduced by the revised workflow:

- `proposed-deltas.md`
- `increment-validation.md`

These schemas are intended to be minimal but sufficient for:

- explicit delta tracking;
- baseline-aware validation;
- downstream PRD consumption;
- later backend verification integration.

## 1. proposed-deltas.md

## Role

`proposed-deltas.md` is the ledger of formal increments proposed against the current baseline.

It answers:

- what change is being proposed;
- which canonical assertions introduced it;
- what kind of formal change it is;
- what its current review and disposition state is.

It does **not** record detailed validation results. That belongs in `increment-validation.md`.

## Row Schema

Each row should represent exactly one delta.

Recommended columns:

| Column | Meaning | Required |
| --- | --- | --- |
| `Delta ID` | Stable identifier for the proposed increment | yes |
| `Source Brainstorm Outcome` | Human-facing summary of the idea that triggered the delta | yes |
| `Source Assertion IDs` | Canonical structural/assertion IDs that define the delta | yes |
| `Change Kind` | `add`, `modify`, `supersede`, or `remove` | yes |
| `Target Layer(s)` | One or more of `Ontology`, `ASM`, `Property`, `Mixed` | yes |
| `Summary` | Short explanation of the formal change | yes |
| `Affected Existing IDs` | Existing ontology/ASM/property IDs impacted by the delta | no |
| `DeltaLifecycleStatus` | `proposed`, `under_review`, `accepted`, `rejected`, `deferred` | yes |
| `DeltaValidationStatus` | `not_checked`, `ontology_checked`, `asm_checked`, `impact_checked`, `backend_checked`, `complete` | yes |
| `Disposition` | current decision status for the delta | yes |
| `Notes` | free-form qualification, conflict note, or review rationale | no |

## Constraints

- `Delta ID` must be unique.
- `Source Assertion IDs` must not be empty.
- `Change Kind` must describe the baseline effect, not merely the user’s wording.
- `Disposition` and `DeltaLifecycleStatus` should normally agree, but both are retained because one is lifecycle-oriented and the other is decision-oriented.

## Suggested Identifier Form

- `D-001`
- `D-002`

or grouped by topic if needed:

- `D-ORD-001`

## 2. increment-validation.md

## Role

`increment-validation.md` records whether a proposed delta is a valid increment to the current formal baseline.

It answers:

- what existing formal elements are affected;
- whether the ontology increment is acceptable;
- whether the ASM increment is acceptable;
- which properties must be generated or rechecked;
- what backend evidence exists;
- whether the delta should be accepted into the baseline.

## Row Schema

Each row should correspond to one delta validation record.

Recommended columns:

| Column | Meaning | Required |
| --- | --- | --- |
| `Delta ID` | Identifier linking back to `proposed-deltas.md` | yes |
| `Affected Ontology Elements` | Classes, properties, or semantic constraints touched by the delta | no |
| `Affected ASM Elements` | Domains, functions, predicates, rules, invariants touched by the delta | no |
| `Affected Property IDs` | Existing properties affected by the delta | no |
| `New Property IDs` | Properties newly created because of the delta | no |
| `Obsolete Property IDs` | Properties made obsolete or superseded | no |
| `Recheck Property IDs` | Properties that must be rechecked because of the delta | no |
| `Ontology Increment Result` | `pass`, `fail`, `unknown`, `deferred`, `not_applicable` | yes |
| `ASM Increment Result` | `pass`, `fail`, `unknown`, `deferred`, `not_applicable` | yes |
| `Property Impact Result` | `pass`, `fail`, `unknown`, `deferred`, `not_applicable` | yes |
| `Backend Check Result` | `pass`, `fail`, `unknown`, `deferred`, `not_run` | yes |
| `Overall Increment Result` | `accepted`, `rejected`, `deferred`, `needs_clarification` | yes |
| `Counterexample / Conflict Reference` | Reference to failing check, contradiction, or witness | no |
| `Notes` | reviewer rationale or unresolved issue | no |

## Constraints

- `Delta ID` must exist in `proposed-deltas.md`.
- `Overall Increment Result = accepted` should not occur if a required result field is `fail`.
- `Backend Check Result = not_run` is allowed during brainstorming if the delta is explicitly accepted at a lower confidence stage.
- `Recheck Property IDs` should be used whenever an accepted delta changes previously checked model elements.

## 3. Relationship Between The Two Artifacts

`proposed-deltas.md` is the change ledger.

`increment-validation.md` is the validation ledger.

The intended relationship is:

- every delta begins in `proposed-deltas.md`;
- once reviewed, it gets one corresponding row in `increment-validation.md`;
- the validation row may evolve as more checks are performed;
- the delta should only be merged into the accepted baseline when the validation record’s `Overall Increment Result` permits it.

## 4. Minimal Example

### proposed-deltas.md

| Delta ID | Source Brainstorm Outcome | Source Assertion IDs | Change Kind | Target Layer(s) | Summary | Affected Existing IDs | DeltaLifecycleStatus | DeltaValidationStatus | Disposition | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `D-ORD-001` | Shipment requires confirmed payment | `A-BEH-07` | `add` | `ASM,Property` | Adds shipment prohibition before payment confirmation | `RULE-ShipOrder`, `INV-OrderSafety` | `under_review` | `impact_checked` | `proposed` | central safety rule |

### increment-validation.md

| Delta ID | Affected Ontology Elements | Affected ASM Elements | Affected Property IDs | New Property IDs | Obsolete Property IDs | Recheck Property IDs | Ontology Increment Result | ASM Increment Result | Property Impact Result | Backend Check Result | Overall Increment Result | Counterexample / Conflict Reference | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `D-ORD-001` | `Order`, `Payment`, `hasPayment` | `RULE-ShipOrder`, `INV-OrderSafety` | `P-OLD-002` | `P-NEW-014` |  | `P-OLD-002` | `pass` | `pass` | `pass` | `deferred` | `accepted` |  | accepted with property recheck pending |

## 5. Recommended Markdown Presentation

The first implementation can keep these artifacts as tables because they are ledger-oriented rather than grammar-oriented.

That is different from the canonical DSL itself:

- canonical DSL should remain hybrid and declaration-oriented;
- delta and validation artifacts can remain strongly table-oriented.

## 6. Downstream Consumption Requirement

PRD should eventually consume:

- accepted deltas from `proposed-deltas.md`;
- their validation outcomes from `increment-validation.md`;
- and any deferred or failed increments that materially affect requirement confidence.

This is necessary so PRD reflects not just accepted assertions, but the validation state of the evolving formal baseline.
