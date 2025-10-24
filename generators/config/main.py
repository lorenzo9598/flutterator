# import click

from .pubspec import update_pubspec
from .analisy_options import update_analysis_options

def generate_config_files(lib_path, has_login, project_name):
    # Create pubspec.yaml
    update_pubspec(project_name, has_login)

    # Create analysis_options.yaml
    update_analysis_options(project_name)
