from pathlib import Path
from ..copier import generate_file

def generate_files(project_name: str, lib_path: Path):
    generate_presentation(project_name, lib_path)
    generate_model(project_name, lib_path)
    generate_application(project_name, lib_path)
    generate_infrastructure(project_name, lib_path)

def generate_presentation(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "auth/presentation/login_screen_template.jinja", "auth/presentation/login_screen.dart")

def generate_model(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "auth/model/auth_failure_template.jinja", "auth/model/auth_failure.dart")
    generate_file(project_name, lib_path, "auth/model/i_auth_facade_template.jinja", "auth/model/i_auth_facade.dart")
    generate_file(project_name, lib_path, "auth/model/user_template.jinja", "auth/model/user.dart")
    generate_file(project_name, lib_path, "auth/model/value_objects_template.jinja", "auth/model/value_objects.dart")

def generate_application(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "auth/application/auth_bloc_template.jinja", "auth/application/auth_bloc.dart")
    generate_file(project_name, lib_path, "auth/application/auth_event_template.jinja", "auth/application/auth_event.dart")
    generate_file(project_name, lib_path, "auth/application/auth_state_template.jinja", "auth/application/auth_state.dart")

def generate_infrastructure(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "auth/infrastructure/firebase_auth_facade_template.jinja", "auth/infrastructure/firebase_auth_facade.dart")
    generate_file(project_name, lib_path, "auth/infrastructure/firebase_user_mapper_template.jinja", "auth/infrastructure/firebase_user_mapper.dart")
