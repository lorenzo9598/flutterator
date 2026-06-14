---
name: layer-presentation
description: Creates presentation UI with CaravaggioUI and shared widgets from lib/widgets/common/. Handles feature pages, components, and lib/features/components/. Runs after layer-application.
model: inherit
readonly: false
is_background: false
---

Implement only the **presentation** layer for the current epic.

## Before coding

Read both:

1. `docs/architecture/WIDGETS_AND_CARAVAGGIO.md`
2. `docs/architecture/CARAVAGGIO_COMPONENTS.md`

Optional pattern reference: skill `/caravaggio-ui`.

## Output paths

- `lib/features/<feature>/presentation/<name>_page.dart` or `<name>_component.dart`
- `lib/features/components/<name>/` for cross-feature reusable components
- `lib/features/<feature>/presentation/widgets/` for feature-local widgets

## Rules

- **Pages:** `CustomScaffold` (not Material `Scaffold`). `showBackButton: false` only on Home/Splash/Login.
- **Components:** no scaffold; parent provides `CustomScaffold` + `BlocProvider`.
- Use CaravaggioUI components from the catalog where available.
- Reuse `LoadingWidget`, `ErrorWidget`, `UnknownStateWidget` from `lib/widgets/common/`.
- Use `BlocBuilder` with typed states and `ErrorLocalizer` for failures.
- Do not modify `router.dart` — leave to `integration-wiring`.
