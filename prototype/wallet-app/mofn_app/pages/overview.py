"""Overview: what this wallet holds, as six counts (mockup v1, graphite).

No context switcher (removed 2026-11-17): a verdict is computed in one
context, chosen on Verify and Trust under *More options*; W-8 (#180) gives
contexts their own page as communities."""

from PySide6.QtWidgets import QGridLayout, QPushButton

from ..widgets import Card, Page, label


class Overview(Page):
    pill = "Wallet"
    title = "Overview"
    sub = "Your identities, the keys you know, and who you trust. Nothing leaves this Mac."

    def build(self):
        self.empty = self.add(Card("No wallet here yet"))
        self.where = self.empty.add(label("", "sub"))
        make = QPushButton("Create this wallet")
        make.setObjectName("primary")
        make.clicked.connect(self.app.create_here)
        self.empty.add(make)
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.cards = {}
        for i, (key, title) in enumerate(
            [
                ("owned", "Your identities"),
                ("known", "Keys you know"),
                ("anchors", "Trusted roots"),
                ("statements", "Statements"),
                ("definitions", "Vocabularies"),
                ("contexts", "Contexts"),
            ]
        ):
            c = Card(title)
            big = c.add(label("0", "big"))
            cap = c.add(label("", "cap"))
            self.cards[key] = (big, cap)
            self.grid.addWidget(c, i // 3, i % 3)
        self.body.addLayout(self.grid)
        self.reload()

    def reload(self):
        s = self.app.session
        self.h2.setText(s.root.name)
        self.empty.setVisible(not s.exists)
        self.where.setText(f"{s.root} has no wallet. Create one here, or pick another wallet below the sidebar.")
        n = s.counts()
        if not n:
            for big, cap in self.cards.values():
                big.setText("–")
                cap.setText("")
            return
        names = lambda ps: ", ".join(p.label or p.kid.hex()[:8] for p in ps[:3]) + ("…" if len(ps) > 3 else "")
        text = {
            "owned": (len(n["owned"]), names(n["owned"]) or "none yet: + New identity"),
            "known": (len(n["known"]), names(n["known"]) or "import one on Keys"),
            "anchors": (n["anchors"], "keys you decided to believe" if n["anchors"] else "none: verdicts will say no standing"),
            "statements": (n["statements"], "made here or collected"),
            "definitions": (n["definitions"], "vocabularies used for trust"),
            "contexts": (len(n["contexts"]), " · ".join(n["contexts"])),
        }
        for k, (big, cap) in self.cards.items():
            big.setText(str(text[k][0]))
            cap.setText(text[k][1])
