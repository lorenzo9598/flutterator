"""Component generation functions"""

import re
from pathlib import Path
from typing import Optional, List, Dict
from generators.templates.copier import generate_file
from generators.templates._core.core_generator import ensure_common_widgets
from .utils import to_pascal_case, to_pascal_case_preserve, map_field_type, get_form_field_metadata, PRIMITIVE_TYPES


def infer_lib_path(component_dir: Path) -> Path:
    """Resolve ``lib/`` from a directory inside the Flutter project (e.g. a component folder)."""
    current = component_dir.resolve()
    for parent in [current, *current.parents]:
        pub = parent / "pubspec.yaml"
        if pub.is_file():
            lib = parent / "lib"
            if lib.is_dir():
                return lib
    return current.parent


def get_repository_info(lib_path: Path, domain_folder: str, model_name: str, model_folder: Optional[str] = None) -> Dict:
    """Extract failure type and available methods from a repository interface.
    
    Reads i_{model_name}_repository.dart and parses:
    - The failure class name from Either<FailureType, ...>
    - The failure import path
    - Which CRUD methods are available
    
    Returns:
        Dict with keys: failure_class, failure_import, methods (set of method names)
        Falls back to {ModelName}Failure conventions if parsing fails.
    """
    if model_folder is None:
        model_folder = model_name
    
    repo_file = lib_path / domain_folder / model_folder / "model" / f"i_{model_name}_repository.dart"
    
    model_pascal = to_pascal_case_preserve(model_name)
    fallback = {
        'failure_class': f"{model_pascal}Failure",
        'failure_import': f"package:{Path(domain_folder) / model_folder / 'model' / f'{model_name}_failure.dart'}",
        'methods': {'getAll', 'getById', 'create', 'update', 'delete'},
    }
    
    if not repo_file.exists():
        return fallback
    
    try:
        content = repo_file.read_text()
    except Exception:
        return fallback
    
    # Extract failure class from Either<FailureType, ...>
    failure_match = re.search(r'Either<(\w+),', content)
    failure_class = failure_match.group(1) if failure_match else fallback['failure_class']
    
    # Extract the import line for the failure class
    failure_import = fallback['failure_import']
    failure_file_stem = model_name + '_failure'
    for line in content.splitlines():
        if 'import' in line and failure_file_stem in line:
            import_match = re.search(r"import\s+'(package:[^']+)'", line)
            if import_match:
                failure_import = import_match.group(1)
                break
    
    # Detect available methods by matching method signatures (name followed by '(')
    methods = set()
    method_patterns = {
        'getAll': r'\bgetAll\s*\(',
        'getById': r'\bgetById\s*\(',
        'create': r'\bcreate\s*\(',
        'update': r'\bupdate\s*\(',
        'delete': r'\bdelete\s*\(',
        'getByAuthId': r'\bgetByAuthId\s*\(',
        'createOrUpdate': r'\bcreateOrUpdate\s*\(',
        'getCurrentUserProfile': r'\bgetCurrentUserProfile\s*\(',
        'updateCurrentUserProfile': r'\bupdateCurrentUserProfile\s*\(',
        'uploadAvatar': r'\buploadAvatar\s*\(',
        'logout': r'\blogout\s*\(',
    }
    for method_name, pattern in method_patterns.items():
        if re.search(pattern, content):
            methods.add(method_name)
    
    return {
        'failure_class': failure_class,
        'failure_import': failure_import,
        'methods': methods,
    }


def ensure_base_form_bloc(project_name: str, lib_path: Path) -> None:
    """Generate core/bloc/base_form_bloc.dart if it doesn't already exist.

    Called automatically when creating a form component, so the BaseFormBloc
    is only added to projects that actually use form components.
    """
    target = lib_path / "core" / "bloc" / "base_form_bloc.dart"
    if not target.exists():
        generate_file(project_name, lib_path, "core/bloc/base_form_bloc_template.jinja", "core/bloc/base_form_bloc.dart")


