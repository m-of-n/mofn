"""`check` at the engine level, over the published vectors: TV-1 (Alice's
key), TV-3 (DV-1's define), TV-4 (Alice's attestation about the example
artifact). No wallet directory is involved."""

import hashlib

import pytest

from conftest import VECTORS, envelope, keystore, seed
from engine import check, definition, envelope as env, ksatime, signer
from engine.encoding.ksa_cbor import decode, encode
from engine.reduce import Anchor

ARTIFACT = b"ksa example artifact\n"
DV1 = bytes.fromhex(VECTORS["definitions"]["DV-1"]["body"])
DV1_ID = bytes.fromhex(VECTORS["definitions"]["DV-1"]["id"])
ALICE = bytes.fromhex(VECTORS["keys"]["alice"]["kid"])
BOB = bytes.fromhex(VECTORS["keys"]["bob"]["kid"])
CAROL = bytes.fromhex(VECTORS["keys"]["carol"]["kid"])
BP = {1: DV1_ID, 2: "build-provenance"}
SENTENCE = "Alice attests that sha-256:48dfc39586b0c4f9 was built reproducibly from published sources."


def anchor(trusts=ALICE, rng=("reproducible", "attested")):
    return Anchor(
        "releases",
        trusts,
        [{1: BP, 3: list(rng)} if rng else {1: BP}],
        CAROL,
        ksatime.from_text("2026-10-06T00:00:00Z"),
    )


def run(
    statements,
    anchors=None,
    at="2026-10-10T12:00:00Z",
    artifact=ARTIFACT,
    definition=DV1,
    ks=None,
):
    ks = keystore() if ks is None else ks
    items = [check.handed(f"s{i}", e, ks) for i, e in enumerate(statements)]
    return check.run(
        items,
        artifact,
        definition,
        {ALICE: "Alice", BOB: "Bob"},
        [anchor()] if anchors is None else anchors,
        "releases",
        ksatime.from_text(at),
    )


def lines(answer):
    return {ln.name: ln.result for ln in answer.lines}


def attestation(signer_name, valid, template=None, carry_pub=False):
    body = {1: [{1: BP, 2: "reproducible"}]}
    if template:
        body[3] = {1: DV1_ID, 2: template}
    kid = bytes.fromhex(VECTORS["keys"][signer_name]["kid"])
    s = {
        1: 4,
        2: 1,
        3: kid,
        4: [2, 1, hashlib.sha256(ARTIFACT).digest()],
        5: {1: ksatime.from_text(valid[0]), 2: ksatime.from_text(valid[1])},
        6: body,
    }
    return signer.sign(seed(signer_name), s, carry_pub=carry_pub)


def test_tv4_renders_the_spec_sentence():
    a = run([envelope("TV-4"), envelope("TV-3")])
    assert a.sentences == [SENTENCE]
    assert set(lines(a).values()) == {"pass"}
    assert a.yes and a.exit_code == 0


def test_json_answer_has_the_spec_shape():
    j = run([envelope("TV-4"), envelope("TV-3")]).to_json()
    assert j["answer"] == "yes" and j["at"] == "2026-10-10T12:00:00Z"
    assert j["because"][0]["used"] == [VECTORS["positive"]["TV-4"]["digest"]]
    assert j["because"][0]["path"][0]["scope"] == {
        "build-provenance": ["reproducible", "attested"]
    }
    assert {"revocations considered": 0} in j["because"]
    assert set(j["verdict"]) == {
        "integrity",
        "authenticity",
        "names",
        "authorization",
        "acceptance",
        "semantics",
    }


def test_tampered_statement_fails_integrity_at_the_signature():
    e = bytearray(envelope("TV-4"))
    e[-1] ^= 0x01
    a = run([bytes(e), envelope("TV-3")])
    assert lines(a)["integrity"] == "fail" and "(signature)" in a.lines[0].sentence
    assert a.exit_code == 3


def test_unknown_field_is_invalid_at_v7():
    s = decode(bytes.fromhex(VECTORS["positive"]["TV-4"]["tbs"]))
    s[7] = "extra"
    a = run([signer.sign(seed("alice"), s), envelope("TV-3")])
    assert (a.handed[0].step, a.handed[0].reason) == ("V7", "structure")
    assert lines(a)["integrity"] == "fail" and a.exit_code == 3


def test_definition_without_its_define_is_unattributed():
    a = run([envelope("TV-4")])
    assert lines(a)["semantics"] == "fail" and "unattributed" in a.lines[5].sentence
    assert lines(a)["authorization"] == "fail"
    assert a.coverage.stopped[0].code == "unattributed-definition"


