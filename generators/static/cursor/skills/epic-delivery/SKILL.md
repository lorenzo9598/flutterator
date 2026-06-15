---
name: epic-delivery
description: Decompose a high-level project description into epics and orchestrate implementation via subagents. Use when the user describes features, product scope, or asks to plan and build new functionality.
---

# Epic delivery

Turn a high-level product description into implemented DDD features.

## Prerequisites

Read before starting:

- Root `AGENTS.md`
- `docs/architecture/DDD_LAYERS.md`
- `docs/architecture/FILE_TEMPLATES.md`
- `docs/architecture/CARAVAGGIO_COMPONENTS.md` (when epic includes UI)
- `docs/architecture/MOCK_AND_REMOTE_DATA.md` (when epic includes domain entities or API)

## Workflow

### 1. Analyze

Understand the user's description. Identify domain entities, UI use cases, and dependencies between features.

### 2. Decompose into epics

Create one file per epic: `docs/epics/EPIC-NNN-<slug>.md` using template in `templates/epic.md`.

Each epic should be atomic: typically **one domain aggregate + one UI use case**.

Assign complexity tag:

| Tag | When |
|-----|------|
| `small` | 1 entity, 1 UI use case, no new API endpoints |
| `large` | Multiple entities, multiple screens, new Retrofit endpoints, or cross-feature components |

### 3. Order epics

Respect dependencies (e.g. auth before protected features). Implement independent epics sequentially or note parallelization in epic files.

### 4. Implement each epic

Delegate to subagent **`epic-orchestrator`** with:

- Epic file path
- Complexity tag (`small` | `large`)

**small** pipeline (~4 subagents):

```
feature-implementer → integration-wiring → doc-writer → layer-guardian
```

**large** pipeline (~6–7 subagents):

```
layer-model → layer-infrastructure → layer-application → layer-presentation
  → integration-wiring → doc-writer → layer-guardian
```

### 5. Close epic

- Update epic file status (template: `templates/epic-status.md`)
- Run `flutter analyze`
- Address `layer-guardian` findings

## Constraints

- **Never** run `flutterator` CLI — write Dart files directly.
- Do not duplicate widget policy — use `docs/architecture/WIDGETS_AND_CARAVAGGIO.md` and `docs/architecture/CARAVAGGIO_COMPONENTS.md`.
- For data layers use `docs/architecture/MOCK_AND_REMOTE_DATA.md` — default mock, create `assets/mock/<entity>.json`.
- Use Explore subagent for codebase search; Bash for analyze and build_runner.