def create_component_form_layers(component_dir: Path, component_name: str, field_list: list[dict], project_name: str, folder: Optional[str], domain_model_name: Optional[str] = None, domain_folder: Optional[str] = None, domain_model_folder: Optional[str] = None, lib_path: Optional[Path] = None) -> None:
    """Create all layers for a form component
    
    Args:
        component_dir: Path to component directory
        component_name: Name of the component
        field_list: List of field dictionaries
        project_name: Name of the project
        folder: Optional folder path
        domain_model_name: Optional domain model name / file stem (if using domain model)
        domain_folder: Optional domain folder name (e.g., 'domain')
        domain_model_folder: Optional containing folder for the model. Defaults to domain_model_name.
        lib_path: Path to lib/ directory (used to generate core/bloc/base_form_bloc.dart)
    """
    if lib_path is not None:
        ensure_base_form_bloc(project_name, lib_path)

    # Discover enums for type-aware form generation
    from .feature import find_enums_with_info
    known_enums: set = set()
    enums_info: Dict = {}
    if lib_path and domain_folder:
        enums_info = find_enums_with_info(lib_path, domain_folder)
        known_enums = set(enums_info.keys())

    # Build the import path prefix
    if folder:
        import_prefix = f"{folder.replace('/', '/')}/{component_name}"
    else:
        import_prefix = component_name
    
    # Application layer
    app_dir = component_dir / "application"
    app_dir.mkdir(exist_ok=True)
    
    domain_value_objects_import: Optional[str] = None
    if domain_folder and domain_model_name:
        model_folder = domain_model_folder or domain_model_name
        domain_value_objects_import = f"{domain_folder}/{model_folder}/model/value_objects.dart"

    # Create form-specific BLoC files using templates
    generate_form_event_from_template(component_name, field_list, app_dir, project_name, known_enums=known_enums)
    generate_form_state_from_template(component_name, field_list, app_dir, project_name, known_enums=known_enums)
    generate_form_bloc_from_template(
        component_name,
        field_list,
        app_dir,
        project_name,
        known_enums=known_enums,
        enums_info=enums_info,
        domain_value_objects_import=domain_value_objects_import,
    )

    # Presentation layer
    presentation_dir = component_dir / "presentation"
    presentation_dir.mkdir(exist_ok=True)

    # Create component widget - pass field_list and domain info for form components
    generate_form_widget_from_template(
        component_name,
        field_list,
        presentation_dir,
        project_name,
        import_prefix,
        known_enums=known_enums,
        enums_info=enums_info,
        domain_value_objects_import=domain_value_objects_import,
    )


