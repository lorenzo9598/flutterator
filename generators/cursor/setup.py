"""Copy and render Cursor ecosystem files into a newly created Flutter project."""

from __future__ import annotations

import shutil
from pathlib import Path

from jinja2 import Template

CURSOR_STATIC_DIR = Path(__file__).resolve().parent.parent / "static" / "cursor"

JINJA_KWARGS = {"variable_start_string": "[[", "variable_end_string": "]]"}


def _render_template_text(content: str, context: dict) -> str:
    template = Template(content, **JINJA_KWARGS)
    return template.render(**context)


def _render_file(src: Path, dest: Path, context: dict) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    rendered = _render_template_text(src.read_text(encoding="utf-8"), context)
    dest.write_text(rendered, encoding="utf-8")


def _copy_static_file(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def copy_cursor_ecosystem(project_path: Path, login: bool, project_name: str) -> None:
    """Render Cursor rules, agents, skills, docs, and AGENTS.md into the project."""
    if not CURSOR_STATIC_DIR.is_dir():
        raise FileNotFoundError(f"Cursor templates not found: {CURSOR_STATIC_DIR}")

    context = {
        "project_name": project_name,
        "login": login,
        "has_login": login,
    }
    root = project_path.resolve()

    rules_src = CURSOR_STATIC_DIR / "rules"
    for src in sorted(rules_src.glob("*.mdc.jinja")):
        if src.name == "login-context.mdc.jinja" and not login:
            continue
        dest_name = src.name.replace(".jinja", "")
        _render_file(src, root / ".cursor" / "rules" / dest_name, context)

    agents_src = CURSOR_STATIC_DIR / "agents"
    for src in sorted(agents_src.glob("*.md")):
        _copy_static_file(src, root / ".cursor" / "agents" / src.name)

    skill_root = CURSOR_STATIC_DIR / "skills" / "epic-delivery"
    skill_dest = root / ".cursor" / "skills" / "epic-delivery"
    for src in skill_root.rglob("*"):
        if src.is_dir():
            continue
        rel = src.relative_to(skill_root)
        dest = skill_dest / rel
        if src.suffix == ".jinja":
            _render_file(src, dest.with_suffix(""), context)
        else:
            _copy_static_file(src, dest)

    arch_src = CURSOR_STATIC_DIR / "docs" / "architecture"
    for src in sorted(arch_src.glob("*.md.jinja")):
        dest_name = src.name.replace(".jinja", "")
        _render_file(src, root / "docs" / "architecture" / dest_name, context)

    _render_file(
        CURSOR_STATIC_DIR / "AGENTS.md.jinja",
        root / "AGENTS.md",
        context,
    )

    for rel in ("lib/domain/AGENTS.md", "lib/features/AGENTS.md", "lib/widgets/AGENTS.md"):
        _copy_static_file(CURSOR_STATIC_DIR / rel, root / rel)

    _copy_static_file(CURSOR_STATIC_DIR / "docs" / "epics" / "README.md", root / "docs" / "epics" / "README.md")
    _copy_static_file(CURSOR_STATIC_DIR / "test" / "README.md", root / "test" / "README.md")
