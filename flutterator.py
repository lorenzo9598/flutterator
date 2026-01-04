#!/usr/bin/env python3
"""
Flutterator - CLI to create and manage Flutter projects with custom structure

Created by Lorenzo Busi @ GetAutomation
"""

import click
import sys
from pathlib import Path
import subprocess
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree
from rich.text import Text
from rich import print as rprint

from generators import init
from generators.helpers import (
    get_project_name,
    validate_flutter_project,
    generate_page_file,
    update_router,
    create_feature_layers,
    create_presentation_feature_layers,
    create_domain_entity_layers,
    find_domain_models,
    get_model_fields_from_domain,
    create_drawer_page,
    update_home_screen_with_drawer,
    create_drawer_widget,
    create_bottom_nav_page,
    update_home_screen_with_bottom_nav,
    create_bottom_nav_widget,
    create_component_layers,
    create_component_form_layers,
    create_component_list_layers,
    # Configuration
    FlutteratorConfig,
    load_config,
    apply_cli_overrides,
    create_default_config,
    show_config,
    PROJECT_CONFIG_FILE,
)

# Rich console for colored output
console = Console()


def print_success(message: str) -> None:
    """Print success message in green"""
    console.print(f"[bold green]✅ {message}[/bold green]")


def print_error(message: str) -> None:
    """Print error message in red"""
    console.print(f"[bold red]❌ {message}[/bold red]")


def print_warning(message: str) -> None:
    """Print warning message in yellow"""
    console.print(f"[bold yellow]⚠️  {message}[/bold yellow]")


def print_info(message: str) -> None:
    """Print info message in blue"""
    console.print(f"[bold blue]ℹ️  {message}[/bold blue]")


def print_step(message: str) -> None:
    """Print step message"""
    console.print(f"[cyan]→ {message}[/cyan]")


def print_dry_run_header() -> None:
    """Print dry-run mode header with rich panel"""
    console.print()
    console.print(Panel.fit(
        "[bold yellow]🔍 DRY-RUN MODE[/bold yellow]\n[dim]No files will be created[/dim]",
        border_style="yellow"
    ))
    console.print()


def print_dry_run_tree(base_path: str, structure: list[tuple[str, list[str]]]) -> None:
    """Print a tree structure for dry-run output using rich Tree"""
    tree = Tree(f"[bold blue]📁 {base_path}/[/bold blue]")
    
    for folder, files in structure:
        folder_branch = tree.add(f"[blue]📁 {folder}/[/blue]")
        for file in files:
            folder_branch.add(f"[green]📄 {file}[/green]")
    
    console.print(tree)


def print_dry_run_footer() -> None:
    """Print dry-run mode footer"""
    console.print()
    console.print("[dim]─" * 50 + "[/dim]")
    print_info("Run without --dry-run to create these files")
    console.print()


def print_created_structure(name: str, structure: list[tuple[str, list[str]]], updated_files: list[str] = None) -> None:
    """Print the structure of created files"""
    tree = Tree(f"[bold green]📦 Created: {name}[/bold green]")
    
    for folder, files in structure:
        folder_branch = tree.add(f"[blue]📁 {folder}/[/blue]")
        for file in files:
            folder_branch.add(f"[green]✅ {file}[/green]")
    
    console.print(tree)
    
    if updated_files:
        console.print()
        console.print("[bold]📝 Updated files:[/bold]")
        for file in updated_files:
            console.print(f"   [cyan]→ {file}[/cyan]")


def run_flutter_commands(project_path: Path) -> None:
    """Run flutter pub get and build_runner build after project modifications"""
    try:
        print_step("Running flutter pub get...")
        subprocess.run(["flutter", "pub", "get"], cwd=project_path, check=True, capture_output=True)
        
        # Check if build_runner is available before running it
        try:
            print_step("Running build_runner build...")
            subprocess.run(["dart", "run", "build_runner", "build"], cwd=project_path, check=True, capture_output=True)
        except subprocess.CalledProcessError:
            print_warning("build_runner not available or failed. You may need to add it as a dev dependency.")
        
        print_success("Dependencies updated!")
    except subprocess.CalledProcessError as e:
        print_warning(f"Could not run flutter commands: {e}")
        print_info("You may need to run 'flutter pub get' manually.")


@click.group()
def cli():
    """
    🚀 Flutterator - CLI to create and manage Flutter projects with DDD architecture.
    
    \b
    Quick Start:
      flutterator create --name my_app
      cd my_app
      flutterator add-domain --name todo --fields "title:string,done:bool"
      flutterator add-component --name todo_list --type list
    
    \b
    Available Commands:
      create              Create a new Flutter project
      add-page            Add a simple page
      add-domain          Add a domain entity (model + infrastructure only)
      add-component       Add a reusable component (form, list, or single)
      add-drawer-item     Add drawer navigation item
      add-bottom-nav-item Add bottom navigation item
      config              Manage configuration
    
    \b
    Tips:
      • Use --dry-run to preview changes before creating files
      • Use --no-build to skip flutter pub get
      • Create flutterator.yaml for project-specific defaults
    
    Created by Lorenzo Busi @ GetAutomation
    """
    pass


