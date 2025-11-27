#!/usr/bin/env python3

import click
import os
import sys
from pathlib import Path
import shutil
from generators import *
from generators.templates.copier import generate_file
import subprocess

def run_flutter_commands(project_path):
    """Run flutter pub get and build_runner build after project modifications"""
    try:
        click.echo("📦 Running flutter pub get...")
        subprocess.run(["flutter", "pub", "get"], cwd=project_path, check=True, capture_output=True)
        
        # Check if build_runner is available before running it
        try:
            click.echo("🔨 Running dart run build_runner build...")
            subprocess.run(["dart", "run", "build_runner", "build"], cwd=project_path, check=True, capture_output=True)
        except subprocess.CalledProcessError:
            click.echo("⚠️ build_runner not available or failed. You may need to add it as a dev dependency.")
        
        click.echo("✅ Dependencies updated!")
    except subprocess.CalledProcessError as e:
        click.echo(f"⚠️ Warning: Could not run flutter commands: {e}")
        click.echo("You may need to run 'flutter pub get' manually.")

@click.group()
def cli():
    """
    🚀 Flutterator - CLI to create and manage Flutter projects with custom structure
    
    Created by Lorenzo Busi @ GetAutomation
    
    """
    pass

@cli.command()
@click.option('--name', prompt='Project name', help='Name of the Flutter project')
@click.option('--login', is_flag=True, prompt='Does the project have login?', help='Include login functionality')
def create(name, login):
    """
    Create a new Flutter project with custom structure
    """
    print(name)
    # Project name validation
    if not name.replace('_', '').replace('-', '').isalnum():
        click.echo("❌ The project name must contain only letters, numbers, _ and -")
        sys.exit(1)

    # Convert name for Flutter (lowercase with underscore)
    flutter_name = name.lower().replace('-', '_')

    init(flutter_name, login)
    
    # Run flutter commands after project creation
    run_flutter_commands(Path(flutter_name))

@cli.command()
@click.option('--name', prompt='Page name', help='Name of the page to add')
@click.option('--project-path', default='.', help='Path to the Flutter project (default: current directory)')
def add_page(name, project_path):
    """
    Add a new page to an existing Flutter project
    """
    project_dir = Path(project_path)
    if not (project_dir / "pubspec.yaml").exists():
        click.echo("❌ Not a valid Flutter project. pubspec.yaml not found.")
        sys.exit(1)
    
    lib_path = project_dir / "lib"
    if not lib_path.exists():
        click.echo("❌ lib directory not found.")
        sys.exit(1)
    
    # Convert name to appropriate format
    page_name = name.lower().replace(' ', '_')
    
    click.echo(f"📄 Adding page: {page_name}")
    
    # Create page directory structure
    page_dir = lib_path / page_name
    page_dir.mkdir(exist_ok=True)
    
    # Create presentation layer
    presentation_dir = page_dir / "presentation"
    presentation_dir.mkdir(exist_ok=True)
    
    # Generate page file
    generate_page_file(page_name, presentation_dir)
    
    # Update router
    update_router(project_dir, page_name)
    
    # Run Flutter commands to update dependencies and generate code
    run_flutter_commands(project_dir)
    
    click.echo(f"✅ Page '{page_name}' added successfully!")

