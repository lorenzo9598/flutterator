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
    
    # Create component widget
    generate_component_widget_from_template(component_name, presentation_dir, project_name, True, import_prefix)


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
    
    # Create standard BLoC files
    generate_file(project_name, app_dir, "component/component_event_template.jinja", f"{component_name}_event.dart", {"feature_name": component_name})
    generate_file(project_name, app_dir, "component/component_state_template.jinja", f"{component_name}_state.dart", {"feature_name": component_name})
    
    # Generate BLoC with domain model imports if provided
    if domain_import_prefix:
        bloc_content = f"""import 'dart:async';

import 'package:bloc/bloc.dart';
import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:injectable/injectable.dart';
import 'package:{project_name}/{domain_import_prefix}/model/{domain_model_name}.dart';
import 'package:{project_name}/{domain_import_prefix}/model/{domain_model_name}_failure.dart';
import 'package:{project_name}/{domain_import_prefix}/model/i_{domain_model_name}_repository.dart';

part '{component_name}_bloc.freezed.dart';
part '{component_name}_event.dart';
part '{component_name}_state.dart';

@injectable
class {to_pascal_case(component_name)}Bloc extends Bloc<{to_pascal_case(component_name)}Event, {to_pascal_case(component_name)}State> {{
  final I{to_pascal_case(domain_model_name)}Repository _repository;

  {to_pascal_case(component_name)}Bloc(this._repository) : super(const {to_pascal_case(component_name)}State.initial()) {{
    on<LoadRequested>(_onLoadRequested);
    on<DeleteRequested>(_onDeleteRequested);
  }}

  void _onLoadRequested(LoadRequested event, Emitter<{to_pascal_case(component_name)}State> emit) async {{
    emit(const {to_pascal_case(component_name)}State.loading());
    final result = await _repository.getAll();
    result.fold(
      (failure) => emit({to_pascal_case(component_name)}State.error(failure.toString())),
      (items) => emit({to_pascal_case(component_name)}State.loaded(items)),
    );
  }}

  void _onDeleteRequested(DeleteRequested event, Emitter<{to_pascal_case(component_name)}State> emit) async {{
    emit(const {to_pascal_case(component_name)}State.loading());
    final result = await _repository.delete(event.id);
    result.fold(
      (failure) => emit({to_pascal_case(component_name)}State.error(failure.toString())),
      (_) async {{
        final itemsResult = await _repository.getAll();
        itemsResult.fold(
          (failure) => emit({to_pascal_case(component_name)}State.error(failure.toString())),
          (items) => emit({to_pascal_case(component_name)}State.loaded(items)),
        );
      }},
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
    generate_component_widget_from_template(component_name, presentation_dir, project_name, False, import_prefix)


def generate_component_widget_from_template(component_name: str, presentation_dir: Path, project_name: str, is_form: bool, import_prefix: str) -> None:
    """Generate component widget file using Jinja template"""
    pascal_name = to_pascal_case(component_name)
    
    if is_form:
        bloc_name = f"{pascal_name}FormBloc"
        state_name = f"{pascal_name}FormState"
        bloc_import = f"import 'package:{project_name}/{import_prefix}/application/{component_name}_form_bloc.dart';"
        state_import = f"import 'package:{project_name}/{import_prefix}/application/{component_name}_form_state.dart';"
    else:
        bloc_name = f"{pascal_name}Bloc"
        state_name = f"{pascal_name}State"
        bloc_import = f"import 'package:{project_name}/{import_prefix}/application/{component_name}_bloc.dart';"
        state_import = f"import 'package:{project_name}/{import_prefix}/application/{component_name}_state.dart';"
    
    generate_file(project_name, presentation_dir, "component/component_widget_template.jinja", f"{component_name}_component.dart", {
        "component_name": component_name,
        "pascal_name": pascal_name,
        "is_form": is_form,
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
    
    # If using domain model, we still use the template but note that
    # the form bloc will work with the domain model fields
    generate_file(project_name, app_dir, "component/component_form_bloc_template.jinja", f"{component_name}_form_bloc.dart", {
        "component_name": component_name,
        "pascal_name": pascal_name,
        "field_list": field_list,
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

