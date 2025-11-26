#!/usr/bin/env python3
import os
import re
from pathlib import Path

def update_template_references(content):
    """Update template file references from .dart to .jinja"""
    # Replace template file references in generate_file calls
    content = re.sub(r'(".*?_template)\.dart(")', r'\1.jinja\2', content)
    return content

def main():
    generators_dir = Path("/Users/lorenzobusi/development/flutterator/generators")

    for py_file in generators_dir.rglob("*.py"):
        print(f"Updating {py_file}")

        # Read the content
        content = py_file.read_text()

        # Update template references
        updated_content = update_template_references(content)

        # Write back if changed
        if updated_content != content:
            py_file.write_text(updated_content)
            print(f"Updated {py_file}")
        else:
            print(f"No changes needed for {py_file}")

if __name__ == "__main__":
    main()
