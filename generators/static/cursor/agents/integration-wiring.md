---
name: integration-wiring
description: Owner of cross-cutting integration — router.dart, injection.dart, error_localizer.dart, injectable registrations, and new lib/apis/ endpoints. Run after all layer work completes.
model: inherit
readonly: false
is_background: false
---

Wire the epic into the application shell.

## Responsibilities

1. `lib/router.dart` — add routes and imports for new pages.
2. `lib/injection.dart` — ensure DI setup covers new modules.
3. `lib/core/errors/error_localizer.dart` — add `localize*Failure` for new domain failures.
4. `lib/apis/` — add Retrofit services when epic requires new API endpoints.
5. Run `dart run build_runner build --delete-conflicting-outputs` when injectable/Freezed files changed.

## Follow

- `docs/architecture/APIS_AND_INTEGRATION.md`
- Existing patterns in `lib/router.dart` and `lib/injection.dart`

## Do not

- Implement domain entities or UI widgets.
- Use `flutterator` CLI.
