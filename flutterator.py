#!/usr/bin/env python3
"""
Flutterator - CLI to create and manage Flutter projects with custom structure

Created by Lorenzo Busi @ GetAutomation
"""

import click
import sys
from pathlib import Path
import subprocess

from generators import init
from generators.helpers import (
    get_project_name,
    validate_flutter_project,
    generate_page_file,
    update_router,
    create_feature_layers,
    create_drawer_page,
    update_home_screen_with_drawer,
    create_drawer_widget,
    create_bottom_nav_page,
    update_home_screen_with_bottom_nav,
    create_bottom_nav_widget,
    create_component_layers,
    create_component_form_layers,
)


def run_flutter_commands(project_path: Path) -> None:
    """Run flutter pub get and build_runner build after project modifications"""
    try:
        click.echo("📦 Running flutter pub get...")
        subprocess.run(["flutter", "pub", "get"], cwd=project_path, check=True, capture_output=True)
        
        # Check if build_runner is available before running it
        try:
            click.echo("🔨 Running build_runner build...")
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
    lib_path, project_name = validate_flutter_project(project_dir)
    
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
    generate_page_file(page_name, presentation_dir, project_name)
    
    # Update router
    update_router(project_dir, page_name, project_name)
    
    # Run flutter commands after project creation
    run_flutter_commands(project_dir)


@cli.command()
@click.option('--name', prompt='Feature name', help='Name of the feature to add')
@click.option('--folder', help='Folder to create the feature in (default: lib/feature_name)')
@click.option('--fields', help='Model fields in format: field1:type,field2:type (e.g., title:string,done:bool)')
@click.option('--project-path', default='.', help='Path to the Flutter project (default: current directory)')
def add_feature(name, folder, fields, project_path):
    """
    Add a complete feature to an existing Flutter project
    """
    project_dir = Path(project_path)
    lib_path, project_name = validate_flutter_project(project_dir)
    
    # Convert name to appropriate format
    feature_name = name.lower().replace(' ', '_')

    # Interactive folder
    if not folder:
        folder = click.prompt("Folder (leave empty for root)", default="")
    
    # Parse fields
    field_list = []
    if not fields:
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
    
    if folder:
        click.echo(f"📁 Component will be placed in folder: {folder}")
    
    # Create component directory structure
    if folder:
        # Create nested folder structure
        folder_path = lib_path
        for folder_part in folder.split('/'):
            folder_path = folder_path / folder_part
        feature_dir = folder_path / feature_name
    else:
        feature_dir = lib_path / feature_name

    # Create feature directory structure
    feature_dir.mkdir(exist_ok=True)
    
    # Create all layers
    create_feature_layers(feature_dir, feature_name, field_list, project_name, folder)
    
    # Update router
    update_router(project_dir, feature_name, project_name, folder)
    
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
    lib_path, project_name = validate_flutter_project(project_dir)
    
    # Convert name to appropriate format
    drawer_item_name = name.lower().replace(' ', '_')
    
    click.echo(f"📱 Adding drawer item: {drawer_item_name}")
    
    # Check if home screen exists
    home_presentation_dir = lib_path / "home" / "presentation"
    if not home_presentation_dir.exists():
        click.echo("❌ Home presentation directory not found. Make sure this is a Flutterator project.")
        sys.exit(1)
    
    # Create page for the drawer item
    create_drawer_page(project_dir, drawer_item_name, project_name)
    
    # Update home screen to include drawer
    update_home_screen_with_drawer(project_dir, project_name)
    
    # Create drawer widget if it doesn't exist
    create_drawer_widget(project_dir, drawer_item_name, project_name)
    
    click.echo(f"✅ Drawer item '{drawer_item_name}' added successfully!")


@cli.command()
@click.option('--name', prompt='Bottom nav item name', help='Name of the bottom navigation item to add')
@click.option('--project-path', default='.', help='Path to the Flutter project (default: current directory)')
def add_bottom_nav_item(name, project_path):
    """
    Add a bottom navigation item to an existing Flutter project
    """
    project_dir = Path(project_path)
    lib_path, project_name = validate_flutter_project(project_dir)
    
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
    update_home_screen_with_bottom_nav(project_dir, bottom_nav_item_name, project_name)
    
    # Create bottom navigation widget if it doesn't exist
    create_bottom_nav_widget(project_dir, bottom_nav_item_name)
    
    # Run Flutter commands to update dependencies and generate code
    run_flutter_commands(project_dir)
    
    click.echo(f"✅ Bottom nav item '{bottom_nav_item_name}' added successfully!")


@cli.command()
@click.option('--name', help='Name of the component to add')
@click.option('--fields', help='Model fields in format: field1:type,field2:type (e.g., title:string,done:bool)')
@click.option('--form', is_flag=True, default=None, help='Create a form component with form-specific BLoC state and events')
@click.option('--folder', help='Folder where to place the component (e.g., "forms", "shared", "features/auth")')
@click.option('--project-path', default='.', help='Path to the Flutter project (default: current directory)')
def add_component(name, fields, form, folder, project_path):
    """
    Add a complete component to an existing Flutter project
    """
    project_dir = Path(project_path)
    lib_path, project_name = validate_flutter_project(project_dir)

    if form is False and fields is not None:
        click.echo("❌ The --fields option can only be used with --form to create a form component.")
        sys.exit(1)
    
    # Interactive mode - always ask for missing parameters
    if not name:
        name = click.prompt("Component name")
    
    component_name = name.lower().replace(' ', '_')

    # Interactive folder
    if not folder:
        folder = click.prompt("Folder (leave empty for root)", default="")
    
    # Interactive form flag - use parameter if provided via CLI, otherwise ask
    if form is not None:
        is_form = form
    else:
        is_form = click.confirm("Is this a form component?", default=False)
    
    if is_form:
        # Interactive fields
        if not fields:
            click.echo("🔧 Adding fields interactively. Type 'done' when finished.")
            field_list = []
            while True:
                field_name = click.prompt("Field name (or 'done')")
                if field_name.lower() == 'done':
                    break
                field_type = click.prompt("Field type", default='String')
                field_list.append(f"{field_name.strip()}:{field_type.strip()}")
            fields = ','.join(field_list)
    
        # Parse fields
        field_list = []
        for field in fields.split(','):
            field_name, field_type = field.split(':')
            field_list.append({'name': field_name.strip(), 'type': field_type.strip()})

        if not field_list:
            click.echo("❌ No fields specified.")
            sys.exit(1)

        click.echo(f"🔧 Adding component: {component_name} with fields: {', '.join([f'{f['name']}:{f['type']}' for f in field_list])}")
        click.echo("📝 Component will be created as a form component")

    
    if folder:
        click.echo(f"📁 Component will be placed in folder: {folder}")
    
    # Create component directory structure
    if folder:
        # Create nested folder structure
        folder_path = lib_path
        for folder_part in folder.split('/'):
            folder_path = folder_path / folder_part
        component_dir = folder_path / component_name
    else:
        component_dir = lib_path / component_name
    
    component_dir.mkdir(parents=True, exist_ok=True)
    
    if not is_form:
        # Create all layers
        create_component_layers(component_dir, component_name, project_name, folder)
    else:
        # Create all layers
        create_component_form_layers(component_dir, component_name, field_list, project_name, folder)

    # Run Flutter commands to update dependencies and generate code
    run_flutter_commands(project_dir)
    
    click.echo(f"✅ Component '{component_name}' added successfully!")
