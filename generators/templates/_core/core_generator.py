from pathlib import Path
from ..copier import generate_file


def infer_has_login(lib_path: Path) -> bool:
    """Detect whether the project includes generated auth/sign-in (``flutterator create --login``).

    Used when regenerating ``error_localizer.dart`` outside of ``create`` (e.g. ``add-domain``),
    so ``localizeAuthFailure`` is preserved.
    """
    return (
        lib_path / "features" / "auth" / "sign_in_form" / "presentation" / "sign_in_form.dart"
    ).exists()


def generate_files(project_name: str, lib_path: Path, has_login: bool):
    generate_app_widget(project_name, lib_path, has_login)
    generate_model(project_name, lib_path)
    generate_infrastructure(project_name, lib_path)
    generate_error_localizer(project_name, lib_path, domain_folder="domain", has_login=has_login)
    generate_common_widgets(project_name, lib_path)


def generate_common_widgets(project_name: str, lib_path: Path) -> None:
    """Write shared UI widgets under lib/widgets/common/ (new project create)."""
    generate_file(project_name, lib_path, "widgets/common/loading_widget_template.jinja", "widgets/common/loading_widget.dart")
    generate_file(project_name, lib_path, "widgets/common/error_widget_template.jinja", "widgets/common/error_widget.dart")
    generate_file(project_name, lib_path, "widgets/common/unknown_state_widget_template.jinja", "widgets/common/unknown_state_widget.dart")


def ensure_common_widgets(project_name: str, lib_path: Path) -> None:
    """Ensure lib/widgets/common exists (e.g. add-component on older projects)."""
    if (lib_path / "widgets" / "common" / "loading_widget.dart").exists():
        return
    generate_common_widgets(project_name, lib_path)

def generate_model(project_name: str, lib_path: Path):
    generate_common_interfaces(project_name, lib_path)
    generate_entity(project_name, lib_path)
    generate_errors(project_name, lib_path)
    generate_failures(project_name, lib_path)
    generate_value_objects(project_name, lib_path)
    generate_value_validators(project_name, lib_path)

def generate_infrastructure(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "core/infrastructure/base_mapper_template.jinja", "core/infrastructure/base_mapper.dart")
    generate_file(project_name, lib_path, "core/infrastructure/repository_error_handler_template.jinja", "core/infrastructure/repository_error_handler.dart")
    generate_file(project_name, lib_path, "core/infrastructure/base_repository_mixin_template.jinja", "core/infrastructure/base_repository_mixin.dart")


def generate_error_localizer(project_name: str, lib_path: Path, domain_folder: str = "domain", has_login: bool = False):
    """Generate error_localizer.dart with a localize method per domain failure.

    Scans ``lib_path / domain_folder`` for domain models that have a
    corresponding ``*_failure.dart`` file and builds the template context
    so the error localizer contains one method per domain failure.

    ``localizeAuthFailure`` is emitted when login UI was generated (``has_login``)
    **or** when ``domain/auth/model/auth_failure.dart`` exists, so sign-in code
    can localize errors even on projects created without ``--login``.
    """
    from generators.helpers.feature import find_domain_models_with_class_names

    auth_failure_path = lib_path / domain_folder / "auth" / "model" / "auth_failure.dart"
    include_auth_failure_localizer = bool(has_login or auth_failure_path.is_file())

    domain_failures = []
    models = find_domain_models_with_class_names(lib_path, domain_folder) if lib_path.exists() else {}

    for file_stem, info in sorted(models.items()):
        failure_file = lib_path / domain_folder / info['folder'] / "model" / f"{file_stem}_failure.dart"
        if not failure_file.exists():
            continue

        class_name = info['class_name']
        failure_class = f"{class_name}Failure"
        # Dedicated AuthFailure block below; skip generic template for entity stem "auth".
        if include_auth_failure_localizer and file_stem == "auth" and failure_class == "AuthFailure":
            continue
        alias = f"{file_stem}_failure"
        import_path = f"{project_name}/{domain_folder}/{info['folder']}/model/{file_stem}_failure.dart"

        domain_failures.append({
            "import_path": import_path,
            "alias": alias,
            "failure_class": failure_class,
            "class_name": class_name,
        })

    generate_file(
        project_name, lib_path,
        "core/errors/error_localizer_template.jinja",
        "core/errors/error_localizer.dart",
        {"domain_failures": domain_failures, "has_login": include_auth_failure_localizer},
    )


def generate_app_widget(project_name: str, lib_path: Path, has_login: bool):
    """Generate app widget file using Jinja template"""
    generate_file(project_name, lib_path, "core/presentation/app_widget_template.jinja", "core/presentation/app_widget.dart", {
        "has_login": has_login
    })

def generate_common_interfaces(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "core/model/common_interfaces_template.jinja", "core/model/common_interfaces.dart")

def generate_entity(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "core/model/entity_template.jinja", "core/model/entity.dart")

def generate_errors(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "core/model/errors_template.jinja", "core/model/errors.dart")

def generate_failures(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "core/model/failures_template.jinja", "core/model/failures.dart")

def generate_value_objects(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "core/model/value_objects_template.jinja", "core/model/value_objects.dart")

def generate_value_validators(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "core/model/value_validators_template.jinja", "core/model/value_validators.dart")