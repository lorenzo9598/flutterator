"""Project validation and utility functions"""

import sys
from pathlib import Path
from rich.console import Console

console = Console()


def get_project_name(project_dir: Path) -> str:
    """Extract project name from pubspec.yaml"""
    pubspec_path = project_dir / "pubspec.yaml"
    if pubspec_path.exists():
        with open(pubspec_path, 'r') as f:
            for line in f:
                if line.strip().startswith('name:'):
                    return line.split(':', 1)[1].strip().strip('"').strip("'")
    return project_dir.name


def validate_flutter_project(project_dir: Path) -> tuple[Path, str]:
    """Validate Flutter project and return lib_path and project_name"""
    if not (project_dir / "pubspec.yaml").exists():
        console.print("[bold red]❌ Not a valid Flutter project. pubspec.yaml not found.[/bold red]")
        sys.exit(1)
    
    lib_path = project_dir / "lib"
    if not lib_path.exists():
        console.print("[bold red]❌ lib directory not found.[/bold red]")
        sys.exit(1)
    
    return lib_path, get_project_name(project_dir)

