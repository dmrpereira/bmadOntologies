---
name: formally-bmad-ontology-alignment
description: Aligns project concepts with ontologies. Use when the user requests to 'align ontology concepts', 'search ontology repositories', or 'import ontology terms into formally-bmad'.
---

# formally-bmad-ontology-alignment

## Overview

This workflow discovers relevant external ontology concepts, compares them with Formally BMAD project concepts, proposes controlled mappings/imports, records external provenance, and submits ontology deltas to the steward for validation. Act as an ontology alignment specialist: use external repositories to improve grounding, but never silently import external commitments into the canonical model.

## Conventions

- Bare paths (e.g. `scripts/alignment_workspace.py`) resolve from the skill root.
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

If `--headless` or `-H` is invoked without explicit concepts, create only the alignment workspace and a repository registry, then stop with a report explaining that concept selection is required for meaningful alignment.

## Workflow

### Prepare Alignment Workspace

Run the deterministic workspace helper:

```bash
python3 scripts/alignment_workspace.py --project-root {project-root} --module-root "{formally_bmad_project_root}"
```

The helper creates `{formally_bmad_project_root}/artifacts/ontology-alignment/`, a default repository registry, a candidate mapping file, and a Markdown alignment report skeleton.

### Select Project Concepts

Identify the project concepts to align from one of these sources:

- canonical ontology concepts under `{formally_bmad_canonical_model_path}/ontology/`;
- candidate concepts produced by `formally-bmad-formal-import`;
- concepts named by the user;
- concepts from PRD, architecture, epic, or story companions.

Do not align vague terms until their project meaning is clear enough to compare. If the local concept definition is missing, create an `open-question` rather than searching blindly.

### Search External Repositories

Search configured open ontology repositories and knowledge sources relevant to the domain. Default repository families include:

- BioPortal for broad biomedical ontology discovery;
- OBO Foundry for interoperable open biomedical ontologies;
- Linked Open Vocabularies for RDF/OWL vocabularies;
- Wikidata for identifiers, cross-links, and term grounding;
- Ontohub or similar sources for heterogeneous formal ontologies when relevant.

Record search provenance for every candidate: repository, query, retrieved label, URI, ontology/source, version or retrieval date, license/status if available, and source URL.

If live web/API access is unavailable, produce a degraded alignment report and do not fabricate repository results.

### Compare Meanings

For each candidate external concept, compare it with the project concept and propose exactly one mapping status:

- `exact` — same intended concept;
- `broader` — external concept is more general;
- `narrower` — external concept is more specific;
- `related` — useful association but not substitutable;
- `conflict` — incompatible assumptions or axioms;
- `no-match` — not suitable.

Explain the mapping in rigorous English and identify any external axioms or commitments that could affect the canonical model.

### Propose Controlled Imports

External concepts enter the Formally BMAD model only as `candidate` or `provisional` ontology deltas unless the user explicitly approves promotion. Each proposed import must include:

- project concept identifier;
- external label and URI;
- source repository and ontology;
- version/date and license/status;
- mapping status and rationale;
- imported commitments, excluded commitments, and known risks;
- provenance back to the source artifact or canonical concept that motivated the search.

### Submit to Steward

Submit approved ontology deltas to `formally-bmad-agent-steward` through the `Accept Canonical Delta` and `Validate Update Consistency` capabilities.

If the steward reports semantic conflict or contradiction, block the import until the user chooses a repair, rejects the mapping, narrows the import, or explicitly overrides continuation. Overrides must mark the canonical model inconsistent.

### Produce Alignment Report

Create `{formally_bmad_project_root}/reports/ontology-alignment-report.md` summarizing:

- project concepts considered;
- repositories searched and search provenance;
- candidate terms and mapping statuses;
- accepted, rejected, and deferred imports;
- semantic conflicts and repair proposals;
- steward validation outcomes;
- next recommended formalization or verification action.

HTML may be produced later by reporting workflows; this workflow must always produce Markdown.

### Handoff

If useful mappings were accepted, recommend the lifecycle workflow that benefits most from the grounded concepts. If conflicts remain, recommend `formally-bmad-formal-verification` or steward contradiction review before continuing implementation-facing artifacts.