def create_component_layers(component_dir: Path, component_name: str, project_name: str, folder: Optional[str], domain_model_name: Optional[str] = None, domain_folder: Optional[str] = None, domain_model_folder: Optional[str] = None, lib_path: Optional[Path] = None) -> None:
    """Create all layers for a single-item component (load by ID).
    
    Args:
        component_dir: Path to component directory
        component_name: Name of the component
        project_name: Name of the project
        folder: Optional folder path
        domain_model_name: Optional domain model name / file stem (if using domain model)
        domain_folder: Optional domain folder name (e.g., 'domain')
        domain_model_folder: Optional containing folder for the model (e.g., 'auth' for user_profile).
                             Defaults to domain_model_name if not specified.
        lib_path: Optional path to lib/ directory (for reading repository interface)
    """
    if domain_model_folder is None:
        domain_model_folder = domain_model_name
    
    # Build the import path prefix
    if folder:
        import_prefix = f"{folder.replace('/', '/')}/{component_name}"
    else:
        import_prefix = component_name

    resolved_lib_path = lib_path or infer_lib_path(component_dir)
    ensure_common_widgets(project_name, resolved_lib_path)
    
    # Application layer
    app_dir = component_dir / "application"
    app_dir.mkdir(exist_ok=True)
    
    # Determine import prefix for domain model
    if domain_model_name and domain_folder:
        domain_import_prefix = f"{domain_folder}/{domain_model_folder}"
    else:
        domain_import_prefix = None
    
    # Get PascalCase names
    component_pascal = to_pascal_case_preserve(component_name)
    failure_class_for_widget: Optional[str] = None
    widget_domain_import_prefix = ""
    widget_domain_model_name = ""
    widget_domain_model_pascal = ""

    # Generate event and state files
    if domain_import_prefix:
        domain_model_pascal = to_pascal_case_preserve(domain_model_name)
        widget_domain_import_prefix = domain_import_prefix
        widget_domain_model_name = domain_model_name or ""
        widget_domain_model_pascal = domain_model_pascal
        
        # Read repository interface to detect failure type
        repo_info = None
        if resolved_lib_path:
            repo_info = get_repository_info(resolved_lib_path, domain_folder, domain_model_name, domain_model_folder)
        
        failure_class = repo_info['failure_class'] if repo_info else f"{domain_model_pascal}Failure"
        failure_class_for_widget = failure_class
        failure_import = f"import '{repo_info['failure_import']}';" if repo_info else f"import 'package:{project_name}/{domain_import_prefix}/model/{domain_model_name}_failure.dart';"
        
        freezed_mixin_event = "_$" + component_pascal + "Event"
        freezed_mixin_state = "_$" + component_pascal + "State"
        
        # Determine load method: use getCurrentUserProfile if available, otherwise getById
        available_methods = repo_info['methods'] if repo_info else {'getById'}
        has_get_current = 'getCurrentUserProfile' in available_methods
        
        if has_get_current:
            event_load_factory = f"  const factory {component_pascal}Event.loadRequested() = LoadRequested;"
            load_await_rhs = "_repository.getCurrentUserProfile()"
            reload_await_rhs = "_repository.getCurrentUserProfile()"
            last_id_field = ""
            fold_success = f"      ({domain_model_pascal} item) => emit({component_pascal}State.loaded(item)),"
        else:
            event_load_factory = f"  const factory {component_pascal}Event.loadRequested(String id) = LoadRequested;"
            load_await_rhs = "_repository.getById(event.id)"
            reload_await_rhs = "_repository.getById(_lastLoadedId!)"
            last_id_field = "\n  String? _lastLoadedId;"
            fold_success = f"""      ({domain_model_pascal} item) {{
        _lastLoadedId = event.id;
        emit({component_pascal}State.loaded(item));
      }},"""

        event_reload_factory = f"  const factory {component_pascal}Event.reloadRequested() = ReloadRequested;"

        # Generate event file (load + reload)
        event_content = f"""part of '{component_name}_bloc.dart';

@freezed
abstract class {component_pascal}Event with {freezed_mixin_event} {{
{event_load_factory}
{event_reload_factory}
}}
"""
        (app_dir / f"{component_name}_event.dart").write_text(event_content)
        
        # Generate state file with domain model type
        state_content = f"""part of '{component_name}_bloc.dart';

@freezed
abstract class {component_pascal}State with {freezed_mixin_state} {{
  const factory {component_pascal}State.initial() = Initial;
  const factory {component_pascal}State.loading() = Loading;
  const factory {component_pascal}State.loaded({domain_model_pascal} item, {{@Default(false) bool isReloading}}) = Loaded;
  const factory {component_pascal}State.error({failure_class} failure) = Error;
}}
"""
        (app_dir / f"{component_name}_state.dart").write_text(state_content)
    else:
        # Empty (Vuoto) component: minimal event/state without domain model
        freezed_mixin_event_empty = "_$" + component_pascal + "Event"
        freezed_mixin_state_empty = "_$" + component_pascal + "State"

        event_content = f"""part of '{component_name}_bloc.dart';

@freezed
abstract class {component_pascal}Event with {freezed_mixin_event_empty} {{
  const factory {component_pascal}Event.loadRequested() = LoadRequested;
}}
"""
        (app_dir / f"{component_name}_event.dart").write_text(event_content)

        state_content = f"""part of '{component_name}_bloc.dart';

@freezed
abstract class {component_pascal}State with {freezed_mixin_state_empty} {{
  const factory {component_pascal}State.initial() = Initial;
  const factory {component_pascal}State.loading() = Loading;
  const factory {component_pascal}State.loaded() = Loaded;
  const factory {component_pascal}State.error(String message) = Error;
}}
"""
        (app_dir / f"{component_name}_state.dart").write_text(state_content)

    # Generate BLoC with domain model imports if provided
    if domain_import_prefix:
        bloc_content = f"""import 'package:bloc/bloc.dart';
import 'package:dartz/dartz.dart';
import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:{project_name}/{domain_import_prefix}/model/{domain_model_name}.dart';
{failure_import}
import 'package:{project_name}/{domain_import_prefix}/model/i_{domain_model_name}_repository.dart';

part '{component_name}_bloc.freezed.dart';
part '{component_name}_event.dart';
part '{component_name}_state.dart';

class {component_pascal}Bloc extends Bloc<{component_pascal}Event, {component_pascal}State> {{
  final I{domain_model_pascal}Repository _repository;{last_id_field}

  {component_pascal}Bloc(this._repository) : super(const {component_pascal}State.initial()) {{
    on<LoadRequested>(_onLoadRequested);
    on<ReloadRequested>(_onReloadRequested);
  }}

  Future<void> _onLoadRequested(LoadRequested event, Emitter<{component_pascal}State> emit) async {{
    emit(const {component_pascal}State.loading());
    final Either<{failure_class}, {domain_model_pascal}> result = await {load_await_rhs};
    result.fold(
      ({failure_class} failure) => emit({component_pascal}State.error(failure)),
{fold_success}
    );
  }}

  Future<void> _onReloadRequested(ReloadRequested event, Emitter<{component_pascal}State> emit) async {{
    if (state is! Loaded) return;
    final Loaded current = state as Loaded;
    emit(current.copyWith(isReloading: true));
    final Either<{failure_class}, {domain_model_pascal}> result = await {reload_await_rhs};
    result.fold(
      ({failure_class} failure) => emit(current.copyWith(isReloading: false)),
      ({domain_model_pascal} item) => emit({component_pascal}State.loaded(item)),
    );
  }}
}}
"""
        (app_dir / f"{component_name}_bloc.dart").write_text(bloc_content)
    else:
        # Empty (Vuoto) BLoC: no repository, stub handlers
        bloc_content = f"""import 'package:bloc/bloc.dart';
import 'package:freezed_annotation/freezed_annotation.dart';

part '{component_name}_bloc.freezed.dart';
part '{component_name}_event.dart';
part '{component_name}_state.dart';

class {component_pascal}Bloc extends Bloc<{component_pascal}Event, {component_pascal}State> {{
  {component_pascal}Bloc() : super(const {component_pascal}State.initial()) {{
    on<LoadRequested>(_onLoadRequested);
  }}

  Future<void> _onLoadRequested(LoadRequested event, Emitter<{component_pascal}State> emit) async {{
    emit(const {component_pascal}State.loading());
    // TODO: implement load logic
    emit(const {component_pascal}State.loaded());
  }}
}}
"""
        (app_dir / f"{component_name}_bloc.dart").write_text(bloc_content)
    
    # Presentation layer
    presentation_dir = component_dir / "presentation"
    presentation_dir.mkdir(exist_ok=True)
    
    # Create component widget
    generate_component_widget_from_template(
        component_name,
        presentation_dir,
        project_name,
        'single',
        import_prefix,
        failure_class=failure_class_for_widget,
        domain_import_prefix=widget_domain_import_prefix,
        domain_model_name=widget_domain_model_name,
        domain_model_pascal=widget_domain_model_pascal,
    )


