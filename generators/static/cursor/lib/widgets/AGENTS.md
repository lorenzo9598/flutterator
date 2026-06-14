# Widgets

## App-wide (`lib/widgets/common/`)

Shared across the app:

- `custom_scaffold.dart` — **required** for all routed pages (wraps `CScaffold`)
- `loading_widget.dart` — `CLoader.bouncing()`
- `error_widget.dart` — localized error display
- `unknown_state_widget.dart` — unhandled BLoC states

Always check here before creating new page shells or loading/error UI.

## Feature components

Reusable UI with BLoC: `lib/features/components/` — not under `widgets/`.

## Policy

- `docs/architecture/WIDGETS_AND_CARAVAGGIO.md` — locations, CustomScaffold rules
- `docs/architecture/CARAVAGGIO_COMPONENTS.md` — full CaravaggioUI catalog
