"""The menu, `--version` and the missing-dependency message (#127)."""

import subprocess
import sys

import engine
from conftest import WALLET, run_mofn

MOFN = WALLET / "mofn"


def test_bare_mofn_prints_the_menu():
    bare, helped = run_mofn(), run_mofn("-h")
    assert bare.returncode == helped.returncode == 0
    assert bare.stdout == helped.stdout == run_mofn("--help").stdout
    assert bare.stdout.startswith(f"mofn {engine.__version__} (prototype: ")
    assert bare.stderr == ""


def test_menu_names_every_command():
    menu = run_mofn().stdout
    for command in (
        "init",
        "key gen",
        "key import",
        "root add",
        "root list",
        "make",
        "check",
        "show",
        "key list",
        "key export",
        "hash",
    ):
        assert f"\n  {command} " in menu, command


def test_menu_lists_only_commands_that_exist():
    menu = run_mofn().stdout
    listed = menu.split("Commands:\n")[1].split("\n\n")[0].splitlines()
    for row in listed:
        word = row.split()[0]
        assert run_mofn(word, "-h").returncode == 0, word


def test_per_command_help_is_kept():
    for args in (("key", "-h"), ("check", "-h"), ("root", "add", "-h")):
        p = run_mofn(*args)
        assert p.returncode == 0 and p.stdout.startswith("usage: mofn "), args


def test_version():
    p = run_mofn("--version")
    assert p.returncode == 0
    lines = p.stdout.splitlines()
    assert lines[0] == f"mofn {engine.__version__} (prototype)"
    assert [l.split(":")[0] for l in lines[1:]] == [
        "Follows",
        "Open",
        "Codecs",
        "Suite",
        "Wallet",
    ]
    assert "DEC-004, DEC-005" in lines[2]
    assert lines[3].endswith("ksa-cbor (default), review-yaml")
    assert "over PyNaCl " in lines[4]


def test_version_names_the_wallet_in_use(tmp_path):
    p = run_mofn("--wallet", tmp_path / "w", "--version")
    assert p.stdout.splitlines()[-1] == f"Wallet:  {tmp_path / 'w'}"


def test_version_is_semver():
    parts = engine.__version__.split(".")
    assert len(parts) == 3 and all(x.isdigit() for x in parts)


def test_changelog_has_this_version():
    changelog = (WALLET / "CHANGELOG.md").read_text(encoding="utf-8")
    assert f"\n## {engine.__version__} — " in changelog


def test_missing_pynacl_is_one_line():
    p = subprocess.run(
        [
            sys.executable,
            "-c",
            "import runpy, sys; sys.modules['nacl'] = None; "
            f"sys.argv = ['mofn']; runpy.run_path({str(MOFN)!r}, run_name='__main__')",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert p.returncode == 2
    assert p.stdout == ""
    assert "Traceback" not in p.stderr
    assert len(p.stderr.splitlines()) == 1
    assert "PyNaCl" in p.stderr and "requirements.txt" in p.stderr
