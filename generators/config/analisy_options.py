from pathlib import Path

def update_analysis_options(flutter_name):
    # Percorso del progetto
    project_path = Path(flutter_name)

    """Aggiorna analysis_options.yaml con configurazioni comuni"""
    analysis_options_path = project_path / "analysis_options.yaml"
    analysis_options_content = """include: package:flutter_lints/flutter.yaml

linter:
  rules:
    - always_use_package_imports
    - avoid_relative_lib_imports
    - prefer_const_constructors
    - prefer_const_declarations
    - always_declare_return_types
    - always_specify_types

analyzer:
  errors:
    always_use_package_imports: warning
    avoid_relative_lib_imports: warning
    prefer_const_constructors: error
    unused_import: error
    prefer_const_declarations: error
    unnecessary_null_comparison: error
    always_declare_return_types: error
    always_specify_types: warning

  exclude:
    - lib/infrastructure/openapi/generated/**
    - lib/**.g.dart
    - lib/**.freezed.dart

strong-mode:
  implicit-casts: false
"""
    with open(analysis_options_path, "w") as f:
        f.write(analysis_options_content)

        