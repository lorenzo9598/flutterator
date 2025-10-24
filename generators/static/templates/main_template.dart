// import 'package:caravaggio_ui/caravaggio_ui.dart';
// import 'package:flutter/material.dart';
// import 'package:injectable/injectable.dart';
// import 'package:$project_name/apis/common/constants.dart';
// import 'package:$project_name/injection.dart';
// import 'package:$project_name/presentation/core/app_widget.dart';

// Future<void> main() async {
//   CaravaggioUI.initialize(
//     primaryColor: Colors.red, // Change this to your desired primary color
//     // fontFamily: 'Noto Sans', // Uncomment and set your desired font family
//   );

//   WidgetsFlutterBinding.ensureInitialized();

//   initEnvironment();

//   await configureDependencies(Environment.dev);

//   runApp(const AppWidget());
// }

// void initEnvironment() {
//   const String environment = String.fromEnvironment(
//     'ENV',
//     defaultValue: "local",
//   );

//   if (environment.toLowerCase() == "production") {
//     Constants.apiUrl = "INSERT YOUR PRODUCTION URL HERE";
//   } else if (environment.toLowerCase() == "development") {
//     Constants.apiUrl = "INSERT YOUR DEVELOPMENT URL HERE";
//   } else if (environment.toLowerCase() == "staging") {
//     Constants.apiUrl = "INSERT YOUR STAGING URL HERE";
//   } else {
//     Constants.apiUrl = "INSERT YOUR LOCAL URL HERE";
//   }
// }
