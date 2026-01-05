"""Validation functions for Flutterator CLI input"""

import re
from typing import Optional, List, Tuple, Dict
from pathlib import Path
from .feature import find_domain_models, find_domain_models_with_class_names
from .utils import to_pascal_case


# Dart reserved keywords
DART_RESERVED_KEYWORDS = {
    'abstract', 'as', 'assert', 'async', 'await', 'break', 'case', 'catch',
    'class', 'const', 'continue', 'covariant', 'default', 'deferred', 'do',
    'dynamic', 'else', 'enum', 'export', 'extends', 'extension', 'external',
    'factory', 'false', 'final', 'finally', 'for', 'Function', 'get', 'hide',
    'if', 'implements', 'import', 'in', 'interface', 'is', 'library', 'mixin',
    'new', 'null', 'on', 'operator', 'part', 'required', 'rethrow', 'return',
    'set', 'show', 'static', 'super', 'switch', 'sync', 'this', 'throw',
    'true', 'try', 'typedef', 'var', 'void', 'while', 'with', 'yield'
}

# Valid Dart primitive types
VALID_PRIMITIVE_TYPES = {
    'string', 'String', 'int', 'double', 'bool', 'Bool', 'DateTime', 'datetime', 'date'
}

# Valid Dart collection types (without generic parameters)
VALID_COLLECTION_TYPES = {
    'List', 'list', 'Set', 'set', 'Map', 'map'
}


