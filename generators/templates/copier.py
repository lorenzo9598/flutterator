from pathlib import Path
from jinja2 import Template


BASE_DIR = Path(__file__).parent  
TEMPLATE_DIR = BASE_DIR.parent / "static" / "templates"

def hex_to_dart_color(hex_color: str) -> str:
    """
    Convert hex color string to Dart Color object.
    
    Args:
        hex_color: Hex color string (e.g., "#2196F3" or "2196F3")
    
    Returns:
        Dart Color string (e.g., "Color(0xFF2196F3)")
    """
    # Remove # if present
    hex_color = hex_color.lstrip('#')
    
    # Ensure it's 6 characters
    if len(hex_color) != 6:
        # Default to blue if invalid
        hex_color = "2196F3"
    
    # Convert to uppercase for consistency
    hex_color = hex_color.upper()
    
    # Return Dart Color format
    return f"Color(0xFF{hex_color})"

def generate_file(project_name: str, lib_path: Path, template_name: str, output_path: str, args: dict = None):
    template_content = (TEMPLATE_DIR / template_name).read_text()
    
    # Use custom delimiters to avoid conflicts with Dart string interpolation
    template = Template(template_content, variable_start_string='[[', variable_end_string=']]')
    
    # Prepare variables for substitution
    template_vars = {"project_name": project_name, "feature_name": args.get("feature_name", "") if args else ""}
    if args:
        template_vars.update(args)
    
    # Add special variables for complex expressions
    template_vars.update({
        "err_response_statusMessage": "err.response?.statusMessage",
    })
    
    content = template.render(**template_vars)
    (lib_path / output_path).write_text(content)