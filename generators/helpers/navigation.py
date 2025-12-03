"""Navigation functions (drawer and bottom navigation)"""

import click
from pathlib import Path
from generators.templates.copier import generate_file
from .project import get_project_name
from .page import generate_page_file, update_router


def create_drawer_page(project_dir: Path, drawer_item_name: str, project_name: str) -> None:
    """Create a page for the drawer item"""
    lib_path = project_dir / "lib"
    
    # Create page directory structure
    page_dir = lib_path / drawer_item_name
    page_dir.mkdir(exist_ok=True)
    
    # Create presentation layer
    presentation_dir = page_dir / "presentation"
    presentation_dir.mkdir(exist_ok=True)
    
    # Generate page file
    generate_page_file(drawer_item_name, presentation_dir, project_name)
    
    # Update router
    update_router(project_dir, drawer_item_name, project_name)


def update_home_screen_with_drawer(project_dir: Path, project_name: str) -> None:
    """Update the home screen to include a drawer"""
    home_screen_path = project_dir / "lib" / "home" / "presentation" / "home_screen.dart"
    
    if not home_screen_path.exists():
        click.echo("⚠️ Home screen not found, creating basic drawer implementation")
        return
    
    content = home_screen_path.read_text()
    
    # Check if drawer is already implemented
    if "drawer:" in content:
        click.echo("ℹ️ Drawer already exists in home screen")
        return
    
    # Add drawer import if not present
    drawer_import = f"import 'package:{project_name}/core/presentation/app_drawer.dart';"
    if drawer_import not in content:
        # Add import after existing imports
        lines = content.split('\n')
        insert_index = 0
        for i, line in enumerate(lines):
            if line.startswith('import'):
                insert_index = i + 1
            elif line.strip() and not line.startswith('//'):
                break
        
        lines.insert(insert_index, drawer_import)
        content = '\n'.join(lines)
    
    # Modify the Scaffold to include drawer
    if "return const Scaffold(" in content:
        content = content.replace(
            "return const Scaffold(",
            "return Scaffold(\n      drawer: const AppDrawer(),"
        )
    elif "return Scaffold(" in content:
        if "drawer:" not in content:
            content = content.replace(
                "return Scaffold(",
                "return Scaffold(\n      drawer: const AppDrawer(),"
            )
    
    home_screen_path.write_text(content)


def create_drawer_widget(project_dir: Path, drawer_item_name: str, project_name: str) -> None:
    """Create or update the drawer widget using Jinja template"""
    core_presentation_dir = project_dir / "lib" / "core" / "presentation"
    core_presentation_dir.mkdir(parents=True, exist_ok=True)
    
    drawer_path = core_presentation_dir / "app_drawer.dart"
    
    # Get all drawer items
    drawer_items = []
    
    if drawer_path.exists():
        content = drawer_path.read_text()
        lines = content.split('\n')
        
        for line in lines:
            if f'package:{project_name}/' in line and '_page.dart' in line:
                import_match = line.strip()
                if import_match.startswith("import 'package:") and import_match.endswith("_page.dart';"):
                    start = import_match.find(f'package:{project_name}/') + len(f'package:{project_name}/')
                    end = import_match.find('/presentation/', start)
                    if start != -1 and end != -1:
                        existing_item = import_match[start:end]
                        if existing_item != 'home':
                            drawer_items.append({"name": existing_item})
    
    if not any(item["name"] == drawer_item_name for item in drawer_items):
        drawer_items.append({"name": drawer_item_name})
    
    generate_file(project_name, core_presentation_dir, "core/presentation/app_drawer_template.jinja", "app_drawer.dart", {
        "project_name": project_name,
        "drawer_items": drawer_items
    })


def update_router_for_drawer_item(project_dir: Path, drawer_item_name: str) -> None:
    """Update router to include the drawer item route if needed"""
    router_path = project_dir / "lib" / "router.dart"
    
    if not router_path.exists():
        click.echo("⚠️ router.dart not found, skipping router update")
        return
    
    content = router_path.read_text()
    
    route_pattern = f"path: '/{drawer_item_name}'"
    if route_pattern in content:
        click.echo("ℹ️ Route already exists in router")
        return
    
    route_line = f"""GoRoute(
      path: '/{drawer_item_name}',
      builder: (BuildContext context, GoRouterState state) => const Placeholder(),
    ),"""
    
    if route_line not in content:
        if 'routes: <RouteBase>[' in content:
            content = content.replace('  ],', f'    {route_line}\n  ],')
        elif 'routes: [' in content:
            content = content.replace('  ],', f'    {route_line}\n  ],')
        else:
            click.echo("⚠️ Could not find routes list in router.dart")
    
    router_path.write_text(content)


