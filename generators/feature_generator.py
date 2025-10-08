from pathlib import Path
from string import Template

def create_feature(feature_name: str, lib_path: Path, has_api: bool = False):
    """
    Crea una nuova feature con tutti i file necessari seguendo la Clean Architecture
    """
    
    # Determina il nome del progetto dal pubspec.yaml
    pubspec_path = lib_path.parent / "pubspec.yaml"
    project_name = get_project_name_from_pubspec(pubspec_path)
    
    # Crea le cartelle necessarie
    create_feature_directories(lib_path, feature_name)
    
    # Genera tutti i file
    generate_model_files(lib_path, feature_name, project_name)
    generate_presentation_files(lib_path, feature_name, project_name)
    generate_application_files(lib_path, feature_name, project_name)
    generate_infrastructure_files(lib_path, feature_name, project_name)

    add_route_to_router(lib_path, feature_name, project_name)
    
    if has_api:
        generate_api_files(lib_path, feature_name, project_name)

def get_project_name_from_pubspec(pubspec_path: Path) -> str:
    """Estrae il nome del progetto dal pubspec.yaml"""
    try:
        content = pubspec_path.read_text()
        for line in content.split('\n'):
            if line.startswith('name:'):
                return line.split(':', 1)[1].strip()
    except Exception:
        pass
    return "unknown_project"

def create_feature_directories(lib_path: Path, feature_name: str):
    """Crea tutte le directory necessarie per la feature"""
    directories = [
        f"model/{feature_name}",
        f"presentation/{feature_name}",
        f"application/{feature_name}",
        f"infrastructure/{feature_name}",
        f"apis/clients"  # Solo se non esiste già
    ]
    
    for directory in directories:
        dir_path = lib_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)

def generate_model_files(lib_path: Path, feature_name: str, project_name: str):
    """Genera i file del model"""
    singular = feature_name.rstrip('s')  # notes -> note
    
    # model/{feature_name}/{singular}.dart
    model_content = f"""import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:{project_name}/model/core/value_objects.dart';

part '{singular}.freezed.dart';

@freezed
abstract class {singular.title()} with _${singular.title()} {{
  const factory {singular.title()}({{
    required UniqueId id,
    // TODO: add more fields here
    // Example: NoteTitle title,
    required DateTime createdAt,
    required DateTime updatedAt,
    required bool archived,
  }}) = _{singular.title()};
}}
"""

    value_objects_content = f"""// import 'package:dartz/dartz.dart';
// import 'package:prova/model/core/failures.dart';
// import 'package:prova/model/core/value_objects.dart';

// class NoteTitle extends ValueObject<String> {{
//   @override
//   final Either<NoteFailure<String>, String> value;

//   factory NoteTitle(String input) {{
//     return NoteTitle._(
//         // Add validation logic if needed
//         right(input));
//   }}

//   const NoteTitle._(this.value);
// }}
"""
    
    model_file = lib_path / "model" / feature_name / f"{singular}.dart"
    model_file.write_text(model_content)

    value_objects_file = lib_path / "model" / feature_name / "value_objects.dart"
    value_objects_file.write_text(value_objects_content)

