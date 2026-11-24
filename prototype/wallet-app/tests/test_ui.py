"""The window, driven headless (pytest-qt, QT_QPA_PLATFORM=offscreen):
every page opens, the forms do what their command does, and Verify shows
the CLI's verdict with the four attributes for the slice cases."""

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QWidget,
)

from conftest import AT, FIXTURES, PASS, STATEMENTS, VOCAB

from mofn_app import core
from mofn_app.widgets import Chain

pytestmark = pytest.mark.usefixtures("settings")


@pytest.fixture
def win(qtbot, world):
    from mofn_app.window import Window

    w = Window(world.session.root)
    qtbot.addWidget(w)
    w.show()
    return w


def texts(widget) -> str:
    QApplication.processEvents()  # a layout shows new children on the next event-loop turn
    return "\n".join(l.text() for l in widget.findChildren(QLabel) if l.isVisibleTo(widget))


def test_every_page_opens(win):
    for name in ["Overview", "Personas", "Keys", "Trust", "Communities",
                 "Sign", "Verify", "Show", "Learn"]:
        win.go(name)
        assert win.stack.currentWidget() is win.pages[name]
        assert win.title.text() == name


def test_identity_is_the_wallets_owned_persona(win):
    assert win.identity.label == "me"
    assert "me" in win.who.text()


def test_a_missing_wallet_can_be_created(qtbot, tmp_path):
    from mofn_app.window import Window

    w = Window(tmp_path / "fresh")
    qtbot.addWidget(w)
    o = w.pages["Overview"]
    assert o.empty.isVisibleTo(o)
    w.create_here()
    assert w.session.exists and not o.empty.isVisibleTo(o)
    assert w.cmd.text().endswith(" init")


def test_new_identity_dialog_checks_the_passphrase_twice(win, qtbot):
    from mofn_app.window import NewIdentity

    d = NewIdentity(win)
    d.name.setText("Zoe")
    d.p1.setText("one")
    d.p2.setText("two")
    d.check()
    assert "differ" in d.err.text() and d.p2.text() == ""
    d.p2.setText("one")
    d.check()
    name, kind, secret = d.take()
    assert (name, kind, secret) == ("Zoe", "person", b"one")
    assert d.p1.text() == d.p2.text() == ""


def test_sign_writes_a_statement_and_clears_the_passphrase(win, world, qtbot):
    win.go("Sign")
    p = win.pages["Sign"]
    p.subject.set(world.app)
    assert p.digest.text().startswith("sha-256:")
    p.claim.setCurrentText("build-provenance")
    p.value.setCurrentText("reproducible")
    qtbot.keyClicks(p.passphrase, PASS.decode())
    assert p.passphrase.echoMode() == QLineEdit.EchoMode.Password
    qtbot.keyClick(p.passphrase, Qt.Key.Key_Return)
    assert p.passphrase.text() == ""
    assert p.done.isVisibleTo(p), win.state.text()
    assert p.written.text().endswith(".stmt")
    assert PASS.decode() not in win.cmd.text()
    assert win.cmd.text().startswith("mofn --wallet ") and " make --as me " in win.cmd.text()


def test_trust_form_adds_a_root(win):
    win.go("Trust")
    t = win.pages["Trust"]
    t.key.setCurrentText("Alice")
    t.claim.setCurrentText("build-provenance")
    for c in t.checks:
        c.setChecked(c.text() == "reproducible")
    t.depth.setValue(1)
    t.trust()
    assert t.table.rowCount() == 1
    assert [t.table.item(0, i).text() for i in range(4)] == ["Alice", "build-provenance", "reproducible", "1 level"]


def verify(win, world, artifact):
    win.go("Verify")
    v = win.pages["Verify"]
    v.at.setText(AT)
    v.prefill(statements=STATEMENTS, subject=artifact, vocab=VOCAB)
    return v


@pytest.mark.parametrize("case", ["green", "unauthorized", "tampered"])
def test_verify_shows_the_cli_verdict_and_the_four(win, world, case):
    if case != "unauthorized":
        world.trust_alice()
    artifact = world.bad if case == "tampered" else world.app
    v = verify(win, world, artifact)
    _, cli = world.cli_json(artifact)
    assert v.json == cli
    shown = texts(v.result)
    assert ("YES" if case == "green" else "NO") in shown
    assert cli["verdict"]["authorization"]["sentence"] in shown
    for title in ["AUTHORIZATION", "CHECKS", "SUBJECT — WHAT THIS IS ABOUT", "SIGNED BY", "STANDING — WHY THEY MAY SAY IT"]:
        assert title in shown, title
    a = cli["associations"][0]
    assert a["signed-by"]["key"] in shown
    assert a["topic"]["value-name"] in shown
    assert a["subject"]["digest"] in shown
    assert cli["limit"] in shown
    if case == "tampered":
        assert "✕ Integrity" in shown


