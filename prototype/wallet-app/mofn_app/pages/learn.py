"""Learn: the six pages `mofn run` ships (`screens/learn/*.md`), from the
same source, rendered as formatted text. Reading only; nothing runs."""

from PySide6.QtWidgets import QHBoxLayout, QListWidget, QPushButton, QTextBrowser

from .. import core
from ..widgets import Card, Page, holder


class Learn(Page):
    pill = "Learn"
    title = "Learn"
    sub = "What each page does, and the mofn command behind it."

    def build(self):
        self.pages = core.learn_pages()
        row = QHBoxLayout()
        self.list = QListWidget()
        self.list.setFixedWidth(170)
        self.list.addItems([f"{i + 1} · {p.title}" for i, p in enumerate(self.pages)])
        self.list.currentRowChanged.connect(self.open)
        row.addWidget(self.list)
        c = Card()
        self.doc = QTextBrowser()
        self.doc.setOpenExternalLinks(True)
        self.doc.setMinimumHeight(460)
        c.add(self.doc)
        self.go = QPushButton("")
        self.go.clicked.connect(self.goto)
        c.add(self.go)
        row.addWidget(c, 1)
        self.add(holder(row))
        self.list.setCurrentRow(0)

    def open(self, i: int):
        if 0 <= i < len(self.pages):
            p = self.pages[i]
            self.doc.setMarkdown(p.text)
            target = {"check": "Verify", "wallet": "Overview"}.get(p.go, p.go.capitalize())
            self.go.setText(f"Go to {target} →" if p.go else "")
            self.go.setVisible(bool(p.go))
            self._go = target

    def goto(self):
        self.app.go(self._go)
