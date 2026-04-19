# Roadmap

## v0.2

- **Reload on config change** — watch `~/.agentops/services.yaml` for changes and refresh the sidebar without restarting
- **Service status indicators** — show a dot in the sidebar when a service is unreachable (port not open)
- **Native menubar** — File (Open Config, Reload, Quit), View (Zoom In/Out, Open in Browser)
- **Deeplink support** — `agentops://open?service=mission-control` so external tools can switch the view programmatically

## v0.3

- **Windows and Linux builds** — cross-platform PyInstaller target; WKWebView (macOS), Edge WebView2 (Windows), WebKitGTK (Linux)
- **Service groups** — visual separators in the sidebar for grouping related services
- **Per-service window state** — remember scroll position and zoom level per service

## Later

- **Code signing and notarization** — remove the Gatekeeper right-click requirement
- **Auto-update** — check GitHub releases for a newer version on startup
- **Multi-window** — optional detached windows per service for multi-monitor setups
