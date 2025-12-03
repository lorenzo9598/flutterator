"""Feature generation functions"""

from pathlib import Path
from typing import Optional
from generators.templates.copier import generate_file
from .utils import map_field_type


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
            entity_fields.append(f"  required {field_name.capitalize()} {field_name},")
    
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
        capitalized_name = field_name.capitalize()
        
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
    generate_file(project_name, model_dir, "feature/value_validators_template.jinja", "value_validators.dart", {
        "project_name": project_name,
        "field_list": field_list
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
            capitalized_name = field_name.capitalize()
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

