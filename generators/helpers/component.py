"""Component generation functions"""

import re
from pathlib import Path
from typing import Optional, List
from generators.templates.copier import generate_file
from .utils import to_pascal_case, to_pascal_case_preserve


def create_component_form_layers(component_dir: Path, component_name: str, field_list: list[dict], project_name: str, folder: Optional[str], domain_model_name: Optional[str] = None, domain_folder: Optional[str] = None) -> None:
    """Create all layers for a form component
    
    Args:
        component_dir: Path to component directory
        component_name: Name of the component
        field_list: List of field dictionaries
        project_name: Name of the project
        folder: Optional folder path
        domain_model_name: Optional domain model name (if using domain model)
        domain_folder: Optional domain folder name
    """
    # Build the import path prefix
    if folder:
        import_prefix = f"{folder.replace('/', '/')}/{component_name}"
    else:
        import_prefix = component_name
    
    # Application layer
    app_dir = component_dir / "application"
    app_dir.mkdir(exist_ok=True)
    
    # Create form-specific BLoC files using templates
    generate_form_event_from_template(component_name, field_list, app_dir, project_name)
    generate_form_state_from_template(component_name, field_list, app_dir, project_name)
    generate_form_bloc_from_template(component_name, field_list, app_dir, project_name, domain_model_name, domain_folder)
    
    # Presentation layer
    presentation_dir = component_dir / "presentation"
    presentation_dir.mkdir(exist_ok=True)
    
    # Create component widget - pass field_list and domain info for form components
    generate_form_widget_from_template(component_name, field_list, presentation_dir, project_name, import_prefix)


def create_component_layers(component_dir: Path, component_name: str, project_name: str, folder: Optional[str], domain_model_name: Optional[str] = None, domain_folder: Optional[str] = None) -> None:
    """Create all layers for a component
    
    Args:
        component_dir: Path to component directory
        component_name: Name of the component
        project_name: Name of the project
        folder: Optional folder path
        domain_model_name: Optional domain model name (if using domain model)
        domain_folder: Optional domain folder name
    """
    # Build the import path prefix
    if folder:
        import_prefix = f"{folder.replace('/', '/')}/{component_name}"
    else:
        import_prefix = component_name
    
    # Application layer
    app_dir = component_dir / "application"
    app_dir.mkdir(exist_ok=True)
    
    # Determine import prefix for domain model
    if domain_model_name and domain_folder:
        domain_import_prefix = f"{domain_folder}/{domain_model_name}"
    else:
        domain_import_prefix = None
    
    # Get PascalCase names
    component_pascal = to_pascal_case_preserve(component_name)
    
    # Generate event and state files
    if domain_import_prefix:
        # When using domain model, generate event and state with domain model types
        domain_model_pascal = to_pascal_case_preserve(domain_model_name)
        
        # Build Freezed mixin names correctly
        freezed_mixin_event = "_$" + component_pascal + "Event"
        freezed_mixin_state = "_$" + component_pascal + "State"
        
        # Generate event file
        event_content = f"""part of '{component_name}_bloc.dart';

@freezed
abstract class {component_pascal}Event with {freezed_mixin_event} {{
  const factory {component_pascal}Event.loadRequested(String id) = LoadRequested;
  const factory {component_pascal}Event.deleteRequested(String id) = DeleteRequested;
}}
"""
        (app_dir / f"{component_name}_event.dart").write_text(event_content)
        
        # Generate state file with domain model type
        state_content = f"""part of '{component_name}_bloc.dart';

@freezed
abstract class {component_pascal}State with {freezed_mixin_state} {{
  const factory {component_pascal}State.initial() = Initial;
  const factory {component_pascal}State.loading() = Loading;
  const factory {component_pascal}State.loaded({domain_model_pascal} item) = Loaded;
  const factory {component_pascal}State.error(String message) = Error;
}}
"""
        (app_dir / f"{component_name}_state.dart").write_text(state_content)
    else:
        # Standard generation without domain model
        generate_file(project_name, app_dir, "component/component_event_template.jinja", f"{component_name}_event.dart", {"feature_name": component_name})
        generate_file(project_name, app_dir, "component/component_state_template.jinja", f"{component_name}_state.dart", {"feature_name": component_name})
    
    # Generate BLoC with domain model imports if provided
    if domain_import_prefix:
        bloc_content = f"""import 'package:bloc/bloc.dart';
import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:injectable/injectable.dart';
import 'package:{project_name}/{domain_import_prefix}/model/{domain_model_name}.dart';
import 'package:{project_name}/{domain_import_prefix}/model/{domain_model_name}_failure.dart';
import 'package:{project_name}/{domain_import_prefix}/model/i_{domain_model_name}_repository.dart';

part '{component_name}_bloc.freezed.dart';
part '{component_name}_event.dart';
part '{component_name}_state.dart';

@injectable
class {component_pascal}Bloc extends Bloc<{component_pascal}Event, {component_pascal}State> {{
  final I{domain_model_pascal}Repository _repository;

  {component_pascal}Bloc(this._repository) : super(const {component_pascal}State.initial()) {{
    on<LoadRequested>(_onLoadRequested);
    on<DeleteRequested>(_onDeleteRequested);
  }}

  void _onLoadRequested(LoadRequested event, Emitter<{component_pascal}State> emit) async {{
    emit(const {component_pascal}State.loading());
    final result = await _repository.getById(event.id);
    result.fold(
      ({domain_model_pascal}Failure failure) => emit({component_pascal}State.error(failure.toString())),
      (item) => emit({component_pascal}State.loaded(item)),
    );
  }}

  void _onDeleteRequested(DeleteRequested event, Emitter<{component_pascal}State> emit) async {{
    emit(const {component_pascal}State.loading());
    final result = await _repository.delete(event.id);
    result.fold(
      ({domain_model_pascal}Failure failure) => emit({component_pascal}State.error(failure.toString())),
      (_) => emit(const {component_pascal}State.initial()),
    );
  }}
}}
"""
        (app_dir / f"{component_name}_bloc.dart").write_text(bloc_content)
    else:
        generate_file(project_name, app_dir, "component/component_bloc_template.jinja", f"{component_name}_bloc.dart", {
            "feature_name": component_name,
            "feature_import_prefix": f"{project_name}/{import_prefix}"
        })
    
    # Presentation layer
    presentation_dir = component_dir / "presentation"
    presentation_dir.mkdir(exist_ok=True)
    
    # Create component widget
    generate_component_widget_from_template(component_name, presentation_dir, project_name, 'single', import_prefix)


