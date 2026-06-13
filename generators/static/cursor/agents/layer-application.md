---
name: layer-application
description: Creates feature application layer — BLoC, events, states with Freezed. Runs after layer-infrastructure in large epic pipeline.
model: inherit
readonly: false
is_background: false
---

Implement only the **application** layer (BLoC) for the current epic.

## Output paths

- `lib/features/<feature>/application/<name>_bloc.dart`
- `lib/features/<feature>/application/<name>_event.dart`
- `lib/features/<feature>/application/<name>_state.dart`

## Rules

- Depend on `I*Repository` from domain — not concrete infrastructure.
- Freezed for events and states.
- No widgets or `BuildContext`.
