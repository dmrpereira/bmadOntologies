---
name: formally-bmad-formal-brainstorming
description: Brainstorms with formal capture. Use when the user requests to 'run formal brainstorming', 'brainstorm with formally-bmad', or 'capture ideas as provisional formal concepts'.
---

# formally-bmad-formal-brainstorming

## Overview

This workflow runs BMad-style brainstorming while capturing exploratory ideas as provisional formal knowledge. It preserves alternatives, assumptions, open questions, and candidate concepts without treating them as commitments, then promotes decisions into steward-reviewed canonical deltas when the user converges. Act as a creative BMad facilitator with a formalization layer underneath: keep the session generative, but make future traceability possible.

## Conventions

- Bare paths (e.g. `scripts/brainstorm_workspace.py`) resolve from the skill root.
- `{skill-root}` resolves to this skill's installed directory.
- `{project-root}`-prefixed paths resolve from the project working directory.
- `{skill-name}` resolves to the skill directory's basename.

## On Activation

Load available config from `{project-root}/_bmad/config.yaml` and `{project-root}/_bmad/config.user.yaml` (root level and `formally-bmad` section). Resolve these values, using setup defaults only when config is absent:

- `formally_bmad_project_root`: `{project-root}/_bmad/formally-bmad`
- `formally_bmad_canonical_model_path`: `{project-root}/_bmad/formally-bmad/canonical`
- `formally_bmad_validation_strictness`: `stage-aware`
- `formally_bmad_report_format`: `markdown,html`

If `{formally_bmad_project_root}` or `{formally_bmad_canonical_model_path}/status.md` is missing, stop and direct the user to run `formally-bmad-setup`.

If `--headless` or `-H` is invoked, require an input brief or source artifact path. Without one, create the workspace and stop with a report saying interactive brainstorming needs user input.

## Workflow

### Open the Floor

Invite the user to share the full idea space before structuring: goals, frustrations, examples, constraints, terminology, candidate concepts, and anything uncertain. Capture generously without forcing formal language into the conversation.

Keep the user-facing style BMad-like. Formal notation belongs in companions and deltas, not in the normal brainstorming flow unless the user asks for it.

### Initialize Workspace

Run the deterministic workspace helper once the brainstorming topic is known:

```bash
python3 scripts/brainstorm_workspace.py --project-root {project-root} --module-root "{formally_bmad_project_root}" --topic "{topic-slug}"
```

The helper creates a source-artifact-oriented companion folder under `{formally_bmad_project_root}/artifacts/brainstorming/`, plus Markdown files for raw capture, rigorous English formalization, candidate delta, provenance, and local validation.

### Exploratory Capture

Capture ideas in two synchronized forms:

- a readable BMad-style brainstorming artifact for the user;
- companion formal notes that classify concepts, alternatives, assumptions, open questions, and candidate relationships.

Use conservative assertion states:

- `provisional` for exploratory ideas;
- `candidate` for plausible concepts, goals, constraints, or relationships;
- `open-question` for unresolved ambiguity;
- `assumption` only when the user frames something as assumed;
- `rejected` or `superseded` when the user explicitly rules something out.

Do not submit raw exploratory ideas as accepted canonical assertions.

### Model Alternatives

Represent competing ideas as alternatives, not contradictions. Preserve enough structure for future PRD formalization:

- alternative label;
- what it would imply if chosen;
- what it conflicts with or excludes;
- what evidence or decision would promote it;
- current state.

### Clarify Only When Formalization Is Blocked

Stay generative unless ambiguity blocks useful formal capture. When clarification is needed, ask a concise artifact-oriented question and explain what downstream formalization it unlocks.

Distinguish:

- tolerable underspecification;
- explicit assumption;
- formalization blocker;
- contradiction among accepted or promoted claims.

### Promote Decisions

When the user converges, convert selected ideas into candidate or accepted-for-validation deltas. Before submission, state the promoted decision in structured English and identify the source brainstorming section.

Submit promoted deltas to `formally-bmad-agent-steward` through `Accept Canonical Delta`. If the steward requests clarification or reports conflict, keep the decision in the brainstorming companion until resolved.

### Produce Companions

Maintain the companion folder with:

- `brainstorm.md` — readable brainstorming artifact;
- `formalization.md` — rigorous English formalization of concepts and relationships;
- `candidate-delta.md` — provisional/candidate/promoted assertions;
- `alternatives.md` — competing options and decision state;
- `provenance.md` — source idea to assertion mapping;
- `local-validation.md` — ambiguity, blockers, steward responses, and next steps.

### Handoff

End with:

- the brainstorming artifact path;
- the companion folder path;
- promoted concepts and still-open questions;
- whether any steward-accepted deltas were created;
- recommended next workflow: `formally-bmad-ontology-alignment` for concept grounding or `formally-bmad-formal-prd` for requirements.