def generate_presentation_files(lib_path: Path, feature_name: str, project_name: str):
    """Genera i file della presentation"""
    singular = feature_name.rstrip('s')
    class_name = f"{singular.title()}s"
    
    # presentation/{feature_name}/{feature_name}_screen.dart
    screen_content = f"""import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:caravaggio_ui/caravaggio_ui.dart';
import 'package:{project_name}/application/{feature_name}/{feature_name}_bloc.dart';
import 'package:{project_name}/injection.dart';
import 'package:{project_name}/model/notes/note.dart';
import 'package:{project_name}/infrastructure/notes/note_failure.dart';

class {class_name}Screen extends StatelessWidget {{
  static const String routeName = '/{feature_name}';

  const {class_name}Screen({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return BlocProvider<{class_name}Bloc>(
      create: (BuildContext context) => getIt<{class_name}Bloc>()..add(const {class_name}Event.started()),
      child: Scaffold(
        appBar: AppBar(
          title: CText.title('{class_name}'),
          actions: <Widget>[
            IconButton(
              icon: const Icon(Icons.add),
              onPressed: () {{
                // TODO: Navigate to add {singular} screen
              }},
            ),
          ],
        ),
        body: BlocBuilder<{class_name}Bloc, {class_name}State>(
          builder: (BuildContext context, {class_name}State state) {{
            return switch(state){{
              Initial() => const Center(child: CircularProgressIndicator()),
              Loading() => const Center(child: CircularProgressIndicator()),
              Loaded({feature_name}: List<{singular.title()}> {feature_name}) => ListView.builder(
                itemCount: {feature_name}.length,
                itemBuilder: (BuildContext context, int index) {{
                  final {singular.title()} {singular} = {feature_name}[index];
                  return ListTile(
                    title: Text({singular}.id.getOrCrash()),
                    trailing: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: <Widget>[
                        IconButton(
                          icon: const Icon(Icons.edit),
                          onPressed: () {{
                            // TODO: Edit {singular}
                          }},
                        ),
                        IconButton(
                          icon: const Icon(Icons.delete),
                          onPressed: () {{
                            context.read<{class_name}Bloc>().add(
                              {class_name}Event.deleted({singular}.id),
                            );
                          }},
                        ),
                      ],
                    ),
                  );
                }},
              ),
              Error(failure: {singular.title()}Failure failure) => Center(
                  child: Text('Error: ${{failure.mapFailureToMessage}}'),
              ),
              _ => const SizedBox.shrink(),
            }};
          }},
        ),
      ),
    );
  }}
}}
"""
    
    screen_file = lib_path / "presentation" / feature_name / f"{feature_name}_screen.dart"
    screen_file.write_text(screen_content)

def generate_application_files(lib_path: Path, feature_name: str, project_name: str):
    """Genera i file dell'application (BLoC)"""
    singular = feature_name.rstrip('s')
    class_name = f"{singular.title()}s"
    
    # application/{feature_name}/{feature_name}_bloc.dart
    bloc_content = f"""import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:injectable/injectable.dart';
import 'package:{project_name}/model/{feature_name}/{singular}.dart';
import 'package:{project_name}/model/{feature_name}/i_{feature_name}_repository.dart';
import 'package:{project_name}/infrastructure/notes/note_failure.dart';
import 'package:{project_name}/model/core/value_objects.dart';
import 'package:dartz/dartz.dart';

part '{feature_name}_event.dart';
part '{feature_name}_state.dart';
part '{feature_name}_bloc.freezed.dart';

@injectable
class {class_name}Bloc extends Bloc<{class_name}Event, {class_name}State> {{
  final I{class_name}Repository _{feature_name}Repository;

  {class_name}Bloc(this._{feature_name}Repository) : super(const {class_name}State.initial()) {{
    on<_Started>(_onStarted);
    on<_Reloaded>(_onReloaded);
    on<_Deleted>(_onDeleted);
  }}

  void _onStarted(_Started event, Emitter<{class_name}State> emit) async {{
    emit(const {class_name}State.loading());
    final Either<{singular.title()}Failure, List<{singular.title()}>> result = await _{feature_name}Repository.getAll();
    result.fold(
      ({singular.title()}Failure failure) => emit({class_name}State.error(failure)),
      (List<{singular.title()}> {feature_name}) => emit({class_name}State.loaded({feature_name})),
    );
  }}

  void _onReloaded(_Reloaded event, Emitter<{class_name}State> emit) async {{
    emit(const {class_name}State.loading());
    final Either<{singular.title()}Failure, List<{singular.title()}>> result = await _{feature_name}Repository.getAll();
    result.fold(
      ({singular.title()}Failure failure) => emit({class_name}State.error(failure)),
      (List<{singular.title()}> {feature_name}) => emit({class_name}State.loaded({feature_name})),
    );
  }}

  void _onDeleted(_Deleted event, Emitter<{class_name}State> emit) async {{
    emit(const {class_name}State.loading());
    final Either<{singular.title()}Failure, Unit> result = await _{feature_name}Repository.delete(event.id);
    result.fold(
      ({singular.title()}Failure failure) => emit({class_name}State.error(failure)),
      (_) => add(const {class_name}Event.started()),
    );
  }}
}}
"""
    
    # Crea anche i file event e state
    event_content = f"""part of '{feature_name}_bloc.dart';

@freezed
class {class_name}Event with _${class_name}Event {{
  const factory {class_name}Event.started() = _Started;
  const factory {class_name}Event.reloaded({singular.title()} {singular}) = _Reloaded;
  const factory {class_name}Event.deleted(UniqueId id) = _Deleted;
}}
"""
    
    state_content = f"""part of '{feature_name}_bloc.dart';

@freezed
class {class_name}State with _${class_name}State {{
  const factory {class_name}State.initial() = Initial;
  const factory {class_name}State.loading() = Loading;
  const factory {class_name}State.loaded(List<{singular.title()}> {feature_name}) = Loaded;
  const factory {class_name}State.error(NoteFailure failure) = Error;
}}
"""
    
    bloc_file = lib_path / "application" / feature_name / f"{feature_name}_bloc.dart"
    event_file = lib_path / "application" / feature_name / f"{feature_name}_event.dart"
    state_file = lib_path / "application" / feature_name / f"{feature_name}_state.dart"
    
    bloc_file.write_text(bloc_content)
    event_file.write_text(event_content)
    state_file.write_text(state_content)

