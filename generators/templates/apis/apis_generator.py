from pathlib import Path
from ..copier import generate_file

def generate_files(project_name: str, lib_path: Path):
    generate_common(project_name, lib_path)
    generate_core(project_name, lib_path)
    generate_interceptors(project_name, lib_path)

def generate_common(project_name: str, lib_path: Path):
    generate_constants(project_name, lib_path)

def generate_core(project_name: str, lib_path: Path):
    generate_api_injectable_module(project_name, lib_path)

def generate_interceptors(project_name: str, lib_path: Path):
    generate_api_logger(project_name, lib_path)
    generate_auth_interceptor(project_name, lib_path)

def generate_constants(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "apis/common/constants_template.jinja", "apis/common/constants.dart")

def generate_api_injectable_module(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "apis/core/api_injectable_module_template.jinja", "apis/core/api_injectable_module.dart")

def generate_api_logger(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "apis/interceptors/api_logger_template.jinja", "apis/interceptors/api_logger.dart")

def generate_auth_interceptor(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "apis/interceptors/auth_interceptor_template.jinja", "apis/interceptors/auth_interceptor.dart")
