"""`mofn run`: every screen, driven headless with Textual's pilot (#127 §2)."""

import ast
import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("textual")

from textual.widgets import Input, ListView, Static, TabbedContent

import cli
from conftest import WALLET, run_mofn
from screens import forms, learn, runner
from screens.app import TABS, WalletApp

PASS = "pilot passphrase, not a secret"
GOLDENS = ("green", "unauthorized", "unknown-key", "tampered", "statement-changed", "expired")


def drive(script, size=(130, 60)):
    async def go():
        app = WalletApp(None, None)
        async with app.run_test(size=size) as pilot:
            await pilot.pause()
            await script(app, pilot)
        return app

    return asyncio.run(go())


async def first_run(app, pilot, name="me", example=True):
    fr = app.screen
    fr.query_one("#first-name", Input).value = name
    fr.query_one("#first-pass", Input).value = PASS
    fr.query_one("#first-again", Input).value = PASS
    if not example:
        fr.query_one("#first-example").value = False
    await pilot.pause()
    await pilot.click("#first-go")
    await pilot.pause()


async def tab(app, pilot, name):
    app.query_one(TabbedContent).active = name
    await pilot.pause()


async def passphrase(app, pilot):
    app.screen.query_one("#ask-1", Input).value = PASS
    confirm = app.screen.query("#ask-2")
    if confirm:
        confirm.first().value = PASS
    await pilot.click("#ask-ok")
    await pilot.pause()


async def set_(form, pilot, **values):
    for key, v in values.items():
        form.w(key).value = v
        await pilot.pause()


LIST = ["key", "list", "--format", "json"]


def ran(spy) -> list[list[str]]:
    return [a for a, _ in spy if a != LIST]


def runs(form) -> str:
    return str(form.query_one(f"#{form.NAME}-runs", Static).content)


@pytest.fixture
def here(tmp_path, monkeypatch):
    monkeypatch.delenv("MOFN_WALLET", raising=False)
    monkeypatch.chdir(tmp_path)
    return tmp_path


@pytest.fixture
def spy(monkeypatch):
    seen = []
    real = runner.run

    def run(argv, passphrase=None):
        seen.append((list(argv), passphrase))
        return real(argv, passphrase)

    monkeypatch.setattr(runner, "run", run)
    return seen


def test_first_run_makes_the_wallet_your_key_and_the_example(here, spy):
    async def script(app, pilot):
        assert type(app.screen).__name__ == "FirstRun"
        await first_run(app, pilot)
        assert type(app.screen).__name__ != "FirstRun"
        summary = str(app.query_one("#wallet-summary", Static).content)
        assert "me" in summary and "Alice (definer)" in summary
        assert "Made your wallet" in str(app.query_one("#wallet-result", Static).content)

    drive(script)
    assert (here / "wallet" / "wallet.yaml").is_file()
    assert (here / "me.pub.stmt").is_file()
    assert sorted(p.name for p in (here / "example").iterdir()) == [
        "alice-define.stmt",
        "alice.pub.stmt",
        "alice.stmt",
        "artifact.bin",
        "dv-1.def",
    ]
    assert LIST in [a for a, _ in spy]
    assert ran(spy) == [
        ["init"],
        ["key", "gen", "me", "-o", "me.pub.stmt"],
        ["key", "import", "example/alice.pub.stmt", "--label", "Alice (definer)"],
    ]


def test_first_run_refuses_passphrases_that_differ(here):
    async def script(app, pilot):
        fr = app.screen
        fr.query_one("#first-pass", Input).value = "one"
        fr.query_one("#first-again", Input).value = "two"
        await pilot.click("#first-go")
        await pilot.pause()
        assert type(app.screen).__name__ == "FirstRun"
        assert "differ" in str(fr.query_one("#first-err", Static).content)

    drive(script)
    assert not (here / "wallet").exists()


def test_first_run_can_be_left_without_making_anything(here):
    async def script(app, pilot):
        await pilot.press("escape")
        await pilot.pause()
        assert not app.is_running

    drive(script)
    assert list(here.iterdir()) == []


