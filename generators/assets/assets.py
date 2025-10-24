
# move assets folder with his contents to lib/assets 
import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent 
STATIC_DIR = BASE_DIR.parent / "static"

def move_assets_to_lib(project_name):
    flutter_name = project_name.lower().replace(" ", "_")
    project_path = Path(flutter_name)
    assets_src = STATIC_DIR / "assets"
    assets_dst = project_path / "assets"
    
    if not assets_src.exists():
        print(f"Source assets folder {assets_src} does not exist.")
        return
    
    # Create destination directory if it doesn't exist
    assets_dst.mkdir(parents=True, exist_ok=True)
    
    # Move all files from assets_src to assets_dst
    for item in assets_src.iterdir():
        dest = assets_dst / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)
    