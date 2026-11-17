"""Verify: check the statements you were handed (`mofn check --format
json`), shown as rows, top to bottom (mockup v2, approved 2026-11-17):

1. Authorization, prominent, with YES / NO
2. The other five lines, in one row
3. Subject: the sentence, the file, its digest, the claim, the vocabulary
4. Signed by
5. Standing: the chain (timeline rows) or the same chain in words
6. The limit line

Everything shown is read from the CLI's JSON (W-5's `associations` for 3–5),
so the app shows the CLI's verdict; nothing here decides anything."""

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QWidget

from .. import core
from ..widgets import Card, Chain, FileField, Page, Rows, Toggle, holder, label

OTHER = ("integrity", "authenticity", "names", "acceptance", "semantics")


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
        self.reload()

    def reload(self):
        cur = self.context.currentText() or "default"
        self.context.clear()
        self.context.addItems(self.app.session.contexts())
        self.context.setCurrentText(cur)
        me = self.app.identity
        self.subline.setText(
            f"Checked as {me.label}, against the roots you trust."
            if me
            else "Pick the statements you were handed and the file they are about."
        )

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
        r, j = self.app.session.check(
            self.statements.files(), self.subject.text(), self.vocab.text(),
            self.context.currentText() or "default", self.at.text().strip() or None,
        )
        self.app.ran(r)
        if j is None:
            return self.error(self.form, r.error)
        self.json = j
        self.render(j)

    # ------------------------------------------------------------- render

    def render(self, j: dict):
        t = self.app.tokens
        v = j["verdict"]
        yes = j["answer"] == "yes"
        self.h2.setText(self.subject.text().rsplit("/", 1)[-1] or "Verify")

        auth = v["authorization"]
        ok = auth["result"] == "pass"
        a = Card("Authorization", tone="ok" if ok else "bad")
        top = QHBoxLayout()
        top.addWidget(label(f"<b style='font-size:14px'>{auth['sentence']}</b>"), 1)
        chip = label("YES" if yes else "NO", "chip", wrap=False)
        chip.setProperty("tone", "ok" if yes else "bad")
        top.addWidget(chip)
        a.add(holder(top))
        self.results.addWidget(a)

        checks = Card("Checks")
        line = QHBoxLayout()
        for name in OTHER:
            res = v[name]["result"]
            line.addWidget(label(("✓ " if res == "pass" else "✕ ") + name.capitalize(),
                                 "ok" if res == "pass" else "bad", wrap=False))
            line.addStretch(1)
        checks.add(holder(line))
        for name in OTHER:
            if v[name]["result"] != "pass":
                checks.add(label(f"{name.capitalize()}: {v[name]['sentence']}", "bad"))
                checks.tone("bad")
        self.results.addWidget(checks)

        assoc = j.get("associations") or []
        sentences = j.get("sentences") or []
        if not assoc:
            c = Card("Subject — what this is about")
            c.add(label("No verified attestation was handed over, so there is no subject, signer or standing to show.", "cap"))
            self.results.addWidget(c)
        for i, x in enumerate(assoc):
            self.results.addWidget(self.subject_card(x, sentences[i] if i < len(sentences) else None, j))
            self.results.addWidget(self.signer_card(x))
            self.results.addWidget(self.standing_card(x, t))
        self.results.addWidget(label(j["limit"], "cap"))

    def subject_card(self, x: dict, sentence: str | None, j: dict) -> Card:
        c = Card("Subject — what this is about")
        if sentence:
            c.add(label(f"“{sentence}”"))
        if not j.get("sentences_about_your_file", True):
            c.add(label("These statements are about another file, not the one you picked.", "bad"))
            c.tone("bad")
        s, topic = x["subject"], x["topic"]
        rows = Rows(110)
        name = self.subject.text().rsplit("/", 1)[-1]
        rows.row("File", label(f"{name} · " + ("<span style='color:%s'>matches the file you picked ✓</span>" % self.app.tokens["ok"]
                                                if s["matches"] else "<span style='color:%s'>does not match ✕</span>" % self.app.tokens["bad"])))
        rows.row("Digest", label(s["digest"] or "—", "mono"))
        if not s["matches"]:
            rows.row("Yours", label(s["yours"] or "—", "mono"))
        rows.row("Claim", label(f"{topic['type-name']} = <b>{topic['value-name']}</b>"))
        rows.row("Vocabulary", topic["domain"])
        c.add(holder(rows))
        return c

    def signer_card(self, x: dict) -> Card:
        c = Card("Signed by")
        sb = x["signed-by"]
        rows = Rows(110)
        rows.row("Key", label(f"<b>{sb['key']}</b> · <span style='font-family:Menlo'>{sb['kid'][:4]} {sb['kid'][4:8]} …</span>"))
        if sb.get("principal"):
            rows.row("Named", sb["principal"])
        rows.row("In your wallet", "your label for this key" if sb.get("label") else "not named by you")
        c.add(holder(rows))
        return c

    def standing_card(self, x: dict, t: dict) -> Card:
        st = x["standing"]
        c = Card(tone=None)
        head = QHBoxLayout()
        head.addWidget(label("STANDING — WHY THEY MAY SAY IT", "lab", wrap=False), 1)
        view = QSettings().value("standing/view", "Chain")
        toggle = Toggle(["Chain", "In words"], view)
        head.addWidget(toggle)
        c.add(holder(head))
        chain = Chain(st, x["signed-by"]["key"], t)
        words = label(core.standing_words(st, x["signed-by"]["key"]))
        c.add(chain)
        c.add(words)
        chain.setVisible(view == "Chain")
        words.setVisible(view != "Chain")

        def pick(o):
            QSettings().setValue("standing/view", o)
            chain.setVisible(o == "Chain")
            words.setVisible(o != "Chain")

        toggle.picked.connect(pick)
        if st["result"] != "standing":
            c.tone("bad")
        return c
