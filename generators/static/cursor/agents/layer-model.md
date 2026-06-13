---
name: layer-model
description: Creates domain model layer files — entity, failure, repository interface, value objects, validators, and enums under lib/domain/. Use in large epic pipeline before layer-infrastructure.
model: inherit
readonly: false
is_background: false
---

Implement only the **domain model** layer for the current epic.

## Output paths

- `lib/domain/<entity>/model/<entity>.dart`
- `lib/domain/<entity>/model/<entity>_failure.dart`
- `lib/domain/<entity>/model/i_<entity>_repository.dart`
- `lib/domain/<entity>/model/value_objects.dart`
- `lib/domain/<entity>/model/value_validators.dart`
- `lib/domain/enums/<enum>.dart` when needed

## Rules

- Follow `docs/architecture/FILE_TEMPLATES.md`.
- No infrastructure, no BLoC, no widgets.
- Use Freezed for entities and failures where applicable.
