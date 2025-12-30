"""Domain entity generation functions

Domain entities are shared business entities that can be used by multiple features.
They only contain model and infrastructure layers (no application/presentation).
"""

from pathlib import Path
from typing import Optional
from generators.templates.copier import generate_file
from .utils import map_field_type, to_pascal_case_preserve
from .feature import (
    generate_value_objects_and_validators,
)


def create_domain_entity_layers(domain_dir: Path, entity_name: str, field_list: list[dict], project_name: str, folder: Optional[str]) -> None:
    """Create model and infrastructure layers for a domain entity
    
    Domain entities do NOT include application or presentation layers.
    They are meant to be shared across multiple features.
    """
    # Build the import path prefix
    if folder:
        import_prefix = f"{folder.replace('/', '/')}/{entity_name}"
    else:
        import_prefix = entity_name
    
    # Model layer
    model_dir = domain_dir / "model"
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
    generate_file(project_name, model_dir, "feature/feature_entity_template.jinja", f"{entity_name}.dart", {
        "feature_name": entity_name, 
        "fields": entity_fields_str,
        "entity_import": entity_import
    })
    
    # Create failure
    generate_file(project_name, model_dir, "feature/feature_failure_template.jinja", f"{entity_name}_failure.dart", {"feature_name": entity_name})
    
    # Infrastructure layer
    infra_dir = domain_dir / "infrastructure"
    infra_dir.mkdir(exist_ok=True)
    
    # Create DTO
    dto_fields = ",\n".join([f"    required {map_field_type(field['type'])} {field['name']}" for field in field_list])
    generate_file(project_name, infra_dir, "feature/feature_dto_template.jinja", f"{entity_name}_dto.dart", {"feature_name": entity_name, "fields": dto_fields})
    
    # Create repository interface
    i_repo_import = f"""import 'package:{project_name}/{import_prefix}/model/{entity_name}.dart';
import 'package:{project_name}/{import_prefix}/model/{entity_name}_failure.dart';
"""
    generate_file(project_name, model_dir, "feature/i_feature_repository_template.jinja", f"i_{entity_name}_repository.dart", {
        "feature_name": entity_name,
        "i_repo_import": i_repo_import
    })

    # Generate mapper fields for DTO-Domain conversions
    from_dto_fields = []
    to_dto_fields = []
    for field in field_list:
        field_name = field['name']
        capitalized_name = to_pascal_case_preserve(field_name)
        
        if field_name == 'id':
            from_dto_fields.append(f"      id: UniqueId.fromUniqueString(dto.id)")
            to_dto_fields.append(f"      id: entity.id.getOrCrash()")
        else:
            from_dto_fields.append(f"      {field_name}: {capitalized_name}(dto.{field_name})")
            to_dto_fields.append(f"      {field_name}: entity.{field_name}.getOrCrash()")
    
    from_dto_fields_str = ",\n".join(from_dto_fields)
    to_dto_fields_str = ",\n".join(to_dto_fields)
    
    # Create Service (Retrofit)
    generate_file(project_name, infra_dir, "domain/domain_service_template.jinja", f"{entity_name}_service.dart", {
        "entity_name": entity_name,
        "import_prefix": import_prefix
    })
    
    # Create Mapper
    generate_file(project_name, infra_dir, "domain/domain_mapper_template.jinja", f"{entity_name}_mapper.dart", {
        "entity_name": entity_name,
        "import_prefix": import_prefix,
        "from_dto_fields": from_dto_fields_str,
        "to_dto_fields": to_dto_fields_str
    })
    
    # Create Repository (uses Service + Mapper)
    repo_import = f"""import 'package:{project_name}/{import_prefix}/model/{entity_name}.dart';
import 'package:{project_name}/{import_prefix}/model/{entity_name}_failure.dart';
import 'package:{project_name}/{import_prefix}/model/i_{entity_name}_repository.dart';
import 'package:{project_name}/{import_prefix}/infrastructure/{entity_name}_service.dart';
import 'package:{project_name}/{import_prefix}/infrastructure/{entity_name}_mapper.dart';
"""
    generate_file(project_name, infra_dir, "domain/domain_repository_template.jinja", f"{entity_name}_repository.dart", {
        "entity_name": entity_name,
        "import_prefix": import_prefix,
        "repo_import": repo_import
    })
