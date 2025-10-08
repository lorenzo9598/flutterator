// @override
// Future<Either<AuthFailure, Unit>> registerWithEmailAndPassword({
//   required EmailAddress emailAddress,
//   required Password password,
// }) async {
//   // Uncomment the following code to implement Email/Password Registration

//   // final emailAddressStr = emailAddress.value.getOrElse(() => 'INVALID EMAIL');
//   // final passwordStr = password.value.getOrElse(() => 'INVALID PASSWORD');
//   // try {
//   //   final userCredential = await _firebaseAuth.createUserWithEmailAndPassword(
//   //     email: emailAddressStr,
//   //     password: passwordStr,
//   //   );

//   //   // Utente registrato e loggato
//   //   final user = userCredential.user;

//   //   // Ottieni ID token (JWT)
//   //   final idToken = await user?.getIdToken();

//   //   if (idToken != null) {
//   //     await _storageRepository.saveToken(idToken);
//   //   }

//   //   return right(unit);
//   // } on PlatformException catch (e) {
//   //   if (e.code == 'ERROR_EMAIL_ALREADY_IN_USE') {
//   //     return left(const AuthFailure.emailAlreadyInUse());
//   //   } else {
//   //     return left(const AuthFailure.serverError());
//   //   }
//   // }
//   throw UnimplementedError();
// }

// @override
// Future<Either<AuthFailure, Unit>> signInWithEmailAndPassword({
//   required EmailAddress emailAddress,
//   required Password password,
// }) async {
//   // Uncomment the following code to implement Email/Password Sign-In

//   // final emailAddressStr = emailAddress.value.getOrElse(() => 'INVALID EMAIL');
//   // final passwordStr = password.value.getOrElse(() => 'INVALID PASSWORD');
//   // try {
//   //   final userCredential = await _firebaseAuth.signInWithEmailAndPassword(
//   //     email: emailAddressStr,
//   //     password: passwordStr,
//   //   );

//   //   // Utente loggato
//   //   final user = userCredential.user;

//   //   // Ottieni ID token (JWT)
//   //   final idToken = await user?.getIdToken();

//   //   if (idToken != null) {
//   //     await _storageRepository.saveToken(idToken);
//   //   }

//   //   return right(unit);
//   // } on PlatformException catch (e) {
//   //   if (e.code == 'ERROR_WRONG_PASSWORD' || e.code == 'ERROR_USER_NOT_FOUND') {
//   //     return left(const AuthFailure.invalidEmailAndPasswordCombination());
//   //   }
//   //   return left(const AuthFailure.serverError());
//   // }

//   throw UnimplementedError();
// }
