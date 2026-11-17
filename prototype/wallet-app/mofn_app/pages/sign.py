"""Sign: one statement about one file, as the active identity (`mofn make`).

The passphrase is a masked field. Its bytes go to `cli.main` in this
process and the field is cleared straight after; it is never put in argv,
the environment, settings or the status bar."""

from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLineEdit, QPushButton, QSpinBox

from .. import core
from ..widgets import Card, FileField, Page, Rows, holder, label


class Sign(Page):
    pill = "Sign"
    title = "Sign one statement about a file"
    sub = ""

    def build(self):
        f = self.form = self.add(Card())
        rows = Rows()
        self.subject = rows.row("File", FileField("the file you are vouching for"))
        self.subject.changed.connect(self.show_digest)
        self.digest = rows.row("Its digest", label("", "mono"))
        self.vocab = rows.row("Vocabulary", FileField("a .def file", filter="Vocabularies (*.def)"))
        self.vocab.set(str(core.EXAMPLE_VOCABULARY))
        self.vocab.changed.connect(self.offer_claims)
        self.claim = rows.row("Claim", QComboBox())
        self.claim.currentTextChanged.connect(self.offer_values)
        self.value = rows.row("Value", QComboBox())
        self.days = rows.row("Valid for", QSpinBox())
        self.days.setRange(1, 3650)
        self.days.setValue(30)
        self.days.setSuffix(" days")
        self.out = rows.row("Save to", FileField("default: the wallet's statements folder", mode="save"))
        self.passphrase = rows.row("Passphrase", QLineEdit())
        self.passphrase.setEchoMode(QLineEdit.EchoMode.Password)
        self.passphrase.setPlaceholderText("your identity's passphrase — never stored")
        self.passphrase.returnPressed.connect(self.sign)
        f.add(holder(rows))
        go = QPushButton("Sign")
        go.setObjectName("primary")
        go.clicked.connect(self.sign)
        f.add(go)

        self.done = self.add(Card("Signed", tone="ok"))
        self.sentence = self.done.add(label(""))
        dr = Rows()
        self.written = dr.row("Written to", label("", "mono"))
        nxt = QHBoxLayout()
        verify = QPushButton("Verify it")
        verify.clicked.connect(self.verify_it)
        nxt.addWidget(verify)
        nxt.addStretch(1)
        dr.row("Next", holder(nxt))
        self.done.add(holder(dr))
        self.done.setVisible(False)
        self.offer_claims()
        self.reload()

    def reload(self):
        me = self.app.identity
        self.subline.setText(
            f"Signing as {me.label}. Anyone with your key file can check it; nobody can change it."
            if me
            else "You have no identity in this wallet yet: + New identity."
        )

    def show_digest(self, path: str):
        try:
            self.digest.setText(core.digest_text(path) if path else "")
        except OSError:
            self.digest.setText("")

    def offer_claims(self, *_):
        self.claim.clear()
        self.claim.addItems(core.claims(core.vocabulary(self.vocab.text())))

    def offer_values(self, claim: str):
        self.value.clear()
        self.value.addItems(core.values(core.vocabulary(self.vocab.text()), claim))

    def sign(self):
        self.form.tone(None)
        me = self.app.identity
        if me is None:
            return self.error(self.form, "Make an identity first: + New identity.")
        if not (self.subject.text() and self.claim.currentText() and self.value.currentText()):
            return self.error(self.form, "Pick the file, the claim and its value.")
        secret = self.passphrase.text().encode("utf-8")
        self.passphrase.clear()
        r = self.app.run(
            self.app.session.sign(
                me.label, self.subject.text(), self.vocab.text(), self.claim.currentText(),
                self.value.currentText(), self.days.value(), secret, self.out.text() or None,
            )
        )
        del secret
        if not r.ok:
            self.done.setVisible(False)
            return self.error(self.form, r.error)
        lines = r.out.strip().splitlines()
        self.written.setText(lines[0].removeprefix("wrote ") if lines else "")
        self.sentence.setText(f"“{lines[1]}”" if len(lines) > 1 else "")
        self.done.setVisible(True)

    def verify_it(self):
        """Open Verify on what was just signed. With the example vocabulary,
        also hand over its definer's define statement, as a relying party
        would be handed it."""
        stmts = [self.written.text()]
        if self.vocab.text() == str(core.EXAMPLE_VOCABULARY):
            stmts.append(str(core.EXAMPLE_DEFINE))
        self.app.go("Verify", statements=stmts, subject=self.subject.text(), vocab=self.vocab.text())
