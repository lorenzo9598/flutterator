"""Integration tests for Flutterator CLI commands"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import click.testing

# Import from the correct module
from generators.helpers import (
    generate_page_file,
    update_router,
    create_feature_layers,
    create_presentation_feature_layers,
    create_domain_entity_layers,
    find_domain_models,
    get_model_fields_from_domain,
    create_drawer_widget,
    update_home_screen_with_drawer,
    create_drawer_page,
    create_bottom_nav_widget,
    create_component_layers,
    create_component_form_layers,
    create_bottom_nav_page,
)


class TestPageGeneration:
    """Test page generation functionality"""

    def test_generate_page_file(self, sample_project_structure):
        """Test that generate_page_file creates correct page structure"""
        project_dir = sample_project_structure
        presentation_dir = project_dir / "lib" / "test_page" / "presentation"
        presentation_dir.mkdir(parents=True, exist_ok=True)

        generate_page_file("test_page", presentation_dir, "test_project")

        page_file = presentation_dir / "test_page_page.dart"
        assert page_file.exists()

        content = page_file.read_text()
        # Verify Dart class structure
        assert "class Test_pagePage" in content
        assert "@override" in content
        assert "Widget build" in content
        assert "BuildContext context" in content
        assert "import 'package:flutter/material.dart'" in content

    def test_update_router(self, sample_project_structure):
        """Test that update_router correctly adds routes"""
        project_dir = sample_project_structure

        # Initial router content
        initial_router = """import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:test_project/home/presentation/home_screen.dart';