def test_standing_toggle_switches_to_words_and_is_remembered(win, world):
    world.trust_alice()
    v = verify(win, world, world.app)
    texts(v.result)
    chain = v.result.findChild(Chain)
    assert chain.isVisibleTo(v.result)
    from mofn_app.widgets import Toggle

    toggle = v.result.findChild(Toggle)
    [b for b in toggle.group.buttons() if b.text() == "In words"][0].click()
    assert "So Alice may say this." in texts(v.result)
    assert not chain.isVisibleTo(v.result)
    v.verify()
    texts(v.result)
    assert not v.result.findChild(Chain).isVisibleTo(v.result)


def test_sign_then_verify_it(win, world, qtbot):
    world.trust_alice()
    assert world.session.root_add("me", "me", VOCAB, "build-provenance", ["reproducible"]).ok
    win.refresh()
    win.go("Sign")
    p = win.pages["Sign"]
    p.subject.set(world.app)
    p.value.setCurrentText("reproducible")
    p.passphrase.setText(PASS.decode())
    p.sign()
    p.verify_it()
    v = win.pages["Verify"]
    assert win.stack.currentWidget() is v
    assert v.json and v.json["answer"] == "yes"


def test_keys_import_and_table(win, world):
    win.go("Keys")
    k = win.pages["Keys"]
    assert k.table.rowCount() == 2
    k.file.set(str(FIXTURES / "tv-1-alice.pub.stmt"))
    k.name.setText("Alice twice")
    k.do_import()
    assert "mofn --wallet" in win.cmd.text() and " key import " in win.cmd.text()


def test_show_decodes_a_statement(win):
    win.go("Show")
    s = win.pages["Show"]
    s.open(STATEMENTS[0])
    assert "attestation" in texts(s.card)
    assert "envelope" in s.text.toPlainText()


def test_learn_has_the_tui_pages(win):
    win.go("Learn")
    l = win.pages["Learn"]
    assert l.list.count() == len(core.learn_pages()) == 6
    l.list.setCurrentRow(3)
    assert "Sign" in l.doc.toPlainText()


def test_sidebar_collapses_to_icons_and_back(win):
    win.set_collapsed(True)
    assert win.side.width() == 56
    assert all(b.text() == "" for b, _ in win.navs.values())
    win.set_collapsed(False)
    assert win.navs["Verify"][0].text() == "Verify"


def test_theme_switches(win):
    win.set_scheme("Light")
    assert win.tokens is __import__("mofn_app.theme", fromlist=["LIGHT"]).LIGHT
    win.set_scheme("Dark")
    assert win.tokens["bg"] == "#0c0c0e"


def test_the_prototype_warning_is_always_shown(win):
    assert "PROTOTYPE" in win.badge.text()
    assert "DEC-004" in win.badge.toolTip()


# ------------------------------------------------- W-8: several personas


@pytest.fixture
def win2(qtbot, two):
    """The window on a wallet with two owned personas (W-8, mofn#180)."""
    from mofn_app.window import Window

    w = Window(two.session.root)
    qtbot.addWidget(w)
    w.show()
    w.pick_identity("me")  # "me" sorts first, but say so rather than rely on it
    return w


def test_personas_page_lists_both_with_their_fingerprints(win2):
    win2.go("Personas")
    p = win2.pages["Personas"]
    assert p.mine.rowCount() == 2
    names = {p.mine.item(i, 1).text() for i in range(2)}
    assert names == {"me", "work"}
    prints = {p.mine.item(i, 3).text() for i in range(2)}
    assert len(prints) == 2 and all(f.startswith("key:") for f in prints)
    kinds = {p.mine.item(i, 2).text() for i in range(2)}
    assert kinds == {"person · self-claimed", "organisation · self-claimed"}
    assert "SPEC-0001 §3.1" in texts(p), "the unlinkability sentence is on screen"


def test_the_sidebar_offers_both_identities(win2):
    actions = [a for a in win2.who.menu().actions() if a.isCheckable()]
    assert {a.text().split(" ")[0] for a in actions} >= {"me", "work"}
    assert sum(1 for a in actions if a.isChecked()) == 1


