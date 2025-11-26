# from pathlib import Path
# from .copier import generate_file

# def generate_api(project_name: str, lib_path: Path, has_login: bool):
#     # constants.dart
#     generate_constants(project_name, lib_path)

#     # logger.dart
#     generate_logger(project_name, lib_path)

#     # console.dart
#     generate_console(project_name, lib_path)

#     # analytics_logging.dart
#     generate_analytics_logging(project_name, lib_path)

#     # logger_injectable_module.dart
#     generate_logger_injectable_module(project_name, lib_path)

#     # api_logger.dart
#     generate_api_logger(project_name, lib_path)

#     # auth_interceptor.dart
#     generate_auth_interceptor(project_name, lib_path)

#     # storage_repository.dart
#     generate_storage_repository(project_name, lib_path)

#     # api_injectable_module.dart
#     generate_api_injectable_module(project_name, lib_path)

# def generate_constants(project_name: str, lib_path: Path):
#     generate_file(project_name, lib_path, "apis/common/constants_template.jinja", "apis/common/constants.dart")

# def generate_auth_interceptor(project_name: str, lib_path: Path):
#     generate_file(project_name, lib_path, "apis/interceptors/auth_interceptor_template.jinja", "apis/interceptors/auth_interceptor.dart")

# def generate_storage_repository(project_name: str, lib_path: Path):
#     generate_file(project_name, lib_path, "infrastructure/storage/storage_repository_template.jinja", "infrastructure/storage/storage_repository.dart")

# def generate_logger(project_name: str, lib_path: Path):
#     generate_file(project_name, lib_path, "logging/logger_template.jinja", "logging/logger.dart")

# def generate_console(project_name: str, lib_path: Path):
#     generate_file(project_name, lib_path, "logging/console_template.jinja", "logging/console.dart")

# def generate_analytics_logging(project_name: str, lib_path: Path):
#     generate_file(project_name, lib_path, "logging/analytics_logging_template.jinja", "logging/analytics_logging.dart")

# def generate_logger_injectable_module(project_name: str, lib_path: Path):
#     generate_file(project_name, lib_path, "logging/logger_injectable_module_template.jinja", "logging/logger_injectable_module.dart")

# def generate_api_logger(project_name: str, lib_path: Path):
#     generate_file(project_name, lib_path, "apis/interceptors/api_logger_template.jinja", "apis/interceptors/api_logger.dart")

# def generate_api_injectable_module(project_name: str, lib_path: Path):
#     generate_file(project_name, lib_path, "apis/core/api_injectable_module_template.jinja", "apis/core/api_injectable_module.dart")