def test_choices_come_from_the_wallet_and_the_vocabulary(here):
    async def script(app, pilot):
        await first_run(app, pilot)
        await tab(app, pilot, "trust")
        t = app.query_one(forms.Trust)
        assert [v for _, v in t.w("whose")._offered] == ["Alice (definer)"]
        assert [v for _, v in t.w("as")._offered] == ["me"]
        await tab(app, pilot, "sign")
        s = app.query_one(forms.Sign)
        assert [v for _, v in s.w("as")._offered] == ["me"]
        assert [v for _, v in s.w("claim")._offered] == ["build-provenance", "outcome"]
        await set_(s, pilot, claim="outcome")
        assert [v for _, v in s.w("value")._offered] == ["approve", "changes", "reject"]

    drive(script)


def test_the_runs_line_is_the_command_that_runs(here, spy):
    async def script(app, pilot):
        await first_run(app, pilot)
        await tab(app, pilot, "trust")
        t = app.query_one(forms.Trust)
        await set_(t, pilot, whose="Alice (definer)")
        t.w("values").select("reproducible")
        await pilot.pause()
        shown = runs(t)
        await pilot.click("#trust-go")
        await pilot.pause()
        assert shown == "Runs   " + runner.shown(ran(spy)[-1])
        assert ran(spy)[-1] == [
            "root",
            "add",
            "Alice (definer)",
            "--as",
            "me",
            "--def",
            "example/dv-1.def",
            "--type",
            "build-provenance",
            "--values",
            "reproducible",
        ]
        assert "trusted in default about build-provenance" in str(
            t.query_one("#trust-anchors", Static).content
        )

    drive(script)


def test_check_shows_six_lines_and_marks_the_deciding_one(here, spy):
    async def script(app, pilot):
        await first_run(app, pilot)
        await tab(app, pilot, "check")
        c = app.query_one(forms.Check)
        await set_(c, pilot, add="example/alice.stmt")
        await pilot.click("#check-add-go")
        await pilot.pause()
        await set_(c, pilot, file="example/artifact.bin", at="2026-10-15T00:00:00Z")
        await pilot.click("#check-go")
        await pilot.pause()
        out = str(c.query_one("#check-result", Static).content)
        assert "▶ 4 authorization  fail" in out
        assert "answer: no" in out
        assert "it does not establish that it is true" in out
        assert ran(spy)[-1][:3] == ["check", "example/alice.stmt", "example/alice-define.stmt"]
        assert ran(spy)[-1][-2:] == ["--format", "json"]

    drive(script)


def test_an_engine_error_is_shown_on_its_field(here):
    async def script(app, pilot):
        await first_run(app, pilot)
        await tab(app, pilot, "keys")
        k = app.query_one(forms.KeyImport)
        await set_(k, pilot, file="example/alice-define.stmt", label="not a key")
        await pilot.click("#keyimport-go")
        await pilot.pause()
        err = str(k.query_one("#keyimport-file-err", Static).content)
        assert err.startswith("unverifiable at V3 (unknown-key)")
        assert k.v("file") == "example/alice-define.stmt" and k.v("label") == "not a key"
        assert str(k.query_one("#keyimport-err", Static).content) == ""

    drive(script)


def test_open_a_file(here):
    async def script(app, pilot):
        await first_run(app, pilot)
        app.action_open_file()
        await pilot.pause()
        show = app.screen.query_one(forms.Show)
        await set_(show, pilot, file="example/dv-1.def")
        assert runs(show) == "Runs   mofn show example/dv-1.def"
        await pilot.click("#show-go")
        await pilot.pause()
        assert str(show.query_one("#show-result", Static).content).startswith("definition ")

    drive(script)


