"""Keys: the keys this wallet holds, importing one, and sending yours
(`mofn key list / import / export`). Knowing a key is not trusting it."""

from PySide6.QtWidgets import (
    QAbstractItemView,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
)

from ..widgets import Card, FileField, Page, Rows, holder, label


class Keys(Page):
    pill = "Keys"
    title = "Keys"
    sub = "Keys this wallet holds. Knowing a key is not trusting it: trust is on the Trust page."

    def build(self):
        send = QPushButton("Send my key…")
        send.clicked.connect(self.send)
        self.head.addWidget(send)

        table = self.add(Card())
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["NAME", "KIND", "FINGERPRINT", "HELD", "FROM"])
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table.setShowGrid(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(True)
        table.add(self.table)

        imp = self.add(Card("Import a key someone sent you"))
        rows = Rows()
        self.file = rows.row("Key file", FileField("their .pub.stmt file", filter="Statements (*.stmt *.yaml);;All files (*)"))
        self.name = rows.row("Call it", QLineEdit())
        self.name.setPlaceholderText("a name for you, e.g. Dave")
        imp.add(holder(rows))
        go = QPushButton("Import")
        go.setObjectName("primary")
        go.clicked.connect(self.do_import)
        line = QHBoxLayout()
        line.addWidget(go)
        line.addWidget(label("The signature is checked before the key is added.", "cap"), 1)
        imp.add(holder(line))
        self.imp = imp
        self.reload()

    def reload(self):
        rows = self.app.session.keys()
        self.table.setRowCount(len(rows))
        for i, r in enumerate(rows):
            held = "yours · can sign" if r["yours"] else "known"
            src = "made here" if r["yours"] else (r["from"] or "")
            for j, v in enumerate([r["label"] or "—", r["kind"] or "—", r["fingerprint"], held, src]):
                self.table.setItem(i, j, QTableWidgetItem(v))
        self.table.setFixedHeight(34 + 32 * max(len(rows), 1))

    def do_import(self):
        self.imp.tone(None)
        if not self.file.text():
            return self.error(self.imp, "Choose the key file first.")
        r = self.app.run(self.app.session.key_import(self.file.text(), self.name.text().strip() or None))
        if r.ok:
            self.file.set("")
            self.name.clear()

    def send(self):
        me = self.app.identity
        if me is None:
            return self.app.status("Make an identity first: + New identity.", ok=False)
        out, _ = QFileDialog.getSaveFileName(self, "Save your key file", f"{me.label}.pub{self.app.session.suffix}")
        if out:
            self.app.run(self.app.session.key_export(me.label, out))