def generate_infrastructure_files(lib_path: Path, feature_name: str, project_name: str):
    """Genera i file dell'infrastructure"""
    singular = feature_name.rstrip('s')
    class_name = f"{singular.title()}s"
    
    # model/{feature_name}/i_{feature_name}_repository.dart
    interface_content = f"""import 'package:dartz/dartz.dart';
import 'package:{project_name}/model/{feature_name}/{singular}.dart';
import 'package:{project_name}/model/core/value_objects.dart';
import 'package:{project_name}/infrastructure/notes/note_failure.dart';

abstract class I{class_name}Repository {{
  Future<Either<NoteFailure, List<{singular.title()}>>> getAll();
  Future<Either<NoteFailure, {singular.title()}>> getById(UniqueId id);
  Future<Either<NoteFailure, Unit>> create({singular.title()} {singular});
  Future<Either<NoteFailure, Unit>> update({singular.title()} {singular});
  Future<Either<NoteFailure, Unit>> delete(UniqueId id);
}}
"""
    
    # infrastructure/{feature_name}/{singular}_dto.dart
    dto_content = f"""import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:{project_name}/model/{feature_name}/{singular}.dart';
import 'package:{project_name}/model/core/value_objects.dart';

part '{singular}_dto.freezed.dart';
part '{singular}_dto.g.dart';

@freezed
abstract class {singular.title()}Dto with _${singular.title()}Dto {{
  const factory {singular.title()}Dto({{
    required String id,
    required DateTime createdAt,
    required DateTime updatedAt,
    required bool archived,
  }}) = _{singular.title()}Dto;

  factory {singular.title()}Dto.fromJson(Map<String, dynamic> json) => _${singular.title()}DtoFromJson(json);

  factory {singular.title()}Dto.fromDomain({singular.title()} {singular}) {{
    return {singular.title()}Dto(
      id: {singular}.id.getOrCrash(),
      createdAt: {singular}.createdAt,
      updatedAt: {singular}.updatedAt,
      archived: {singular}.archived,
    );
  }}
}}

extension {singular.title()}DtoX on {singular.title()}Dto {{
  {singular.title()} toDomain() {{
    return {singular.title()}(
      id: UniqueId.fromUniqueString(id),
      createdAt: createdAt,
      updatedAt: updatedAt,
      archived: archived,
    );
  }}
}}
"""

    # infrastructure/{feature_name}/{singular}_failure.dart
    failure_content = f"""import 'package:freezed_annotation/freezed_annotation.dart';

part '{singular}_failure.freezed.dart';

@freezed
abstract class {singular.title()}Failure with _${singular.title()}Failure {{
  const {singular.title()}Failure._();

  const factory {singular.title()}Failure.unexpected() = _Unexpected;
  const factory {singular.title()}Failure.insufficientPermission() = _InsufficientPermission;
  const factory {singular.title()}Failure.unableToUpdate() = _UnableToUpdate;
  const factory {singular.title()}Failure.unableToDelete() = _UnableToDelete;
  const factory {singular.title()}Failure.unableToCreate() = _UnableToCreate;
  const factory {singular.title()}Failure.notFound() = _NotFound;
  const factory {singular.title()}Failure.serverError() = _ServerError;

  String get mapFailureToMessage => switch (this) {{
      _Unexpected() => "Unexpected error",
      _InsufficientPermission() => "Insufficient permissions",
      _UnableToUpdate() => "Unable to update",
      _UnableToDelete() => "Unable to delete",
      _UnableToCreate() => "Unable to create",
      _NotFound() => "Not found",
      _ServerError() => "Server error",
      _ => "Unknown error",
    }};
}}
"""
    
    interface_file = lib_path / "model" / feature_name / f"i_{feature_name}_repository.dart"
    dto_file = lib_path / "infrastructure" / feature_name / f"{singular}_dto.dart"
    failure_file = lib_path / "infrastructure" / feature_name / f"{singular}_failure.dart"
    
    interface_file.write_text(interface_content)
    dto_file.write_text(dto_content)
    failure_file.write_text(failure_content)