@cli.command()
@click.option('--project-path', default='.', help='Path to the Flutter project (default: current directory)')
@click.option('--init', 'init_config', is_flag=True, help='Create a new flutterator.yaml config file')
@click.option('--show', is_flag=True, help='Show current configuration')
def config(project_path, init_config, show):
    """
    Manage Flutterator configuration.
    
    Configuration is loaded from (highest to lowest priority):
    1. CLI flags
    2. Project flutterator.yaml
    3. Global ~/.flutteratorrc
    4. Built-in defaults
    
    Examples:
    
      flutterator config --show
      
      flutterator config --init
    """
    project_dir = Path(project_path)
    
    if init_config:
        # Check if pubspec.yaml exists (it's a Flutter project)
        if not (project_dir / "pubspec.yaml").exists():
            print_error("Not a Flutter project. pubspec.yaml not found.")
            print_info("Run this command from a Flutter project directory.")
            sys.exit(1)
        
        config_path = project_dir / PROJECT_CONFIG_FILE
        if config_path.exists():
            if not click.confirm(f"⚠️  {PROJECT_CONFIG_FILE} already exists. Overwrite?"):
                print_info("Aborted.")
                return
        
        project_name = get_project_name(project_dir)
        create_default_config(project_dir, project_name)
        print_success(f"Created {PROJECT_CONFIG_FILE}")
        console.print(f"   [dim]Edit this file to customize Flutterator behavior[/dim]")
        return
    
    if show or (not init_config and not show):
        # Show current configuration
        cfg = load_config(project_dir if (project_dir / "pubspec.yaml").exists() else None)
        show_config(cfg)
        
        # Show where config was loaded from
        console.print()
        config_file = project_dir / PROJECT_CONFIG_FILE
        if config_file.exists():
            console.print(f"[dim]📄 Project config: {config_file}[/dim]")
        else:
            console.print(f"[dim]📄 No project config found. Run 'flutterator config --init' to create one.[/dim]")


@cli.command()
@click.option('--name', prompt='Project name', help='Project name (lowercase, underscores allowed)')
@click.option('--login', is_flag=True, prompt='Does the project have login?', help='Include login/auth functionality')
def create(name, login):
    """
    Create a new Flutter project with DDD architecture.
    
    \b
    Creates a complete project structure with:
      • Core layer (app widget, router, injection)
      • Home screen with scaffold
      • BLoC pattern ready
      • Injectable setup
    
    \b
    Examples:
      # Basic project
      flutterator create --name my_app
    
      # Project with authentication
      flutterator create --name my_app --login
    
      # Non-interactive mode
      flutterator create --name my_app --no-login
    """
    # Project name validation
    if not name.replace('_', '').replace('-', '').isalnum():
        print_error("The project name must contain only letters, numbers, _ and -")
        sys.exit(1)

    # Convert name for Flutter (lowercase with underscore)
    flutter_name = name.lower().replace('-', '_')
    
    console.print(Panel.fit(
        f"[bold cyan]🚀 Creating project: {flutter_name}[/bold cyan]",
        border_style="cyan"
    ))

    init(flutter_name, login)
    
    # Run flutter commands after project creation
    run_flutter_commands(Path(flutter_name))
    
    console.print()
    print_success(f"Project '{flutter_name}' created successfully!")
    console.print()
    console.print("[bold]Next steps:[/bold]")
    console.print(f"   [cyan]cd {flutter_name}[/cyan]")
    console.print(f"   [cyan]flutter run[/cyan]")


@cli.command()
@click.option('--name', prompt='Page name', help='Page name (e.g., profile, settings, about)')
@click.option('--project-path', default='.', help='Path to Flutter project')
@click.option('--dry-run', is_flag=True, help='Preview without creating files')
@click.option('--no-build', is_flag=True, help='Skip flutter pub get')
def add_page(name, project_path, dry_run, no_build):
    """
    Add a simple page to an existing Flutter project.
    
    \b
    Creates:
      • lib/features/<name>/presentation/<name>_page.dart
      • Updates lib/router.dart with new route
    
    \b
    Use this for simple pages without business logic.
    For pages with state management, use add-component --type list instead.
    
    \b
    Examples:
      # Add a profile page
      flutterator add-page --name profile
      
      # Preview what will be created
      flutterator add-page --name settings --dry-run
      
      # Skip flutter pub get
      flutterator add-page --name about --no-build
    """
    project_dir = Path(project_path)
    lib_path, project_name = validate_flutter_project(project_dir)
    
    # Load configuration
    cfg = load_config(project_dir)
    
    # Convert name to appropriate format
    page_name = name.lower().replace(' ', '_')
    
    # Dry-run mode: show what would be created
    if dry_run:
        print_dry_run_header()
        console.print(f"[bold]📄 Would add page:[/bold] [cyan]{page_name}[/cyan]")
        console.print()
        print_dry_run_tree(f"lib/features/{page_name}", [
            ("presentation", [f"{page_name}_page.dart"])
        ])
        console.print()
        console.print("[bold]📝 Would update:[/bold] [cyan]lib/router.dart[/cyan]")
        print_dry_run_footer()
        return
    
    console.print(f"[bold cyan]📄 Adding page: {page_name}[/bold cyan]")
    
    # Create page directory structure inside features folder
    features_dir = lib_path / "features"
    features_dir.mkdir(exist_ok=True)
    page_dir = features_dir / page_name
    page_dir.mkdir(exist_ok=True)
    
    # Create presentation layer
    presentation_dir = page_dir / "presentation"
    presentation_dir.mkdir(exist_ok=True)
    
    # Generate page file
    generate_page_file(page_name, presentation_dir, project_name)
    
    # Update router with features folder
    update_router(project_dir, page_name, project_name, folder="features")
    
    # Show created structure
    print_created_structure(page_name, [
        ("presentation", [f"{page_name}_page.dart"])
    ], ["lib/router.dart"])
    
    # Run flutter commands (respecting --no-build and config)
    if not no_build and cfg.auto_run_build_runner:
        run_flutter_commands(project_dir)
    elif no_build:
        print_info("Skipping flutter pub get and build_runner (--no-build)")
    
    print_success(f"Page '{page_name}' added successfully!")