def generate_form_widget_from_template(component_name: str, field_list: list[dict], presentation_dir: Path, project_name: str, import_prefix: str) -> None:
    """Generate form component widget file using Jinja template
    
    Args:
        component_name: Name of the component
        field_list: List of field dictionaries
        presentation_dir: Path to presentation directory
        project_name: Name of the project
        import_prefix: Import path prefix for the component
    """
    pascal_name = to_pascal_case(component_name)
    bloc_name = f"{pascal_name}FormBloc"
    state_name = f"{pascal_name}FormState"
    bloc_import = f"import 'package:{project_name}/{import_prefix}/application/{component_name}_form_bloc.dart';"
    
    # Add pascal_name and label to each field for template use
    processed_field_list = []
    for field in field_list:
        field_dict = dict(field)  # Create a copy
        field_dict['pascal_name'] = to_pascal_case_preserve(field['name'])
        # Generate label: convert snake_case to Title Case (e.g., "user_name" -> "User Name")
        field_name = field['name']
        field_dict['label'] = ' '.join(word.capitalize() for word in field_name.split('_'))
        processed_field_list.append(field_dict)
    
    generate_file(project_name, presentation_dir, "component/component_form_widget_template.jinja", f"{component_name}_component.dart", {
        "component_name": component_name,
        "pascal_name": pascal_name,
        "bloc_name": bloc_name,
        "state_name": state_name,
        "bloc_import": bloc_import,
        "field_list": processed_field_list
    })


