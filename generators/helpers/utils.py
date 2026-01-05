"""Utility functions for Flutterator"""


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


def map_field_type(field_type: str) -> str:
    """
    Map field type from string to Dart type.
    Supports complex types like List<ModelName>.
    For DTOs, use map_field_type_to_dto() instead.
    """
    # Handle generic types (e.g., List<NoteItem>)
    if '<' in field_type and '>' in field_type:
        # Return as-is, assuming it's already in correct format
        return field_type
    
    type_mapping = {
        'string': 'String',
        'int': 'int',
        'double': 'double',
        'bool': 'bool',
        'date': 'DateTime',
        'datetime': 'DateTime',
    }
    return type_mapping.get(field_type.lower(), field_type)  # Return original if not found


def map_field_type_to_dto(field_type: str) -> str:
    """
    Map field type from string to Dart type for DTOs.
    Converts List<ModelName> to List<ModelNameDto>.
    
    Args:
        field_type: Field type (e.g., "List<TodoItem>", "string", "TodoItem")
    
    Returns:
        Dart type for DTO (e.g., "List<TodoItemDto>", "String", "TodoItemDto")
    """
    # Handle generic types (e.g., List<NoteItem> -> List<NoteItemDto>)
    if '<' in field_type and '>' in field_type:
        import re
        # Extract base type and generic type
        match = re.match(r'^(\w+)\s*<\s*(\w+)\s*>$', field_type)
        if match:
            base_type = match.group(1)
            generic_type = match.group(2)
            # Convert generic type to DTO (e.g., TodoItem -> TodoItemDto)
            return f"{base_type}<{generic_type}Dto>"
        # If regex doesn't match, return as-is (shouldn't happen)
        return field_type
    
    # Handle domain models (PascalCase, not primitives)
    PRIMITIVE_TYPES = {'String', 'int', 'double', 'bool', 'DateTime'}
    if field_type not in PRIMITIVE_TYPES and field_type and field_type[0].isupper():
        # It's a domain model, convert to DTO
        return f"{field_type}Dto"
    
    # For primitives, use map_field_type
    return map_field_type(field_type)