@cli.command()
@click.option('--name', help='Domain entity name (e.g., todo, user, product)')
@click.option('--fields', help='Fields as name:type,name:type (e.g., "title:string,done:bool,priority:int")')
@click.option('--folder', help='Domain folder (default from config)')
@click.option('--project-path', default='.', help='Path to Flutter project')
@click.option('--dry-run', is_flag=True, help='Preview without creating files')
@click.option('--no-build', is_flag=True, help='Skip flutter pub get')
def add_domain(name, fields, folder, project_path, dry_run, no_build):
    """
    Add a domain entity (model + infrastructure only).
    
    \b
    Creates:
      • lib/<domain_folder>/<name>/model/ - Entity, failure, repository interface
      • lib/<domain_folder>/<name>/infrastructure/ - DTO, service, mapper, repository
    
    \b
    Domain entities are shared business entities that can be used by multiple features.
    They do NOT include application or presentation layers.
    
    \b
    Examples:
      # Domain entity with fields
      flutterator add-domain --name todo --fields "title:string,done:bool,priority:int"
      
      # Interactive mode (will prompt for fields)
      flutterator add-domain --name user
      
      # Preview what will be created
      flutterator add-domain --name product --fields "name:string,price:double" --dry-run
      
      # Custom domain folder
      flutterator add-domain --name note --fields "title:string" --folder shared/domain
    """
    project_dir = Path(project_path)
    lib_path, project_name = validate_flutter_project(project_dir)
    
    # Load configuration
    cfg = load_config(project_dir)
    
    # Interactive mode - ask for missing parameters (skip if dry-run)
    if not name:
        if dry_run:
            print_error("--name is required with --dry-run")
            sys.exit(1)
        name = click.prompt("Domain entity name")
    
    entity_name = name.lower().replace(' ', '_')
    
    # Use folder from CLI or config
    if folder is None:
        folder = cfg.domain_folder if cfg.domain_folder else "domain"
    
    # Parse fields
    field_list = []
    if fields:
        # Parse fields from string: "name:type,name:type"
        for field_str in fields.split(','):
            field_str = field_str.strip()
            if ':' not in field_str:
                print_error(f"Invalid field format: {field_str}. Expected format: name:type")
                sys.exit(1)
            field_name, field_type = field_str.split(':', 1)
            field_list.append({"name": field_name.strip(), "type": field_type.strip()})
    elif not dry_run:
        # Interactive mode for fields
        console.print("[bold cyan]Adding fields interactively. Type 'done' when finished.[/bold cyan]")
        while True:
            field_name = click.prompt("Field name (or 'done')", default="done")
            if field_name.lower() == 'done':
                break
            field_type = click.prompt("Field type", default="string", type=click.Choice(['string', 'int', 'double', 'bool', 'datetime', 'list', 'map'], case_sensitive=False))
            field_list.append({"name": field_name.strip(), "type": field_type.strip()})
    
    # Ensure id field exists (add if not present)
    has_id = any(field['name'] == 'id' for field in field_list)
    if not has_id:
        field_list.insert(0, {"name": "id", "type": "string"})
    
    # Build base path for display
    base_path = f"lib/{folder}/{entity_name}"
    
    # Dry-run mode: show what would be created
    if dry_run:
        print_dry_run_header()
        console.print(f"[bold]📦 Would add domain entity:[/bold] [cyan]{entity_name}[/cyan]")
        console.print(f"   [dim]Domain folder:[/dim] [blue]{folder}[/blue]")
        if field_list:
            fields_str = ', '.join([f"[green]{field['name']}[/green]:[magenta]{field['type']}[/magenta]" for field in field_list])
            console.print(f"   [dim]Fields:[/dim] {fields_str}")
        console.print()
        
        print_dry_run_tree(base_path, [
            ("model", [
                f"{entity_name}.dart",
                f"{entity_name}_failure.dart",
                f"i_{entity_name}_repository.dart",
                "value_objects.dart",
                "value_validators.dart"
            ]),
            ("infrastructure", [
                f"{entity_name}_dto.dart",
                f"{entity_name}_service.dart",
                f"{entity_name}_mapper.dart",
                f"{entity_name}_repository.dart"
            ])
        ])
        print_dry_run_footer()
        return
    
    console.print(f"[bold cyan]📦 Adding domain entity: {entity_name}[/bold cyan]")
    console.print(f"   [dim]Domain folder:[/dim] [blue]{folder}[/blue]")
    if field_list:
        fields_str = ', '.join([f"[green]{field['name']}[/green]:[magenta]{field['type']}[/magenta]" for field in field_list])
        console.print(f"   [dim]Fields:[/dim] {fields_str}")
    
    # Create domain directory structure
    domain_dir = lib_path / folder / entity_name
    domain_dir.mkdir(parents=True, exist_ok=True)
    
    # Create domain entity layers (model + infrastructure only)
    create_domain_entity_layers(domain_dir, entity_name, field_list, project_name, folder)
    
    # Show created structure
    print_created_structure(entity_name, [
        ("model", [
            f"{entity_name}.dart",
            f"{entity_name}_failure.dart",
            f"i_{entity_name}_repository.dart",
            "value_objects.dart",
            "value_validators.dart"
        ]),
        ("infrastructure", [
            f"{entity_name}_dto.dart",
            f"{entity_name}_service.dart",
            f"{entity_name}_mapper.dart",
            f"{entity_name}_repository.dart"
        ])
    ])
    
    # Run Flutter commands (respecting --no-build and config)
    if not no_build and cfg.auto_run_build_runner:
        run_flutter_commands(project_dir)
    elif no_build:
        print_info("Skipping flutter pub get and build_runner (--no-build)")
    
    print_success(f"Domain entity '{entity_name}' added successfully!")


