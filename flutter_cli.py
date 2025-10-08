#!/usr/bin/env python3

import click
import os
import sys
from pathlib import Path
import shutil
from generators import *

@click.group()
def cli():
    """
    🚀 Flutterator - CLI per creare e gestire progetti Flutter con struttura personalizzata
    
    Creato da Lorenzo Busi @ GetAutomation
    
    """
    pass

@cli.command()
@click.option('--name', prompt='Nome del progetto', help='Nome del progetto Flutter')
@click.option('--login', is_flag=True, prompt='Il progetto ha login?', help='Include funzionalità di login')
def create(name, login):
    """
    Crea un nuovo progetto Flutter con struttura personalizzata
    """
    
    # Validazione nome progetto
    if not name.replace('_', '').replace('-', '').isalnum():
        click.echo("❌ Il nome del progetto deve contenere solo lettere, numeri, _ e -")
        sys.exit(1)

    # Converti nome per Flutter (lowercase con underscore)
    flutter_name = name.lower().replace('-', '_')

    init(flutter_name, login)

@cli.command()
@click.option('--page', help='Nome della pagina da aggiungere (es: notes, tasks, products)')
def add(page):
    """
    Aggiunge una nuova pagina al progetto Flutter esistente
    """

    if not page:
        click.echo("🔧 Comando ADD - Crea una nuova pagina nell'app")
        click.echo("")
        click.echo("💡 Uso: flutterator add --page <nome_pagina>")
        click.echo("")
        click.echo("📝 Esempio: flutterator add --page notes")
        click.echo("   Questo creerà:")
        click.echo("   • model/notes/note.dart")
        click.echo("   • presentation/notes/notes_screen.dart")
        click.echo("   • application/notes/notes_bloc.dart")
        click.echo("   • infrastructure/notes/i_notes_repository.dart")
        click.echo("   • infrastructure/notes/note_dto.dart")
        click.echo("   • API CRUD (se il progetto ha API)")
        return
    
    # Verifica che siamo in un progetto Flutter
    if not Path("pubspec.yaml").exists():
        click.echo("❌ Non sei in un progetto Flutter. Esegui questo comando dalla root del progetto.")
        sys.exit(1)
    
    # Validazione nome feature
    if not page.replace('_', '').isalnum():
        click.echo("❌ Il nome della feature deve contenere solo lettere, numeri e _")
        sys.exit(1)
    
    # Converti nome per essere consistente
    feature_name = page.lower().replace('-', '_')
    
    # Verifica se il progetto ha la struttura di Flutterator
    lib_path = Path("lib")
    if not (lib_path / "model" / "core").exists():
        click.echo("❌ Questo progetto non sembra essere stato creato con Flutterator")
        click.echo("   Il comando add funziona solo con progetti creati con 'flutterator create'")
        sys.exit(1)
    
    # Verifica se ha API (controlla se esiste la cartella apis)
    has_api = (lib_path / "apis").exists()
    
    click.echo(f"\n� Aggiungendo feature '{feature_name}' al progetto...")
    if has_api:
        click.echo("🔗 Rilevate API - verranno aggiunti anche i file CRUD")
    
    try:
        create_feature(feature_name, lib_path, has_api)
        click.echo(f"\n✅ Feature '{feature_name}' aggiunta con successo!")
        click.echo(f"\n📋 File creati:")
        click.echo(f"   • model/{feature_name}/{feature_name}.dart")
        click.echo(f"   • presentation/{feature_name}/{feature_name}_screen.dart")
        click.echo(f"   • application/{feature_name}/{feature_name}_bloc.dart")
        click.echo(f"   • infrastructure/{feature_name}/i_{feature_name}_repository.dart")
        click.echo(f"   • infrastructure/{feature_name}/{feature_name}_dto.dart")
        if has_api:
            click.echo(f"   • apis/clients/{feature_name}s_client.dart")
        
        click.echo(f"\n🚀 Prossimi passi:")
        click.echo(f"   1. Implementa la logica nei file generati")
        click.echo(f"   2. Aggiungi le route in presentation/router/router.dart")
        click.echo(f"   3. Registra i servizi in injection.dart")
        
    except Exception as e:
        click.echo(f"❌ Errore nella creazione della feature: {e}")
        sys.exit(1)


if __name__ == '__main__':
    cli()