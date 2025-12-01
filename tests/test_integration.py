"""Integration tests for Flutterator CLI commands"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from flutterator import (
    generate_page_file,
    update_router,
    create_feature_layers,
    create_drawer_widget,
    update_home_screen_with_drawer,
    create_bottom_nav_widget,
    create_component_layers,
    create_component_form_layers,
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
        assert "class Test_pagePage" in content
        assert "@override" in content
        assert "Widget build" in content

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


class TestFeatureGeneration:
    """Test feature generation functionality"""

    def test_create_feature_layers(self, sample_project_structure):
        """Test creating standard feature layers"""
        project_dir = sample_project_structure
        feature_dir = project_dir / "lib" / "todo"
        feature_dir.mkdir(parents=True, exist_ok=True)  # Create parent directories

        print(feature_dir)

        field_list = [
            {"name": "title", "type": "string"},
            {"name": "completed", "type": "bool"}
        ]

        create_feature_layers(feature_dir, "todo", field_list, "test_project", "")

        # Check model layer
        assert (feature_dir / "model" / "todo.dart").exists()
        assert (feature_dir / "model" / "value_objects.dart").exists()
        assert (feature_dir / "model" / "value_validators.dart").exists()
        assert (feature_dir / "model" / "todo_failure.dart").exists()

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

        # Count ListTile widgets
        list_tile_count = content.count("ListTile(")
        assert list_tile_count == 3

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


class TestComponentGeneration:
    """Test component generation functionality"""

    def test_create_component_layers_standard(self, sample_project_structure):
        """Test creating standard component layers"""
        project_dir = sample_project_structure
        component_dir = project_dir / "lib" / "user_card"
        component_dir.mkdir(parents=True, exist_ok=True)  # Create parent directories

        create_component_layers(component_dir, "user_card", "test_project", "")

        # Check application layer
        assert (component_dir / "application" / "user_card_bloc.dart").exists()

        # Check presentation layer
        assert (component_dir / "presentation" / "user_card_component.dart").exists()

    def test_create_component_layers_form(self, sample_project_structure):
        """Test creating form component layers"""
        project_dir = sample_project_structure
        component_dir = project_dir / "lib" / "login_form"
        component_dir.mkdir(parents=True, exist_ok=True)  # Create parent directories

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


class TestCLIParameterValidation:
    """Test CLI parameter validation"""

    def test_project_name_validation(self):
        """Test project name validation logic"""
        from flutterator import cli
        import click.testing
        from unittest.mock import patch, MagicMock

        runner = click.testing.CliRunner()

        # Valid names should work (mock all external dependencies)
        with patch('flutterator.init') as mock_init, \
             patch('flutterator.run_flutter_commands') as mock_flutter, \
             patch('pathlib.Path.mkdir') as mock_mkdir:
            
            mock_init.return_value = None
            mock_flutter.return_value = None
            mock_mkdir.return_value = None
            
            result = runner.invoke(cli, ["create", "--name", "valid_name", "--login"])
            print(f"Valid name result: {result.output}")
            assert result.exit_code == 0

        # Invalid names should fail
        result = runner.invoke(cli, ["create", "--name", "invalid-name!", "--login"])
        print(f"Invalid name result: {result.output}")
        assert result.exit_code != 0
        assert "must contain only letters, numbers, _ and -" in result.output
