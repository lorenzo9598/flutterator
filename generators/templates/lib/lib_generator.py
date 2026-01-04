from pathlib import Path
from ..copier import generate_file, hex_to_dart_color


def generate_files(project_name: str, lib_path: Path, has_login: bool, primary_color: str = None, secondary_color: str = None):
    """Generate main lib files using Jinja templates"""
    generate_main(project_name, lib_path, primary_color, secondary_color)
    generate_injection(project_name, lib_path)
    generate_router(project_name, lib_path, has_login)


def generate_main(project_name: str, lib_path: Path, primary_color: str = None, secondary_color: str = None):
    """Generate main.dart file using Jinja template"""
    # Convert hex colors to Dart Color format, fallback to default colors if not provided
    if primary_color and primary_color.strip():
        primary_dart_color = hex_to_dart_color(primary_color)
    else:
        primary_dart_color = "Colors.blue"
    
    if secondary_color and secondary_color.strip():
        secondary_dart_color = hex_to_dart_color(secondary_color)
    else:
        secondary_dart_color = "Colors.orange"
    
    generate_file(project_name, lib_path, "main_template.jinja", "main.dart", {
        "primary_color": primary_dart_color,
        "secondary_color": secondary_dart_color,
    })


def generate_injection(project_name: str, lib_path: Path):
    """Generate injection.dart file using Jinja template"""
    generate_file(project_name, lib_path, "injection_template.jinja", "injection.dart")


def generate_router(project_name: str, lib_path: Path, has_login: bool):
    """Generate router.dart file using Jinja template"""
    generate_file(project_name, lib_path, "router_template.jinja", "router.dart", {
        "has_login": has_login
    })