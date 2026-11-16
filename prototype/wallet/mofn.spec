# PyInstaller spec for the one-file `mofn` build (mofn#127 §6, DL-0043).
#
#   cd prototype/wallet && pyinstaller --clean --noconfirm mofn.spec
#
# writes dist/mofn (dist/mofn.exe on Windows). `.github/workflows/release.yml`
# runs exactly this on each OS. The pins are in requirements-release.txt.
#
# The data files are placed at the paths the modules already compute from
# their own __file__, so no code knows it is frozen:
#   screens/learn.py   -> README.md and screens/learn/*.md (the Learn tab)
#   screens/example.py -> fixtures/ (the example vocabulary, DV-1)
#   screens/learn.py   -> fixtures/golden/ (Learn's example output)
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

datas = [
    ("README.md", "."),
    ("CHANGELOG.md", "."),
    ("requirements.txt", "."),
    ("screens/learn", "screens/learn"),
    ("fixtures", "fixtures"),
]
datas += collect_data_files("textual")

# textual.widgets and rich load submodules lazily, by name; PyInstaller's
# import scan cannot see those.
hiddenimports = collect_submodules("textual") + collect_submodules("rich")
hiddenimports += collect_submodules("screens") + collect_submodules("engine")
# PyNaCl's bindings import cffi's C module by name, which the scan misses: the
# first build ran and died on `No module named '_cffi_backend'`.
hiddenimports += ["_cffi_backend"]

a = Analysis(
    ["mofn"],
    pathex=["."],
    datas=datas,
    hiddenimports=hiddenimports,
    excludes=["pytest", "tkinter"],
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    name="mofn",
    console=True,
    upx=False,
)
