"""SDSI name resolution through the engine (SPEC-0004 §5.3; T-040; DL-0040):
R-1…R-10 (`resolutions`) and E-8…E-10 (`name_evaluations`)."""

import pytest

from conftest import VECTORS, keystore
from engine import definition, ksatime
from engine.names import T_NAME, resolve
from engine.reduce import Anchor, Ask, evaluate
from engine.verifier import verify

POS = VECTORS["positive"]
KID = {n: bytes.fromhex(k["kid"]) for n, k in VECTORS["keys"].items()}
NAME_OF = {v: n for n, v in KID.items()}
DEFS = {
    d.id: d
    for d in (
        definition.load(bytes.fromhex(v["body"]), bytes.fromhex(v["id"]))
        for v in VECTORS["definitions"].values()
    )
}
DV1 = bytes.fromhex(VECTORS["definitions"]["DV-1"]["id"])
ARTIFACT = [2, 1, bytes.fromhex(VECTORS["artifact_sha256"])]


def verified(name):
    return verify(bytes.fromhex(POS[name]["envelope"]), keystore())


def by_digest(v):
    return next(n for n, p in POS.items() if bytes.fromhex(p["digest"]) == v.digest)


@pytest.mark.parametrize("rid", sorted(VECTORS["resolutions"], key=lambda r: int(r[2:])))
def test_resolution(rid):
    r = VECTORS["resolutions"][rid]
    name = [T_NAME, KID[r["name"]["issuer"]], r["name"]["labels"]]
    got = resolve(name, [verified(n) for n in r["statements"]], DEFS, ksatime.from_text(r["at"]))
    assert sorted(NAME_OF[k] for k in got.keys) == sorted(r["keys"])
    assert got.reason == r["reason"]
    if r["keys"]:  # §10.3: the bindings used are named, and each is a listed statement
        assert {by_digest(b) for b in got.bindings} <= set(r["statements"])


@pytest.mark.parametrize("eid", sorted(VECTORS["name_evaluations"]))
def test_name_evaluation(eid):
    e = VECTORS["name_evaluations"][eid]
    tv = verified(e["anchor"])
    anchor = Anchor(e["context"], tv.this, tv.body[1], tv.says, 0, source="statement")
    label = next(k for k in e["ask"] if k != "this")
    ask = Ask(
        e["context"],
        ARTIFACT,
        [{1: {1: DV1, 2: label}, 2: e["ask"][label]}],
        ksatime.from_text(e["at"]),
    )
    got = evaluate(ask, [verified(n) for n in e["statements"]], [anchor], DEFS, {DV1})
    assert ("yes" if got.yes else "no") == e["answer"]
    if got.yes:
        return
    first = got.stopped[0]
    at = by_digest(first.statement) if first.statement else e["anchor"]
    assert (first.code, at) == (e["reason"], e["at_statement"])


def test_tv13_is_not_a_binding():
    """DV-2's `name` has base kind text (SPEC-0004 §5.3.6)."""
    got = resolve([T_NAME, KID["alice"], ["fred"]], [verified("TV-13")], DEFS, ksatime.from_text("2026-10-10T12:00:00Z"))
    assert not got.keys and got.reason == "name-unresolved"


def test_a_binding_outside_its_window_is_not_used():
    got = resolve([T_NAME, KID["alice"], ["fred"]], [verified("TV-28")], DEFS, ksatime.from_text("2026-12-02T00:00:00Z"))
    assert got.reason == "name-unresolved"


def test_a_binding_needs_its_naming_definition():
    dv4 = bytes.fromhex(VECTORS["definitions"]["DV-4"]["id"])
    held = {k: v for k, v in DEFS.items() if k != dv4}
    got = resolve([T_NAME, KID["alice"], ["fred"]], [verified("TV-28")], held, ksatime.from_text("2026-10-10T12:00:00Z"))
    assert not got.keys


def test_the_result_does_not_depend_on_order():
    names = ["TV-34", "TV-29", "TV-28"]
    at = ksatime.from_text("2026-10-10T12:00:00Z")
    one = resolve([T_NAME, KID["alice"], ["fred"]], [verified(n) for n in names], DEFS, at)
    two = resolve([T_NAME, KID["alice"], ["fred"]], [verified(n) for n in reversed(names)], DEFS, at)
    assert one.keys == two.keys == {KID["bob"], KID["dave"]}
