import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:${project_name}/presentation/home/home_screen.dart';

class SplashScreen extends StatefulWidget {
  static const String routeName = '/';

  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      // After 500 milliseconds, navigate to the next screen
      Future<void>.delayed(const Duration(milliseconds: 500), () {
        // Navigate to the next screen or perform any action here
        context.replace(HomeScreen.routeName);
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: SizedBox(
          width: 200,
          child: Image.asset('assets/logo.png'),
        ),
      ),
    );
  }
}