final GoRouter router = GoRouter(
  routes: <RouteBase>[
    GoRoute(
      path: HomeScreen.routeName,
      builder: (BuildContext context, GoRouterState state) => const HomeScreen(),
    ),
  ],
);
"""
        router_file = project_dir / "lib" / "router.dart"
        router_file.write_text(initial_router)

        update_router(project_dir, "test_page", "test_project")

        updated_content = router_file.read_text()
        assert "test_page/presentation/test_page_page.dart" in updated_content
        assert "Test_pagePage.routeName" in updated_content
        assert "Test_pagePage()" in updated_content
        # Verify original route still exists
        assert "HomeScreen.routeName" in updated_content

    def test_update_router_with_folder(self, sample_project_structure):
        """Test update_router with nested folder"""
        project_dir = sample_project_structure
        
        router_file = project_dir / "lib" / "router.dart"
        
        update_router(project_dir, "settings", "test_project", folder="features")
        
        updated_content = router_file.read_text()
        assert "features/settings/presentation/settings_page.dart" in updated_content


class TestFeatureGeneration:
    """Test feature generation functionality"""

    def test_create_feature_layers(self, sample_project_structure):
        """Test creating standard feature layers"""
        project_dir = sample_project_structure
        feature_dir = project_dir / "lib" / "todo"
        feature_dir.mkdir(parents=True, exist_ok=True)

        field_list = [
            {"name": "id", "type": "string"},
            {"name": "title", "type": "string"},
            {"name": "completed", "type": "bool"}
        ]

        create_feature_layers(feature_dir, "todo", field_list, "test_project", "")

        # Check model layer
        assert (feature_dir / "model" / "todo.dart").exists()
        assert (feature_dir / "model" / "value_objects.dart").exists()
        assert (feature_dir / "model" / "value_validators.dart").exists()
        assert (feature_dir / "model" / "todo_failure.dart").exists()
        assert (feature_dir / "model" / "i_todo_repository.dart").exists()

        # Check application layer
        assert (feature_dir / "application" / "todo_event.dart").exists()
        assert (feature_dir / "application" / "todo_state.dart").exists()
        assert (feature_dir / "application" / "todo_bloc.dart").exists()

        # Check infrastructure layer
        assert (feature_dir / "infrastructure" / "todo_dto.dart").exists()
        assert (feature_dir / "infrastructure" / "todo_extensions.dart").exists()
        assert (feature_dir / "infrastructure" / "todo_repository.dart").exists()

        # Check presentation layer
        assert (feature_dir / "presentation" / "todo_page.dart").exists()

    def test_create_feature_layers_content(self, sample_project_structure):
        """Test that feature files have correct content"""
        project_dir = sample_project_structure
        feature_dir = project_dir / "lib" / "user"
        feature_dir.mkdir(parents=True, exist_ok=True)

        field_list = [
            {"name": "id", "type": "string"},
            {"name": "name", "type": "string"},
            {"name": "age", "type": "int"}
        ]

        create_feature_layers(feature_dir, "user", field_list, "test_project", "")

        # Check entity content
        entity_content = (feature_dir / "model" / "user.dart").read_text()
        assert "class User" in entity_content
        assert "freezed" in entity_content.lower() or "@freezed" in entity_content or "required" in entity_content

        # Check bloc content
        bloc_content = (feature_dir / "application" / "user_bloc.dart").read_text()
        assert "class UserBloc" in bloc_content
        assert "Bloc<" in bloc_content

        # Check DTO content
        dto_content = (feature_dir / "infrastructure" / "user_dto.dart").read_text()
        assert "class UserDto" in dto_content
        assert "String" in dto_content  # id field
        assert "int" in dto_content     # age field

    def test_create_feature_with_folder(self, sample_project_structure):
        """Test creating feature in nested folder"""
        project_dir = sample_project_structure
        feature_dir = project_dir / "lib" / "features" / "auth" / "login"
        feature_dir.mkdir(parents=True, exist_ok=True)

        field_list = [
            {"name": "id", "type": "string"},
            {"name": "email", "type": "string"}
        ]

        create_feature_layers(feature_dir, "login", field_list, "test_project", "features/auth")

        # Check import paths include folder
        bloc_content = (feature_dir / "application" / "login_bloc.dart").read_text()
        assert "features/auth" in bloc_content


class TestDrawerGeneration:
    """Test drawer generation functionality"""

    def test_create_drawer_widget_first_time(self, sample_project_structure):
        """Test creating drawer widget for first time"""
        project_dir = sample_project_structure

        create_drawer_widget(project_dir, "profile", "test_project")

        drawer_file = project_dir / "lib" / "core" / "presentation" / "app_drawer.dart"
        assert drawer_file.exists()

        content = drawer_file.read_text()
        assert "class AppDrawer" in content
        assert "profile/presentation/profile_page.dart" in content
        assert "ListTile" in content
        assert "Drawer" in content

    def test_create_drawer_widget_incremental(self, sample_project_structure):
        """Test adding drawer items incrementally"""
        project_dir = sample_project_structure

        # Add first item
        create_drawer_widget(project_dir, "profile", "test_project")

        # Add second item
        create_drawer_widget(project_dir, "settings", "test_project")

        drawer_file = project_dir / "lib" / "core" / "presentation" / "app_drawer.dart"
        content = drawer_file.read_text()

        # Both items should be present
        assert "profile/presentation/profile_page.dart" in content
        assert "settings/presentation/settings_page.dart" in content

    def test_update_home_screen_with_drawer(self, sample_project_structure):
        """Test updating home screen to include drawer"""
        project_dir = sample_project_structure

        update_home_screen_with_drawer(project_dir, "test_project")

        home_file = project_dir / "lib" / "home" / "presentation" / "home_screen.dart"
        content = home_file.read_text()

        assert "drawer: const AppDrawer()" in content
        assert "import 'package:test_project/core/presentation/app_drawer.dart';" in content


class TestBottomNavGeneration:
    """Test bottom navigation generation functionality"""

    def test_create_bottom_nav_widget(self, sample_project_structure):
        """Test creating bottom navigation widget"""
        project_dir = sample_project_structure

        create_bottom_nav_widget(project_dir, "search")

        nav_file = project_dir / "lib" / "core" / "presentation" / "bottom_nav_bar.dart"
        assert nav_file.exists()

        content = nav_file.read_text()
        assert "class BottomNavBar" in content
        assert "BottomNavigationBar" in content

    def test_create_bottom_nav_page(self, sample_project_structure):
        """Test creating bottom nav page screen"""
        project_dir = sample_project_structure

        create_bottom_nav_page(project_dir, "search")

        screen_file = project_dir / "lib" / "home" / "presentation" / "search_screen.dart"
        assert screen_file.exists()

        content = screen_file.read_text()
        assert "class SearchScreen" in content
        assert "StatelessWidget" in content


class TestComponentGeneration:
    """Test component generation functionality"""

    def test_create_component_layers_standard(self, sample_project_structure):
        """Test creating standard component layers"""
        project_dir = sample_project_structure
        component_dir = project_dir / "lib" / "user_card"
        component_dir.mkdir(parents=True, exist_ok=True)

        create_component_layers(component_dir, "user_card", "test_project", "")

        # Check application layer
        assert (component_dir / "application" / "user_card_bloc.dart").exists()
        assert (component_dir / "application" / "user_card_event.dart").exists()
        assert (component_dir / "application" / "user_card_state.dart").exists()

        # Check presentation layer
        assert (component_dir / "presentation" / "user_card_component.dart").exists()

        # Check content - Note: template currently generates User_cardBloc (snake_case preserved)
        bloc_content = (component_dir / "application" / "user_card_bloc.dart").read_text()
        assert "class User_cardBloc" in bloc_content or "class UserCardBloc" in bloc_content

    def test_create_component_layers_form(self, sample_project_structure):
        """Test creating form component layers"""
        project_dir = sample_project_structure
        component_dir = project_dir / "lib" / "login_form"
        component_dir.mkdir(parents=True, exist_ok=True)

        field_list = [
            {"name": "email", "type": "string"},
            {"name": "password", "type": "string"}
        ]

        create_component_form_layers(component_dir, "login_form", field_list, "test_project", "")

        # Check form-specific files
        assert (component_dir / "application" / "login_form_form_event.dart").exists()
        assert (component_dir / "application" / "login_form_form_state.dart").exists()
        assert (component_dir / "application" / "login_form_form_bloc.dart").exists()

        # Check presentation layer
        assert (component_dir / "presentation" / "login_form_component.dart").exists()

        # Check form event content has field change events
        event_content = (component_dir / "application" / "login_form_form_event.dart").read_text()
        assert "emailChanged" in event_content or "EmailChanged" in event_content


class TestCLICommands:
    """Test CLI command execution"""

    def test_cli_help(self):
        """Test that CLI help works"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Flutterator" in result.output
        assert "create" in result.output
        assert "add-page" in result.output
        assert "add-feature" in result.output

    def test_create_valid_name(self):
        """Test create command with valid name"""
        from flutterator import cli
        runner = click.testing.CliRunner()

        with patch('flutterator.init') as mock_init, \
             patch('flutterator.run_flutter_commands') as mock_flutter:
            
            mock_init.return_value = None
            mock_flutter.return_value = None
            
            result = runner.invoke(cli, ["create", "--name", "valid_name", "--login"])
            assert result.exit_code == 0

    def test_create_invalid_name(self):
        """Test create command with invalid name"""
        from flutterator import cli
        runner = click.testing.CliRunner()

        result = runner.invoke(cli, ["create", "--name", "invalid-name!", "--login"])
        assert result.exit_code != 0
        assert "must contain only letters, numbers, _ and -" in result.output

    def test_add_page_help(self):
        """Test add-page command help"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        result = runner.invoke(cli, ["add-page", "--help"])
        assert result.exit_code == 0
        assert "--name" in result.output
        assert "--dry-run" in result.output

    def test_add_feature_help(self):
        """Test add-feature command help"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        result = runner.invoke(cli, ["add-feature", "--help"])
        assert result.exit_code == 0
        assert "--name" in result.output
        assert "--fields" in result.output
        assert "--folder" in result.output
        assert "--dry-run" in result.output


