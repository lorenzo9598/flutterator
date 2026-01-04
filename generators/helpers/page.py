"""Page generation functions"""

import click
from pathlib import Path
from typing import Optional
from generators.templates.copier import generate_file


def generate_page_file(page_name: str, presentation_dir: Path, project_name: str) -> None:
    """Generate a basic page file using Jinja template"""
    generate_file(project_name, presentation_dir, "page_template.jinja", f"{page_name}_page.dart", {
        "page_name": page_name
    })


def update_router(project_dir: Path, page_name: str, project_name: str, folder: Optional[str] = None) -> None:
    """Update the router.dart file to include the new page"""
    router_path = project_dir / "lib" / "router.dart"
    if not router_path.exists():
        click.echo("⚠️ router.dart not found, skipping router update")
        return

    # Build the import path prefix
    if folder:
        import_prefix = f"{folder.replace('/', '/')}/{page_name}"
    else:
        import_prefix = page_name

    # Read current router
    content = router_path.read_text()
    
    # Add import
    import_line = f"import 'package:{project_name}/{import_prefix}/{page_name}_page.dart';"
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

