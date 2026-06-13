---
name: layer-presentation
description: Creates presentation UI with CaravaggioUI and shared widgets from lib/widgets/common/. Handles feature pages, components, and lib/features/components/. Runs after layer-application.
model: inherit
readonly: false
is_background: false
---

Implement only the **presentation** layer for the current epic.

## Before coding

Read `docs/architecture/WIDGETS_AND_CARAVAGGIO.md`.

## Output paths

- `lib/features/<feature>/presentation/<name>_page.dart` or `<name>_component.dart`
- `lib/features/components/<name>/` for cross-feature reusable components
- `lib/features/<feature>/presentation/widgets/` for feature-local widgets

## Rules

- Use CaravaggioUI components where available.
- Reuse `LoadingWidget`, `ErrorWidget`, `UnknownStateWidget` from `lib/widgets/common/`.
- Use `BlocBuilder` with typed states and `ErrorLocalizer` for failures.
- Do not modify `router.dart` — leave to `integration-wiring`.
