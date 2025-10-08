from pathlib import Path
from .copier import generate_file

def generate_application(project_name: str, lib_path: Path):  
    """ Crea i file nella cartella application/auth """
    # auth_bloc.dart
    generate_auth_bloc(project_name, lib_path)

    # auth_event.dart
    generate_auth_event(project_name, lib_path)
        
    # auth_state.dart
    generate_auth_state(project_name, lib_path)
    
    # sign_in_form_bloc.dart
    generate_sign_in_form_bloc(project_name, lib_path)

    # sign_in_form_event.dart
    generate_sign_in_form_event(project_name, lib_path)

    # sign_in_form_state.dart
    generate_sign_in_form_state(project_name, lib_path)


def generate_auth_bloc(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "application/auth/auth_bloc_template.dart", "application/auth/auth_bloc.dart")

def generate_auth_event(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "application/auth/auth_event_template.dart", "application/auth/auth_event.dart")

def generate_auth_state(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "application/auth/auth_state_template.dart", "application/auth/auth_state.dart")

def generate_sign_in_form_bloc(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "application/auth/sign_in_form/sign_in_form_bloc_template.dart", "application/auth/sign_in_form/sign_in_form_bloc.dart")    

def generate_sign_in_form_state(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "application/auth/sign_in_form/sign_in_form_state_template.dart", "application/auth/sign_in_form/sign_in_form_state.dart")

def generate_sign_in_form_event(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "application/auth/sign_in_form/sign_in_form_event_template.dart", "application/auth/sign_in_form/sign_in_form_event.dart")