class TestDryRunMode:
    """Test --dry-run flag functionality"""

    def test_add_page_dry_run(self, sample_project_structure):
        """Test add-page with --dry-run doesn't create files"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        project_dir = sample_project_structure
        
        with runner.isolated_filesystem():
            # Copy sample project to isolated filesystem
            import shutil
            shutil.copytree(project_dir, "test_project")
            
            result = runner.invoke(cli, [
                "add-page", 
                "--name", "settings",
                "--project-path", "test_project",
                "--dry-run"
            ])
            
            assert result.exit_code == 0
            assert "DRY-RUN MODE" in result.output
            assert "settings" in result.output
            
            # Verify no files were created
            settings_dir = Path("test_project/lib/settings")
            assert not settings_dir.exists()

    def test_add_feature_dry_run(self, sample_project_structure):
        """Test add-feature with --dry-run doesn't create files"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        project_dir = sample_project_structure
        
        with runner.isolated_filesystem():
            import shutil
            shutil.copytree(project_dir, "test_project")
            
            result = runner.invoke(cli, [
                "add-feature",
                "--name", "todo",
                "--fields", "title:string,done:bool",
                "--project-path", "test_project",
                "--dry-run"
            ])
            
            assert result.exit_code == 0
            assert "DRY-RUN MODE" in result.output
            assert "todo" in result.output
            assert "model" in result.output
            assert "infrastructure" in result.output
            assert "application" in result.output
            assert "presentation" in result.output
            
            # Verify no files were created
            todo_dir = Path("test_project/lib/todo")
            assert not todo_dir.exists()

    def test_add_component_dry_run(self, sample_project_structure):
        """Test add-component with --dry-run doesn't create files"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        project_dir = sample_project_structure
        
        with runner.isolated_filesystem():
            import shutil
            shutil.copytree(project_dir, "test_project")
            
            result = runner.invoke(cli, [
                "add-component",
                "--name", "user_card",
                "--project-path", "test_project",
                "--dry-run"
            ])
            
            assert result.exit_code == 0
            assert "DRY-RUN MODE" in result.output
            
            # Verify no files were created
            component_dir = Path("test_project/lib/user_card")
            assert not component_dir.exists()


class TestDryRunModeExtended:
    """Extended dry-run tests for drawer and bottom nav"""

    def test_add_drawer_item_dry_run(self, sample_project_structure):
        """Test add-drawer-item with --dry-run doesn't create files"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        project_dir = sample_project_structure
        
        with runner.isolated_filesystem():
            import shutil
            shutil.copytree(project_dir, "test_project")
            
            result = runner.invoke(cli, [
                "add-drawer-item",
                "--name", "profile",
                "--project-path", "test_project",
                "--dry-run"
            ])
            
            assert result.exit_code == 0
            assert "DRY-RUN MODE" in result.output
            assert "profile" in result.output
            assert "router.dart" in result.output
            assert "app_drawer.dart" in result.output
            
            # Verify no files were created
            profile_dir = Path("test_project/lib/profile")
            assert not profile_dir.exists()
            drawer_file = Path("test_project/lib/core/presentation/app_drawer.dart")
            assert not drawer_file.exists()

    def test_add_bottom_nav_item_dry_run(self, sample_project_structure):
        """Test add-bottom-nav-item with --dry-run doesn't create files"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        project_dir = sample_project_structure
        
        with runner.isolated_filesystem():
            import shutil
            shutil.copytree(project_dir, "test_project")
            
            result = runner.invoke(cli, [
                "add-bottom-nav-item",
                "--name", "search",
                "--project-path", "test_project",
                "--dry-run"
            ])
            
            assert result.exit_code == 0
            assert "DRY-RUN MODE" in result.output
            assert "search" in result.output
            assert "home_screen.dart" in result.output
            assert "bottom_nav_bar.dart" in result.output
            
            # Verify no files were created
            screen_file = Path("test_project/lib/home/presentation/search_screen.dart")
            assert not screen_file.exists()
            nav_file = Path("test_project/lib/core/presentation/bottom_nav_bar.dart")
            assert not nav_file.exists()


class TestCLICommandsExtended:
    """Extended CLI command tests"""

    def test_add_drawer_item_cli(self, sample_project_structure):
        """Test add-drawer-item CLI command executes correctly"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        project_dir = sample_project_structure
        
        with runner.isolated_filesystem():
            import shutil
            shutil.copytree(project_dir, "test_project")
            
            result = runner.invoke(cli, [
                "add-drawer-item",
                "--name", "settings",
                "--project-path", "test_project",
                "--no-build"
            ])
            
            assert result.exit_code == 0
            assert "settings" in result.output.lower() or "Settings" in result.output
            
            # Verify files were created
            page_file = Path("test_project/lib/settings/presentation/settings_page.dart")
            assert page_file.exists()
            
            drawer_file = Path("test_project/lib/core/presentation/app_drawer.dart")
            assert drawer_file.exists()
            
            # Verify drawer contains settings
            drawer_content = drawer_file.read_text()
            assert "settings" in drawer_content.lower()

    def test_add_bottom_nav_item_cli(self, sample_project_structure):
        """Test add-bottom-nav-item CLI command executes correctly"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        project_dir = sample_project_structure
        
        with runner.isolated_filesystem():
            import shutil
            shutil.copytree(project_dir, "test_project")
            
            result = runner.invoke(cli, [
                "add-bottom-nav-item",
                "--name", "favorites",
                "--project-path", "test_project",
                "--no-build"
            ])
            
            assert result.exit_code == 0
            assert "favorites" in result.output.lower() or "Favorites" in result.output
            
            # Verify screen was created
            screen_file = Path("test_project/lib/home/presentation/favorites_screen.dart")
            assert screen_file.exists()
            
            # Verify bottom nav was created
            nav_file = Path("test_project/lib/core/presentation/bottom_nav_bar.dart")
            assert nav_file.exists()

    def test_add_drawer_item_help(self):
        """Test add-drawer-item command help"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        result = runner.invoke(cli, ["add-drawer-item", "--help"])
        assert result.exit_code == 0
        assert "--name" in result.output
        assert "--dry-run" in result.output
        assert "drawer" in result.output.lower()

    def test_add_bottom_nav_item_help(self):
        """Test add-bottom-nav-item command help"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        result = runner.invoke(cli, ["add-bottom-nav-item", "--help"])
        assert result.exit_code == 0
        assert "--name" in result.output
        assert "--dry-run" in result.output
        assert "bottom" in result.output.lower() or "navigation" in result.output.lower()


class TestContentVerification:
    """Test that generated content is correct"""

    def test_component_content_standard(self, sample_project_structure):
        """Test that standard component has correct content structure"""
        project_dir = sample_project_structure
        component_dir = project_dir / "lib" / "product_card"
        component_dir.mkdir(parents=True, exist_ok=True)

        create_component_layers(component_dir, "product_card", "test_project", "")

        # Check bloc content structure
        bloc_content = (component_dir / "application" / "product_card_bloc.dart").read_text()
        assert "Bloc<" in bloc_content
        assert "Event" in bloc_content
        assert "State" in bloc_content
        
        # Check event content
        event_content = (component_dir / "application" / "product_card_event.dart").read_text()
        assert "sealed class" in event_content or "abstract class" in event_content or "@freezed" in event_content
        
        # Check state content
        state_content = (component_dir / "application" / "product_card_state.dart").read_text()
        assert "class" in state_content
        
        # Check widget content
        widget_content = (component_dir / "presentation" / "product_card_component.dart").read_text()
        assert "Widget" in widget_content
        assert "build" in widget_content
        assert "BlocProvider" in widget_content or "BlocBuilder" in widget_content or "Bloc" in widget_content

    def test_bottom_nav_screen_content(self, sample_project_structure):
        """Test that bottom nav screen has correct content"""
        project_dir = sample_project_structure

        create_bottom_nav_page(project_dir, "explore")

        screen_file = project_dir / "lib" / "home" / "presentation" / "explore_screen.dart"
        assert screen_file.exists()
        
        content = screen_file.read_text()
        
        # Verify basic structure
        assert "class ExploreScreen" in content
        assert "StatelessWidget" in content
        assert "Widget build" in content
        assert "BuildContext" in content
        assert "import 'package:flutter/material.dart'" in content
        
        # Verify it returns a widget
        assert "return" in content

    def test_drawer_page_content(self, sample_project_structure):
        """Test that drawer page has correct content"""
        from generators.helpers import create_drawer_page
        
        project_dir = sample_project_structure
        
        create_drawer_page(project_dir, "about", "test_project")
        
        page_file = project_dir / "lib" / "about" / "presentation" / "about_page.dart"
        assert page_file.exists()
        
        content = page_file.read_text()
        
        # Verify basic structure
        assert "class About" in content or "class AboutPage" in content
        assert "StatelessWidget" in content
        assert "Widget build" in content
        assert "routeName" in content  # Should have route name


class TestErrorHandling:
    """Test error handling"""

    def test_invalid_project_directory(self):
        """Test error when not in Flutter project"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        with runner.isolated_filesystem():
            # Create empty directory (no pubspec.yaml)
            result = runner.invoke(cli, ["add-page", "--name", "test"])
            
            assert result.exit_code != 0
            assert "Not a valid Flutter project" in result.output

    def test_missing_lib_directory(self):
        """Test error when lib directory is missing"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        with runner.isolated_filesystem():
            # Create pubspec but no lib
            Path("pubspec.yaml").write_text("name: test\n")
            
            result = runner.invoke(cli, ["add-page", "--name", "test"])
            
            assert result.exit_code != 0
            assert "lib directory not found" in result.output

    def test_drawer_item_error_no_home(self, sample_project_structure):
        """Test error when home presentation doesn't exist for drawer"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        with runner.isolated_filesystem():
            # Create minimal project without home/presentation
            Path("pubspec.yaml").write_text("name: test\n")
            Path("lib").mkdir()
            
            result = runner.invoke(cli, [
                "add-drawer-item",
                "--name", "settings"
            ])
            
            assert result.exit_code != 0
            assert "Home presentation directory not found" in result.output

    def test_bottom_nav_error_no_home(self, sample_project_structure):
        """Test error when home presentation doesn't exist for bottom nav"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        with runner.isolated_filesystem():
            # Create minimal project without home/presentation
            Path("pubspec.yaml").write_text("name: test\n")
            Path("lib").mkdir()
            
            result = runner.invoke(cli, [
                "add-bottom-nav-item",
                "--name", "search"
            ])
            
            assert result.exit_code != 0
            assert "Home presentation directory not found" in result.output

    def test_component_error_invalid_fields(self):
        """Test error when form component has invalid fields format"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        with runner.isolated_filesystem():
            # Create valid project structure
            Path("pubspec.yaml").write_text("name: test\n")
            Path("lib").mkdir()
            
            # Try to create form component with invalid field format (missing type)
            result = runner.invoke(cli, [
                "add-component",
                "--name", "test_form",
                "--form",
                "--fields", "invalid_field_no_type"
            ])
            
            # Should fail because field format is wrong (missing :type)
            assert result.exit_code != 0


