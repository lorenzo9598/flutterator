from pathlib import Path
from ..copier import generate_file


def generate_files(project_name: str, lib_path: Path, has_login: bool):
    """Generate main lib files using Jinja templates"""
    generate_main(project_name, lib_path)
    generate_injection(project_name, lib_path)
    generate_router(project_name, lib_path, has_login)


def generate_main(project_name: str, lib_path: Path):
    """Generate main.dart file using Jinja template"""
    generate_file(project_name, lib_path, "main_template.jinja", "main.dart")


def generate_injection(project_name: str, lib_path: Path):
    """Generate injection.dart file using Jinja template"""
    generate_file(project_name, lib_path, "injection_template.jinja", "injection.dart")


def generate_router(project_name: str, lib_path: Path, has_login: bool):
    """Generate router.dart file using Jinja template"""
    generate_file(project_name, lib_path, "router_template.jinja", "router.dart", {
        "has_login": has_login
    })