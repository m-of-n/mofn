"""Trust: the roots you trust, and trusting a key about one kind of claim
(`mofn root add / root list`). The context is under More options."""

from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QHeaderView,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)

from .. import core
from ..widgets import Card, FileField, Page, Rows, holder, label


class Trust(Page):
    pill = "Trust"
    title = "Who you trust"
    sub = "Roots: keys you decided to believe, about one kind of claim. Every verdict starts here."

    def build(self):
        tc = self.add(Card())
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["KEY", "ABOUT", "VALUES", "MAY DELEGATE", "NOTE"])
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(True)
        tc.add(self.table)
        self.none = tc.add(label("You trust no key yet, so every verdict says no standing. Trust one below.", "cap"))

        f = self.form = self.add(Card("Trust a key"))
        rows = Rows()
        self.key = rows.row("Key", QComboBox())
        self.vocab = rows.row("Vocabulary", FileField("a .def file", filter="Vocabularies (*.def)"))
        self.vocab.set(str(core.EXAMPLE_VOCABULARY))
        self.vocab.changed.connect(self.offer_claims)
        self.claim = rows.row("About", QComboBox())
        self.claim.currentTextChanged.connect(self.offer_values)
        self.values_box = QWidget()
        self.values_row = QHBoxLayout(self.values_box)
        self.values_row.setContentsMargins(0, 0, 0, 0)
        rows.row("Values", self.values_box)
        self.depth = rows.row("May delegate", QSpinBox())
        self.depth.setRange(0, 5)
        self.depth.setSuffix(" levels")
        self.note = rows.row("Note", QLineEdit())
        self.note.setPlaceholderText("optional, for you")
        f.add(holder(rows))

        more = QPushButton("▸ More options")
        more.setObjectName("icon")
        more.clicked.connect(lambda: self.more.setVisible(not self.more.isVisible()))
        f.add(more)
        mr = Rows()
        self.context = mr.row("Context", QComboBox())
        self.context.setEditable(True)
        self.context.currentTextChanged.connect(lambda _: self.fill_table())
        self.more = holder(mr)
        self.more.setVisible(False)
        f.add(self.more)

        go = QPushButton("Trust this key")
        go.setObjectName("primary")
        go.clicked.connect(self.trust)
        line = QHBoxLayout()
        line.addWidget(go)
        self.as_ = label("", "cap")
        line.addWidget(self.as_, 1)
        f.add(holder(line))
        self.checks: list[QCheckBox] = []
        self.offer_claims()
        self.reload()

    def reload(self):
        s = self.app.session
        self.key.clear()
        for p in s.known() + s.owned():
            self.key.addItem(p.label or p.kid.hex()[:16])
        cur = self.context.currentText() or "default"
        self.context.blockSignals(True)
        self.context.clear()
        self.context.addItems(s.contexts())
        self.context.setCurrentText(cur)
        self.context.blockSignals(False)
        me = self.app.identity
        self.as_.setText(f"Accepted by {me.label}." if me else "Make an identity first: + New identity.")
        self.fill_table()

    def fill_table(self):
        rows = self.app.session.anchors(self.context.currentText() or "default")
        self.table.setRowCount(len(rows))
        for i, a in enumerate(rows):
            depth = f"{a.depth} level{'s' if a.depth > 1 else ''}" if a.depth else "no"
            for j, v in enumerate([a.key, a.about, a.values, depth, a.note]):
                self.table.setItem(i, j, QTableWidgetItem(v))
        self.table.setVisible(bool(rows))
        self.table.setFixedHeight(34 + 32 * max(len(rows), 1))
        self.none.setVisible(not rows)

    def offer_claims(self, *_):
        d = core.vocabulary(self.vocab.text())
        self.claim.clear()
        self.claim.addItems(core.claims(d))

    def offer_values(self, claim: str):
        for c in self.checks:
            c.deleteLater()
        self.checks = []
        for v in core.values(core.vocabulary(self.vocab.text()), claim):
            c = QCheckBox(v)
            self.values_row.addWidget(c)
            self.checks.append(c)
        if not self.checks:
            c = QCheckBox("any value")
            c.setEnabled(False)
            self.values_row.addWidget(c)
            self.checks.append(c)

    def trust(self):
        self.form.tone(None)
        me = self.app.identity
        if me is None:
            return self.error(self.form, "Make an identity first: + New identity.")
        if not self.key.currentText() or not self.claim.currentText():
            return self.error(self.form, "Pick a key and what you trust it about.")
        values = [c.text() for c in self.checks if c.isChecked() and c.isEnabled()]
        r = self.app.run(
            self.app.session.root_add(
                self.key.currentText(), me.label, self.vocab.text(), self.claim.currentText(),
                values, self.depth.value(), self.context.currentText() or "default", self.note.text().strip(),
            )
        )
        if r.ok:
            self.note.clear()