class TestFeatureBehavior:
    """Test feature behavior in edge cases"""

    def test_feature_duplicate_directory(self, sample_project_structure):
        """Test behavior when feature directory already exists"""
        project_dir = sample_project_structure
        feature_dir = project_dir / "lib" / "existing_feature"
        feature_dir.mkdir(parents=True, exist_ok=True)
        
        # Create some existing content
        (feature_dir / "model").mkdir()
        (feature_dir / "model" / "old_file.dart").write_text("// old content")
        
        field_list = [
            {"name": "id", "type": "string"},
            {"name": "title", "type": "string"}
        ]
        
        # Should not fail - mkdir with exist_ok=True
        create_feature_layers(feature_dir, "existing_feature", field_list, "test_project", "")
        
        # Verify new files were created alongside old
        assert (feature_dir / "model" / "existing_feature.dart").exists()
        assert (feature_dir / "model" / "old_file.dart").exists()  # Old file preserved


class TestNewCommands:
    """Test new commands: init, list, config"""

    def test_init_command_creates_config(self, sample_project_structure):
        """Test init command creates flutterator.yaml"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        project_dir = sample_project_structure
        
        with runner.isolated_filesystem():
            import shutil
            shutil.copytree(project_dir, "test_project")
            
            result = runner.invoke(cli, [
                "init",
                "--project-path", "test_project"
            ])
            
            assert result.exit_code == 0
            assert "Flutterator initialized" in result.output
            
            # Verify config file was created
            config_file = Path("test_project/flutterator.yaml")
            assert config_file.exists()
            
            # Verify content has expected sections
            content = config_file.read_text()
            assert "defaults:" in content
            assert "feature_folder" in content

    def test_init_command_creates_directories(self, sample_project_structure):
        """Test init command creates directory structure"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        with runner.isolated_filesystem():
            # Create minimal project
            Path("pubspec.yaml").write_text("name: my_app\n")
            Path("lib").mkdir()
            
            result = runner.invoke(cli, ["init"])
            
            assert result.exit_code == 0
            
            # Verify directories were created
            assert Path("lib/core").exists()
            assert Path("lib/features").exists()
            assert Path("lib/shared").exists()

    def test_init_command_force_flag(self, sample_project_structure):
        """Test init --force overwrites existing config"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        project_dir = sample_project_structure
        
        with runner.isolated_filesystem():
            import shutil
            shutil.copytree(project_dir, "test_project")
            
            # Create existing config
            config_file = Path("test_project/flutterator.yaml")
            config_file.write_text("# old config\n")
            
            result = runner.invoke(cli, [
                "init",
                "--project-path", "test_project",
                "--force"
            ])
            
            assert result.exit_code == 0
            
            # Verify config was overwritten
            content = config_file.read_text()
            assert "defaults:" in content  # New config format
            assert "# old config" not in content

    def test_list_command_all(self, sample_project_structure):
        """Test list command shows all resources"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        project_dir = sample_project_structure
        
        # Create a feature to list
        feature_dir = project_dir / "lib" / "todo"
        feature_dir.mkdir(parents=True, exist_ok=True)
        (feature_dir / "model").mkdir()
        (feature_dir / "application").mkdir()
        (feature_dir / "model" / "todo.dart").write_text("class Todo {}")
        (feature_dir / "application" / "todo_bloc.dart").write_text("class TodoBloc {}")
        
        with runner.isolated_filesystem():
            import shutil
            shutil.copytree(project_dir, "test_project")
            
            result = runner.invoke(cli, [
                "list",
                "--project-path", "test_project"
            ])
            
            assert result.exit_code == 0
            assert "Features" in result.output or "features" in result.output.lower()
            assert "todo" in result.output.lower()

    def test_list_command_features_only(self, sample_project_structure):
        """Test list features command"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        project_dir = sample_project_structure
        
        # Create a feature
        feature_dir = project_dir / "lib" / "user"
        feature_dir.mkdir(parents=True, exist_ok=True)
        (feature_dir / "model").mkdir()
        (feature_dir / "application").mkdir()
        (feature_dir / "model" / "user.dart").write_text("class User {}")
        
        with runner.isolated_filesystem():
            import shutil
            shutil.copytree(project_dir, "test_project")
            
            result = runner.invoke(cli, [
                "list", "features",
                "--project-path", "test_project"
            ])
            
            assert result.exit_code == 0
            assert "user" in result.output.lower()

    def test_list_command_routes(self, sample_project_structure):
        """Test list routes command"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        project_dir = sample_project_structure
        
        # Create router with routes
        router_content = """
AutoRoute(page: HomePage, path: '/home')
AutoRoute(page: SettingsPage, path: '/settings')
"""
        (project_dir / "lib" / "router.dart").write_text(router_content)
        
        with runner.isolated_filesystem():
            import shutil
            shutil.copytree(project_dir, "test_project")
            
            result = runner.invoke(cli, [
                "list", "routes",
                "--project-path", "test_project"
            ])
            
            assert result.exit_code == 0
            assert "/home" in result.output or "home" in result.output.lower()

    def test_config_command_show(self, sample_project_structure):
        """Test config --show displays configuration"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        project_dir = sample_project_structure
        
        with runner.isolated_filesystem():
            import shutil
            shutil.copytree(project_dir, "test_project")
            
            result = runner.invoke(cli, [
                "config", "--show",
                "--project-path", "test_project"
            ])
            
            assert result.exit_code == 0
            assert "Configuration" in result.output
            assert "Feature Folder" in result.output or "feature_folder" in result.output.lower()

    def test_config_command_init(self, sample_project_structure):
        """Test config --init creates config file"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        project_dir = sample_project_structure
        
        with runner.isolated_filesystem():
            import shutil
            shutil.copytree(project_dir, "test_project")
            
            result = runner.invoke(cli, [
                "config", "--init",
                "--project-path", "test_project"
            ])
            
            assert result.exit_code == 0
            assert "Created flutterator.yaml" in result.output
            
            # Verify file exists
            assert Path("test_project/flutterator.yaml").exists()

    def test_config_not_flutter_project(self):
        """Test config --init fails on non-Flutter project"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        with runner.isolated_filesystem():
            # Empty directory - no pubspec.yaml
            result = runner.invoke(cli, ["config", "--init"])
            
            assert result.exit_code != 0
            assert "Not a Flutter project" in result.output


class TestFeatureModes:
    """Test the three modes of add-feature command"""

    def test_find_domain_models(self, sample_project_structure):
        """Test finding domain models in domain folder"""
        project_dir = sample_project_structure
        lib_path = project_dir / "lib"
        
        # Create domain folder with models
        domain_dir = lib_path / "domain"
        domain_dir.mkdir(exist_ok=True)
        
        # Create first domain model
        model1_dir = domain_dir / "user"
        model1_dir.mkdir()
        (model1_dir / "model").mkdir()
        (model1_dir / "model" / "user.dart").write_text("class User {}")
        
        # Create second domain model
        model2_dir = domain_dir / "note"
        model2_dir.mkdir()
        (model2_dir / "model").mkdir()
        (model2_dir / "model" / "note.dart").write_text("class Note {}")
        
        models = find_domain_models(lib_path, "domain")
        
        assert len(models) == 2
        assert "user" in models
        assert "note" in models

    def test_find_domain_models_empty(self, sample_project_structure):
        """Test finding domain models when domain folder doesn't exist"""
        project_dir = sample_project_structure
        lib_path = project_dir / "lib"
        
        models = find_domain_models(lib_path, "domain")
        
        assert models == []

    def test_create_domain_entity_only(self, sample_project_structure):
        """Test creating only domain entity with --domain flag"""
        project_dir = sample_project_structure
        lib_path = project_dir / "lib"
        domain_dir = lib_path / "domain" / "product"
        domain_dir.mkdir(parents=True, exist_ok=True)
        
        field_list = [
            {"name": "id", "type": "string"},
            {"name": "name", "type": "string"},
            {"name": "price", "type": "double"}
        ]
        
        create_domain_entity_layers(domain_dir, "product", field_list, "test_project", "domain")
        
        # Should have model and infrastructure
        assert (domain_dir / "model" / "product.dart").exists()
        assert (domain_dir / "model" / "product_failure.dart").exists()
        assert (domain_dir / "model" / "i_product_repository.dart").exists()
        assert (domain_dir / "infrastructure" / "product_repository.dart").exists()
        
        # Should NOT have application or presentation
        assert not (domain_dir / "application").exists()
        assert not (domain_dir / "presentation").exists()

    def test_create_presentation_feature_layers(self, sample_project_structure):
        """Test creating only presentation feature layers"""
        project_dir = sample_project_structure
        lib_path = project_dir / "lib"
        
        # First create a domain model
        domain_dir = lib_path / "domain" / "todo"
        domain_dir.mkdir(parents=True, exist_ok=True)
        
        field_list = [
            {"name": "id", "type": "string"},
            {"name": "title", "type": "string"}
        ]
        
        create_domain_entity_layers(domain_dir, "todo", field_list, "test_project", "domain")
        
        # Now create feature that uses this domain model
        feature_dir = lib_path / "features" / "todo"
        feature_dir.mkdir(parents=True, exist_ok=True)
        
        create_presentation_feature_layers(
            feature_dir, "todo", "todo", "domain", "test_project", "features"
        )
        
        # Should have application and presentation
        assert (feature_dir / "application" / "todo_bloc.dart").exists()
        assert (feature_dir / "application" / "todo_event.dart").exists()
        assert (feature_dir / "application" / "todo_state.dart").exists()
        assert (feature_dir / "presentation" / "todo_page.dart").exists()
        
        # Should NOT have model or infrastructure
        assert not (feature_dir / "model").exists()
        assert not (feature_dir / "infrastructure").exists()
        
        # Check that bloc imports from domain
        bloc_content = (feature_dir / "application" / "todo_bloc.dart").read_text()
        assert "domain/todo" in bloc_content
        assert "ITodoRepository" in bloc_content

    def test_add_feature_default_mode(self, sample_project_structure):
        """Test add-feature default mode creates both domain and feature"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        project_dir = sample_project_structure
        
        with runner.isolated_filesystem():
            import shutil
            shutil.copytree(project_dir, "test_project")
            
            result = runner.invoke(cli, [
                "add-feature",
                "--name", "product",
                "--fields", "name:string,price:double",
                "--project-path", "test_project",
                "--no-build"
            ])
            
            assert result.exit_code == 0
            
            # Should create domain entity
            domain_dir = Path("test_project/lib/domain/product")
            assert (domain_dir / "model" / "product.dart").exists()
            assert (domain_dir / "infrastructure" / "product_repository.dart").exists()
            
            # Should create feature
            feature_dir = Path("test_project/lib/features/product")
            assert (feature_dir / "application" / "product_bloc.dart").exists()
            assert (feature_dir / "presentation" / "product_page.dart").exists()

    def test_add_feature_domain_mode(self, sample_project_structure):
        """Test add-feature --domain creates only domain entity"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        project_dir = sample_project_structure
        
        with runner.isolated_filesystem():
            import shutil
            shutil.copytree(project_dir, "test_project")
            
            result = runner.invoke(cli, [
                "add-feature",
                "--name", "category",
                "--domain",
                "--fields", "name:string",
                "--project-path", "test_project",
                "--no-build"
            ])
            
            assert result.exit_code == 0
            
            # Should create domain entity
            domain_dir = Path("test_project/lib/domain/category")
            assert (domain_dir / "model" / "category.dart").exists()
            assert (domain_dir / "infrastructure" / "category_repository.dart").exists()
            
            # Should NOT create feature
            feature_dir = Path("test_project/lib/features/category")
            assert not feature_dir.exists()

    def test_add_feature_presentation_mode(self, sample_project_structure):
        """Test add-feature --presentation creates only feature using domain model"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        project_dir = sample_project_structure
        
        # First create a domain model
        lib_path = project_dir / "lib"
        domain_dir = lib_path / "domain" / "user"
        domain_dir.mkdir(parents=True, exist_ok=True)
        
        field_list = [
            {"name": "id", "type": "string"},
            {"name": "name", "type": "string"},
            {"name": "email", "type": "string"}
        ]
        
        from generators.helpers import create_domain_entity_layers
        create_domain_entity_layers(domain_dir, "user", field_list, "test_project", "domain")
        
        with runner.isolated_filesystem():
            import shutil
            shutil.copytree(project_dir, "test_project")
            
            # Use input to select the first model (user)
            result = runner.invoke(cli, [
                "add-feature",
                "--name", "user_profile",
                "--presentation",
                "--project-path", "test_project",
                "--no-build"
            ], input="1\n")  # Select first model
            
            assert result.exit_code == 0
            
            # Should create feature
            feature_dir = Path("test_project/lib/features/user_profile")
            assert (feature_dir / "application" / "user_profile_bloc.dart").exists()
            assert (feature_dir / "presentation" / "user_profile_page.dart").exists()
            
            # Should NOT create domain (already exists)
            # Check that bloc imports from domain
            bloc_content = (feature_dir / "application" / "user_profile_bloc.dart").read_text()
            assert "domain/user" in bloc_content
            assert "IUserRepository" in bloc_content

    def test_add_feature_presentation_no_domain_models(self, sample_project_structure):
        """Test add-feature --presentation fails when no domain models exist"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        project_dir = sample_project_structure
        
        with runner.isolated_filesystem():
            import shutil
            shutil.copytree(project_dir, "test_project")
            
            result = runner.invoke(cli, [
                "add-feature",
                "--name", "test_feature",
                "--presentation",
                "--project-path", "test_project",
                "--no-build"
            ])
            
            assert result.exit_code != 0
            assert "No domain models found" in result.output