@cli.command()
@click.option('--name', prompt='Feature name', help='Name of the feature to add')
@click.option('--fields', help='Model fields in format: field1:type,field2:type (e.g., title:string,done:bool)')
@click.option('--interactive', is_flag=True, help='Interactive mode to add fields one by one')
@click.option('--project-path', default='.', help='Path to the Flutter project (default: current directory)')
def add_feature(name, fields, interactive, project_path):
    """
    Add a complete feature to an existing Flutter project
    """
    project_dir = Path(project_path)
    if not (project_dir / "pubspec.yaml").exists():
        click.echo("❌ Not a valid Flutter project. pubspec.yaml not found.")
        sys.exit(1)
    
    lib_path = project_dir / "lib"
    if not lib_path.exists():
        click.echo("❌ lib directory not found.")
        sys.exit(1)
    
    # Get project name from pubspec.yaml
    pubspec_path = project_dir / "pubspec.yaml"
    project_name = project_dir.name  # fallback
    if pubspec_path.exists():
        with open(pubspec_path, 'r') as f:
            for line in f:
                if line.strip().startswith('name:'):
                    project_name = line.split(':', 1)[1].strip().strip('"').strip("'")
                    break
    
    # Convert name to appropriate format
    feature_name = name.lower().replace(' ', '_')
    
    # Parse fields
    field_list = []
    if interactive:
        click.echo("🔧 Adding fields interactively. Type 'done' when finished.")
        while True:
            field_name = click.prompt("Field name (or 'done')")
            if field_name.lower() == 'done':
                break
            field_type = click.prompt("Field type", default='String')
            field_list.append({'name': field_name.strip(), 'type': field_type.strip()})
    elif fields:
        for field in fields.split(','):
            field_name, field_type = field.split(':')
            field_list.append({'name': field_name.strip(), 'type': field_type.strip()})
    
    # Automatically add 'id' field as the first field
    field_list.insert(0, {'name': 'id', 'type': 'string'})
    
    if not field_list:
        click.echo("❌ No fields specified. Use --fields or --interactive")
        sys.exit(1)
    
    click.echo(f"🔧 Adding feature: {feature_name} with fields: {', '.join([f'{f['name']}:{f['type']}' for f in field_list])}")
    
    # Create feature directory structure
    feature_dir = lib_path / feature_name
    feature_dir.mkdir(exist_ok=True)
    
    # Create all layers
    create_feature_layers(feature_dir, feature_name, field_list, project_name)
    
    # Update router
    update_router(project_dir, feature_name)
    
    # Run Flutter commands to update dependencies and generate code
    run_flutter_commands(project_dir)
    
    click.echo(f"✅ Feature '{feature_name}' added successfully!")

@cli.command()
@click.option('--name', prompt='Drawer item name', help='Name of the drawer item to add')
@click.option('--project-path', default='.', help='Path to the Flutter project (default: current directory)')
def add_drawer_item(name, project_path):
    """
    Add a drawer navigation item to an existing Flutter project
    """
    project_dir = Path(project_path)
    if not (project_dir / "pubspec.yaml").exists():
        click.echo("❌ Not a valid Flutter project. pubspec.yaml not found.")
        sys.exit(1)
    
    lib_path = project_dir / "lib"
    if not lib_path.exists():
        click.echo("❌ lib directory not found.")
        sys.exit(1)
    
    # Convert name to appropriate format
    drawer_item_name = name.lower().replace(' ', '_')
    
    click.echo(f"📱 Adding drawer item: {drawer_item_name}")
    
    # Check if home screen exists
    home_presentation_dir = lib_path / "home" / "presentation"
    if not home_presentation_dir.exists():
        click.echo("❌ Home presentation directory not found. Make sure this is a Flutterator project.")
        sys.exit(1)
    
    # Create page for the drawer item
    create_drawer_page(project_dir, drawer_item_name)
    
    # Update home screen to include drawer
    update_home_screen_with_drawer(project_dir, drawer_item_name)
    
    # Create drawer widget if it doesn't exist
    create_drawer_widget(project_dir, drawer_item_name)
    
    click.echo(f"✅ Drawer item '{drawer_item_name}' added successfully!")

