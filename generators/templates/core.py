from pathlib import Path

from .copier import generate_file

def generate_core_files(project_name: str, lib_path: Path, has_login: bool):
    generate_main(project_name, lib_path)
    generate_app_widget(project_name, lib_path, has_login)
    generate_injection(project_name, lib_path)

def generate_main(project_name: str, lib_path: Path):
    # main.dart
    generate_file(project_name, lib_path, ("main_template.dart"), "main.dart")

def generate_app_widget(project_name: str, lib_path: Path, has_login: bool):
    # app_widget.dart
    generate_file(project_name, lib_path, ("presentation/core/app_widget_auth_template.dart" if has_login else "presentation/core/app_widget_template.dart"), "presentation/core/app_widget.dart")

def generate_injection(project_name: str, lib_path: Path):
    # injection.dart
    generate_file(project_name, lib_path, "injection_template.dart", "injection.dart")
