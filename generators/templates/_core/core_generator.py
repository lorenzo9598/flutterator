from pathlib import Path
from ..copier import generate_file

def generate_files(project_name: str, lib_path: Path, has_login: bool):
    generate_app_widget(project_name, lib_path, has_login)
    generate_model(project_name, lib_path)
    generate_infrastructure(project_name, lib_path)

def generate_model(project_name: str, lib_path: Path):
    generate_common_interfaces(project_name, lib_path)
    generate_entity(project_name, lib_path)
    generate_errors(project_name, lib_path)
    generate_failures(project_name, lib_path)
    generate_value_objects(project_name, lib_path)
    generate_value_validators(project_name, lib_path)

def generate_infrastructure(project_name: str, lib_path: Path):
    generate_firebase_injectable_module(project_name, lib_path)
    generate_firestore_helpers(project_name, lib_path)


def generate_app_widget(project_name: str, lib_path: Path, has_login: bool):
    content = "";

    content = f"""
import 'package:flutter/material.dart';
import 'package:caravaggio_ui/caravaggio_ui.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:{project_name}/injection.dart';
"""

    if( has_login ):
        content += f"""
import 'package:{project_name}/auth/application/auth_bloc.dart';
"""

    content += f"""
import 'package:{project_name}/router.dart';

class AppWidget extends StatelessWidget {{
  const AppWidget({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return MultiBlocProvider(
      // ignore: always_specify_types
      providers: [""";
    if has_login:
        content += f"""
        BlocProvider<AuthBloc>(create: (BuildContext context) => getIt<AuthBloc>()..add(const AuthCheckRequested())),
"""
    content += f"""
        // Add blocs here if needed
      ],
      child: const _App(),
    );
  }}
}}

class _App extends StatelessWidget {{
  const _App();

  @override
  Widget build(BuildContext context) {{
    return MaterialApp.router(
      title: '{project_name}',
      theme: CUI.themeData,
      routerConfig: router,
    );
  }}
}}
"""

    (lib_path / "core/presentation/app_widget.dart").write_text(content)

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

def generate_firebase_injectable_module(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "core/infrastructure/firebase_injectable_module_template.jinja", "core/infrastructure/firebase_injectable_module.dart")

def generate_firestore_helpers(project_name: str, lib_path: Path):
    generate_file(project_name, lib_path, "core/infrastructure/firestore_helpers_template.jinja", "core/infrastructure/firestore_helpers.dart")