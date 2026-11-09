"""Delegation evaluations E-1..E-4 (SPEC-0004 §6.3, Appendix A; mofn#136) and the
DV-2/TV-13 rendered sentence (ADR-0007; T-049).

The engine v0 has no delegation (engine/reduce.py), so E-1..E-4 are checked by
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


def stmt(name):
    return verify(bytes.fromhex(POS[name]["envelope"]), keystore()).statement


def ranges(body_part):
    return set(body_part[0][3])


def walk(anchor, names, value):
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
        for s in attests.values():
            if s[3] == key and s[4] == [2, 1, ARTIFACT] and s[6][1][0][2] == value and value in scope:
                return ("yes", None, None)
        for n, s in trusts.items():
            if s[3] != key or s[4][1] in seen:
                continue
            depth = (deleg or {}).get(1, 0)
            if deleg is None or depth < 1:  # item 3
                failure = ("no", "depth", n)
                continue
            about = ranges(s[6][1])
            allowed = set(deleg[2][0][3]) if 2 in deleg else scope
            if not (about <= scope and about <= allowed):  # item 4
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
    got = walk(e["anchor"], e["statements"], e["ask"]["build-provenance"])
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
