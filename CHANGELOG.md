# Changelog

## 0.1.1 — 2026-04-24

- Added `TEST_PLAN.md` covering config, UI, iframe/overlay regressions, keyboard shortcuts, persistence, install, and packaged-bundle sanity
- Added `tests/test_config.py` — 14 pytest cases for config loading, bootstrap, validation, icon resolution, and state persistence
- Added `dev` optional dependency group in `pyproject.toml` (installs pytest)

## 0.1.0 — 2026-04-18

Initial release.

- One-window companion app for local agent services
- Sidebar with service icons, iframe-hosted main view
- YAML-driven config at `~/.agentops/services.yaml`
- Keyboard shortcuts: `Cmd+1..9` to switch, `Cmd+R` to reload
- macOS `.app` bundle via PyInstaller (WKWebView, pywebview Cocoa backend)
- "Open in Browser" fallback for services that refuse iframe embedding