class TestComponentWithDomainModels:
    """Test component generation with domain model selection"""

    def test_get_model_fields_from_domain(self, sample_project_structure):
        """Test extracting fields from domain model entity file"""
        project_dir = sample_project_structure
        lib_path = project_dir / "lib"
        
        # Create domain model
        domain_dir = lib_path / "domain" / "product"
        domain_dir.mkdir(parents=True, exist_ok=True)
        
        # Create entity file
        model_dir = domain_dir / "model"
        model_dir.mkdir()
        entity_content = """@freezed
abstract class Product with _$Product {
  const factory Product({
    required UniqueId id,
    required Title title,
    required Description description,
  }) = _Product;
}
"""
        (model_dir / "product.dart").write_text(entity_content)
        
        fields = get_model_fields_from_domain(lib_path, "domain", "product")
        
        assert len(fields) == 3
        assert fields[0]["name"] == "id"
        assert fields[1]["name"] == "title"
        assert fields[2]["name"] == "description"

    def test_add_component_with_domain_model(self, sample_project_structure):
        """Test add-component selects and uses domain model"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        project_dir = sample_project_structure
        lib_path = project_dir / "lib"
        
        # Create domain model
        domain_dir = lib_path / "domain" / "user"
        domain_dir.mkdir(parents=True, exist_ok=True)
        
        field_list = [
            {"name": "id", "type": "string"},
            {"name": "name", "type": "string"},
            {"name": "email", "type": "string"}
        ]
        
        from generators.helpers import create_domain_entity_layers
        create_domain_entity_layers(domain_dir, "user", field_list, "test_project", "domain")
        
        with runner.isolated_filesystem():
            import shutil
            shutil.copytree(project_dir, "test_project")
            
            result = runner.invoke(cli, [
                "add-component",
                "--name", "user_card",
                "--project-path", "test_project",
                "--no-build"
            ], input="1\n")  # Select first model
            
            assert result.exit_code == 0
            
            # Should create component
            component_dir = Path("test_project/lib/user_card")
            assert (component_dir / "application" / "user_card_bloc.dart").exists()
            assert (component_dir / "presentation" / "user_card_component.dart").exists()
            
            # Check that bloc imports from domain
            bloc_content = (component_dir / "application" / "user_card_bloc.dart").read_text()
            assert "domain/user" in bloc_content
            assert "IUserRepository" in bloc_content

    def test_add_component_form_with_domain_model(self, sample_project_structure):
        """Test add-component --form uses fields from domain model"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        project_dir = sample_project_structure
        lib_path = project_dir / "lib"
        
        # Create domain model
        domain_dir = lib_path / "domain" / "todo"
        domain_dir.mkdir(parents=True, exist_ok=True)
        
        field_list = [
            {"name": "id", "type": "string"},
            {"name": "title", "type": "string"},
            {"name": "completed", "type": "bool"}
        ]
        
        from generators.helpers import create_domain_entity_layers
        create_domain_entity_layers(domain_dir, "todo", field_list, "test_project", "domain")
        
        # Create entity file with proper structure
        model_dir = domain_dir / "model"
        entity_content = """@freezed
abstract class Todo with _$Todo {
  const factory Todo({
    required UniqueId id,
    required Title title,
    required Completed completed,
  }) = _Todo;
}
"""
        (model_dir / "todo.dart").write_text(entity_content)
        
        with runner.isolated_filesystem():
            import shutil
            shutil.copytree(project_dir, "test_project")
            
            result = runner.invoke(cli, [
                "add-component",
                "--name", "todo_form",
                "--form",
                "--project-path", "test_project",
                "--no-build"
            ], input="1\n")  # Select first model
            
            assert result.exit_code == 0
            
            # Should create form component
            component_dir = Path("test_project/lib/todo_form")
            assert (component_dir / "application" / "todo_form_form_bloc.dart").exists()
            assert (component_dir / "application" / "todo_form_form_event.dart").exists()
            assert (component_dir / "application" / "todo_form_form_state.dart").exists()
            assert (component_dir / "presentation" / "todo_form_component.dart").exists()
            
            # Check form state has fields from domain model
            state_content = (component_dir / "application" / "todo_form_form_state.dart").read_text()
            # Should have title field (id is typically skipped in forms)
            assert "title" in state_content.lower() or "Title" in state_content

    def test_add_component_no_domain_models(self, sample_project_structure):
        """Test add-component fails when no domain models exist"""
        from flutterator import cli
        runner = click.testing.CliRunner()
        
        project_dir = sample_project_structure
        
        with runner.isolated_filesystem():
            import shutil
            shutil.copytree(project_dir, "test_project")
            
            result = runner.invoke(cli, [
                "add-component",
                "--name", "test_component",
                "--project-path", "test_project",
                "--no-build"
            ])
            
            assert result.exit_code != 0
            assert "No domain models found" in result.output
