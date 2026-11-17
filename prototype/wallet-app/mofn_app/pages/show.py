"""Show: open any file to read it. A statement or a vocabulary is decoded
(`mofn show`); any file gets its SHA-256, as a statement names it."""

from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QFileDialog, QHBoxLayout, QPlainTextEdit, QPushButton

from .. import core
from ..widgets import Card, Page, Rows, holder, label


class Show(Page):
    pill = "Show"
    title = "Open a file to read it"
    sub = "A statement or vocabulary is decoded; any other file is hashed."

    def build(self):
        b = QPushButton("Open…")
        b.clicked.connect(self.pick)
        self.head.addWidget(b)
        self.card = self.add(Card())
        self.facts = Rows(110)
        self.card.add(holder(self.facts))
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        self.text.setObjectName("mono")
        self.text.setMinimumHeight(260)
        self.card.add(self.text)
        self.card.setVisible(False)

    def pick(self):
        f, _ = QFileDialog.getOpenFileName(self, "Open a file")
        if f:
            self.open(f)

    def open(self, path: str):
        while self.facts.count():
            w = self.facts.takeAt(0).widget()
            if w:
                w.deleteLater()
        s = self.app.session
        info = s.inspect(path)
        name = path.rsplit("/", 1)[-1]
        kind = info.get("kind")
        self.h2.setText(name)
        digest = core.digest_text(path)
        copy = QPushButton("Copy")
        copy.clicked.connect(lambda: QGuiApplication.clipboard().setText(digest))
        line = QHBoxLayout()
        line.addWidget(label(digest, "mono"), 1)
        line.addWidget(copy)
        self.facts.row("SHA-256", holder(line))
        self.facts.row("Size", f"{info['size']:,} bytes")
        if kind and kind != "definition":
            self.facts.row("Kind", kind)
            if info.get("verified"):
                self.facts.row("Signed by", info["says"])
                self.facts.row("Signature", label("valid ✓", "ok"))
            else:
                self.facts.row("Signature", label(f"not verified: {info.get('why', '')}", "bad"))
        if kind:
            r = self.app.run(s.show(path))
            self.text.setPlainText(r.out if r.ok else r.error)
            self.text.setVisible(True)
        else:
            self.text.setVisible(False)
        self.card.setVisible(True)
