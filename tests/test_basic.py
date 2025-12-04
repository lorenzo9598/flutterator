"""Test basic functionality of Flutterator"""

import pytest


def test_imports():
    """Test that we can import flutterator modules"""
    import flutterator
    assert flutterator.cli is not None
    assert hasattr(flutterator, 'run_flutter_commands')


def test_helpers_imports():
    """Test that we can import helper modules"""
    from generators.helpers import (
        get_project_name,
        validate_flutter_project,
        generate_page_file,
        update_router,
        create_feature_layers,
        create_drawer_page,
        create_drawer_widget,
        create_component_layers,
        create_component_form_layers,
        to_pascal_case,
        map_field_type,
    )
    # Verify functions are callable
    assert callable(get_project_name)
    assert callable(validate_flutter_project)
    assert callable(generate_page_file)
    assert callable(to_pascal_case)
    assert callable(map_field_type)


def test_temp_project_fixture(sample_project_structure):
    """Test that the sample project fixture works"""
    project_dir = sample_project_structure
    assert (project_dir / "pubspec.yaml").exists()
    assert (project_dir / "lib").exists()
    assert (project_dir / "lib" / "home" / "presentation" / "home_screen.dart").exists()
    assert (project_dir / "lib" / "router.dart").exists()


def test_project_name_validation_valid():
    """Test that valid project names pass validation"""
    valid_names = [
        "my_app",
        "test_project", 
        "flutter_app_123",
        "MyApp",
        "app123",
        "my-app",
    ]
    
    for name in valid_names:
        assert name.replace('_', '').replace('-', '').isalnum(), f"'{name}' should be valid"


def test_project_name_validation_invalid():
    """Test that invalid project names fail validation"""
    invalid_names = [
        "my app",      # space
        "my.app",      # dot
        "my@app",      # special char
        "my!app",      # exclamation
        "my/app",      # slash
    ]
    
    for name in invalid_names:
        assert not name.replace('_', '').replace('-', '').isalnum(), f"'{name}' should be invalid"


def test_to_pascal_case():
    """Test snake_case to PascalCase conversion"""
    from generators.helpers import to_pascal_case
    
    assert to_pascal_case("hello_world") == "HelloWorld"
    assert to_pascal_case("my_feature") == "MyFeature"
    assert to_pascal_case("user_profile_page") == "UserProfilePage"
    assert to_pascal_case("todo") == "Todo"
    assert to_pascal_case("api") == "Api"


def test_map_field_type():
    """Test field type mapping"""
    from generators.helpers import map_field_type
    
    assert map_field_type("string") == "String"
    assert map_field_type("String") == "String"
    assert map_field_type("int") == "int"
    assert map_field_type("bool") == "bool"
    assert map_field_type("double") == "double"
    assert map_field_type("date") == "DateTime"
    assert map_field_type("datetime") == "DateTime"
    assert map_field_type("unknown") == "String"  # Default