def generate_form_widget_from_template(
    component_name: str,
    field_list: list[dict],
    presentation_dir: Path,
    project_name: str,
    import_prefix: str,
    known_enums: set = None,
    enums_info: Dict = None,
    domain_value_objects_import: Optional[str] = None,
) -> None:
    """Generate form component widget file using Jinja template"""
    _enums = known_enums or set()
    _enums_info = enums_info or {}
    pascal_name = to_pascal_case(component_name)
    bloc_name = f"{pascal_name}FormBloc"
    state_name = f"{pascal_name}FormState"
    bloc_import = f"import 'package:{project_name}/{import_prefix}/application/{component_name}_form_bloc.dart';"

    # Build extra imports needed by the template (enum imports)
    extra_imports: list[str] = []

    processed_field_list = []
    for field in field_list:
        field_name = field['name']
        field_type = field['type']
        base_ft = field_type[:-1] if field_type.endswith('?') else field_type

        field_dict = dict(field)
        field_dict['pascal_name'] = to_pascal_case_preserve(field_name)
        field_dict['label'] = ' '.join(word.capitalize() for word in field_name.split('_'))

        meta = get_form_field_metadata(base_ft, field_name, known_enums=_enums)
        field_dict.update(meta)

        if meta['is_enum']:
            info = _enums_info.get(base_ft)
            if info:
                imp = f"import 'package:{project_name}/{info['folder']}/{info['file_stem']}.dart';"
                if imp not in extra_imports:
                    extra_imports.append(imp)

        processed_field_list.append(field_dict)

    generate_file(project_name, presentation_dir, "component/component_form_widget_template.jinja", f"{component_name}_component.dart", {
        "component_name": component_name,
        "pascal_name": pascal_name,
        "bloc_name": bloc_name,
        "state_name": state_name,
        "bloc_import": bloc_import,
        "extra_imports": "\n".join(extra_imports),
        "field_list": processed_field_list,
        "domain_value_objects_import": domain_value_objects_import,
    })


def generate_component_widget_from_template(
    component_name: str,
    presentation_dir: Path,
    project_name: str,
    component_type: str,
    import_prefix: str,
    failure_class: Optional[str] = None,
    domain_import_prefix: str = "",
    domain_model_name: str = "",
    domain_model_pascal: str = "",
) -> None:
    """Generate component widget file using Jinja template
    
    Args:
        component_name: Name of the component
        presentation_dir: Path to presentation directory
        project_name: Name of the project
        component_type: Type of component ('form', 'list', or 'single')
        import_prefix: Import path prefix for the component
        domain_import_prefix: Domain lib path (e.g. domain/note) for package imports in the widget
        domain_model_name: Domain entity file stem (e.g. note)
        domain_model_pascal: Domain entity class name (e.g. Note) for typed switch patterns
    """
    pascal_name = to_pascal_case(component_name)
    
    if component_type == 'form':
        # Form components now use generate_form_widget_from_template
        # This should not be called for form components anymore
        raise ValueError("Use generate_form_widget_from_template for form components")
    elif component_type == 'list':
        raise ValueError(
            "List components must be generated via create_component_list_layers / "
            "create_component_list_layers_empty (not generate_component_widget_from_template).",
        )
    else:  # single
        bloc_name = f"{pascal_name}Bloc"
        state_name = f"{pascal_name}State"
        bloc_import = f"import 'package:{project_name}/{import_prefix}/application/{component_name}_bloc.dart';"
        generate_file(project_name, presentation_dir, "component/component_widget_template.jinja", f"{component_name}_component.dart", {
            "component_name": component_name,
            "pascal_name": pascal_name,
            "is_form": False,
            "bloc_name": bloc_name,
            "state_name": state_name,
            "bloc_import": bloc_import,
            "failure_class": failure_class or "",
            "domain_import_prefix": domain_import_prefix,
            "domain_model_name": domain_model_name,
            "domain_model_pascal": domain_model_pascal,
        })


def generate_form_event_from_template(component_name: str, field_list: list[dict], app_dir: Path, project_name: str, known_enums: set = None) -> None:
    """Generate form event file using Jinja template"""
    _enums = known_enums or set()
    pascal_name = to_pascal_case(component_name)

    field_events = []
    for field in field_list:
        field_name = field['name']
        if field_name == 'id':
            continue
        field_type = field['type']
        base_ft = field_type[:-1] if field_type.endswith('?') else field_type
        meta = get_form_field_metadata(base_ft, field_name, known_enums=_enums)
        capitalized_name = to_pascal_case_preserve(field_name)
        param_type = meta['event_param_type']
        param_name = meta['event_param_name']
        field_events.append(
            f"  const factory {pascal_name}FormEvent.{field_name}Changed({param_type} {param_name}) = {capitalized_name}Changed;"
        )

    field_events_str = "\n".join(field_events)

    generate_file(project_name, app_dir, "component/component_form_event_template.jinja", f"{component_name}_form_event.dart", {
        "component_name": component_name,
        "pascal_name": pascal_name,
        "field_events": field_events_str,
    })


