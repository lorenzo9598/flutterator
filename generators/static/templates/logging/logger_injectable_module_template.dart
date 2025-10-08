import 'package:injectable/injectable.dart';
import 'package:$project_name/logging/analytics_logging.dart';
import 'package:$project_name/logging/console.dart';
import 'package:$project_name/logging/logger.dart';

@module
abstract class RegisterModule {
  @lazySingleton
  List<LoggingIntegration> get loggingIntegrations => <LoggingIntegration>[
        const AnalyticsLoggingIntegration(),
        const ConsoleLoggingIntegration(),
      ];
}
