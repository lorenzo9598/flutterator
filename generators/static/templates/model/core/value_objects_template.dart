import 'package:dartz/dartz.dart';
import 'package:meta/meta.dart';
import 'package:uuid/uuid.dart';
import 'package:$project_name/model/core/common_interfaces.dart';
import 'package:$project_name/model/core/errors.dart';
import 'package:$project_name/model/core/failures.dart';
import 'package:$project_name/model/core/value_validators.dart';

// Used for attributes within the domain. Each attribute is a ValueObject<T>
// Example:
//
// Note({required Description description})
//
// Description extends a ValueObject<String> and has a validator that ensures, for example, that the string is not empty
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

@immutable
abstract class ValueObject<T> implements IValidatable {
  const ValueObject();
  Either<ValueFailure<T>, T> get value;

  /// Throws [UnexpectedValueError] containing the [ValueFailure]
  T getOrCrash() {
    // id = identity - same as writing (right) => right
    return value.fold((ValueFailure<T> f) => throw UnexpectedValueError(f), id);
  }

  T getOrElse(T dflt) {
    return value.getOrElse(() => dflt);
  }

  /// Returns the [ValueFailure] if the value is invalid, otherwise returns [Unit]
  ///
  /// Example:
  ///
  /// extension NoteX on Note {
  ///   Option<ValueFailure<dynamic>> get failureOption {
  ///     return description.failureOrUnit
  ///         .andThen(color.failureOrUnit)
  ///         .andThen(todos.failureOrUnit)
  ///         .andThen(
  ///           todos
  ///               .getOrCrash()
  ///               .map((todoItem) => todoItem.failureOption)
  ///               .filter((o) => o.isSome())
  ///               .getOrElse(0, (_) => none())
  ///               .fold(() => right(unit), (f) => left(f)),
  ///         )
  ///         .fold((f) => some(f), (_) => none());
  ///   }
  /// }
  ///
  /// Usage in a Widget:
  /// if (note.failureOption.isSome()) {
  ///   return ErrorNoteCard(note: note);
  /// }
  Either<ValueFailure<dynamic>, Unit> get failureOrUnit {
    return value.fold(
      (ValueFailure<T> l) => left(l),
      (T r) => right(unit),
    );
  }

  @override
  bool isValid() {
    return value.isRight();
  }

  @override
  bool operator ==(Object o) {
    if (identical(this, o)) return true;
    return o is ValueObject<T> && o.value == value;
  }

  @override
  int get hashCode => value.hashCode;

  @override
  String toString() => 'Value($$value)';
}

class UniqueId extends ValueObject<String> {
  @override
  final Either<ValueFailure<String>, String> value;

  // We cannot let a simple String be passed in. This would allow for possible non-unique IDs.
  factory UniqueId() {
    return UniqueId._(
      right(const Uuid().v1()),
    );
  }

  /// Used with strings we trust are unique, such as database IDs.
  factory UniqueId.fromUniqueString(String uniqueIdStr) {
    return UniqueId._(
      right(uniqueIdStr),
    );
  }

  const UniqueId._(this.value);
}

class StringSingleLine extends ValueObject<String> {
  @override
  final Either<ValueFailure<String>, String> value;

  factory StringSingleLine(String input) {
    return StringSingleLine._(
      validateSingleLine(input),
    );
  }

  const StringSingleLine._(this.value);
}