def generate_api_files(lib_path: Path, feature_name: str, project_name: str):
    """Genera i file API per il CRUD"""
    singular = feature_name.rstrip('s')
    class_name = f"{singular.title()}s"
    
    # apis/clients/{feature_name}_client.dart
    api_content = f"""import 'package:dio/dio.dart';
import 'package:injectable/injectable.dart';
import 'package:retrofit/retrofit.dart';
import 'package:{project_name}/infrastructure/{feature_name}/{singular}_dto.dart';

part '{feature_name}_client.g.dart';

@injectable
@RestApi()
abstract class {class_name}Client {{
  @factoryMethod
  factory {class_name}Client(Dio dio) = _{class_name}Client;

  @GET('/{feature_name}')
  Future<List<{singular.title()}Dto>> getAll();

  @GET('/{feature_name}/{{id}}')
  Future<{singular.title()}Dto> getById(@Path('id') String id);

  @POST('/{feature_name}')
  Future<{singular.title()}Dto> create(@Body() {singular.title()}Dto {singular});

  @PUT('/{feature_name}/{{id}}')
  Future<{singular.title()}Dto> update(
    @Path('id') String id,
    @Body() {singular.title()}Dto {singular},
  );

  @DELETE('/{feature_name}/{{id}}')
  Future<void> delete(@Path('id') String id);
}}
"""
    
    # infrastructure/{feature_name}/{feature_name}_repository.dart (implementazione)
    repo_impl_content = f"""import 'package:dartz/dartz.dart';
import 'package:injectable/injectable.dart';
import 'package:{project_name}/apis/clients/{feature_name}_client.dart';
import 'package:{project_name}/infrastructure/{feature_name}/{singular}_dto.dart';
import 'package:{project_name}/model/{feature_name}/{singular}.dart';
import 'package:{project_name}/model/{feature_name}/i_{feature_name}_repository.dart';
import 'package:{project_name}/model/core/value_objects.dart';
import 'package:{project_name}/infrastructure/notes/note_failure.dart';

@LazySingleton(as: I{class_name}Repository)
class {class_name}Repository implements I{class_name}Repository {{
  final {class_name}Client _{feature_name}Client;

  {class_name}Repository(this._{feature_name}Client);

  @override
  Future<Either<NoteFailure, List<{singular.title()}>>> getAll() async {{
    try {{
      final List<{singular.title()}Dto> dtos = await _{feature_name}Client.getAll();
      final List<{singular.title()}> {feature_name} = dtos.map(({singular.title()}Dto dto) => dto.toDomain()).toList();
      return right({feature_name});
    }} catch (e) {{
      return left(const NoteFailure.serverError());
    }}
  }}

  @override
  Future<Either<NoteFailure, {singular.title()}>> getById(UniqueId id) async {{
    try {{
      final {singular.title()}Dto dto = await _{feature_name}Client.getById(id.getOrCrash());
      return right(dto.toDomain());
    }} catch (e) {{
      return left(const NoteFailure.serverError());
    }}
  }}

  @override
  Future<Either<NoteFailure, Unit>> create({singular.title()} {singular}) async {{
    try {{
      final {singular.title()}Dto dto = {singular.title()}Dto.fromDomain({singular});
      await _{feature_name}Client.create(dto);
      return right(unit);
    }} catch (e) {{
      return left(const NoteFailure.serverError());
    }}
  }}

  @override
  Future<Either<NoteFailure, Unit>> update({singular.title()} {singular}) async {{
    try {{
      final {singular.title()}Dto dto = {singular.title()}Dto.fromDomain({singular});
      await _{feature_name}Client.update({singular}.id.getOrCrash(), dto);
      return right(unit);
    }} catch (e) {{
      return left(const NoteFailure.serverError());
    }}
  }}

  @override
  Future<Either<NoteFailure, Unit>> delete(UniqueId id) async {{
    try {{
      await _{feature_name}Client.delete(id.getOrCrash());
      return right(unit);
    }} catch (e) {{
      return left(const NoteFailure.serverError());
    }}
  }}
}}
"""
    
    api_file = lib_path / "apis" / "clients" / f"{feature_name}_client.dart"
    repo_impl_file = lib_path / "infrastructure" / feature_name / f"{feature_name}_repository.dart"
    
    api_file.write_text(api_content)
    repo_impl_file.write_text(repo_impl_content)

