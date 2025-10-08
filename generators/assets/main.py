# import click

from .assets import move_assets_to_lib

def copy_assets(project_name):
    move_assets_to_lib(project_name)
    # click.echo("\n✅ Assets spostati nella cartella lib/assets")
