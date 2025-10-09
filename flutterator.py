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
@click.option('--name', prompt='Project name', help='Name of the Flutter project')
@click.option('--login', is_flag=True, prompt='Does the project have login?', help='Include login functionality')
def create(name, login):
    """
    Crea un nuovo progetto Flutter con struttura personalizzata
    """
    print(name)
    # Validazione nome progetto
    if not name.replace('_', '').replace('-', '').isalnum():
        click.echo("❌ The project name must contain only letters, numbers, _ and -")
        sys.exit(1)

    # Converti nome per Flutter (lowercase con underscore)
    flutter_name = name.lower().replace('-', '_')

    init(flutter_name, login)

if __name__ == '__main__':
    cli()
