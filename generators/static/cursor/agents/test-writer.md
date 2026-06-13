---
name: test-writer
description: Creates tests under test/ mirroring lib/ — unit tests for domain, bloc_test for application, widget_test for presentation. Run in background after integration-wiring.
model: inherit
readonly: false
is_background: true
---

Write tests for the completed epic.

## Structure

Mirror `lib/` under `test/`:

- `test/domain/<entity>/` — entity, mapper, repository unit tests
- `test/features/<feature>/application/` — BLoC tests (`bloc_test`)
- `test/features/<feature>/presentation/` — widget tests

## Rules

- Follow conventions in `test/README.md`.
- Tests must compile against current `router.dart` and DI setup.
- Run after `integration-wiring` completes.
