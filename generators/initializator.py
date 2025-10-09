import click
from pathlib import Path

def initialize_project(lib_path, project_path, has_login):
    remove_default_files(lib_path, project_path)
    click.echo("\n📁 Creating folder structure...")
    create_folder_structure(lib_path, has_login)

def remove_default_files(lib_path, project_path):
     # Remove default main.dart and test files
    default_main = lib_path / "main.dart"
    if default_main.exists():
        default_main.unlink()

    # Remove default test folder if empty or contains only widget_test.dart
    test_path = project_path / "test"
    if test_path.exists():
        widget_test = test_path / "widget_test.dart"
        if widget_test.exists():
            widget_test.unlink()
        # Try to remove the test directory if it's empty
        try:
            test_path.rmdir()
        except OSError:
            pass  # Not empty, leave it be

def create_folder_structure(lib_path, login):
     # Create folder structure
    folders = [
        "apis/clients",
        "apis/common", 
        "apis/core",
        "apis/interceptors",
        "application",
        "infrastructure/core",
        "logging",
        "model/core",
        "presentation/core",
        "presentation/home",
        "presentation/splash",
        "infrastructure/storage"
    ]

    # Add auth folders if login is enabled
    if login:
        folders.extend([
            "application/auth",
            "application/auth/sign_in_form",
            "infrastructure/auth", 
            "model/auth",
            "presentation/auth",
            "presentation/auth/widgets"
        ])

    # Create all folders
    for folder in folders:
        folder_path = lib_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)