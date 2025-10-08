import 'package:dartz/dartz.dart';
import 'package:$project_name/model/auth/auth_failure.dart';
import 'package:$project_name/model/auth/user.dart';
import 'package:$project_name/model/auth/value_objects.dart';

abstract class IAuthFacade {
  Option<User> getSignedInUser();
  Future<Either<AuthFailure, Unit>> registerWithEmailAndPassword({
    required EmailAddress emailAddress,
    required Password password,
  });
  Future<Either<AuthFailure, Unit>> signInWithEmailAndPassword({
    required EmailAddress emailAddress,
    required Password password,
  });
  Future<void> signOut();
}
