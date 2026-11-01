"""Shared test data: the published vectors and the fixture directory."""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

WALLET = Path(__file__).resolve().parents[1]
FIXTURES = WALLET / "fixtures"
VECTORS = json.loads(
    (WALLET.parents[1] / "spec" / "vectors" / "ksa-core" / "vectors.json").read_text()
)


def keystore() -> dict:
    out = {}
    for k in VECTORS["keys"].values():
        pub = bytes.fromhex(k["pub"])
        out[(1, hashlib.sha256(pub).digest())] = pub
    return out


def seed(name: str) -> bytearray:
    return bytearray.fromhex(VECTORS["keys"][name]["seed"])


def envelope(name: str) -> bytes:
    return bytes.fromhex(VECTORS["positive"][name]["envelope"])


def run_mofn(*args, stdin: str = "", cwd=None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(WALLET / "mofn"), *map(str, args)],
        input=stdin,
        capture_output=True,
        text=True,
        cwd=cwd,
    )


@pytest.fixture
def vectors():
    return VECTORS
