# Widgets

## App-wide (`lib/widgets/common/`)

Shared across the app:

- `loading_widget.dart`
- `error_widget.dart`
- `unknown_state_widget.dart`

Always check here before creating new loading/error UI.

## Feature components

Reusable UI with BLoC: `lib/features/components/` — not under `widgets/`.

## Policy

See `docs/architecture/WIDGETS_AND_CARAVAGGIO.md`.
