# Canonical DSL Rationale And BNF

## Purpose

This note records the proposed direction for the canonical DSL used by `formally-bmad-dsl-brainstorming` before further implementation work.

The goal is to define a user-facing formalization surface that is:

- readable during brainstorming;
- rigorous enough to support ontology projection;
- rigorous enough to support ASM projection;
- structured enough to support generated formal properties and backend verification;
- traceable enough to prove that brainstorm outcomes were actually reflected in the formal model and verification workflow.

## Design Position

The canonical DSL should be **assertion-centered** and should combine three complementary styles:

- ontology-style declarations for vocabulary and semantic grounding;
- EARS-like requirement patterns for behavioral assertions;
- Gherkin-like scenarios only as optional examples or validation evidence.

This means the DSL should not be a raw logic language, should not be a raw theorem-prover syntax, and should not be a pure scenario language.

## Why The DSL Should Not Be Raw ASM

The user-facing artifact should not be the ASM itself.

Reasons:

- brainstorming sessions begin with domain language, not update rules;
- ontology grounding and vocabulary control need a separate semantic layer;
- many brainstorm outcomes are better expressed first as normalized assertions than as direct state-transition rules;
- forcing users into ASM too early would distort the elicitation process and make the workflow less usable.

Therefore:

- the canonical DSL is the authoritative surface;
- the ontology is a maintained projection from the DSL;
- the ASM model is a maintained projection from the DSL;
- generated properties and backend checks are also maintained from the DSL.

## Why The Ontology Still Needs Its Own Representation

The ontology should continue to exist as a first-class formal projection.

Reasons:

- it captures what exists and how terms relate;
- it supports semantic grounding and vocabulary reuse;
- it preserves concept-level structure independently of behavioral evolution;
- it provides a clean source for OWL 2 DL-oriented formalization;
- it prevents the ASM model from being overloaded with semantic responsibilities that belong to concept modeling.

The ontology is therefore not replaced by ASM. It remains a separate formal artifact linked to canonical assertion IDs.

## Why EARS-Like Patterns Are A Good Move

Behavioral assertions should use EARS-like normal forms.

Reasons:

- they normalize trigger/condition/response structure cleanly;
- they are much closer to formal behavioral projection than unconstrained prose;
- they remain readable for humans during brainstorming;
- they map naturally into ASM rules, guards, and invariants;
- they can drive property generation more reliably than free-form text.

Recommended behavioral assertion patterns:

- `Ubiquitous`: `The system shall <response>.`
- `EventDriven`: `When <trigger>, the system shall <response>.`
- `StateDriven`: `While <state/condition>, the system shall <response>.`
- `Conditional`: `If <precondition>, then the system shall <response>.`
- `OptionalFeature`: `Where <feature is present>, the system shall <response>.`
- `Negative`: `The system shall never <forbidden outcome>.`

These patterns should live inside a broader assertion-centered DSL rather than being presented as raw EARS compliance.

## Why Gherkin Should Not Be The Canonical Core

Gherkin-like scenarios should be optional supporting artifacts, not the semantic center.

Reasons:

- Gherkin is scenario-first rather than assertion-first;
- it is better for examples and acceptance narratives than for formal semantic projection;
- it is awkward as the primary source for ontology construction;
- it tends to express example traces rather than model-wide obligations.

Gherkin-like scenarios still have value:

- to illustrate intended behavior;
- to provide evidence or validation examples;
- to contextualize canonical assertions;
- to help explain backend counterexamples.

But they should reference canonical assertion IDs, not replace them.

## Why Assertion IDs Are Central

Each accepted structural or behavioral claim should receive an assertion ID.

The assertion ID is the unit that supports:

- ontology grounding;
- ASM mapping;
- generated property derivation;
- backend result tracking;
- traceability from brainstorm to mechanized evidence.

Without assertion IDs, the workflow cannot cleanly establish:

- whether a brainstorm outcome was formalized;
- how it was formalized;
- whether it was checked;
- whether it passed or failed.

## Traceability Requirement

Every stable brainstorm outcome that matters formally should be able to move through this chain:

1. brainstorm outcome
2. canonical DSL assertion
3. ontology element(s)
4. ASM element(s)
5. generated property
6. backend check result

This chain is not optional. It is the mechanism that turns “formal brainstorming” into a defensible verification-oriented workflow.

## Proposed Canonical Sections

The DSL document should normally maintain:

1. `Scope`
2. `Concepts`
3. `Relations`
4. `States`
5. `Events And Actions`
6. `Assertion Catalog`
7. `Scenarios`
8. `Assumptions`
9. `Alternatives`
10. `Open Questions`

The `Assertion Catalog` is the semantic pivot for downstream ontology projection, ASM projection, property generation, and backend checking.

## Validated Critique Decisions

The following decisions were validated before revising the grammar:

1. Use a **hybrid surface**:
   - declaration semantics;
   - Markdown-friendly structured presentation.
2. Keep structural sections such as `Concepts`, `Relations`, `States`, and `Events And Actions`, but give every declaration its own ID.
3. Keep behavioral assertions as:
   - a readable normalized sentence;
   - plus decomposed fields for formal projection.
