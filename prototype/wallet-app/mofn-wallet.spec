# PyInstaller spec for the desktop wallet's macOS app (W-7, mofn#179).
#
#   cd prototype/wallet-app && pyinstaller --clean --noconfirm mofn-wallet.spec
#
# writes "dist/m-of-n Wallet.app". `.github/workflows/release.yml` runs exactly
# this on macOS, then signs and notarizes it when the Developer ID secrets are
# set (entitlements.plist), and zips it with `ditto` and makes the DMG (a plain
# zip breaks the bundle's symlinks and its signature). Pins: requirements-release.txt.
#
# The engine, `cli` and the Qt-free parts of `screens` come from
# ../wallet, placed at the bundle root, where their own __file__ arithmetic
# looks (as in ../wallet/mofn.spec):
#   screens/learn.py -> README.md and screens/learn/*.md (the Learn page)
#   mofn_app/core.py -> fixtures/ (the example vocabulary, DV-1; the self-test)
# `screens/app.py` (Textual) is not bundled: the app never imports it.
import re
from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules

WALLET = Path("../wallet").resolve()
VERSION = re.search(r'__version__ = "(.+)"', (WALLET / "engine" / "__init__.py").read_text()).group(1)

datas = [
    (str(WALLET / "README.md"), "."),
    (str(WALLET / "screens" / "learn"), "screens/learn"),
    (str(WALLET / "fixtures"), "fixtures"),
    ("README.md", "wallet-app"),
]
hiddenimports = collect_submodules("engine") + [
    "cli", "screens", "screens.runner", "screens.data", "screens.learn", "_cffi_backend",
]
# Qt modules the app does not use; PySide6-Essentials still ships some of them.
UNUSED_QT = [
    "PySide6.Qt3DCore", "PySide6.QtBluetooth", "PySide6.QtCharts", "PySide6.QtDataVisualization",
    "PySide6.QtMultimedia", "PySide6.QtNetwork", "PySide6.QtOpenGL", "PySide6.QtPdf", "PySide6.QtQml",
    "PySide6.QtQuick", "PySide6.QtSql", "PySide6.QtTest", "PySide6.QtWebEngineCore", "PySide6.QtWebSockets",
]

a = Analysis(
    ["mofn-wallet"],
    pathex=[".", str(WALLET)],
    datas=datas,
    hiddenimports=hiddenimports,
    excludes=["pytest", "pytestqt", "tkinter", "textual", "rich", "screens.app", *UNUSED_QT],
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="mofn-wallet",
    console=False,
    upx=False,
)
coll = COLLECT(exe, a.binaries, a.datas, name="mofn-wallet", upx=False)
app = BUNDLE(
    coll,
    name="m-of-n Wallet.app",
    bundle_identifier="org.m-of-n.wallet",
    version=VERSION,
    info_plist={
        "CFBundleShortVersionString": VERSION,
        "CFBundleVersion": VERSION,
        "NSHighResolutionCapable": True,
        "LSMinimumSystemVersion": "13.0",
        "NSHumanReadableCopyright": "Prototype: DEC-004 and DEC-005 are open; do not use real keys.",
    },
)
