"""Tests for Cursor ecosystem generation at project create."""

from pathlib import Path

import pytest

from generators.cursor.setup import copy_cursor_ecosystem

EXPECTED_AGENTS = [
    "epic-orchestrator.md",
    "feature-implementer.md",
    "layer-model.md",
    "layer-infrastructure.md",
    "layer-application.md",
    "layer-presentation.md",
    "integration-wiring.md",
    "doc-writer.md",
    "layer-guardian.md",
]

EXPECTED_RULES = [
    "architecture-core.mdc",
    "dart-conventions.mdc",
    "domain-layer.mdc",
    "application-layer.mdc",
    "presentation-layer.mdc",
    "ui-caravaggio.mdc",
    "apis-layer.mdc",
    "quality-gate.mdc",
]

EXPECTED_ARCH_DOCS = [
    "DDD_LAYERS.md",
    "FILE_TEMPLATES.md",
    "WIDGETS_AND_CARAVAGGIO.md",
    "CARAVAGGIO_COMPONENTS.md",
    "MOCK_AND_REMOTE_DATA.md",
    "REFERENCE_IMPLEMENTATIONS.md",
    "APIS_AND_INTEGRATION.md",
]

EXPECTED_SKILLS = [
    "epic-delivery",
    "caravaggio-ui",
]


@pytest.fixture
def cursor_project(tmp_path):
    """Minimal project root for cursor setup."""
    project = tmp_path / "my_app"
    project.mkdir()
    (project / "pubspec.yaml").write_text("name: my_app\n")
    (project / "lib").mkdir()
    return project


def test_copy_cursor_ecosystem_default(cursor_project):
    copy_cursor_ecosystem(cursor_project, login=False, project_name="my_app")

    assert (cursor_project / "AGENTS.md").exists()
    assert "my_app" in (cursor_project / "AGENTS.md").read_text()
    assert "flutterator" in (cursor_project / "AGENTS.md").read_text().lower()
    assert "caravaggio-ui" in (cursor_project / "AGENTS.md").read_text()

    core_rule = (cursor_project / ".cursor/rules/architecture-core.mdc").read_text()
    assert "my_app" in core_rule
    assert "flutterator" in core_rule.lower()
    assert "Never run" in core_rule or "Never" in core_rule

    for rule in EXPECTED_RULES:
        assert (cursor_project / ".cursor/rules" / rule).exists()

    assert not (cursor_project / ".cursor/rules/login-context.mdc").exists()

    agents_dir = cursor_project / ".cursor/agents"
    assert agents_dir.is_dir()
    assert len(list(agents_dir.glob("*.md"))) == len(EXPECTED_AGENTS)
    for agent in EXPECTED_AGENTS:
        assert (agents_dir / agent).exists()

    for skill_name in EXPECTED_SKILLS:
        skill = cursor_project / ".cursor" / "skills" / skill_name / "SKILL.md"
        assert skill.exists(), f"Missing skill: {skill_name}"

    epic_skill = (cursor_project / ".cursor/skills/epic-delivery/SKILL.md").read_text()
    assert "small" in epic_skill
    assert "large" in epic_skill

    caravaggio_skill = (cursor_project / ".cursor/skills/caravaggio-ui/SKILL.md").read_text()
    assert "CustomScaffold" in caravaggio_skill
    assert "CARAVAGGIO_COMPONENTS.md" in caravaggio_skill

    for doc in EXPECTED_ARCH_DOCS:
        assert (cursor_project / "docs/architecture" / doc).exists()

    assert (cursor_project / "docs/epics/README.md").exists()
    assert not (cursor_project / "test/README.md").exists()
    assert (cursor_project / "lib/domain/AGENTS.md").exists()
    assert (cursor_project / "lib/features/AGENTS.md").exists()
    assert (cursor_project / "lib/widgets/AGENTS.md").exists()


def test_copy_cursor_ecosystem_with_login(cursor_project):
    copy_cursor_ecosystem(cursor_project, login=True, project_name="my_app")

    assert (cursor_project / ".cursor/rules/login-context.mdc").exists()
    ref_impl = (cursor_project / "docs/architecture/REFERENCE_IMPLEMENTATIONS.md").read_text()
    assert "auth" in ref_impl.lower()


def test_init_skips_cursor_when_disabled(cursor_project):
    """When cursor_setup=False, init must not call copy_cursor_ecosystem."""
    from unittest.mock import patch

    with patch("generators.main.run_cmd"), patch(
        "generators.main.initialize_project"
    ), patch("generators.main.load_config") as mock_cfg, patch(
        "generators.main.generate_files"
    ), patch(
        "generators.main.generate_config_files"
    ), patch(
        "generators.main.copy_assets"
    ), patch(
        "generators.cursor.copy_cursor_ecosystem"
    ) as mock_cursor:
        mock_cfg.return_value.primary_color = "#000000"
        mock_cfg.return_value.secondary_color = "#FFFFFF"
        from generators.main import init

        init("my_app", login=False, cursor_setup=False)
        mock_cursor.assert_not_called()


def test_widgets_doc_contains_caravaggio(cursor_project):
    copy_cursor_ecosystem(cursor_project, login=False, project_name="my_app")
    widgets_doc = (cursor_project / "docs/architecture/WIDGETS_AND_CARAVAGGIO.md").read_text()
    assert "caravaggio" in widgets_doc.lower()
    assert "widgets/common" in widgets_doc
    assert "CustomScaffold" in widgets_doc
    assert "CARAVAGGIO_COMPONENTS.md" in widgets_doc


def test_ui_caravaggio_rule_mentions_custom_scaffold(cursor_project):
    copy_cursor_ecosystem(cursor_project, login=False, project_name="my_app")
    rule = (cursor_project / ".cursor/rules/ui-caravaggio.mdc").read_text()
    assert "CustomScaffold" in rule
    assert "CARAVAGGIO_COMPONENTS.md" in rule


def test_caravaggio_components_catalog(cursor_project):
    copy_cursor_ecosystem(cursor_project, login=False, project_name="my_app")
    catalog = (cursor_project / "docs/architecture/CARAVAGGIO_COMPONENTS.md").read_text()
    assert "1.0.6" in catalog
    assert "CTile" in catalog
    assert "CLoader" in catalog
    assert "CustomScaffold" in catalog


def test_mock_and_remote_doc(cursor_project):
    copy_cursor_ecosystem(cursor_project, login=False, project_name="my_app")
    doc = (cursor_project / "docs/architecture/MOCK_AND_REMOTE_DATA.md").read_text()
    assert "DataSourceConfig" in doc
    assert "assets/mock" in doc
    infra = (cursor_project / ".cursor/agents/layer-infrastructure.md").read_text()
    assert "assets/mock" in infra
