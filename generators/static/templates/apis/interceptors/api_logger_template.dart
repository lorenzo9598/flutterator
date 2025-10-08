import 'package:dio/dio.dart';
import 'package:$project_name/injection.dart';
import 'package:$project_name/logging/logger.dart';

class ApiLogger extends Interceptor {
  final bool showRequest;
  ApiLogger({
    this.showRequest = false,
    this.request = false,
    this.requestHeader = false,
    this.requestBody = false,
    this.responseHeader = false,
    this.responseBody = false,
    this.error = true,
  });

  /// Print request [Options]
  bool request;

  /// Print request header [Options.headers]
  bool requestHeader;

  /// Print request data [Options.data]
  bool requestBody;

  /// Print [Response.data]
  bool responseBody;

  /// Print [Response.headers]
  bool responseHeader;

  /// Print error message
  bool error;

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) async {
    if (showRequest) {
      _printKV(options.method, options.uri);
    }
    if (request) {
      // _println('[REQUEST]');
      _printKV(options.method, options.uri);
      //options.headers;
      _printKV('method', options.method);
      _printKV('responseType', options.responseType.toString());
      _printKV('followRedirects', options.followRedirects);
      _printKV('connectTimeout', options.connectTimeout);
      _printKV('sendTimeout', options.sendTimeout);
      _printKV('receiveTimeout', options.receiveTimeout);
      _printKV('receiveDataWhenStatusError', options.receiveDataWhenStatusError);
      _printKV('extra', options.extra);
    }
    if (requestHeader) {
      _println('headers:');
      options.headers.forEach((String key, dynamic v) => _printKV(' $$key', v));
    }
    if (requestBody) {
      _println('data:');
      _printAll(options.data);
    }
    // _println('');

    handler.next(options);
  }

  @override
  void onResponse(Response<dynamic> response, ResponseInterceptorHandler handler) async {
    // _println('[RESPONSE]');
    _printResponse(response);
    handler.next(response);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) async {
    if (error) {
      // _println('Dio Error:', statusCode: err.response?.statusCode);
      // // _println('uri: $${err.requestOptions.uri}');
      // if (err.response != null) {
      //   _printResponse(err.response!);
      // }
      _println('$$err', statusCode: err.response?.statusCode);
      _printKV('Message', "$${err.response?.statusMessage}", statusCode: err.response?.statusCode);
    }

    handler.next(err);
  }

  void _printResponse(Response<dynamic> response) {
    final int? statusCode = response.statusCode;
    _printKV(statusCode?.toString() ?? "No status", response.requestOptions.uri, statusCode: statusCode);
    if (responseHeader) {
      _printKV('statusCode', statusCode, statusCode: statusCode);
      if (response.isRedirect == true) {
        _printKV('redirect', response.realUri, statusCode: statusCode);
      }

      _println('headers:', statusCode: statusCode);
      response.headers.forEach((String key, List<String> v) => _printKV(' $$key', v.join('\r\n\t'), statusCode: statusCode));
    }
    if (responseBody) {
      _println('Response Text:', statusCode: statusCode);
      _printAll(response.toString(), statusCode: statusCode);
    }
    // _println('', statusCode: statusCode);
  }

  void _printKV(String key, Object? v, {int? statusCode}) {
    _println('$$key: $$v', statusCode: statusCode);
  }

  void _println(String value, {int? statusCode}) {
    final Logger logger = getIt<Logger>();
    statusCode != null
        ? (statusCode > 399 && statusCode < 600)
            ? statusCode == 401
                ? logger.logWarning(value)
                : logger.logError(value)
            : logger.logApiRes(value)
        : logger.logApiReq(value);
  }

  void _printAll(dynamic msg, {int? statusCode}) {
    msg.toString().split('\n').forEach((String x) => _println(x, statusCode: statusCode));
  }
}
