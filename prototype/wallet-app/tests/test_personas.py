"""Several personas in one wallet (W-8, mofn#180), through `core` — the app's
only door to the engine.

One group per acceptance box on the issue:

1. two personas in one wallet, with separate identity keys
2. switching persona changes the signing key and the trust context
3. each persona lists the tags it received, each with its verdict
4. each persona lists its communities and their members
5. nothing here decides DEC-004 / DEC-005
"""

import json

import pytest

from conftest import FIXTURES, PASS, VOCAB, mofn

from mofn_app import core


# --------------------------------------------- 1. two personas, two keys


def test_two_personas_have_separate_identity_keys(two):
    s = two.session
    owned = s.owned()
    assert [p.label for p in owned] == ["me", "work"]
    assert owned[0].kid != owned[1].kid
    for p in owned:
        d = s.root / "personas" / p.kid.hex()
        assert (d / "persona.yaml").is_file()
        assert list((d / "keys").glob("*.key")), "an owned persona holds a private key"
    # Unlinkable means no shared key and no statement linking them
    # (SPEC-0001 §3.1): neither record mentions the other's kid.
    for p, other in (owned, owned[::-1]):
        text = (s.root / "personas" / p.kid.hex() / "persona.yaml").read_text()
        assert other.kid.hex() not in text


def test_owned_is_ordered_by_label_not_by_kid(two):
    """The store sorts personas by kid, which is random. The app sorts by
    label, so "the first identity" is stable once there are two."""
    labels = [p.label for p in two.session.owned()]
    assert labels == sorted(labels)


def test_a_persona_states_its_controller_kind(two):
    s = two.session
    assert s.find("work").controller == "organisation"
    assert s.find("me").controller == "person"


# ------------------------------- 2. switching changes key and trust context


def test_check_as_scopes_the_verdict_to_one_personas_anchors(two):
    s = two.session
    two.trust_alice()  # accepted by "me"
    stmts = [str(FIXTURES / "tv-4-attestation.stmt"), str(FIXTURES / "tv-3-define.stmt")]

    def answer(as_):
        _, j = s.check(stmts, two.app, VOCAB, at="2026-10-15T00:00:00Z", as_=as_)
        return j["answer"]

    assert answer("me") == "yes"      # me accepted the anchor
    assert answer("work") == "no"     # work accepted nothing
    assert answer(None) == "yes"      # the union, as before


def test_the_check_command_names_the_persona(two):
    s = two.session
    r, _ = s.check([str(FIXTURES / "tv-4-attestation.stmt")], two.app, VOCAB, as_="work")
    assert " --as work " in r.shown + " "
    assert "--context" not in r.shown, "default context is left off, as before"


def test_contexts_are_per_persona(two):
    s = two.session
    two.trust_alice()
    assert s.root_add("Alice", "work", VOCAB, "build-provenance", [], context="studio").ok
    assert s.contexts("me") == ["default"]
    assert s.contexts("work") == ["default", "studio"]
    assert s.contexts() == ["default", "studio"]
    assert s.anchors("studio", persona="me") == []
    assert [a.key for a in s.anchors("studio", persona="work")] == ["Alice"]


def test_signing_names_the_persona_that_signs(two):
    s = two.session
    r = s.sign("work", two.app, VOCAB, "build-provenance", "reproducible", 30, PASS)
    assert r.ok and " make --as work " in r.shown
    assert s.inspect(r.out.splitlines()[0].removeprefix("wrote "))["says"] == "work"


# ----------------------------------------- 3. the tags a persona received


def test_received_lists_only_tags_about_this_persona(two):
    s = two.session
    two.tag("work", "me")
    got = s.received("me")
    assert len(got) == 1
    assert got[0].says == "work" and got[0].from_self is False
    assert "Reproducible" in got[0].claim or "reproducible" in got[0].claim
    assert s.received("work") == []


def test_received_ignores_key_publish_statements(two):
    """Every persona's own key-publish carries `this = [1, kid]` too
    (`statement.key_publish`). A key's publication is not a tag."""
    s = two.session
    held = [v for _, v in s.held()]
    assert any(v.kind == 1 and v.this[0] == 1 for v in held), "the wallet holds some"
    assert s.received("me") == [] and s.received("work") == []


def test_a_self_issued_tag_is_marked(two):
    two.tag("me", "me")
    assert two.session.received("me")[0].from_self is True


