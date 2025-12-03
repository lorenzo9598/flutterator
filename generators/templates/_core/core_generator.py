from pathlib import Path
from ..copier import generate_file

def generate_files(project_name: str, lib_path: Path, has_login: bool):
    generate_app_widget(project_name, lib_path, has_login)
    generate_model(project_name, lib_path)
    generate_infrastructure(project_name, lib_path)

def generate_model(project_name: str, lib_path: Path):
    generate_common_interfaces(project_name, lib_path)
    generate_entity(project_name, lib_path)
    generate_errors(project_name, lib_path)
    generate_failures(project_name, lib_path)
    generate_value_objects(project_name, lib_path)
    generate_value_validators(project_name, lib_path)

def generate_infrastructure(project_name: str, lib_path: Path):
    generate_firebase_injectable_module(project_name, lib_path)
    generate_firestore_helpers(project_name, lib_path)


def generate_app_widget(project_name: str, lib_path: Path, has_login: bool):
    """Generate app widget file using Jinja template"""
    generate_file(project_name, lib_path, "core/presentation/app_widget_template.jinja", "core/presentation/app_widget.dart", {
        "has_login": has_login
    })

def generate_common_interfaces(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "core/model/common_interfaces_template.jinja", "core/model/common_interfaces.dart")

def generate_entity(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "core/model/entity_template.jinja", "core/model/entity.dart")

def generate_errors(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "core/model/errors_template.jinja", "core/model/errors.dart")

def generate_failures(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "core/model/failures_template.jinja", "core/model/failures.dart")

def generate_value_objects(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "core/model/value_objects_template.jinja", "core/model/value_objects.dart")

def generate_value_validators(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "core/model/value_validators_template.jinja", "core/model/value_validators.dart")

def generate_firebase_injectable_module(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "core/infrastructure/firebase_injectable_module_template.jinja", "core/infrastructure/firebase_injectable_module.dart")

def generate_firestore_helpers(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "core/infrastructure/firestore_helpers_template.jinja", "core/infrastructure/firestore_helpers.dart")