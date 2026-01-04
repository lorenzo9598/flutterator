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
        "core",
        "core/infrastructure",
        "core/presentation",
        "core/model",
        "domain",  # Domain entities folder
        "features",
        "features/home",
        "features/splash",
        "logging",
        "storage",
    ]

    # Add auth folders if login is enabled
    # Domain entities (shared): model + infrastructure only
    # Feature (use case): application + presentation
    if login:
        folders.extend([
            # Domain entities (shared)
            "domain/auth",
            "domain/auth/infrastructure",
            "domain/auth/model",
            # Feature (use case with UI)
            "features/auth",
            "features/auth/application",
            "features/auth/presentation",
            "features/auth/sign_in_form",
            "features/auth/sign_in_form/application",
            "features/auth/sign_in_form/presentation",
        ])

    # Create all folders
    for folder in folders:
        folder_path = lib_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)