"""One renderer for `mofn check --format json`, shared by Verify and Personas.

The rows are the ones approved for W-7 (mockup v2, 2026-11-17), in order:

1. Authorization, prominent, with YES / NO
2. The other five lines, in one row
3. Subject: the sentence, what it is about, the claim, the vocabulary
4. Signed by
5. Standing: the chain (timeline rows) or the same chain in words
6. The limit line

Everything shown is read from the CLI's JSON, so the app shows the CLI's
verdict; nothing here decides anything.

The subject may be a file digest or a key (`check --subject-key`, W-8): the
engine marks a key ask with `subject.target == "key"` and leaves the field
absent for a digest ask, so `subject_form` reads it with a default. This
module imports `widgets` and `core` only, never a page.
"""

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QHBoxLayout, QWidget

from . import core
from .widgets import Card, Chain, Rows, Toggle, holder, label

# The five lines beside authorization. Named once, from the engine's own list,
# so the six lines are not written out twice.
OTHER = tuple(n for n in core.LINES if n != "authorization")


def subject_form(subject: dict) -> str:
    """"key" or "digest": which shape `check` returned. A digest ask carries
    no `target`, so W-5's goldens and this renderer agree (DL-0049)."""
    return subject.get("target", "digest")


def cards(j: dict, *, shown: str, tokens: dict, names=None) -> list[QWidget]:
    """The whole verdict, top to bottom. `shown` is what the subject row
    names — the file you picked, or the persona whose key was asked about.
    `names` maps a kid to the wallet's label, for a key subject."""
    out = [answer_card(j), checks_card(j)]
    assoc = j.get("associations") or []
    sentences = j.get("sentences") or []
    if not assoc:
        c = Card("Subject — what this is about")
        c.add(label("No verified attestation was handed over, so there is no "
                    "subject, signer or standing to show.", "cap"))
        out.append(c)
    for i, x in enumerate(assoc):
        out.append(subject_card(x, sentences[i] if i < len(sentences) else None, j,
                                shown=shown, tokens=tokens, names=names or {}))
        out.append(signer_card(x))
        out.append(standing_card(x, tokens))
    out.append(label(j["limit"], "cap"))
    return out


def answer_card(j: dict) -> Card:
    auth = j["verdict"]["authorization"]
    yes = j["answer"] == "yes"
    c = Card("Authorization", tone="ok" if auth["result"] == "pass" else "bad")
    top = QHBoxLayout()
    top.addWidget(label(f"<b style='font-size:14px'>{auth['sentence']}</b>"), 1)
    chip = label("YES" if yes else "NO", "chip", wrap=False)
    chip.setProperty("tone", "ok" if yes else "bad")
    top.addWidget(chip)
    c.add(holder(top))
    return c


def checks_card(j: dict) -> Card:
    v = j["verdict"]
    c = Card("Checks")
    line = QHBoxLayout()
    for name in OTHER:
        res = v[name]["result"]
        line.addWidget(label(("✓ " if res == "pass" else "✕ ") + name.capitalize(),
                             "ok" if res == "pass" else "bad", wrap=False))
        line.addStretch(1)
    c.add(holder(line))
    for name in OTHER:
        if v[name]["result"] != "pass":
            c.add(label(f"{name.capitalize()}: {v[name]['sentence']}", "bad"))
            c.tone("bad")
    return c


def subject_card(x: dict, sentence: str | None, j: dict, *, shown: str,
                 tokens: dict, names: dict) -> Card:
    c = Card("Subject — what this is about")
    if sentence:
        c.add(label(f"“{sentence}”"))
    s, topic = x["subject"], x["topic"]
    key_ask = subject_form(s) == "key"
    if not j.get("sentences_about_your_file", True):
        c.add(label("These statements are about another key, not the one you named."
                    if key_ask else
                    "These statements are about another file, not the one you picked.", "bad"))
        c.tone("bad")
    rows = Rows(110)
    good = f"<span style='color:{tokens['ok']}'>%s ✓</span>"
    bad = f"<span style='color:{tokens['bad']}'>%s ✕</span>"
    if key_ask:
        kid = s.get("kid") or ""
        rows.row("Key", label(
            f"{shown} · " + (good % "this is the key you named" if s["matches"]
                             else bad % "this tag is about another key")))
        # `subject.key` is the wallet's own name for the key when it has one,
        # so it is not a fingerprint. Derive the fingerprint from the kid.
        rows.row("Key id", label(
            (core.fingerprint(bytes.fromhex(kid)) if kid else "—") + "  ·  " + kid, "mono"))
        if not s["matches"]:
            yours = s["yours"] or ""
            rows.row("You named", label(
                names.get(yours, core.fingerprint(bytes.fromhex(yours)) if yours else "—"),
                "mono"))
    else:
        rows.row("File", label(
            f"{shown} · " + (good % "matches the file you picked" if s["matches"]
                             else bad % "does not match")))
        rows.row("Digest", label(s["digest"] or "—", "mono"))
        if not s["matches"]:
            rows.row("Yours", label(s["yours"] or "—", "mono"))
    rows.row("Claim", label(f"{topic['type-name']} = <b>{topic['value-name']}</b>"))
    rows.row("Vocabulary", topic["domain"])
    c.add(holder(rows))
    return c


def signer_card(x: dict) -> Card:
    c = Card("Signed by")
    sb = x["signed-by"]
    rows = Rows(110)
    rows.row("Key", label(f"<b>{sb['key']}</b> · <span style='font-family:Menlo'>{sb['kid'][:4]} {sb['kid'][4:8]} …</span>"))
    if sb.get("principal"):
        rows.row("Named", sb["principal"])
    rows.row("In your wallet", "your label for this key" if sb.get("label") else "not named by you")
    c.add(holder(rows))
    return c


def standing_card(x: dict, t: dict) -> Card:
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