@cli.command()
@click.option('--name', prompt='Bottom nav item name', help='Name of the bottom navigation item to add')
@click.option('--project-path', default='.', help='Path to the Flutter project (default: current directory)')
def add_bottom_nav_item(name, project_path):
    """
    Add a bottom navigation item to an existing Flutter project
    """
    project_dir = Path(project_path)
    if not (project_dir / "pubspec.yaml").exists():
        click.echo("❌ Not a valid Flutter project. pubspec.yaml not found.")
        sys.exit(1)
    
    lib_path = project_dir / "lib"
    if not lib_path.exists():
        click.echo("❌ lib directory not found.")
        sys.exit(1)
    
    # Convert name to appropriate format
    bottom_nav_item_name = name.lower().replace(' ', '_')
    
    click.echo(f"📱 Adding bottom nav item: {bottom_nav_item_name}")
    
    # Check if home screen exists
    home_presentation_dir = lib_path / "home" / "presentation"
    if not home_presentation_dir.exists():
        click.echo("❌ Home presentation directory not found. Make sure this is a Flutterator project.")
        sys.exit(1)
    
    # Create page for the bottom nav item
    create_bottom_nav_page(project_dir, bottom_nav_item_name)
    
    # Update home screen to include bottom navigation
    update_home_screen_with_bottom_nav(project_dir, bottom_nav_item_name)
    
    # Create bottom navigation widget if it doesn't exist
    create_bottom_nav_widget(project_dir, bottom_nav_item_name)
    
    # Run Flutter commands to update dependencies and generate code
    run_flutter_commands(project_dir)
    
    click.echo(f"✅ Bottom nav item '{bottom_nav_item_name}' added successfully!")

def generate_page_file(page_name, presentation_dir):
    """Generate a basic page file"""
    page_content = f"""import 'package:flutter/material.dart';

class {page_name.capitalize()}Page extends StatelessWidget {{
  static const String routeName = '/{page_name}';
  
  const {page_name.capitalize()}Page({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(
        title: const Text('{page_name.replace("_", " ").capitalize()}'),
      ),
      body: const Center(
        child: Text('{page_name.replace("_", " ").capitalize()} Page'),
      ),
    );
  }}
}}
"""
    (presentation_dir / f"{page_name}_page.dart").write_text(page_content)

def update_router(project_dir, page_name):
    """Update the router.dart file to include the new page"""
    router_path = project_dir / "lib" / "router.dart"
    if not router_path.exists():
        click.echo("⚠️ router.dart not found, skipping router update")
        return
    
    # Read current router
    content = router_path.read_text()
    
    # Add import
    import_line = f"import 'package:{project_dir.name}/{page_name}/presentation/{page_name}_page.dart';"
    if import_line not in content:
        # Find where to insert import (after other imports)
        lines = content.split('\n')
        insert_index = 0
        for i, line in enumerate(lines):
            if line.startswith('import'):
                insert_index = i + 1
            elif line.strip() and not line.startswith('//'):
                break
        
        lines.insert(insert_index, import_line)
        content = '\n'.join(lines)
    
    # Add route
    route_line = f"""GoRoute(
      path: {page_name.capitalize()}Page.routeName,
      builder: (BuildContext context, GoRouterState state) => const {page_name.capitalize()}Page(),
    ),"""
    if route_line not in content:
        # Find routes list and add the new route before the closing bracket
        if 'routes: <RouteBase>[' in content:
            # Replace the closing bracket with the new route + closing bracket
            content = content.replace('  ],', f'    {route_line}\n  ],')
        elif 'routes: [' in content:
            content = content.replace('  ],', f'    {route_line}\n  ],')
        else:
            click.echo("⚠️ Could not find routes list in router.dart")
    
    router_path.write_text(content)

