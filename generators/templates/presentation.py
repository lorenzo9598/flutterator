# from pathlib import Path
# from .copier import generate_file

# BASE_DIR = Path(__file__).parent  # la cartella dove si trova copier.py, cioè "templates/"
# TEMPLATE_DIR = BASE_DIR.parent / "static" / "templates"

# def generate_presentation(project_name: str, lib_path: Path, has_login: bool):
#     # home_screen.dart
#     generate_home_screen(project_name, lib_path)

#     if has_login:
#         # login_screen.dart
#         generate_login_screen(project_name, lib_path)

#         # sign_in_form.dart
#         generate_sign_in_form(project_name, lib_path)

#     # splash_screen.dart
#     generate_splash_screen(project_name, lib_path, has_login)

#     # router.dart
#     generate_router(project_name, lib_path, has_login)


# def generate_home_screen(project_name: str, lib_path: Path):
#     generate_file(project_name, lib_path, "presentation/home/home_screen_template.jinja", "presentation/home/home_screen.dart")

# def generate_login_screen(project_name: str, lib_path: Path):
#     generate_file(project_name, lib_path, "presentation/auth/login_screen_template.jinja", "presentation/auth/login_screen.dart")

# def generate_sign_in_form(project_name: str, lib_path: Path):
#     generate_file(project_name, lib_path, "presentation/auth/widgets/sign_in_form_template.jinja", "presentation/auth/widgets/sign_in_form.dart")

# def generate_splash_screen(project_name: str, lib_path: Path, has_login: bool):
#     generate_file(project_name, lib_path, ("presentation/splash/splash_screen_auth_template.jinja" if has_login else "presentation/splash/splash_screen_template.jinja"), "presentation/splash/splash_screen.dart")

# def generate_router(project_name: str, lib_path: Path, has_login: bool):
#     content = ""

#     if has_login:
#         content += f"import 'package:{project_name}/presentation/auth/login_screen.dart';\n"

#     content += f"""import 'package:{project_name}/presentation/home/home_screen.dart';
# import 'package:flutter/material.dart';
# import 'package:{project_name}/presentation/splash/splash_screen.dart';
# import 'package:go_router/go_router.dart';

# final GoRouter router = GoRouter(
#   routes: <RouteBase>["""
    
#     if has_login:
#         content += f"""
#     GoRoute(
#         path: LoginScreen.routeName,
#         builder: (BuildContext context, GoRouterState state) => const LoginScreen(),
#     ),"""
    
#     content += f"""
#     GoRoute(
#       path: HomeScreen.routeName,
#       builder: (BuildContext context, GoRouterState state) => const HomeScreen(),
#     ),
#     GoRoute(
#       path: SplashScreen.routeName,
#       builder: (BuildContext context, GoRouterState state) => const SplashScreen(),
#     ),
#   ],
# );
# """
#     (lib_path / "router.dart").write_text(content)