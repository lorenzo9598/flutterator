from pathlib import Path
from .copier import generate_file

BASE_DIR = Path(__file__).parent  # la cartella dove si trova copier.py, cioè "templates/"
TEMPLATE_DIR = BASE_DIR.parent / "static" / "templates"


def generate_infrastructure(project_name: str, lib_path: Path):
    # firebase_auth_facade.dart
    generate_firebase_auth_facade(project_name, lib_path)

    # firebase_user_mapper.dart
    generate_firebase_user_mapper(project_name, lib_path)

    # firebase_injectable_module.dart
    generate_firebase_injectable_module(project_name, lib_path)
        

def generate_firebase_auth_facade(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "infrastructure/auth/firebase_auth_facade_template.dart", "infrastructure/auth/firebase_auth_facade.dart")

def generate_firebase_user_mapper(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "infrastructure/auth/firebase_user_mapper_template.dart", "infrastructure/auth/firebase_user_mapper.dart")

def generate_firebase_injectable_module(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "infrastructure/core/firebase_injectable_module_template.dart", "infrastructure/core/firebase_injectable_module.dart")

def generate_firestore_helpers(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "infrastructure/core/firestore_helpers_template.dart", "infrastructure/core/firestore_helpers.dart")