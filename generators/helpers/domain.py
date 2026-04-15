"""Domain entity generation functions

Domain entities are shared business entities that can be used by multiple features.
They only contain model and infrastructure layers (no application/presentation).
"""

from pathlib import Path
from typing import Optional
from generators.templates.copier import generate_file
import re
from .utils import map_field_type, map_field_type_to_dto, to_pascal_case_preserve, pascal_case_to_kebab_case, pascal_case_to_camel_case, PRIMITIVE_TYPES, KNOWN_VALUE_OBJECTS
from .validation import parse_field_type
from .feature import (
    generate_value_objects_and_validators,
    find_domain_models_with_class_names,
    get_domain_model_class_name,
    find_enums_with_info,
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
    
    # Discover domain models and enums early (needed by VO generation and entity building)
    lib_path = domain_dir.parent.parent if folder else domain_dir.parent
    domain_folder = folder if folder else "domain"
    models_with_classes = find_domain_models_with_class_names(lib_path, domain_folder) if lib_path.exists() else {}
    enums_info = find_enums_with_info(lib_path, domain_folder) if lib_path.exists() else {}
    known_enums = set(enums_info.keys())
    
    def _is_enum(t: str) -> bool:
        return t in known_enums
    
    # Model layer
    model_dir = domain_dir / "model"
    model_dir.mkdir(exist_ok=True)

    # Create value objects and validators
    generate_value_objects_and_validators(import_prefix, field_list, model_dir, project_name, known_enums=known_enums, skip_local_validators=True)
    
    # Create entity (domain model)
    entity_fields = []
    needs_dartz = False
    
    for field in field_list:
        field_name = field['name']
        field_type = field['type']
        is_nullable = field_type.endswith('?')
        base_type_raw = field_type[:-1] if is_nullable else field_type
        
        if field_name == 'id':
            entity_fields.append(f"  required UniqueId id,")
        elif is_nullable and _is_enum(base_type_raw):
            needs_dartz = True
            entity_fields.append(f"  required Option<{base_type_raw}> {field_name},")
        elif is_nullable:
            coll_root, _, _ = parse_field_type(base_type_raw)
            if coll_root.lower() in ('list', 'set', 'map'):
                entity_fields.append(f"  {base_type_raw}? {field_name},")
                continue
            needs_dartz = True
            if base_type_raw in PRIMITIVE_TYPES:
                entity_fields.append(f"  required Option<{to_pascal_case_preserve(field_name)}> {field_name},")
            elif base_type_raw in KNOWN_VALUE_OBJECTS:
                entity_fields.append(f"  required Option<{base_type_raw}> {field_name},")
            else:
                entity_fields.append(f"  required Option<{base_type_raw}> {field_name},")
        elif _is_enum(field_type):
            entity_fields.append(f"  required {field_type} {field_name},")
        elif '<' in field_type:
            entity_fields.append(f"  required {field_type} {field_name},")
        elif field_type in KNOWN_VALUE_OBJECTS:
            entity_fields.append(f"  required {field_type} {field_name},")
        elif field_type in PRIMITIVE_TYPES:
            entity_fields.append(f"  required {to_pascal_case_preserve(field_name)} {field_name},")
        else:
            entity_fields.append(f"  required {field_type} {field_name},")
    
    entity_import = f"import 'package:{project_name}/{import_prefix}/model/value_objects.dart';"
    
    referenced_imports = []
    if needs_dartz:
        referenced_imports.append("import 'package:dartz/dartz.dart';")
    
    def _add_enum_import(enum_name: str) -> None:
        """Add an import for an enum if it exists in the project."""
        info = enums_info.get(enum_name)
        if info:
            ref_import = f"import 'package:{project_name}/{info['folder']}/{info['file_stem']}.dart';"
            if ref_import not in referenced_imports:
                referenced_imports.append(ref_import)
    
    def _add_model_import(class_name: str) -> None:
        """Add an import for a domain model if it exists in the project."""
        for file_stem, model_info in models_with_classes.items():
            if model_info['class_name'] == class_name:
                ref_import = f"import 'package:{project_name}/{domain_folder}/{model_info['folder']}/model/{file_stem}.dart';"
                if ref_import not in referenced_imports:
                    referenced_imports.append(ref_import)
                break
    
    for field in field_list:
        field_type = field['type']
        # Strip nullable suffix for import resolution
        ft = field_type[:-1] if field_type.endswith('?') else field_type
        if '<' in ft:
            base_type, gp1, gp2 = parse_field_type(ft)
            for gp in (gp1, gp2):
                if gp and gp[0].isupper() and gp not in PRIMITIVE_TYPES and gp not in KNOWN_VALUE_OBJECTS:
                    if _is_enum(gp):
                        _add_enum_import(gp)
                    else:
                        _add_model_import(gp)
        elif ft and ft[0].isupper() and ft not in PRIMITIVE_TYPES and ft not in KNOWN_VALUE_OBJECTS:
            if _is_enum(ft):
                _add_enum_import(ft)
            else:
                _add_model_import(ft)
    
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
    
    # Create DTO (convert types to DTO format - List<Model> -> List<ModelDto>, Model -> ModelDto, Enum -> String)
    dto_fields = ",\n".join([f"    required {map_field_type_to_dto(field['type'], known_enums=known_enums)} {field['name']}" for field in field_list])
    
    # Find referenced DTOs and add imports
    referenced_dto_imports = []
    
    for field in field_list:
        field_type = field['type']
        dto_field_type = map_field_type_to_dto(field_type, known_enums=known_enums)
        
        if 'Dto' in dto_field_type:
            for model_match in re.finditer(r'(\w+)Dto', dto_field_type):
                model_name = model_match.group(1)
                for file_stem, model_info in models_with_classes.items():
                    if model_info['class_name'] == model_name:
                        ref_import = f"import 'package:{project_name}/{domain_folder}/{model_info['folder']}/infrastructure/{file_stem}_dto.dart';"
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
    mapper_needs_dartz = False
    
    def _find_mapper_dep(class_name: str):
        """Find and register a mapper dependency for a domain model, return (mapper_var_name, found)."""
        for file_stem, model_info in models_with_classes.items():
            if model_info['class_name'] == class_name:
                mcn = f"{model_info['class_name']}Mapper"
                mvn = f"_{pascal_case_to_camel_case(model_info['class_name'])}Mapper"
                mi = f"package:{project_name}/{domain_folder}/{model_info['folder']}/infrastructure/{file_stem}_mapper.dart"
                if not any(m[0] == mcn for m in mapper_dependencies):
                    mapper_dependencies.append((mcn, mvn, mi))
                return mvn, True
        return None, False
    
    def _is_domain_model_local(t: str) -> bool:
        return bool(t and t[0].isupper() and t not in PRIMITIVE_TYPES and t not in KNOWN_VALUE_OBJECTS and t not in known_enums)
    
    mapper_enum_imports = []
    
    for field in field_list:
        field_name = field['name']
        field_type = field['type']
        capitalized_name = to_pascal_case_preserve(field_name)
        is_nullable = field_type.endswith('?')
        base_type_raw = field_type[:-1] if is_nullable else field_type
        
        if field_name == 'id':
            from_dto_fields.append(f"      id: UniqueId.fromUniqueString(dto.id)")
            to_dto_fields.append(f"      id: entity.id.getOrCrash()")
            continue
        
        # --- Nullable enum (EnumName?) ---
        if is_nullable and _is_enum(base_type_raw):
            mapper_needs_dartz = True
            from_dto_fields.append(f"      {field_name}: dto.{field_name} != null ? some({base_type_raw}.values.byName(dto.{field_name}!)) : none()")
            to_dto_fields.append(f"      {field_name}: entity.{field_name}.fold(() => null, (v) => v.name)")
            info = enums_info.get(base_type_raw)
            if info:
                ei = f"import 'package:{project_name}/{info['folder']}/{info['file_stem']}.dart';"
                if ei not in mapper_enum_imports:
                    mapper_enum_imports.append(ei)
            continue
        
        # --- Nullable Map / List / Set (Dart T?, not Option) ---
        coll_root, cg1, cg2 = parse_field_type(base_type_raw)
        if is_nullable and coll_root.lower() == 'map' and cg1 and cg2:
            if _is_enum(cg2):
                from_dto_fields.append(
                    f"      {field_name}: dto.{field_name} != null ? dto.{field_name}!.map((k, v) => MapEntry(k, {cg2}.values.byName(v))) : null"
                )
                to_dto_fields.append(
                    f"      {field_name}: entity.{field_name} != null ? entity.{field_name}!.map((k, v) => MapEntry(k, v.name)) : null"
                )
                info = enums_info.get(cg2)
                if info:
                    ei = f"import 'package:{project_name}/{info['folder']}/{info['file_stem']}.dart';"
                    if ei not in mapper_enum_imports:
                        mapper_enum_imports.append(ei)
            elif _is_domain_model_local(cg2):
                mvn, found = _find_mapper_dep(cg2)
                if found:
                    from_dto_fields.append(
                        f"      {field_name}: dto.{field_name} != null ? dto.{field_name}!.map((k, v) => MapEntry(k, {mvn}.toDomain(v))) : null"
                    )
                    to_dto_fields.append(
                        f"      {field_name}: entity.{field_name} != null ? entity.{field_name}!.map((k, v) => MapEntry(k, {mvn}.toDto(v))) : null"
                    )
                else:
                    from_dto_fields.append(f"      {field_name}: dto.{field_name}")
                    to_dto_fields.append(f"      {field_name}: entity.{field_name}")
            else:
                from_dto_fields.append(f"      {field_name}: dto.{field_name}")
                to_dto_fields.append(f"      {field_name}: entity.{field_name}")
            continue
        
        if is_nullable and coll_root.lower() in ('list', 'set') and cg1:
            if _is_enum(cg1):
                from_dto_fields.append(
                    f"      {field_name}: dto.{field_name} != null ? dto.{field_name}!.map((e) => {cg1}.values.byName(e)).toList() : null"
                )
                to_dto_fields.append(
                    f"      {field_name}: entity.{field_name} != null ? entity.{field_name}!.map((e) => e.name).toList() : null"
                )
                info = enums_info.get(cg1)
                if info:
                    ei = f"import 'package:{project_name}/{info['folder']}/{info['file_stem']}.dart';"
                    if ei not in mapper_enum_imports:
                        mapper_enum_imports.append(ei)
            elif _is_domain_model_local(cg1):
                mvn, found = _find_mapper_dep(cg1)
                if found:
                    from_dto_fields.append(
                        f"      {field_name}: dto.{field_name} != null ? {mvn}.toDomainList(dto.{field_name}!) : null"
                    )
                    to_dto_fields.append(
                        f"      {field_name}: entity.{field_name} != null ? {mvn}.toDtoList(entity.{field_name}!) : null"
                    )
                else:
                    from_dto_fields.append(f"      {field_name}: dto.{field_name}")
                    to_dto_fields.append(f"      {field_name}: entity.{field_name}")
            else:
                from_dto_fields.append(f"      {field_name}: dto.{field_name}")
                to_dto_fields.append(f"      {field_name}: entity.{field_name}")
            continue
        
        # --- Nullable types (Type?) ---
        if is_nullable:
            mapper_needs_dartz = True
            if base_type_raw in PRIMITIVE_TYPES:
                from_dto_fields.append(f"      {field_name}: dto.{field_name} != null ? some({capitalized_name}(dto.{field_name}!)) : none()")
                to_dto_fields.append(f"      {field_name}: entity.{field_name}.fold(() => null, (v) => v.getOrCrash())")
            elif base_type_raw in KNOWN_VALUE_OBJECTS:
                from_dto_fields.append(f"      {field_name}: dto.{field_name} != null ? some(UniqueId.fromUniqueString(dto.{field_name}!)) : none()")
                to_dto_fields.append(f"      {field_name}: entity.{field_name}.fold(() => null, (v) => v.getOrCrash())")
            elif _is_domain_model_local(base_type_raw):
                mvn, found = _find_mapper_dep(base_type_raw)
                if found:
                    from_dto_fields.append(f"      {field_name}: dto.{field_name} != null ? some({mvn}.toDomain(dto.{field_name}!)) : none()")
                    to_dto_fields.append(f"      {field_name}: entity.{field_name}.fold(() => null, (v) => {mvn}.toDto(v))")
                else:
                    from_dto_fields.append(f"      {field_name}: dto.{field_name} != null ? some(dto.{field_name}!) : none()")
                    to_dto_fields.append(f"      {field_name}: entity.{field_name}.fold(() => null, (v) => v)")
            continue
        
        ft_parse = field_type[:-1] if field_type.endswith('?') else field_type
        base_type, gp1, gp2 = parse_field_type(ft_parse)
        
        # --- Enum (standalone, no generics) ---
        if _is_enum(field_type):
            from_dto_fields.append(f"      {field_name}: {field_type}.values.byName(dto.{field_name})")
            to_dto_fields.append(f"      {field_name}: entity.{field_name}.name")
            info = enums_info.get(field_type)
            if info:
                ei = f"import 'package:{project_name}/{info['folder']}/{info['file_stem']}.dart';"
                if ei not in mapper_enum_imports:
                    mapper_enum_imports.append(ei)
        
        # --- Map<K, V> ---
        elif base_type == 'Map' and gp1 and gp2:
            if _is_enum(gp2):
                from_dto_fields.append(f"      {field_name}: dto.{field_name}.map((k, v) => MapEntry(k, {gp2}.values.byName(v)))")
                to_dto_fields.append(f"      {field_name}: entity.{field_name}.map((k, v) => MapEntry(k, v.name))")
                info = enums_info.get(gp2)
                if info:
                    ei = f"import 'package:{project_name}/{info['folder']}/{info['file_stem']}.dart';"
                    if ei not in mapper_enum_imports:
                        mapper_enum_imports.append(ei)
            elif _is_domain_model_local(gp2):
                mvn, found = _find_mapper_dep(gp2)
                if found:
                    from_dto_fields.append(f"      {field_name}: dto.{field_name}.map((k, v) => MapEntry(k, {mvn}.toDomain(v)))")
                    to_dto_fields.append(f"      {field_name}: entity.{field_name}.map((k, v) => MapEntry(k, {mvn}.toDto(v)))")
                else:
                    from_dto_fields.append(f"      {field_name}: dto.{field_name}")
                    to_dto_fields.append(f"      {field_name}: entity.{field_name}")
            else:
                from_dto_fields.append(f"      {field_name}: dto.{field_name}")
                to_dto_fields.append(f"      {field_name}: entity.{field_name}")
        
        # --- List<T>, Set<T> ---
        elif '<' in ft_parse and gp1:
            if _is_enum(gp1):
                from_dto_fields.append(f"      {field_name}: dto.{field_name}.map((e) => {gp1}.values.byName(e)).toList()")
                to_dto_fields.append(f"      {field_name}: entity.{field_name}.map((e) => e.name).toList()")
                info = enums_info.get(gp1)
                if info:
                    ei = f"import 'package:{project_name}/{info['folder']}/{info['file_stem']}.dart';"
                    if ei not in mapper_enum_imports:
                        mapper_enum_imports.append(ei)
            elif _is_domain_model_local(gp1):
                mvn, found = _find_mapper_dep(gp1)
                if found:
                    from_dto_fields.append(f"      {field_name}: {mvn}.toDomainList(dto.{field_name})")
                    to_dto_fields.append(f"      {field_name}: {mvn}.toDtoList(entity.{field_name})")
                else:
                    from_dto_fields.append(f"      {field_name}: dto.{field_name}")
                    to_dto_fields.append(f"      {field_name}: entity.{field_name}")
            else:
                from_dto_fields.append(f"      {field_name}: dto.{field_name}")
                to_dto_fields.append(f"      {field_name}: entity.{field_name}")
        
        # --- UniqueId ---
        elif field_type in KNOWN_VALUE_OBJECTS:
            from_dto_fields.append(f"      {field_name}: UniqueId.fromUniqueString(dto.{field_name})")
            to_dto_fields.append(f"      {field_name}: entity.{field_name}.getOrCrash()")
        
        # --- Domain model (standalone, no generics) ---
        elif _is_domain_model_local(field_type):
            mvn, found = _find_mapper_dep(field_type)
            if found:
                from_dto_fields.append(f"      {field_name}: {mvn}.toDomain(dto.{field_name})")
                to_dto_fields.append(f"      {field_name}: {mvn}.toDto(entity.{field_name})")
            else:
                from_dto_fields.append(f"      {field_name}: dto.{field_name}")
                to_dto_fields.append(f"      {field_name}: entity.{field_name}")
        
        # --- Primitive type -> ValueObject ---
        else:
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
    extra_mapper_imports = []
    if mapper_needs_dartz:
        extra_mapper_imports.append("import 'package:dartz/dartz.dart';")
    dep_imports = [f"import '{imp}';" for _, _, imp in mapper_dependencies]
    mapper_imports = "\n".join(extra_mapper_imports + mapper_enum_imports + dep_imports)
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
