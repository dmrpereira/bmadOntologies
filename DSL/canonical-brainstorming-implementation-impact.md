# Canonical Brainstorming Implementation Impact

## Purpose

This note identifies the implementation changes required in `formally-bmad-canonical-brainstorming` once the DSL and mapping contract are accepted.

The goal is to define:

- what the brainstorming skill must produce directly;
- what it may defer;
- what should be delegated to later workflows such as `formally-bmad-formal-verification`.

This is still a design-level artifact, not a code change request.

## Boundary Decision

The brainstorming skill should be responsible for:

1. capturing stable canonical assertions in the DSL;
2. maintaining ontology and ASM projection drafts from those assertions;
3. generating initial formal property records from accepted behavioral assertions;
4. maintaining traceability rows for formalized outcomes;
5. recording verification readiness and gaps.

The brainstorming skill should not be responsible for:

1. performing heavy backend verification by default during open-ended ideation;
2. guaranteeing that every property is checked in-session;
3. managing backend-specific syntax as the primary user-facing artifact;
4. replacing the later dedicated verification workflow.

So the boundary is:

- brainstorming produces **formalization-ready and partially verification-ready artifacts**;
- the verification skill performs **backend-oriented checking, translation, and evidence consolidation**.

## Required Changes To The Brainstorming Skill Contract

### 1. Canonical DSL capture rules must become stricter

The skill currently treats the canonical surface as a structured artifact, but it does not yet require the full assertion schema.

It will need to require:

- structural IDs for concepts, relations, states, events, and actions;
- assertion IDs for behavioral claims;
- decomposed fields for behavioral assertions;
- split status dimensions;
- optional qualified names / namespace usage.

Practical effect:

- the skill must no longer accept “good enough prose” once a claim becomes stable;
- it must normalize stable claims into the required canonical schema.

### 2. Assertion pattern recognition must become explicit

The skill will need an internal rule for classifying stable behavioral claims into one of:

- `Ubiquitous`
- `EventDriven`
- `StateDriven`
- `Conditional`
- `OptionalFeature`
- `Negative`

Practical effect:

- the skill must ask for clarification if a stable claim cannot be assigned a pattern cleanly;
- the classification decision should be visible in the canonical artifact.

### 3. Ontology projection must be assertion-linked

`ontology-projection.md` must stop being only a companion summary and become an assertion-linked formal projection.

It will need to include:

- source IDs on classes, properties, and semantic constraints;
- optional qualified names where ontology alignment matters;
- a distinction between semantic structure and dynamic behavior.

Practical effect:

- the skill must preserve ontology grounding as part of the active workflow, not only as a later possible refinement.

### 4. ASM projection must be assertion-linked

`asm-model.md` must explicitly reference canonical structural and behavioral source IDs.

It will need to include:

- domains;
- controlled functions;
- monitored functions;
- derived predicates;
- rules;
- invariants;
- source assertion IDs on each mapped item.

Practical effect:

- the ASM model becomes a real controlled projection, not a loose narrative summary.

### 5. Property generation must begin in brainstorming

The brainstorming skill should generate initial property records for accepted behavioral assertions rather than deferring all property creation to the verification skill.

At minimum, for each eligible accepted behavioral assertion, it should create:

- a property ID;
- property kind;
- informal meaning;
- source assertion IDs;
- target backend form placeholder;
- status.

Practical effect:

- the brainstorming skill becomes the place where verification intent first appears explicitly;
- later verification no longer starts from scratch.

### 6. Verification traceability must be mandatory

`verification-traceability.md` should not be optional bookkeeping.

It should be required whenever a stable formally significant brainstorm outcome exists.

Practical effect:

- every important stable outcome gets tracked through the projection chain;
- missing ontology, ASM, property, or backend coverage becomes visible.

### 7. Mechanized evidence language must be stricter

The skill must clearly distinguish:

- mapped but unchecked;
- property generated but unchecked;
- checked pass;
- checked fail;
- checked unknown.

Practical effect:

- the skill must stop using generic “formalized” language once actual backend evidence is the real issue.

## Required Changes To Workspace Templates

The workspace templates will need to align with the mapping contract.

### canonical-surface.md

Must support:

- optional namespace section;
- structural declarations with IDs;
- assertion catalog with:
  - statement;
  - decomposed fields;
  - ontology terms;
  - behavior terms;
  - split statuses.

### ontology-projection.md

Must support:

- source IDs on all major elements;
- optional qualified names;
- semantic constraints linked back to assertions.

### asm-model.md

Must support:

- explicit mapping from canonical IDs to ASM domains, functions, rules, and invariants.

### generated-properties.md

Must support:

- property creation during brainstorming;
- placeholders for target backend form.

### verification-traceability.md

Must support:

- one row per stable formally meaningful outcome;
- partial completion when later verification has not yet happened.

### backend-checks.md

Must support:

- empty by default when no checking occurred;
- explicit population once verification runs.

## Interaction Design Impact

The brainstorming conversation will need to change in subtle but important ways.

### The skill should remain generative early

During exploration:

- accept loose ideas;
- avoid forcing formal fields too early.

### The skill must normalize once ideas stabilize

When a claim becomes stable enough to matter formally:

- assign IDs;
- classify the pattern;
- decompose the behavior fields;
- update ontology and ASM projections;
- create property placeholders where required.

This suggests a two-mode interaction inside one session:

1. exploratory mode;
2. normalization mode.

### Clarification questions should become artifact-driven

The skill should ask questions such as:

- “Is this a trigger-response rule or a state-conditioned rule?”
- “Is this a forbidden outcome or a required response?”
- “Should this be treated as an assumption or an asserted requirement?”
- “Does this relation affect runtime behavior or only semantic grounding?”

These questions are better than generic brainstorming prompts once formalization begins.

## What Should Remain Deferred To The Verification Skill

The later verification workflow should still own:

- backend-specific concrete syntax generation;
- model translation or flattening;
- actual model-checking runs;
- counterexample harvesting and interpretation;
- consolidated verification reports.

This is important because the brainstorming skill should remain usable during creative discovery and not collapse into a verification console too early.

## Recommended First Implementation Boundary

For the first implementation, the brainstorming skill should:

- create property records;
- create traceability rows;
- leave `backend-checks.md` empty unless an explicit verification action occurs;
- clearly mark assertions as:
  - `not_mapped`
  - `mapped`
  - `property_generated`

Then the verification skill can later advance them to:

- `checked_pass`
- `checked_fail`
- `checked_unknown`

This is the cleanest division of labor.

## Implementation Sequence Recommendation

Once implementation begins, the canonical brainstorming skill should be changed in this order:

1. update workspace templates;
2. update canonical DSL authoring instructions;
3. update ontology projection instructions;
4. update ASM projection instructions;
5. add generated-property and traceability maintenance rules;
6. tighten evidence language around backend checks;
7. only then update downstream PRD consumption rules.

## Resulting Readiness Condition

The brainstorming skill is ready to hand off downstream when:

- canonical assertions are stable and identified;
- ontology and ASM projections exist for all relevant accepted items;
- generated properties exist for eligible accepted behavioral assertions;
- traceability rows exist for stable formally significant outcomes;
- unchecked items are explicitly marked as such.

That is the minimum stable artifact package the PRD workflow should consume.
