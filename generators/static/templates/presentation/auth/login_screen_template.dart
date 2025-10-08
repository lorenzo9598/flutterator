import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:$project_name/application/auth/sign_in_form/sign_in_form_bloc.dart';
import 'package:$project_name/injection.dart';
import 'package:$project_name/presentation/auth/widgets/sign_in_form.dart';

class LoginScreen extends StatefulWidget {
  static const String routeName = '/login';

  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: BlocProvider<SignInFormBloc>(
        create: (BuildContext context) => getIt<SignInFormBloc>(),
        child: const SignInForm(),
      ),
    );
  }
}
