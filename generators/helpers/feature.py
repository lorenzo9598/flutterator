"""Feature generation functions"""

from pathlib import Path
from typing import Optional, List
from generators.templates.copier import generate_file
from .utils import map_field_type, to_pascal_case, to_pascal_case_preserve


def create_feature_layers(feature_dir: Path, feature_name: str, field_list: list[dict], project_name: str, folder: Optional[str]) -> None:
    """Create all layers for a feature"""
    # Build the import path prefix
    if folder:
        import_prefix = f"{folder.replace('/', '/')}/{feature_name}"
    else:
        import_prefix = feature_name
    
    # Model layer
    model_dir = feature_dir / "model"
    model_dir.mkdir(exist_ok=True)

    # Create value objects and validators
    generate_value_objects_and_validators(import_prefix, field_list, model_dir, project_name)
    
    # Create entity (domain model)
    entity_fields = []
    for field in field_list:
        field_name = field['name']
        if field_name == 'id':
            entity_fields.append(f"  required UniqueId id,")
        else:
            entity_fields.append(f"  required {to_pascal_case_preserve(field_name)} {field_name},")
    
    entity_import = f"import 'package:{project_name}/{import_prefix}/model/value_objects.dart';"
    
    entity_fields_str = "\n".join(entity_fields)
    generate_file(project_name, model_dir, "feature/feature_entity_template.jinja", f"{feature_name}.dart", {
        "feature_name": feature_name, 
        "fields": entity_fields_str,
        "entity_import": entity_import
    })
    
    # Create failure
    generate_file(project_name, model_dir, "feature/feature_failure_template.jinja", f"{feature_name}_failure.dart", {"feature_name": feature_name})
    
    # Infrastructure layer
    infra_dir = feature_dir / "infrastructure"
    infra_dir.mkdir(exist_ok=True)
    
    # Create DTO
    dto_fields = ",\n".join([f"    required {map_field_type(field['type'])} {field['name']}" for field in field_list])
    generate_file(project_name, infra_dir, "feature/feature_dto_template.jinja", f"{feature_name}_dto.dart", {"feature_name": feature_name, "fields": dto_fields})
    
    # Create extensions for DTO-Domain conversions
    generate_extensions(feature_name, field_list, infra_dir, project_name, import_prefix)
    
    i_repo_import = f"""import 'package:{project_name}/{import_prefix}/model/{feature_name}.dart';
import 'package:{project_name}/{import_prefix}/model/{feature_name}_failure.dart';
"""
    
    # Create repository interface
    generate_file(project_name, model_dir, "feature/i_feature_repository_template.jinja", f"i_{feature_name}_repository.dart", {
        "feature_name": feature_name,
        "i_repo_import": i_repo_import
    })

    repo_import = f"""import 'package:{project_name}/{import_prefix}/infrastructure/{feature_name}_extensions.dart';
import 'package:{project_name}/{import_prefix}/model/{feature_name}.dart';
import 'package:{project_name}/{import_prefix}/infrastructure/{feature_name}_dto.dart';
import 'package:{project_name}/{import_prefix}/model/{feature_name}_failure.dart';
import 'package:{project_name}/{import_prefix}/model/i_{feature_name}_repository.dart';
"""
    
    # Create repository implementation
    generate_file(project_name, infra_dir, "feature/feature_repository_template.jinja", f"{feature_name}_repository.dart", {
        "feature_name": feature_name,
        "repo_import": repo_import
    })
    
    # Application layer
    app_dir = feature_dir / "application"
    app_dir.mkdir(exist_ok=True)
    
    # Create BLoC files
    generate_file(project_name, app_dir, "feature/feature_event_template.jinja", f"{feature_name}_event.dart", {"feature_name": feature_name})
    generate_file(project_name, app_dir, "feature/feature_state_template.jinja", f"{feature_name}_state.dart", {"feature_name": feature_name})
    generate_file(project_name, app_dir, "feature/feature_bloc_template.jinja", f"{feature_name}_bloc.dart", {
        "feature_name": feature_name,
        "feature_import_prefix": f"{project_name}/{import_prefix}"
    })

    # Presentation layer
    presentation_dir = feature_dir / "presentation"
    presentation_dir.mkdir(exist_ok=True)
    
    # Create page
    generate_file(project_name, presentation_dir, "feature/feature_page_template.jinja", f"{feature_name}_page.dart", {"feature_name": feature_name})


