import click

from .core import generate_core_files
from .model import generate_model
from .presentation import generate_presentation
from .application import generate_application
from .infrastructure import generate_infrastructure
from .api import generate_api

def generate_files(lib_path, login: bool, project_name: str):
    click.echo("\n📁 Generando file...")
    # Crea file in core
    generate_core_files(project_name, lib_path, login)
    
    # Crea file in model
    generate_model(project_name, lib_path, login)
    
    # Crea file in presentation
    generate_presentation(project_name, lib_path, login)

    if login:
        # Crea file in application
        generate_application(project_name, lib_path)

        # Crea file in infrastructure
        generate_infrastructure(project_name, lib_path)

    # Crea file in infrastructure per storage
    generate_api(project_name, lib_path, login)