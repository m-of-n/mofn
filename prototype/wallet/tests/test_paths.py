"""Delegation paths in the engine (SPEC-0004 §6; T-065, T-041, W-3 / mofn#67).

Each case builds a chain from Carol's local anchor, signs the hops with the
vector keys, and asks about the example artifact. What is tested is the §6.3
intersection: topic *and* range, validity, depth, key lists, and that a hop
that fails is named. The `delegation: 1` cases are the evidence for T-042
(R-0006 §4.7): the same range is the same bytes, and nothing else is.
"""

import pytest

from conftest import VECTORS, keystore, seed
from engine import definition, ksatime, signer, statement
from engine.encoding.ksa_cbor import encode
from engine.reduce import Anchor, Ask, evaluate
from engine.verifier import verify

KID = {n: bytes.fromhex(k["kid"]) for n, k in VECTORS["keys"].items()}
DV1 = definition.load(bytes.fromhex(VECTORS["definitions"]["DV-1"]["body"]))
BP = {1: DV1.id, 2: "build-provenance"}
OUTCOME = {1: DV1.id, 2: "outcome"}
ARTIFACT = [2, 1, bytes.fromhex(VECTORS["artifact_sha256"])]
T = ksatime.from_text
AT = "2026-10-10T12:00:00Z"
WINDOW = ("2026-10-01T00:00:00Z", "2026-11-01T00:00:00Z")

# A one-type definition whose type is `delegation: 1` (same), for T-042.
SAME_BODY = {
    1: KID["alice"],
    2: "same-only",
    3: "1",
    5: [[1, {
        1: "grade",
        2: 1,
        3: {"en": "Grade"},
        4: {"en": "A grade"},
        6: [{1: v, 2: {"en": v}, 3: {"en": v}} for v in ("gold", "silver", "bronze")],
        8: 1,
    }]],
}
SAME = definition.load(encode(SAME_BODY))
GRADE = {1: SAME.id, 2: "grade"}
DEFS = {DV1.id: DV1, SAME.id: SAME}


def rng(tref, *values):
    return {1: tref, 3: list(values)} if values else {1: tref}


def signed(who, s):
    return verify(signer.sign(seed(who), s), keystore())


def trust(who, to, about, may=None, window=WINDOW):
    s = statement.trust(KID[who], [1, KID[to]], about, T(window[0]), T(window[1]), T(window[0]), may)
    return signed(who, s)


def attest(who, value="reproducible", tref=BP):
    s = statement.attestation(KID[who], ARTIFACT, [{1: tref, 2: value}], T(WINDOW[0]), T(WINDOW[1]), T(WINDOW[0]))
    return signed(who, s)


def anchor(about, may=None, trusts="alice", cap=None):
    return Anchor("releases", KID[trusts], about, KID["carol"], 0, may_delegate=may, not_on_or_after=cap)


def ask(statements, anchors, value="reproducible", tref=BP, at=AT):
    a = Ask("releases", ARTIFACT, [{1: tref, 2: value}], T(at))
    return evaluate(a, statements, anchors, DEFS, set(DEFS))


def reason(got):
    s = got.stopped[0]
    return s.code, s.link


# ---------------------------------------------------------------- chains


def test_two_hops_reduce():
    """Carol → Alice (depth 2) → Bob (depth 1) → Dave; Dave attests."""
    ab = trust("alice", "bob", [rng(BP, "reproducible")], {1: 1})
    bd = trust("bob", "dave", [rng(BP, "reproducible")])
    got = ask([ab, bd, attest("dave")], [anchor([rng(BP, "reproducible", "attested")], {1: 2})])
    assert got.yes, got.stopped
    assert [h.key for h in got.covered[0].path] == [KID["bob"], KID["dave"]]
    assert got.covered[0].scope == rng(BP, "reproducible")


def test_the_scope_narrows_along_the_chain():
    """Bob holds only {reproducible}; his delegate's `attested` is not covered."""
    ab = trust("alice", "bob", [rng(BP, "reproducible")], {1: 1})
    bd = trust("bob", "dave", [rng(BP, "attested")])
    got = ask([ab, bd, attest("dave", "attested")], [anchor([rng(BP)], {1: 2})], "attested")
    assert reason(got) == ("widening", bd)


def test_out_of_topic_link_is_named():
    """A hop about a type the delegator is not trusted about: topic intersection."""
    other = definition.load(encode({**SAME_BODY, 2: "other"}))
    defs = {**DEFS, other.id: other}
    g = {1: other.id, 2: "grade"}
    ab = trust("alice", "bob", [rng(g, "gold", "silver", "bronze")])
    a = Ask("releases", ARTIFACT, [{1: g, 2: "gold"}], T(AT))
    got = evaluate(a, [ab, attest("bob", "gold", g)], [anchor([rng(GRADE)], {1: 1})], defs, set(defs))
    assert reason(got) == ("widening", ab)
    assert "not a topic" in got.stopped[0].detail


def test_a_type_with_delegation_none_cannot_be_delegated():
    ab = trust("alice", "bob", [rng(OUTCOME)])
    got = ask([ab, attest("bob", "approve", OUTCOME)], [anchor([rng(OUTCOME)], {1: 1})], "approve", OUTCOME)
    assert reason(got) == ("type-error", ab)


# ---------------------------------------------------------------- validity


