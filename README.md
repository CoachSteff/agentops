# AgentOps

Lightweight companion browser for developers who work with local AI agent services.

One minimal, native-feeling macOS window where you can centrally open, group, and view all your local agent services and web UIs — Craft Agents, Mission Control, Claude Code, n8n, your own tools — without the noise of a regular browser. It acts as an operational control center for your agents: fast switching between views, stable demo setups, and a vendor-agnostic workflow around everything you run locally.

## Why

- You already run several local services on different localhost ports
- Chrome tabs are noisy, distracting, and lose context
- You want something that feels like an app, not a browser

## Features (v0.1)

- **One window** with a slim sidebar — switch services without switching apps
- **Zero browser chrome** — no URL bar, no tabs, no back/forward clutter
- **Config-driven** — add any service in a single YAML file
- **Keyboard-first** — `Cmd+1..9` to switch services, `Cmd+R` to reload the active view
- **Remembers your last service** across sessions
- **Native macOS bundle** via PyInstaller (WKWebView under the hood)
- **Vendor agnostic** — works with any HTTP service that runs locally

## Install (macOS)

**Requirements:** macOS 13+, Python 3.12+

```bash
git clone https://github.com/CoachSteff/agentops.git
cd agentops
./install.sh
```

This creates a virtual env, builds `AgentOps.app` with PyInstaller, and copies it to `/Applications/`.

On first launch: **right-click → Open** to bypass Gatekeeper (app is not code-signed in v0.1).

## Dev run

No build step needed — just install the package in editable mode:

```bash
cd agentops
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
agentops
```

## Configure services

On first launch, AgentOps creates `~/.agentops/services.yaml` with a default config. Edit it to add your own services:

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

  - id: n8n
    name: n8n
    url: http://localhost:5678
    icon: n8n.svg

  - id: my-tool
    name: My Tool
    url: http://localhost:3000
    # icon omitted → shows a colored initial tile
```

**Restart AgentOps** after editing the config — it is read once at startup.

### Icons

Drop any SVG or PNG into `~/.agentops/icons/` and reference it by filename in the YAML. If you omit the icon, AgentOps shows a colored tile with the service's initial letter instead.

### Keyboard shortcuts

| Shortcut | Action |
|----------|--------|
| `Cmd+1` … `Cmd+9` | Switch to service 1–9 (in sidebar order) |
| `Cmd+R` | Reload the active service view |

## Limitations

- Services that set `X-Frame-Options: DENY` or a strict `Content-Security-Policy: frame-ancestors` cannot be embedded. For those, copy the URL and open it in your browser manually.
- macOS 13+ only. Windows and Linux support is planned for a future release.
- Not code-signed — Gatekeeper requires a one-time right-click → Open.

## Uninstall

```bash
./uninstall.sh            # removes /Applications/AgentOps.app
./uninstall.sh --purge    # also removes ~/.agentops/
```

## License

MIT — see [LICENSE](LICENSE).
