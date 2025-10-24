// import 'package:flutter/material.dart';
// import 'package:caravaggio_ui/caravaggio_ui.dart';
// import 'package:flutter_bloc/flutter_bloc.dart';
// import 'package:$project_name/application/auth/auth_bloc.dart';
// import 'package:$project_name/injection.dart';
// import 'package:$project_name/router.dart';

// class AppWidget extends StatelessWidget {
//   const AppWidget({super.key});

//   @override
//   Widget build(BuildContext context) {
//     return MultiBlocProvider(
//       // ignore: always_specify_types
//       providers: [
//         BlocProvider<AuthBloc>(create: (BuildContext context) => getIt<AuthBloc>()..add(const AuthCheckRequested())),
//         // Add more blocs here if needed
//       ],
//       child: const _App(),
//     );
//   }
// }

// class _App extends StatelessWidget {
//   const _App();

//   @override
//   Widget build(BuildContext context) {
//     return MaterialApp.router(
//       title: '$project_name',
//       theme: CUI.themeData,
//       routerConfig: router,
//     );
//   }
// }
