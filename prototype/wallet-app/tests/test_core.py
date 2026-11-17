"""The app's engine door (`mofn_app/core.py`), without a window.

The acceptance case of #179: for the W-4 slice cases the app shows the same
verdict as the CLI. Here "the CLI" is `mofn` run in its own process, and the
app's JSON must equal it, `associations` included."""

import json
import os

from conftest import AT, GOLDEN, PASS, STATEMENTS, VOCAB, mofn

from mofn_app import core


def comparable(j):
    return [{k: v for k, v in a.items() if k != "file"} for a in j["associations"]]


def app_check(world, artifact):
    r, j = world.session.check(STATEMENTS, artifact, VOCAB, at=AT)
    return r.code, j


def test_unauthorized_matches_the_cli(world):
    code, j = app_check(world, world.app)
    assert (code, j) == world.cli_json(world.app)
    assert j["verdict"]["authorization"]["result"] == "fail"
    assert comparable(j) == json.loads((GOLDEN / "associations-unauthorized.json").read_text())


def test_integrity_fail_matches_the_cli(world):
    world.trust_alice()
    code, j = app_check(world, world.bad)
    assert (code, j) == world.cli_json(world.bad)
    assert j["verdict"]["integrity"]["result"] == "fail"
    assert comparable(j) == json.loads((GOLDEN / "associations-tampered.json").read_text())


def test_green_matches_the_cli(world):
    world.trust_alice()
    code, j = app_check(world, world.app)
    assert (code, j) == world.cli_json(world.app)
    assert (code, j["answer"]) == (0, "yes")
    assert comparable(j) == json.loads((GOLDEN / "associations-green.json").read_text())
    a = j["associations"][0]
    assert {"signed-by", "topic", "subject", "standing"} <= set(a)


def test_sign_then_verify_is_green(world, tmp_path):
    s = world.session
    world.trust_alice()
    assert s.root_add("me", "me", VOCAB, "build-provenance", ["reproducible"]).ok
    r = s.sign("me", world.app, VOCAB, "build-provenance", "reproducible", 30, PASS)
    assert r.ok, r.err
    written = r.out.splitlines()[0].removeprefix("wrote ")
    r2, j = s.check([written, str(core.EXAMPLE_DEFINE)], world.app, VOCAB)
    assert j["answer"] == "yes", j["verdict"]
    assert j["associations"][0]["signed-by"]["key"] == "me"


def test_a_wrong_passphrase_is_an_error_not_a_signature(world):
    before = sorted((world.session.root / "statements").iterdir())
    r = world.session.sign("me", world.app, VOCAB, "build-provenance", "reproducible", 30, b"wrong")
    assert not r.ok and "passphrase" in r.error.lower()
    assert sorted((world.session.root / "statements").iterdir()) == before


def test_the_passphrase_is_never_on_argv_or_in_the_environment(world):
    secret = b"a passphrase that must not leak"
    before = dict(os.environ)
    r = world.session.key_gen("you", "person", secret)
    assert r.ok
    assert all(secret.decode() not in a for a in r.argv)
    assert secret.decode() not in r.shown
    assert dict(os.environ) == before
    assert all(secret.decode() not in v for v in os.environ.values())
    assert secret.decode() not in r.out + r.err


def test_the_status_command_is_what_a_shell_would_type(world):
    r = world.session.key_import(str(core.WALLET_SOURCE / "fixtures" / "tv-1-alice.pub.stmt"), "Again")
    assert r.shown.startswith(f"mofn --wallet {world.session.root} key import ")


def test_anchors_and_counts_read_the_wallet(world):
    world.trust_alice()
    a = world.session.anchors()
    assert [(x.key, x.about, x.values) for x in a] == [("Alice", "build-provenance", "reproducible")]
    n = world.session.counts()
    assert [p.label for p in n["owned"]] == ["me"] and n["anchors"] == 1


def test_inspect_names_kind_and_signer(world):
    info = world.session.inspect(STATEMENTS[0])
    assert info["kind"] == "attestation" and info["verified"] and info["says"] == "Alice"
    assert world.session.inspect(VOCAB)["kind"] == "definition"


def test_self_test_passes():
    assert core.self_test() == 0


def test_cli_and_app_share_one_wallet(world):
    """A key made in the app is listed by the CLI, from the same folder."""
    p = mofn("--wallet", world.session.root, "key", "list", "--format", "json")
    assert "me" in [k["label"] for k in json.loads(p.stdout)["keys"]]


# ----------------------------------------------------------- standing words

ROOT = {"role": "root", "anchor": "local", "accepted-by": "me", "key": "Alice", "kid": "aa"}
HOP = {"role": "delegation", "trust": "bb", "key": "Bob", "kid": "cc"}


def test_words_for_a_chain():
    st = {"result": "standing", "chain": [ROOT, HOP]}
    assert core.standing_words(st, "Bob") == (
        "You trust Alice (accepted by me). Alice passed that on to Bob. So Bob may say this."
    )


def test_words_for_a_broken_link():
    st = {"result": "no-standing", "chain": [ROOT], "detail": "more than Alice was given",
          "broken": {"from": "Alice", "to": "Carol"}}
    assert core.standing_words(st, "Carol").endswith("But the link Alice → Carol is broken: more than Alice was given.")


def test_words_for_no_standing():
    st = {"result": "no-standing", "chain": [], "text": "no standing: no anchor trusts the speaker (no-path)"}
    assert core.standing_words(st, "Alice") == "No anchor trusts the speaker (no-path)."