def add_route_to_router(lib_path: Path, feature_name: str, project_name: str):
        """Aggiunge la nuova route al router dell'app"""
        singular = feature_name.rstrip('s')
        class_name = f"{singular.title()}s"
        
        # Cerca il file router (possibili nomi comuni)
        possible_router_files = [
            "router.dart",
            "app_router.dart", 
            "routes.dart",
            "routing.dart"
        ]
        
        router_file = None
        for filename in possible_router_files:
            potential_path = lib_path / filename
            if potential_path.exists():
                router_file = potential_path
                break
        
        if not router_file:
            # Se non trova il router, crea un file di esempio
            print("Router file not found. Please add the route manually.")
            return
        
        # Legge il contenuto esistente del router
        content = router_file.read_text()
        
        # Aggiunge l'import se non esiste già
        import_line = f"import 'package:{project_name}/presentation/{feature_name}/{feature_name}_screen.dart';"
        if import_line not in content:
            # Trova l'ultimo import e aggiunge dopo
            lines = content.split('\n')
            import_index = -1
            for i, line in enumerate(lines):
                if line.strip().startswith('import '):
                    import_index = i
            
            if import_index >= 0:
                lines.insert(import_index + 1, import_line)
                content = '\n'.join(lines)
        
        # Configurazione della route
        route_content = f"""
    GoRoute(
      path: {class_name}Screen.routeName,
      builder: (context, state) => const {class_name}Screen(),
    ),
    """
        # Aggiunge la route nel blocco delle rotte
        if route_content.strip() not in content:
            # Trova la posizione dove inserire la nuova route
            insert_index = content.rfind('GoRoute(')
            if insert_index != -1:
                # Trova la fine del blocco delle rotte
                end_index = content.find(']', insert_index)
                if end_index != -1:
                    content = content[:end_index] + route_content + content[end_index:]
                    print("Route added to router configuration.")
            else:
                print("Could not find GoRoute block. Please add the route manually.")
                return
        else:
            print("Route already exists in router configuration.")
            return
        
        router_file.write_text(content)