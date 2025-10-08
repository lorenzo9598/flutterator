// @override
// Future<Either<AuthFailure, Unit>> signInWithGoogle() async {
//   // Uncomment the following code to implement Google Sign-In

//   // try {
//   //   final googleUser = await _googleSignIn.signIn();

//   //   if (googleUser == null) {
//   //     return left(const AuthFailure.cancelledByUser());
//   //   }

//   //   final googleAuthentication = await googleUser.authentication;
//   //   final authCredential = GoogleAuthProvider.credential(
//   //     accessToken: googleAuthentication.accessToken,
//   //     idToken: googleAuthentication.idToken,
//   //   );
//   //   final userCredential = await _firebaseAuth.signInWithCredential(authCredential);

//   //   // Utente loggato
//   //   final user = userCredential.user;

//   //   // Ottieni ID token (JWT)
//   //   final idToken = await user?.getIdToken();

//   //   if (idToken != null) {
//   //     await _storageRepository.saveToken(idToken);
//   //   }

//   //   return right(unit);
//   // } on PlatformException catch (_) {
//   //   return left(const AuthFailure.serverError());
//   // }

//   // TODO: Implement Google Sign-In
//   return throw UnimplementedError();
// }