def generate_form_state_from_template(component_name: str, field_list: list[dict], app_dir: Path, project_name: str, known_enums: set = None) -> None:
    """Generate form state file using Jinja template"""
    _enums = known_enums or set()
    pascal_name = to_pascal_case(component_name)

    field_declarations = []
    initial_values = []
    for field in field_list:
        field_name = field['name']
        if field_name == 'id':
            continue
        field_type = field['type']
        base_ft = field_type[:-1] if field_type.endswith('?') else field_type
        meta = get_form_field_metadata(base_ft, field_name, known_enums=_enums)
        capitalized_name = to_pascal_case_preserve(field_name)

        if meta['is_enum']:
            field_declarations.append(f"    required {meta['enum_class']} {field_name},")
            initial_values.append(f"        {field_name}: {meta['initial_value_expr']},")
        else:
            field_declarations.append(f"    required {capitalized_name} {field_name},")
            initial_values.append(f"        {field_name}: {capitalized_name}({meta['initial_value_expr']}),")

    field_declarations_str = "\n".join(field_declarations)
    initial_values_str = "\n".join(initial_values)

    generate_file(project_name, app_dir, "component/component_form_state_template.jinja", f"{component_name}_form_state.dart", {
        "component_name": component_name,
        "pascal_name": pascal_name,
        "field_declarations": field_declarations_str,
        "initial_values": initial_values_str,
    })


def generate_form_bloc_from_template(
    component_name: str,
    field_list: list[dict],
    app_dir: Path,
    project_name: str,
    known_enums: set = None,
    enums_info: Dict = None,
    domain_value_objects_import: Optional[str] = None,
) -> None:
    """Generate form bloc file using Jinja template"""
    _enums = known_enums or set()
    _enums_info = enums_info or {}
    pascal_name = to_pascal_case(component_name)

    extra_imports: list[str] = []
    processed_field_list = []
    for field in field_list:
        field_name = field['name']
        field_type = field['type']
        base_ft = field_type[:-1] if field_type.endswith('?') else field_type

        field_dict = dict(field)
        field_dict['pascal_name'] = to_pascal_case_preserve(field_name)
        meta = get_form_field_metadata(base_ft, field_name, known_enums=_enums)
        field_dict.update(meta)

        if meta['is_enum']:
            info = _enums_info.get(base_ft)
            if info:
                imp = f"import 'package:{project_name}/{info['folder']}/{info['file_stem']}.dart';"
                if imp not in extra_imports:
                    extra_imports.append(imp)

        processed_field_list.append(field_dict)

    generate_file(project_name, app_dir, "component/component_form_bloc_template.jinja", f"{component_name}_form_bloc.dart", {
        "component_name": component_name,
        "pascal_name": pascal_name,
        "field_list": processed_field_list,
        "domain_value_objects_import": domain_value_objects_import,
        "extra_imports": "\n".join(extra_imports),
    })


def _parse_value_objects_file(vo_file: Path) -> Dict[str, str]:
    """Parse a value_objects.dart file and return a mapping from VO class name
    to its underlying Dart type.

    Looks for ``class Foo extends ValueObject<Bar>`` patterns.

    Returns:
        e.g. {'Title': 'String', 'Vote': 'int', 'CreatedAt': 'DateTime'}
    """
    if not vo_file.exists():
        return {}
    try:
        content = vo_file.read_text()
    except Exception:
        return {}
    vo_pattern = r'class\s+(\w+)\s+extends\s+ValueObject\s*<\s*(\w+)\s*>'
    return {m.group(1): m.group(2) for m in re.finditer(vo_pattern, content)}


def _dart_type_to_field_type(dart_type: str) -> str:
    """Convert a Dart type string (from ``ValueObject<T>``) to the lowercase
    field-type convention used by the rest of the pipeline.

    'String' -> 'string', 'DateTime' -> 'datetime', 'int' -> 'int', etc.
    """
    mapping = {
        'String': 'string',
        'int': 'int',
        'double': 'double',
        'bool': 'bool',
        'DateTime': 'datetime',
    }
    return mapping.get(dart_type, dart_type.lower())