def test_two_people_hand_over_a_key_and_a_signed_file(tmp_path, monkeypatch, spy):
    monkeypatch.delenv("MOFN_WALLET", raising=False)
    david, chip = tmp_path / "david", tmp_path / "chip"
    david.mkdir()
    chip.mkdir()

    async def sign(app, pilot):
        await first_run(app, pilot, "david")
        await tab(app, pilot, "sign")
        s = app.query_one(forms.Sign)
        await set_(s, pilot, file="example/artifact.bin", claim="outcome", value="approve")
        await pilot.click("#sign-go")
        await pilot.pause()
        await passphrase(app, pilot)

    monkeypatch.chdir(david)
    drive(sign)
    signed = david / "artifact.bin.stmt"
    assert signed.is_file()

    async def check(app, pilot):
        await first_run(app, pilot, "chip")
        await tab(app, pilot, "keys")
        k = app.query_one(forms.KeyImport)
        await set_(k, pilot, file=str(david / "david.pub.stmt"), label="David")
        await pilot.click("#keyimport-go")
        await pilot.pause()
        await tab(app, pilot, "trust")
        t = app.query_one(forms.Trust)
        await set_(t, pilot, whose="David", claim="outcome")
        t.w("values").select("approve")
        await pilot.pause()
        await pilot.click("#trust-go")
        await pilot.pause()
        await tab(app, pilot, "check")
        c = app.query_one(forms.Check)
        await set_(c, pilot, add=str(signed))
        await pilot.click("#check-add-go")
        await pilot.pause()
        await set_(c, pilot, file="example/artifact.bin")
        await pilot.click("#check-go")
        await pilot.pause()
        verdict = json.loads(app.last.out)
        assert verdict["answer"] == "yes", verdict["verdict"]
        assert "answer: yes" in str(c.query_one("#check-result", Static).content)

    monkeypatch.chdir(chip)
    drive(check)

    for argv, _ in spy:
        assert PASS not in " ".join(argv)
    assert PASS not in "".join(os.environ.values())
    for f in tmp_path.rglob("*"):
        if f.is_file():
            assert PASS.encode() not in f.read_bytes()


def test_learn_runs_nothing(here, monkeypatch):
    drive(first_run)
    before = {p: p.read_bytes() for p in here.rglob("*") if p.is_file()}

    def refuse(*a, **k):
        raise AssertionError("Learn ran a command")

    async def script(app, pilot):
        monkeypatch.setattr(runner, "run", refuse)
        monkeypatch.setattr(cli, "main", refuse)
        await tab(app, pilot, "learn")
        pages = app.query_one("#learn-list", ListView)
        for i in range(len(learn.pages())):
            pages.index = i
            await pilot.pause()
        app.query_one("#learn-go").press()
        await pilot.pause()
        assert app.query_one(TabbedContent).active == learn.pages()[-1].go

    drive(script)
    after = {p: p.read_bytes() for p in here.rglob("*") if p.is_file()}
    assert after == before


def test_learn_is_open_from_any_tab(here):
    async def script(app, pilot):
        await first_run(app, pilot)
        await tab(app, pilot, "sign")
        app.set_focus(None)
        await pilot.press("question_mark")
        assert app.query_one(TabbedContent).active == "learn"

    drive(script)


def test_learn_pages_show_the_goldens_and_the_readme():
    pages = learn.pages()
    assert [p.title for p in pages] == [
        "Your wallet",
        "Keys",
        "Trust",
        "Sign",
        "Check",
        "When a check fails",
    ]
    assert all(p.go in TABS for p in pages)
    failures = pages[-1].text
    for name in GOLDENS:
        assert learn.golden(name) in failures, name
    assert learn.section("What the six lines mean") in pages[4].text
    assert learn.section("The cases") in failures
    assert learn.section("What the wallet keeps") in pages[0].text
    for p in pages:
        assert "<!--" not in p.text


def test_learn_imports_no_command_code():
    tree = ast.parse(Path(learn.__file__).read_text(encoding="utf-8"))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names |= {a.name for a in node.names}
        elif isinstance(node, ast.ImportFrom):
            names |= {node.module or ""} | {a.name for a in node.names}
    assert not names & {"cli", "runner", "screens.runner", "engine"}


