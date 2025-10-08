import 'package:dartz/dartz.dart';
import 'package:flutter/foundation.dart';
import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:$project_name/model/auth/value_objects.dart';
import 'package:$project_name/model/core/entity.dart';
import 'package:$project_name/model/core/failures.dart';
import 'package:$project_name/model/core/value_objects.dart';

part 'user.freezed.dart';

@freezed
abstract class User with _$$User implements IEntity {
  const factory User({
    required UniqueId id,
    required StringSingleLine name,
    required EmailAddress emailAddress,
  }) = _User;
}

extension UserX on User {
  Option<ValueFailure<dynamic>> get failureOption {
    return name.failureOrUnit.andThen(emailAddress.failureOrUnit).fold((ValueFailure<dynamic> l) => some(l), (Unit r) => none());
  }
}
