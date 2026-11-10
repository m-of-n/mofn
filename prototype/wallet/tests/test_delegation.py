"""Delegation evaluations E-1..E-7 (SPEC-0004 §6.3, Appendix A; mofn#136;
ARCH-0001 §2.3) and the DV-2/TV-13 rendered sentence (ADR-0007; T-049).

The engine v0 has no delegation (engine/reduce.py), so E-1..E-7 are checked by
`walk` below: a test-only reading of §6.3 items 1, 3, 4 and 6 for one attribute
type, single-key anchors, no key lists and no revocation. It is not the engine.
When the engine gains delegation, these expectations move to it unchanged.
"""

import pytest

from conftest import VECTORS, keystore
from engine import definition, render
from engine.verifier import verify

POS = VECTORS["positive"]
EVALS = VECTORS["evaluations"]
ARTIFACT = bytes.fromhex(VECTORS["artifact_sha256"])
RECORD = bytes.fromhex(VECTORS["record_sha256"])
ALL = None  # the unbounded range: an attribute range with no `range`


def stmt(name):
    return verify(bytes.fromhex(POS[name]["envelope"]), keystore()).statement


def ranges(body_part):
    return set(body_part[0][3]) if 3 in body_part[0] else ALL


def within(a, b):
    return b is ALL or (a is not ALL and a <= b)


def subject(name):
    return {"artifact": [2, 1, ARTIFACT], "record": [2, 1, RECORD]}.get(name) or stmt("TV-26")[4]


def walk(anchor, names, label, value, this):
    """Return ("yes", None, None) or ("no", reason, statement-name)."""
    a = stmt(anchor)[6]
    # state at the anchor's key (§6.2)
    frontier = [(stmt(anchor)[4][1], ranges(a[1]), a.get(2))]
    trusts = {n: stmt(n) for n in names if stmt(n)[1] == 5}
    attests = {n: stmt(n) for n in names if stmt(n)[1] == 4}
    failure = ("no", "no-path", None)
    seen = set()
    while frontier:
        key, scope, deleg = frontier.pop()
        seen.add(key)
        for n, s in attests.items():
            said = {a[1][2]: a[2] for a in s[6][1]}
            if s[3] == key and s[4] == this and said.get(label) == value:
                if scope is ALL or value in scope:
                    return ("yes", None, None)
                failure = ("no", "no-path", n)  # trusted, but not about this value
        for n, s in trusts.items():
            if s[3] != key or s[4][1] in seen:
                continue
            depth = (deleg or {}).get(1, 0)
            if deleg is None or depth < 1:  # item 3
                failure = ("no", "depth", n)
                continue
            about = ranges(s[6][1])
            allowed = ranges(deleg[2]) if 2 in deleg else scope
            if not (within(about, scope) and within(about, allowed)):  # item 4
                failure = ("no", "widening", n)
                continue
            onward = s[6].get(2)
            if onward is not None and onward.get(1, 0) > depth - 1:  # item 6, depth
                failure = ("no", "widening", n)
                continue
            frontier.append((s[4][1], about, onward))
    return failure


@pytest.mark.parametrize("name", sorted(EVALS))
def test_delegation_evaluation(name):
    e = EVALS[name]
    label = next(k for k in e["ask"] if k != "this")
    got = walk(e["anchor"], e["statements"], label, e["ask"][label], subject(e["ask"]["this"]))
    assert got == (e["answer"], e["reason"], e["at_statement"])


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
