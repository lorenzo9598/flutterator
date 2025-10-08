import 'package:dartz/dartz.dart';
import 'package:$project_name/model/core/failures.dart';

// Used to validate ValueObjects within the domain
// Example:
//
// Note({required Description description})
//
// Description extends a ValueObject<String> and has a validator that ensures, for example, that the string is not empty
//
//
// class Description extends ValueObject<String> {
//   @override
//   final Either<ValueFailure<String>, String> value;
//   static const maxLength = 1000;
//   factory Description(String input) {
//     assert(input != null);
//     return Description._(
//       validateMaxStringLength(input, maxLength).flatMap(validateStringNotEmpty),
//     );
//   }
//   const Description._(this.value);
// }
//
//
// NOTE:  All domain ValueObjects extend ValueObject<T>
//        Each domain ValueObject has a validator specified in core/value_validators.dart
//        Validators return an Either<ValueFailure<T>, T> representing the result of the validation
//        If validation fails, a ValueFailure<T> is returned with the reason for the failure
//        If validation succeeds, the valid value of type T is returned
//
//        The Failures defined in the domain folder (e.g. note_failure.dart) are instead used to represent specific errors
//        that can occur during the execution of operations in the domain (e.g. error while saving a note)
//        These Failures are used to handle errors at the application level and not for data validation

Either<ValueFailure<String>, String> validateMaxStringLength(
  String input,
  int maxLength,
) {
  if (input.length <= maxLength) {
    return right(input);
  } else {
    return left(ValueFailure<String>.exceedingLength(
      failedValue: input,
      max: maxLength,
    ));
  }
}

Either<ValueFailure<String>, String> validateStringNotEmpty(String input) {
  if (input.isEmpty) {
    return left(ValueFailure<String>.empty(failedValue: input));
  } else {
    return right(input);
  }
}

Either<ValueFailure<String>, String> validateSingleLine(String input) {
  if (input.contains('\n')) {
    return left(ValueFailure<String>.multiline(failedValue: input));
  } else {
    return right(input);
  }
}

Either<ValueFailure<List<T>>, List<T>> validateMaxListLength<T>(List<T> input, int maxLength) {
  if (input.length <= maxLength) {
    return right(input);
  } else {
    return left(ValueFailure<List<T>>.listTooLong(
      failedValue: input,
      max: maxLength,
    ));
  }
}

Either<ValueFailure<String>, String> validateEmailAddress(String input) {
  // Maybe not the most robust way of email validation but it's good enough
  const String emailRegex = r"""^[a-zA-Z0-9.a-zA-Z0-9.!#$$%&'*+-/=?^_`{|}~]+@[a-zA-Z0-9]+\.[a-zA-Z]+""";
  if (RegExp(emailRegex).hasMatch(input)) {
    return right(input);
  } else {
    return left(ValueFailure<String>.invalidEmail(failedValue: input));
  }
}

Either<ValueFailure<String>, String> validatePassword(String input) {
  // You can also add some advanced password checks (uppercase/lowercase, at least 1 number, ...)
  if (input.length >= 6) {
    return right(input);
  } else {
    return left(ValueFailure<String>.shortPassword(failedValue: input));
  }
}

Either<ValueFailure<String>, String> validateConfirmPassword(
  String password,
  String confirmPassword,
) {
  if (password == confirmPassword) {
    return right(confirmPassword);
  } else {
    return left(ValueFailure<String>.passwordsDoNotMatch(failedValue: confirmPassword));
  }
}
