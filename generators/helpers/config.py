"""Configuration management for Flutterator.

Supports configuration from multiple sources with priority:
1. CLI flags (highest priority)
2. Project-level flutterator.yaml
3. Global ~/.flutteratorrc
4. Default values (lowest priority)
"""

import os
from pathlib import Path
from typing import Any, Optional
from dataclasses import dataclass, field

import yaml
from rich.console import Console

console = Console()

# Default configuration values
DEFAULTS = {
    "feature_folder": "features",  # Default features folder
    "domain_folder": "domain",  # Domain entities folder
    "component_folder": "features/components",  # Default components folder
    "auto_run_build_runner": True,
    "primary_color": "#2196F3",
    "secondary_color": "#FF9800",
}

# Config file names
PROJECT_CONFIG_FILE = "flutterator.yaml"
GLOBAL_CONFIG_FILE = ".flutteratorrc"


@dataclass
class FlutteratorConfig:
    """Configuration class for Flutterator."""
    
    # Folder defaults
    feature_folder: str = "features"
    domain_folder: str = "domain"
    component_folder: str = "features/components"
    
    # Automation
    auto_run_build_runner: bool = True
    
    # UI/Styling
    primary_color: str = "#2196F3"
    secondary_color: str = "#FF9800"
    
    # Custom templates (optional paths)
    custom_templates: dict = field(default_factory=dict)
    
    # Extra dependencies to add
    extra_dependencies: list = field(default_factory=list)
    
    # Source of config (for debugging)
    _source: str = "defaults"
    
    @classmethod
    def from_dict(cls, data: dict, source: str = "unknown") -> "FlutteratorConfig":
        """Create config from dictionary."""
        config = cls()
        
        # Map nested 'defaults' section
        if "defaults" in data:
            defaults = data["defaults"]
            if "feature_folder" in defaults:
                config.feature_folder = defaults["feature_folder"]
            if "domain_folder" in defaults:
                config.domain_folder = defaults["domain_folder"]
            if "component_folder" in defaults:
                config.component_folder = defaults["component_folder"]
            if "auto_run_build_runner" in defaults:
                config.auto_run_build_runner = defaults["auto_run_build_runner"]
        
        # Map 'styling' section
        if "styling" in data:
            styling = data["styling"]
            if "primary_color" in styling:
                config.primary_color = styling["primary_color"]
            if "secondary_color" in styling:
                config.secondary_color = styling["secondary_color"]
        
        # Map 'templates' section
        if "templates" in data:
            config.custom_templates = data["templates"]
        
        # Map 'dependencies' section
        if "dependencies" in data:
            config.extra_dependencies = data["dependencies"]
        
        # Also support flat structure (for simple configs)
        for key in ["feature_folder", "domain_folder", "component_folder", 
                    "auto_run_build_runner",
                    "primary_color", "secondary_color"]:
            if key in data:
                setattr(config, key, data[key])
        
        config._source = source
        return config
    
    def merge_with(self, other: "FlutteratorConfig") -> "FlutteratorConfig":
        """Merge this config with another, other takes precedence for non-default values."""
        result = FlutteratorConfig()
        
        # Feature folder: use other's if set (default is "features")
        result.feature_folder = other.feature_folder if other.feature_folder != "features" else self.feature_folder
        
        # Component folder: use other's if set (default is "features/components")
        result.component_folder = other.component_folder if other.component_folder != "features/components" else self.component_folder
        
        # Domain folder has default "domain", so use other's if set
        result.domain_folder = other.domain_folder if other.domain_folder != "domain" else self.domain_folder
        
        # Automation: use other's value (it's explicitly set)
        result.auto_run_build_runner = other.auto_run_build_runner
        
        for key in ["primary_color", "secondary_color"]:
            setattr(result, key, getattr(other, key))
        
        # Merge dictionaries and lists
        result.custom_templates = {**self.custom_templates, **other.custom_templates}
        result.extra_dependencies = self.extra_dependencies + other.extra_dependencies
        
        result._source = f"{self._source} + {other._source}"
        return result


