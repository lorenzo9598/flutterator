import click
from pathlib import Path

def initialize_project(lib_path, project_path, has_login):
    click.echo("\n📁 Rimuovendo file di default...")
    remove_default_files(lib_path, project_path)
    click.echo("\n📁 Creando struttura delle cartelle...")
    create_folder_structure(lib_path, has_login)

def remove_default_files(lib_path, project_path):
     # Rimuovi il main.dart di default e test di default
    default_main = lib_path / "main.dart"
    if default_main.exists():
        default_main.unlink()
    
    # Rimuovi cartella test di default se vuota o contiene solo widget_test.dart
    test_path = project_path / "test"
    if test_path.exists():
        widget_test = test_path / "widget_test.dart"
        if widget_test.exists():
            widget_test.unlink()
        # Rimuovi cartella test se ora è vuota
        try:
            test_path.rmdir()
        except OSError:
            pass  # Non vuota, lascia stare

def create_folder_structure(lib_path, login):
     # Crea struttura delle cartelle    
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
    
    # Aggiungi cartelle auth se login è abilitato
    if login:
        folders.extend([
            "application/auth",
            "application/auth/sign_in_form",
            "infrastructure/auth", 
            "model/auth",
            "presentation/auth",
            "presentation/auth/widgets"
        ])

    # Crea tutte le cartelle
    for folder in folders:
        folder_path = lib_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)