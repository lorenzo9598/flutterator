---
name: layer-infrastructure
description: Creates domain infrastructure — DTO, service interface, mock/remote services, mapper, repository implementation. Runs after layer-model in large epic pipeline.
model: inherit
readonly: false
is_background: false
---

Implement only the **domain infrastructure** layer for the current epic.

Read `docs/architecture/MOCK_AND_REMOTE_DATA.md` first.

## Output paths

- `lib/domain/<entity>/infrastructure/<entity>_dto.dart`
- `lib/domain/<entity>/infrastructure/i_<entity>_service.dart`
- `lib/domain/<entity>/infrastructure/<entity>_remote_service.dart`
- `lib/domain/<entity>/infrastructure/mock_<entity>_service.dart`
- `lib/domain/<entity>/infrastructure/<entity>_service_module.dart`
- `lib/domain/<entity>/infrastructure/<entity>_mapper.dart`
- `lib/domain/<entity>/infrastructure/<entity>_repository.dart`
- `assets/mock/<entity>.json` — **required** seed data

## Rules

- Implement interfaces from `model/i_<entity>_repository.dart`.
- Repository injects `I<Entity>Service` only.
- Mock service reads `assets/mock/<entity>.json`; create/update JSON with 2–3 realistic rows matching the DTO.
- Register entity in `DataSourceConfig.entities` as `DataSource.mock` unless remote is explicitly required.
- Use `@injectable` on repository implementation.
- Run after model layer exists. Do not create presentation or BLoC files.
