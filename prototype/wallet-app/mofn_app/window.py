"""The window: sidebar, page, status bar (mockups v2/v3, approved
2026-11-17).

Sidebar, top to bottom: the active identity and its switcher (+ New
identity) — the scaffold W-8 (#180) builds personas on — then the pages,
then the wallet switcher and the prototype badge. The sidebar collapses to
icons. The status bar shows the `mofn` command the last action ran, so the
same thing can be typed in a terminal against the same wallet."""

from pathlib import Path

from PySide6.QtCore import QSettings, QSize, Qt
from PySide6.QtGui import QAction, QGuiApplication
from PySide6.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QMenu,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from . import core, theme
from .pages.communities import Communities
from .pages.keys import Keys
from .pages.learn import Learn
from .pages.overview import Overview
from .pages.personas import Personas
from .pages.show import Show
from .pages.sign import Sign
from .pages.trust import Trust
from .pages.verify import Verify
from .widgets import Rows, Toggle, holder, label

PAGES = [
    ("WALLET", [
        ("Overview", "overview", Overview),
        ("Personas", "personas", Personas),
        ("Keys", "keys", Keys),
        ("Trust", "trust", Trust),
        ("Communities", "communities", Communities),
    ]),
    ("ACT", [("Sign", "sign", Sign), ("Verify", "verify", Verify), ("Show", "show", Show), ("Learn", "learn", Learn)]),
]
RECENT = 6


class NewIdentity(QDialog):
    """`mofn key gen`: a name, a kind, and the passphrase twice. The
    passphrase stays in this dialog's fields until it is handed over."""

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("New identity")
        v = QVBoxLayout(self)
        v.addWidget(label("An identity is a key of your own. Its private half stays in this wallet, "
                          "locked with the passphrase.", "sub"))
        rows = Rows(110)
        self.name = rows.row("Name", QLineEdit())
        self.name.setPlaceholderText("e.g. Alice")
        self.kind = rows.row("Kind", QComboBox())
        self.kind.addItems(list(core.CONTROLLERS))
        self.p1 = rows.row("Passphrase", QLineEdit())
        self.p2 = rows.row("Again", QLineEdit())
        for p in (self.p1, self.p2):
            p.setEchoMode(QLineEdit.EchoMode.Password)
        v.addWidget(holder(rows))
        self.err = label("", "bad")
        v.addWidget(self.err)
        b = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        b.button(QDialogButtonBox.StandardButton.Ok).setText("Create")
        b.accepted.connect(self.check)
        b.rejected.connect(self.reject)
        v.addWidget(b)

    def check(self):
        if not self.name.text().strip():
            return self.err.setText("Give it a name.")
        if not self.p1.text():
            return self.err.setText("Choose a passphrase.")
        if self.p1.text() != self.p2.text():
            self.p2.clear()
            return self.err.setText("The passphrases differ.")
        self.accept()

    def take(self) -> tuple[str, str, bytes]:
        secret = self.p1.text().encode("utf-8")
        self.p1.clear()
        self.p2.clear()
        return self.name.text().strip(), self.kind.currentText(), secret


