"""Utility functions for Flutterator"""

from typing import Optional, Set


def to_pascal_case(snake_str: str) -> str:
    """Convert snake_case to PascalCase"""
    return ''.join(word.capitalize() for word in snake_str.split('_'))


def to_camel_case(snake_str: str) -> str:
    """
    Convert snake_case to camelCase.
    
    Examples:
        todo_item → todoItem
        note → note
    """
    words = snake_str.split('_')
    return words[0] + ''.join(word.capitalize() for word in words[1:])


def pascal_case_to_camel_case(pascal_str: str) -> str:
    """
    Convert PascalCase to camelCase.
    
    Examples:
        TodoItem → todoItem
        Note → note
    """
    if not pascal_str:
        return pascal_str
    return pascal_str[0].lower() + pascal_str[1:]


def to_pascal_case_preserve(name: str) -> str:
    """
    Convert camelCase/snake_case to PascalCase, preserving internal capital letters.
    
    - If name is snake_case → uses to_pascal_case()
    - If name is already PascalCase → returns as-is
    - If name is camelCase → converts first letter to uppercase, preserves rest
    
    Examples:
        inviteCode → InviteCode
        invite_code → InviteCode
        InviteCode → InviteCode
        userName → UserName
        apiKey → ApiKey
        httpStatusCode → HttpStatusCode
    """
    if not name:
        return name
    
    # Check if already PascalCase (starts with uppercase and has no underscores)
    if name[0].isupper() and '_' not in name:
        return name
    
    # Check if snake_case (contains underscores)
    if '_' in name:
        return to_pascal_case(name)
    
    # Otherwise, it's camelCase - capitalize first letter, preserve rest
    return name[0].upper() + name[1:] if name else name


def pascal_case_to_snake_case(pascal_str: str) -> str:
    """
    Convert PascalCase to snake_case.
    
    Examples:
        NoteItem → note_item
        Note → note
        HTTPRequest → http_request
    """
    if not pascal_str:
        return pascal_str
    
    # Insert underscore before uppercase letters (except the first one)
    result = pascal_str[0].lower()
    for char in pascal_str[1:]:
        if char.isupper():
            result += '_' + char.lower()
        else:
            result += char
    
    return result


def pascal_case_to_kebab_case(pascal_str: str) -> str:
    """
    Convert PascalCase to kebab-case.
    
    Examples:
        TodoItem → todo-item
        Note → note
        HTTPRequest → http-request
    """
    if not pascal_str:
        return pascal_str
    
    # Insert hyphen before uppercase letters (except the first one)
    result = pascal_str[0].lower()
    for char in pascal_str[1:]:
        if char.isupper():
            result += '-' + char.lower()
        else:
            result += char
    
    return result


PRIMITIVE_TYPES = {'String', 'int', 'double', 'bool', 'DateTime'}
KNOWN_VALUE_OBJECTS = {'UniqueId'}


def get_form_field_metadata(base_type: str, field_name: str, known_enums: Optional[Set[str]] = None) -> dict:
    """Return UI-control and code-generation metadata for a form field.

    The returned dict contains:
        control_type       – 'text' | 'number' | 'checkbox' | 'date' | 'dropdown'
        keyboard_type      – Dart TextInputType expression (only for 'number')
        validator_input_expr – Dart expression converting the validator param to T
        bloc_parse_expr    – Dart expression converting event param to T in bloc handler
        initial_value_expr – Dart literal for FormState.initial()
        mapped_field_type  – Dart type string for ValueFailure<T>
        event_param_type   – Dart type of the event constructor parameter
        event_param_name   – name of the event constructor parameter
        has_value_object   – whether the field is wrapped in a ValueObject
        is_enum            – True when the field is an enum
        enum_class         – enum class name (only when is_enum)
    """
    _enums = known_enums or set()
    is_enum = base_type in _enums

    if is_enum:
        return {
            'control_type': 'dropdown',
            'keyboard_type': '',
            'validator_input_expr': '',
            'bloc_parse_expr': f'event.{field_name}Value',
            'initial_value_expr': f'{base_type}.values.first',
            'mapped_field_type': base_type,
            'event_param_type': base_type,
            'event_param_name': f'{field_name}Value',
            'has_value_object': False,
            'is_enum': True,
            'enum_class': base_type,
        }

    dart_type = map_field_type(base_type)

    if dart_type == 'bool':
        return {
            'control_type': 'checkbox',
            'keyboard_type': '',
            'validator_input_expr': 'value ?? false',
            'bloc_parse_expr': f'event.{field_name}Value',
            'initial_value_expr': 'false',
            'mapped_field_type': 'bool',
            'event_param_type': 'bool',
            'event_param_name': f'{field_name}Value',
            'has_value_object': True,
            'is_enum': False,
            'enum_class': '',
        }

    if dart_type == 'DateTime':
        return {
            'control_type': 'date',
            'keyboard_type': '',
            'validator_input_expr': 'value ?? DateTime(0)',
            'bloc_parse_expr': f'event.{field_name}Value',
            'initial_value_expr': 'DateTime.now()',
            'mapped_field_type': 'DateTime',
            'event_param_type': 'DateTime',
            'event_param_name': f'{field_name}Value',
            'has_value_object': True,
            'is_enum': False,
            'enum_class': '',
        }

    if dart_type == 'int':
        return {
            'control_type': 'number',
            'keyboard_type': 'TextInputType.number',
            'validator_input_expr': "int.tryParse(value ?? '') ?? 0",
            'bloc_parse_expr': f'int.tryParse(event.{field_name}Str) ?? 0',
            'initial_value_expr': '0',
            'mapped_field_type': 'int',
            'event_param_type': 'String',
            'event_param_name': f'{field_name}Str',
            'has_value_object': True,
            'is_enum': False,
            'enum_class': '',
        }

    if dart_type == 'double':
        return {
            'control_type': 'number',
            'keyboard_type': 'const TextInputType.numberWithOptions(decimal: true)',
            'validator_input_expr': "double.tryParse(value ?? '') ?? 0.0",
            'bloc_parse_expr': f'double.tryParse(event.{field_name}Str) ?? 0.0',
            'initial_value_expr': '0.0',
            'mapped_field_type': 'double',
            'event_param_type': 'String',
            'event_param_name': f'{field_name}Str',
            'has_value_object': True,
            'is_enum': False,
            'enum_class': '',
        }

    # Default: String
    return {
        'control_type': 'text',
        'keyboard_type': '',
        'validator_input_expr': "value ?? ''",
        'bloc_parse_expr': f'event.{field_name}Str',
        'initial_value_expr': "''",
        'mapped_field_type': 'String',
        'event_param_type': 'String',
        'event_param_name': f'{field_name}Str',
        'has_value_object': True,
        'is_enum': False,
        'enum_class': '',
    }


