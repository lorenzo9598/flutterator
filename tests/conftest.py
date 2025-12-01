import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
import subprocess


@pytest.fixture
def temp_project_dir():
    """Create a temporary directory for testing project generation"""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    # Cleanup after test
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def mock_subprocess():
    """Mock subprocess calls for testing"""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout='', stderr='')
        yield mock_run


@pytest.fixture
def sample_project_structure(temp_project_dir):
    """Create a sample Flutter project structure for testing"""
    # Create basic Flutter project structure
    lib_dir = temp_project_dir / "lib"
    lib_dir.mkdir()

    # Create pubspec.yaml
    pubspec_content = """name: test_project
description: A test Flutter project
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter

dev_dependencies:
  flutter_test:
    sdk: flutter
"""
    (temp_project_dir / "pubspec.yaml").write_text(pubspec_content)

    # Create basic home structure
    home_dir = lib_dir / "home" / "presentation"
    home_dir.mkdir(parents=True)

    home_screen_content = """import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  static const String routeName = '/home';

  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      appBar: AppBar(
        title: Text('Home'),
      ),
      body: Center(
        child: Text('Home Content'),
      ),
    );
  }
}
"""
    (home_dir / "home_screen.dart").write_text(home_screen_content)

    # Create router.dart
    router_content = """import 'package:flutter/material.dart';
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
    (lib_dir / "router.dart").write_text(router_content)

    return temp_project_dir


@pytest.fixture
def mock_click_echo():
    """Mock click.echo to capture output"""
    with patch('click.echo') as mock_echo:
        yield mock_echo


@pytest.fixture
def mock_interactive_inputs():
    """Mock for interactive CLI inputs using pexpect-like behavior"""
    def mock_input_sequence(inputs):
        """Return a function that provides inputs in sequence"""
        input_iter = iter(inputs)
        def mock_prompt(text="", default=None, **kwargs):
            try:
                return next(input_iter)
            except StopIteration:
                return default
        return mock_prompt
    return mock_input_sequence


@pytest.fixture
def flutterator_command():
    """Helper fixture to run flutterator commands"""
    def run_command(*args, cwd=None, **kwargs):
        """Run a flutterator command with given arguments"""
        cmd = [sys.executable, "-m", "flutterator"] + list(args)
        return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, **kwargs)
    return run_command
