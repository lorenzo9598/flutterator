// /// Generates a cryptographically secure random nonce, to be included in a
// /// credential request.
// String generateNonce([int length = 32]) {
//   const String charset = '0123456789ABCDEFGHIJKLMNOPQRSTUVXYZabcdefghijklmnopqrstuvwxyz-._';
//   final random = Random.secure();
//   return List.generate(length, (_) => charset[random.nextInt(charset.length)]).join();
// }

// /// Returns the sha256 hash of [input] in hex notation.
// String sha256ofString(String input) {
//   final bytes = utf8.encode(input);
//   final digest = sha256.convert(bytes);
//   return digest.toString();
// }

// Future<Either<AuthFailure, Unit>> signInWithApple() async {
//   // Uncomment the following code to implement Apple Sign-In

//   // // To prevent replay attacks with the credential returned from Apple, we
//   // // include a nonce in the credential request. When signing in with
//   // // Firebase, the nonce in the id token returned by Apple, is expected to
//   // // match the sha256 hash of `rawNonce`.
//   // final rawNonce = generateNonce();
//   // final nonce = sha256ofString(rawNonce);

//   // // Request credential for the currently signed in Apple account.
//   // final appleCredential = await SignInWithApple.getAppleIDCredential(
//   //   scopes: [
//   //     AppleIDAuthorizationScopes.email,
//   //     AppleIDAuthorizationScopes.fullName,
//   //   ],
//   //   nonce: nonce,
//   // );

//   // // Create an `OAuthCredential` from the credential returned by Apple.
//   // final oauthCredential = OAuthProvider("apple.com").credential(
//   //   idToken: appleCredential.identityToken,
//   //   rawNonce: rawNonce,
//   // );

//   // // Sign in the user with Firebase. If the nonce we generated earlier does
//   // // not match the nonce in `appleCredential.identityToken`, sign in will fail.
//   // final userCredential = await _firebaseAuth.signInWithCredential(oauthCredential);

//   // // Utente loggato
//   // final user = userCredential.user;

//   // // Ottieni ID token (JWT)
//   // final idToken = await user?.getIdToken();

//   // if (idToken != null) {
//   //   await _storageRepository.saveToken(idToken);
//   // }

//   // return right(unit);
//   return throw UnimplementedError();
// }