def create_feature_layers(feature_dir, feature_name, field_list, project_name):
    """Create all layers for a feature"""
    # Model layer
    model_dir = feature_dir / "model"
    model_dir.mkdir(exist_ok=True)
    
    # Create value objects and validators
    generate_value_objects_and_validators(feature_name, field_list, model_dir, project_name)
    
    # Create entity (domain model)
    entity_fields = []
    for field in field_list:
        field_name = field['name']
        if field_name == 'id':
            entity_fields.append(f"  required UniqueId id,")
        else:
            entity_fields.append(f"  required {field_name.capitalize()} {field_name},")
    
    entity_fields_str = "\n".join(entity_fields)
    generate_file(project_name, model_dir, "feature/feature_entity_template.jinja", f"{feature_name}.dart", {
        "feature_name": feature_name, 
        "fields": entity_fields_str
    })
    
    # Create failure
    generate_file(project_name, model_dir, "feature/feature_failure_template.jinja", f"{feature_name}_failure.dart", {"feature_name": feature_name})
    
    # Infrastructure layer
    infra_dir = feature_dir / "infrastructure"
    infra_dir.mkdir(exist_ok=True)
    
    # Create DTO
    dto_fields = ",\n".join([f"    required {map_field_type(field['type'])} {field['name']}" for field in field_list])
    generate_file(project_name, infra_dir, "feature/feature_dto_template.jinja", f"{feature_name}_dto.dart", {"feature_name": feature_name, "fields": dto_fields})
    
    # Create extensions for DTO-Domain conversions
    generate_extensions(feature_name, field_list, infra_dir, project_name)
    
    # Create repository interface
    generate_file(project_name, model_dir, "feature/i_feature_repository_template.jinja", f"i_{feature_name}_repository.dart", {"feature_name": feature_name})
    
    # Create repository implementation
    generate_file(project_name, infra_dir, "feature/feature_repository_template.jinja", f"{feature_name}_repository.dart", {"feature_name": feature_name})
    
    # Application layer
    app_dir = feature_dir / "application"
    app_dir.mkdir(exist_ok=True)
    
    # Create BLoC files
    generate_file(project_name, app_dir, "feature/feature_event_template.jinja", f"{feature_name}_event.dart", {"feature_name": feature_name})
    generate_file(project_name, app_dir, "feature/feature_state_template.jinja", f"{feature_name}_state.dart", {"feature_name": feature_name})
    generate_file(project_name, app_dir, "feature/feature_bloc_template.jinja", f"{feature_name}_bloc.dart", {"feature_name": feature_name})
    
    # Presentation layer
    presentation_dir = feature_dir / "presentation"
    presentation_dir.mkdir(exist_ok=True)
    
    # Create page
    generate_file(project_name, presentation_dir, "feature/feature_page_template.jinja", f"{feature_name}_page.dart", {"feature_name": feature_name})

def map_field_type(field_type):
    """Map field type from string to Dart type"""
    type_mapping = {
        'string': 'String',
        'int': 'int',
        'double': 'double',
        'bool': 'bool',
        'date': 'DateTime',
        'datetime': 'DateTime',
    }
    return type_mapping.get(field_type.lower(), 'String')

def generate_value_objects_and_validators(feature_name, field_list, model_dir, project_name):
    """Generate consolidated value objects and validators"""
    # Generate value objects (base + specific ones)
    value_objects_content = generate_consolidated_value_objects(feature_name, field_list, project_name)
    (model_dir / "value_objects.dart").write_text(value_objects_content)
    
    # Generate validators
    validators_content = generate_value_validators(feature_name, field_list, project_name)
    (model_dir / "value_validators.dart").write_text(validators_content)

def generate_consolidated_value_objects(feature_name, field_list, project_name):
    """Generate consolidated value objects file"""
    # Base ValueObject class
    base_vo = f"""import 'package:dartz/dartz.dart';
import 'package:{project_name}/core/model/failures.dart';
import 'package:{project_name}/core/model/value_objects.dart';
import 'package:{project_name}/{feature_name}/model/value_validators.dart';

"""
    
    # Specific Value Objects for each field (excluding 'id' since we have UniqueId)
    field_vos = []
    for field in field_list:
        field_name = field['name']
        # Skip 'id' field since we have UniqueId
        if field_name == 'id':
            continue
            
        field_type = map_field_type(field['type'])
        capitalized_name = field_name.capitalize()
        
        field_vo = f"""
class {capitalized_name} extends ValueObject<{field_type}> {{
  @override
  final Either<ValueFailure<{field_type}>, {field_type}> value;

  factory {capitalized_name}({field_type} input) {{
    return {capitalized_name}._(validate{capitalized_name}(input));
  }}

  const {capitalized_name}._(this.value);
}}
"""
        field_vos.append(field_vo)
    
    return base_vo + "\n".join(field_vos)