def generate_value_objects_and_validators(import_prefix: str, field_list: list[dict], model_dir: Path, project_name: str) -> None:
    """Generate consolidated value objects and validators"""
    # Generate value objects (base + specific ones)
    value_objects_content = generate_consolidated_value_objects(import_prefix, field_list, project_name)
    (model_dir / "value_objects.dart").write_text(value_objects_content)
    
    # Generate validators
    generate_value_validators(field_list, model_dir, project_name)


def generate_consolidated_value_objects(import_prefix: str, field_list: list[dict], project_name: str) -> str:
    """Generate consolidated value objects file"""
    # Base ValueObject class
    base_vo = f"""import 'package:dartz/dartz.dart';
import 'package:{project_name}/core/model/failures.dart';
import 'package:{project_name}/core/model/value_objects.dart';
import 'package:{project_name}/{import_prefix}/model/value_validators.dart';

"""
    
    # Specific Value Objects for each field (excluding 'id' since we have UniqueId)
    field_vos = []
    for field in field_list:
        field_name = field['name']
        # Skip 'id' field since we have UniqueId
        if field_name == 'id':
            continue
            
        field_type = map_field_type(field['type'])
        capitalized_name = to_pascal_case_preserve(field_name)
        
        field_vo = f"""
class {capitalized_name} extends ValueObject<{field_type}> {{
  @override
  final Either<ValueFailure<{field_type}>, {field_type}> value;

  factory {capitalized_name}({field_type} input) {{
    return {capitalized_name}._(validate{capitalized_name}(input));
  }}

  const {capitalized_name}._(this.value);
}}
"""
        field_vos.append(field_vo)
    
    return base_vo + "\n".join(field_vos)


def generate_value_validators(field_list: list[dict], model_dir: Path, project_name: str) -> None:
    """Generate value validators file using Jinja template"""
    # Pre-process field_list to add pascal_name field
    processed_field_list = []
    for field in field_list:
        field_dict = dict(field)  # Create a copy
        field_dict['pascal_name'] = to_pascal_case_preserve(field['name'])
        processed_field_list.append(field_dict)
    
    generate_file(project_name, model_dir, "feature/value_validators_template.jinja", "value_validators.dart", {
        "project_name": project_name,
        "field_list": processed_field_list
    })


def generate_extensions(feature_name: str, field_list: list[dict], infra_dir: Path, project_name: str, import_prefix: str) -> None:
    """Generate DTO-Domain conversion extensions"""
    
    # Generate toDto() method
    to_dto_fields = []
    for field in field_list:
        field_name = field['name']
        if field_name == 'id':
            to_dto_fields.append(f"      id: id.getOrCrash()")
        else:
            to_dto_fields.append(f"      {field_name}: {field_name}.getOrCrash()")
    
    # Generate fromDto() method
    from_dto_fields = []
    for field in field_list:
        field_name = field['name']
        if field_name == 'id':
            from_dto_fields.append(f"      id: UniqueId.fromUniqueString(id)")
        else:
            capitalized_name = to_pascal_case_preserve(field_name)
            from_dto_fields.append(f"      {field_name}: {capitalized_name}({field_name})")
    
    extension_content = f"""import 'package:{project_name}/core/model/value_objects.dart';
import 'package:{project_name}/{import_prefix}/model/{feature_name}.dart';
import 'package:{project_name}/{import_prefix}/model/value_objects.dart';
import 'package:{project_name}/{import_prefix}/infrastructure/{feature_name}_dto.dart';

extension {feature_name.capitalize()}DtoX on {feature_name.capitalize()}Dto {{
  {feature_name.capitalize()} toDomain() {{
    return {feature_name.capitalize()}(
{','.join(from_dto_fields)}
    );
  }}
}}

extension {feature_name.capitalize()}DomainX on {feature_name.capitalize()} {{
  {feature_name.capitalize()}Dto toDto() {{
    return {feature_name.capitalize()}Dto(
{','.join(to_dto_fields)}
    );
  }}
}}

"""
    (infra_dir / f"{feature_name}_extensions.dart").write_text(extension_content)


