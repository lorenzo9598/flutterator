"""Utility functions for Flutterator"""


def to_pascal_case(snake_str: str) -> str:
    """Convert snake_case to PascalCase"""
    return ''.join(word.capitalize() for word in snake_str.split('_'))


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

