# Domain layer

## Structure

- `model/` — entity, failure, repository interface, value objects
- `infrastructure/` — DTO, `I*Service`, mock/remote services, service module, mapper, repository

## Mock vs remote

Per-entity switch in `lib/apis/common/data_source_config.dart`. Default: **mock**.

When adding entities manually:

1. Create full infrastructure including `mock_<entity>_service.dart` and `<entity>_service_module.dart`.
2. Add `assets/mock/<entity>.json` with 2–3 sample items.
3. Register in `DataSourceConfig.entities`.

See `docs/architecture/MOCK_AND_REMOTE_DATA.md`.

## Rules

- No UI or BLoC in domain.
- Repository interface in `model/`; implementation uses `I*Service`.