def create_bottom_nav_page(project_dir: Path, bottom_nav_item_name: str) -> None:
    """Create a screen for the bottom nav item in home/presentation using Jinja template"""
    home_presentation_dir = project_dir / "lib" / "home" / "presentation"
    home_presentation_dir.mkdir(parents=True, exist_ok=True)
    
    project_name = get_project_name(project_dir)
    
    generate_file(project_name, home_presentation_dir, "home/screen_template.jinja", f"{bottom_nav_item_name}_screen.dart", {
        "screen_name": bottom_nav_item_name.capitalize(),
        "screen_title": bottom_nav_item_name.replace("_", " ").capitalize()
    })


def update_home_screen_with_bottom_nav(project_dir: Path, bottom_nav_item_name: str, project_name: str) -> None:
    """Update the home screen to include bottom navigation"""
    home_screen_path = project_dir / "lib" / "home" / "presentation" / "home_screen.dart"
    
    if not home_screen_path.exists():
        click.echo("⚠️ Home screen not found, creating basic bottom nav implementation")
        return
    
    content = home_screen_path.read_text()
    
    if "BottomNavigationBar" in content or "BottomNavBar" in content:
        class_name = bottom_nav_item_name.capitalize() + 'Screen'
        
        screen_import = f"import 'package:{project_name}/home/presentation/{bottom_nav_item_name}_screen.dart';"
        if screen_import not in content:
            lines = content.split('\n')
            insert_index = 0
            for i, line in enumerate(lines):
                if line.startswith('import'):
                    insert_index = i + 1
                elif line.strip() and not line.startswith('//'):
                    break
            
            lines.insert(insert_index, screen_import)
            content = '\n'.join(lines)
        
        lines = content.split('\n')
        pages_list_start = -1
        for i, line in enumerate(lines):
            if 'final List<Widget> _pages = [' in line or '_pages = [' in line:
                pages_list_start = i
                break
        
        if pages_list_start != -1:
            bracket_count = 0
            for j in range(pages_list_start, len(lines)):
                bracket_count += lines[j].count('[')
                bracket_count -= lines[j].count(']')
                if bracket_count == 0 and '];' in lines[j]:
                    lines.insert(j, f'    const {class_name}(),')
                    break
            
            content = '\n'.join(lines)
    else:
        capitalized_name = bottom_nav_item_name.replace('_', ' ').title()
        class_name = bottom_nav_item_name.capitalize() + 'Screen'
        
        existing_content = home_screen_path.read_text()
        has_drawer = "drawer:" in existing_content
        drawer_import_needed = "import 'package:" + project_name + "/core/presentation/app_drawer.dart';" in existing_content
        
        imports = f"""import 'package:flutter/material.dart';
import 'package:{project_name}/core/presentation/bottom_nav_bar.dart';
import 'package:{project_name}/home/presentation/{bottom_nav_item_name}_screen.dart';"""
        
        if drawer_import_needed:
            imports += f"\nimport 'package:{project_name}/core/presentation/app_drawer.dart';"
        
        drawer_line = ""
        if has_drawer:
            drawer_line = "      drawer: const AppDrawer(),"
        
        content = f"""{imports}

class HomeScreen extends StatefulWidget {{
  static const String routeName = '/home';

  const HomeScreen({{super.key}});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}}

class _HomeScreenState extends State<HomeScreen> {{
  int _selectedIndex = 0;
  
  final List<Widget> _pages = [
    const Center(child: Text('Home Content')),
    const {class_name}(),
  ];
  
  void _onItemTapped(int index) {{
    setState(() {{
      _selectedIndex = index;
    }});
  }}

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(
        title: const Text('Home'),
      ),
{drawer_line}
      body: _pages[_selectedIndex],
      bottomNavigationBar: BottomNavBar(
        currentIndex: _selectedIndex,
        onTap: _onItemTapped,
      ),
    );
  }}
}}
"""
    
    home_screen_path.write_text(content)


def create_bottom_nav_widget(project_dir: Path, bottom_nav_item_name: str) -> None:
    """Create or update the bottom navigation widget using Jinja template"""
    core_presentation_dir = project_dir / "lib" / "core" / "presentation"
    core_presentation_dir.mkdir(parents=True, exist_ok=True)
    
    bottom_nav_path = core_presentation_dir / "bottom_nav_bar.dart"
    
    project_name = project_dir.name
    
    nav_items = [{"name": bottom_nav_item_name}]
    
    generate_file(project_name, core_presentation_dir, "core/presentation/bottom_nav_bar_template.jinja", "bottom_nav_bar.dart", {
        "nav_items": nav_items
    })

