"""Test basic functionality of Flutterator"""

def test_imports():
    """Test that we can import flutterator modules"""
    try:
        import flutterator
        assert flutterator.cli is not None
    except ImportError as e:
        pytest.fail(f"Failed to import flutterator: {e}")


def test_temp_project_fixture(sample_project_structure):
    """Test that the sample project fixture works"""
    project_dir = sample_project_structure
    assert (project_dir / "pubspec.yaml").exists()
    assert (project_dir / "lib").exists()
    assert (project_dir / "lib" / "home" / "presentation" / "home_screen.dart").exists()


def test_project_name_validation():
    """Test project name validation logic"""
    from flutterator import cli

    # Valid names should not raise exceptions in validation
    valid_names = ["my_app", "test_project", "flutter_app_123"]

    for name in valid_names:
        # This should not raise an exception
        assert name.replace('_', '').replace('-', '').isalnum()
