# Epics

Track feature delivery as epics under `EPIC-NNN-<slug>.md`.

## Workflow

1. Invoke skill `/epic-delivery` with a high-level product description.
2. Skill creates epic files from `.cursor/skills/epic-delivery/templates/epic.md`.
3. Each epic is implemented via `epic-orchestrator` subagent.
4. Status updated on completion; `layer-guardian` audits DDD boundaries.

## Complexity

- **small** — 1 entity + 1 UI use case → `feature-implementer`
- **large** — multiple entities/screens/API → layer pipeline

See root `AGENTS.md` and `docs/architecture/`.
