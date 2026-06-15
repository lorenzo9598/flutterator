from pathlib import Path
from ..copier import generate_file

def generate_files(project_name: str, lib_path: Path, has_login: bool = False):
    generate_presentation(project_name, lib_path, has_login)
    generate_model(project_name, lib_path)
    generate_application(project_name, lib_path)
    generate_infrastructure(project_name, lib_path)

def generate_presentation(project_name: str, lib_path: Path, has_login: bool = False):
    generate_file(
        project_name,
        lib_path,
        "home/presentation/home_screen_template.jinja",
        "features/home/home_page.dart",
        {"has_login": has_login},
    )
    
def generate_model(project_name: str, lib_path: Path):
    pass

def generate_application(project_name: str, lib_path: Path):
    pass

def generate_infrastructure(project_name: str, lib_path: Path):
    pass
