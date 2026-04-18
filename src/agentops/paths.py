"""Path helpers for dev and PyInstaller-frozen runtime."""
from __future__ import annotations

import sys
from pathlib import Path

USER_DIR = Path.home() / ".agentops"
CONFIG_FILE = USER_DIR / "services.yaml"
ICONS_DIR = USER_DIR / "icons"
STATE_FILE = USER_DIR / "state.json"


def resource_root() -> Path:
    """Directory containing bundled assets (dev: src/agentops, frozen: _MEIPASS/agentops)."""
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / "agentops"  # type: ignore[attr-defined]
    return Path(__file__).resolve().parent


def asset(*parts: str) -> Path:
    return resource_root().joinpath("assets", *parts)


def default(*parts: str) -> Path:
    return resource_root().joinpath("defaults", *parts)