def load_yaml_file(path: Path) -> Optional[dict]:
    """Load a YAML file, return None if not found or invalid."""
    if not path.exists():
        return None
    
    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        console.print(f"[yellow]⚠️  Warning: Invalid YAML in {path}: {e}[/yellow]")
        return None
    except Exception as e:
        console.print(f"[yellow]⚠️  Warning: Could not read {path}: {e}[/yellow]")
        return None


def get_global_config_path() -> Path:
    """Get path to global config file."""
    return Path.home() / GLOBAL_CONFIG_FILE


def get_project_config_path(project_dir: Path) -> Path:
    """Get path to project config file."""
    return project_dir / PROJECT_CONFIG_FILE


def load_config(project_dir: Optional[Path] = None) -> FlutteratorConfig:
    """
    Load configuration from all sources with proper priority.
    
    Priority (highest to lowest):
    1. CLI flags (handled by caller)
    2. Project-level flutterator.yaml
    3. Global ~/.flutteratorrc
    4. Default values
    """
    # Start with defaults
    config = FlutteratorConfig(_source="defaults")
    
    # Load global config
    global_path = get_global_config_path()
    global_data = load_yaml_file(global_path)
    if global_data:
        global_config = FlutteratorConfig.from_dict(global_data, f"~/{GLOBAL_CONFIG_FILE}")
        config = config.merge_with(global_config)
    
    # Load project config (if project_dir provided)
    if project_dir:
        project_path = get_project_config_path(project_dir)
        project_data = load_yaml_file(project_path)
        if project_data:
            project_config = FlutteratorConfig.from_dict(project_data, PROJECT_CONFIG_FILE)
            config = config.merge_with(project_config)
    
    return config


def apply_cli_overrides(config: FlutteratorConfig, **cli_args) -> FlutteratorConfig:
    """
    Apply CLI argument overrides to config.
    Only non-None CLI args override config values.
    """
    if cli_args.get("folder"):
        config.feature_folder = cli_args["folder"]
        config.component_folder = cli_args["folder"]
    
    if cli_args.get("no_build") is True:
        config.auto_run_build_runner = False
    
    return config


def create_default_config(project_dir: Path, project_name: str) -> Path:
    """Create a default flutterator.yaml in the project directory."""
    config_path = project_dir / PROJECT_CONFIG_FILE
    
    default_config = f"""# Flutterator Configuration
# Project: {project_name}
# Documentation: https://github.com/lorenzobusi/flutterator

# Default folders for generated code
defaults:
  feature_folder: "features"         # Features folder
  domain_folder: "domain"           # Domain entities folder (shared entities)
  component_folder: "features/components"  # Components folder
  auto_run_build_runner: true       # Run build_runner after generation

# UI/Styling configuration
styling:
  primary_color: "#2196F3"
  secondary_color: "#FF9800"

# Custom templates (optional)
# templates:
#   entity: "templates/custom_entity.jinja"
#   bloc: "templates/custom_bloc.jinja"

# Additional dependencies to include (optional)
# dependencies:
#   - package: dartz
#     version: ^0.10.1
"""
    
    with open(config_path, 'w') as f:
        f.write(default_config)
    
    return config_path


def show_config(config: FlutteratorConfig) -> None:
    """Display current configuration using rich."""
    from rich.table import Table
    from rich.panel import Panel
    
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Setting", style="dim")
    table.add_column("Value")
    
    table.add_row("Feature Folder", config.feature_folder)
    table.add_row("Domain Folder", config.domain_folder)
    table.add_row("Component Folder", config.component_folder)
    table.add_row("Auto Build Runner", "✅" if config.auto_run_build_runner else "❌")
    table.add_row("Primary Color", config.primary_color)
    table.add_row("Secondary Color", config.secondary_color)
    
    console.print(Panel(table, title=f"⚙️  Configuration ({config._source})", border_style="blue"))
