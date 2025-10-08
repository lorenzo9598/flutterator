part of 'sign_in_form_bloc.dart';

enum SignInAction { signIn, signUp }

@freezed
abstract class SignInFormState with _$$SignInFormState {
  const factory SignInFormState({
    required EmailAddress emailAddress,
    required Password password,
    required ConfirmPassword confirmPassword,
    required SignInAction signInAction,
    required bool showErrorMessages,
    required bool isSubmitting,
    required Option<Either<AuthFailure, Unit>> authFailureOrSuccessOption,
  }) = _SignInFormState;

  factory SignInFormState.initial() => SignInFormState(
        emailAddress: kDebugMode ? EmailAddress('email@example.com') : EmailAddress(''),
        password: kDebugMode ? Password('password') : Password(''),
        confirmPassword: kDebugMode ? ConfirmPassword('password', 'password') : ConfirmPassword('', ''),
        signInAction: SignInAction.signIn,
        showErrorMessages: false,
        isSubmitting: false,
        authFailureOrSuccessOption: none(),
      );
}