def generate_value_validators(feature_name, field_list, project_name):
    """Generate value validators file"""
    validators = []
    
    for field in field_list:
        field_name = field['name']
        # Skip 'id' field since UniqueId doesn't need custom validation
        if field_name == 'id':
            continue
            
        field_type = map_field_type(field['type'])
        capitalized_name = field_name.capitalize()
        
        # Generate appropriate validation based on type
        if field_type == 'String':
            validator = f"""
Either<ValueFailure<String>, String> validate{capitalized_name}(String input) {{
  if (input.isEmpty) {{
    return left(ValueFailure.empty(failedValue: input));
  }}
  // Additional string validations can be added here
  return right(input);
}}
"""
        elif field_type == 'int':
            validator = f"""
Either<ValueFailure<int>, int> validate{capitalized_name}(int input) {{
  // Additional int validations can be added here
  return right(input);
}}
"""
        elif field_type == 'double':
            validator = f"""
Either<ValueFailure<double>, double> validate{capitalized_name}(double input) {{
  // Additional double validations can be added here
  return right(input);
}}
"""
        elif field_type == 'bool':
            validator = f"""
Either<ValueFailure<bool>, bool> validate{capitalized_name}(bool input) {{
  // Boolean validation - always valid
  // Additional boolean validations can be added here
  return right(input);
}}
"""
        elif field_type == 'DateTime':
            validator = f"""
Either<ValueFailure<DateTime>, DateTime> validate{capitalized_name}(DateTime input) {{
  // Additional datetime validations can be added here
  return right(input);
}}
"""
        else:
            # Default string validation for unknown types
            validator = f"""
Either<ValueFailure<String>, String> validate{capitalized_name}(String input) {{
  if (input.isEmpty) {{
    return left(ValueFailure.empty(failedValue: input));
  }}
  // Additional string validations can be added here
  return right(input);
}}
"""
        
        validators.append(validator)

    return f"import 'package:dartz/dartz.dart';\nimport 'package:{project_name}/core/model/failures.dart';\n\n" + "\n".join(validators)

def generate_extensions(feature_name, field_list, infra_dir, project_name):
    """Generate DTO-Domain conversion extensions"""
    
    # Generate toDto() method
    to_dto_fields = []
    for field in field_list:
        field_name = field['name']
        if field_name == 'id':
            to_dto_fields.append(f"      id: id.getOrCrash()")
        else:
            to_dto_fields.append(f"      {field_name}: {field_name}.getOrCrash()")
    
    # Generate fromDto() method
    from_dto_fields = []
    for field in field_list:
        field_name = field['name']
        if field_name == 'id':
            from_dto_fields.append(f"      id: UniqueId.fromUniqueString(id)")
        else:
            capitalized_name = field_name.capitalize()
            from_dto_fields.append(f"      {field_name}: {capitalized_name}({field_name})")
    
    extension_content = f"""import 'package:{project_name}/core/model/value_objects.dart';
import 'package:{project_name}/{feature_name}/model/{feature_name}.dart';
import 'package:{project_name}/{feature_name}/model/value_objects.dart';
import 'package:{project_name}/{feature_name}/infrastructure/{feature_name}_dto.dart';

extension {feature_name.capitalize()}DtoX on {feature_name.capitalize()}Dto {{
  {feature_name.capitalize()} toDomain() {{
    return {feature_name.capitalize()}(
{',\n'.join(from_dto_fields)}
    );
  }}
}}

extension {feature_name.capitalize()}DomainX on {feature_name.capitalize()} {{
  {feature_name.capitalize()}Dto toDto() {{
    return {feature_name.capitalize()}Dto(
{',\n'.join(to_dto_fields)}
    );
  }}
}}

"""
    (infra_dir / f"{feature_name}_extensions.dart").write_text(extension_content)

def create_drawer_page(project_dir, drawer_item_name):
    """Create a page for the drawer item"""
    lib_path = project_dir / "lib"
    
    # Create page directory structure
    page_dir = lib_path / drawer_item_name
    page_dir.mkdir(exist_ok=True)
    
    # Create presentation layer
    presentation_dir = page_dir / "presentation"
    presentation_dir.mkdir(exist_ok=True)
    
    # Generate page file
    generate_page_file(drawer_item_name, presentation_dir)
    
    # Update router
    update_router(project_dir, drawer_item_name)

