"""The second domain (mofn#66, W-2): the archives scenario of APP-0003 through
the same `mofn make` and `mofn check` as supply chain, under both codecs.

Only the domain file differs. Nothing here may need code that knows what a
library record is; if a case below only passes with such code, that is a
finding against the vocabulary claim, not a fix (PLAN-0004 §3).
"""

import subprocess
import sys

import pytest

from conftest import WALLET, run_mofn

PASS = "archives scenario passphrase"
DOMAIN = WALLET / "domains" / "archives"
DEF = DOMAIN / "archives.def"
GOLDEN = DOMAIN / "golden"
RECORD = (DOMAIN / "record.yaml").read_bytes()


def ok(p):
    assert p.returncode == 0, p.stderr + p.stdout
    return p


@pytest.fixture(scope="module", params=["ksa-cbor", "review-yaml"])
def library(request, tmp_path_factory):
    codec = request.param
    suffix = ".stmt" if codec == "ksa-cbor" else ".stmt.yaml"
    root = tmp_path_factory.mktemp("archives-" + codec)
    hand = root / "handover"
    hand.mkdir()
    (hand / "record.yaml").write_bytes(RECORD)

    def m(wallet, *args, stdin="", cwd=hand):
        return run_mofn(
            "--wallet", root / wallet, "--codec", codec, *args, stdin=stdin, cwd=cwd
        )

    # Issuers: a person who read the record against its source, and the
    # ingestion agent that wrote it. Each signs `reviewed`.
    for wallet, label, kind in (("reviewer", "reviewer", "person"), ("agent", "agent", "service")):
        ok(m(wallet, "init"))
        ok(
            m(
                wallet, "key", "gen", label, "--controller", kind,
                "--passphrase-stdin", "-o", hand / f"{label}.pub{suffix}",
                stdin=PASS + "\n",
            )
        )
        ok(
            m(
                wallet, "make", "--as", label, "--subject", "record.yaml",
                "--def", DEF, "--type", "record-review", "--value", "reviewed",
                "-o", hand / f"{label}{suffix}", "--passphrase-stdin",
                stdin=PASS + "\n",
            )
        )

    # The relying party: a researcher citing the record.
    ok(m("rp", "init"))
    ok(m("rp", "key", "gen", "researcher", "--passphrase-stdin", "-o", root / "rp.pub", stdin=PASS + "\n"))
    ok(m("rp", "key", "import", DOMAIN / f"archivist.pub{suffix}", "--label", "Archivist (definer)"))
    ok(m("rp", "key", "import", hand / f"reviewer.pub{suffix}", "--label", "Reviewer"))
    ok(m("rp", "key", "import", hand / f"agent.pub{suffix}", "--label", "ingest agent"))
    anchor = ("--as", "researcher", "--def", DEF, "--type", "record-review", "--context", "library")
    ok(m("rp", "root", "add", "Reviewer", *anchor, "--values", "reviewed,summarized,unverified"))
    ok(m("rp", "root", "add", "ingest agent", *anchor, "--values", "summarized,unverified"))

    def chk(who, *extra):
        return m(
            "rp", *extra, "check", f"{who}{suffix}", DOMAIN / f"archivist-define{suffix}",
            "--artifact", "record.yaml", "--def", DEF, "--context", "library",
        )

    return {
        "reviewed": chk("reviewer"),
        "agent-not-entitled": chk("agent"),
        "agent-not-entitled-es": chk("agent", "--lang", "es"),
    }


@pytest.mark.parametrize(
    "case,code",
    [("reviewed", 0), ("agent-not-entitled", 1), ("agent-not-entitled-es", 1)],
)
def test_archives_golden_verdicts(library, case, code):
    p = library[case]
    assert p.stdout == (GOLDEN / f"{case}.txt").read_text(encoding="utf-8")
    assert p.returncode == code, p.stderr


def test_domain_files_are_reproducible():
    p = subprocess.run(
        [sys.executable, str(DOMAIN / "generate.py"), "--check"],
        capture_output=True, text=True,
    )
    assert p.returncode == 0, p.stdout + p.stderr
