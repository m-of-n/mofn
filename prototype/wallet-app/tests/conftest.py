"""Shared fixtures for the desktop wallet's tests (W-7, mofn#179).

`world` is a relying party's wallet with the W-4 slice cases ready to
check: green (Alice trusted), authorization fail (Alice not trusted) and
integrity fail (a file one byte different). Every app test runs against a
throwaway QSettings, so nothing touches the user's own preferences."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from mofn_app import core

FIXTURES = core.WALLET_SOURCE / "fixtures"
GOLDEN = FIXTURES / "golden"
VOCAB = str(core.EXAMPLE_VOCABULARY)
AT = "2026-10-15T00:00:00Z"
PASS = b"app test passphrase, not a secret"
STATEMENTS = [str(FIXTURES / "tv-4-attestation.stmt"), str(FIXTURES / "tv-3-define.stmt")]


def mofn(*args) -> subprocess.CompletedProcess:
    """The CLI in its own process: the reference the app must match."""
    return subprocess.run(
        [sys.executable, str(core.WALLET_SOURCE / "mofn"), *map(str, args)],
        capture_output=True, text=True, encoding="utf-8",
    )


@pytest.fixture(autouse=True)
def settings(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.delenv("MOFN_WALLET", raising=False)
    try:
        from PySide6.QtCore import QSettings
    except ImportError:
        return
    QSettings.setDefaultFormat(QSettings.Format.IniFormat)
    QSettings.setPath(QSettings.Format.IniFormat, QSettings.Scope.UserScope, str(tmp_path / "settings"))


@pytest.fixture
def world(tmp_path):
    s = core.Session(tmp_path / "wallet")
    assert s.init().ok
    assert s.key_gen("me", "person", PASS).ok
    assert s.key_import(str(FIXTURES / "tv-1-alice.pub.stmt"), "Alice").ok
    (tmp_path / "app.bin").write_bytes((FIXTURES / "artifact.bin").read_bytes())
    (tmp_path / "bad.bin").write_bytes(b"X" + (FIXTURES / "artifact.bin").read_bytes()[1:])

    class World:
        session = s
        root = tmp_path
        app = str(tmp_path / "app.bin")
        bad = str(tmp_path / "bad.bin")

        @staticmethod
        def trust_alice():
            assert s.root_add("Alice", "me", VOCAB, "build-provenance", ["reproducible"]).ok

        @staticmethod
        def add_persona(label, controller="person"):
            assert s.key_gen(label, controller, PASS).ok
            return s.find(label)

        @staticmethod
        def tag(says, about, value="reproducible", type_="build-provenance"):
            """`says` tags `about`'s identity key: a tag `about` received."""
            r = s.sign(says, None, VOCAB, type_, value, 30, PASS, subject_key=about)
            assert r.ok, r.err
            return r

        @staticmethod
        def cli_key_json(subject_key, *statements, as_=None, at=None):
            """The same check in the CLI's own process: the reference.

            `at` is pinned by the caller because the verdict carries the
            evaluation time, and two runs a second apart would differ."""
            args = ["--wallet", s.root, "check", *statements, "--subject-key",
                    subject_key, "--def", VOCAB, "--format", "json"]
            if as_:
                args += ["--as", as_]
            if at:
                args += ["--at", at]
            p = mofn(*args)
            return p.returncode, json.loads(p.stdout)

        @staticmethod
        def cli_json(artifact):
            p = mofn("--wallet", s.root, "check", *STATEMENTS, "--artifact", artifact,
                     "--def", VOCAB, "--at", AT, "--format", "json")
            return p.returncode, json.loads(p.stdout)

    return World


@pytest.fixture
def two(world):
    """`world` plus a second owned persona, so personas can be switched.

    `world` keeps exactly one, so the W-7 tests go on meaning what they
    meant; the two-persona cases ask for this fixture instead."""
    world.add_persona("work", "organisation")
    return world
