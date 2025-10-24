from pathlib import Path
from string import Template


BASE_DIR = Path(__file__).parent  
TEMPLATE_DIR = BASE_DIR.parent / "static" / "templates"

def generate_file(project_name: str, lib_path: Path, template_name: str, output_path: str, args: dict = None):
    template_content = (TEMPLATE_DIR / template_name).read_text()
    template = Template(template_content)
    
    # Prepare variables for substitution
    template_vars = {"project_name": project_name}
    if args:
        template_vars.update(args)
    
    content = template.substitute(**template_vars)
    (lib_path / output_path).write_text(content)