# @cli.command()  # Disabled - use add-domain + add-component --type list instead
def add_feature(name=None, folder=None, fields=None, project_path='.', dry_run=False, no_build=False, domain=False, presentation=False):
    """
    [DEPRECATED] This command has been removed.
    
    Use the following instead:
    - For domain entities: `flutterator add-domain --name <model_name>`
    - For list components: `flutterator add-component --name <name> --type list`
    - For single components: `flutterator add-component --name <name> --type single`
    - For form components: `flutterator add-component --name <name> --type form`
    
    This function is kept for backward compatibility only.
    """
    # Early exit with error message
    print_error("The 'add-feature' command has been removed.")
    print_error("Use 'flutterator add-domain --name <model_name>' to create domain entities.")
    print_error("Use 'flutterator add-component --name <name> --type list' to create list components.")
    print_error("Use 'flutterator add-component --name <name> --type single' to create single item components.")
    print_error("Use 'flutterator add-component --name <name> --type form' to create form components.")
    sys.exit(1)


@cli.command()
@click.option('--name', prompt='Drawer item name', help='Item name (e.g., settings, profile)')
@click.option('--project-path', default='.', help='Path to Flutter project')
@click.option('--dry-run', is_flag=True, help='Preview without creating files')
@click.option('--no-build', is_flag=True, help='Skip flutter pub get')
def add_drawer_item(name, project_path, dry_run, no_build):
    """
    Add a drawer navigation item to the home screen.
    
    \b
    Creates/Updates:
      • lib/<name>/presentation/<name>_page.dart
      • lib/core/presentation/app_drawer.dart
      • lib/home/presentation/home_screen.dart (adds drawer)
      • lib/router.dart (new route)
    
    \b
    Examples:
      # Add settings drawer item
      flutterator add-drawer-item --name settings
    
      # Add profile with preview
      flutterator add-drawer-item --name profile --dry-run
    
    \b
    Note: Creates drawer widget on first use, adds items on subsequent calls.
    """
    project_dir = Path(project_path)
    lib_path, project_name = validate_flutter_project(project_dir)
    
    # Convert name to appropriate format
    drawer_item_name = name.lower().replace(' ', '_')
    
    # Dry-run mode: show what would be created
    if dry_run:
        print_dry_run_header()
        console.print(f"[bold]📱 Would add drawer item:[/bold] [cyan]{drawer_item_name}[/cyan]")
        console.print()
        print_dry_run_tree(f"lib/{drawer_item_name}", [
            ("presentation", [f"{drawer_item_name}_page.dart"])
        ])
        console.print()
        console.print("[bold]📝 Would update/create:[/bold]")
        console.print("   [cyan]├── lib/router.dart[/cyan]")
        console.print("   [cyan]├── lib/home/presentation/home_screen.dart[/cyan]")
        console.print("   [cyan]└── lib/core/presentation/app_drawer.dart[/cyan]")
        print_dry_run_footer()
        return
    
    console.print(f"[bold cyan]📱 Adding drawer item: {drawer_item_name}[/bold cyan]")
    
    # Check if home screen exists
    home_presentation_dir = lib_path / "home" / "presentation"
    if not home_presentation_dir.exists():
        print_error("Home presentation directory not found. Make sure this is a Flutterator project.")
        sys.exit(1)
    
    # Create page for the drawer item
    create_drawer_page(project_dir, drawer_item_name, project_name)
    
    # Update home screen to include drawer
    update_home_screen_with_drawer(project_dir, project_name)
    
    # Create drawer widget if it doesn't exist
    create_drawer_widget(project_dir, drawer_item_name, project_name)
    
    print_created_structure(drawer_item_name, [
        ("presentation", [f"{drawer_item_name}_page.dart"])
    ], ["lib/router.dart", "lib/home/presentation/home_screen.dart", "lib/core/presentation/app_drawer.dart"])
    
    print_success(f"Drawer item '{drawer_item_name}' added successfully!")