def update_home_screen_with_drawer(project_dir, drawer_item_name):
    """Update the home screen to include a drawer"""
    home_screen_path = project_dir / "lib" / "home" / "presentation" / "home_screen.dart"
    
    if not home_screen_path.exists():
        click.echo("⚠️ Home screen not found, creating basic drawer implementation")
        return
    
    content = home_screen_path.read_text()
    
    # Check if drawer is already implemented
    if "drawer:" in content:
        click.echo("ℹ️ Drawer already exists in home screen")
        return
    
    # Add drawer import if not present
    project_name = project_dir.name
    drawer_import = f"import 'package:{project_name}/core/presentation/app_drawer.dart';"
    if drawer_import not in content:
        # Add import after existing imports
        lines = content.split('\n')
        insert_index = 0
        for i, line in enumerate(lines):
            if line.startswith('import'):
                insert_index = i + 1
            elif line.strip() and not line.startswith('//'):
                break
        
        lines.insert(insert_index, drawer_import)
        content = '\n'.join(lines)
    
    # Modify the Scaffold to include drawer
    # Replace "return const Scaffold(" with "return Scaffold(" and add drawer
    if "return const Scaffold(" in content:
        content = content.replace(
            "return const Scaffold(",
            "return Scaffold(\n      drawer: const AppDrawer(),"
        )
    elif "return Scaffold(" in content:
        # If it's already non-const, just add the drawer
        if "drawer:" not in content:
            content = content.replace(
                "return Scaffold(",
                "return Scaffold(\n      drawer: const AppDrawer(),"
            )
    
    home_screen_path.write_text(content)

def create_drawer_widget(project_dir, drawer_item_name):
    """Create or update the drawer widget"""
    core_presentation_dir = project_dir / "lib" / "core" / "presentation"
    core_presentation_dir.mkdir(parents=True, exist_ok=True)
    
    drawer_path = core_presentation_dir / "app_drawer.dart"
    
    if drawer_path.exists():
        # Update existing drawer - add new drawer item
        content = drawer_path.read_text()
        
        # Add import for the new page
        project_name = project_dir.name
        page_import = f"import 'package:{project_name}/{drawer_item_name}/presentation/{drawer_item_name}_page.dart';"
        if page_import not in content:
            # Add import after existing imports
            lines = content.split('\n')
            insert_index = 0
            for i, line in enumerate(lines):
                if line.startswith('import'):
                    insert_index = i + 1
                elif line.strip() and not line.startswith('//'):
                    break
            
            lines.insert(insert_index, page_import)
            content = '\n'.join(lines)
        
        # Add new drawer item to the list - replace the closing bracket of children list
        if f"{drawer_item_name.capitalize()}Page.routeName" not in content:
            capitalized_name = drawer_item_name.replace('_', ' ').title()
            class_name = drawer_item_name.capitalize() + 'Page'
            new_tile = f"""          ListTile(
            leading: const Icon(Icons.star),
            title: const Text('{capitalized_name}'),
            onTap: () {{
              Navigator.of(context).pop(); // Close drawer
              context.go({class_name}.routeName);
            }},
          ),"""
            
            # Replace the closing bracket of the children list with the new tile + closing bracket
            content = content.replace('        ],', f'          {new_tile}\n        ],')
        
        drawer_path.write_text(content)
    else:
        # Create new drawer widget
        project_name = project_dir.name
        capitalized_name = drawer_item_name.replace('_', ' ').title()
        class_name = drawer_item_name.capitalize() + 'Page'
        
        drawer_content = f"""import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:{project_name}/home/presentation/home_screen.dart';
import 'package:{project_name}/{drawer_item_name}/presentation/{drawer_item_name}_page.dart';

class AppDrawer extends StatelessWidget {{
  const AppDrawer({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          const DrawerHeader(
            decoration: BoxDecoration(
              color: Colors.blue,
            ),
            child: Text(
              'App Navigation',
              style: TextStyle(
                color: Colors.white,
                fontSize: 24,
              ),
            ),
          ),
          ListTile(
            leading: const Icon(Icons.home),
            title: const Text('Home'),
            onTap: () {{
              Navigator.of(context).pop(); // Close drawer
              context.go(HomeScreen.routeName);
            }},
          ),
          ListTile(
            leading: const Icon(Icons.star),
            title: const Text('{capitalized_name}'),
            onTap: () {{
              Navigator.of(context).pop(); // Close drawer
              context.go({class_name}.routeName);
            }},
          ),
        ],
      ),
    );
  }}
}}
"""
        drawer_path.write_text(drawer_content)

