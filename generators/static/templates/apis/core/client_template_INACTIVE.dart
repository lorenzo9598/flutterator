// // ignore_for_file: always_specify_types

// import 'package:dio/dio.dart';

// class Client {
//   final String _baseUrl;

//   final Dio dio = Dio();

//   Client(this._baseUrl) {
//     dio.options.baseUrl = _baseUrl;
//   }

//   Future get({required String endpoint, Map<String, dynamic>? queryParams, String? contentType}) async {
//     Response rs = await dio.get(
//       endpoint,
//       queryParameters: queryParams,
//       options: Options(contentType: contentType),
//     );
//     return rs;
//   }

//   Future post({
//     required String endpoint,
//     Map<String, dynamic>? body,
//     Map<String, dynamic>? queryParams,
//     String? contentType,
//   }) async {
//     Response rs = await dio.post(
//       endpoint,
//       queryParameters: queryParams,
//       data: body,
//       options: Options(
//         contentType: contentType,
//       ),
//     );
//     return rs;
//   }

//   Future postList({
//     required String endpoint,
//     List<dynamic>? body,
//     Map<String, dynamic>? queryParams,
//     String? contentType,
//   }) async {
//     Response rs = await dio.post(
//       endpoint,
//       queryParameters: queryParams,
//       data: body,
//       options: Options(
//         contentType: contentType,
//       ),
//     );
//     return rs;
//   }

//   Future put({
//     required String endpoint,
//     Map<String, dynamic>? body,
//     String? contentType,
//   }) async {
//     Response rs = await dio.put(
//       endpoint,
//       data: body,
//       options: Options(
//         contentType: contentType,
//       ),
//     );
//     return rs;
//   }

//   Future delete({required String endpoint, Map<String, dynamic>? body, Map<String, dynamic>? queryParams, String? contentType}) async {
//     Response rs = await dio.delete(
//       endpoint,
//       data: body,
//       queryParameters: queryParams,
//       options: Options(contentType: contentType),
//     );
//     return rs;
//   }
// }
