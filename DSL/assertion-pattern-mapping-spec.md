# Assertion Pattern Mapping Spec

## Purpose

This note defines the initial mapping contract from the canonical DSL into:

- ontology projection;
- ASM projection;
- generated properties;
- verification traceability.

It is intentionally narrow. The goal is to stabilize the canonical brainstorming workflow before downstream skill changes.

## Scope

This first version covers:

- structural declarations:
  - `Concept`
  - `Relation`
  - `State`
  - `Event`
  - `Action`
- behavioral assertion patterns:
  - `Ubiquitous`
  - `EventDriven`
  - `StateDriven`
  - `Conditional`
  - `OptionalFeature`
  - `Negative`

## Shared Mapping Rules

These rules apply to every mapped item.

### R1. Source of truth

The canonical DSL is authoritative.

- ontology, ASM, generated properties, and backend check ledgers are projections;
- projections must cite source IDs from the canonical DSL;
- if a projection conflicts with the canonical DSL, the projection is wrong.

### R2. Structural IDs and assertion IDs

- structural sections use structural IDs such as `C-`, `R-`, `S-`, `E-`, `ACT-`;
- behavioral assertions use assertion IDs such as `A-`.

Every projected ontology element, ASM element, and generated property must cite one or more of these IDs.

### R3. Mapping states

Every item may exist in one of these verification progression states:

- `not_mapped`
- `mapped`
- `property_generated`
- `checked_pass`
- `checked_fail`
- `checked_unknown`

Only `generated-properties.md` and `backend-checks.md` may move an item beyond `mapped`.

### R4. Traceability row

Every stable brainstorm outcome with formal significance gets one row in `verification-traceability.md`:

| Brainstorm Outcome | Canonical Source ID(s) | Ontology Element(s) | ASM Element(s) | Generated Property ID(s) | Backend Check Result | Notes |

### R5. Delta creation is mandatory for stable formal changes

Every stable structural or behavioral change with formal significance must create or update a delta record.

That means:

- mapping does not stop at ontology/ASM/property generation;
- it must also identify the formal increment being proposed against the current baseline.

### R6. Recheck obligations are part of mapping

For every delta, the mapping must determine:

- whether new properties are required;
- whether existing properties become obsolete;
- whether existing properties must be rechecked because the baseline changed.

Property generation and recheck planning are both part of the mapping contract.

## Structural Declaration Mapping

### 1. Concept

Canonical shape:

- ID
- local name
- kind
- optional qualified name
- definition

Ontology mapping:

- create or reuse an OWL class for `Actor`, `Entity`, `Resource`, or `Role`;
- create datatype-style support concepts for `StateType` and `ValueType` when needed;
- attach source ID.

ASM mapping:

- create a domain, carrier set, or typed vocabulary element if behavior refers to the concept;
- if the concept is purely semantic and never behaviorally referenced, no ASM element is required yet.

Generated property mapping:

- none by default;
- properties only generated if later behavioral assertions constrain the concept.

Traceability rule:

- ontology element required;
- ASM element optional.

Delta rule:

- creates `add` delta for new concept;
- creates `modify` delta if definition, qualified name, or kind changes;
- creates `supersede` delta if a concept replaces or merges earlier concept meaning.

Recheck rule:

- no property recheck by default unless the concept participates in existing behavioral assertions or invariants.

### 2. Relation

Canonical shape:

- ID
- subject
- relation name
- cardinality
- object
- optional qualified name

Ontology mapping:

- create or reuse an object property or data property;
- attach domain/range;
- map cardinality into semantic constraint where supported;
- attach source ID.

ASM mapping:

- if relation participates in behavior, introduce controlled/monitored function or predicate;
- if relation is static semantic structure only, ASM element is optional.

Generated property mapping:

- cardinality-like or exclusivity constraints may generate invariants when they affect runtime behavior.

Traceability rule:

- ontology element required;
- ASM element conditional on behavioral use.

Delta rule:

- creates `add` delta for new relation;
- creates `modify` delta if cardinality, domain/range intent, or semantics change;
- creates `supersede` delta if relation meaning replaces earlier relation semantics.

Recheck rule:

- recheck required when relation is already referenced by ASM functions, predicates, rules, or generated properties.

### 3. State

Canonical shape:

- ID
- state family name
- enumerated members

Ontology mapping:

- optional controlled vocabulary projection only;
- do not force the entire state system into ontology semantics unless useful.