def generate_component_widget_from_template(component_name: str, presentation_dir: Path, project_name: str, component_type: str, import_prefix: str) -> None:
    """Generate component widget file using Jinja template
    
    Args:
        component_name: Name of the component
        presentation_dir: Path to presentation directory
        project_name: Name of the project
        component_type: Type of component ('form', 'list', or 'single')
        import_prefix: Import path prefix for the component
    """
    pascal_name = to_pascal_case(component_name)
    
    if component_type == 'form':
        # Form components now use generate_form_widget_from_template
        # This should not be called for form components anymore
        raise ValueError("Use generate_form_widget_from_template for form components")
    elif component_type == 'list':
        # List component uses its own template
        generate_file(project_name, presentation_dir, "component/component_list_widget_template.jinja", f"{component_name}_component.dart", {
            "component_name": component_name,
            "component_import_prefix": import_prefix
        })
    else:  # single
        bloc_name = f"{pascal_name}Bloc"
        state_name = f"{pascal_name}State"
        bloc_import = f"import 'package:{project_name}/{import_prefix}/application/{component_name}_bloc.dart';"
        state_import = f"import 'package:{project_name}/{import_prefix}/application/{component_name}_state.dart';"
        generate_file(project_name, presentation_dir, "component/component_widget_template.jinja", f"{component_name}_component.dart", {
            "component_name": component_name,
            "pascal_name": pascal_name,
            "is_form": False,
            "bloc_name": bloc_name,
            "state_name": state_name,
            "bloc_import": bloc_import,
            "state_import": state_import
        })


def generate_form_event_from_template(component_name: str, field_list: list[dict], app_dir: Path, project_name: str) -> None:
    """Generate form event file using Jinja template"""
    pascal_name = to_pascal_case(component_name)
    
    # Generate field change events
    field_events = []
    for field in field_list:
        field_name = field['name']
        if field_name != 'id':  # Skip id field for form events
            capitalized_name = to_pascal_case_preserve(field_name)
            field_events.append(f"  const factory {pascal_name}FormEvent.{field_name}Changed(String {field_name}Str) = {capitalized_name}Changed;")
    
    field_events_str = "\n".join(field_events)
    
    generate_file(project_name, app_dir, "component/component_form_event_template.jinja", f"{component_name}_form_event.dart", {
        "component_name": component_name,
        "pascal_name": pascal_name,
        "field_events": field_events_str
    })


def generate_form_state_from_template(component_name: str, field_list: list[dict], app_dir: Path, project_name: str) -> None:
    """Generate form state file using Jinja template"""
    pascal_name = to_pascal_case(component_name)
    
    # Generate field declarations
    field_declarations = []
    for field in field_list:
        field_name = field['name']
        if field_name != 'id':  # Skip id field for form state
            capitalized_name = to_pascal_case_preserve(field_name)
            field_declarations.append(f"    required {capitalized_name} {field_name},")
    
    field_declarations_str = "\n".join(field_declarations)
    
    # Generate initial values
    initial_values = []
    for field in field_list:
        field_name = field['name']
        if field_name != 'id':  # Skip id field for initial values
            capitalized_name = to_pascal_case_preserve(field_name)
            initial_values.append(f"        {field_name}: {capitalized_name}(''),")
    
    initial_values_str = "\n".join(initial_values)
    
    generate_file(project_name, app_dir, "component/component_form_state_template.jinja", f"{component_name}_form_state.dart", {
        "component_name": component_name,
        "pascal_name": pascal_name,
        "field_declarations": field_declarations_str,
        "initial_values": initial_values_str
    })


def generate_form_bloc_from_template(component_name: str, field_list: list[dict], app_dir: Path, project_name: str, domain_model_name: Optional[str] = None, domain_folder: Optional[str] = None) -> None:
    """Generate form bloc file using Jinja template
    
    Args:
        component_name: Name of the component
        field_list: List of field dictionaries
        app_dir: Application directory path
        project_name: Name of the project
        domain_model_name: Optional domain model name
        domain_folder: Optional domain folder name
    """
    pascal_name = to_pascal_case(component_name)
    
    # Add pascal_name to each field for template use
    processed_field_list = []
    for field in field_list:
        field_dict = dict(field)  # Create a copy
        field_dict['pascal_name'] = to_pascal_case_preserve(field['name'])
        processed_field_list.append(field_dict)
    
    generate_file(project_name, app_dir, "component/component_form_bloc_template.jinja", f"{component_name}_form_bloc.dart", {
        "component_name": component_name,
        "pascal_name": pascal_name,
        "field_list": processed_field_list,
        "domain_model_name": domain_model_name,
        "domain_folder": domain_folder
    })