@cli.command()
@click.option('--name', prompt='Bottom nav item name', help='Tab name (e.g., search, favorites)')
@click.option('--project-path', default='.', help='Path to Flutter project')
@click.option('--dry-run', is_flag=True, help='Preview without creating files')
@click.option('--no-build', is_flag=True, help='Skip flutter pub get')
def add_bottom_nav_item(name, project_path, dry_run, no_build):
    """
    Add a bottom navigation tab to the home screen.
    
    \b
    Creates/Updates:
      • lib/home/presentation/<name>_screen.dart
      • lib/core/presentation/bottom_nav_bar.dart
      • lib/home/presentation/home_screen.dart (adds bottom nav)
    
    \b
    Examples:
      # Add search tab
      flutterator add-bottom-nav-item --name search
    
      # Add favorites tab with preview
      flutterator add-bottom-nav-item --name favorites --dry-run
    
    \b
    Note: Creates bottom navigation on first use, adds tabs on subsequent calls.
    """
    project_dir = Path(project_path)
    lib_path, project_name = validate_flutter_project(project_dir)
    
    # Load configuration
    cfg = load_config(project_dir)
    
    # Convert name to appropriate format
    bottom_nav_item_name = name.lower().replace(' ', '_')
    
    # Dry-run mode: show what would be created
    if dry_run:
        print_dry_run_header()
        console.print(f"[bold]📱 Would add bottom nav item:[/bold] [cyan]{bottom_nav_item_name}[/cyan]")
        console.print()
        tree = Tree(f"[bold blue]📁 lib/home/presentation/[/bold blue]")
        tree.add(f"[green]📄 {bottom_nav_item_name}_screen.dart[/green]")
        console.print(tree)
        console.print()
        console.print("[bold]📝 Would update/create:[/bold]")
        console.print("   [cyan]├── lib/home/presentation/home_screen.dart[/cyan]")
        console.print("   [cyan]└── lib/core/presentation/bottom_nav_bar.dart[/cyan]")
        print_dry_run_footer()
        return
    
    console.print(f"[bold cyan]📱 Adding bottom nav item: {bottom_nav_item_name}[/bold cyan]")
    
    # Check if home screen exists
    home_presentation_dir = lib_path / "home" / "presentation"
    if not home_presentation_dir.exists():
        print_error("Home presentation directory not found. Make sure this is a Flutterator project.")
        sys.exit(1)
    
    # Create page for the bottom nav item
    create_bottom_nav_page(project_dir, bottom_nav_item_name)
    
    # Update home screen to include bottom navigation
    update_home_screen_with_bottom_nav(project_dir, bottom_nav_item_name, project_name)
    
    # Create bottom navigation widget if it doesn't exist
    create_bottom_nav_widget(project_dir, bottom_nav_item_name)
    
    # Run Flutter commands (respecting --no-build and config)
    if not no_build and cfg.auto_run_build_runner:
        run_flutter_commands(project_dir)
    elif no_build:
        print_info("Skipping flutter pub get and build_runner (--no-build)")
    
    console.print()
    console.print("[bold]📝 Updated files:[/bold]")
    console.print("   [cyan]→ lib/home/presentation/home_screen.dart[/cyan]")
    console.print("   [cyan]→ lib/core/presentation/bottom_nav_bar.dart[/cyan]")
    console.print(f"   [green]✅ lib/home/presentation/{bottom_nav_item_name}_screen.dart[/green]")
    
    print_success(f"Bottom nav item '{bottom_nav_item_name}' added successfully!")


