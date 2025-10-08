// // Uncomment the following line to use Firebase Authentication

// import 'package:firebase_auth/firebase_auth.dart';
// import 'package:injectable/injectable.dart';

// import 'package:$project_name/model/auth/user.dart' as auth_user;
// import 'package:$project_name/model/auth/value_objects.dart';
// import 'package:$project_name/model/core/value_objects.dart';

// NOTE: This class is currently a skeleton implementation. Uncomment and implement
// the necessary parts to enable authentication functionality.
//
// This example shows how to map a Firebase User to the domain User model.

// @lazySingleton
// class FirebaseUserMapper {
//   auth_user.User? toDomain(User? _) {
//     return _ == null
//         ? null
//         : auth_user.User(
//             id: UniqueId.fromUniqueString(_.uid),
//             name: StringSingleLine(_.displayName ?? (_.email ?? "").split('@').firstOrNull ?? ""),
//             emailAddress: EmailAddress(_.email ?? ""),
//           );
//   }
// }