def test_expired_link_is_named():
    """Short expiry is the revocation mechanism: the hop's window has ended."""
    ab = trust("alice", "bob", [rng(BP, "reproducible")], window=("2026-10-01T00:00:00Z", "2026-10-05T00:00:00Z"))
    got = ask([ab, attest("bob")], [anchor([rng(BP)], {1: 1})])
    assert reason(got) == ("not-valid-at-time", ab)
    assert got.stopped[0].detail == "the delegation has expired"
    assert got.stopped[0].statement.says == KID["bob"]


def test_link_not_yet_valid_is_named():
    ab = trust("alice", "bob", [rng(BP, "reproducible")], window=("2026-10-20T00:00:00Z", "2026-11-01T00:00:00Z"))
    got = ask([ab, attest("bob")], [anchor([rng(BP)], {1: 1})])
    assert reason(got) == ("not-valid-at-time", ab)
    assert got.stopped[0].detail == "the delegation is not yet valid"


def test_the_right_to_delegate_expires_on_its_own():
    """`may-delegate.not-on-or-after` caps the hop even inside its window."""
    ab = trust("alice", "bob", [rng(BP, "reproducible")])
    got = ask([ab, attest("bob")], [anchor([rng(BP)], {1: 1, 5: T("2026-10-05T00:00:00Z")})])
    assert reason(got) == ("not-valid-at-time", ab)


def test_an_expired_anchor_statement_starts_no_path():
    got = ask([attest("alice")], [anchor([rng(BP)], cap=T("2026-10-05T00:00:00Z"))])
    s = got.stopped[0]
    assert (s.code, s.link) == ("not-valid-at-time", None)


def test_the_same_chain_inside_its_window_is_yes():
    ab = trust("alice", "bob", [rng(BP, "reproducible")], window=("2026-10-01T00:00:00Z", "2026-10-05T00:00:00Z"))
    assert ask([ab, attest("bob")], [anchor([rng(BP)], {1: 1})], at="2026-10-03T00:00:00Z").yes


# ---------------------------------------------------------------- depth, keys, cycles


def test_one_hop_trust_is_not_followed():
    ab = trust("alice", "bob", [rng(BP, "reproducible")])
    assert reason(ask([ab, attest("bob")], [anchor([rng(BP)])])) == ("depth", ab)


def test_exclude_keys():
    ab = trust("alice", "bob", [rng(BP, "reproducible")])
    got = ask([ab, attest("bob")], [anchor([rng(BP)], {1: 1, 4: [KID["bob"]]})])
    assert reason(got) == ("key-excluded", ab)


def test_allow_keys():
    ab = trust("alice", "bob", [rng(BP, "reproducible")])
    got = ask([ab, attest("bob")], [anchor([rng(BP)], {1: 1, 3: [KID["dave"]]})])
    assert reason(got) == ("key-not-allowed", ab)
    assert ask([ab, attest("bob")], [anchor([rng(BP)], {1: 1, 3: [KID["bob"]]})]).yes


def test_allow_keys_accumulate_down_the_chain():
    """Alice's anchor allows only Bob; Bob cannot pass trust on to Dave."""
    ab = trust("alice", "bob", [rng(BP, "reproducible")], {1: 1})
    bd = trust("bob", "dave", [rng(BP, "reproducible")])
    got = ask([ab, bd, attest("dave")], [anchor([rng(BP)], {1: 2, 3: [KID["bob"]]})])
    assert reason(got) == ("key-not-allowed", bd)


def test_a_cycle_terminates():
    ab = trust("alice", "bob", [rng(BP)], {1: 3})
    ba = trust("bob", "alice", [rng(BP)], {1: 2})
    got = ask([ab, ba, attest("dave")], [anchor([rng(BP)], {1: 4})])
    assert not got.yes and got.stopped[0].code == "no-path"


def test_the_answer_does_not_depend_on_statement_order():
    ab = trust("alice", "bob", [rng(BP, "reproducible")], {1: 1})
    bd = trust("bob", "dave", [rng(BP, "reproducible")])
    a = [anchor([rng(BP)], {1: 2})]
    one = ask([ab, bd, attest("dave")], a)
    two = ask([attest("dave"), bd, ab], a)
    assert one.yes and two.yes
    assert [h.statement.digest for h in one.covered[0].path] == [h.statement.digest for h in two.covered[0].path]


# ---------------------------------------------------------------- delegation: 1 is bytes-equal (T-042)


@pytest.mark.parametrize(
    "delegated, ok",
    [
        (("gold", "silver"), True),    # the same range: the same bytes
        (("gold",), False),            # narrower: `delegation: 1` refuses it
        (("silver", "gold"), False),   # the same set, other order: other bytes, refused (fails closed)
        ((), False),                   # unbounded is wider
    ],
)
def test_delegation_same_is_bytes_equal(delegated, ok):
    held = rng(GRADE, "gold", "silver")
    hop = rng(GRADE, *delegated)
    assert (encode(hop) == encode(held)) is ok
    ab = trust("alice", "bob", [hop])
    got = ask([ab, attest("bob", "gold", GRADE)], [anchor([held], {1: 1})], "gold", GRADE)
    assert got.yes is ok
    if not ok:
        assert reason(got) == ("widening", ab)


def test_delegation_scoped_narrows_where_same_cannot():
    """`delegation: 2` (DV-1 build-provenance) accepts the narrower range."""
    ab = trust("alice", "bob", [rng(BP, "reproducible")])
    assert ask([ab, attest("bob")], [anchor([rng(BP, "reproducible", "attested")], {1: 1})]).yes
