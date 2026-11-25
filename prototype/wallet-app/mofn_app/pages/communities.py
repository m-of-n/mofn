"""Communities: the contexts the active persona relies in, and who is in each
(W-8, mofn#180).

**"Community" is this app's word for a SPEC-0004 context.** It is not a term
in any SPEC, and the page says so, because the app must not invent vocabulary
the specification does not have. A context is a wallet-local scope with its
own trust anchors; every evaluation is relative to exactly one context and
uses only that context's anchors (SPEC-0004 §4.1, SPEC-0001 §6.3).

A context has **no roster**. Nobody declares who belongs: the members shown
are derived from the anchors this persona accepted here (`core.members`).
That is said on screen, so a reader never mistakes a derivation for a list.
"""

from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .. import core
from ..widgets import Card, Page, holder, label


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


class Communities(Page):
    pill = "Communities"
    title = "Communities"
    sub = "A community is a context (SPEC-0004 §4.1): a wallet-local scope with its own trust anchors."

    def build(self):
        note = self.add(Card("What a community is here"))
        note.add(label(
            "<b>“Community” is this app's word for a SPEC-0004 <i>context</i>.</b> "
            "It is not a term in the specification. Every verdict is computed in "
            "exactly one context and uses only that context's anchors, so a key "
            "trusted in one gains nothing in another."))
        note.add(label(
            "A context has no roster and no description. The members below are "
            "<b>derived</b> from the anchors this persona accepted here — not "
            "declared by anyone.", "cap"))

        self.box = QWidget()
        self.list = QVBoxLayout(self.box)
        self.list.setContentsMargins(0, 0, 0, 0)
        self.list.setSpacing(10)
        self.add(self.box)
        self.stale = True

    def reload(self):
        self.stale = True
        if self.isVisible():
            self.fill()

    def showEvent(self, e):
        super().showEvent(e)
        if self.stale:
            self.fill()

    def fill(self):
        self.stale = False
        while self.list.count():
            w = self.list.takeAt(0).widget()
            if w:
                w.setParent(None)  # at once: deleteLater() would leave it found
                w.deleteLater()
        me = self.app.identity
        if me is None:
            self.subline.setText("Make an identity first: + New identity.")
            return
        self.subline.setText(
            f"The contexts {me.label} relies in. A community is a context "
            f"(SPEC-0004 §4.1), with its own trust anchors.")
        found = [c for c in self.app.session.communities(me.label) if c.relies]
        if not found:
            c = Card()
            c.add(label(
                f"{me.label} relies in no context yet, so every verdict as "
                f"{me.label} says no standing. Trusting a key on Trust creates one."))
            self.list.addWidget(c)
            return
        for com in found:
            self.list.addWidget(self.card(com))

    def card(self, com) -> Card:
        c = Card()
        head = QHBoxLayout()
        head.addWidget(label(f"CONTEXT · {com.context.upper()}", "lab", wrap=False), 1)
        relies = label("relies here ✓", "chip", wrap=False)
        relies.setProperty("tone", "ok")
        head.addWidget(relies)
        acts = label("acts here — not recorded", "chip", wrap=False)
        acts.setToolTip(
            "A persona publishes that it acts in a context as a `self` or `speaks` "
            "statement (SPEC-0001 §6.3). No mofn command writes one, so this wallet "
            "can only show where a persona relies.")
        head.addWidget(acts)
        c.add(holder(head))

        c.add(label(f"MEMBERS — DERIVED FROM {len(com.anchors)} "
                    f"ANCHOR{'S' if len(com.anchors) != 1 else ''}", "lab", wrap=False))
        t = _table(["NAME", "FINGERPRINT", "HOW THIS CONTEXT NAMES THEM", "ABOUT", "THRESHOLD"])
        t.setRowCount(len(com.members))
        for i, m in enumerate(com.members):
            role = m.role + ("" if m.known else " · not a key in this wallet")
            for j, v in enumerate([
                m.name + (" (yours)" if m.owned else ""),
                # A key with no label is already shown by its fingerprint, so
                # do not print it twice.
                "" if m.name.startswith("key:") else core.fingerprint(m.kid),
                role,
                m.about or "—",
                m.threshold or "—",
            ]):
                t.setItem(i, j, QTableWidgetItem(v))
        t.setFixedHeight(34 + 32 * max(len(com.members), 1))
        c.add(t)
        c.add(label(
            "Members are derived from this context's anchors (SPEC-0004 §4.2). "
            "A key you know but have not anchored here is not a member, however "
            "many statements it signed.", "cap"))

        c.add(label("ANCHORS", "lab", wrap=False))
        a = _table(["KEY", "ABOUT", "VALUES", "MAY DELEGATE", "NOTE"])
        a.setRowCount(len(com.anchors))
        for i, an in enumerate(com.anchors):
            depth = f"{an.depth} level{'s' if an.depth > 1 else ''}" if an.depth else "no"
            for j, v in enumerate([an.key, an.about, an.values, depth, an.note or ""]):
                a.setItem(i, j, QTableWidgetItem(v))
        a.setFixedHeight(34 + 32 * max(len(com.anchors), 1))
        c.add(a)
        return c
