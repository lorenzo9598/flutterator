"""Utility functions for Flutterator"""


def to_pascal_case(snake_str: str) -> str:
    """Convert snake_case to PascalCase"""
    return ''.join(word.capitalize() for word in snake_str.split('_'))


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


def map_field_type(field_type: str) -> str:
    """Map field type from string to Dart type"""
    type_mapping = {
        'string': 'String',
        'int': 'int',
        'double': 'double',
        'bool': 'bool',
        'date': 'DateTime',
        'datetime': 'DateTime',
    }
    return type_mapping.get(field_type.lower(), 'String')

