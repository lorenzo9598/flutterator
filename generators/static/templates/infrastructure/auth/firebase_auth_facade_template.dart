import 'package:dartz/dartz.dart';
import 'package:injectable/injectable.dart';
import 'package:$project_name/infrastructure/storage/storage_repository.dart';
import 'package:$project_name/model/auth/value_objects.dart';
import 'package:$project_name/model/auth/user.dart' as auth_user;
import 'package:$project_name/model/auth/auth_failure.dart';
import 'package:$project_name/model/auth/i_auth_facade.dart';
// import 'package:flutter/services.dart';
// import 'package:firebase_auth/firebase_auth.dart'; // Uncomment the following line to use Firebase Authentication
// import 'package:$project_name/infrastructure/auth/firebase_user_mapper.dart'; // Uncomment the following line to use Firebase Authentication

/// NOTE: This class is currently a skeleton implementation. Uncomment and implement
/// the necessary parts to enable authentication functionality.
///
/// If you are using API from a backend service and authentication from Firebase
/// ensure that backend service is properly set up to work with Firebase Authentication.

@Singleton(as: IAuthFacade)
class FirebaseAuthFacade implements IAuthFacade {
  // final FirebaseAuth _firebaseAuth; // Uncomment the following line to use Firebase Authentication
  // final FirebaseUserMapper _firebaseUserMapper; // Uncomment the following line to use Firebase Authentication
  final StorageRepository _storageRepository;

  FirebaseAuthFacade(
    // this._firebaseAuth, // Uncomment the following line to use Firebase Authentication
    // this._firebaseUserMapper, // Uncomment the following line to use Firebase Authentication
    this._storageRepository,
  );

  @override
  Option<auth_user.User> getSignedInUser() {
    // Uncomment the following line to use Firebase Authentication
    // return optionOf(_firebaseUserMapper.toDomain(_firebaseAuth.currentUser));
    return none();
  }

  @override
  Future<Either<AuthFailure, Unit>> registerWithEmailAndPassword({
    required EmailAddress emailAddress,
    required Password password,
  }) async {
    final String emailAddressStr = emailAddress.value.getOrElse(() => throw 'INVALID EMAIL');
    final String passwordStr = password.value.getOrElse(() => throw 'INVALID PASSWORD');

    // Uncomment the following code to implement Email/Password Registration with Firebase Authentication

    // try {
    //   final userCredential = await _firebaseAuth.createUserWithEmailAndPassword(
    //     email: emailAddressStr,
    //     password: passwordStr,
    //   );

    //   // Uncomment to save the token if needed

    //   // // User registered and logged
    //   // final user = userCredential.user;

    //   // // Get ID token (JWT)
    //   // final idToken = await user?.getIdToken();

    //   // if (idToken != null) {
    //   //   await _storageRepository.saveToken(idToken);
    //   // }

    //   return right(unit);
    // } on PlatformException catch (e) {
    //   if (e.code == 'ERROR_EMAIL_ALREADY_IN_USE') {
    //     return left(const AuthFailure.emailAlreadyInUse());
    //   } else {
    //     return left(const AuthFailure.serverError());
    //   }
    // }

    return right(unit);
  }

  @override
  Future<Either<AuthFailure, Unit>> signInWithEmailAndPassword({
    required EmailAddress emailAddress,
    required Password password,
  }) async {
    final String emailAddressStr = emailAddress.value.getOrElse(() => throw 'INVALID EMAIL');
    final String passwordStr = password.value.getOrElse(() => throw 'INVALID PASSWORD');

    // Uncomment the following code to implement Email/Password Sign-In with Firebase Authentication

    // try {
    //   final userCredential = await _firebaseAuth.signInWithEmailAndPassword(
    //     email: emailAddressStr,
    //     password: passwordStr,
    //   );

    //   // Uncomment to save the token if needed

    //   // // User logged
    //   // final user = userCredential.user;

    //   // // Get ID token (JWT)
    //   // final idToken = await user?.getIdToken();

    //   // if (idToken != null) {
    //   //   await _storageRepository.saveToken(idToken);
    //   // }

    //   return right(unit);
    // } on PlatformException catch (e) {
    //   if (e.code == 'ERROR_WRONG_PASSWORD' || e.code == 'ERROR_USER_NOT_FOUND') {
    //     return left(const AuthFailure.invalidEmailAndPasswordCombination());
    //   }
    //   return left(const AuthFailure.serverError());
    // }

    return right(unit);
  }

  @override
  Future<void> signOut() async {
    await Future.wait(<Future<void>>[
      // _firebaseAuth.signOut(), // Uncomment the following line to use Firebase Authentication
      _storageRepository.removeToken(),
    ]);
  }
}