def get_model_fields_from_domain(lib_path: Path, domain_folder: str, model_name: str) -> List[dict]:
    """Extract field information from a domain model entity file.
    
    Reads the domain model entity file and parses field definitions
    to extract field names and types.
    
    Args:
        lib_path: Path to lib/ directory
        domain_folder: Name of domain folder (e.g., 'domain')
        model_name: Name of the domain model
    
    Returns:
        List of field dictionaries with 'name' and 'type' keys
        compatible with existing field_list format
    """
    entity_file = lib_path / domain_folder / model_name / "model" / f"{model_name}.dart"
    
    if not entity_file.exists():
        raise FileNotFoundError(f"Domain model entity file not found: {entity_file}")
    
    content = entity_file.read_text()
    
    # Find the factory constructor with fields
    # Pattern: const factory ModelName({ required Type field, ... })
    factory_pattern = r'const factory\s+\w+\(\{([^}]+)\}\)'
    match = re.search(factory_pattern, content, re.DOTALL)
    
    if not match:
        raise ValueError(f"Could not parse entity file: {entity_file}")
    
    fields_section = match.group(1)
    
    # Parse individual fields
    # Pattern: required Type field_name,
    field_pattern = r'required\s+(\w+)\s+(\w+),?'
    fields = []
    
    for field_match in re.finditer(field_pattern, fields_section):
        field_type = field_match.group(1)
        field_name = field_match.group(2)
        
        # Map ValueObject types back to basic types
        # This is a simplified mapping - in practice, you might want to
        # check value_objects.dart for more accurate mapping
        type_mapping = {
            'UniqueId': 'string',
            'StringSingleLine': 'string',
            'EmailAddress': 'string',
            'Password': 'string',
            'Title': 'string',
            'Description': 'string',
            'Name': 'string',
        }
        
        # Default to 'string' if not in mapping
        mapped_type = type_mapping.get(field_type, 'string')
        
        fields.append({
            'name': field_name,
            'type': mapped_type
        })
    
    return fields


