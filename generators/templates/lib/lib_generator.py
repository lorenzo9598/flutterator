from pathlib import Path
from ..copier import generate_file

# from .core import generate_core_files
# from .model import generate_model
# from .presentation import generate_presentation
# from .application import generate_application
# from .infrastructure import generate_infrastructure
# from .api import generate_api

def generate_files(project_name: str, lib_path: Path, has_login: bool):
    generate_main(project_name, lib_path)
    generate_injection(project_name, lib_path)
    generate_router(project_name, lib_path, has_login)

def generate_main(project_name: str, lib_path: Path):
    content = f"""
import 'package:caravaggio_ui/caravaggio_ui.dart';
import 'package:flutter/material.dart';
import 'package:injectable/injectable.dart';
import 'package:{project_name}/apis/common/constants.dart';
import 'package:{project_name}/injection.dart';
import 'package:{project_name}/core/presentation/app_widget.dart';

Future<void> main() async {{
  CaravaggioUI.initialize(
    primaryColor: Colors.blue, // Change this to your desired primary color
    secondaryColor: Colors.orange
    // fontFamily: 'Noto Sans', // Uncomment and set your desired font family
  );

  WidgetsFlutterBinding.ensureInitialized();

  initEnvironment();

  await configureDependencies(Environment.dev);

  runApp(const AppWidget());
}}

void initEnvironment() {{
  const String environment = String.fromEnvironment(
    'ENV',
    defaultValue: "local",
  );

  if (environment.toLowerCase() == "production") {{
    Constants.apiUrl = "INSERT YOUR PRODUCTION URL HERE";
  }} else if (environment.toLowerCase() == "development") {{
    Constants.apiUrl = "INSERT YOUR DEVELOPMENT URL HERE";
  }} else if (environment.toLowerCase() == "staging") {{
    Constants.apiUrl = "INSERT YOUR STAGING URL HERE";
  }} else {{
    Constants.apiUrl = "INSERT YOUR LOCAL URL HERE";
  }}
}}
"""

    (lib_path / "main.dart").write_text(content)
    

def generate_injection(project_name: str, lib_path: Path):
    content = f"""
import 'package:{project_name}/injection.config.dart';
import 'package:get_it/get_it.dart';
import 'package:injectable/injectable.dart';

final GetIt getIt = GetIt.instance;

@InjectableInit()
Future<void> configureDependencies(String env) async => getIt.init(environment: env);
"""

    (lib_path / "injection.dart").write_text(content)

def generate_router(project_name: str, lib_path: Path, has_login: bool):
    content = ""

    if has_login:
        content += f"import 'package:{project_name}/auth/presentation/login_screen.dart';\n"

    content += f"""import 'package:{project_name}/home/presentation/home_screen.dart';
import 'package:flutter/material.dart';
import 'package:{project_name}/splash/presentation/splash_screen.dart';
import 'package:go_router/go_router.dart';

final GoRouter router = GoRouter(
  routes: <RouteBase>["""
    
    if has_login:
        content += f"""
    GoRoute(
        path: LoginScreen.routeName,
        builder: (BuildContext context, GoRouterState state) => const LoginScreen(),
    ),"""
    
    content += f"""
    GoRoute(
      path: HomeScreen.routeName,
      builder: (BuildContext context, GoRouterState state) => const HomeScreen(),
    ),
    GoRoute(
      path: SplashScreen.routeName,
      builder: (BuildContext context, GoRouterState state) => const SplashScreen(),
    ),
  ],
);
"""
    (lib_path / "router.dart").write_text(content)