def test_run_without_a_terminal_refuses():
    p = subprocess.run(
        [sys.executable, str(WALLET / "mofn"), "run"],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
    )
    assert p.returncode == 2
    assert p.stderr == "mofn: error: run needs a terminal\n"


def test_run_without_textual_says_what_to_install(tmp_path):
    code = (
        "import sys; sys.modules['textual'] = None; "
        "sys.stdin.isatty = sys.stdout.isatty = lambda: True; "
        f"sys.path.insert(0, {str(WALLET)!r}); import cli; "
        "sys.exit(cli.main(['run']))"
    )
    p = subprocess.run(
        [sys.executable, "-c", code],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
        cwd=tmp_path,
    )
    assert p.returncode == 2, p.stderr
    assert len(p.stderr.splitlines()) == 1
    assert "needs Textual" in p.stderr and "requirements.txt" in p.stderr


def test_the_menu_lists_run_first():
    menu = run_mofn().stdout
    rows = menu.split("Commands:\n")[1]
    assert rows.startswith("  run                              open the wallet as a terminal app (start here)\n")
    assert "\n  mofn run                                    use your wallet through forms\n" in menu


def test_only_the_tab_scrolls_and_the_key_line_stays(here):
    async def script(app, pilot):
        await first_run(app, pilot)
        for name in TABS:
            await tab(app, pilot, name)
            await pilot.pause()
            help_line = app.query_one("#help")
            assert help_line.region.bottom <= app.screen.size.height, name
            assert help_line.region.height == 1, name
            assert app.screen.max_scroll_y == 0, name
            if name in ("keys", "check", "learn"):
                pane = app.query_one(TabbedContent).active_pane
                assert any(w.max_scroll_y > 0 for w in pane.query("VerticalScroll")), name

    drive(script, size=(80, 24))


def test_the_keys_table_is_key_list(here, spy):
    async def script(app, pilot):
        await first_run(app, pilot)
        await tab(app, pilot, "keys")
        table = app.query_one("#key-table")
        listed = json.loads(runner.run(LIST).out)["keys"]
        rows = [table.get_row_at(i) for i in range(table.row_count)]
        assert [r[0] for r in rows] == [k["label"] for k in listed] == ["me", "Alice (definer)"]
        assert [r[2] for r in rows] == ["yours", "known"]
        assert rows[1][4].startswith("example/alice.pub.stmt, ")

    drive(script)
    assert LIST in [a for a, _ in spy]


def test_export_sends_your_key_again(here, spy):
    async def script(app, pilot):
        await first_run(app, pilot)
        await tab(app, pilot, "keys")
        e = app.query_one(forms.KeyExport)
        assert e.v("as") == "me" and e.v("save") == "me.pub.stmt"
        await set_(e, pilot, save="again.pub.stmt")
        shown = runs(e)
        e.query_one("#keyexport-go").press()
        await pilot.pause()
        assert shown == "Runs   " + runner.shown(ran(spy)[-1])
        assert ran(spy)[-1] == ["key", "export", "me", "-o", "again.pub.stmt"]
        assert all(pp is None for a, pp in spy if a[:2] == ["key", "export"])

    drive(script)
    assert (here / "again.pub.stmt").read_bytes() == (here / "me.pub.stmt").read_bytes()


def test_open_hashes_a_file_that_is_not_a_statement(here, spy):
    async def script(app, pilot):
        await first_run(app, pilot)
        app.action_open_file()
        await pilot.pause()
        show = app.screen.query_one(forms.Show)
        await set_(show, pilot, file="example/artifact.bin")
        assert runs(show) == "Runs   mofn hash example/artifact.bin --format json"
        show.query_one("#show-go").press()
        await pilot.pause()
        out = str(show.query_one("#show-result", Static).content)
        assert out.startswith("sha-256:48dfc39586b0c4f9e905b3b60f59a30b7c0c7408e44f7cb4df2a09fbf3e67ba7")

    drive(script)
    assert ["hash", "example/artifact.bin", "--format", "json"] in ran(spy)