def update_router_for_drawer_item(project_dir, drawer_item_name):
    """Update router to include the drawer item route if needed"""
    router_path = project_dir / "lib" / "router.dart"
    
    if not router_path.exists():
        click.echo("⚠️ router.dart not found, skipping router update")
        return
    
    content = router_path.read_text()
    
    # Check if route already exists
    route_pattern = f"path: '/{drawer_item_name}'"
    if route_pattern in content:
        click.echo("ℹ️ Route already exists in router")
        return
    
    # Add route for the drawer item
    route_line = f"""GoRoute(
      path: '/{drawer_item_name}',
      builder: (BuildContext context, GoRouterState state) => const Placeholder(),
    ),"""
    
    if route_line not in content:
        # Find routes list and add the new route before the closing bracket
        if 'routes: <RouteBase>[' in content:
            content = content.replace('  ],', f'    {route_line}\n  ],')
        elif 'routes: [' in content:
            content = content.replace('  ],', f'    {route_line}\n  ],')
        else:
            click.echo("⚠️ Could not find routes list in router.dart")
    
    router_path.write_text(content)

def create_bottom_nav_page(project_dir, bottom_nav_item_name):
    """Create a screen for the bottom nav item in home/presentation"""
    home_presentation_dir = project_dir / "lib" / "home" / "presentation"
    home_presentation_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate screen file (not a full page with route)
    screen_content = f"""import 'package:flutter/material.dart';

class {bottom_nav_item_name.capitalize()}Screen extends StatelessWidget {{
  const {bottom_nav_item_name.capitalize()}Screen({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return const Center(
      child: Text('{bottom_nav_item_name.replace("_", " ").capitalize()} Page'),
    );
  }}
}}
"""
    screen_path = home_presentation_dir / f"{bottom_nav_item_name}_screen.dart"
    screen_path.write_text(screen_content)

