from pathlib import Path
from ..copier import generate_file

def generate_files(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "storage/storage_repository_template.jinja", "storage/storage_repository.dart")
