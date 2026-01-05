"""Domain entity generation functions

Domain entities are shared business entities that can be used by multiple features.
They only contain model and infrastructure layers (no application/presentation).
"""

from pathlib import Path
from typing import Optional
from generators.templates.copier import generate_file
from .utils import map_field_type, map_field_type_to_dto, to_pascal_case_preserve, pascal_case_to_kebab_case, pascal_case_to_camel_case
from .validation import parse_field_type
from .feature import (
    generate_value_objects_and_validators,
    find_domain_models_with_class_names,
    get_domain_model_class_name,
)


def create_domain_entity_layers(domain_dir: Path, entity_folder_name: str, entity_class_name: str, field_list: list[dict], project_name: str, folder: Optional[str]) -> None:
    """Create model and infrastructure layers for a domain entity
    
    Args:
        domain_dir: Path to domain entity directory
        entity_folder_name: Folder name (snake_case, e.g., "note_item")
        entity_class_name: Class name (PascalCase, e.g., "NoteItem")
        field_list: List of field dictionaries
        project_name: Name of the project
        folder: Domain folder path
    
    Domain entities do NOT include application or presentation layers.
    They are meant to be shared across multiple features.
    """
    # Build the import path prefix (use folder name for paths)
    if folder:
        import_prefix = f"{folder.replace('/', '/')}/{entity_folder_name}"
    else:
        import_prefix = entity_folder_name
    
    # Model layer
    model_dir = domain_dir / "model"
    model_dir.mkdir(exist_ok=True)

    # Create value objects and validators
    generate_value_objects_and_validators(import_prefix, field_list, model_dir, project_name)
    
    # Create entity (domain model)
    # For entity fields, handle complex types like List<ModelName>
    entity_fields = []
    for field in field_list:
        field_name = field['name']
        field_type = field['type']
        
        if field_name == 'id':
            entity_fields.append(f"  required UniqueId id,")
        else:
            # For complex types like List<NoteItem>, use the type directly
            # For simple types (string, int, double, bool, DateTime), create ValueObject
            # For domain models (PascalCase but not primitive types), use directly
            PRIMITIVE_TYPES = {'String', 'int', 'double', 'bool', 'DateTime'}
            if '<' in field_type:
                # Complex type like List<NoteItem> - use directly (no ValueObject)
                entity_fields.append(f"  required {field_type} {field_name},")
            elif field_type in PRIMITIVE_TYPES:
                # Simple type - use ValueObject
                entity_fields.append(f"  required {to_pascal_case_preserve(field_name)} {field_name},")
            else:
                # Domain model (PascalCase, not primitive) - use directly (no ValueObject)
                entity_fields.append(f"  required {field_type} {field_name},")
    
    entity_import = f"import 'package:{project_name}/{import_prefix}/model/value_objects.dart';"
    
    # Find referenced domain models and add imports
    referenced_imports = []
    # Derive lib_path from domain_dir (domain_dir is like lib/domain/entity_name)
    lib_path = domain_dir.parent.parent if folder else domain_dir.parent
    domain_folder = folder if folder else "domain"
    models_with_classes = find_domain_models_with_class_names(lib_path, domain_folder) if lib_path.exists() else {}
    
    for field in field_list:
        field_type = field['type']
        if '<' in field_type:
            # List<ModelName> - extract ModelName
            base_type, generic_type = parse_field_type(field_type)
            if generic_type in models_with_classes.values():
                # Find folder name for this class
                for folder_name, class_name in models_with_classes.items():
                    if class_name == generic_type:
                        ref_import = f"import 'package:{project_name}/{domain_folder}/{folder_name}/model/{folder_name}.dart';"
                        if ref_import not in referenced_imports:
                            referenced_imports.append(ref_import)
                        break
        elif field_type and field_type[0].isupper() and field_type not in {'String', 'DateTime'}:
            # Domain model (not primitive)
            if field_type in models_with_classes.values():
                # Find folder name for this class
                for folder_name, class_name in models_with_classes.items():
                    if class_name == field_type:
                        ref_import = f"import 'package:{project_name}/{domain_folder}/{folder_name}/model/{folder_name}.dart';"
                        if ref_import not in referenced_imports:
                            referenced_imports.append(ref_import)
                        break
    
    # Combine entity_import with referenced imports
    all_entity_imports = entity_import
    if referenced_imports:
        all_entity_imports = entity_import + "\n" + "\n".join(referenced_imports)
    
    entity_fields_str = "\n".join(entity_fields)
    generate_file(project_name, model_dir, "feature/feature_entity_template.jinja", f"{entity_folder_name}.dart", {
        "feature_name": entity_class_name,  # Use class name for template (PascalCase) - for class name
        "file_name": entity_folder_name,  # Use folder name for file references (snake_case) - for part statements
        "fields": entity_fields_str,
        "entity_import": all_entity_imports
    })
    
    # Create failure
    generate_file(project_name, model_dir, "feature/feature_failure_template.jinja", f"{entity_folder_name}_failure.dart", {
        "feature_name": entity_class_name,  # Use class name for template (PascalCase)
        "file_name": entity_folder_name  # Use folder name for file references (snake_case)
    })
    
    # Infrastructure layer
    infra_dir = domain_dir / "infrastructure"
    infra_dir.mkdir(exist_ok=True)
    
    # Create DTO (convert types to DTO format - List<Model> -> List<ModelDto>, Model -> ModelDto)
    dto_fields = ",\n".join([f"    required {map_field_type_to_dto(field['type'])} {field['name']}" for field in field_list])
    
    # Find referenced DTOs and add imports
    referenced_dto_imports = []
    domain_folder = folder if folder else "domain"
    # Derive lib_path from domain_dir (domain_dir is like lib/domain/entity_name)
    lib_path = domain_dir.parent.parent if folder else domain_dir.parent
    models_with_classes = find_domain_models_with_class_names(lib_path, domain_folder) if lib_path.exists() else {}
    
    for field in field_list:
        field_type = field['type']
        dto_field_type = map_field_type_to_dto(field_type)
        
        # Check if DTO field type contains a DTO reference (e.g., List<TodoItemDto> or TodoItemDto)
        if 'Dto' in dto_field_type:
            # Extract model name (e.g., TodoItemDto -> TodoItem, List<TodoItemDto> -> TodoItem)
            import re
            model_match = re.search(r'(\w+)Dto', dto_field_type)
            if model_match:
                model_name = model_match.group(1)
                # Find folder name for this class
                for folder_name, class_name in models_with_classes.items():
                    if class_name == model_name:
                        ref_import = f"import 'package:{project_name}/{domain_folder}/{folder_name}/infrastructure/{folder_name}_dto.dart';"
                        if ref_import not in referenced_dto_imports:
                            referenced_dto_imports.append(ref_import)
                        break
    
    # Combine DTO imports
    dto_imports = "\n".join(referenced_dto_imports) if referenced_dto_imports else ""
    
    generate_file(project_name, infra_dir, "feature/feature_dto_template.jinja", f"{entity_folder_name}_dto.dart", {
        "feature_name": entity_class_name,  # Use class name for template (PascalCase)
        "file_name": entity_folder_name,  # Use folder name for file references (snake_case)
        "fields": dto_fields,
        "dto_imports": dto_imports
    })
    
    # Create repository interface
    i_repo_import = f"""import 'package:{project_name}/{import_prefix}/model/{entity_folder_name}.dart';
import 'package:{project_name}/{import_prefix}/model/{entity_folder_name}_failure.dart';
"""
    generate_file(project_name, model_dir, "feature/i_feature_repository_template.jinja", f"i_{entity_folder_name}_repository.dart", {
        "feature_name": entity_class_name,
        "i_repo_import": i_repo_import
    })

    # Generate mapper fields for DTO-Domain conversions
    from_dto_fields = []
    to_dto_fields = []
    mapper_dependencies = []  # List of (mapper_class_name, mapper_var_name, import_path)
    PRIMITIVE_TYPES = {'String', 'int', 'double', 'bool', 'DateTime'}
    
    for field in field_list:
        field_name = field['name']
        field_type = field['type']
        capitalized_name = to_pascal_case_preserve(field_name)
        
        if field_name == 'id':
            from_dto_fields.append(f"      id: UniqueId.fromUniqueString(dto.id)")
            to_dto_fields.append(f"      id: entity.id.getOrCrash()")
        else:
            # Check if field type is complex (List<T> or domain model) - use mapper
            if '<' in field_type:
                # List<ModelName> - use mapper.toDomainList/toDtoList
                base_type, generic_type = parse_field_type(field_type)
                if generic_type and generic_type[0].isupper() and generic_type not in PRIMITIVE_TYPES:
                    # Find folder name for this class
                    if generic_type in models_with_classes.values():
                        for folder_name, class_name in models_with_classes.items():
                            if class_name == generic_type:
                                mapper_class_name = f"{class_name}Mapper"
                                mapper_var_name = f"_{pascal_case_to_camel_case(class_name)}Mapper"
                                mapper_import = f"package:{project_name}/{domain_folder}/{folder_name}/infrastructure/{folder_name}_mapper.dart"
                                
                                # Check if already added
                                if not any(m[0] == mapper_class_name for m in mapper_dependencies):
                                    mapper_dependencies.append((mapper_class_name, mapper_var_name, mapper_import))
                                
                                from_dto_fields.append(f"      {field_name}: {mapper_var_name}.toDomainList(dto.{field_name})")
                                to_dto_fields.append(f"      {field_name}: {mapper_var_name}.toDtoList(entity.{field_name})")
                                break
                    else:
                        # Fallback: direct assignment (should not happen if validation worked)
                        from_dto_fields.append(f"      {field_name}: dto.{field_name}")
                        to_dto_fields.append(f"      {field_name}: entity.{field_name}")
                else:
                    # Primitive list, direct assignment
                    from_dto_fields.append(f"      {field_name}: dto.{field_name}")
                    to_dto_fields.append(f"      {field_name}: entity.{field_name}")
            elif field_type and field_type[0].isupper() and field_type not in PRIMITIVE_TYPES:
                # Domain model (PascalCase, not primitive) - use mapper.toDomain/toDto
                if field_type in models_with_classes.values():
                    for folder_name, class_name in models_with_classes.items():
                        if class_name == field_type:
                            mapper_class_name = f"{class_name}Mapper"
                            mapper_var_name = f"_{pascal_case_to_camel_case(class_name)}Mapper"
                            mapper_import = f"package:{project_name}/{domain_folder}/{folder_name}/infrastructure/{folder_name}_mapper.dart"
                            
                            # Check if already added
                            if not any(m[0] == mapper_class_name for m in mapper_dependencies):
                                mapper_dependencies.append((mapper_class_name, mapper_var_name, mapper_import))
                            
                            from_dto_fields.append(f"      {field_name}: {mapper_var_name}.toDomain(dto.{field_name})")
                            to_dto_fields.append(f"      {field_name}: {mapper_var_name}.toDto(entity.{field_name})")
                            break
                else:
                    # Fallback: direct assignment (should not happen if validation worked)
                    from_dto_fields.append(f"      {field_name}: dto.{field_name}")
                    to_dto_fields.append(f"      {field_name}: entity.{field_name}")
            else:
                # Simple type - use ValueObject
                from_dto_fields.append(f"      {field_name}: {capitalized_name}(dto.{field_name})")
                to_dto_fields.append(f"      {field_name}: entity.{field_name}.getOrCrash()")
    
    from_dto_fields_str = ",\n".join(from_dto_fields)
    to_dto_fields_str = ",\n".join(to_dto_fields)
    
    # Create Service (Retrofit)
    generate_file(project_name, infra_dir, "domain/domain_service_template.jinja", f"{entity_folder_name}_service.dart", {
        "entity_name": entity_class_name,  # Use class name for template (PascalCase)
        "file_name": entity_folder_name,  # Use folder name for file references (snake_case)
        "entity_name_camel": pascal_case_to_camel_case(entity_class_name),  # camelCase for variable names
        "kebab_name": pascal_case_to_kebab_case(entity_class_name),  # kebab-case for API routes
        "import_prefix": import_prefix
    })
    
    # Create Mapper
    # Build mapper imports and constructor parameters
    mapper_imports = "\n".join([f"import '{imp}';" for _, _, imp in mapper_dependencies])
    if mapper_dependencies:
        mapper_constructor_params = ",\n".join([f"    this.{var_name}" for _, var_name, _ in mapper_dependencies])
    else:
        mapper_constructor_params = ""
    mapper_fields = "\n".join([f"  final {class_name} {var_name};" for class_name, var_name, _ in mapper_dependencies])
    
    generate_file(project_name, infra_dir, "domain/domain_mapper_template.jinja", f"{entity_folder_name}_mapper.dart", {
        "entity_name": entity_class_name,  # Use class name for template (PascalCase)
        "file_name": entity_folder_name,  # Use folder name for file references (snake_case)
        "import_prefix": import_prefix,
        "from_dto_fields": from_dto_fields_str,
        "to_dto_fields": to_dto_fields_str,
        "mapper_imports": mapper_imports,
        "mapper_fields": mapper_fields,
        "mapper_constructor_params": mapper_constructor_params
    })
    
    # Create Repository (uses Service + Mapper)
    repo_import = f"""import 'package:{project_name}/{import_prefix}/model/{entity_folder_name}.dart';
import 'package:{project_name}/{import_prefix}/model/{entity_folder_name}_failure.dart';
import 'package:{project_name}/{import_prefix}/model/i_{entity_folder_name}_repository.dart';
import 'package:{project_name}/{import_prefix}/infrastructure/{entity_folder_name}_service.dart';
import 'package:{project_name}/{import_prefix}/infrastructure/{entity_folder_name}_mapper.dart';
"""
    generate_file(project_name, infra_dir, "domain/domain_repository_template.jinja", f"{entity_folder_name}_repository.dart", {
        "entity_name": entity_class_name,  # Use class name for template (PascalCase)
        "file_name": entity_folder_name,  # Use folder name for file references (snake_case)
        "import_prefix": import_prefix,
        "repo_import": repo_import
    })
