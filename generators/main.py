
import click
import subprocess
import sys
import shutil

from pathlib import Path

from .assets import copy_assets
from .config import generate_config_files
from .templates import generate_files
from .initializator import initialize_project
from .feature_generator import create_feature

def run_cmd(cmd, capture_output=False):
    """Esegue un comando di shell e mostra output"""
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
      click.echo(f"⚠️ Esiste già una cartella chiamata '{flutter_name}' in questa directory.")
      if click.confirm("Vuoi sovrascrivere la cartella esistente?", default=False):
          # Rimuovi la cartella esistente
          shutil.rmtree(project_dir)
          click.echo("✅ Cartella precedente rimossa.")
      else:
          click.echo("❌ Operazione annullata.")
          sys.exit(1)
    
    
    click.echo(f"\n🚀 Creando progetto Flutter: {flutter_name}")
    
    # Crea il progetto Flutter base
    run_cmd(f"flutter create {flutter_name} --org com.example --project-name {flutter_name} --template app", capture_output=True)
    
    # Percorso del progetto
    project_path = Path(flutter_name)
    lib_path = project_path / "lib"
    
    # Inizializza il progetto (rimuovi file di default, crea cartelle, ecc.)
    initialize_project(lib_path, project_path, login)

    # Genera i file nelle varie cartelle
    generate_files(lib_path, login, flutter_name)
    
    # Genera i file di configurazione (pubspec.yaml, analysis_options.yaml)
    generate_config_files(lib_path, login, flutter_name)

    # Copia gli asset nella cartella lib/assets
    copy_assets(flutter_name)

    click.echo("\n✅ Progetto creato con successo!")
    click.echo(f"\n📋 Riepilogo:")
    click.echo(f"   Nome: {flutter_name}")
    click.echo(f"   Percorso: {project_path.absolute()}")
    if login:
        click.echo(f"   Login: ✅ Email/Password")
    else:
        click.echo(f"   Login: ❌ Nessuno")
    
    click.echo(f"\n🚀 Per iniziare:")
    click.echo(f"   cd {flutter_name}")
    click.echo(f"   flutter pub get")
    click.echo(f"   dart run build_runner build")
    click.echo(f"   flutter run")
