"""`mofn run`: the steps, the session, `run --check` and the screen (#127)."""

import asyncio
import dataclasses
import os
import subprocess
import sys

import pytest

import cli
from conftest import WALLET, run_mofn
from guide import check, session, steps
from guide.session import LINES, Session

PASS = b"guide test passphrase"


def test_every_command_is_one_the_cli_takes():
    p = cli.parser()
    for _, a in steps.ACTIONS:
        if a.argv:
            assert p.parse_args(list(a.argv)).command, a.argv


def test_no_command_or_environment_holds_the_passphrase(tmp_path):
    before = dict(os.environ)
    s = Session(tmp_path, passphrase=PASS)
    s.prepare()
    while s.advance():
        pass
    assert s.step == len(steps.STEPS)
    assert dict(os.environ) == before
    for _, a in steps.ACTIONS:
        assert PASS.decode() not in steps.shown(a.argv)
        assert "--passphrase-stdin" not in a.argv
    for f in tmp_path.rglob("*"):
        if f.is_file():
            assert PASS not in f.read_bytes()


def test_every_command_is_plain_mofn():
    for _, a in steps.ACTIONS:
        assert "--wallet" not in a.argv, a.argv


def test_mofn_wallet_is_set_aside(tmp_path, monkeypatch):
    real = tmp_path / "real-wallet"
    monkeypatch.setenv("MOFN_WALLET", str(real))
    s = Session(tmp_path / "guide", passphrase=PASS)
    s.prepare()
    while s.step < 3:
        assert s.advance().ok
    assert not real.exists()
    assert os.environ["MOFN_WALLET"] == str(real)
    assert (tmp_path / "guide" / "wallet").is_dir()


def test_each_check_names_the_line_it_decides():
    checks = [a for _, a in steps.ACTIONS if a.check]
    assert checks
    for a in checks:
        assert a.decides in LINES + ("",), a
        assert (a.code == 0) == (a.decides == ""), a


def test_the_questions_come_before_a_check():
    for step in steps.STEPS:
        if step.question:
            assert any(a.check and a.decides for a in step.actions), step.title
    assert [n for n, s in enumerate(steps.STEPS) if s.question] == [2, 3]


def test_the_files_are_alices_fixtures(tmp_path):
    s = Session(tmp_path)
    s.prepare()
    for name, fixture in steps.FILES.items():
        assert (tmp_path / name).read_bytes() == (session.FIXTURES / fixture).read_bytes()


def test_a_wrong_expectation_is_caught(tmp_path):
    s = Session(tmp_path, passphrase=PASS)
    s.prepare()
    while s.step < 2:
        assert s.advance().ok
    n, a = steps.ACTIONS[s.done]
    o = s.do(dataclasses.replace(a, decides="", code=0))
    assert not o.ok
    assert any("first line to fail is authenticity" in p for p in o.problems)
    assert any("exit 1, expected 0" in p for p in o.problems)


def test_progress_survives_a_new_session(tmp_path):
    s = Session(tmp_path, passphrase=PASS)
    s.prepare()
    while s.step < 3:
        s.advance()
    again = Session(tmp_path)
    assert again.step == 3 and not again.needs_passphrase(3)
    assert again.advance().ok
    again.reset()
    assert Session(tmp_path).done == 0
    assert (tmp_path / "artifact.bin").exists()
    assert not (tmp_path / "wallet").exists()


def test_a_resume_before_signing_asks_again(tmp_path):
    s = Session(tmp_path, passphrase=PASS)
    s.prepare()
    while s.step < 7:
        assert s.advance().ok
    again = Session(tmp_path)
    assert again.needs_passphrase(7)
    assert not again.needs_passphrase(4)


def test_run_check(capsys):
    assert check.run_all() == 0
    out = capsys.readouterr().out
    assert out.endswith(f"run --check: 8 steps, {len(steps.ACTIONS)} actions passed\n")
    assert "[FAILED]" not in out


def test_run_check_from_the_command_line():
    p = run_mofn("run", "--check")
    assert p.returncode == 0, p.stdout + p.stderr


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
    assert "run needs a terminal" in p.stderr


def test_the_menu_lists_run_first():
    menu = run_mofn().stdout
    assert menu.split("Commands:\n")[1].startswith("  run ")
    assert "\n  mofn run " in menu


def test_the_screen_walks_four_steps(tmp_path):
    pytest.importorskip("textual")
    from guide.screen import Run

    async def walk():
        app = Run(tmp_path)
        async with app.run_test(size=(110, 40)) as pilot:
            await pilot.press("enter")
            assert app.asking == "passphrase"
            await pilot.press(*"typed here")
            await pilot.press("enter")
            await pilot.pause()
            assert app.session.step == 1
            await pilot.press("enter", "enter")
            await pilot.pause()
            assert app.session.step == 2
            await pilot.press("enter", "enter")
            assert app.asking == "answer"
            await pilot.press("2", "enter")
            await pilot.pause()
            assert app.session.step == 3
            assert 3 not in app.answers
            await pilot.press("enter", "enter")
            assert app.asking == "answer"
            await pilot.press("4", "enter")
            await pilot.pause()
            assert app.session.step == 4
            await pilot.press("q")

    asyncio.run(walk())
    assert Session(tmp_path).step == 4
    for f in tmp_path.rglob("*"):
        if f.is_file():
            assert b"typed here" not in f.read_bytes()


def test_run_without_textual_says_what_to_install(tmp_path):
    code = (
        "import sys; sys.modules['textual'] = None; "
        "sys.stdin.isatty = sys.stdout.isatty = lambda: True; "
        f"sys.path.insert(0, {str(WALLET)!r}); import cli; "
        f"sys.exit(cli.main(['run', '--dir', {str(tmp_path)!r}]))"
    )
    p = subprocess.run(
        [sys.executable, "-c", code],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
    )
    assert p.returncode == 2, p.stderr
    assert len(p.stderr.splitlines()) == 1
    assert "needs Textual" in p.stderr and "requirements.txt" in p.stderr
