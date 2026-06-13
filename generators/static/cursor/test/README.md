# Tests

Mirror `lib/` structure under `test/`.

## Conventions

| Layer | Path | Package |
|-------|------|---------|
| Domain | `test/domain/<entity>/` | `flutter_test` |
| Application | `test/features/<f>/application/` | `bloc_test`, `flutter_test` |
| Presentation | `test/features/<f>/presentation/` | `flutter_test` |

## Guidelines

- Unit-test mappers and value objects in domain.
- BLoC tests: use `bloc_test` with mocked `I*Repository`.
- Widget tests: pump widget with `BlocProvider` / `MultiBlocProvider`.
- Run `flutter test` before closing an epic.

Tests are created by the `test-writer` subagent after `integration-wiring`.
