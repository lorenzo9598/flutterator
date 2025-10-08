import 'package:$project_name/logging/logger.dart';

class AnalyticsLoggingIntegration implements LoggingIntegration {
  const AnalyticsLoggingIntegration();

  @override
  // ignore: always_specify_types
  void log(String message, LoggerLevel level, {ex, st}) async {
    switch (level) {
      case LoggerLevel.fatal:
        break;
      case LoggerLevel.error:
        break;
      case LoggerLevel.warning:
        break;
      case LoggerLevel.info:
        break;
      case LoggerLevel.verbose:
        break;
      case LoggerLevel.success:
        break;
      case LoggerLevel.apiReq:
        break;
      case LoggerLevel.apiRes:
        break;
    }
  }
}
