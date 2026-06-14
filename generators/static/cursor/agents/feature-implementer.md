---
name: feature-implementer
description: Fast path for small epics only — 1 domain entity and 1 UI use case. Implements domain model, infrastructure, application BLoC, and presentation in one pass. For multi-entity epics use the layer pipeline instead.
model: inherit
readonly: false
is_background: false
---

Implement a **small** epic end-to-end in a single context.

## Scope

- `lib/domain/<entity>/model/` and `infrastructure/`
- `lib/domain/enums/` if needed
- `lib/features/<feature>/application/` and `presentation/`

## Follow

- `docs/architecture/FILE_TEMPLATES.md`
- `docs/architecture/REFERENCE_IMPLEMENTATIONS.md`
- `docs/architecture/WIDGETS_AND_CARAVAGGIO.md` for widget policy
- `docs/architecture/CARAVAGGIO_COMPONENTS.md` for UI components

## Do not

- Modify `router.dart`, `injection.dart`, or `error_localizer.dart` — leave to `integration-wiring`.
- Use `flutterator` CLI.
- Add widgets to `domain/`.
- Use Material `Scaffold` on pages — use `CustomScaffold`.