@cli.command()
@click.option('--name', help='Component name (e.g., user_card, login_form)')
@click.option('--fields', help='Form fields as name:type,name:type (only for form type)')
@click.option('--type', type=click.Choice(['form', 'list', 'single'], case_sensitive=False), help='Component type: form, list, or single')
@click.option('--folder', help='Target folder (e.g., components, shared)')
@click.option('--project-path', default='.', help='Path to Flutter project')
@click.option('--dry-run', is_flag=True, help='Preview without creating files')
@click.option('--no-build', is_flag=True, help='Skip flutter pub get')
def add_component(name, fields, type, folder, project_path, dry_run, no_build):
    """
    Add a reusable component with optional BLoC.
    
    \b
    Three types available:
    
    SINGLE COMPONENT (--type single or default):
      Creates a component that displays a single item loaded by ID.
      • application/  - BLoC, events, states
      • presentation/ - Widget
    
    LIST COMPONENT (--type list):
      Creates a component that displays a list of items with full CRUD operations.
      • application/  - BLoC with getAll, create, update, delete
      • presentation/ - Widget with ListView
    
    FORM COMPONENT (--type form):
      Creates a form with field validation and submission handling.
      Requires --fields to define form inputs.
      • application/  - Form BLoC, events, states
      • presentation/ - Form widget
    
    \b
    Examples:
      # Single component (default)
      flutterator add-component --name user_card
      
      # List component
      flutterator add-component --name todo_list --type list
      
      # Form component with fields
      flutterator add-component --name login --type form \\
        --fields "email:string,password:string"
    
      # Component in specific folder
      flutterator add-component --name search_bar --folder shared/widgets
    
      # Preview component
      flutterator add-component --name register --type list --dry-run
    
    \b
    Configure default folder in flutterator.yaml:
      defaults:
        component_folder: "components"
    """
    project_dir = Path(project_path)
    lib_path, project_name = validate_flutter_project(project_dir)
    
    # Load configuration
    cfg = load_config(project_dir)

    # Validate fields option
    if fields is not None and type and type.lower() != 'form':
        print_error("The --fields option can only be used with --type form.")
        sys.exit(1)
    
    # Interactive mode - always ask for missing parameters (skip if dry-run)
    if not name:
        if dry_run:
            print_error("--name is required with --dry-run")
            sys.exit(1)
        name = click.prompt("Component name")
    
    component_name = name.lower().replace(' ', '_')

    # Use folder from CLI, config, or prompt
    if folder is None:
        if cfg.component_folder:
            folder = cfg.component_folder
        elif not dry_run:
            folder = click.prompt("Folder (leave empty for root)", default="")
    
    # Determine component type - use parameter if provided via CLI, otherwise ask interactively
    if type:
        component_type = type.lower()
    elif dry_run:
        component_type = 'single'  # Default to single component in dry-run
    else:
        console.print("[bold cyan]Select component type:[/bold cyan]")
        console.print("  1. Single item (loads one item by ID)")
        console.print("  2. List (shows all items with CRUD operations)")
        console.print("  3. Form (form with validation)")
        console.print()
        while True:
            choice = click.prompt("Type (1-3)", type=int)
            if choice == 1:
                component_type = 'single'
                break
            elif choice == 2:
                component_type = 'list'
                break
            elif choice == 3:
                component_type = 'form'
                break
            console.print("[red]Invalid choice. Please select 1, 2, or 3.[/red]")
    
    # Select domain model
    available_models = find_domain_models(lib_path, cfg.domain_folder)
    if not available_models:
        print_error(f"No domain models found in {cfg.domain_folder}/ folder.")
        print_error("Create a domain model first using: flutterator add-domain --name <model_name>")
        sys.exit(1)
    
    domain_model_name = None
    if not dry_run:
        console.print(f"[bold cyan]Available domain models:[/bold cyan]")
        for i, model in enumerate(available_models, 1):
            console.print(f"  {i}. {model}")
        console.print()
        
        while True:
            choice = click.prompt(f"Select domain model (1-{len(available_models)})", type=int)
            if 1 <= choice <= len(available_models):
                domain_model_name = available_models[choice - 1]
                break
            console.print("[red]Invalid choice. Please try again.[/red]")
    else:
        # Dry run: use first available model
        domain_model_name = available_models[0]
    
    # Build base path for display
    base_path = f"lib/{folder}/{component_name}" if folder else f"lib/{component_name}"
    
    # Get fields from domain model (for form components)
    field_list = []
    if component_type == 'form':
        try:
            field_list = get_model_fields_from_domain(lib_path, cfg.domain_folder, domain_model_name)
        except Exception as e:
            print_error(f"Error reading domain model: {e}")
            sys.exit(1)
    
    # Dry-run mode: show what would be created
    if dry_run:
        print_dry_run_header()
        console.print(f"[bold]🔧 Would add component:[/bold] [cyan]{component_name}[/cyan]")
        console.print(f"   [dim]Using domain model:[/dim] [blue]{domain_model_name}[/blue]")
        console.print(f"   [dim]Type:[/dim] [magenta]{component_type.capitalize()} component[/magenta]")
        if component_type == 'form' and field_list:
            fields_str = ', '.join([f"[green]{field['name']}[/green]:[magenta]{field['type']}[/magenta]" for field in field_list])
            console.print(f"   [dim]Fields:[/dim] {fields_str}")
        if folder:
            console.print(f"   [dim]Folder:[/dim] [blue]{folder}[/blue]")
        console.print()
        
        if component_type == 'form':
            print_dry_run_tree(base_path, [
                ("application", [
                    f"{component_name}_form_bloc.dart",
                    f"{component_name}_form_event.dart",
                    f"{component_name}_form_state.dart"
                ]),
                ("presentation", [
                    f"{component_name}_component.dart"
                ])
            ])
        elif component_type == 'list':
            print_dry_run_tree(base_path, [
                ("application", [
                    f"{component_name}_bloc.dart",
                    f"{component_name}_event.dart",
                    f"{component_name}_state.dart"
                ]),
                ("presentation", [
                    f"{component_name}_component.dart"
                ])
            ])
        else:  # single
            print_dry_run_tree(base_path, [
                ("application", [
                    f"{component_name}_bloc.dart",
                    f"{component_name}_event.dart",
                    f"{component_name}_state.dart"
                ]),
                ("presentation", [
                    f"{component_name}_component.dart"
                ])
            ])
        print_dry_run_footer()
        return
    
    console.print(f"[bold cyan]🔧 Adding {component_type} component: {component_name}[/bold cyan]")
    console.print(f"   [dim]Using domain model:[/dim] [blue]{domain_model_name}[/blue]")
    if component_type == 'form' and field_list:
        fields_str = ', '.join([f"[green]{field['name']}[/green]:[magenta]{field['type']}[/magenta]" for field in field_list])
        console.print(f"   [dim]Fields:[/dim] {fields_str}")
    
    if folder:
        console.print(f"   [dim]Folder:[/dim] [blue]{folder}[/blue]")
    
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
    
    if component_type == 'form':
        # Create all layers with domain model fields
        create_component_form_layers(component_dir, component_name, field_list, project_name, folder, domain_model_name, cfg.domain_folder)
        # Show created structure
        print_created_structure(component_name, [
            ("application", [f"{component_name}_form_bloc.dart", f"{component_name}_form_event.dart", f"{component_name}_form_state.dart"]),
            ("presentation", [f"{component_name}_component.dart"])
        ])
    elif component_type == 'list':
        # Create all layers with list functionality (CRUD operations)
        create_component_list_layers(component_dir, component_name, project_name, folder, domain_model_name, cfg.domain_folder)
        # Show created structure
        print_created_structure(component_name, [
            ("application", [f"{component_name}_bloc.dart", f"{component_name}_event.dart", f"{component_name}_state.dart"]),
            ("presentation", [f"{component_name}_component.dart"])
        ])
    else:  # single
        # Create all layers with domain model reference
        create_component_layers(component_dir, component_name, project_name, folder, domain_model_name, cfg.domain_folder)
        # Show created structure
        print_created_structure(component_name, [
            ("application", [f"{component_name}_bloc.dart", f"{component_name}_event.dart", f"{component_name}_state.dart"]),
            ("presentation", [f"{component_name}_component.dart"])
        ])

    # Run Flutter commands (respecting --no-build and config)
    if not no_build and cfg.auto_run_build_runner:
        run_flutter_commands(project_dir)
    elif no_build:
        print_info("Skipping flutter pub get and build_runner (--no-build)")
    
    print_success(f"Component '{component_name}' added successfully!")