ASM mapping:

- required if referenced by behavior;
- becomes domain enumeration, controlled function range, or predicate family.

Generated property mapping:

- none by default;
- later behavioral assertions generate state-related properties.

Traceability rule:

- ASM element usually required once behavior exists.

Delta rule:

- creates `add` delta for new state family or new member;
- creates `modify` delta if state membership or interpretation changes;
- creates `supersede` delta if state family replaces earlier behavioral partitioning.

Recheck rule:

- recheck required for any property that references affected states or dependent rules.

### 4. Event / Action

Canonical shape:

- ID
- name
- parameters

Ontology mapping:

- optional event/action concept or relation only if semantic grounding matters.

ASM mapping:

- becomes monitored event, derived trigger abstraction, or named rule anchor.

Generated property mapping:

- none by default;
- later behavioral assertions may generate trigger/guard/response properties.

Traceability rule:

- ASM element usually required if used in behavior.

Delta rule:

- creates `add` delta for new event/action;
- creates `modify` delta if parameters or meaning change;
- creates `supersede` delta if event/action replaces an earlier behavioral trigger.

Recheck rule:

- recheck required for any rule or property whose trigger or effect depends on the event/action.

## Behavioral Assertion Mapping

## Common Behavioral Field Rules

Every behavioral assertion must include:

- `Assertion ID`
- `Pattern`
- `Statement`
- `OntologyTerms`
- `BehaviorTerms`
- `LifecycleStatus`
- `KnowledgeStatus`
- `VerificationStatus`

Additional fields depend on pattern type.

### 5. Ubiquitous

Canonical intent:

- unconditional obligation or invariant

Required fields:

- `Response`

Ontology mapping:

- ground referenced terms only;
- create no dynamic ontology structure unless the response carries semantic constraints.

ASM mapping:

- map into invariant, always-enabled rule obligation, or global consistency condition.

Generated property mapping:

- generate an invariant property by default.

Traceability rule:

- property generation expected unless explicitly deferred.

Delta rule:

- usually creates `add` delta for new invariant-style commitment;
- creates `modify` or `supersede` delta if it tightens, weakens, or replaces an earlier global commitment.

Recheck rule:

- recheck all invariants or temporal obligations that mention affected ontology/ASM terms.

### 6. EventDriven

Canonical intent:

- when trigger occurs, system must respond

Required fields:

- `Trigger`
- `Response`

Ontology mapping:

- ground trigger and response vocabulary terms;
- semantic event classifications only if useful.

ASM mapping:

- trigger becomes event/rule activation condition;
- response becomes update summary, enabled consequence, or post-state effect.

Generated property mapping:

- generate one of:
  - transition precondition property;
  - response obligation property;
  - temporal trigger-response property.

Initial default:

- generate trigger-response safety/obligation form.

Traceability rule:

- ASM element and property both expected.

Delta rule:

- creates `add` delta for new trigger-response rule;
- creates `modify` delta if trigger or response semantics refine an existing rule;
- creates `supersede` delta if it replaces prior trigger-response logic.

Recheck rule:

- recheck all properties tied to the affected trigger, rule, or response state.

### 7. StateDriven

Canonical intent:

- while some state or condition holds, the system must maintain a behavior or constraint

Required fields:

- `Condition`
- `Response`

Ontology mapping:

- ground state vocabulary and affected concepts.

ASM mapping:

- condition becomes state predicate or guard context;
- response becomes maintained invariant or permitted/forbidden update condition.

Generated property mapping:

- generate invariant or state-conditioned temporal property.

Initial default:

- invariant if expressible as state safety;
- temporal property otherwise.

Traceability rule:

- property generation expected.

Delta rule:

- creates `add` delta for new state-conditioned obligation;
- creates `modify` delta if the state predicate or maintained response changes;
- creates `supersede` delta if it replaces an earlier state-conditioned commitment.

Recheck rule:

- recheck all properties and invariants dependent on the referenced state predicate.

### 8. Conditional

Canonical intent:

- if precondition holds, required response follows

Required fields:

- `Condition`
- `Response`

Ontology mapping:

- ground terms only;
- static semantic implication only if clearly ontological.

ASM mapping:

- condition becomes guard or predicate antecedent;
- response becomes update effect, obligation, or enablement.

Generated property mapping:

- generate implication-style invariant or temporal obligation.

Initial default:

