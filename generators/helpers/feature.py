"""Feature generation functions"""

import re
from pathlib import Path
from typing import Optional, List, Dict
from generators.templates.copier import generate_file
from .utils import map_field_type, map_field_type_to_dto, to_pascal_case, to_pascal_case_preserve


def create_feature_layers(feature_dir: Path, feature_name: str, field_list: list[dict], project_name: str, folder: Optional[str], lib_path: Optional[Path] = None, domain_folder: str = "domain") -> None:
    """Create all layers for a feature"""
    # Build the import path prefix
    if folder:
        import_prefix = f"{folder.replace('/', '/')}/{feature_name}"
    else:
        import_prefix = feature_name
    
    # Discover enums for enum-aware generation
    known_enums: set = set()
    enums_info: Dict[str, dict] = {}
    _lib = lib_path or (feature_dir.parent.parent if feature_dir.parent.exists() else None)
    if _lib and (_lib / domain_folder / "enums").exists():
        enums_info = find_enums_with_info(_lib, domain_folder)
        known_enums = set(enums_info.keys())
    
    # Model layer
    model_dir = feature_dir / "model"
    model_dir.mkdir(exist_ok=True)

    # Create value objects and validators
    generate_value_objects_and_validators(import_prefix, field_list, model_dir, project_name, known_enums=known_enums)
    
    # Create entity (domain model)
    entity_fields = []
    enum_imports = []
    for field in field_list:
        field_name = field['name']
        field_type = field['type']
        base_ft = field_type[:-1] if field_type.endswith('?') else field_type
        if field_name == 'id':
            entity_fields.append(f"  required UniqueId id,")
        elif base_ft in known_enums:
            entity_fields.append(f"  required {field_type} {field_name},")
            info = enums_info.get(base_ft)
            if info:
                ei = f"import 'package:{project_name}/{info['folder']}/{info['file_stem']}.dart';"
                if ei not in enum_imports:
                    enum_imports.append(ei)
        else:
            entity_fields.append(f"  required {to_pascal_case_preserve(field_name)} {field_name},")
    
    entity_import = f"import 'package:{project_name}/{import_prefix}/model/value_objects.dart';"
    if enum_imports:
        entity_import = entity_import + "\n" + "\n".join(enum_imports)
    
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
    
    # Create DTO (enum -> String in DTO)
    dto_fields = ",\n".join([f"    required {map_field_type_to_dto(field['type'], known_enums=known_enums) if known_enums else map_field_type(field['type'])} {field['name']}" for field in field_list])
    generate_file(project_name, infra_dir, "feature/feature_dto_template.jinja", f"{feature_name}_dto.dart", {"feature_name": feature_name, "fields": dto_fields})
    
    # Create extensions for DTO-Domain conversions
    generate_extensions(feature_name, field_list, infra_dir, project_name, import_prefix, known_enums=known_enums, enums_info=enums_info)
    
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
    generate_file(project_name, presentation_dir, "feature/feature_page_template.jinja", f"{feature_name}_page.dart", {
        "feature_name": feature_name,
        "model_import_prefix": f"{project_name}/{import_prefix}",
        "model_file_stem": feature_name,
        "model_class_pascal": to_pascal_case_preserve(feature_name),
    })


def generate_value_objects_and_validators(import_prefix: str, field_list: list[dict], model_dir: Path, project_name: str, known_enums: Optional[set] = None, skip_local_validators: bool = False) -> None:
    """Generate consolidated value objects and optionally validators.

    When skip_local_validators is True (e.g. for domain entities), value_validators.dart
    is not generated; value_objects use right(input) with a TODO pointing to core validators.
    """
    value_objects_content = generate_consolidated_value_objects(
        import_prefix, field_list, project_name,
        known_enums=known_enums,
        use_placeholder_validation=skip_local_validators,
    )
    (model_dir / "value_objects.dart").write_text(value_objects_content)

    if not skip_local_validators:
        generate_value_validators(field_list, model_dir, project_name, known_enums=known_enums)


