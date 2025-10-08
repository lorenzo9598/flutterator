import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:flutter/foundation.dart';

part 'failures.freezed.dart';

// Used if the validation of ValueObjects within the domain fails
// Example:
//
// Note({required Description description})
//
// Description extends a ValueObject<String> and has a validator that ensures, for example, that the string is not empty.
// If validation fails, a ValueFailure<String> is returned with the reason for the failure.
//
// NOTE:  All domain ValueObjects extend the ValueObject<T> defined in core/value_objects.dart
//        Each domain ValueObject has a specific validator in core/value_validators.dart
//        Validators return an Either<ValueFailure<T>, T> representing the result of the validation.
//        If validation fails, a ValueFailure<T> is returned with the reason for the failure.
//        If validation succeeds, the valid value of type T is returned.
//
//        The Failures defined in the domain folder (e.g. note_failure.dart) are instead used to represent specific errors
//        that can occur during the execution of operations in the domain (e.g. error while saving a note).
//        These Failures are used to handle errors at the application level and not for data validation.

@freezed
abstract class ValueFailure<T> with _$$ValueFailure<T> {
  const factory ValueFailure.exceedingLength({
    required T failedValue,
    required int max,
  }) = ExceedingLength<T>;
  const factory ValueFailure.empty({
    required T failedValue,
  }) = Empty<T>;
  const factory ValueFailure.multiline({
    required T failedValue,
  }) = Multiline<T>;
  const factory ValueFailure.numberTooLarge({
    required T failedValue,
    required num max,
  }) = NumberTooLarge<T>;
  const factory ValueFailure.listTooLong({
    required T failedValue,
    required int max,
  }) = ListTooLong<T>;
  const factory ValueFailure.invalidEmail({
    required T failedValue,
  }) = InvalidEmail<T>;
  const factory ValueFailure.shortPassword({
    required T failedValue,
  }) = ShortPassword<T>;
  const factory ValueFailure.invalidPhotoUrl({
    required T failedValue,
  }) = InvalidPhotoUrl<T>;
  const factory ValueFailure.passwordsDoNotMatch({
    required T failedValue,
  }) = PasswordsDoNotMatch<T>;
}
