from pathlib import Path
from ..copier import generate_file

def generate_files(project_name: str, lib_path: Path):
    generate_presentation(project_name, lib_path)
    generate_model(project_name, lib_path)
    generate_application(project_name, lib_path)
    generate_infrastructure(project_name, lib_path)

def generate_presentation(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "auth/sign_in_form/presentation/sign_in_form_template.jinja", "auth/sign_in_form/presentation/sign_in_form.dart")

def generate_model(project_name: str, lib_path: Path):
    pass

def generate_application(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "auth/sign_in_form/application/sign_in_form_bloc_template.jinja", "auth/sign_in_form/application/sign_in_form_bloc.dart")
    generate_file(project_name, lib_path, "auth/sign_in_form/application/sign_in_form_event_template.jinja", "auth/sign_in_form/application/sign_in_form_event.dart")
    generate_file(project_name, lib_path, "auth/sign_in_form/application/sign_in_form_state_template.jinja", "auth/sign_in_form/application/sign_in_form_state.dart")

def generate_infrastructure(project_name: str, lib_path: Path):
    pass