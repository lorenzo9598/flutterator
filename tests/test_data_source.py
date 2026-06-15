"""Tests for mock vs remote data source helpers."""

import json
from pathlib import Path

import pytest

from generators.helpers.data_source import (
    build_entities_map,
    generate_mock_json,
    read_preserved_remote_keys,
    regenerate_data_source_config,
    scan_domain_entity_keys,
)


def test_scan_domain_entity_keys(tmp_path):
    lib = tmp_path / "lib" / "domain"
    task = lib / "task" / "model"
    task.mkdir(parents=True)
    (task / "i_task_repository.dart").write_text("// repo")
    note = lib / "note" / "model"
    note.mkdir(parents=True)
    (note / "i_note_repository.dart").write_text("// repo")

    keys = scan_domain_entity_keys(tmp_path / "lib", "domain")
    assert keys == ["note", "task"]


def test_read_preserved_remote_keys_tmp(tmp_path):
    config = tmp_path / "data_source_config.dart"
    config.write_text(
        "static const Map<String, DataSource> entities = {\n"
        "  'task': DataSource.remote,\n"
        "  'note': DataSource.mock,\n"
        "};\n"
    )
    preserved = read_preserved_remote_keys(config)
    assert preserved == {"task"}


def test_build_entities_map_preserves_remote():
    entities = build_entities_map(
        ["task", "note"],
        has_login=True,
        preserved_remote={"task"},
    )
    assert entities["auth"] == "mock"
    assert entities["task"] == "remote"
    assert entities["note"] == "mock"


def test_generate_mock_json(tmp_path):
    fields = [
        {"name": "id", "type": "string"},
        {"name": "title", "type": "string"},
        {"name": "done", "type": "bool"},
    ]
    out = generate_mock_json(tmp_path, "todo", fields)
    assert out == tmp_path / "assets" / "mock" / "todo.json"
    data = json.loads(out.read_text())
    assert len(data["items"]) == 3
    assert data["items"][0]["id"] == "1"
    assert data["items"][0]["title"] == "sample-title-1"
    assert data["items"][0]["done"] is False


def test_regenerate_data_source_config(tmp_path):
    lib = tmp_path / "lib"
    entity = lib / "domain" / "todo" / "model"
    entity.mkdir(parents=True)
    (entity / "i_todo_repository.dart").write_text("//")

    regenerate_data_source_config("my_app", lib, domain_folder="domain", has_login=False)
    config = (lib / "apis" / "common" / "data_source_config.dart").read_text()
    assert "'todo': DataSource.mock" in config
    assert "validateRemoteRequiresApiUrl" in config

    # Mark todo remote and regenerate — should preserve
    config_path = lib / "apis" / "common" / "data_source_config.dart"
    config_path.write_text(
        config_path.read_text().replace(
            "'todo': DataSource.mock",
            "'todo': DataSource.remote",
        )
    )
    regenerate_data_source_config("my_app", lib, domain_folder="domain", has_login=False)
    updated = config_path.read_text()
    assert "'todo': DataSource.remote" in updated
