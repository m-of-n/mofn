"""Verify: check the statements you were handed (`mofn check --format
json`), shown as rows, top to bottom (mockup v2, approved 2026-11-17):

1. Authorization, prominent, with YES / NO
2. The other five lines, in one row
3. Subject: the sentence, the file, its digest, the claim, the vocabulary
4. Signed by
5. Standing: the chain (timeline rows) or the same chain in words
6. The limit line

Everything shown is read from the CLI's JSON (W-5's `associations` for 3–5),
so the app shows the CLI's verdict; nothing here decides anything. The rows
themselves are drawn by `verdict.py`, which Personas shares (W-8).

The verdict is computed **as the active persona**: `check --as` uses only that
persona's anchors, and the context list is that persona's (SPEC-0001 §6.3).
Switching persona therefore clears a verdict computed as the other one."""

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QWidget

from .. import core, verdict
from ..widgets import Card, FileField, Page, Rows, holder, label


class Verify(Page):
    pill = "✓ Verdict"
    title = "Verify"
    sub = "Pick the statements you were handed and the file they are about."

    def build(self):
        f = self.form = self.add(Card())
        rows = Rows()
        self.statements = rows.row("Statements", FileField("one or more .stmt files", mode="many",
                                                           filter="Statements (*.stmt *.yaml);;All files (*)"))
        self.subject = rows.row("File", FileField("the file they are about"))
        self.vocab = rows.row("Vocabulary", FileField("a .def file", filter="Vocabularies (*.def)"))
        self.vocab.set(str(core.EXAMPLE_VOCABULARY))
        f.add(holder(rows))
        more = QPushButton("▸ More options")
        more.setObjectName("icon")
        more.clicked.connect(lambda: self.more.setVisible(not self.more.isVisible()))
        f.add(more)
        mr = Rows()
        self.as_ = mr.row("As", label("—"))
        mr.row("", label("the active persona — switch it in the sidebar or on Personas", "cap"))
        self.context = mr.row("Context", QComboBox())
        self.context.setEditable(True)
        self.at = mr.row("As of", QLineEdit())
        self.at.setPlaceholderText("now, or YYYY-MM-DDTHH:MM:SSZ")
        self.more = holder(mr)
        self.more.setVisible(False)
        f.add(self.more)
        go = QPushButton("Verify")
        go.setObjectName("primary")
        go.clicked.connect(self.verify)
        f.add(go)

        self.result = QWidget()
        self.results = QVBoxLayout(self.result)
        self.results.setContentsMargins(0, 0, 0, 0)
        self.results.setSpacing(10)
        self.add(self.result)
        self.json = None
        self.checked_as = None
        self.reload()

    def reload(self):
        me = self.app.identity
        cur = self.context.currentText() or "default"
        self.context.clear()
        self.context.addItems(self.app.session.contexts(me.label if me else None))
        offered = [self.context.itemText(i) for i in range(self.context.count())]
        self.context.setCurrentText(cur if cur in offered else "default")
        self.as_.setText(me.label if me else "—")
        self.subline.setText(
            f"Checked as {me.label}, in the community “{self.context.currentText()}”, "
            f"against the roots {me.label} accepted."
            if me
            else "Pick the statements you were handed and the file they are about."
        )
        # A verdict computed as one persona must not sit on screen while
        # another is active: `--as` means it is that persona's verdict.
        who = me.label if me else None
        if self.json is not None and self.checked_as != who:
            self.clear()
            self.json = None
            self.app.status(
                f"Switched to {who}. Verify again for {who}'s verdict."
                if who else "No identity: make one with + New identity.")

    def prefill(self, statements=None, subject=None, vocab=None):
        if statements:
            self.statements.set("; ".join(statements))
        if subject:
            self.subject.set(subject)
        if vocab:
            self.vocab.set(vocab)
        if statements and subject:
            self.verify()

    def clear(self):
        while self.results.count():
            w = self.results.takeAt(0).widget()
            if w:
                w.deleteLater()

    def verify(self):
        self.form.tone(None)
        self.clear()
        if not (self.statements.files() and self.subject.text() and self.vocab.text()):
            return self.error(self.form, "Pick the statements, the file and the vocabulary.")
        me = self.app.identity
        r, j = self.app.session.check(
            self.statements.files(), self.subject.text(), self.vocab.text(),
            self.context.currentText() or "default", self.at.text().strip() or None,
            as_=(me.label if me else None),
        )
        self.checked_as = me.label if me else None
        self.app.ran(r)
        if j is None:
            return self.error(self.form, r.error)
        self.json = j
        self.render(j)

    def render(self, j: dict):
        shown = self.subject.text().rsplit("/", 1)[-1]
        self.h2.setText(shown or "Verify")
        for w in verdict.cards(j, shown=shown or "your file", tokens=self.app.tokens):
            self.results.addWidget(w)

    def restyle(self):
        """Re-draw the verdict in the new theme's colours (the cards hold
        colour literals from `tokens`)."""
        if self.json is not None:
            self.clear()
            self.render(self.json)
