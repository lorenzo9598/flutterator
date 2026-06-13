---
name: layer-infrastructure
description: Creates domain infrastructure — DTO, Retrofit service, mapper, repository implementation. Runs after layer-model in large epic pipeline.
model: inherit
readonly: false
is_background: false
---

Implement only the **domain infrastructure** layer for the current epic.

## Output paths

- `lib/domain/<entity>/infrastructure/<entity>_dto.dart`
- `lib/domain/<entity>/infrastructure/<entity>_service.dart`
- `lib/domain/<entity>/infrastructure/<entity>_mapper.dart`
- `lib/domain/<entity>/infrastructure/<entity>_repository.dart`

## Rules

- Implement interfaces from `model/i_<entity>_repository.dart`.
- Use `@injectable` on repository implementation.
- Run after model layer exists. Do not create presentation or BLoC files.
