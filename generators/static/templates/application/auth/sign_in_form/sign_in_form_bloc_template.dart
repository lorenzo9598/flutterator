import 'dart:async';

import 'package:bloc/bloc.dart';
import 'package:dartz/dartz.dart';
import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:injectable/injectable.dart';
import 'package:$project_name/model/auth/auth_failure.dart';
import 'package:flutter/foundation.dart';
import 'package:$project_name/model/auth/value_objects.dart';
import 'package:$project_name/model/auth/i_auth_facade.dart';

part 'sign_in_form_event.dart';
part 'sign_in_form_state.dart';

part 'sign_in_form_bloc.freezed.dart';

@injectable
class SignInFormBloc extends Bloc<SignInFormEvent, SignInFormState> {
  final IAuthFacade _authFacade;

  SignInFormBloc(this._authFacade) : super(SignInFormState.initial()) {
    on<EmailChanged>(_onEmailChanged);
    on<PasswordChanged>(_onPasswordChanged);
    on<ConfirmPasswordChanged>(_onConfirmPasswordChanged);
    on<ToggleSignInAction>(_onToggleSignInAction);
    on<RegisterWithEmailAndPasswordPressed>(_onRegisterWithEmailAndPasswordPressed);
    on<SignInWithEmailAndPasswordPressed>(_onSignInWithEmailAndPasswordPressed);
  }

  void _onEmailChanged(EmailChanged event, Emitter<SignInFormState> emit) {
    emit(state.copyWith(
      emailAddress: EmailAddress(event.emailStr),
      authFailureOrSuccessOption: none(),
    ));
  }

  void _onPasswordChanged(PasswordChanged event, Emitter<SignInFormState> emit) {
    emit(state.copyWith(
      password: Password(event.passwordStr),
      confirmPassword: state.signInAction == SignInAction.signUp ? ConfirmPassword(event.passwordStr, state.confirmPassword.rawValue) : state.confirmPassword,
      authFailureOrSuccessOption: none(),
    ));
  }

  void _onConfirmPasswordChanged(ConfirmPasswordChanged event, Emitter<SignInFormState> emit) {
    emit(state.copyWith(
      confirmPassword: ConfirmPassword(state.password.rawValue, event.confirmPasswordStr),
      authFailureOrSuccessOption: none(),
    ));
  }

  void _onToggleSignInAction(ToggleSignInAction event, Emitter<SignInFormState> emit) {
    final SignInAction toggledAction = state.signInAction == SignInAction.signIn ? SignInAction.signUp : SignInAction.signIn;

    emit(state.copyWith(
      signInAction: toggledAction,
      confirmPassword: toggledAction == SignInAction.signUp ? ConfirmPassword(state.password.rawValue, state.confirmPassword.rawValue) : state.confirmPassword,
      authFailureOrSuccessOption: none(),
    ));
  }

  void _onRegisterWithEmailAndPasswordPressed(RegisterWithEmailAndPasswordPressed event, Emitter<SignInFormState> emit) async {
    await _performActionOnAuthFacadeWithEmailAndPassword(_authFacade.registerWithEmailAndPassword, emit);
  }

  void _onSignInWithEmailAndPasswordPressed(SignInWithEmailAndPasswordPressed event, Emitter<SignInFormState> emit) async {
    await _performActionOnAuthFacadeWithEmailAndPassword(_authFacade.signInWithEmailAndPassword, emit);
  }

  Future<void> _performActionOnAuthFacadeWithEmailAndPassword(
    Future<Either<AuthFailure, Unit>> Function({
      required EmailAddress emailAddress,
      required Password password,
    }) forwardedCall,
    Emitter<SignInFormState> emit,
  ) async {
    Either<AuthFailure, Unit>? failureOrSuccess;

    final bool isEmailValid = state.emailAddress.isValid();
    final bool isPasswordValid = state.password.isValid();

    final bool isConfirmPasswordValid = state.signInAction == SignInAction.signUp ? state.confirmPassword.isValid() : true;

    if (isEmailValid && isPasswordValid && isConfirmPasswordValid) {
      emit(state.copyWith(
        isSubmitting: true,
        authFailureOrSuccessOption: none(),
      ));

      failureOrSuccess = await forwardedCall(
        emailAddress: state.emailAddress,
        password: state.password,
      );
    }
    emit(state.copyWith(
      isSubmitting: false,
      showErrorMessages: true,
      authFailureOrSuccessOption: optionOf(failureOrSuccess),
    ));
  }
}
