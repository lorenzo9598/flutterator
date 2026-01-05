from pathlib import Path
from ..copier import generate_file

def generate_files(project_name: str, lib_path: Path, has_login: bool):
    generate_presentation(project_name, lib_path, has_login)
    generate_model(project_name, lib_path, has_login)
    generate_application(project_name, lib_path, has_login)
    generate_infrastructure(project_name, lib_path, has_login)

def generate_presentation(project_name: str, lib_path: Path, has_login: bool):
    generate_file(project_name, lib_path, ("splash/presentation/splash_screen_auth_template.jinja" if has_login else "splash/presentation/splash_screen_template.jinja"), "features/splash/splash_page.dart")

def generate_model(project_name: str, lib_path: Path, has_login: bool):
    pass

def generate_application(project_name: str, lib_path: Path, has_login: bool):
    pass

def generate_infrastructure(project_name: str, lib_path: Path, has_login: bool):
    pass
