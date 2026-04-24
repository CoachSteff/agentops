"""Section A (config + bootstrap) and E2 (corrupt state) of TEST_PLAN.md."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from agentops import config as config_mod
from agentops import paths as paths_mod
from agentops.config import (
    AgentOpsConfig,
    Service,
    bootstrap_user_dir,
    load_config,
    resolve_icon,
)


@pytest.fixture
def fake_home(tmp_path, monkeypatch):
    """Redirect USER_DIR and derived paths into a temp dir for isolation."""
    user_dir = tmp_path / ".agentops"
    config_file = user_dir / "services.yaml"
    icons_dir = user_dir / "icons"
    state_file = user_dir / "state.json"

    for name, value in [
        ("USER_DIR", user_dir),
        ("CONFIG_FILE", config_file),
        ("ICONS_DIR", icons_dir),
        ("STATE_FILE", state_file),
    ]:
        monkeypatch.setattr(paths_mod, name, value)

    for name in ("USER_DIR", "CONFIG_FILE", "ICONS_DIR"):
        monkeypatch.setattr(config_mod, name, locals()[name.lower() if name != "USER_DIR" else "user_dir"])

    return user_dir


def _write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data))


# A1 — first launch creates dir, copies default yaml + icons, loads config
def test_a1_first_launch_bootstrap(fake_home):
    cfg = load_config()

    assert fake_home.exists()
    assert (fake_home / "services.yaml").exists()
    assert (fake_home / "icons").exists()
    assert isinstance(cfg, AgentOpsConfig)
    assert cfg.services, "default config should have at least one service"


# A2 — second launch does not overwrite existing yaml or icons
def test_a2_second_launch_preserves_user_edits(fake_home):
    bootstrap_user_dir()
    user_yaml = fake_home / "services.yaml"
    user_yaml.write_text("version: 1\nservices: []\n")
    custom_icon = fake_home / "icons" / "custom.svg"
    custom_icon.write_text("<svg/>")

    bootstrap_user_dir()

    assert user_yaml.read_text() == "version: 1\nservices: []\n"
    assert custom_icon.read_text() == "<svg/>"


# A3 — malformed YAML raises, does not silently pass
def test_a3_malformed_yaml_raises(fake_home):
    bootstrap_user_dir()
    (fake_home / "services.yaml").write_text("version: 1\nservices: [unclosed")

    with pytest.raises(yaml.YAMLError):
        load_config()


# A4 — duplicate service ids rejected
def test_a4_duplicate_ids_rejected():
    with pytest.raises(ValidationError, match="unique"):
        AgentOpsConfig(
            services=[
                Service(id="a", name="A", url="http://x"),
                Service(id="a", name="A2", url="http://y"),
            ]
        )


# A5 — whitespace in id rejected
def test_a5_whitespace_id_rejected():
    with pytest.raises(ValidationError):
        Service(id="has space", name="x", url="http://x")


def test_a5_empty_id_rejected():
    with pytest.raises(ValidationError):
        Service(id="", name="x", url="http://x")


# A6 — empty services list is valid
def test_a6_empty_services_allowed(fake_home):
    bootstrap_user_dir()
    _write_yaml(fake_home / "services.yaml", {"version": 1, "services": []})

    cfg = load_config()
    assert cfg.services == []


# A7 — missing icon resolves to None
def test_a7_missing_icon_returns_none(fake_home):
    bootstrap_user_dir()
    assert resolve_icon("does-not-exist.svg") is None


# A8 — absolute icon path is resolved as-is when it exists
def test_a8_absolute_icon_path(tmp_path, fake_home):
    icon = tmp_path / "my-icon.svg"
    icon.write_text("<svg/>")
    assert resolve_icon(str(icon)) == icon


def test_a8_absolute_icon_path_missing_returns_none(tmp_path, fake_home):
    assert resolve_icon(str(tmp_path / "nope.svg")) is None


# A9 — window defaults when omitted
def test_a9_window_defaults():
    cfg = AgentOpsConfig()
    assert cfg.window.width == 1400
    assert cfg.window.height == 900
    assert cfg.window.min_width == 900
    assert cfg.window.min_height == 600


def test_a9_window_defaults_from_yaml(fake_home):
    bootstrap_user_dir()
    _write_yaml(
        fake_home / "services.yaml",
        {"version": 1, "services": [{"id": "x", "name": "X", "url": "http://x"}]},
    )
    cfg = load_config()
    assert cfg.window.width == 1400
    assert cfg.window.height == 900


# E2 — corrupt state.json is tolerated by JsApi.get_last_service
def test_e2_corrupt_state_returns_none(fake_home, monkeypatch):
    from agentops import app as app_mod

    monkeypatch.setattr(app_mod, "STATE_FILE", fake_home / "state.json")
    fake_home.mkdir(exist_ok=True)
    (fake_home / "state.json").write_text("{ not valid json")

    api = app_mod.JsApi(AgentOpsConfig())
    assert api.get_last_service() is None


def test_e2_state_roundtrip(fake_home, monkeypatch):
    from agentops import app as app_mod

    monkeypatch.setattr(app_mod, "STATE_FILE", fake_home / "state.json")
    api = app_mod.JsApi(AgentOpsConfig())

    api.select_service("mission-control")
    assert api.get_last_service() == "mission-control"

    # overwrite
    api.select_service("n8n")
    assert api.get_last_service() == "n8n"
    assert json.loads((fake_home / "state.json").read_text()) == {"last_service": "n8n"}