def find_domain_models(lib_path: Path, domain_folder: str) -> List[str]:
    """Find all available domain models in the domain folder.
    
    Scans lib/{domain_folder}/ directory for subdirectories that contain
    model/ folders with .dart entity files.
    
    Args:
        lib_path: Path to lib/ directory
        domain_folder: Name of domain folder (e.g., 'domain')
    
    Returns:
        List of model names (e.g., ['user', 'note', 'product'])
    """
    domain_path = lib_path / domain_folder
    
    if not domain_path.exists():
        return []
    
    models = []
    for item in domain_path.iterdir():
        if item.is_dir():
            model_dir = item / "model"
            if model_dir.exists() and model_dir.is_dir():
                # Check if there's an entity file (same name as directory)
                entity_file = model_dir / f"{item.name}.dart"
                if entity_file.exists():
                    models.append(item.name)
    
    return sorted(models)


def create_presentation_feature_layers(feature_dir: Path, feature_name: str, domain_model_name: str, domain_folder: str, project_name: str, folder: Optional[str]) -> None:
    """Create only application and presentation layers for a feature.
    
    This function creates a feature that uses an existing domain model.
    It does NOT create model or infrastructure layers - those should
    already exist in the domain folder.
    
    Args:
        feature_dir: Path to feature directory
        feature_name: Name of the feature
        domain_model_name: Name of the domain model to use
        domain_folder: Name of domain folder (e.g., 'domain')
        project_name: Name of the project
        folder: Optional folder path for the feature
    """
    # Build import paths
    if folder:
        feature_import_prefix = f"{folder.replace('/', '/')}/{feature_name}"
    else:
        feature_import_prefix = feature_name
    
    domain_import_prefix = f"{domain_folder}/{domain_model_name}"
    
    # Application layer
    app_dir = feature_dir / "application"
    app_dir.mkdir(exist_ok=True)
    
    # Get PascalCase names
    # Use to_pascal_case_preserve to handle camelCase names like "todoPage" -> "TodoPage"
    feature_pascal = to_pascal_case_preserve(feature_name)
    domain_model_pascal = to_pascal_case_preserve(domain_model_name)
    
    # Build Freezed mixin names correctly (e.g., _$TodoPageEvent)
    freezed_mixin_event = "_$" + feature_pascal + "Event"
    freezed_mixin_state = "_$" + feature_pascal + "State"
    
    # Create event file that uses domain model for item types
    event_content = f"""/*
 * BLoC events template for feature operations
 * Defines immutable events using Freezed that trigger BLoC actions:
 * - LoadRequested: Fetch all items
 * - CreateRequested: Create new item
 * - UpdateRequested: Update existing item
 * - DeleteRequested: Remove item by ID
 * 
 * Events represent user intentions and trigger state changes
 */

part of '{feature_name}_bloc.dart';

@freezed
abstract class {feature_pascal}Event with {freezed_mixin_event} {{
  const factory {feature_pascal}Event.loadRequested() = LoadRequested;
  const factory {feature_pascal}Event.createRequested({domain_model_pascal} item) = CreateRequested;
  const factory {feature_pascal}Event.updateRequested({domain_model_pascal} item) = UpdateRequested;
  const factory {feature_pascal}Event.deleteRequested(String id) = DeleteRequested;
}}
"""
    (app_dir / f"{feature_name}_event.dart").write_text(event_content)
    
    # Create state file that uses domain model for list types
    state_content = f"""/*
 * BLoC states template for feature UI representation
 * Defines immutable states using Freezed for different UI states:
 * - Initial: App just started, no data loaded
 * - Loading: Data is being fetched/processed
 * - Loaded: Data successfully retrieved with items list
 * - Error: Something went wrong with error message
 * 
 * States represent the current condition of the feature
 */

part of '{feature_name}_bloc.dart';

@freezed
abstract class {feature_pascal}State with {freezed_mixin_state} {{
  const factory {feature_pascal}State.initial() = Initial;
  const factory {feature_pascal}State.loading() = Loading;
  const factory {feature_pascal}State.loaded(List<{domain_model_pascal}> items) = Loaded;
  const factory {feature_pascal}State.error(String message) = Error;
}}
"""
    (app_dir / f"{feature_name}_state.dart").write_text(state_content)
    
    # Create BLoC that uses domain repository
    bloc_content = f"""import 'package:bloc/bloc.dart';
import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:injectable/injectable.dart';
import 'package:{project_name}/{domain_import_prefix}/model/{domain_model_name}.dart';
import 'package:{project_name}/{domain_import_prefix}/model/{domain_model_name}_failure.dart';
import 'package:{project_name}/{domain_import_prefix}/model/i_{domain_model_name}_repository.dart';

part '{feature_name}_bloc.freezed.dart';
part '{feature_name}_event.dart';
part '{feature_name}_state.dart';

@injectable
class {feature_pascal}Bloc extends Bloc<{feature_pascal}Event, {feature_pascal}State> {{
  final I{domain_model_pascal}Repository _repository;

  {feature_pascal}Bloc(this._repository) : super(const {feature_pascal}State.initial()) {{
    on<LoadRequested>(_onLoadRequested);
    on<CreateRequested>(_onCreateRequested);
    on<UpdateRequested>(_onUpdateRequested);
    on<DeleteRequested>(_onDeleteRequested);
  }}

  void _onLoadRequested(LoadRequested event, Emitter<{feature_pascal}State> emit) async {{
    emit(const {feature_pascal}State.loading());
    final result = await _repository.getAll();
    result.fold(
      ({domain_model_pascal}Failure failure) => emit({feature_pascal}State.error(failure.toString())),
      (items) => emit({feature_pascal}State.loaded(items)),
    );
  }}

  void _onCreateRequested(CreateRequested event, Emitter<{feature_pascal}State> emit) async {{
    emit(const {feature_pascal}State.loading());
    final result = await _repository.create(event.item);
    result.fold(
      ({domain_model_pascal}Failure failure) => emit({feature_pascal}State.error(failure.toString())),
      (_) async {{
        final itemsResult = await _repository.getAll();
        itemsResult.fold(
          ({domain_model_pascal}Failure failure) => emit({feature_pascal}State.error(failure.toString())),
          (items) => emit({feature_pascal}State.loaded(items)),
        );
      }},
    );
  }}

  void _onUpdateRequested(UpdateRequested event, Emitter<{feature_pascal}State> emit) async {{
    emit(const {feature_pascal}State.loading());
    final result = await _repository.update(event.item);
    result.fold(
      ({domain_model_pascal}Failure failure) => emit({feature_pascal}State.error(failure.toString())),
      (_) async {{
        final itemsResult = await _repository.getAll();
        itemsResult.fold(
          ({domain_model_pascal}Failure failure) => emit({feature_pascal}State.error(failure.toString())),
          (items) => emit({feature_pascal}State.loaded(items)),
        );
      }},
    );
  }}

  void _onDeleteRequested(DeleteRequested event, Emitter<{feature_pascal}State> emit) async {{
    emit(const {feature_pascal}State.loading());
    final result = await _repository.delete(event.id);
    result.fold(
      ({domain_model_pascal}Failure failure) => emit({feature_pascal}State.error(failure.toString())),
      (_) async {{
        final itemsResult = await _repository.getAll();
        itemsResult.fold(
          ({domain_model_pascal}Failure failure) => emit({feature_pascal}State.error(failure.toString())),
          (items) => emit({feature_pascal}State.loaded(items)),
        );
      }},
    );
  }}
}}
"""
    (app_dir / f"{feature_name}_bloc.dart").write_text(bloc_content)

    # Presentation layer
    presentation_dir = feature_dir / "presentation"
    presentation_dir.mkdir(exist_ok=True)
    
    # Create page
    generate_file(project_name, presentation_dir, "feature/feature_page_template.jinja", f"{feature_name}_page.dart", {
        "feature_name": feature_name
    })

