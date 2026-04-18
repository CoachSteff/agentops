from __future__ import annotations

import base64
import json
import mimetypes
import webbrowser
from pathlib import Path

import webview

from agentops.config import AgentOpsConfig, load_config, resolve_icon
from agentops.paths import STATE_FILE, asset


def _to_data_uri(path: Path) -> str:
    mime, _ = mimetypes.guess_type(str(path))
    if not mime:
        mime = "image/svg+xml" if path.suffix.lower() == ".svg" else "application/octet-stream"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


class JsApi:
    def __init__(self, config: AgentOpsConfig) -> None:
        self.config = config

    def list_services(self) -> list[dict]:
        out = []
        for s in self.config.services:
            p = resolve_icon(s.icon)
            out.append(
                {
                    "id": s.id,
                    "name": s.name,
                    "url": s.url,
                    "default": s.default,
                    "icon_url": _to_data_uri(p) if p else None,
                }
            )
        return out

    def select_service(self, service_id: str) -> dict:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(json.dumps({"last_service": service_id}))
        return {"ok": True}

    def get_last_service(self) -> str | None:
        if not STATE_FILE.exists():
            return None
        try:
            return json.loads(STATE_FILE.read_text()).get("last_service")
        except (json.JSONDecodeError, OSError):
            return None

    def open_in_browser(self, url: str) -> None:
        webbrowser.open(url)


def launch() -> None:
    config = load_config()
    api = JsApi(config)
    shell = asset("shell.html")
    webview.create_window(
        title="AgentOps",
        url=str(shell),
        js_api=api,
        width=config.window.width,
        height=config.window.height,
        min_size=(config.window.min_width, config.window.min_height),
    )
    webview.start()
