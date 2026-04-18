# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for AgentOps.app — macOS bundle."""

import os
from pathlib import Path

PROJECT_ROOT = Path(SPECPATH)
SRC = PROJECT_ROOT / "src" / "agentops"

datas = [
    (str(SRC / "assets"), os.path.join("agentops", "assets")),
    (str(SRC / "defaults"), os.path.join("agentops", "defaults")),
]

hiddenimports = [
    "webview",
    "webview.platforms.cocoa",
    "AppKit",
    "Foundation",
    "PyObjCTools",
    "PyObjCTools.AppHelper",
    "objc",
    "yaml",
    "pydantic",
    "typer",
    "agentops.app",
    "agentops.cli",
    "agentops.config",
    "agentops.paths",
]

a = Analysis(
    [str(SRC / "__main__.py")],
    pathex=[str(PROJECT_ROOT / "src")],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["pytest", "ruff", "tkinter", "unittest"],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="AgentOps",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    target_arch=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name="AgentOps",
)

icns_path = PROJECT_ROOT / "dist" / "AppIcon.icns"
app = BUNDLE(
    coll,
    name="AgentOps.app",
    icon=str(icns_path) if icns_path.exists() else None,
    bundle_identifier="com.coachsteff.agentops",
    info_plist={
        "CFBundleName": "AgentOps",
        "CFBundleDisplayName": "AgentOps",
        "CFBundleShortVersionString": "0.1.0",
        "CFBundleVersion": "0.1.0",
        "LSMinimumSystemVersion": "13.0",
        "NSHighResolutionCapable": True,
        "LSApplicationCategoryType": "public.app-category.developer-tools",
    },
)
