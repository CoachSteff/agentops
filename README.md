# AgentOps

Lightweight companion browser for developers who work with local AI agent services.

One minimal, native-feeling macOS window where you can centrally open, group, and view all your local agent services and web UIs (Craft Agents, Claude Code, Mission Control, your own tools) — without the noise of a regular browser. It acts as an operational control center for your agents: fast switching between views, stable demo setups, and a vendor-agnostic workflow around everything you run locally.

## Why

- You already run several local services on different localhost ports
- Chrome tabs are noisy, distracting, and lose track
- You want something that feels like an app, not a browser

## Features (v0.1)

- **One window**, one configurable sidebar, one iframe-hosted service at a time
- **Zero browser chrome** — no URL bar, no tabs, no back/forward clutter
- **Config-driven** — add services via a single YAML file
- **Keyboard-first** — `Cmd+1..9` to switch services, `Cmd+R` to reload
- **Native macOS bundle** via PyInstaller (WKWebView under the hood)
- **Vendor agnostic** — any HTTP service that runs locally

## Install (macOS)

```bash
cd ~/Development/agentops
./install.sh
```

This creates a virtual env, builds `AgentOps.app` with PyInstaller, and copies it to `/Applications/`. First launch: right-click the app and choose "Open" to bypass Gatekeeper (not code-signed yet).

## Dev run

```bash
cd ~/Development/agentops
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[build]"
agentops
```

## Configure services

On first launch, AgentOps writes a default config to `~/.agentops/services.yaml`. Edit it to add your own services:

```yaml
version: 1

window:
  width: 1400
  height: 900

services:
  - id: mission-control
    name: Mission Control
    url: http://localhost:9753
    icon: mission-control.svg
    default: true

  - id: my-tool
    name: My Tool
    url: http://localhost:3000
    icon: default.svg
```

Reopen the app (or `Cmd+R` the view) and your service is in the sidebar.

## Limitations

- Services that set `X-Frame-Options: DENY` or strict `Content-Security-Policy: frame-ancestors` cannot be embedded. Use **View → Open in Browser** for those.
- macOS 13+ only. Windows and Linux builds are planned for a later release.

## License

MIT. See [LICENSE](LICENSE).
