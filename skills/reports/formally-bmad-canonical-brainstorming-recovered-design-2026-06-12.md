# Recovered Design For Canonical Brainstorming

## Source

Recovered from [codex_chat_history.md](/Users/dmrpereira/Propostas/bmadOntologies/codex_chat_history.md:401), especially Turns 38 to 41.

## Recovered Interaction Summary

The prior design discussion established that the top surface for the brainstorming skill should not expose raw formal notations such as Why3, TLA+, OWL syntax, or dependent-type languages directly to the user. Instead, the user-facing artifact should be a controlled conceptual modeling DSL written in structured Markdown and rigorous English.

The conversation then refined the architecture into an asymmetric three-layer structure:

- canonical DSL surface as the single authoritative artifact;
- formal ontology maintained from that canonical surface;
- formal system model maintained from that canonical surface.

The key clarification was explicit: these are not three peer artifacts. The ontology and the system model are maintained projections and must follow the canonical surface.

## Recovered Technical Decisions

### Canonical Surface

The canonical artifact should support interactive capture of:

- concepts;
- roles and actors;
- resources and entities;
- relations;
- states;
- events and actions;
- constraints and invariants;
- assumptions;
- open questions;
- alternatives;
- goals and non-goals.

Suggested section structure from the prior interaction:

- Scope
- Concepts
- Relations
- State Model
- Actions
- Constraints
- Invariants
- Assumptions
- Alternatives
- Open Questions

### Ontology Projection

The recommended ontology target was:

- OWL 2 DL as the formal ontology language;
- Manchester Syntax as the preferred human-readable rendering when needed.

Reasoning recovered from the earlier interaction:

- strong formal semantics and standards grounding;
- suitable for concepts, taxonomies, relations, and semantic constraints;
- not suitable as the primary notation for dynamic behavior.

### System-Model Projection

The recommended system-model direction was:

- a restricted hierarchical typed EFSM;
- statechart-inspired, but not full UML state machines.

The intended core features were:

- finite control states;
- typed variables or data state;
- events;
- guarded transitions;
- update actions or effects;
- explicit invariants;
- optional hierarchy;
- optional orthogonal regions only if truly needed.

The intended exclusions for the first implementation were:

- unrestricted orthogonal concurrency;
- do-activities;
- history pseudostates;
- rich pseudostate machinery;
- other semantics-heavy UML features.

### Export And Refinement Direction

The recovered design also positioned the canonical surface as a source for later selective exports:

- OWL/DL for ontology reasoning;
- Alloy for bounded structural exploration;
- TLA+ for temporal or behavior-heavy refinement;
- Why3 for proof obligations and contract derivation.

## Resulting Skill Design Implication

The new skill should preserve conversational brainstorming at the top layer while continuously maintaining:

- `canonical-surface.md` as the authoritative DSL;
- `ontology-projection.md` as the OWL-oriented projection;
- `system-model.md` as the restricted hierarchical typed EFSM projection.

This recovered design supersedes the earlier logic-neutral single-model interpretation when the goal is to make the top surface itself an interactive formal-specification workflow.
