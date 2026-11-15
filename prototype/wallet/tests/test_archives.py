"""The second domain (mofn#66, W-2; W-2b): the archives scenario of APP-0003
through the same `mofn make`, `mofn delegate` and `mofn check` as supply
chain, under both codecs.

Since W-2b the vocabulary is the published DV-5 `library-review` v2, and the
relying party trusts the library lead, who delegates. Only the domain file
differs from supply chain. Nothing here may need code that knows what a
library record is; if a case below only passes with such code, that is a
finding against the vocabulary claim, not a fix (PLAN-0004 §3).
"""

import datetime
import subprocess
import sys

import pytest

from conftest import WALLET, run_mofn

PASS = "archives scenario passphrase"
DOMAIN = WALLET / "domains" / "archives"
DEF = DOMAIN / "library-review.def"
GOLDEN = DOMAIN / "golden"
RECORD = (DOMAIN / "record.yaml").read_bytes()
ALL = "reviewed,summarized,unverified"


def ok(p):
    assert p.returncode == 0, p.stderr + p.stdout
    return p


def in_days(n):
    t = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=n)
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


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

    def signing(wallet, *args):
        return ok(m(wallet, *args, "--passphrase-stdin", stdin=PASS + "\n"))

    def gen(wallet, label, kind="person"):
        ok(m(wallet, "init"))
        signing(wallet, "key", "gen", label, "--controller", kind, "-o", hand / f"{label}.pub{suffix}")

    # The library lead, who answers for the library's reviews, and two issuers:
    # a person who read the record against its source, and the ingestion agent
    # that wrote it.
    gen("lead", "lead")
    gen("reviewer", "reviewer")
    gen("agent", "agent", "service")

    def make(who, value, name):
        signing(
            who, "make", "--as", who, "--subject", "record.yaml", "--def", DEF,
            "--type", "record-review", "--value", value, "--valid-days", "90",
            "-o", hand / f"{name}{suffix}",
        )

    make("reviewer", "reviewed", "reviewer")
    make("agent", "reviewed", "agent")
    make("agent", "summarized", "agent-summarized")

    # The lead delegates for 30 days: the reviewer for every value, the agent
    # only for what an agent's run can establish. Short expiry is the
    # revocation mechanism (W-3).
    ok(m("lead", "key", "import", hand / f"reviewer.pub{suffix}", "--label", "Reviewer"))
    ok(m("lead", "key", "import", hand / f"agent.pub{suffix}", "--label", "ingest agent"))
    for who, values in (("Reviewer", ALL), ("ingest agent", "summarized,unverified")):
        signing(
            "lead", "delegate", who, "--as", "lead", "--def", DEF, "--type", "record-review",
            "--values", values, "--valid-days", "30",
            "-o", hand / f"lead-{who.split()[-1].lower()}{suffix}",
        )

    # The relying party, a researcher citing the record, knows four keys and
    # anchors one: the lead, who may delegate one hop.
    ok(m("rp", "init"))
    signing("rp", "key", "gen", "researcher", "-o", root / "rp.pub")
    for f, label in (
        (DOMAIN / f"dave.pub{suffix}", "Dave (definer)"),
        (hand / f"lead.pub{suffix}", "Library lead"),
        (hand / f"reviewer.pub{suffix}", "Reviewer"),
        (hand / f"agent.pub{suffix}", "ingest agent"),
    ):
        ok(m("rp", "key", "import", f, "--label", label))
    ok(
        m(
            "rp", "root", "add", "Library lead", "--as", "researcher", "--def", DEF,
            "--type", "record-review", "--values", ALL, "--depth", "1", "--context", "library",
        )
    )

    def chk(stmt, delegation, *extra, at=None):
        return m(
            "rp", *extra, "check", f"{stmt}{suffix}", f"lead-{delegation}{suffix}",
            DOMAIN / f"dave-define{suffix}", "--artifact", "record.yaml", "--def", DEF,
            "--context", "library", *(("--at", at) if at else ()),
        )

    return {
        "reviewed": chk("reviewer", "reviewer"),
        "agent-not-entitled": chk("agent", "agent"),
        "agent-not-entitled-es": chk("agent", "agent", "--lang", "es"),
        "agent-summarized": chk("agent-summarized", "agent"),
        "reviewer-expired": chk("reviewer", "reviewer", at=in_days(31)),
    }


@pytest.mark.parametrize(
    "case,code",
    [
        ("reviewed", 0),
        ("agent-not-entitled", 1),
        ("agent-not-entitled-es", 1),
        ("agent-summarized", 0),
        ("reviewer-expired", 1),
    ],
)
def test_archives_golden_verdicts(library, case, code):
    p = library[case]
    assert p.stdout == (GOLDEN / f"{case}.txt").read_text(encoding="utf-8")
    assert p.returncode == code, p.stderr


def test_domain_files_are_copies_of_the_vectors():
    p = subprocess.run(
        [sys.executable, str(DOMAIN / "generate.py"), "--check"],
        capture_output=True, text=True,
    )
    assert p.returncode == 0, p.stdout + p.stderr