def _is_domain_model(t: str, known_enums: Optional[Set[str]] = None) -> bool:
    """Check if a type is a domain model (PascalCase, not a primitive, known VO, or enum)."""
    if not t or not t[0].isupper():
        return False
    if t in PRIMITIVE_TYPES or t in KNOWN_VALUE_OBJECTS:
        return False
    if known_enums and t in known_enums:
        return False
    return True


def _dto_for_single_type(t: str, known_enums: Optional[Set[str]] = None) -> str:
    """Map a single (non-generic) type to its DTO equivalent."""
    if t in PRIMITIVE_TYPES:
        return t
    if t in KNOWN_VALUE_OBJECTS:
        return 'String'
    if known_enums and t in known_enums:
        return 'String'
    if t and t[0].isupper():
        return f"{t}Dto"
    return t


def map_field_type(field_type: str) -> str:
    """
    Map field type from string to Dart type.
    Supports complex types like List<ModelName>, Option<String>, Map<K, V>.
    For DTOs, use map_field_type_to_dto() instead.
    """
    if '<' in field_type and '>' in field_type:
        return field_type
    
    type_mapping = {
        'string': 'String',
        'int': 'int',
        'double': 'double',
        'bool': 'bool',
        'date': 'DateTime',
        'datetime': 'DateTime',
    }
    return type_mapping.get(field_type.lower(), field_type)


def map_field_type_to_dto(field_type: str, known_enums: Optional[Set[str]] = None) -> str:
    """
    Map field type from string to Dart type for DTOs.
    
    Conversions:
        Type?           -> Type? (nullable). UniqueId? -> String?, Model? -> ModelDto?
        Enum            -> String (when known_enums is provided and type is in set)
        Option<T>       -> T?  (nullable, for static templates). If T is domain model, TDto?
        List<Model>     -> List<ModelDto>
        Set<Model>      -> Set<ModelDto>
        Map<K, V>       -> Map<KDto, VDto> (only domain models get Dto suffix)
        UniqueId        -> String
        DomainModel     -> DomainModelDto
        primitives      -> as-is
    """
    import re
    
    # Nullable suffix: Type? -> DtoType? (including List<T>? -> List<TDto>?)
    if field_type.endswith('?'):
        base = field_type[:-1]
        if '<' in base and '>' in base:
            return f"{map_field_type_to_dto(base, known_enums)}?"
        dto_base = _dto_for_single_type(base, known_enums)
        return f"{dto_base}?"
    
    if '<' in field_type and '>' in field_type:
        # Option<T> -> T? (kept for backward compat with static templates)
        option_match = re.match(r'^Option\s*<\s*(\w+)\s*>$', field_type)
        if option_match:
            inner = option_match.group(1)
            dto_inner = _dto_for_single_type(inner, known_enums)
            return f"{dto_inner}?"
        
        # Map<K, V>
        map_match = re.match(r'^(\w+)\s*<\s*(\w+)\s*,\s*(\w+)\s*>$', field_type)
        if map_match:
            base = map_match.group(1)
            key_type = map_match.group(2)
            val_type = map_match.group(3)
            dto_key = _dto_for_single_type(key_type, known_enums)
            dto_val = _dto_for_single_type(val_type, known_enums)
            return f"{base}<{dto_key}, {dto_val}>"
        
        # Single-param generic: List<T>, Set<T>
        single_match = re.match(r'^(\w+)\s*<\s*(\w+)\s*>$', field_type)
        if single_match:
            base = single_match.group(1)
            inner = single_match.group(2)
            dto_inner = _dto_for_single_type(inner, known_enums)
            return f"{base}<{dto_inner}>"
        
        return field_type
    
    # UniqueId -> String in DTO
    if field_type in KNOWN_VALUE_OBJECTS:
        return 'String'
    
    # Enum -> String in DTO
    if known_enums and field_type in known_enums:
        return 'String'
    
    # Domain models -> ModelDto
    if _is_domain_model(field_type, known_enums):
        return f"{field_type}Dto"
    
    return map_field_type(field_type)