def create_component_list_layers(component_dir: Path, component_name: str, project_name: str, folder: Optional[str], domain_model_name: Optional[str] = None, domain_folder: Optional[str] = None) -> None:
    """Create all layers for a list component.
    
    This function creates a component that shows a list of items with full CRUD operations.
    It riutilizes the logic from create_presentation_feature_layers but for components.
    
    Args:
        component_dir: Path to component directory
        component_name: Name of the component
        project_name: Name of the project
        folder: Optional folder path
        domain_model_name: Domain model name (required)
        domain_folder: Domain folder name (required)
    """
    if not domain_model_name or not domain_folder:
        raise ValueError("domain_model_name and domain_folder are required for list components")
    
    # Build import paths
    if folder:
        component_import_prefix = f"{folder.replace('/', '/')}/{component_name}"
    else:
        component_import_prefix = component_name
    
    domain_import_prefix = f"{domain_folder}/{domain_model_name}"
    
    # Application layer
    app_dir = component_dir / "application"
    app_dir.mkdir(exist_ok=True)
    
    # Get PascalCase names
    component_pascal = to_pascal_case_preserve(component_name)
    domain_model_pascal = to_pascal_case_preserve(domain_model_name)
    
    # Build Freezed mixin names correctly
    freezed_mixin_event = "_$" + component_pascal + "Event"
    freezed_mixin_state = "_$" + component_pascal + "State"
    
    # Create event file that uses domain model for item types (same as feature)
    event_content = f"""/*
 * BLoC events template for component list operations
 * Defines immutable events using Freezed that trigger BLoC actions:
 * - LoadRequested: Fetch all items
 * - CreateRequested: Create new item
 * - UpdateRequested: Update existing item
 * - DeleteRequested: Remove item by ID
 * 
 * Events represent user intentions and trigger state changes
 */

part of '{component_name}_bloc.dart';

@freezed
abstract class {component_pascal}Event with {freezed_mixin_event} {{
  const factory {component_pascal}Event.loadRequested() = LoadRequested;
  const factory {component_pascal}Event.createRequested({domain_model_pascal} item) = CreateRequested;
  const factory {component_pascal}Event.updateRequested({domain_model_pascal} item) = UpdateRequested;
  const factory {component_pascal}Event.deleteRequested(String id) = DeleteRequested;
}}
"""
    (app_dir / f"{component_name}_event.dart").write_text(event_content)
    
    # Create state file that uses domain model for list types (same as feature)
    state_content = f"""/*
 * BLoC states template for component list UI representation
 * Defines immutable states using Freezed for different UI states:
 * - Initial: App just started, no data loaded
 * - Loading: Data is being fetched/processed
 * - Loaded: Data successfully retrieved with items list
 * - Error: Something went wrong with error message
 * 
 * States represent the current condition of the component
 */

part of '{component_name}_bloc.dart';

@freezed
abstract class {component_pascal}State with {freezed_mixin_state} {{
  const factory {component_pascal}State.initial() = Initial;
  const factory {component_pascal}State.loading() = Loading;
  const factory {component_pascal}State.loaded(List<{domain_model_pascal}> items) = Loaded;
  const factory {component_pascal}State.error(String message) = Error;
}}
"""
    (app_dir / f"{component_name}_state.dart").write_text(state_content)
    
    # Create BLoC that uses domain repository (same as feature)
    bloc_content = f"""import 'package:bloc/bloc.dart';
import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:injectable/injectable.dart';
import 'package:{project_name}/{domain_import_prefix}/model/{domain_model_name}.dart';
import 'package:{project_name}/{domain_import_prefix}/model/{domain_model_name}_failure.dart';
import 'package:{project_name}/{domain_import_prefix}/model/i_{domain_model_name}_repository.dart';

part '{component_name}_bloc.freezed.dart';
part '{component_name}_event.dart';
part '{component_name}_state.dart';

@injectable
class {component_pascal}Bloc extends Bloc<{component_pascal}Event, {component_pascal}State> {{
  final I{domain_model_pascal}Repository _repository;

  {component_pascal}Bloc(this._repository) : super(const {component_pascal}State.initial()) {{
    on<LoadRequested>(_onLoadRequested);
    on<CreateRequested>(_onCreateRequested);
    on<UpdateRequested>(_onUpdateRequested);
    on<DeleteRequested>(_onDeleteRequested);
  }}

  void _onLoadRequested(LoadRequested event, Emitter<{component_pascal}State> emit) async {{
    emit(const {component_pascal}State.loading());
    final result = await _repository.getAll();
    result.fold(
      ({domain_model_pascal}Failure failure) => emit({component_pascal}State.error(failure.toString())),
      (items) => emit({component_pascal}State.loaded(items)),
    );
  }}

  void _onCreateRequested(CreateRequested event, Emitter<{component_pascal}State> emit) async {{
    emit(const {component_pascal}State.loading());
    final result = await _repository.create(event.item);
    result.fold(
      ({domain_model_pascal}Failure failure) => emit({component_pascal}State.error(failure.toString())),
      (_) async {{
        final itemsResult = await _repository.getAll();
        itemsResult.fold(
          ({domain_model_pascal}Failure failure) => emit({component_pascal}State.error(failure.toString())),
          (items) => emit({component_pascal}State.loaded(items)),
        );
      }},
    );
  }}

  void _onUpdateRequested(UpdateRequested event, Emitter<{component_pascal}State> emit) async {{
    emit(const {component_pascal}State.loading());
    final result = await _repository.update(event.item);
    result.fold(
      ({domain_model_pascal}Failure failure) => emit({component_pascal}State.error(failure.toString())),
      (_) async {{
        final itemsResult = await _repository.getAll();
        itemsResult.fold(
          ({domain_model_pascal}Failure failure) => emit({component_pascal}State.error(failure.toString())),
          (items) => emit({component_pascal}State.loaded(items)),
        );
      }},
    );
  }}

  void _onDeleteRequested(DeleteRequested event, Emitter<{component_pascal}State> emit) async {{
    emit(const {component_pascal}State.loading());
    final result = await _repository.delete(event.id);
    result.fold(
      ({domain_model_pascal}Failure failure) => emit({component_pascal}State.error(failure.toString())),
      (_) async {{
        final itemsResult = await _repository.getAll();
        itemsResult.fold(
          ({domain_model_pascal}Failure failure) => emit({component_pascal}State.error(failure.toString())),
          (items) => emit({component_pascal}State.loaded(items)),
        );
      }},
    );
  }}
}}
"""
    (app_dir / f"{component_name}_bloc.dart").write_text(bloc_content)
    
    # Presentation layer
    presentation_dir = component_dir / "presentation"
    presentation_dir.mkdir(exist_ok=True)
    
    # Create component widget using list template
    generate_file(project_name, presentation_dir, "component/component_list_widget_template.jinja", f"{component_name}_component.dart", {
        "component_name": component_name,
        "component_pascal": component_pascal,
        "component_import_prefix": component_import_prefix
    })

