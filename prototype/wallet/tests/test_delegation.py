"""Delegation evaluations E-1..E-7 and E-20..E-22 (SPEC-0004 §6.3, Appendix A; mofn#136;
ARCH-0001 §2.3) and the DV-2/TV-13 rendered sentence (ADR-0007; T-049).

E-1..E-7 run through the engine (`engine/reduce.py`, T-065). Until wallet
0.7.0 they were checked by a test-only walker here; the expectations moved to
the engine unchanged. The failing statement of a **no** is the broken link
when the chain broke, and otherwise the attestation.
"""

import pytest

from conftest import VECTORS, keystore
from engine import definition, ksatime, render
from engine.reduce import Ask, anchor_from, evaluate
from engine.verifier import verify

POS = VECTORS["positive"]
EVALS = VECTORS["evaluations"]
ARTIFACT = bytes.fromhex(VECTORS["artifact_sha256"])
RECORD = bytes.fromhex(VECTORS["record_sha256"])
DEFS = {
    d.id: d
    for d in (
        definition.load(bytes.fromhex(v["body"]), bytes.fromhex(v["id"]))
        for v in VECTORS["definitions"].values()
    )
}


def verified(name):
    return verify(bytes.fromhex(POS[name]["envelope"]), keystore())


def stmt(name):
    return verified(name).statement


def by_digest(v):
    return next(n for n, p in POS.items() if bytes.fromhex(p["digest"]) == v.digest)


def subject(name):
    fixed = {"artifact": [2, 1, ARTIFACT], "record": [2, 1, RECORD]}
    return fixed.get(name) or stmt({"work": "TV-26", "work-v2": "TV-44"}[name])[4]


def engine_eval(e):
    tv = verified(e["anchor"])
    anchor = anchor_from(tv, e["context"], tv.says, 0)
    label = next(k for k in e["ask"] if k != "this")
    tref = next(r[1] for r in tv.body[1] if r[1][2] == label)
    ask = Ask(e["context"], subject(e["ask"]["this"]), [{1: tref, 2: e["ask"][label]}],
              ksatime.from_text(e["at"]))
    return evaluate(ask, [verified(n) for n in e["statements"]], [anchor], DEFS, set(DEFS))


@pytest.mark.parametrize("name", sorted(EVALS))
def test_delegation_evaluation(name):
    e = EVALS[name]
    got = engine_eval(e)
    if got.yes:
        assert (e["answer"], e["reason"], e["at_statement"]) == ("yes", None, None)
        return
    first = got.stopped[0]
    at = by_digest(first.link or first.statement)
    assert ("no", first.code, at) == (e["answer"], e["reason"], e["at_statement"])


def test_e2_path_names_each_hop():
    """§10.3: the path is the anchor and each trust statement, with the scope after it."""
    got = engine_eval(EVALS["E-2"])
    (c,) = got.covered
    assert [by_digest(h.statement) for h in c.path] == ["TV-16"]
    assert c.path[0].scope[0][3] == ["reproducible"]


def test_evaluations_cover_depth_and_widening():
    reasons = {e["reason"] for e in EVALS.values()}
    assert {"depth", "widening"} <= reasons


def test_tv13_renders_under_dv2():
    d = definition.load(
        bytes.fromhex(VECTORS["definitions"]["DV-2"]["body"]),
        bytes.fromhex(VECTORS["definitions"]["DV-2"]["id"]),
    )
    labels = {
        bytes.fromhex(VECTORS["keys"]["alice"]["kid"]): "Alice",
        bytes.fromhex(VECTORS["keys"]["bob"]["kid"]): "Bob",
    }
    assert render.sentence(d, stmt("TV-13"), labels) == "Alice says that for Bob, name is fred."


def test_tv13_without_dv2_is_unresolved():
    s = render.sentence(None, stmt("TV-13"), {})
    assert s.startswith("key:") and "unresolved vocabulary definition:" in s


# ---------------------------------------------------------------- archives (ARCH-0001 §2.3.2)
DV3 = definition.load(
    bytes.fromhex(VECTORS["definitions"]["DV-3"]["body"]),
    bytes.fromhex(VECTORS["definitions"]["DV-3"]["id"]),
)
LABELS = {bytes.fromhex(VECTORS["keys"][n]["kid"]): n.capitalize() for n in ("bob", "dave")}


@pytest.mark.parametrize("name", ["TV-24", "TV-25", "TV-26"])
def test_archive_statements_conform_to_record_reviewed(name):
    s = stmt(name)
    assert definition.conforms_to_template(DV3, DV3.templates["record-reviewed"], s) is None


def test_archive_renders_through_the_same_renderer():
    assert render.sentence(DV3, stmt("TV-25"), LABELS) == (
        "Bob says sha-256:60cec9d66dd8f1f2 is reviewed: checked in part against its source."
    )
    assert render.sentence(DV3, stmt("TV-26"), LABELS) == (
        "Dave says a described object is reviewed: checked in full against its source."
    )


def test_description_target_through_the_engine():
    """E-7 is one hop, which engine v0 does: Carol's anchor trusts Dave."""
    from engine import ksatime
    from engine.reduce import Anchor, Ask, evaluate

    v = verify(bytes.fromhex(POS["TV-26"]["envelope"]), keystore())
    reviewed = {1: {1: DV3.id, 2: "reviewed"}, 2: "yes"}
    got = evaluate(
        Ask("library", stmt("TV-26")[4], [reviewed], ksatime.from_text(EVALS["E-7"]["at"])),
        [v],
        [Anchor("library", v.says, [{1: reviewed[1]}], b"carol", 0)],
        {DV3.id: DV3},
        {DV3.id},
    )
    assert got.yes, got.stopped
