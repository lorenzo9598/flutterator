import click
import subprocess
import sys
import shutil

from pathlib import Path

from .assets import copy_assets
from .config import generate_config_files
from .templates import generate_files
from .initializator import initialize_project
from generators.helpers.config import load_config

def run_cmd(cmd, capture_output=False):
    """Executes a shell command and displays output"""
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=capture_output)
        return result.returncode
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Errore nell'esecuzione del comando {cmd}: {e}")
        click.echo(f"Output: {e.stdout}")
        click.echo(f"Error: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        click.echo("❌ Comando non trovato. Assicurati che sia installato e nel PATH.")
        sys.exit(1)

def init(flutter_name, login):
    # Controlla se esiste già una cartella con lo stesso nome del progetto
    project_dir = Path(flutter_name)
    if project_dir.exists():
        click.echo(f"⚠️ Folder named '{flutter_name}' already exists in this directory.")
        if click.confirm("Do you want to overwrite the existing folder?", default=False):
            # Rimuovi la cartella esistente
            shutil.rmtree(project_dir)
            click.echo("✅ Previous folder removed.")
        else:
            click.echo("❌ Operation canceled.")
            sys.exit(1)
    
    
    click.echo(f"\n🚀 Creating Flutter project: {flutter_name}")

    # Create the base Flutter project
    run_cmd(f"flutter create {flutter_name} --org com.example --project-name {flutter_name} --template app", capture_output=False)
    
    # Project path
    project_path = Path(flutter_name)
    lib_path = project_path / "lib"
    
    # Initialize the project (remove default files, create folders, etc.)
    initialize_project(lib_path, project_path, login)

    # Load configuration (will use defaults + global config if exists)
    cfg = load_config(project_path)

    # Generate files in various folders
    generate_files(lib_path, login, flutter_name, cfg.primary_color, cfg.secondary_color)
    
    # Generate configuration files (pubspec.yaml, analysis_options.yaml)
    generate_config_files(lib_path, login, flutter_name)

    # Copy assets to the lib/assets folder
    copy_assets(flutter_name)


    click.echo("\n✅ Project created successfully!")
    click.echo(f"\n📋 Summary:")
    click.echo(f"   Name: {flutter_name}")
    click.echo(f"   Path: {project_path.absolute()}")
    if login:
        click.echo(f"   Login: ✅ Email/Password")
    else:
        click.echo(f"   Login: ❌ None")

    click.echo(f"\n🚀 Dependencies and code generation will be handled automatically!")
    click.echo(f"   flutter run")
