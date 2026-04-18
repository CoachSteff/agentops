from __future__ import annotations

import shutil
from pathlib import Path

import yaml
from pydantic import BaseModel, Field, field_validator

from agentops.paths import CONFIG_FILE, ICONS_DIR, USER_DIR, default


class Service(BaseModel):
    id: str
    name: str
    url: str
    icon: str | None = None
    default: bool = False

    @field_validator("id")
    @classmethod
    def _id_slug(cls, v: str) -> str:
        v = v.strip()
        if not v or any(c.isspace() for c in v):
            raise ValueError("service id must be a non-empty slug without whitespace")
        return v


class Window(BaseModel):
    width: int = 1400
    height: int = 900
    min_width: int = 900
    min_height: int = 600
    remember_size: bool = True


class AgentOpsConfig(BaseModel):
    version: int = 1
    window: Window = Field(default_factory=Window)
    services: list[Service] = Field(default_factory=list)

    @field_validator("services")
    @classmethod
    def _unique_ids(cls, v: list[Service]) -> list[Service]:
        ids = [s.id for s in v]
        if len(ids) != len(set(ids)):
            raise ValueError("service ids must be unique")
        return v


def bootstrap_user_dir() -> None:
    """Copy default config + icons to ~/.agentops/ on first run."""
    USER_DIR.mkdir(parents=True, exist_ok=True)
    ICONS_DIR.mkdir(parents=True, exist_ok=True)

    if not CONFIG_FILE.exists():
        src = default("services.yaml")
        if src.exists():
            shutil.copy(src, CONFIG_FILE)

    default_icons = default("icons")
    if default_icons.exists():
        for icon in default_icons.iterdir():
            target = ICONS_DIR / icon.name
            if not target.exists():
                shutil.copy(icon, target)


def load_config() -> AgentOpsConfig:
    bootstrap_user_dir()
    with CONFIG_FILE.open("r") as f:
        raw = yaml.safe_load(f) or {}
    return AgentOpsConfig.model_validate(raw)


def resolve_icon(icon: str | None) -> Path | None:
    """Turn a config icon reference into an absolute path, or None."""
    if not icon:
        return None
    p = Path(icon).expanduser()
    if p.is_absolute() and p.exists():
        return p
    candidate = ICONS_DIR / icon
    if candidate.exists():
        return candidate
    return None
