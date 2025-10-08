import 'package:dartz/dartz.dart';
import 'package:$project_name/model/core/failures.dart';
import 'package:$project_name/model/core/value_objects.dart';
import 'package:$project_name/model/core/value_validators.dart';

class EmailAddress extends ValueObject<String> {
  @override
  final Either<ValueFailure<String>, String> value;

  factory EmailAddress(String input) {
    return EmailAddress._(
      validateEmailAddress(input),
    );
  }

  const EmailAddress._(this.value);
}

class Password extends ValueObject<String> {
  @override
  final Either<ValueFailure<String>, String> value;

  factory Password(String input) {
    return Password._(
      validatePassword(input),
    );
  }

  String get rawValue {
    return value.fold((ValueFailure<String> l) => l.failedValue, (String r) => r);
  }

  const Password._(this.value);
}

class ConfirmPassword extends ValueObject<String> {
  @override
  final Either<ValueFailure<String>, String> value;

  factory ConfirmPassword(
    String password,
    String confirmPassword,
  ) {
    return ConfirmPassword._(
      validateConfirmPassword(password, confirmPassword),
    );
  }

  String get rawValue {
    return value.fold((ValueFailure<String> l) => l.failedValue, (String r) => r);
  }

  const ConfirmPassword._(this.value);
}