class Window(QMainWindow):
    def __init__(self, wallet: Path | None = None):
        super().__init__()
        self.setWindowTitle("m-of-n wallet")
        self.resize(1080, 760)
        self.settings = QSettings()
        start = wallet or self.settings.value("wallet/current") or core.resolve_wallet()
        self.session = core.Session(Path(start))
        self.scheme = self.settings.value("theme", "System")
        self.tokens = theme.DARK
        self.identity = None
        self.collapsed = self.settings.value("sidebar/collapsed", False, type=bool)

        root = QWidget()
        row = QHBoxLayout(root)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(0)
        row.addWidget(self.sidebar())
        row.addWidget(self.content(), 1)
        self.setCentralWidget(root)
        QGuiApplication.styleHints().colorSchemeChanged.connect(lambda _: self.apply_theme())
        self.pick_identity(self.settings.value(self.key("identity")))
        self.apply_theme()
        self.set_collapsed(self.collapsed)
        self.go("Overview")

    # ------------------------------------------------------------- layout

    def sidebar(self) -> QWidget:
        side = QWidget()
        side.setObjectName("sidebar")
        self.side = side
        v = QVBoxLayout(side)
        v.setContentsMargins(8, 10, 8, 10)
        v.setSpacing(3)
        self.sec = []

        def section(text):
            s = label(text, "section", wrap=False)
            self.sec.append(s)
            v.addWidget(s)

        section("IDENTITY")
        self.who = QToolButton()
        self.who.setObjectName("who")
        self.who.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.who.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.who.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.who_menu = QMenu(self.who)
        self.who.setMenu(self.who_menu)
        v.addWidget(self.who)
        self.add_id = QPushButton("+ New identity")
        self.add_id.setObjectName("dashed")
        self.add_id.clicked.connect(self.new_identity)
        v.addWidget(self.add_id)

        self.nav = QButtonGroup(self)
        self.navs = {}
        for title, items in PAGES:
            v.addSpacing(8)
            section(title)
            for name, icon, _ in items:
                b = QPushButton(name)
                b.setObjectName("nav")
                b.setCheckable(True)
                b.setIconSize(QSize(15, 15))
                b.clicked.connect(lambda _=False, n=name: self.go(n))
                self.nav.addButton(b)
                self.navs[name] = (b, icon)
                v.addWidget(b)
        v.addStretch(1)
        self.wal = QToolButton()
        self.wal.setObjectName("wallet")
        self.wal.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.wal_menu = QMenu(self.wal)
        self.wal_menu.aboutToShow.connect(self.fill_wallets)
        self.wal.setMenu(self.wal_menu)
        v.addWidget(self.wal)
        self.badge = label("PROTOTYPE · not for real keys", "badge")
        self.badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.badge.setToolTip(f"{' and '.join(core.OPEN)} are open. Do not use real keys. mofn {core.VERSION}")
        v.addWidget(self.badge)
        return side

    def content(self) -> QWidget:
        c = QWidget()
        c.setObjectName("content")
        v = QVBoxLayout(c)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(0)
        top = QWidget()
        top.setObjectName("topbar")
        t = QHBoxLayout(top)
        t.setContentsMargins(10, 8, 14, 8)
        self.fold = QPushButton()
        self.fold.setObjectName("icon")
        self.fold.setToolTip("Show or hide the sidebar")
        self.fold.clicked.connect(lambda: self.set_collapsed(not self.collapsed))
        t.addWidget(self.fold)
        self.title = label("", "title", wrap=False)
        t.addWidget(self.title, 1)
        self.themes = Toggle(["Light", "System", "Dark"], self.scheme)
        self.themes.picked.connect(self.set_scheme)
        t.addWidget(self.themes)
        v.addWidget(top)

        self.stack = QStackedWidget()
        self.pages = {}
        for _, items in PAGES:
            for name, _, cls in items:
                p = cls(self)
                self.pages[name] = p
                self.stack.addWidget(p)
        v.addWidget(self.stack, 1)

        bar = QWidget()
        bar.setObjectName("statusbar")
        b = QHBoxLayout(bar)
        b.setContentsMargins(16, 5, 16, 5)
        self.state = label("", None, wrap=False)
        self.cmd = label("", "cmd", wrap=False)
        self.cmd.setToolTip("The mofn command this ran. The same wallet works from a terminal.")
        for w in (self.state, self.cmd):
            # Long paths must not widen the window: clip, full text in the tooltip.
            w.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        self.cmd.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        b.addWidget(self.state, 2)
        b.addWidget(self.cmd, 3)
        v.addWidget(bar)
        return c

    # ------------------------------------------------------------- state

    def key(self, name: str) -> str:
        return f"wallets/{self.session.root}/{name}"

    def go(self, name: str, **prefill):
        page = self.pages[name]
        self.navs[name][0].setChecked(True)
        self.title.setText(name)
        page.reload()
        if prefill and hasattr(page, "prefill"):
            page.prefill(**prefill)
        self.stack.setCurrentWidget(page)

    def refresh(self):
        self.fill_identities()
        self.wal.setText(("" if self.collapsed else f"Wallet ▾  {self.session.root.name}"))
        self.wal.setToolTip(str(self.session.root))
        for p in self.pages.values():
            p.reload()

    def status(self, text: str, ok: bool = True):
        dot = self.tokens["ok"] if ok else self.tokens["bad"]
        self.state.setText(f"{text} <span style='color:{dot}'>●</span>")

    def ran(self, r: core.Result) -> core.Result:
        self.cmd.setText(r.shown)
        self.cmd.setToolTip(r.shown)
        if r.ok or r.code == 1:
            first = (r.out.strip().splitlines() or ["done"])[0]
            word = {"check": "Checked", "show": "Opened"}.get(next((a for a in r.argv if a in ("check", "show")), ""))
            self.status(word or first[:90], ok=r.ok)
        else:
            self.status(r.error, ok=False)
        return r

    def run(self, r: core.Result) -> core.Result:
        """After a command that changed the wallet: show it, then re-read."""
        self.ran(r)
        if r.ok:
            self.refresh()
        return r

    # ------------------------------------------------------------- identity

    def fill_identities(self):
        owned = self.session.owned()
        if self.identity and self.identity.kid not in {p.kid for p in owned}:
            self.identity = None
        if self.identity is None and owned:
            self.identity = owned[0]
        self.who_menu.clear()
        for p in owned:
            a = QAction(f"{p.label}  ·  {p.controller}", self.who_menu)
            a.setCheckable(True)
            a.setChecked(p is self.identity or (self.identity and p.kid == self.identity.kid))
            a.triggered.connect(lambda _=False, p=p: self.pick_identity(p.label))
            self.who_menu.addAction(a)
        if owned:
            self.who_menu.addSeparator()
        self.who_menu.addAction("New identity…", self.new_identity)
        me = self.identity
        av = theme.icon("person", self.tokens["acc_fg"])
        self.who.setIcon(av)
        if self.collapsed:
            self.who.setText("")
        elif me:
            self.who.setText(f"{me.label} ▾\n{me.controller} · {me.kid.hex()[:4]} {me.kid.hex()[4:8]}")
        else:
            self.who.setText("No identity yet")
        self.who.setToolTip(me.label if me else "No identity yet")

    def pick_identity(self, label_: str | None):
        owned = self.session.owned()
        self.identity = next((p for p in owned if p.label == label_), owned[0] if owned else None)
        if self.identity:
            self.settings.setValue(self.key("identity"), self.identity.label)
        self.refresh()

    def new_identity(self):
        if not self.session.exists:
            return self.status("Create the wallet first (Overview).", ok=False)
        d = NewIdentity(self)
        if d.exec() != QDialog.DialogCode.Accepted:
            return
        name, kind, secret = d.take()
        r = self.run(self.session.key_gen(name, kind, secret))
        del secret
        if r.ok:
            self.pick_identity(name)

    # ------------------------------------------------------------- wallets

    def recent(self) -> list[str]:
        return [w for w in (self.settings.value("wallet/recent") or []) if w]

    def open_wallet(self, path: str | Path):
        path = str(Path(path).expanduser())
        self.session = core.Session(path)
        self.settings.setValue("wallet/current", path)
        rec = [path] + [w for w in self.recent() if w != path]
        self.settings.setValue("wallet/recent", rec[:RECENT])
        self.pick_identity(self.settings.value(self.key("identity")))
        self.status(f"Opened {path}" if self.session.exists else f"No wallet at {path} yet")
        self.go("Overview")

    def fill_wallets(self):
        m = self.wal_menu
        m.clear()
        for w in self.recent() or [str(self.session.root)]:
            a = m.addAction(w, lambda w=w: self.open_wallet(w))
            a.setCheckable(True)
            a.setChecked(w == str(self.session.root))
        m.addSeparator()
        m.addAction("Open a wallet folder…", self.pick_wallet)
        m.addAction("Create a wallet…", self.create_wallet)

    def pick_wallet(self):
        d = QFileDialog.getExistingDirectory(self, "Open a wallet folder", str(self.session.root.parent))
        if d:
            self.open_wallet(d)

    def create_wallet(self):
        d = QFileDialog.getExistingDirectory(self, "Choose an empty folder for the new wallet", str(Path.home()))
        if d:
            self.session = core.Session(d)
            self.create_here()

    def create_here(self):
        r = self.run(self.session.init())
        if r.ok:
            self.open_wallet(self.session.root)

    # ------------------------------------------------------------- look

    def set_scheme(self, scheme: str):
        self.scheme = scheme
        self.settings.setValue("theme", scheme)
        self.apply_theme()

    def apply_theme(self):
        dark = self.scheme == "Dark" or (
            self.scheme == "System" and QGuiApplication.styleHints().colorScheme() != Qt.ColorScheme.Light
        )
        self.tokens = theme.DARK if dark else theme.LIGHT
        self.setStyleSheet(theme.sheet(self.tokens))
        for name, (b, icon) in self.navs.items():
            b.setIcon(theme.icon(icon, self.tokens["soft"]))
        self.fold.setIcon(theme.icon("sidebar", self.tokens["soft"]))
        self.fill_identities()
        for p in self.pages.values():
            p.restyle()

    def set_collapsed(self, yes: bool):
        self.collapsed = yes
        self.settings.setValue("sidebar/collapsed", yes)
        self.side.setFixedWidth(56 if yes else 190)
        for name, (b, _) in self.navs.items():
            b.setText("" if yes else name)
            b.setToolTip(name)
        for s in self.sec:
            s.setVisible(not yes)
        self.add_id.setText("+" if yes else "+ New identity")
        self.badge.setText("!" if yes else "PROTOTYPE · not for real keys")
        self.refresh()