def _resolve_entity_field_type(
    raw_type: str,
    vo_type_map: Dict[str, str],
    known_enums: set,
) -> str:
    """Resolve an entity field's Dart type to the form-field type string.

    Resolution order:
        1. Nullable (``T?``) – strip ``?``, resolve inner, re-append ``?``
        2. ``Option<T>`` – resolve inner T, append ``?``
        3. Known ValueObject – map via *vo_type_map* to underlying primitive
        4. Known enum – keep class name as-is
        5. Dart primitive – lowercase
        6. Generic collection (``List<T>``, etc.) – returned as-is
        7. Fallback – ``'string'``
    """
    if raw_type.endswith('?'):
        base = raw_type[:-1].strip()
        inner = _resolve_entity_field_type(base, vo_type_map, known_enums)
        return inner if inner.endswith('?') else inner + '?'

    option_match = re.match(r'^Option\s*<\s*(.+)\s*>$', raw_type)
    if option_match:
        inner = option_match.group(1).strip()
        resolved = _resolve_entity_field_type(inner, vo_type_map, known_enums)
        return resolved if resolved.endswith('?') else resolved + '?'

    if raw_type in vo_type_map:
        return _dart_type_to_field_type(vo_type_map[raw_type])

    if raw_type in known_enums:
        return raw_type

    primitive_map = {
        'String': 'string',
        'int': 'int',
        'double': 'double',
        'bool': 'bool',
        'DateTime': 'datetime',
    }
    if raw_type in primitive_map:
        return primitive_map[raw_type]

    if '<' in raw_type and '>' in raw_type:
        return raw_type

    return 'string'


def get_model_fields_from_domain(lib_path: Path, domain_folder: str, model_name: str, model_folder: Optional[str] = None) -> List[dict]:
    """Extract field information from a domain model entity file.

    Reads the entity file **and** both core and local ``value_objects.dart``
    to resolve ValueObject wrappers to their underlying Dart types.  Also
    detects enums from the ``domain/enums/`` folder.

    Args:
        lib_path: Path to lib/ directory
        domain_folder: Name of domain folder (e.g., 'domain')
        model_name: Name of the domain model (file stem)
        model_folder: Containing folder for the model. Defaults to model_name.

    Returns:
        List of field dicts ``{'name': ..., 'type': ...}`` compatible with
        the existing ``field_list`` format used by form generators.
    """
    if model_folder is None:
        model_folder = model_name

    entity_file = lib_path / domain_folder / model_folder / "model" / f"{model_name}.dart"

    if not entity_file.exists():
        raise FileNotFoundError(f"Domain model entity file not found: {entity_file}")

    content = entity_file.read_text()

    # --- Build ValueObject → underlying type mapping ----------------------
    vo_type_map: Dict[str, str] = {}
    core_vo_file = lib_path / "core" / "model" / "value_objects.dart"
    vo_type_map.update(_parse_value_objects_file(core_vo_file))
    local_vo_file = lib_path / domain_folder / model_folder / "model" / "value_objects.dart"
    vo_type_map.update(_parse_value_objects_file(local_vo_file))

    # --- Discover enums ---------------------------------------------------
    from .feature import find_enums_with_info
    enums_info = find_enums_with_info(lib_path, domain_folder)
    known_enums = set(enums_info.keys())

    # --- Parse factory constructor fields ---------------------------------
    factory_pattern = r'const factory\s+\w+\(\{([^}]+)\}\)'
    match = re.search(factory_pattern, content, re.DOTALL)

    if not match:
        raise ValueError(f"Could not parse entity file: {entity_file}")

    fields_section = match.group(1)

    # Capture full type including generics: ``required Option<Desc> name,``
    field_pattern = r'required\s+(.+?)\s+(\w+)\s*[,}]'
    fields = []

    for field_match in re.finditer(field_pattern, fields_section):
        raw_type = field_match.group(1).strip()
        field_name = field_match.group(2)

        mapped_type = _resolve_entity_field_type(raw_type, vo_type_map, known_enums)

        fields.append({
            'name': field_name,
            'type': mapped_type,
        })

    return fields


def _create_component_list_layers_empty(component_dir: Path, component_name: str, project_name: str, folder: Optional[str]) -> None:
    """Create all layers for an empty (Vuoto) list component with no domain model."""
    if folder:
        component_import_prefix = f"{folder.replace('/', '/')}/{component_name}"
    else:
        component_import_prefix = component_name

    ensure_common_widgets(project_name, infer_lib_path(component_dir))

    app_dir = component_dir / "application"
    app_dir.mkdir(exist_ok=True)

    component_pascal = to_pascal_case_preserve(component_name)
    freezed_mixin_event = "_$" + component_pascal + "Event"
    freezed_mixin_state = "_$" + component_pascal + "State"

    event_content = f"""part of '{component_name}_bloc.dart';

@freezed
abstract class {component_pascal}Event with {freezed_mixin_event} {{
  const factory {component_pascal}Event.loadRequested() = LoadRequested;
}}
"""
    (app_dir / f"{component_name}_event.dart").write_text(event_content)

    state_content = f"""part of '{component_name}_bloc.dart';

@freezed
abstract class {component_pascal}State with {freezed_mixin_state} {{
  const factory {component_pascal}State.initial() = Initial;
  const factory {component_pascal}State.loading() = Loading;
  const factory {component_pascal}State.loaded() = Loaded;
  const factory {component_pascal}State.error(String message) = Error;
}}
"""
    (app_dir / f"{component_name}_state.dart").write_text(state_content)

    bloc_content = f"""import 'package:bloc/bloc.dart';
import 'package:freezed_annotation/freezed_annotation.dart';

part '{component_name}_bloc.freezed.dart';
part '{component_name}_event.dart';
part '{component_name}_state.dart';

class {component_pascal}Bloc extends Bloc<{component_pascal}Event, {component_pascal}State> {{
  {component_pascal}Bloc() : super(const {component_pascal}State.initial()) {{
    on<LoadRequested>(_onLoadRequested);
  }}

  Future<void> _onLoadRequested(LoadRequested event, Emitter<{component_pascal}State> emit) async {{
    emit(const {component_pascal}State.loading());
    // TODO: implement load logic
    emit(const {component_pascal}State.loaded());
  }}
}}
"""
    (app_dir / f"{component_name}_bloc.dart").write_text(bloc_content)

    presentation_dir = component_dir / "presentation"
    presentation_dir.mkdir(exist_ok=True)

    generate_file(project_name, presentation_dir, "component/component_list_widget_template.jinja", f"{component_name}_component.dart", {
        "component_name": component_name,
        "component_pascal": component_pascal,
        "component_import_prefix": component_import_prefix,
        "empty_component": True,
    })


