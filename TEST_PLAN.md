# AgentOps v0.1 — Test Plan

Test plan for `main` @ `920aecd`. Python 3.12+, macOS 13+, pywebview + WKWebView.

## Scope

**In scope:** config loading, first-run bootstrap, icon resolution, sidebar render, service switching, iframe embedding, `[hidden]` overlay behavior (regression area for commit `7fa9828`), keyboard shortcuts, last-service persistence, install/uninstall scripts, PyInstaller bundle.

**Out of scope:** deeplinks, config hot-reload, status indicators, cross-platform — those are v0.2 / v0.3 per ROADMAP.

## Risk map

| Area | Why risky |
|---|---|
| `shell.js` iframe + overlays | Recent `[hidden]` fix — regression candidate |
| `config.py` YAML validation | User-edited file, pydantic errors could crash startup silently |
| `bootstrap_user_dir` on first run | File-system writes, runs every launch |
| PyInstaller bundle | Assets + default icons must resolve inside the `.app` |
| Gatekeeper / unsigned bundle | First-launch friction for new users |
| `X-Frame-Options` / CSP sites | Documented limitation; must fail gracefully, not silently blank |

## Tests

### A — Config loading & bootstrap *(automated, pytest)*

| ID | Case | Expected |
|---|---|---|
| A1 | First launch, no `~/.agentops/` | Dir + default YAML + default icons created; app opens on default service |
| A2 | Second launch, config present | Existing YAML and icons untouched |
| A3 | Malformed YAML | Clean error surfaced, not silent blank window |
| A4 | Duplicate service id | Rejected by `_unique_ids` validator |
| A5 | Service id with whitespace | Rejected by `_id_slug` validator |
| A6 | `services: []` | App opens to empty-state panel, no JS errors |
| A7 | Icon refers to missing file | `resolve_icon` returns `None` → initial-letter tile |
| A8 | Icon is an absolute path that exists | Path resolved as-is |
| A9 | Window size omitted | Defaults 1400×900 / min 900×600 applied |

### B — Sidebar & service switching *(manual)*

- **B1** Sidebar renders one button per service, in YAML order.
- **B2** Default service highlighted and loaded on startup.
- **B3** Click a service → iframe loads, title updates to `AgentOps — <name>`, active state moves.
- **B4** Hover a sidebar button → tooltip shows name + `(⌘N)`.
- **B5** Service with no icon shows a colored initial-letter tile.
- **B6** Long service name doesn't break sidebar layout.

### C — Iframe & overlays *(manual — regression around commit `7fa9828`)*

- **C1** Empty-state → first service: empty-state hides, iframe visible and interactive.
- **C2** Rapid switching between services: only one iframe visible, no ghost overlay catching clicks.
- **C3** Mouse events reach iframe content (click nodes in n8n, type in a form).
- **C4** Frame-error panel stays hidden on successful load.
- **C5** Attempt to embed a `X-Frame-Options: DENY` site (e.g. github.com): iframe may blank, but "Open in Browser" still works; no stacked overlay intercepting clicks.

### D — Keyboard shortcuts *(manual)*

- **D1** `Cmd+1` … `Cmd+N` switches to service at that index (N = min(services, 9)).
- **D2** `Cmd+<beyond list>` is a no-op, no console error.
- **D3** `Cmd+R` reloads the active iframe.
- **D4** `Cmd+R` with no active service does nothing, no error.
- **D5** Shortcuts with focus inside the iframe — document the behavior (known pywebview quirk).

### E — Persistence *(E1, E3 manual — E2 automated)*

- **E1** Select a non-default service → quit → relaunch → that service is selected.
- **E2** Corrupt `state.json` → `get_last_service` returns `None`, app falls back to default.
- **E3** Last-selected service removed from config → falls back to default or first service.

### F — Install / uninstall *(manual, run once on a clean environment)*

- **F1** `./install.sh` on a clean machine → venv created, PyInstaller runs, `AgentOps.app` in `/Applications/`.
- **F2** Re-run `./install.sh` → overwrites cleanly, no stale artifacts.
- **F3** First launch of `.app` → Gatekeeper warning appears; right-click → Open works; README instruction is accurate.
- **F4** `./uninstall.sh` → removes `/Applications/AgentOps.app`, leaves `~/.agentops/` alone.
- **F5** `./uninstall.sh --purge` → also removes `~/.agentops/`.

### G — Packaged bundle sanity *(manual)*

- **G1** Bundled `.app` resolves `shell.html`, `shell.js`, `shell.css`, default icons.
- **G2** `~/.agentops/services.yaml` is created on first run from the bundled default.
- **G3** No resource-404 errors in the WKWebView console at startup.

## How to run

**Automated slice:**

```bash
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

**Manual slice:**

```bash
agentops
```

Run through sections B, C, D, E1, E3 in one sitting (≈10 min). Screenshot the C1–C3 scenarios since that's the regression area.

**Install slice (F, G):** run on a fresh machine *or* temporarily move `~/.agentops/` aside and remove `/Applications/AgentOps.app` to simulate first-install conditions.

## Run log

| Section | Date | Result | Notes |
|---|---|---|---|
| A (pytest) | 2026-04-24 | PASS | 14/14 green in 0.10s |
| B | 2026-04-24 | PASS | Sidebar + switching verified manually |
| C | 2026-04-24 | PASS | `[hidden]` fix holds; no overlay regression |
| D | 2026-04-24 | PASS | `Cmd+1..9` and `Cmd+R` behave as expected |
| E | 2026-04-24 | PASS | Last-service persistence works across relaunch |
| F | 2026-04-24 | PASS | `./install.sh` built + installed `AgentOps.app` (35 MB); Gatekeeper prompt as documented |
| G | 2026-04-24 | PASS | Bundled assets resolve, no console 404s |

## Readiness note

v0.1 is ship-ready on macOS 13+. No blockers. Known limitations already documented in README (X-Frame-Options sites, unsigned bundle). Carry-over into v0.2 per ROADMAP.
