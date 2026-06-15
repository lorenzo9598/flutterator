"""Mock vs remote data source helpers — DataSourceConfig and mock JSON assets."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

from generators.templates.copier import generate_file

REMOTE_PATTERN = re.compile(
    r"['\"](?P<key>[a-z][a-z0-9_]*)['\"]\s*:\s*DataSource\.remote",
)


def scan_domain_entity_keys(lib_path: Path, domain_folder: str = "domain") -> list[str]:
    """Return snake_case entity keys that have a repository interface."""
    domain_root = lib_path / domain_folder
    if not domain_root.is_dir():
        return []
    keys: list[str] = []
    for entity_dir in sorted(domain_root.iterdir()):
        if not entity_dir.is_dir():
            continue
        i_repo = entity_dir / "model" / f"i_{entity_dir.name}_repository.dart"
        if i_repo.is_file():
            keys.append(entity_dir.name)
    return keys


def read_preserved_remote_keys(config_path: Path) -> set[str]:
    """Parse existing data_source_config.dart for entries already set to remote."""
    if not config_path.is_file():
        return set()
    content = config_path.read_text(encoding="utf-8")
    return {m.group("key") for m in REMOTE_PATTERN.finditer(content)}


def build_entities_map(
    entity_keys: list[str],
    *,
    has_login: bool,
    preserved_remote: set[str],
) -> dict[str, str]:
    """Build entity key -> 'mock' | 'remote' for template rendering."""
    entities: dict[str, str] = {}
    if has_login:
        entities["auth"] = "remote" if "auth" in preserved_remote else "mock"
    for key in entity_keys:
        if key in preserved_remote:
            entities[key] = "remote"
        else:
            entities[key] = "mock"
    return entities


def _format_entities_entries(entities: dict[str, str]) -> str:
    if not entities:
        return ""
    lines = []
    for key, source in entities.items():
        enum_val = "DataSource.mock" if source == "mock" else "DataSource.remote"
        lines.append(f"    '{key}': {enum_val},")
    return "\n".join(lines)


def regenerate_data_source_config(
    project_name: str,
    lib_path: Path,
    *,
    domain_folder: str = "domain",
    has_login: bool = False,
) -> None:
    """Regenerate lib/apis/common/data_source_config.dart from scanned entities."""
    config_rel = "apis/common/data_source_config.dart"
    config_path = lib_path / config_rel
    entity_keys = scan_domain_entity_keys(lib_path, domain_folder)
    preserved_remote = read_preserved_remote_keys(config_path)
    entities = build_entities_map(
        entity_keys,
        has_login=has_login,
        preserved_remote=preserved_remote,
    )
    generate_file(
        project_name,
        lib_path,
        "apis/common/data_source_config_template.jinja",
        config_rel,
        {
            "entities_entries": _format_entities_entries(entities),
            "login": has_login,
        },
    )


def ensure_mock_assets_dir(project_path: Path) -> Path:
    """Ensure assets/mock/ exists in the Flutter project root."""
    mock_dir = project_path / "assets" / "mock"
    mock_dir.mkdir(parents=True, exist_ok=True)
    return mock_dir


def _sample_value_for_type(
    field_name: str,
    field_type: str,
    index: int,
    *,
    known_enums: Optional[dict] = None,
) -> object:
    """Return a JSON-serializable sample value for a DTO field."""
    known_enums = known_enums or {}
    is_nullable = field_type.endswith("?")
    base = field_type[:-1] if is_nullable else field_type

    if field_name == "id":
        return str(index)

    base_lower = base.lower()
    if base_lower in ("string", "str"):
        return f"sample-{field_name}-{index}"
    if base_lower == "bool":
        return False
    if base_lower == "int":
        return index
    if base_lower in ("double", "num", "float"):
        return round(9.99 * index, 2)
    if base_lower in ("datetime", "date"):
        return "2024-01-15T10:00:00.000Z"

    if base in known_enums:
        values = known_enums[base].get("values") or []
        if values:
            return values[0]
        return "pending"

    if base.startswith("List<") or base.startswith("Set<"):
        inner = base[base.index("<") + 1 : base.rindex(">")]
        if inner in known_enums:
            vals = known_enums[inner].get("values") or []
            if vals:
                return [vals[0]]
        return []

    if base.startswith("Map<"):
        return {}

    if base[0].isupper() if base else False:
        return f"sample-{field_name}-{index}"

    return f"sample-{field_name}-{index}"


def generate_mock_json(
    project_path: Path,
    entity_folder_name: str,
    field_list: list[dict],
    *,
    known_enums: Optional[dict] = None,
    item_count: int = 3,
) -> Path:
    """Write assets/mock/<entity>.json with sample items."""
    mock_dir = ensure_mock_assets_dir(project_path)
    items = []
    for i in range(1, item_count + 1):
        item: dict[str, object] = {}
        for field in field_list:
            item[field["name"]] = _sample_value_for_type(
                field["name"],
                field["type"],
                i,
                known_enums=known_enums,
            )
        items.append(item)
    out_path = mock_dir / f"{entity_folder_name}.json"
    out_path.write_text(
        json.dumps({"items": items}, indent=2) + "\n",
        encoding="utf-8",
    )
    return out_path
