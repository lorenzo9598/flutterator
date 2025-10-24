import 'package:another_flushbar/flushbar_helper.dart';
import 'package:caravaggio_ui/caravaggio_ui.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:$project_name/application/auth/auth_bloc.dart';
import 'package:$project_name/application/auth/sign_in_form/sign_in_form_bloc.dart';
import 'package:$project_name/presentation/home/home_screen.dart';
import 'package:$project_name/model/auth/auth_failure.dart';
import 'package:go_router/go_router.dart';
import 'package:$project_name/model/core/failures.dart';
import 'package:dartz/dartz.dart' as dz;

class SignInForm extends StatelessWidget {
  const SignInForm({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocConsumer<SignInFormBloc, SignInFormState>(
      listener: (BuildContext context, SignInFormState state) {
        state.authFailureOrSuccessOption.fold(
          () {},
          (dz.Either<AuthFailure, dz.Unit> either) {
            either.fold(
              (AuthFailure failure) {
                FlushbarHelper.createError(
                  message: switch (failure) {
                    // Use localized strings here in your apps
                    CancelledByUser() => 'Cancelled',
                    ServerError() => 'Server error',
                    EmailAlreadyInUse() => 'Email already in use',
                    InvalidEmailAndPasswordCombination() => 'Invalid email and password combination',
                    // TODO: Handle this case.
                    AuthFailure() => throw UnimplementedError(),
                  },
                ).show(context);
              },
              (_) {
                context.read<AuthBloc>().add(const AuthEvent.authCheckRequested());
                context.go(HomeScreen.routeName);
              },
            );
          },
        );
      },
      builder: (BuildContext context, SignInFormState state) {
        return Form(
          autovalidateMode: state.showErrorMessages ? AutovalidateMode.always : AutovalidateMode.disabled,
          child: SingleChildScrollView(
            child: SafeArea(
              child: Padding(
                padding: const EdgeInsets.only(top: 50, left: 16, right: 16),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: <Widget>[
                    Image.asset(
                      'assets/logo.png',
                      height: 80,
                    ),
                    const SizedBox(height: 8),
                    CText.display(
                      'Accedi',
                      textAlign: TextAlign.center,
                    ).bold,
                    const SizedBox(height: 8),
                    CTextField.bordered(
                      decoration: const CFieldDecoration(
                        prefixIcon: Icon(Icons.email),
                        labelText: 'Email',
                      ),
                      initialValue: kDebugMode ? 'email@example.com' : null,
                      autocorrect: false,
                      onChanged: (String value) {
                        context.read<SignInFormBloc>().add(SignInFormEvent.emailChanged(value));
                      },
                      validator: (_) {
                        return context.read<SignInFormBloc>().state.emailAddress.value.fold(
                              (ValueFailure<String> f) => switch (f) {
                                ValueFailure.invalidEmail => 'Invalid email',
                                _ => null,
                              },
                              (_) => null,
                            );
                      },
                    ),
                    const SizedBox(height: 8),
                    CTextField.bordered(
                      // controller: passwordController,
                      decoration: const CFieldDecoration(
                        prefixIcon: Icon(Icons.lock),
                        labelText: 'Password',
                      ),
                      obscureText: true,
                      autocorrect: false,
                      initialValue: kDebugMode ? 'password' : null,
                      onChanged: (String value) {
                        context.read<SignInFormBloc>().add(SignInFormEvent.passwordChanged(value));
                      },
                      validator: (_) {
                        return context.read<SignInFormBloc>().state.password.value.fold(
                              (ValueFailure<String> f) => switch (f) {
                                ValueFailure.shortPassword => 'Short password',
                                _ => null,
                              },
                              (_) => null,
                            );
                      },
                    ),
                    if (state.signInAction == SignInAction.signUp) ...<Widget>[
                      const SizedBox(height: 8),
                      CTextField.bordered(
                        decoration: const CFieldDecoration(
                          prefixIcon: Icon(Icons.person),
                          labelText: 'Confirm Password',
                        ),
                        obscureText: true,
                        autocorrect: false,
                        initialValue: kDebugMode ? 'password' : null,
                        onChanged: (String value) {
                          context.read<SignInFormBloc>().add(SignInFormEvent.confirmPasswordChanged(value));
                        },
                        validator: (String? value) {
                          return context.read<SignInFormBloc>().state.confirmPassword.value.fold(
                                (ValueFailure<String> f) => switch (f) {
                                  ValueFailure.passwordsDoNotMatch => 'Passwords do not match',
                                  _ => null,
                                },
                                (_) => null,
                              );
                        },
                      ),
                    ],
                    const SizedBox(height: 8),
                    CButton.elevated(
                      radius: AppRadius.s,
                      onPressed: () {
                        if (state.signInAction == SignInAction.signIn) {
                          context.read<SignInFormBloc>().add(const SignInFormEvent.signInWithEmailAndPasswordPressed());
                        } else {
                          context.read<SignInFormBloc>().add(const SignInFormEvent.registerWithEmailAndPasswordPressed());
                        }
                      },
                      child: state.signInAction == SignInAction.signIn ? CText.label('SIGN IN') : CText.label('REGISTER'),
                    ),
                    const SizedBox(height: 16),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: <Widget>[
                        CText.label(
                          state.signInAction == SignInAction.signIn ? "Don't have an account? " : "Already have an account? ",
                        ),
                        GestureDetector(
                          onTap: () {
                            context.read<SignInFormBloc>().add(const SignInFormEvent.toggleSignInAction());
                          },
                          child: CText.label(
                            state.signInAction == SignInAction.signIn ? 'Register' : 'Sign In',
                          ).bold.withColor(Colors.blue),
                        ),
                      ],
                    ),
                    if (state.isSubmitting) ...<Widget>[
                      const SizedBox(height: 8),
                      const LinearProgressIndicator(value: null),
                    ],
                  ],
                ),
              ),
            ),
          ),
        );
      },
    );
  }
}
