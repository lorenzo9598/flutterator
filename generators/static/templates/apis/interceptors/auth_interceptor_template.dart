// ignore_for_file: always_specify_types

import 'package:dio/dio.dart';
import 'package:$project_name/apis/common/constants.dart';
import 'package:$project_name/infrastructure/storage/storage_repository.dart';
// import 'package:firebase_auth/firebase_auth.dart';

/// Interceptor to send the bearer access token
class AuthInterceptor extends QueuedInterceptor {
  final Dio dioAuth;
  final Dio dio;
  AuthInterceptor(String baseUrl)
      : dioAuth = Dio()..options.baseUrl = Constants.apiUrl,
        dio = Dio()..options.baseUrl = baseUrl;

  @override
  void onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    // Load your token here and pass to the header
    String? accessToken = await StorageRepository().getToken();
    String token = 'Bearer $$accessToken';
    options.headers.addAll({Constants.authorizationHeader: token});
    return handler.next(options);
  }

  // You can also perform some actions in the response or onError.
  @override
  void onResponse(Response response, ResponseInterceptorHandler handler) {
    response.extra = {};
    return handler.next(response);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) async {
    if (err.response?.statusCode == 401) {
      try {
        // TODO: Method to refresh the token
        // Uncomment the following code to use Firebase Authentication
        // final String? newToken = await FirebaseAuth.instance.currentUser?.getIdToken(true);
        const String? newToken = null;

        if (newToken == null) {
          StorageRepository().removeToken();
          return handler.next(err);
        }

        final Map<String, dynamic> headers = err.requestOptions.headers;
        String token = 'Bearer $$newToken';
        headers.addAll({Constants.authorizationHeader: token});

        final options = Options(
          method: err.requestOptions.method,
          headers: headers,
        );

        final Response<dynamic> retryResponse = await dio.request<dynamic>(
          err.requestOptions.path,
          data: err.requestOptions.data,
          queryParameters: err.requestOptions.queryParameters,
          options: options,
        );
        if (retryResponse.statusCode != 401) {
          StorageRepository().saveToken(newToken);
          return handler.resolve(retryResponse);
        } else {
          StorageRepository().removeToken();
          return handler.reject(err);
        }
      } catch (ex) {
        StorageRepository().removeToken();
        handler.next(err);
      }
    }
    return handler.next(err);
  }
}