def create_component_list_layers(component_dir: Path, component_name: str, project_name: str, folder: Optional[str], domain_model_name: Optional[str] = None, domain_folder: Optional[str] = None, domain_model_folder: Optional[str] = None, lib_path: Optional[Path] = None) -> None:
    """Create all layers for a list component.
    
    Generates events and handlers based on the actual methods available
    in the repository interface (e.g., skips delete if no delete method exists).
    If domain_model_name is None, generates an empty (Vuoto) scaffold without a domain model.
    
    Args:
        component_dir: Path to component directory
        component_name: Name of the component
        project_name: Name of the project
        folder: Optional folder path
        domain_model_name: Domain model name / file stem (None for empty scaffold)
        domain_folder: Domain folder name (e.g., 'domain')
        domain_model_folder: Containing folder for the model. Defaults to domain_model_name.
        lib_path: Optional path to lib/ directory (for reading repository interface)
    """
    if domain_model_name is None:
        _create_component_list_layers_empty(component_dir, component_name, project_name, folder)
        return
    
    if domain_model_folder is None:
        domain_model_folder = domain_model_name
    
    # Build import paths
    if folder:
        component_import_prefix = f"{folder.replace('/', '/')}/{component_name}"
    else:
        component_import_prefix = component_name
    
    domain_import_prefix = f"{domain_folder}/{domain_model_folder}"

    resolved_lib_path = lib_path or infer_lib_path(component_dir)
    ensure_common_widgets(project_name, resolved_lib_path)
    
    # Application layer
    app_dir = component_dir / "application"
    app_dir.mkdir(exist_ok=True)
    
    # Get PascalCase names
    component_pascal = to_pascal_case_preserve(component_name)
    domain_model_pascal = to_pascal_case_preserve(domain_model_name)
    
    # Read repository interface to detect failure type and available methods
    repo_info = None
    if resolved_lib_path:
        repo_info = get_repository_info(resolved_lib_path, domain_folder, domain_model_name, domain_model_folder)
    
    failure_class = repo_info['failure_class'] if repo_info else f"{domain_model_pascal}Failure"
    failure_import = f"import '{repo_info['failure_import']}';" if repo_info else f"import 'package:{project_name}/{domain_import_prefix}/model/{domain_model_name}_failure.dart';"
    available_methods = repo_info['methods'] if repo_info else {'getAll', 'getById', 'create', 'update', 'delete'}
    
    has_get_all = 'getAll' in available_methods
    has_create = 'create' in available_methods
    has_update = 'update' in available_methods
    has_delete = 'delete' in available_methods
    
    freezed_mixin_event = "_$" + component_pascal + "Event"
    freezed_mixin_state = "_$" + component_pascal + "State"
    
    # Build events dynamically based on available repository methods
    event_lines = []
    if has_get_all:
        event_lines.append(f"  const factory {component_pascal}Event.loadRequested() = LoadRequested;")
        event_lines.append(f"  const factory {component_pascal}Event.reloadRequested() = ReloadRequested;")
    if has_create:
        event_lines.append(f"  const factory {component_pascal}Event.createRequested({domain_model_pascal} item) = CreateRequested;")
    if has_update:
        event_lines.append(f"  const factory {component_pascal}Event.updateRequested({domain_model_pascal} item) = UpdateRequested;")
    if has_delete:
        event_lines.append(f"  const factory {component_pascal}Event.deleteRequested(String id) = DeleteRequested;")
    events_str = "\n".join(event_lines)
    
    event_content = f"""part of '{component_name}_bloc.dart';

@freezed
abstract class {component_pascal}Event with {freezed_mixin_event} {{
{events_str}
}}
"""
    (app_dir / f"{component_name}_event.dart").write_text(event_content)
    
    # Create state file
    state_content = f"""part of '{component_name}_bloc.dart';

@freezed
abstract class {component_pascal}State with {freezed_mixin_state} {{
  const factory {component_pascal}State.initial() = Initial;
  const factory {component_pascal}State.loading() = Loading;
  const factory {component_pascal}State.loaded(List<{domain_model_pascal}> items, {{@Default(false) bool isReloading}}) = Loaded;
  const factory {component_pascal}State.error({failure_class} failure) = Error;
}}
"""
    (app_dir / f"{component_name}_state.dart").write_text(state_content)
    
    # Build BLoC handlers dynamically
    reload_snippet = f"""final Either<{failure_class}, List<{domain_model_pascal}>> itemsResult = await _repository.getAll();
        itemsResult.fold(
          ({failure_class} failure) => emit({component_pascal}State.error(failure)),
          (List<{domain_model_pascal}> items) => emit({component_pascal}State.loaded(items)),
        );"""
    
    on_registrations = []
    handler_methods = []
    
    if has_get_all:
        on_registrations.append("    on<LoadRequested>(_onLoadRequested);")
        on_registrations.append("    on<ReloadRequested>(_onReloadRequested);")
        handler_methods.append(f"""  Future<void> _onLoadRequested(LoadRequested event, Emitter<{component_pascal}State> emit) async {{
    emit(const {component_pascal}State.loading());
    final Either<{failure_class}, List<{domain_model_pascal}>> result = await _repository.getAll();
    result.fold(
      ({failure_class} failure) => emit({component_pascal}State.error(failure)),
      (List<{domain_model_pascal}> items) => emit({component_pascal}State.loaded(items)),
    );
  }}""")
        handler_methods.append(f"""  Future<void> _onReloadRequested(ReloadRequested event, Emitter<{component_pascal}State> emit) async {{
    if (state is! Loaded) return;
    final Loaded current = state as Loaded;
    emit(current.copyWith(isReloading: true));
    final Either<{failure_class}, List<{domain_model_pascal}>> result = await _repository.getAll();
    result.fold(
      ({failure_class} failure) => emit(current.copyWith(isReloading: false)),
      (List<{domain_model_pascal}> items) => emit({component_pascal}State.loaded(items)),
    );
  }}""")
    
    if has_create:
        on_registrations.append("    on<CreateRequested>(_onCreateRequested);")
        handler_methods.append(f"""  Future<void> _onCreateRequested(CreateRequested event, Emitter<{component_pascal}State> emit) async {{
    emit(const {component_pascal}State.loading());
    final Either<{failure_class}, Unit> result = await _repository.create(event.item);
    result.fold(
      ({failure_class} failure) => emit({component_pascal}State.error(failure)),
      (Unit _) async {{
        {reload_snippet}
      }},
    );
  }}""")
    
    if has_update:
        on_registrations.append("    on<UpdateRequested>(_onUpdateRequested);")
        handler_methods.append(f"""  Future<void> _onUpdateRequested(UpdateRequested event, Emitter<{component_pascal}State> emit) async {{
    emit(const {component_pascal}State.loading());
    final Either<{failure_class}, Unit> result = await _repository.update(event.item);
    result.fold(
      ({failure_class} failure) => emit({component_pascal}State.error(failure)),
      (Unit _) async {{
        {reload_snippet}
      }},
    );
  }}""")
    
    if has_delete:
        on_registrations.append("    on<DeleteRequested>(_onDeleteRequested);")
        handler_methods.append(f"""  Future<void> _onDeleteRequested(DeleteRequested event, Emitter<{component_pascal}State> emit) async {{
    emit(const {component_pascal}State.loading());
    final Either<{failure_class}, Unit> result = await _repository.delete(event.id);
    result.fold(
      ({failure_class} failure) => emit({component_pascal}State.error(failure)),
      (Unit _) async {{
        {reload_snippet}
      }},
    );
  }}""")
    
    on_registrations_str = "\n".join(on_registrations)
    handler_methods_str = "\n\n".join(handler_methods)
    
    bloc_content = f"""import 'package:bloc/bloc.dart';
import 'package:dartz/dartz.dart';
import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:{project_name}/{domain_import_prefix}/model/{domain_model_name}.dart';
{failure_import}
import 'package:{project_name}/{domain_import_prefix}/model/i_{domain_model_name}_repository.dart';

part '{component_name}_bloc.freezed.dart';
part '{component_name}_event.dart';
part '{component_name}_state.dart';

class {component_pascal}Bloc extends Bloc<{component_pascal}Event, {component_pascal}State> {{
  final I{domain_model_pascal}Repository _repository;

  {component_pascal}Bloc(this._repository) : super(const {component_pascal}State.initial()) {{
{on_registrations_str}
  }}

{handler_methods_str}
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
        "component_import_prefix": component_import_prefix,
        "empty_component": False,
        "failure_class": failure_class,
        "domain_import_prefix": domain_import_prefix,
        "domain_model_name": domain_model_name,
        "domain_model_pascal": domain_model_pascal,
    })

