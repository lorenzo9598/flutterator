"""Component generation functions"""

from pathlib import Path
from typing import Optional
from generators.templates.copier import generate_file
from .utils import to_pascal_case


def create_component_form_layers(component_dir: Path, component_name: str, field_list: list[dict], project_name: str, folder: Optional[str]) -> None:
    """Create all layers for a form component"""
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
    generate_form_bloc_from_template(component_name, field_list, app_dir, project_name)
    
    # Presentation layer
    presentation_dir = component_dir / "presentation"
    presentation_dir.mkdir(exist_ok=True)
    
    # Create component widget
    generate_component_widget_from_template(component_name, presentation_dir, project_name, True, import_prefix)


def create_component_layers(component_dir: Path, component_name: str, project_name: str, folder: Optional[str]) -> None:
    """Create all layers for a component"""
    # Build the import path prefix
    if folder:
        import_prefix = f"{folder.replace('/', '/')}/{component_name}"
    else:
        import_prefix = component_name
    
    # Application layer
    app_dir = component_dir / "application"
    app_dir.mkdir(exist_ok=True)
    
    # Create standard BLoC files
    generate_file(project_name, app_dir, "component/component_event_template.jinja", f"{component_name}_event.dart", {"feature_name": component_name})
    generate_file(project_name, app_dir, "component/component_state_template.jinja", f"{component_name}_state.dart", {"feature_name": component_name})
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
            capitalized_name = field_name.capitalize()
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
            capitalized_name = field_name.capitalize()
            field_declarations.append(f"    required {capitalized_name} {field_name},")
    
    field_declarations_str = "\n".join(field_declarations)
    
    # Generate initial values
    initial_values = []
    for field in field_list:
        field_name = field['name']
        if field_name != 'id':  # Skip id field for initial values
            capitalized_name = field_name.capitalize()
            initial_values.append(f"        {field_name}: {capitalized_name}(''),")
    
    initial_values_str = "\n".join(initial_values)
    
    generate_file(project_name, app_dir, "component/component_form_state_template.jinja", f"{component_name}_form_state.dart", {
        "component_name": component_name,
        "pascal_name": pascal_name,
        "field_declarations": field_declarations_str,
        "initial_values": initial_values_str
    })


def generate_form_bloc_from_template(component_name: str, field_list: list[dict], app_dir: Path, project_name: str) -> None:
    """Generate form bloc file using Jinja template"""
    pascal_name = to_pascal_case(component_name)
    
    generate_file(project_name, app_dir, "component/component_form_bloc_template.jinja", f"{component_name}_form_bloc.dart", {
        "component_name": component_name,
        "pascal_name": pascal_name,
        "field_list": field_list
    })

