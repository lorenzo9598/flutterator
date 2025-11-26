from pathlib import Path
from ..copier import generate_file

def generate_files(project_name: str, lib_path: Path):
    # logger.dart
    generate_logger(project_name, lib_path)

    # console.dart
    generate_console(project_name, lib_path)

    # analytics_logging.dart
    generate_analytics_logging(project_name, lib_path)

    # logger_injectable_module.dart
    generate_logger_injectable_module(project_name, lib_path)


def generate_logger(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "logging/logger_template.jinja", "logging/logger.dart")

def generate_console(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "logging/console_template.jinja", "logging/console.dart")

def generate_analytics_logging(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "logging/analytics_logging_template.jinja", "logging/analytics_logging.dart")

def generate_logger_injectable_module(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "logging/logger_injectable_module_template.jinja", "logging/logger_injectable_module.dart")