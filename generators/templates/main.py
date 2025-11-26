import click

from .apis.apis_generator import generate_files as generate_apis_files
from .auth.auth_generator import generate_files as generate_auth_files
from .auth.sign_in_form_generator import generate_files as generate_sign_in_form_files
from .home.home_generator import generate_files as generate_home_files
from .lib.lib_generator import generate_files as generate_lib_files
from .logging.logging_generator import generate_files as generate_logging_files
from .splash.splash_generator import generate_files as generate_splash_files
from .storage.storage_generator import generate_files as generate_storage_files
from ._core.core_generator import generate_files as generate_core_files

# from .core import generate_core_files
# from .model import generate_model
# from .presentation import generate_presentation
# from .application import generate_application
# from .infrastructure import generate_infrastructure
# from .api import generate_api

def generate_files(lib_path, login: bool, project_name: str):
    click.echo("\n📁 Generating files...")

    # Generate lib files
    generate_lib_files(project_name, lib_path, login)

    # Generate core files
    generate_core_files(project_name, lib_path, login)

    # Generate splash files
    generate_splash_files(project_name, lib_path, login)

    
    # Generate logging files
    generate_logging_files(project_name, lib_path)

    # Generate storage files
    generate_storage_files(project_name, lib_path)

    # Generate apis files
    generate_apis_files(project_name, lib_path)


    # Generate home files
    generate_home_files(project_name, lib_path)

    if login:
        # Generate auth files
        generate_auth_files(project_name, lib_path)

        # Generate sign-in form files
        generate_sign_in_form_files(project_name, lib_path)
    


    
    # # Create files in core
    # generate_core_files(project_name, lib_path, login)

    # # Create files in model
    # generate_model(project_name, lib_path, login)

    # # Create files in presentation
    # generate_presentation(project_name, lib_path, login)

    # if login:
        # # Create files in application
        # generate_application(project_name, lib_path)

        # # Create files in infrastructure
        # generate_infrastructure(project_name, lib_path)

    # # Create files in infrastructure for storage
    # generate_api(project_name, lib_path, login)