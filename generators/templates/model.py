from pathlib import Path
from .copier import generate_file

def generate_model(project_name: str, lib_path: Path, has_login: bool):
    """ Crea i file nella cartella model/core """
    # common_interfaces.dart
    generate_common_interfaces(project_name, lib_path)

    # entity.dart
    generate_entity(project_name, lib_path)

    # errors.dart
    generate_errors(project_name, lib_path)

    # failures.dart
    generate_failures(project_name, lib_path)

    # value_objects.dart
    generate_value_objects(project_name, lib_path)

    # value_validators.dart
    generate_value_validators(project_name, lib_path)

    if has_login:
        # i_auth_facade.dart
        generate_i_auth_facade(project_name, lib_path)

        # user.dart
        generate_user(project_name, lib_path)

        # auth_failure.dart
        generate_auth_failure(project_name, lib_path)

        # value_objects.dart
        generate_value_objects_auth(project_name, lib_path)


def generate_common_interfaces(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "model/core/common_interfaces_template.dart", "model/core/common_interfaces.dart")

def generate_entity(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "model/core/entity_template.dart", "model/core/entity.dart")

def generate_errors(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "model/core/errors_template.dart", "model/core/errors.dart")

def generate_failures(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "model/core/failures_template.dart", "model/core/failures.dart")

def generate_value_objects(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "model/core/value_objects_template.dart", "model/core/value_objects.dart")

def generate_value_validators(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "model/core/value_validators_template.dart", "model/core/value_validators.dart")

def generate_i_auth_facade(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "model/auth/i_auth_facade_template.dart", "model/auth/i_auth_facade.dart")

def generate_user(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "model/auth/user_template.dart", "model/auth/user.dart")

def generate_auth_failure(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "model/auth/auth_failure_template.dart", "model/auth/auth_failure.dart")

def generate_value_objects_auth(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "model/auth/value_objects_template.dart", "model/auth/value_objects.dart")