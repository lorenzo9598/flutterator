"""Validation functions for Flutterator CLI input"""

import re
from typing import Optional, List, Tuple, Dict
from pathlib import Path
from .feature import find_domain_models, find_domain_models_with_class_names, find_enums
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

# Known value object types (no domain model lookup needed)
KNOWN_VALUE_OBJECT_TYPES = {
    'UniqueId'
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


def parse_field_type(field_type: str) -> Tuple[str, Optional[str], Optional[str]]:
    """
    Parse a field type, handling generics like List<NoteItem> and Map<String, int>.
    
    Args:
        field_type: The field type string (e.g., "List<NoteItem>", "Map<String, int>", "string")
        
    Returns:
        Tuple of (base_type, generic_param1, generic_param2).
        generic_param1/2 are None if not a generic type.
        For Map<K, V>: returns (Map, K, V).
        For List<T>/Set<T>/Option<T>: returns (List, T, None).
    """
    field_type = field_type.strip()
    
    # Two-param generics (e.g., Map<String, int>)
    two_param_match = re.match(r'^(\w+)\s*<\s*(\w+)\s*,\s*(\w+)\s*>$', field_type)
    if two_param_match:
        return two_param_match.group(1), two_param_match.group(2), two_param_match.group(3)
    
    # Single-param generics (e.g., List<NoteItem>)
    single_param_match = re.match(r'^(\w+)\s*<\s*(\w+)\s*>$', field_type)
    if single_param_match:
        return single_param_match.group(1), single_param_match.group(2), None
    
    return field_type, None, None


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
    
    # Detect nullable suffix (e.g., String?, int?, SomeModel?)
    is_nullable = field_type.endswith('?')
    if is_nullable:
        base_field_type = field_type[:-1]
    else:
        base_field_type = field_type
    
    base_type, generic_param1, generic_param2 = parse_field_type(base_field_type)
    
    base_type_lower = base_type.lower()
    
    NORMALIZE_PRIMITIVE = {
        'string': 'String',
        'datetime': 'DateTime',
        'date': 'DateTime',
        'bool': 'bool',
        'Bool': 'bool',
    }
    
    def _normalize_primitive(t: str) -> str:
        return NORMALIZE_PRIMITIVE.get(t.lower(), t)
    
    def _resolve_generic_type(gtype: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """Resolve a generic type parameter: primitive, known VO, enum, or domain model."""
        # Dart top types (e.g. Map<String, dynamic> for JSON blobs)
        if gtype.lower() == 'dynamic':
            return True, None, 'dynamic'
        if gtype.lower() == 'object':
            return True, None, 'Object'
        if gtype.lower() in VALID_PRIMITIVE_TYPES:
            return True, None, _normalize_primitive(gtype)
        if gtype in KNOWN_VALUE_OBJECT_TYPES:
            return True, None, gtype
        if lib_path:
            known_enums = find_enums(lib_path, domain_folder)
            if gtype in known_enums:
                return True, None, gtype
            available_models = find_domain_models(lib_path, domain_folder)
            models_with_classes = find_domain_models_with_class_names(lib_path, domain_folder)
            if gtype in available_models:
                return True, None, models_with_classes[gtype]['class_name']
            for _stem, info in models_with_classes.items():
                if info['class_name'] == gtype:
                    return True, None, gtype
            available_str = ', '.join([f"{k} ({v['class_name']})" for k, v in models_with_classes.items()]) if models_with_classes else 'none'
            return False, f"Model '{gtype}' not found in domain. Available models: {available_str}. Create it first using: flutterator add-domain --name {gtype.lower()}", None
        return False, f"Model '{gtype}' cannot be validated (lib_path not provided). Please ensure the project path is correct.", None
    
    def _with_nullable(normalized: str) -> str:
        return f"{normalized}?" if is_nullable else normalized
    
    # --- UniqueId (known value object, no generic) ---
    if base_type in KNOWN_VALUE_OBJECT_TYPES:
        if generic_param1:
            return False, f"'{base_type}' does not take generic parameters", None
        return True, None, _with_nullable(base_type)
    
    # --- Primitive types ---
    if base_type_lower in VALID_PRIMITIVE_TYPES:
        if generic_param1:
            return False, f"Primitive type '{base_type}' cannot have generic parameters", None
        return True, None, _with_nullable(_normalize_primitive(base_type))
    
    # --- Collection types: List<T>, Set<T>, Map<K, V> ---
    if base_type_lower in VALID_COLLECTION_TYPES:
        normalized_base = {'list': 'List', 'set': 'Set', 'map': 'Map'}.get(base_type_lower, base_type)
        
        if normalized_base == 'Map':
            if not generic_param1 or not generic_param2:
                return False, f"Map requires two generic parameters (e.g., Map<String, int>)", None
            ok1, err1, norm_key = _resolve_generic_type(generic_param1)
            if not ok1:
                return False, f"Invalid Map key type: {err1}", None
            ok2, err2, norm_val = _resolve_generic_type(generic_param2)
            if not ok2:
                return False, f"Invalid Map value type: {err2}", None
            return True, None, _with_nullable(f"Map<{norm_key}, {norm_val}>")
        else:
            if not generic_param1:
                return False, f"Collection type '{base_type}' requires a generic parameter (e.g., {normalized_base}<ItemType>)", None
            if generic_param2:
                return False, f"'{normalized_base}' takes only one generic parameter", None
            ok, err, normalized_inner = _resolve_generic_type(generic_param1)
            if not ok:
                return False, err, None
            return True, None, _with_nullable(f"{normalized_base}<{normalized_inner}>")
    
    # --- Enum type (PascalCase, found in domain/enums/) ---
    if base_type[0].isupper() and base_type_lower not in VALID_PRIMITIVE_TYPES and lib_path:
        known_enums = find_enums(lib_path, domain_folder)
        if base_type in known_enums:
            if generic_param1:
                return False, f"Enum type '{base_type}' cannot have generic parameters.", None
            return True, None, _with_nullable(base_type)
    
    # --- Domain model (PascalCase, not a known type) ---
    if base_type[0].isupper() and base_type_lower not in VALID_PRIMITIVE_TYPES:
        if generic_param1:
            return False, f"Domain model type '{base_type}' cannot have generic parameters directly. Use List<{base_type}> for lists.", None
        
        if lib_path:
            available_models = find_domain_models(lib_path, domain_folder)
            models_with_classes = find_domain_models_with_class_names(lib_path, domain_folder)
            
            for _stem, info in models_with_classes.items():
                if info['class_name'] == base_type:
                    return True, None, _with_nullable(base_type)
            
            if base_type in available_models:
                class_name = models_with_classes[base_type]['class_name']
                return True, None, _with_nullable(class_name)
            
            available_str = ', '.join([f"{k} ({v['class_name']})" for k, v in models_with_classes.items()]) if models_with_classes else 'none'
            return False, f"Model '{base_type}' not found in domain. Available models: {available_str}. Create it first using: flutterator add-domain --name {base_type.lower()}", None
        
        return False, f"Model '{base_type}' cannot be validated (lib_path not provided). Please ensure the project path is correct.", None
    
    # --- Unknown type ---
    suggestions = []
    if base_type_lower.startswith('str'):
        suggestions.append('String')
    elif base_type_lower.startswith('int'):
        suggestions.append('int')
    elif base_type_lower.startswith('doub') or base_type_lower.startswith('floa'):
        suggestions.append('double')
    elif base_type_lower.startswith('bool'):
        suggestions.append('bool')
    elif base_type_lower.startswith('opt'):
        suggestions.append('String? (use Type? for nullable)')
    elif base_type_lower.startswith('uni'):
        suggestions.append('UniqueId')
    
    suggestion_msg = f" Did you mean '{suggestions[0]}'?" if suggestions else ""
    return False, f"Unknown type '{field_type}'. Valid types: String, int, double, bool, DateTime, UniqueId, dynamic, Object, List<T>, Set<T>, Map<K,V> (e.g. Map<String, dynamic>), enum names, or domain model names (PascalCase). Nullable: String?, Model?, List<T>?, Map<K,V>?, etc.{suggestion_msg}", None


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
    Handles commas inside angle brackets (e.g., Map<String, int>).
    
    Args:
        fields_str: Fields string in format "name:type,name:type"
        
    Returns:
        List of (field_name, field_type) tuples
    """
    # Split on commas that are NOT inside angle brackets
    tokens = []
    current = []
    depth = 0
    for ch in fields_str:
        if ch == '<':
            depth += 1
            current.append(ch)
        elif ch == '>':
            depth -= 1
            current.append(ch)
        elif ch == ',' and depth == 0:
            tokens.append(''.join(current))
            current = []
        else:
            current.append(ch)
    if current:
        tokens.append(''.join(current))
    
    fields = []
    for field_str in tokens:
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