@cli.command(name='list')
@click.argument('resource_type', required=False, default='all', 
                type=click.Choice(['all', 'features', 'pages', 'components', 'routes']))
@click.option('--project-path', default='.', help='Path to Flutter project')
def list_resources(resource_type, project_path):
    """
    List resources in the Flutter project.
    
    \b
    Resource Types:
      all        - Show everything (default)
      features   - DDD features with all layers
      pages      - Simple pages
      components - Reusable components
      routes     - Routes from router.dart
    
    \b
    Examples:
      # List all resources
      flutterator list
    
      # List only features
      flutterator list features
    
      # List routes
      flutterator list routes
    """
    project_dir = Path(project_path)
    lib_path, project_name = validate_flutter_project(project_dir)
    
    console.print(Panel.fit(
        f"[bold cyan]📋 Project: {project_name}[/bold cyan]",
        border_style="cyan"
    ))
    
    if resource_type in ['all', 'features']:
        _list_features(lib_path)
    
    if resource_type in ['all', 'pages']:
        _list_pages(lib_path)
    
    if resource_type in ['all', 'components']:
        _list_components(lib_path)
    
    if resource_type in ['all', 'routes']:
        _list_routes(project_dir, project_name)


def _list_features(lib_path: Path) -> None:
    """List all features in the project."""
    features = []
    
    # A feature has model/, infrastructure/, application/, presentation/ subdirs
    for item in lib_path.iterdir():
        if item.is_dir():
            subdirs = {d.name for d in item.iterdir() if d.is_dir()}
            # Check if it looks like a DDD feature
            if {'model', 'application'}.issubset(subdirs) or \
               {'model', 'infrastructure', 'application', 'presentation'}.issubset(subdirs):
                features.append(item)
    
    if features:
        console.print()
        console.print("[bold blue]📦 Features:[/bold blue]")
        for feature in sorted(features, key=lambda x: x.name):
            feature_tree = Tree(f"[cyan]{feature.name}/[/cyan]")
            
            # List layers
            for layer in ['model', 'infrastructure', 'application', 'presentation']:
                layer_path = feature / layer
                if layer_path.exists():
                    files = [f.stem for f in layer_path.glob("*.dart")]
                    if files:
                        layer_branch = feature_tree.add(f"[dim]{layer}/[/dim]")
                        for f in sorted(files)[:3]:  # Show max 3 files
                            layer_branch.add(f"[green]{f}[/green]")
                        if len(files) > 3:
                            layer_branch.add(f"[dim]... +{len(files)-3} more[/dim]")
            
            console.print(feature_tree)
    else:
        console.print()
        console.print("[dim]📦 No features found[/dim]")


