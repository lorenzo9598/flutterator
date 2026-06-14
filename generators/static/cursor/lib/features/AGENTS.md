# Features layer

Vertical use cases under `lib/features/<name>/`.

## Structure

- `application/` — BLoC, events, states (Freezed)
- `presentation/` — pages, components, feature-local widgets

## Reusable components

Cross-feature UI with its own BLoC: `lib/features/components/<name>/` (same application + presentation layout).

## Rules

- Application depends on domain interfaces, not infrastructure implementations.
- **Pages** use `CustomScaffold` from `lib/widgets/common/custom_scaffold.dart` (never Material `Scaffold`).
- **Components** (`*_component.dart`) have no scaffold — parent page provides it.
- Presentation uses CaravaggioUI — see `docs/architecture/CARAVAGGIO_COMPONENTS.md`.
- Reuse `lib/widgets/common/` shared widgets.
- Routes go in `lib/router.dart` via integration-wiring.

See `docs/architecture/WIDGETS_AND_CARAVAGGIO.md`.
