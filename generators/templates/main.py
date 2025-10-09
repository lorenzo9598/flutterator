import click

from .core import generate_core_files
from .model import generate_model
from .presentation import generate_presentation
from .application import generate_application
from .infrastructure import generate_infrastructure
from .api import generate_api

def generate_files(lib_path, login: bool, project_name: str):
    click.echo("\n📁 Generating files...")
    # Create files in core
    generate_core_files(project_name, lib_path, login)

    # Create files in model
    generate_model(project_name, lib_path, login)

    # Create files in presentation
    generate_presentation(project_name, lib_path, login)

    if login:
        # Create files in application
        generate_application(project_name, lib_path)

        # Create files in infrastructure
        generate_infrastructure(project_name, lib_path)

    # Create files in infrastructure for storage
    generate_api(project_name, lib_path, login)