4. Split status into separate dimensions:
   - `LifecycleStatus`;
   - `KnowledgeStatus`;
   - `VerificationStatus`.
5. Support ontology namespace/prefix declarations from the start as an optional section.

## Revised BNF Grammar

The grammar below reflects those validated decisions. It is still intentionally constrained and favors deterministic parsing over stylistic freedom.

```bnf
<document> ::= [<namespaces-section>]
               <scope-section>
               <concepts-section>
               <relations-section>
               <states-section>
               <events-section>
               <assertions-section>
               [<scenarios-section>]
               [<assumptions-section>]
               [<alternatives-section>]
               [<open-questions-section>]

<namespaces-section> ::= "## Namespaces" <nl>
                         { <prefix-decl> }

<prefix-decl> ::= "Prefix" <ws> <prefix-name> ":" <ws> <iri> <nl>

<prefix-name> ::= <identifier>

<scope-section> ::= "## Scope" <nl>
                    <text-block>

<concepts-section> ::= "## Concepts" <nl>
                       { <concept-decl> }

<concept-decl> ::= "Concept" <ws> <structural-id> ":" <ws> <identifier> <ws> "as" <ws> <concept-kind> <nl>
                   [<qualified-name-line>]
                   [<lifecycle-status-line>]
                   [<knowledge-status-line>]
                   [<verification-status-line>]
                   [<indented-definition>]

<concept-kind> ::= "Actor"
                 | "Entity"
                 | "Resource"
                 | "Role"
                 | "Event"
                 | "StateType"
                 | "ValueType"

<relations-section> ::= "## Relations" <nl>
                        { <relation-decl> }

<relation-decl> ::= "Relation" <ws> <structural-id> ":" <ws>
                    <identifier> <ws> <relation-name> <ws> <cardinality> <ws> <identifier>
                    <nl>
                    [<qualified-name-line>]
                    [<lifecycle-status-line>]
                    [<knowledge-status-line>]
                    [<verification-status-line>]
                    [<indented-notes-line>]

<relation-name> ::= <identifier>

<cardinality> ::= "exactlyOne"
                | "atMostOne"
                | "oneOrMore"
                | "many"
                | "optional"

<states-section> ::= "## States" <nl>
                     { <state-decl> }

<state-decl> ::= "State" <ws> <structural-id> ":" <ws> <identifier> <ws> "=" <ws> <state-list> <nl>
                 [<lifecycle-status-line>]
                 [<knowledge-status-line>]
                 [<verification-status-line>]
                 [<indented-notes-line>]

<state-list> ::= <identifier> { <ws> "|" <ws> <identifier> }

<events-section> ::= "## Events And Actions" <nl>
                     { <event-decl> }

<event-decl> ::= "Event" <ws> <structural-id> ":" <ws> <identifier> [ "(" <parameter-list> ")" ] <nl>
                 [<lifecycle-status-line>]
                 [<knowledge-status-line>]
                 [<verification-status-line>]
                 [<indented-notes-line>]
               | "Action" <ws> <structural-id> ":" <ws> <identifier> [ "(" <parameter-list> ")" ] <nl>
                 [<lifecycle-status-line>]
                 [<knowledge-status-line>]
                 [<verification-status-line>]
                 [<indented-notes-line>]

<parameter-list> ::= <parameter> { "," <ws> <parameter> }

<parameter> ::= <identifier> ":" <ws> <identifier>

<assertions-section> ::= "## Assertion Catalog" <nl>
                         { <assertion-decl> }

<assertion-decl> ::= <assertion-header>
                     <assertion-statement>
                     [<assertion-trigger>]
                     [<assertion-condition>]
                     [<assertion-response>]
                     [<assertion-forbidden-outcome>]
                     [<assertion-feature-scope>]
                     [<assertion-ontology-terms>]
                     [<assertion-behavior-terms>]
                     <lifecycle-status-line>
                     <knowledge-status-line>
                     <verification-status-line>
                     [<assertion-notes>]

<assertion-header> ::= "Assertion" <ws> <assertion-id> ":" <ws> <assertion-pattern> <nl>

<assertion-id> ::= <identifier>

<structural-id> ::= <identifier>

<assertion-pattern> ::= "Concept"
                      | "Relation"
                      | "Ubiquitous"
                      | "EventDriven"
                      | "StateDriven"
                      | "Conditional"
                      | "OptionalFeature"
                      | "Negative"

<assertion-statement> ::= "Statement:" <ws> <quoted-text> <nl>

<assertion-trigger> ::= "Trigger:" <ws> <quoted-text> <nl>

<assertion-condition> ::= "Condition:" <ws> <quoted-text> <nl>

<assertion-response> ::= "Response:" <ws> <quoted-text> <nl>

<assertion-forbidden-outcome> ::= "ForbiddenOutcome:" <ws> <quoted-text> <nl>

<assertion-feature-scope> ::= "FeatureScope:" <ws> <quoted-text> <nl>

<assertion-ontology-terms> ::= "OntologyTerms:" <ws> <identifier-list> <nl>

<assertion-behavior-terms> ::= "BehaviorTerms:" <ws> <identifier-list> <nl>

<assertion-notes> ::= "Notes:" <ws> <text-line> <nl>

<identifier-list> ::= <identifier> { "," <ws> <identifier> }

<scenarios-section> ::= "## Scenarios" <nl>
                        { <scenario-decl> }

<scenario-decl> ::= "Scenario" <ws> <identifier> ":" <ws> <scenario-style> <nl>
                    [<lifecycle-status-line>]
                    [<knowledge-status-line>]
                    [<verification-status-line>]
                    { <scenario-line> }

<scenario-style> ::= "GherkinLike"
                   | "Example"

<scenario-line> ::= "Given" <ws> <text-line> <nl>
                  | "When" <ws> <text-line> <nl>
                  | "Then" <ws> <text-line> <nl>
                  | "And" <ws> <text-line> <nl>
                  | "References:" <ws> <identifier-list> <nl>

<assumptions-section> ::= "## Assumptions" <nl>
                          { <assumption-decl> }

<assumption-decl> ::= "Assumption" <ws> <identifier> ":" <ws> <quoted-text> <nl>
                      <lifecycle-status-line>
                      <knowledge-status-line>
                      <verification-status-line>

<alternatives-section> ::= "## Alternatives" <nl>
                           { <alternative-decl> }

<alternative-decl> ::= "Alternative" <ws> <identifier> ":" <ws> <quoted-text> <nl>
                       <lifecycle-status-line>
                       <knowledge-status-line>
                       <verification-status-line>
                       [<indented-implication>]
                       [<indented-excludes>]

<indented-implication> ::= <indent> "Implication:" <ws> <text-line> <nl>

<indented-excludes> ::= <indent> "Excludes:" <ws> <identifier-list> <nl>

<open-questions-section> ::= "## Open Questions" <nl>
                             { <open-question-decl> }

<open-question-decl> ::= "Question" <ws> <identifier> ":" <ws> <quoted-text> [<ws> <blocking-layer>] <nl>
                         <lifecycle-status-line>
                         <knowledge-status-line>
                         <verification-status-line>

<blocking-layer> ::= "[Ontology]"
                   | "[ASM]"
                   | "[Property]"
                   | "[Backend]"
                   | "[Canonical]"

<qualified-name-line> ::= "QualifiedName:" <ws> <qualified-name> <nl>

<lifecycle-status-line> ::= "LifecycleStatus:" <ws> <lifecycle-status> <nl>

<knowledge-status-line> ::= "KnowledgeStatus:" <ws> <knowledge-status> <nl>

<verification-status-line> ::= "VerificationStatus:" <ws> <verification-status> <nl>

<lifecycle-status> ::= "provisional"
                     | "candidate"
                     | "accepted"
                     | "rejected"
                     | "superseded"

<knowledge-status> ::= "asserted"
                     | "assumption"
                     | "open_question"

<verification-status> ::= "not_mapped"
                        | "mapped"
                        | "property_generated"
                        | "checked_pass"
                        | "checked_fail"
                        | "checked_unknown"

<text-block> ::= <text-line> { <nl> <text-line> } <nl>

<indented-definition> ::= <indent> "Definition:" <ws> <text-line> <nl>

<indented-notes-line> ::= <indent> "Notes:" <ws> <text-line> <nl>

<text-line> ::= <text-char> { <text-char> }

<quoted-text> ::= "\"" <quoted-char-seq> "\""

<quoted-char-seq> ::= { <quoted-char> }

<qualified-name> ::= <prefix-name> ":" <identifier>

<iri> ::= <nonspace-text>

<identifier> ::= <letter> { <letter> | <digit> | "_" | "-" }

<nonspace-text> ::= <nonspace-char> { <nonspace-char> }

<indent> ::= "  "

<ws> ::= " " { " " }

<nl> ::= "\n"
```

