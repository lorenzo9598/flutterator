import 'dart:developer' as developer;

import 'package:$project_name/logging/logger.dart';

class ConsoleLoggingIntegration implements LoggingIntegration {
  const ConsoleLoggingIntegration();

  @override
  void log(String message, LoggerLevel level, {dynamic ex, dynamic st}) {
    switch (level) {
      case LoggerLevel.fatal:
        developer.log('\x1B[31m$$message\x1B[0m');
        if (ex != null) developer.log('\x1B[31mException: $$ex\x1B[0m');
        // print('\x1B[31mStackTrace: $$st\x1B[0m');
        break;
      case LoggerLevel.error:
        developer.log('\x1B[91m$$message\x1B[0m');
        if (ex != null) developer.log('\x1B[91mException: $$ex\x1B[0m');
        if (st != null) developer.log("\x1B[31mStackTrace: $$st\x1B[0m");
        break;
      case LoggerLevel.warning:
        developer.log('\x1B[33m$$message\x1B[0m');
        break;
      case LoggerLevel.info:
        developer.log('\x1B[37m$$message\x1B[0m');
        break;
      case LoggerLevel.verbose:
        developer.log('\x1B[34m$$message\x1B[0m');
        break;
      case LoggerLevel.success:
        developer.log('\x1B[32m$$message\x1B[0m');
        break;
      case LoggerLevel.apiReq:
        developer.log('\x1B[93m$$message\x1B[0m');
        break;
      case LoggerLevel.apiRes:
        developer.log('\x1B[32m$$message\x1B[0m');
        break;
    }
  }
}