def update_home_screen_with_bottom_nav(project_dir, bottom_nav_item_name):
    """Update the home screen to include bottom navigation"""
    home_screen_path = project_dir / "lib" / "home" / "presentation" / "home_screen.dart"
    
    if not home_screen_path.exists():
        click.echo("⚠️ Home screen not found, creating basic bottom nav implementation")
        return
    
    content = home_screen_path.read_text()
    
    # Check if bottom navigation is already implemented
    if "BottomNavigationBar" in content or "BottomNavBar" in content:
        # Update existing bottom navigation - add new screen to the list
        project_name = project_dir.name
        class_name = bottom_nav_item_name.capitalize() + 'Screen'
        
        # Add import for the new screen
        screen_import = f"import 'package:{project_name}/home/presentation/{bottom_nav_item_name}_screen.dart';"
        if screen_import not in content:
            # Add import after existing imports
            lines = content.split('\n')
            insert_index = 0
            for i, line in enumerate(lines):
                if line.startswith('import'):
                    insert_index = i + 1
                elif line.strip() and not line.startswith('//'):
                    break
            
            lines.insert(insert_index, screen_import)
            content = '\n'.join(lines)
        
        # Find the _pages list and add the new page
        lines = content.split('\n')
        pages_list_start = -1
        for i, line in enumerate(lines):
            if 'final List<Widget> _pages = [' in line or '_pages = [' in line:
                pages_list_start = i
                break
        
        if pages_list_start != -1:
            # Find the closing bracket of the _pages list
            bracket_count = 0
            for j in range(pages_list_start, len(lines)):
                bracket_count += lines[j].count('[')
                bracket_count -= lines[j].count(']')
                if bracket_count == 0 and '];' in lines[j]:
                    # Insert the new page before the closing bracket
                    lines.insert(j, f'    const {class_name}(),')
                    break
            
            content = '\n'.join(lines)
    else:
        # Create new home screen with bottom navigation
        project_name = project_dir.name
        capitalized_name = bottom_nav_item_name.replace('_', ' ').title()
        class_name = bottom_nav_item_name.capitalize() + 'Screen'
        
        # Check if drawer exists in current home screen
        existing_content = home_screen_path.read_text()
        has_drawer = "drawer:" in existing_content
        drawer_import_needed = "import 'package:" + project_name + "/core/presentation/app_drawer.dart';" in existing_content
        
        # Build imports
        imports = f"""import 'package:flutter/material.dart';
import 'package:{project_name}/core/presentation/bottom_nav_bar.dart';
import 'package:{project_name}/home/presentation/{bottom_nav_item_name}_screen.dart';"""
        
        if drawer_import_needed:
            imports += f"\nimport 'package:{project_name}/core/presentation/app_drawer.dart';"
        
        # Build drawer line if needed
        drawer_line = ""
        if has_drawer:
            drawer_line = "      drawer: const AppDrawer(),"
        
        content = f"""{imports}

class HomeScreen extends StatefulWidget {{
  static const String routeName = '/home';

  const HomeScreen({{super.key}});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}}

class _HomeScreenState extends State<HomeScreen> {{
  int _selectedIndex = 0;
  
  final List<Widget> _pages = [
    const Center(child: Text('Home Content')),
    const {class_name}(),
  ];
  
  void _onItemTapped(int index) {{
    setState(() {{
      _selectedIndex = index;
    }});
  }}

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(
        title: const Text('Home'),
      ),
{drawer_line}
      body: _pages[_selectedIndex],
      bottomNavigationBar: BottomNavBar(
        currentIndex: _selectedIndex,
        onTap: _onItemTapped,
      ),
    );
  }}
}}
"""
    
    home_screen_path.write_text(content)

def create_bottom_nav_widget(project_dir, bottom_nav_item_name):
    """Create or update the bottom navigation widget"""
    core_presentation_dir = project_dir / "lib" / "core" / "presentation"
    core_presentation_dir.mkdir(parents=True, exist_ok=True)
    
    bottom_nav_path = core_presentation_dir / "bottom_nav_bar.dart"
    
    if bottom_nav_path.exists():
        # Update existing bottom navigation - add new item
        content = bottom_nav_path.read_text()
        
        # Add new bottom nav item to the list - replace the closing bracket of items list
        if f"'{bottom_nav_item_name}'" not in content:
            capitalized_name = bottom_nav_item_name.replace('_', ' ').title()
            new_item = f"""        BottomNavigationBarItem(
          icon: const Icon(Icons.star),
          label: '{capitalized_name}',
        ),"""
            
            # Replace the closing bracket of the items list with the new item + closing bracket
            content = content.replace('      ],', f'        {new_item}\n      ],')
        
        bottom_nav_path.write_text(content)
    else:
        # Create new bottom navigation widget
        capitalized_name = bottom_nav_item_name.replace('_', ' ').title()
        
        bottom_nav_content = f"""import 'package:flutter/material.dart';

class BottomNavBar extends StatelessWidget {{
  final int currentIndex;
  final Function(int) onTap;

  const BottomNavBar({{
    super.key,
    required this.currentIndex,
    required this.onTap,
  }});

  @override
  Widget build(BuildContext context) {{
    return BottomNavigationBar(
      currentIndex: currentIndex,
      onTap: onTap,
      items: const [
        BottomNavigationBarItem(
          icon: Icon(Icons.home),
          label: 'Home',
        ),
        BottomNavigationBarItem(
          icon: Icon(Icons.star),
          label: '{capitalized_name}',
        ),
      ],
    );
  }}
}}
"""
        bottom_nav_path.write_text(bottom_nav_content)