def generate_consolidated_value_objects(import_prefix: str, field_list: list[dict], project_name: str, known_enums: Optional[set] = None, use_placeholder_validation: bool = False) -> str:
    """Generate consolidated value objects file.

    When use_placeholder_validation is True, value_objects do not import local
    value_validators; each factory uses right(input) with a TODO to core validators.
    """
    imports = f"import 'package:dartz/dartz.dart';\n"
    imports += f"import 'package:{project_name}/core/model/failures.dart';\n"
    imports += f"import 'package:{project_name}/core/model/value_objects.dart';\n"
    if not use_placeholder_validation:
        imports += f"import 'package:{project_name}/{import_prefix}/model/value_validators.dart';\n"
    imports += "\n"

    _enums = known_enums or set()

    field_vos = []
    for field in field_list:
        field_name = field['name']
        field_type = field['type']

        if field_name == 'id':
            continue

        base_ft = field_type[:-1] if field_type.endswith('?') else field_type

        if base_ft in _enums:
            continue

        if '<' in base_ft or (base_ft and base_ft[0].isupper() and base_ft not in ['String', 'DateTime']):
            continue

        mapped_field_type = map_field_type(base_ft)
        capitalized_name = to_pascal_case_preserve(field_name)

        if use_placeholder_validation:
            factory_body = (
                f"    // TODO: Validate input here. See core/model/value_validators.dart for examples.\n"
                f"    return {capitalized_name}._(right(input));"
            )
        else:
            factory_body = f"    return {capitalized_name}._(validate{capitalized_name}(input));"

        field_vo = f"""
class {capitalized_name} extends ValueObject<{mapped_field_type}> {{
  @override
  final Either<ValueFailure<{mapped_field_type}>, {mapped_field_type}> value;

  factory {capitalized_name}({mapped_field_type} input) {{
{factory_body}
  }}

  const {capitalized_name}._(this.value);
}}
"""
        field_vos.append(field_vo)

    return imports + "\n".join(field_vos)


def generate_value_validators(field_list: list[dict], model_dir: Path, project_name: str, known_enums: Optional[set] = None) -> None:
    """Generate value validators file using Jinja template"""
    _enums = known_enums or set()
    # Pre-process field_list: add pascal_name and strip nullable suffix so
    # the template matches base types (e.g., String not String?)
    processed_field_list = []
    for field in field_list:
        base_ft = field['type'][:-1] if field['type'].endswith('?') else field['type']
        # Skip enums — they don't need validators
        if base_ft in _enums:
            continue
        field_dict = dict(field)  # Create a copy
        field_dict['pascal_name'] = to_pascal_case_preserve(field['name'])
        if field_dict['type'].endswith('?'):
            field_dict['type'] = field_dict['type'][:-1]
        processed_field_list.append(field_dict)
    
    generate_file(project_name, model_dir, "feature/value_validators_template.jinja", "value_validators.dart", {
        "project_name": project_name,
        "field_list": processed_field_list
    })