## Interpretation Notes For The Grammar

- The grammar is for the **canonical DSL surface**, not for the ontology or ASM artifacts.
- The surface is **hybrid**: Markdown-friendly sections with declaration-oriented semantics.
- Structural sections remain authoritative for structural declarations, and each structural declaration now carries its own ID.
- `Assertion Catalog` is reserved for behavioral and obligation-style assertions rather than duplicating structural declarations.
- Behavioral assertions keep a readable sentence but also include decomposed fields such as `Trigger`, `Condition`, `Response`, or `ForbiddenOutcome` where applicable.
- `Scenarios` are explicitly optional and subordinate.
- Status is now split across `LifecycleStatus`, `KnowledgeStatus`, and `VerificationStatus`.
- Namespace support is optional through the `Namespaces` section and `QualifiedName` lines.
- The grammar is intentionally narrower than natural Markdown so that deterministic parsing and later projection become practical.

## Recommended Next Review Questions

Before implementation, the next useful review points are:

1. whether the assertion pattern set is sufficient;
2. whether the decomposed behavioral fields are sufficient for ASM and property generation;
3. whether `Scenarios` should stay optional or move to a separate companion file;
4. whether the split status vocabulary is right for the intended workflow;
5. whether qualified names should be allowed on more constructs than concepts and relations in the first implementation.
