"""Personas: who this wallet is, who it knows, and what others have said
about each (W-8, mofn#180).

A wallet owns the personas whose private keys it holds and knows the rest;
both are principals (SPEC-0001 §6.1). Each persona is its own identity key —
two personas are unlinkable only if they share no key and no statement links
them (SPEC-0001 §3.1), which is why `+ New identity` makes a whole new key
rather than another key under one.

The **tags received** are the statements held here whose subject is this
persona's identity key. Each is checked by running the real
`mofn check --subject-key … --as …`, so the verdict shown is the CLI's.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QHeaderView,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .. import core, verdict
from ..widgets import Card, FileField, Page, holder, label


def _table(headers: list[str]) -> QTableWidget:
    t = QTableWidget(0, len(headers))
    t.setHorizontalHeaderLabels(headers)
    t.verticalHeader().setVisible(False)
    t.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    t.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
    t.setShowGrid(False)
    t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
    t.horizontalHeader().setStretchLastSection(True)
    return t


class Personas(Page):
    pill = "Personas"
    title = "Personas"
    sub = "Who this wallet is, and who it knows. Each persona is its own identity key."

    def build(self):
        new = QPushButton("+ New identity…")
        new.setObjectName("primary")
        new.clicked.connect(lambda: self.app.new_identity())
        self.head.addWidget(new)

        mine = self.add(Card("Your personas — you hold these keys"))
        self.mine = _table(["", "NAME", "CONTROLLER", "FINGERPRINT", "TAGS", "COMMUNITIES"])
        mine.add(self.mine)
        self.acts = QWidget()
        self.acts_row = QHBoxLayout(self.acts)
        self.acts_row.setContentsMargins(0, 6, 0, 0)
        mine.add(self.acts)
        mine.add(label(
            "Each persona has its own identity key. Two personas are unlinkable only "
            "if they share no key and no statement links them (SPEC-0001 §3.1).", "cap"))
        mine.add(label(
            "The controller kind is what a persona says it is — a claim, not evidence "
            "(SPEC-0001 §3.2).", "cap"))

        theirs = self.add(Card("Keys you know — public only"))
        self.theirs = _table(["NAME", "CONTROLLER", "FINGERPRINT", "FROM"])
        theirs.add(self.theirs)
        self.no_known = theirs.add(label(
            "You know no other key yet. Import one on Keys.", "cap"))

        self.tags = self.add(Card("Tags received"))
        self.tags_head = self.tags.add(label("", "cap"))
        self.tags_box = QWidget()
        self.tags_list = QVBoxLayout(self.tags_box)
        self.tags_list.setContentsMargins(0, 0, 0, 0)
        self.tags_list.setSpacing(8)
        self.tags.add(self.tags_box)
        self.vocab = FileField("a .def file", filter="Vocabularies (*.def)")
        self.vocab.set(str(core.EXAMPLE_VOCABULARY))
        self.vocab_row = holder(self._vocab_row())
        self.tags.add(self.vocab_row)
        self.stale = True

    def _vocab_row(self):
        row = QHBoxLayout()
        row.addWidget(label("Vocabulary for a tag this wallet does not hold one for:", "cap"))
        row.addWidget(self.vocab, 1)
        return row

    # Personas verifies every held statement, and `window.refresh()` reloads
    # every page after every command. Fill only when on screen.
    def reload(self):
        self.stale = True
        if self.isVisible():
            self.fill()

    def showEvent(self, e):
        super().showEvent(e)
        if self.stale:
            self.fill()

    def restyle(self):
        self.stale = True
        if self.isVisible():
            self.fill()

    # ----------------------------------------------------------------- fill

    def fill(self):
        self.stale = False
        s, me = self.app.session, self.app.identity
        owned, known = s.owned(), s.known()

        self.mine.setRowCount(len(owned))
        while self.acts_row.count():
            w = self.acts_row.takeAt(0).widget()
            if w:
                w.setParent(None)  # at once: deleteLater() would leave it found
                w.deleteLater()
        for i, p in enumerate(owned):
            active = me is not None and p.kid == me.kid
            cells = [
                "●" if active else "",
                p.label or "—",
                f"{p.controller} · self-claimed" if p.controller else "—",
                core.fingerprint(p.kid),
                str(len(s.received(p.label or ""))),
                ", ".join(c.context for c in s.communities(p.label) if c.relies) or "none",
            ]
            for j, v in enumerate(cells):
                item = QTableWidgetItem(v)
                if j == 0:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.mine.setItem(i, j, item)
            if not active and p.label:
                b = QPushButton(f"Act as {p.label}")
                b.setObjectName("icon")
                b.clicked.connect(lambda _=False, n=p.label: self.app.pick_identity(n))
                self.acts_row.addWidget(b)
        self.acts_row.addStretch(1)
        self.mine.setFixedHeight(34 + 32 * max(len(owned), 1))
        self.acts.setVisible(len(owned) > 1)

        self.theirs.setRowCount(len(known))
        for i, p in enumerate(known):
            how = (p.provenance or {}).get("how", "")
            for j, v in enumerate([p.label or "—", p.controller or "—",
                                   core.fingerprint(p.kid), how]):
                self.theirs.setItem(i, j, QTableWidgetItem(v))
        self.theirs.setFixedHeight(34 + 32 * max(len(known), 1))
        self.theirs.setVisible(bool(known))
        self.no_known.setVisible(not known)

        self.fill_tags(me)

    def fill_tags(self, me):
        while self.tags_list.count():
            w = self.tags_list.takeAt(0).widget()
            if w:
                w.setParent(None)  # at once: deleteLater() would leave it found
                w.deleteLater()
        if me is None:
            self.tags_head.setText("Make an identity first: + New identity.")
            self.vocab_row.setVisible(False)
            return
        tags = self.app.session.received(me.label or "")
        self.tags_head.setText(
            f"Statements held here whose subject is {me.label}'s identity key — "
            f"what others have said about this persona."
            if tags else
            f"Nobody has tagged {me.label} yet. A tag is a statement whose subject "
            f"is this persona's key (`mofn make --subject-key {me.label}`).")
        self.vocab_row.setVisible(any(t.definition is None for t in tags))
        for t in tags:
            self.tags_list.addWidget(TagRow(self, t, me))


class TagRow(QWidget):
    """One tag, and its six-line verdict when you ask for it."""

    def __init__(self, page: Personas, tag: core.Tag, me):
        super().__init__()
        self.page, self.tag, self.me = page, tag, me
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(6)
        line = QHBoxLayout()
        who = "gave itself" if tag.from_self else "says"
        line.addWidget(label(
            f"<b>{tag.says}</b> {who} <b>{tag.claim}</b> · valid to {tag.not_on_or_after}"), 1)
        self.button = QPushButton("Check")
        self.button.setObjectName("icon")
        self.button.clicked.connect(self.check)
        line.addWidget(self.button)
        box.addLayout(line)
        self.result = QWidget()
        self.results = QVBoxLayout(self.result)
        self.results.setContentsMargins(0, 0, 0, 0)
        self.results.setSpacing(8)
        self.result.setVisible(False)
        box.addWidget(self.result)

    def check(self):
        if self.result.isVisible():
            self.result.setVisible(False)
            self.button.setText("Check")
            return
        while self.results.count():
            w = self.results.takeAt(0).widget()
            if w:
                w.setParent(None)  # at once: deleteLater() would leave it found
                w.deleteLater()
        vocab = self.tag.definition or self.page.vocab.text()
        if not vocab:
            return self.page.error(self.page.tags, "Pick the vocabulary this tag uses.")
        handed = [self.tag.path, *self._define_files()]
        if len(handed) == 1 and self.tag.definition_id == core.example_definition_id():
            # As Sign's "Verify it" does: a relying party is handed the
            # vocabulary's own define statement, or the semantics line cannot
            # attribute it (SPEC-0003 §11.1). Matched by DefinitionId, not by
            # path: the wallet keeps its own copy of the bytes.
            handed.append(str(core.EXAMPLE_DEFINE))
        r, j = self.page.app.session.check(
            handed, definition=vocab, subject_key=self.me.label, as_=self.me.label,
        )
        self.page.app.ran(r)
        if j is None:
            return self.page.error(self.page.tags, r.error)
        names = {self.me.kid.hex(): self.me.label}
        for w in verdict.cards(j, shown=self.me.label, tokens=self.page.app.tokens,
                               names=names):
            self.results.addWidget(w)
        self.result.setVisible(True)
        self.button.setText("Hide")

    def _define_files(self) -> list[str]:
        """The define statements for this tag's vocabulary, so the semantics
        line can attribute it (SPEC-0003 §11.1) — as `mofn run` hands them."""
        root = self.page.app.session.root / "statements"
        return [str(root / f"{d.digest.hex()}.stmt") for d in self.tag.defines
                if (root / f"{d.digest.hex()}.stmt").is_file()]
