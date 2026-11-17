"""Attribute associations on every verdict (W-5, mofn#69; DL-0049).

`check --format json` gives, for each attestation and attribute the answer
describes: who signed, the topic, the subject's digest, and standing. These
tests pin the shape (README "The verdict as JSON") that `mofn run`'s Check tab
and W-7 (#179) render.

- The W-4 slice cases (green, authorization fail, integrity fail) end to end
  through the CLI, against goldens in fixtures/golden/associations-*.json.
  Only vector keys appear in them, so they are stable.
- Standing through a delegation chain, a broken link, and a threshold,
  through the engine with the published vectors (E-2, E-4, E-11).
"""

import json

import pytest

from conftest import FIXTURES, VECTORS, keystore, run_mofn
from engine import definition, ksatime
from engine.check import Answer, Handed, associations
from engine.reduce import Anchor, Ask, Threshold, anchor_from, evaluate
from engine.verifier import verify

PASS = "associations test passphrase, not a secret"
GOLDEN = FIXTURES / "golden"
AT = "2026-10-15T00:00:00Z"
KEYS = {"signed-by", "topic", "subject", "standing", "statement", "file"}


def ok(p):
    assert p.returncode == 0, p.stderr + p.stdout
    return p


@pytest.fixture(scope="module", params=["ksa-cbor", "review-yaml"])
def rp(request, tmp_path_factory):
    """A relying party that knows Alice, checking TV-4 about the fixture file."""
    codec = request.param
    suffix = ".stmt" if codec == "ksa-cbor" else ".stmt.yaml"
    root = tmp_path_factory.mktemp("assoc-" + codec)
    (root / "app.bin").write_bytes((FIXTURES / "artifact.bin").read_bytes())
    (root / "bad.bin").write_bytes(b"X" + (FIXTURES / "artifact.bin").read_bytes()[1:])

    def m(*args):
        return run_mofn("--wallet", root / "w", "--codec", codec, *args, stdin=PASS + "\n", cwd=root)

    ok(m("init"))
    ok(m("key", "gen", "me", "--passphrase-stdin", "-o", root / "me.pub"))
    ok(m("key", "import", FIXTURES / f"tv-1-alice.pub{suffix}", "--label", "Alice"))

    def check(artifact="app.bin"):
        p = m(
            "check", FIXTURES / f"tv-4-attestation{suffix}", FIXTURES / f"tv-3-define{suffix}",
            "--artifact", artifact, "--def", FIXTURES / "dv-1.def", "--at", AT, "--format", "json",
        )
        return p.returncode, json.loads(p.stdout)

    out = {"unauthorized": check(), "tampered": check("bad.bin")}
    ok(m("root", "add", "Alice", "--as", "me", "--def", FIXTURES / "dv-1.def",
         "--type", "build-provenance", "--values", "reproducible"))
    out["green"] = check()
    return out


def comparable(j):
    """The goldens hold no file paths: those differ per codec and per run."""
    return [{k: v for k, v in a.items() if k != "file"} for a in j["associations"]]


@pytest.mark.parametrize(
    "case,code,answer,standing",
    [
        ("green", 0, "yes", "standing"),
        ("unauthorized", 1, "no", "no-standing"),
        ("tampered", 1, "no", "not-evaluated"),
    ],
)
def test_slice_cases_match_their_golden(rp, case, code, answer, standing):
    got, j = rp[case]
    assert (got, j["answer"]) == (code, answer)
    assert all(set(a) == KEYS for a in j["associations"])
    assert j["associations"][0]["standing"]["result"] == standing
    want = json.loads((GOLDEN / f"associations-{case}.json").read_text(encoding="utf-8"))
    assert comparable(j) == want


def test_every_association_names_the_four(rp):
    _, j = rp["green"]
    a = j["associations"][0]
    assert a["signed-by"]["key"] == "Alice" and a["signed-by"]["kid"] == VECTORS["keys"]["alice"]["kid"]
    assert a["topic"]["domain"] == "supply-chain 1" and a["topic"]["type"] == "build-provenance"
    assert a["subject"]["digest"] == "sha-256:" + VECTORS["artifact_sha256"]
    assert a["standing"]["chain"][0]["role"] == "root"


def test_integrity_fail_shows_both_digests(rp):
    _, j = rp["tampered"]
    s = j["associations"][0]["subject"]
    assert s["matches"] is False and s["digest"] != s["yours"]


# ------------------------------------------------- through the engine, vectors

POS = VECTORS["positive"]
KID = {n: bytes.fromhex(k["kid"]) for n, k in VECTORS["keys"].items()}
LABELS = {v: n.capitalize() for n, v in KID.items()}
DEFS = {
    d.id: d
    for d in (
        definition.load(bytes.fromhex(v["body"]), bytes.fromhex(v["id"]))
        for v in VECTORS["definitions"].values()
    )
}
ARTIFACT = [2, 1, bytes.fromhex(VECTORS["artifact_sha256"])]


def verified(name):
    return verify(bytes.fromhex(POS[name]["envelope"]), keystore())


def answer(anchors, names, value, at, context):
    vs = [verified(n) for n in names]
    about = [v for v in vs if v.kind == 4 and v.this == ARTIFACT]
    tref = next(a[1] for a in about[0].body[1])
    ask = Ask(context, ARTIFACT, [{1: tref, 2: value}], ksatime.from_text(at))
    cov = evaluate(ask, vs, anchors, DEFS, set(DEFS))
    handed = [Handed(n, "verified", verified=v) for n, v in zip(names, vs)]
    return Answer(context, ask.at, ARTIFACT, handed, [], [], cov, LABELS,
                  described=about, definition=DEFS[tref[1]])


def delegation(e):
    e = VECTORS["evaluations"][e]
    tv = verified(e["anchor"])
    a = anchor_from(tv, e["context"], tv.says, 0)
    return answer([a], e["statements"], e["ask"]["build-provenance"], e["at"], e["context"])


def test_standing_through_a_delegation_chain():
    st = associations(delegation("E-2"))[0]["standing"]
    assert st["result"] == "standing"
    assert [h["role"] for h in st["chain"]] == ["root", "delegation"]
    assert st["chain"][-1]["key"] == "Bob"
    assert st["text"].endswith("→ Bob")


def test_a_broken_link_is_named():
    st = associations(delegation("E-4"))[0]["standing"]
    assert st["result"] == "no-standing" and st["reason"] == "widening"
    assert st["broken"]["trust"] == POS["TV-20"]["digest"]
    assert "✗" in st["text"]


def test_threshold_standing_names_the_set():
    e = VECTORS["threshold_evaluations"]["E-11"]
    tv = verified(e["anchor"])
    a = Anchor(e["context"], Threshold(tuple(tv.body[3]), tv.body[4]), tv.body[1], tv.says, 0,
               source="statement")
    ans = answer([a], e["statements"], e["ask"]["build-provenance"], e["at"], e["context"])
    got = associations(ans)
    standing = [x["standing"] for x in got if x["standing"]["result"] == "standing"]
    assert len(standing) >= 2
    assert all(s["chain"][0]["threshold"] == {"k": 2, "n": 3} for s in standing)