def validate_field_name(field_name: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a field name.
    
    Args:
        field_name: The field name to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not field_name:
        return False, "Field name cannot be empty"
    
    # Check for reserved keywords
    if field_name.lower() in DART_RESERVED_KEYWORDS:
        return False, f"'{field_name}' is a Dart reserved keyword. Please use a different name."
    
    # Check for valid identifier characters (letters, numbers, underscore)
    # Must start with letter or underscore
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', field_name):
        return False, f"Invalid field name '{field_name}'. Field names must start with a letter or underscore and contain only letters, numbers, and underscores."
    
    return True, None


def parse_field_type(field_type: str) -> Tuple[str, Optional[str]]:
    """
    Parse a field type, handling generics like List<NoteItem>.
    
    Args:
        field_type: The field type string (e.g., "List<NoteItem>", "string", "int")
        
    Returns:
        Tuple of (base_type, generic_type). generic_type is None if not a generic type.
    """
    field_type = field_type.strip()
    
    # Check for generic types (e.g., List<NoteItem>)
    generic_match = re.match(r'^(\w+)\s*<\s*(\w+)\s*>$', field_type)
    if generic_match:
        base_type = generic_match.group(1)
        generic_type = generic_match.group(2)
        return base_type, generic_type
    
    return field_type, None


def validate_field_type(field_type: str, lib_path: Optional[Path] = None, domain_folder: str = "domain") -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Validate a field type.
    
    Args:
        field_type: The field type to validate
        lib_path: Optional path to lib/ directory for checking domain models
        domain_folder: Domain folder name (default: "domain")
        
    Returns:
        Tuple of (is_valid, error_message, normalized_type)
        normalized_type is the type as it should appear in Dart code
    """
    if not field_type:
        return False, "Field type cannot be empty", None
    
    field_type = field_type.strip()
    base_type, generic_type = parse_field_type(field_type)
    
    # Normalize base type
    base_type_lower = base_type.lower()
    
    # Check if it's a valid primitive type
    if base_type_lower in VALID_PRIMITIVE_TYPES:
        normalized_base = {
            'string': 'String',
            'datetime': 'DateTime',
            'date': 'DateTime',
            'bool': 'bool',
            'Bool': 'bool'
        }.get(base_type_lower, base_type)
        
        if generic_type:
            return False, f"Primitive type '{base_type}' cannot have generic parameters", None
        
        return True, None, normalized_base
    
    # Check if it's a valid collection type
    if base_type_lower in VALID_COLLECTION_TYPES:
        normalized_base = {
            'list': 'List',
            'set': 'Set',
            'map': 'Map'
        }.get(base_type_lower, base_type)
        
        if not generic_type:
            return False, f"Collection type '{base_type}' requires a generic parameter (e.g., List<ItemType>)", None
        
        # Validate generic type
        if generic_type.lower() in VALID_PRIMITIVE_TYPES:
            # Generic type is a primitive
            normalized_generic = {
                'string': 'String',
                'datetime': 'DateTime',
                'date': 'DateTime',
                'bool': 'bool'
            }.get(generic_type.lower(), generic_type)
            normalized_type = f"{normalized_base}<{normalized_generic}>"
            return True, None, normalized_type
        
        # Generic type should be a domain model
        # Accept both PascalCase (TodoItem) and snake_case (todo_item)
        if lib_path:
            available_models = find_domain_models(lib_path, domain_folder)
            models_with_classes = find_domain_models_with_class_names(lib_path, domain_folder)
            
            # Check if generic_type is a folder name (snake_case)
            if generic_type in available_models:
                # Convert to PascalCase class name
                class_name = models_with_classes.get(generic_type, to_pascal_case(generic_type))
                normalized_type = f"{normalized_base}<{class_name}>"
                return True, None, normalized_type
            
            # Check if generic_type is a class name (PascalCase)
            if generic_type in models_with_classes.values():
                normalized_type = f"{normalized_base}<{generic_type}>"
                return True, None, normalized_type
            
            # Not found
            available_str = ', '.join([f"{k} ({v})" for k, v in models_with_classes.items()]) if models_with_classes else 'none'
            return False, f"Model '{generic_type}' not found in domain. Available models: {available_str}. Create it first using: flutterator add-domain --name {generic_type.lower()}", None
        
        # If no lib_path, require validation - don't accept unknown models
        return False, f"Model '{generic_type}' cannot be validated (lib_path not provided). Please ensure the project path is correct.", None
    
    # Check if it's a domain model (PascalCase name or snake_case)
    # Accept both PascalCase (TodoItem) and snake_case (todo_item)
    if base_type[0].isupper() and not base_type_lower in VALID_PRIMITIVE_TYPES:
        if generic_type:
            return False, f"Domain model type '{base_type}' cannot have generic parameters directly. Use List<{base_type}> for lists.", None
        
        if lib_path:
            available_models = find_domain_models(lib_path, domain_folder)
            models_with_classes = find_domain_models_with_class_names(lib_path, domain_folder)
            
            # Check if base_type is a class name (PascalCase)
            if base_type in models_with_classes.values():
                return True, None, base_type
            
            # Check if base_type is a folder name (snake_case)
            if base_type in available_models:
                class_name = models_with_classes.get(base_type, to_pascal_case(base_type))
                return True, None, class_name
            
            # Not found
            available_str = ', '.join([f"{k} ({v})" for k, v in models_with_classes.items()]) if models_with_classes else 'none'
            return False, f"Model '{base_type}' not found in domain. Available models: {available_str}. Create it first using: flutterator add-domain --name {base_type.lower()}", None
        
        # If no lib_path, require validation - don't accept unknown models
        return False, f"Model '{base_type}' cannot be validated (lib_path not provided). Please ensure the project path is correct.", None
    
    # Unknown type
    suggestions = []
    if base_type_lower.startswith('str'):
        suggestions.append('string')
    elif base_type_lower.startswith('int'):
        suggestions.append('int')
    elif base_type_lower.startswith('doub') or base_type_lower.startswith('floa'):
        suggestions.append('double')
    elif base_type_lower.startswith('bool'):
        suggestions.append('bool')
    
    suggestion_msg = f" Did you mean '{suggestions[0]}'?" if suggestions else ""
    return False, f"Unknown type '{field_type}'. Valid types: string, int, double, bool, DateTime, List<T>, or domain model names (PascalCase).{suggestion_msg}", None


def validate_entity_name(name: str) -> Tuple[bool, Optional[str]]:
    """
    Validate an entity/model name.
    
    Args:
        name: The entity name to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name:
        return False, "Entity name cannot be empty"
    
    # Check for reserved keywords
    if name.lower() in DART_RESERVED_KEYWORDS:
        return False, f"'{name}' is a Dart reserved keyword. Please use a different name."
    
    # Allow PascalCase, camelCase, snake_case, or kebab-case
    # PascalCase names are preserved as-is (e.g., "NoteItem" stays "NoteItem")
    # snake_case/kebab-case are converted (e.g., "note_item" becomes "note_item" for folder, but entity class uses PascalCase)
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_\-]*$', name):
        return False, f"Invalid entity name '{name}'. Entity names must start with a letter and contain only letters, numbers, underscores, and hyphens."
    
    return True, None


def parse_fields_string(fields_str: str) -> List[Tuple[str, str]]:
    """
    Parse a fields string into a list of (name, type) tuples.
    
    Args:
        fields_str: Fields string in format "name:type,name:type"
        
    Returns:
        List of (field_name, field_type) tuples
    """
    fields = []
    for field_str in fields_str.split(','):
        field_str = field_str.strip()
        if not field_str:
            continue
        
        if ':' not in field_str:
            raise ValueError(f"Invalid field format: '{field_str}'. Expected format: name:type")
        
        parts = field_str.split(':', 1)
        field_name = parts[0].strip()
        field_type = parts[1].strip()
        
        if not field_name:
            raise ValueError(f"Field name cannot be empty in: '{field_str}'")
        if not field_type:
            raise ValueError(f"Field type cannot be empty in: '{field_str}'")
        
        fields.append((field_name, field_type))
    
    return fields