def _list_pages(lib_path: Path) -> None:
    """List all simple pages (not features)."""
    pages = []
    
    # A page only has presentation/ subdir (no model, infrastructure, application)
    for item in lib_path.iterdir():
        if item.is_dir() and item.name not in ['core', 'shared', 'features', 'components']:
            subdirs = {d.name for d in item.iterdir() if d.is_dir()}
            # Only presentation, no model/infrastructure/application
            if 'presentation' in subdirs and not {'model', 'application'}.intersection(subdirs):
                pages.append(item)
    
    if pages:
        console.print()
        console.print("[bold blue]📄 Pages:[/bold blue]")
        for page in sorted(pages, key=lambda x: x.name):
            presentation_path = page / "presentation"
            dart_files = list(presentation_path.glob("*.dart")) if presentation_path.exists() else []
            file_count = f"({len(dart_files)} file{'s' if len(dart_files) != 1 else ''})"
            console.print(f"   [cyan]{page.name}/[/cyan] [dim]{file_count}[/dim]")
    else:
        console.print()
        console.print("[dim]📄 No simple pages found[/dim]")


def _list_components(lib_path: Path) -> None:
    """List all components."""
    components = []
    
    # Check in components/ folder
    components_dir = lib_path / "components"
    if components_dir.exists():
        for item in components_dir.iterdir():
            if item.is_dir():
                components.append(('components', item))
    
    # Check in shared/ folder
    shared_dir = lib_path / "shared"
    if shared_dir.exists():
        for item in shared_dir.iterdir():
            if item.is_dir():
                components.append(('shared', item))
    
    # Check for components in lib root (has application/ and presentation/ but no model/)
    for item in lib_path.iterdir():
        if item.is_dir() and item.name not in ['core', 'shared', 'features', 'components', 'home']:
            subdirs = {d.name for d in item.iterdir() if d.is_dir()}
            if {'application', 'presentation'}.issubset(subdirs) and 'model' not in subdirs:
                components.append(('root', item))
    
    if components:
        console.print()
        console.print("[bold blue]🧩 Components:[/bold blue]")
        for location, comp in sorted(components, key=lambda x: x[1].name):
            # Check if it's a form component
            app_path = comp / "application"
            is_form = any("form" in f.name.lower() for f in app_path.glob("*.dart")) if app_path.exists() else False
            comp_type = "[magenta](form)[/magenta]" if is_form else "[dim](standard)[/dim]"
            location_tag = f"[dim]@{location}[/dim]" if location != 'root' else ""
            console.print(f"   [cyan]{comp.name}/[/cyan] {comp_type} {location_tag}")
    else:
        console.print()
        console.print("[dim]🧩 No components found[/dim]")


def _list_routes(project_dir: Path, project_name: str) -> None:
    """List all routes from router.dart."""
    router_path = project_dir / "lib" / "router.dart"
    
    if not router_path.exists():
        console.print()
        console.print("[dim]🛤️  No router.dart found[/dim]")
        return
    
    routes = []
    try:
        with open(router_path, 'r') as f:
            content = f.read()
            
        # Parse routes - look for AutoRoute patterns
        import re
        
        # Pattern: AutoRoute(page: SomePage, path: '/something')
        pattern1 = r"AutoRoute\s*\(\s*page:\s*(\w+).*?path:\s*['\"]([^'\"]+)['\"]"
        # Pattern: AutoRoute(path: '/something', page: SomePage)
        pattern2 = r"AutoRoute\s*\(\s*path:\s*['\"]([^'\"]+)['\"].*?page:\s*(\w+)"
        
        for match in re.finditer(pattern1, content, re.DOTALL):
            routes.append((match.group(2), match.group(1)))
        
        for match in re.finditer(pattern2, content, re.DOTALL):
            routes.append((match.group(1), match.group(2)))
        
        # Also look for simple route definitions
        # Pattern: '/path': (context) => SomePage()
        pattern3 = r"['\"](/[^'\"]*)['\"].*?=>\s*(\w+)\s*\("
        for match in re.finditer(pattern3, content):
            route = (match.group(1), match.group(2))
            if route not in routes:
                routes.append(route)
                
    except Exception as e:
        console.print(f"[yellow]⚠️  Could not parse router.dart: {e}[/yellow]")
        return
    
    if routes:
        console.print()
        console.print("[bold blue]🛤️  Routes:[/bold blue]")
        # Remove duplicates while preserving order
        seen = set()
        unique_routes = []
        for r in routes:
            if r[0] not in seen:
                seen.add(r[0])
                unique_routes.append(r)
        
        for path, page in sorted(unique_routes, key=lambda x: x[0]):
            console.print(f"   [green]{path:<20}[/green] → [cyan]{page}[/cyan]")
    else:
        console.print()
        console.print("[dim]🛤️  No routes found in router.dart[/dim]")


if __name__ == "__main__":
    cli()
