from pathlib import Path
from ..copier import generate_file

def generate_files(project_name: str, lib_path: Path):
    generate_presentation(project_name, lib_path)
    generate_model(project_name, lib_path)
    generate_application(project_name, lib_path)
    generate_infrastructure(project_name, lib_path)

def generate_presentation(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "home/presentation/home_screen_template.jinja", "features/home/home_page.dart")
    
def generate_model(project_name: str, lib_path: Path):
    pass

def generate_application(project_name: str, lib_path: Path):
    pass

def generate_infrastructure(project_name: str, lib_path: Path):
    pass