def test_a_received_tag_gets_the_cli_verdict(two):
    s = two.session
    two.trust_alice()
    assert s.root_add("me", "me", VOCAB, "build-provenance", ["reproducible"]).ok
    two.tag("me", "work")
    t = s.received("work")[0]
    handed = [t.path, str(FIXTURES / "tv-3-define.stmt")]
    # Pin the evaluation time: the verdict names it, so "now" twice is twice.
    at = t.not_before
    r, j = s.check(handed, definition=VOCAB, subject_key="work", as_="me", at=at)
    code, want = two.cli_key_json("work", *handed, as_="me", at=at)
    assert (r.code, j) == (code, want), "the app's verdict IS the CLI's"
    assert j["subject-target"] == "key"
    from mofn_app import verdict
    assert verdict.subject_form(j["associations"][0]["subject"]) == "key"


def test_a_tag_from_a_stranger_has_no_local_vocabulary(two):
    """Only `root add` puts a .def in the wallet, so a tag may arrive with
    no vocabulary to read it by. `received` says so rather than guessing."""
    two.tag("me", "work")
    assert two.session.received("work")[0].definition is None
    two.trust_alice()
    assert two.session.received("work")[0].definition is not None


# -------------------------------------- 4. communities and their members


def test_communities_are_the_personas_contexts(two):
    s = two.session
    two.trust_alice()
    found = [c for c in s.communities("me") if c.relies]
    assert [c.context for c in found] == ["default"]
    assert found[0].acts is None, "acting in a context is published, and nothing writes it"
    assert [c for c in s.communities("work") if c.relies] == []


def test_members_are_derived_from_anchors_not_declared(two):
    s = two.session  # `world` already knows Alice, and trusts her about nothing
    before = s.community("default", "me").members
    assert [m.name for m in before] == [], "no anchor, no member"
    two.trust_alice()
    after = s.community("default", "me").members
    by = {m.name: m for m in after}
    assert by["me"].role == "accepts anchors here" and by["me"].owned
    assert by["Alice"].role == "trusted" and not by["Alice"].owned
    assert "build-provenance" in by["Alice"].about


def test_a_known_key_with_no_anchor_is_not_a_member(two):
    s = two.session
    two.trust_alice()
    assert s.key_gen("other", "person", PASS).ok
    names = [m.name for m in s.community("default", "me").members]
    assert "other" not in names


def test_threshold_members_are_shown_as_k_of_n():
    """A threshold anchor cannot be written to a wallet yet (`add_anchor`
    stores `trusts` as one kid), so the derivation is exercised directly.
    W-9's groups are what will put one there."""
    from engine.reduce import Anchor, Threshold

    kids = [bytes([i]) * 32 for i in (1, 2, 3)]
    me = bytes([9]) * 32
    about = [{1: {1: b"d" * 32, 2: "build-provenance"}, 3: ["reproducible"]}]
    an = Anchor("default", Threshold(tuple(kids), 2), about, me, 0)
    got = core.members([an], {me: "me"}, {me}, {me})
    members = [m for m in got if m.name != "me"]
    assert len(members) == 3
    assert {m.threshold for m in members} == {"any 2 of 3"}
    assert {m.role for m in members} == {"one of a k-of-n set"}
    assert all(not m.known for m in members), "none of them is a key in this wallet"


# ------------------------------------------- 5. no DEC-004 / DEC-005 here


def test_the_new_reads_run_only_check_and_never_name_an_encoding(two, monkeypatch):
    """DEC-004 (tag language) and DEC-005 (export envelope) stay open: the
    app adds no encoding or envelope choice of its own."""
    from screens import runner

    seen = []
    real = runner.run

    def spy(argv, passphrase=None):
        seen.append(list(map(str, argv)))
        return real(argv, passphrase)

    monkeypatch.setattr(runner, "run", spy)
    s = two.session
    two.trust_alice()
    two.tag("me", "work")
    t = s.received("work")[0]
    s.check([t.path], definition=VOCAB, subject_key="work", as_="me")
    s.communities("me")
    verbs = {a[a.index("--wallet") + 2] for a in seen}
    assert verbs <= {"check", "root", "key", "make"}, verbs
    assert not any("--codec" in a for a in seen)


def test_the_engine_still_says_both_are_open():
    assert core.OPEN == ("DEC-004", "DEC-005")
