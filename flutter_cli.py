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
