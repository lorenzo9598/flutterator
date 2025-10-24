import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:$project_name/application/auth/auth_bloc.dart';
import 'package:$project_name/presentation/auth/login_screen.dart';
import 'package:$project_name/presentation/home/home_screen.dart';
import 'package:go_router/go_router.dart';

class SplashScreen extends StatefulWidget {
  static const String routeName = '/';

  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  int _animation = 0;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      setState(() {
        _animation = 1;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return BlocListener<AuthBloc, AuthState>(
      listener: (BuildContext context, AuthState state) => switch (state) {
        Authenticated() => context.replace(HomeScreen.routeName),
        Unauthenticated() => context.replace(LoginScreen.routeName),
        _ => null,
      },
      child: Scaffold(
        body: Center(
          child: AnimatedContainer(
            duration: const Duration(seconds: 1),
            curve: Curves.easeInOut,
            width: _animation == 1 ? 200 : 100,
            child: Image.asset('assets/logo.png'),
          ),
        ),
      ),
    );
  }
}
