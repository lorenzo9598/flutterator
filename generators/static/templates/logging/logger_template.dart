import 'package:injectable/injectable.dart';

enum LoggerLevel {
  verbose,
  info,
  warning,
  error,
  fatal,
  success,
  apiReq,
  apiRes,
}

abstract class LoggingIntegration {
  void log(String message, LoggerLevel level, {dynamic ex, dynamic st});
}

@injectable
class Logger {
  Logger(this._integrations);

  final List<LoggingIntegration> _integrations;

  void logVerbose(String message) {
    _log(message, LoggerLevel.verbose);
  }

  void logInfo(String message) {
    _log(message, LoggerLevel.info);
  }

  void logWarning(String message) {
    _log(message, LoggerLevel.warning);
  }

  void logSuccess(String message) {
    _log(message, LoggerLevel.success);
  }

  void logError(String message, {dynamic ex, dynamic st}) {
    _log(message, LoggerLevel.error, ex: ex, st: st);
  }

  void logFatal(String message, {dynamic ex, dynamic st}) {
    _log(message, LoggerLevel.fatal, ex: ex, st: st);
  }

  void logApiReq(String message) {
    _log(message, LoggerLevel.apiReq);
  }

  void logApiRes(String message) {
    _log(message, LoggerLevel.apiRes);
  }

  void _log(String message, LoggerLevel level, {dynamic ex, dynamic st}) {
    // First build the "final message" that will look like "[LogLevelPrefix] message"
    String finalMessage = "";
    final String prefix = _getLogPrefix(level);
    if (prefix.isNotEmpty) {
      finalMessage += prefix;
      finalMessage += " ";
    }
    finalMessage += message;

    // Finally send that message to each integration
    for (LoggingIntegration integration in _integrations) {
      integration.log(finalMessage, level, ex: ex, st: st);
    }
  }

  // Returns the log prefix for the given LoggingLevel
  String _getLogPrefix(LoggerLevel level) {
    switch (level) {
      case LoggerLevel.verbose:
        return "[Verbose]";
      case LoggerLevel.info:
        return "[Info]";
      case LoggerLevel.warning:
        return "[Warning]";
      case LoggerLevel.error:
        return "[Error]";
      case LoggerLevel.fatal:
        return "[Fatal error]";
      case LoggerLevel.success:
        return "[Done]";
      case LoggerLevel.apiReq:
        return "[API Request]";
      case LoggerLevel.apiRes:
        return "[API Response]";
    }
  }
}
