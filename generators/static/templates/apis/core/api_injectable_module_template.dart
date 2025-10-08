import 'package:dio/dio.dart';
import 'package:injectable/injectable.dart';
import 'package:$project_name/apis/common/constants.dart';
import 'package:$project_name/apis/interceptors/api_logger.dart';
import 'package:$project_name/apis/interceptors/auth_interceptor.dart';

@module
abstract class ApisInjectableModule {
  @lazySingleton
  Dio get dio => Dio()
    ..options.baseUrl = Constants.apiUrl
    ..interceptors.add(ApiLogger())
    ..interceptors.add(AuthInterceptor(Constants.apiUrl));
}
