"""k-of-n threshold anchors through the engine (SPEC-0004 §6.4; T-043; DL-0042):
E-11…E-19 (`threshold_evaluations`), and what the answer says about each member."""

from dataclasses import replace

import pytest

from conftest import VECTORS, keystore
from engine import definition, ksatime
from engine.check import Answer, _authorization
from engine.reduce import Anchor, Ask, Threshold, ThresholdCovered, evaluate
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
EVALS = VECTORS["threshold_evaluations"]


def verified(name):
    return verify(bytes.fromhex(POS[name]["envelope"]), keystore())


def anchor_from(tv_name, context="releases-panel"):
    tv = verified(tv_name)
    assert tv.this is None  # the threshold form (SPEC-0002 §8.6)
    return Anchor(context, Threshold(tuple(tv.body[3]), tv.body[4]), tv.body[1], tv.says, 0, source="statement")


def ask(value, at, context="releases-panel"):
    return Ask(context, ARTIFACT, [{1: {1: DV1, 2: "build-provenance"}, 2: value}], ksatime.from_text(at))


def run(e):
    return evaluate(
        ask(e["ask"]["build-provenance"], e["at"]),
        [verified(n) for n in e["statements"]],
        [anchor_from(e["anchor"])],
        DEFS,
        {DV1},
    )


@pytest.mark.parametrize("eid", sorted(EVALS, key=lambda e: int(e[2:])))
def test_threshold_evaluation(eid):
    e = EVALS[eid]
    got = run(e)
    assert ("yes" if got.yes else "no") == e["answer"]
    if got.yes:
        c = got.covered[0]
        assert isinstance(c, ThresholdCovered)
        members = c.members
    else:
        first = got.stopped[0]
        assert first.code == e["reason"]
        assert first.anchor.source == "statement" and isinstance(first.anchor.trusts, Threshold)
        members = first.members
    # §10.3: every member is named, and exactly the declared ones counted.
    assert [NAME_OF[m.key] for m in members if m.counted] == e["counted"]
    assert {m.key for m in members} == set(verified(e["anchor"]).body[3])
    for m in members:
        assert m.detail
        if m.counted:
            assert m.statement.says == m.key


def test_a_member_that_did_not_count_says_why():
    """E-13: Bob attested a different value; Dave said nothing."""
    got = run(EVALS["E-13"])
    why = {NAME_OF[m.key]: m for m in got.stopped[0].members}
    assert why["alice"].counted
    assert not why["bob"].counted and why["bob"].code == "not-verified"
    assert not why["dave"].counted and why["dave"].statement is None


def test_an_expired_member_statement_is_not_counted():
    """A member's attestation goes through the same checks a one-key anchor applies."""
    e = dict(EVALS["E-11"], at="2026-11-02T00:00:00Z")  # TV-4 and TV-17 end 2026-11-01
    got = run(e)
    assert not got.yes
    assert {m.code for m in got.stopped[0].members if m.statement} == {"not-valid-at-time"}


def test_rotation_linked_members_count_once():
    """E-18: bob2 is reported as the same member as Bob, not as a second one."""
    got = run(EVALS["E-18"])
    bob2 = next(m for m in got.stopped[0].members if m.key == KID["bob2"])
    assert not bob2.counted and bob2.same_as == KID["bob"]


def test_without_the_rotation_bob_and_bob2_are_two():
    """The same statements as E-18 less TV-8: nothing links them, so 2 of 3 is met."""
    e = dict(EVALS["E-18"], statements=["TV-35", "TV-17", "TV-37"])
    assert run(e).yes


def test_a_listed_key_counts_once():
    """`trusts: [A, A]` passes V8 (SPEC-0002 has no distinctness rule; ARCH-0001
    §7 condition 5), but §6.4 counts distinct kids, so 2 of it is never met."""
    a = replace(anchor_from("TV-9"), trusts=Threshold((KID["alice"], KID["alice"]), 2))
    got = evaluate(ask("reproducible", "2026-10-10T12:00:00Z"), [verified("TV-4")], [a], DEFS, {DV1})
    assert not got.yes
    assert len(got.stopped[0].members) == 1


def test_scope_is_the_thresholds_about():
    """A threshold about {attested} does not cover reproducible, however many agree."""
    a = anchor_from("TV-9")
    a = replace(a, about=[{1: a.about[0][1], 3: ["attested"]}])
    got = evaluate(
        ask("reproducible", "2026-10-10T12:00:00Z"),
        [verified(n) for n in ["TV-4", "TV-17", "TV-19"]],
        [a],
        DEFS,
        {DV1},
    )
    assert not got.yes and got.stopped[0].code == "threshold-not-met"
    assert {m.code for m in got.stopped[0].members} == {"no-path"}


def test_other_contexts_threshold_anchors_are_not_used():
    e = EVALS["E-11"]
    got = evaluate(
        ask("reproducible", e["at"]),
        [verified(n) for n in e["statements"]],
        [anchor_from(e["anchor"], context="elsewhere")],
        DEFS,
        {DV1},
    )
    assert not got.yes


def test_a_one_key_anchor_still_wins_first():
    """A context with both kinds: the one-key path is tried first, as before."""
    tv5 = verified("TV-5")
    one = Anchor("releases-panel", tv5.this[1], tv5.body[1], tv5.says, 0, source="statement")
    got = evaluate(ask("reproducible", "2026-10-10T12:00:00Z"), [verified("TV-4")], [one, anchor_from("TV-9")], DEFS, {DV1})
    assert got.yes and not isinstance(got.covered[0], ThresholdCovered)


def test_the_verdict_line_names_who_counted():
    labels = {KID[n]: n.capitalize() for n in ("alice", "bob", "dave")}
    d = DEFS[DV1]
    about = [verified("TV-4")]
    yes = _authorization(about, run(EVALS["E-11"]), d, "releases-panel", labels)
    assert yes.result == "pass" and "2 of 3" in yes.sentence and "Alice, Bob" in yes.sentence
    no = _authorization(about, run(EVALS["E-12"]), d, "releases-panel", labels)
    assert no.result == "fail" and "1 did (Alice)" in no.sentence
    assert "Bob" in no.sentence and "Dave" in no.sentence and "threshold-not-met" in no.sentence


def test_the_json_answer_lists_every_member():
    cov = run(EVALS["E-11"])
    ans = Answer("releases-panel", ksatime.from_text(EVALS["E-11"]["at"]), ARTIFACT, [], [], [], cov)
    entry = ans.to_json()["because"][0]
    assert entry["path"][0]["threshold"] == {"k": 2, "n": 3}
    assert sorted(m["counted"] for m in entry["path"][0]["members"]) == [False, True, True]
    assert len(entry["used"]) == 2
