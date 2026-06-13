# Domain layer

Shared business entities under `lib/domain/<entity>/`.

## Structure

- `model/` — entity, failure, repository interface, value objects
- `infrastructure/` — DTO, API service, mapper, repository implementation

## Rules

- No UI, no BLoC, no Flutter imports in domain logic.
- Enums live in `lib/domain/enums/`.
- Update `lib/core/errors/error_localizer.dart` when adding failures.

See `docs/architecture/DDD_LAYERS.md` and `FILE_TEMPLATES.md`.
