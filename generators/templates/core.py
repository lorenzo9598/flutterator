# from pathlib import Path

# from .copier import generate_file

# def generate_core_files(project_name: str, lib_path: Path, has_login: bool):
#     generate_main(project_name, lib_path)
#     generate_app_widget(project_name, lib_path, has_login)
#     generate_injection(project_name, lib_path)

# def generate_main(project_name: str, lib_path: Path):
#     content = f"""
# import 'package:caravaggio_ui/caravaggio_ui.dart';
# import 'package:flutter/material.dart';
# import 'package:injectable/injectable.dart';
# import 'package:{project_name}/apis/common/constants.dart';
# import 'package:{project_name}/injection.dart';
# import 'package:{project_name}/presentation/core/app_widget.dart';

# Future<void> main() async {{
#   CaravaggioUI.initialize(
#     primaryColor: Colors.red, // Change this to your desired primary color
#     // fontFamily: 'Noto Sans', // Uncomment and set your desired font family
#   );

#   WidgetsFlutterBinding.ensureInitialized();

#   initEnvironment();

#   await configureDependencies(Environment.dev);

#   runApp(const AppWidget());
# }}

# void initEnvironment() {{
#   const String environment = String.fromEnvironment(
#     'ENV',
#     defaultValue: "local",
#   );

#   if (environment.toLowerCase() == "production") {{
#     Constants.apiUrl = "INSERT YOUR PRODUCTION URL HERE";
#   }} else if (environment.toLowerCase() == "development") {{
#     Constants.apiUrl = "INSERT YOUR DEVELOPMENT URL HERE";
#   }} else if (environment.toLowerCase() == "staging") {{
#     Constants.apiUrl = "INSERT YOUR STAGING URL HERE";
#   }} else {{
#     Constants.apiUrl = "INSERT YOUR LOCAL URL HERE";
#   }}
# }}
# """

#     (lib_path / "main.dart").write_text(content)
    
# def generate_app_widget(project_name: str, lib_path: Path, has_login: bool):
#     content = "";

#     content = f"""
# import 'package:flutter/material.dart';
# import 'package:caravaggio_ui/caravaggio_ui.dart';
# import 'package:flutter_bloc/flutter_bloc.dart';
# import 'package:{project_name}/injection.dart';
# """

#     if( has_login ):
#         content += f"""
# import 'package:{project_name}/application/auth/auth_bloc.dart';
# """

#     content += f"""
# import 'package:{project_name}/router.dart';

# class AppWidget extends StatelessWidget {{
#   const AppWidget({{super.key}});

#   @override
#   Widget build(BuildContext context) {{
#     return MultiBlocProvider(
#       // ignore: always_specify_types
#       providers: [""";
#     if has_login:
#         content += f"""
#         BlocProvider<AuthBloc>(create: (BuildContext context) => getIt<AuthBloc>()..add(const AuthCheckRequested())),
# """
#     content += f"""
#         // Add blocs here if needed
#       ],
#       child: const _App(),
#     );
#   }}
# }}

# class _App extends StatelessWidget {{
#   const _App();

#   @override
#   Widget build(BuildContext context) {{
#     return MaterialApp.router(
#       title: '{project_name}',
#       theme: CUI.themeData,
#       routerConfig: router,
#     );
#   }}
# }}
# """

#     (lib_path / "presentation/core/app_widget.dart").write_text(content)
    
# def generate_injection(project_name: str, lib_path: Path):
#     content = f"""
# import 'package:{project_name}/injection.config.dart';
# import 'package:get_it/get_it.dart';
# import 'package:injectable/injectable.dart';

# final GetIt getIt = GetIt.instance;

# @InjectableInit()
# Future<void> configureDependencies(String env) async => getIt.init(environment: env);
# """

#     (lib_path / "injection.dart").write_text(content)