- invariant if the condition/response are state predicates;
- temporal obligation if event progression is implied.

Traceability rule:

- property generation expected.

Delta rule:

- creates `add` delta for new implication-style rule;
- creates `modify` delta if antecedent or consequent meaning changes;
- creates `supersede` delta if it replaces an earlier implication or guard structure.

Recheck rule:

- recheck all properties tied to the condition or response terms and any ASM guard dependent on them.

### 9. OptionalFeature

Canonical intent:

- behavior applies only where a named feature/configuration is active

Required fields:

- `FeatureScope`
- `Response`

Ontology mapping:

- optionally ground the feature as a concept/configuration capability.

ASM mapping:

- feature scope becomes guard predicate, configuration flag, or monitored capability condition.

Generated property mapping:

- generate scoped invariant or scoped obligation property.

Traceability rule:

- must identify the feature-scoping mechanism explicitly in ASM.

Delta rule:

- creates `add` delta for new feature-scoped behavior;
- creates `modify` delta if the scope or scoped behavior changes;
- creates `supersede` delta if it replaces earlier feature-specific commitments.

Recheck rule:

- recheck properties whose applicability depends on the same feature scope.

### 10. Negative

Canonical intent:

- forbidden behavior or forbidden state

Required fields:

- `ForbiddenOutcome`

Optional fields:

- `Condition`

Ontology mapping:

- ground the forbidden concepts and relations only;
- avoid encoding dynamic prohibition as ontology semantics unless static contradiction is intended.

ASM mapping:

- map into guard prohibition, forbidden-state invariant, or disabled update condition.

Generated property mapping:

- generate forbidden-state or safety invariant by default.

Initial default:

- invariant if the outcome can be expressed as forbidden state;
- temporal safety property if the prohibition is event-sequenced.

Traceability rule:

- property generation is mandatory for accepted negative assertions.

Delta rule:

- creates `add` delta for new prohibition;
- creates `modify` delta if the condition or forbidden outcome changes;
- creates `supersede` delta if it replaces an earlier prohibition or permitted behavior.

Recheck rule:

- recheck every property touching the forbidden outcome, enabling trigger, or affected state region.

## Property Taxonomy

The initial property set is intentionally small.

### P1. Invariant

Use when the assertion can be expressed as a state condition that must always hold.

### P2. Guard / Precondition Property

Use when an event or action must only occur under stated conditions.

### P3. Forbidden-State Property

Use when a combination of states, values, or outcomes must never be reachable.

### P4. Reachability Expectation

Use when the workflow expects that some state or outcome must be reachable under assumptions.

### P5. Temporal Obligation

Use when the assertion implies progression over time rather than a single-state condition.

## Initial Default Mapping Table

| Pattern | Preferred ASM Form | Preferred Property Kind |
| --- | --- | --- |
| `Ubiquitous` | invariant / global condition | `Invariant` |
| `EventDriven` | trigger + rule/update | `Temporal Obligation` or `Guard / Precondition` |
| `StateDriven` | state predicate + maintained condition | `Invariant` |
| `Conditional` | guard / implication | `Invariant` or `Temporal Obligation` |
| `OptionalFeature` | feature guard | `Invariant` or `Temporal Obligation` |
| `Negative` | prohibition / forbidden update | `Forbidden-State Property` or `Invariant` |

## Verification Ledger Contract

### generated-properties.md

Each generated property must include:

- `Property ID`
- `Kind`
- `Source Assertion IDs`
- `Origin Delta ID`
- `Informal Meaning`
- `Target Backend Form`
- `Status`

### backend-checks.md

Each backend check row must include:

- `Check ID`
- `Backend`
- `Model Artifact`
- `Property IDs`
- `Triggered By Delta ID`
- `Result`
- `Counterexample / Witness`
- `Notes`

### verification-traceability.md

Each row should be updated progressively:

- once ontology mapping exists, fill ontology column;
- once ASM mapping exists, fill ASM column;
- once property exists, fill property column;
- once backend result exists, fill backend result column;
- once a delta exists, the row should also indicate whether the change is accepted, deferred, or rejected.

## Non-Goals For This First Version

This first mapping spec does not yet define:

- exact ASM concrete syntax;
- exact nuXmv/NuSMV concrete syntax;
- multi-pattern assertion composition;
- quantified cardinality-to-property expansion rules;
- namespace semantics beyond optional qualified names.

Those are second-step design items, after this mapping contract is accepted.
