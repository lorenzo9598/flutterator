from pathlib import Path
from ..copier import generate_file

def generate_files(project_name: str, lib_path: Path):
    generate_presentation(project_name, lib_path)
    generate_model(project_name, lib_path)
    generate_application(project_name, lib_path)
    generate_infrastructure(project_name, lib_path)

def generate_presentation(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "auth/presentation/login_screen_template.jinja", "features/auth/presentation/login_page.dart")

def generate_model(project_name: str, lib_path: Path):
    # Domain entities (shared)
    generate_file(project_name, lib_path, "auth/model/auth_failure_template.jinja", "domain/auth/model/auth_failure.dart")
    generate_file(project_name, lib_path, "auth/model/i_auth_facade_template.jinja", "domain/auth/model/i_auth_facade.dart")
    generate_file(project_name, lib_path, "auth/model/user_template.jinja", "domain/auth/model/user.dart")
    generate_file(project_name, lib_path, "auth/model/user_profile_template.jinja", "domain/auth/model/user_profile.dart")
    generate_file(project_name, lib_path, "auth/model/i_user_profile_repository_template.jinja", "domain/auth/model/i_user_profile_repository.dart")
    generate_file(project_name, lib_path, "auth/model/value_objects_template.jinja", "domain/auth/model/value_objects.dart")

def generate_application(project_name: str, lib_path: Path):
    # Feature (use case)
    generate_file(project_name, lib_path, "auth/application/auth_bloc_template.jinja", "features/auth/application/auth_bloc.dart")
    generate_file(project_name, lib_path, "auth/application/auth_event_template.jinja", "features/auth/application/auth_event.dart")
    generate_file(project_name, lib_path, "auth/application/auth_state_template.jinja", "features/auth/application/auth_state.dart")

def generate_infrastructure(project_name: str, lib_path: Path):
    # Domain entities (shared)
    generate_file(project_name, lib_path, "auth/infrastructure/auth_facade_template.jinja", "domain/auth/infrastructure/auth_facade.dart")
    generate_file(project_name, lib_path, "auth/infrastructure/user_profile_repository_template.jinja", "domain/auth/infrastructure/user_profile_repository.dart")
    generate_file(project_name, lib_path, "auth/infrastructure/user_profile_mapper_template.jinja", "domain/auth/infrastructure/user_profile_mapper.dart")
    generate_file(project_name, lib_path, "auth/infrastructure/user_profile_dto_template.jinja", "domain/auth/infrastructure/user_profile_dto.dart")