def generate_extensions(feature_name: str, field_list: list[dict], infra_dir: Path, project_name: str, import_prefix: str, known_enums: Optional[set] = None, enums_info: Optional[Dict[str, dict]] = None) -> None:
    """Generate DTO-Domain conversion extensions"""
    _enums = known_enums or set()
    _enums_info = enums_info or {}
    
    # Generate toDto() method
    to_dto_fields = []
    for field in field_list:
        field_name = field['name']
        field_type = field['type']
        base_ft = field_type[:-1] if field_type.endswith('?') else field_type
        if field_name == 'id':
            to_dto_fields.append(f"      id: id.getOrCrash()")
        elif base_ft in _enums:
            to_dto_fields.append(f"      {field_name}: {field_name}.name")
        else:
            to_dto_fields.append(f"      {field_name}: {field_name}.getOrCrash()")
    
    # Generate fromDto() method
    from_dto_fields = []
    for field in field_list:
        field_name = field['name']
        field_type = field['type']
        base_ft = field_type[:-1] if field_type.endswith('?') else field_type
        if field_name == 'id':
            from_dto_fields.append(f"      id: UniqueId.fromUniqueString(id)")
        elif base_ft in _enums:
            from_dto_fields.append(f"      {field_name}: {base_ft}.values.byName({field_name})")
        else:
            capitalized_name = to_pascal_case_preserve(field_name)
            from_dto_fields.append(f"      {field_name}: {capitalized_name}({field_name})")
    
    # Build enum imports for extensions
    enum_ext_imports = []
    for field in field_list:
        ft = field['type']
        base_ft = ft[:-1] if ft.endswith('?') else ft
        if base_ft in _enums:
            info = _enums_info.get(base_ft)
            if info:
                ei = f"import 'package:{project_name}/{info['folder']}/{info['file_stem']}.dart';"
                if ei not in enum_ext_imports:
                    enum_ext_imports.append(ei)
    
    extra_imports = "\n".join(enum_ext_imports)
    if extra_imports:
        extra_imports = "\n" + extra_imports
    
    extension_content = f"""import 'package:{project_name}/core/model/value_objects.dart';
import 'package:{project_name}/{import_prefix}/model/{feature_name}.dart';
import 'package:{project_name}/{import_prefix}/model/value_objects.dart';
import 'package:{project_name}/{import_prefix}/infrastructure/{feature_name}_dto.dart';{extra_imports}

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


def _is_entity_file(file_path: Path) -> bool:
    """Check if a .dart file contains a freezed entity class definition.
    
    Excludes failure files, interfaces, value objects, validators,
    and generated files (.freezed.dart, .g.dart).
    """
    name = file_path.name
    if name.endswith('.freezed.dart') or name.endswith('.g.dart'):
        return False
    if name.startswith('i_') or name.endswith('_failure.dart'):
        return False
    if name in ('value_objects.dart', 'value_validators.dart', 'common_interfaces.dart'):
        return False
    
    try:
        content = file_path.read_text()
        return bool(re.search(r'abstract class (\w+)\s+with\s+_\$', content))
    except Exception:
        return False


def _get_class_name_from_file(file_path: Path) -> Optional[str]:
    """Extract the freezed class name from a .dart entity file."""
    try:
        content = file_path.read_text()
        match = re.search(r'abstract class (\w+)\s+with', content)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None


def find_domain_models(lib_path: Path, domain_folder: str) -> List[str]:
    """Find all available domain models in the domain folder.
    
    Scans lib/{domain_folder}/ subdirectories for model/ folders containing
    entity .dart files. Discovers entities even when the file name differs
    from the containing folder (e.g., user_profile.dart inside auth/).
    
    Args:
        lib_path: Path to lib/ directory
        domain_folder: Name of domain folder (e.g., 'domain')
    
    Returns:
        List of model file stems (e.g., ['test', 'user_profile'])
    """
    models_map = find_domain_models_with_class_names(lib_path, domain_folder)
    return sorted(models_map.keys())


def get_domain_model_class_name(lib_path: Path, domain_folder: str, folder_name: str) -> Optional[str]:
    """Get the class name (PascalCase) from a domain model entity file.
    
    First checks for an entity file matching folder_name, then scans
    all entity files in the folder's model/ directory.
    
    Args:
        lib_path: Path to lib/ directory
        domain_folder: Name of domain folder (e.g., 'domain')
        folder_name: Folder name or file stem of the model (snake_case)
    
    Returns:
        Class name in PascalCase (e.g., 'TodoItem') or None if not found
    """
    domain_path = lib_path / domain_folder
    
    # Try exact match first: folder_name is the file stem
    for item in domain_path.iterdir():
        if item.is_dir():
            candidate = item / "model" / f"{folder_name}.dart"
            if candidate.exists():
                return _get_class_name_from_file(candidate)
    
    return None


def find_domain_models_with_class_names(lib_path: Path, domain_folder: str) -> Dict[str, dict]:
    """Find all available domain models with their class names and folder info.
    
    Scans all model/ subdirectories for entity files, including entities
    whose file name differs from the containing folder.
    
    Args:
        lib_path: Path to lib/ directory
        domain_folder: Name of domain folder (e.g., 'domain')
    
    Returns:
        Dictionary mapping file stems to model info dicts:
        {
            'test': {'class_name': 'Test', 'folder': 'test'},
            'user_profile': {'class_name': 'UserProfile', 'folder': 'auth'},
        }
    """
    domain_path = lib_path / domain_folder
    
    if not domain_path.exists():
        return {}
    
    models_map = {}
    for item in domain_path.iterdir():
        if item.is_dir():
            model_dir = item / "model"
            if not (model_dir.exists() and model_dir.is_dir()):
                continue
            for dart_file in model_dir.iterdir():
                if dart_file.suffix == '.dart' and _is_entity_file(dart_file):
                    class_name = _get_class_name_from_file(dart_file)
                    if class_name:
                        file_stem = dart_file.stem
                        models_map[file_stem] = {
                            'class_name': class_name,
                            'folder': item.name,
                        }
    
    return models_map


def find_enums(lib_path: Path, domain_folder: str) -> List[str]:
    """Find all available enum names in lib/<domain_folder>/enums/.

    Args:
        lib_path: Path to lib/ directory
        domain_folder: Name of domain folder (e.g., 'domain')

    Returns:
        Sorted list of enum names (PascalCase, e.g., ['EventStatus', 'Priority'])
    """
    enums_info = find_enums_with_info(lib_path, domain_folder)
    return sorted(enums_info.keys())


def find_enums_with_info(lib_path: Path, domain_folder: str) -> Dict[str, dict]:
    """Find all enums with their file stems and folder info.

    Scans lib/<domain_folder>/enums/ for .dart files containing ``enum Name {``.

    Args:
        lib_path: Path to lib/ directory
        domain_folder: Name of domain folder (e.g., 'domain')

    Returns:
        Dictionary mapping enum name to info dict::

            {
                'EventStatus': {
                    'file_stem': 'event_status',
                    'folder': 'domain/enums',
                },
            }
    """
    enums_dir = lib_path / domain_folder / "enums"

    if not enums_dir.exists():
        return {}

    enums_map: Dict[str, dict] = {}
    for dart_file in enums_dir.iterdir():
        if dart_file.suffix != '.dart':
            continue
        try:
            content = dart_file.read_text()
        except Exception:
            continue
        for match in re.finditer(r'enum\s+(\w+)\s*\{', content):
            enum_name = match.group(1)
            enums_map[enum_name] = {
                'file_stem': dart_file.stem,
                'folder': f"{domain_folder}/enums",
            }

    return enums_map


def create_presentation_feature_layers(feature_dir: Path, feature_name: str, domain_model_name: str, domain_folder: str, project_name: str, folder: Optional[str], domain_model_folder: Optional[str] = None) -> None:
    """Create only application and presentation layers for a feature.
    
    This function creates a feature that uses an existing domain model.
    It does NOT create model or infrastructure layers - those should
    already exist in the domain folder.
    
    Args:
        feature_dir: Path to feature directory
        feature_name: Name of the feature
        domain_model_name: Name of the domain model to use (file stem)
        domain_folder: Name of domain folder (e.g., 'domain')
        project_name: Name of the project
        folder: Optional folder path for the feature
        domain_model_folder: Containing folder for the model. Defaults to domain_model_name.
    """
    if domain_model_folder is None:
        domain_model_folder = domain_model_name
    
    # Build import paths
    if folder:
        feature_import_prefix = f"{folder.replace('/', '/')}/{feature_name}"
    else:
        feature_import_prefix = feature_name
    
    domain_import_prefix = f"{domain_folder}/{domain_model_folder}"
    
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
import 'package:dartz/dartz.dart';
import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:injectable/injectable.dart';
import 'package:{project_name}/{domain_import_prefix}/model/{domain_model_name}.dart';
import 'package:{project_name}/{domain_import_prefix}/model/{domain_model_name}_failure.dart';
import 'package:{project_name}/{domain_import_prefix}/model/i_{domain_model_name}_repository.dart';

part '{feature_name}_bloc.freezed.dart';
part '{feature_name}_event.dart';
part '{feature_name}_state.dart';

class {feature_pascal}Bloc extends Bloc<{feature_pascal}Event, {feature_pascal}State> {{
  final I{domain_model_pascal}Repository _repository;

  {feature_pascal}Bloc(this._repository) : super(const {feature_pascal}State.initial()) {{
    on<LoadRequested>(_onLoadRequested);
    on<CreateRequested>(_onCreateRequested);
    on<UpdateRequested>(_onUpdateRequested);
    on<DeleteRequested>(_onDeleteRequested);
  }}

  Future<void> _onLoadRequested(LoadRequested event, Emitter<{feature_pascal}State> emit) async {{
    emit(const {feature_pascal}State.loading());
    final Either<{domain_model_pascal}Failure, List<{domain_model_pascal}>> result =
        await _repository.getAll();
    result.fold(
      ({domain_model_pascal}Failure failure) => emit({feature_pascal}State.error(failure.toString())),
      (List<{domain_model_pascal}> items) => emit({feature_pascal}State.loaded(items)),
    );
  }}

  Future<void> _onCreateRequested(CreateRequested event, Emitter<{feature_pascal}State> emit) async {{
    emit(const {feature_pascal}State.loading());
    final Either<{domain_model_pascal}Failure, Unit> result = await _repository.create(event.item);
    result.fold(
      ({domain_model_pascal}Failure failure) => emit({feature_pascal}State.error(failure.toString())),
      (Unit _) async {{
        final Either<{domain_model_pascal}Failure, List<{domain_model_pascal}>> itemsResult =
            await _repository.getAll();
        itemsResult.fold(
          ({domain_model_pascal}Failure failure) => emit({feature_pascal}State.error(failure.toString())),
          (List<{domain_model_pascal}> items) => emit({feature_pascal}State.loaded(items)),
        );
      }},
    );
  }}

  Future<void> _onUpdateRequested(UpdateRequested event, Emitter<{feature_pascal}State> emit) async {{
    emit(const {feature_pascal}State.loading());
    final Either<{domain_model_pascal}Failure, Unit> result = await _repository.update(event.item);
    result.fold(
      ({domain_model_pascal}Failure failure) => emit({feature_pascal}State.error(failure.toString())),
      (Unit _) async {{
        final Either<{domain_model_pascal}Failure, List<{domain_model_pascal}>> itemsResult =
            await _repository.getAll();
        itemsResult.fold(
          ({domain_model_pascal}Failure failure) => emit({feature_pascal}State.error(failure.toString())),
          (List<{domain_model_pascal}> items) => emit({feature_pascal}State.loaded(items)),
        );
      }},
    );
  }}

  Future<void> _onDeleteRequested(DeleteRequested event, Emitter<{feature_pascal}State> emit) async {{
    emit(const {feature_pascal}State.loading());
    final Either<{domain_model_pascal}Failure, Unit> result = await _repository.delete(event.id);
    result.fold(
      ({domain_model_pascal}Failure failure) => emit({feature_pascal}State.error(failure.toString())),
      (Unit _) async {{
        final Either<{domain_model_pascal}Failure, List<{domain_model_pascal}>> itemsResult =
            await _repository.getAll();
        itemsResult.fold(
          ({domain_model_pascal}Failure failure) => emit({feature_pascal}State.error(failure.toString())),
          (List<{domain_model_pascal}> items) => emit({feature_pascal}State.loaded(items)),
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
        "feature_name": feature_name,
        "model_import_prefix": f"{project_name}/{domain_import_prefix}",
        "model_file_stem": domain_model_name,
        "model_class_pascal": domain_model_pascal,
    })