def test_no_anchor_is_no_path():
    a = run([envelope("TV-4"), envelope("TV-3")], anchors=[])
    assert (
        lines(a)["authorization"] == "fail" and a.coverage.stopped[0].code == "no-path"
    )
    assert lines(a)["authenticity"] == "pass" and a.exit_code == 1


def test_anchor_for_another_value_does_not_cover():
    a = run([envelope("TV-4"), envelope("TV-3")], anchors=[anchor(rng=("attested",))])
    assert lines(a)["authorization"] == "fail"
    assert "not about build provenance = reproducible" in a.lines[3].sentence


def test_anchor_in_another_context_does_not_cover():
    other = anchor()
    other.context = "elsewhere"
    assert (
        lines(run([envelope("TV-4"), envelope("TV-3")], anchors=[other]))[
            "authorization"
        ]
        == "fail"
    )


def test_unbounded_anchor_covers():
    assert run([envelope("TV-4"), envelope("TV-3")], anchors=[anchor(rng=None)]).yes


def test_expired_statement_is_not_covered():
    a = run([envelope("TV-4"), envelope("TV-3")], at="2026-11-02T00:00:00Z")
    assert a.coverage.stopped[0].code == "not-valid-at-time"


def test_unknown_key_is_unverifiable_and_fails_authenticity():
    ks = {k: v for k, v in keystore().items() if k[1] != ALICE}
    a = run([envelope("TV-4"), envelope("TV-3")], ks=ks)
    assert a.handed[0].result == "unverifiable" and a.handed[0].reason == "unknown-key"
    assert lines(a)["authenticity"] == "fail" and a.exit_code == 1


def test_key_only_from_pub_hint_fails_authenticity():
    ks = {k: v for k, v in keystore().items() if k[1] != BOB}
    e = attestation(
        "bob", ("2026-10-06T00:00:00Z", "2026-11-01T00:00:00Z"), carry_pub=True
    )
    a = run([e, envelope("TV-3")], anchors=[anchor(trusts=BOB)], ks=ks)
    assert a.handed[0].result == "verified"
    assert lines(a)["authenticity"] == "fail" and not a.yes


def test_tampered_artifact_fails_integrity():
    a = run([envelope("TV-4"), envelope("TV-3")], artifact=b"X" + ARTIFACT[1:])
    assert (
        lines(a)["integrity"] == "fail" and lines(a)["authorization"] == "not evaluated"
    )
    assert a.exit_code == 1


def test_template_that_conforms_passes_acceptance():
    e = attestation(
        "alice",
        ("2026-10-06T00:00:00Z", "2026-11-01T00:00:00Z"),
        template="release-attestation",
    )
    a = run([e, envelope("TV-3")])
    assert (
        lines(a)["acceptance"] == "pass"
        and "release attestation" in a.lines[4].sentence
        and a.yes
    )


def test_template_over_max_validity_fails_acceptance():
    e = attestation(
        "alice",
        ("2026-10-06T00:00:00Z", "2026-11-20T00:00:00Z"),
        template="release-attestation",
    )
    a = run([e, envelope("TV-3")])
    assert lines(a)["acceptance"] == "fail" and a.coverage.stopped[0].code == "template"


def test_wrong_definition_is_unobtainable():
    body = decode(DV1)
    body[3] = "2"
    a = run([envelope("TV-4"), envelope("TV-3")], definition=encode(body))
    assert (
        lines(a)["semantics"] == "fail"
        and "definition-unobtainable" in a.lines[5].sentence
    )


@pytest.mark.parametrize(
    "change", ["no short", "bad label", "duplicate label", "unknown key"]
)
def test_non_conforming_definition_fails_semantics(change):
    body = decode(DV1)
    t = body[5][0][1]
    if change == "no short":
        del t[4]
    elif change == "bad label":
        t[1] = "Build_Provenance"
    elif change == "duplicate label":
        body[5][1][1][1] = "build-provenance"
    else:
        t[99] = 1
    a = run([envelope("TV-4"), envelope("TV-3")], definition=encode(body))
    assert (
        lines(a)["semantics"] == "fail"
        and "definition-non-conforming" in a.lines[5].sentence
    )


def test_envelope_hint_mismatch_is_invalid():
    e = env.split(envelope("TV-4"))
    a = run([env.build(e.suite, BOB, e.tbs, e.sig), envelope("TV-3")])
    assert a.handed[0].result in ("invalid", "unverifiable")
    assert not a.yes


def test_dv1_id_recomputes():
    assert hashlib.sha256(DV1).digest() == DV1_ID
    assert definition.load(DV1).id == DV1_ID
