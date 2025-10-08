import 'package:$project_name/model/core/failures.dart';

class NotAuthenticatedError extends Error {}

class UnexpectedValueError extends Error {
  final ValueFailure<dynamic> valueFailure;

  UnexpectedValueError(this.valueFailure);

  @override
  String toString() {
    const String explanation = 'Encountered a ValueFailure at an unrecoverable point. Terminating.';
    return Error.safeToString('$$explanation Failure was: $$valueFailure');
  }
}