def test_acting_as_another_persona_switches_the_signing_key(win2, two, qtbot):
    win2.go("Personas")
    win2.pages["Personas"].fill()
    buttons = [b for b in win2.pages["Personas"].acts.findChildren(QPushButton)]
    assert [b.text() for b in buttons] == ["Act as work"]
    buttons[0].click()
    assert win2.identity.label == "work"

    win2.go("Sign")
    s = win2.pages["Sign"]
    s.subject.set(two.app)
    s.claim.setCurrentText("build-provenance")
    s.value.setCurrentText("reproducible")
    qtbot.keyClicks(s.passphrase, PASS.decode())
    qtbot.keyClick(s.passphrase, Qt.Key.Key_Return)
    assert " make --as work " in win2.cmd.text()


def test_switching_persona_clears_a_verdict_computed_as_the_other(win2, two):
    two.trust_alice()  # accepted by "me" only
    win2.refresh()
    v = win2.pages["Verify"]
    win2.go("Verify")
    v.statements.set("; ".join(STATEMENTS))
    v.subject.set(two.app)
    v.vocab.set(VOCAB)
    v.at.setText(AT)
    v.verify()
    assert v.json is not None and v.json["answer"] == "yes"
    assert " --as me " in win2.cmd.text() + " "

    win2.pick_identity("work")
    assert v.json is None, "a verdict computed as `me` is not `work`'s verdict"
    assert "work" in win2.state.text()
    v.verify()
    assert v.json["answer"] == "no", "work trusts nobody"
    assert " --as work " in win2.cmd.text() + " "


def test_the_context_list_follows_the_persona(win2, two):
    s = two.session
    assert s.root_add("Alice", "work", VOCAB, "build-provenance", [], context="studio").ok
    win2.refresh()
    v = win2.pages["Verify"]
    win2.go("Verify")
    offered = [v.context.itemText(i) for i in range(v.context.count())]
    assert offered == ["default"], "me has no studio"
    win2.pick_identity("work")
    offered = [v.context.itemText(i) for i in range(v.context.count())]
    assert offered == ["default", "studio"]


def test_a_received_tag_shows_the_six_lines(win2, two):
    two.trust_alice()
    assert two.session.root_add("me", "me", VOCAB, "build-provenance", ["reproducible"]).ok
    two.tag("me", "work")
    win2.pick_identity("work")
    win2.go("Personas")
    p = win2.pages["Personas"]
    rows = p.tags_box.findChildren(QWidget)
    row = next(w for w in p.tags_box.children() if hasattr(w, "check"))
    assert "me" in texts(row) and "says" in texts(row)
    row.check()
    shown = texts(row)
    for line in core.LINES:
        assert line.capitalize() in shown or line in shown.lower(), line
    assert "YES" in shown or "NO" in shown
    assert " --subject-key work " in win2.cmd.text() + " "
    assert " --as work " in win2.cmd.text() + " "


def test_communities_keeps_the_spec_word_and_says_members_are_derived(win2, two):
    two.trust_alice()
    win2.refresh()
    win2.go("Communities")
    shown = texts(win2.pages["Communities"])
    assert "SPEC-0004" in shown and "context" in shown.lower()
    assert "derived" in shown.lower()
    # The members are a table, not labels: read the cells.
    table = win2.pages["Communities"].list.itemAt(0).widget().findChildren(QTableWidget)[0]
    names = {table.item(i, 0).text() for i in range(table.rowCount())}
    assert names == {"me (yours)", "Alice"}


def test_communities_follow_the_active_persona(win2, two):
    s = two.session
    two.trust_alice()
    assert s.root_add("Alice", "work", VOCAB, "build-provenance", [], context="studio").ok
    win2.refresh()
    win2.go("Communities")
    assert "DEFAULT" in texts(win2.pages["Communities"])
    assert "STUDIO" not in texts(win2.pages["Communities"])
    win2.pick_identity("work")
    win2.go("Communities")
    assert "STUDIO" in texts(win2.pages["Communities"])


def test_the_prototype_warning_is_on_the_new_pages(win2):
    for name in ("Personas", "Communities"):
        win2.go(name)
        assert win2.badge.isVisibleTo(win2)
        assert "DEC-004" in win2.badge.toolTip() and "DEC-005" in win2.badge.toolTip()
