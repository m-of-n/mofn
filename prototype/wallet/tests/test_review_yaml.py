"""The human-review codec (SPEC-0002 §11)."""

import pytest

from conftest import FIXTURES, VECTORS, envelope, keystore, seed
from engine import signer
from engine.codecs import CODECS
from engine.errors import EncodingError, Invalid
from engine.verifier import verify

Y = CODECS["review-yaml"]

TV4_HUMAN = """\
kind: attestation
suite: ksa-ed25519-sha256
says: '0x21fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9'
this: {digest: {alg: sha-256, value: '0x48dfc39586b0c4f9e905b3b60f59a30b7c0c7408e44f7cb4df2a09fbf3e67ba7'}}
valid:
  not before: "2026-10-06T00:00:00Z"
  not on or after: "2026-11-01T00:00:00Z"
  issued: "2026-10-06T10:30:00Z"
body:
  has:
    - type: {definition: '0x517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a7175', label: build-provenance}
      value: reproducible
signed:
  value: '0x8f30ee4ef039d81813703a2b629bb60e5abfc5b82a07432594a2add6fb77d24ccb9a41d744022af89e5ce0ead553131929e2f66fbd1c2ec1869b2c4c91319c0f'
"""


def test_tv4_human_form_is_the_printed_example():
    assert Y.dump(envelope("TV-4")).decode() == TV4_HUMAN


def test_printed_example_reads_back_to_tv4():
    assert Y.load(TV4_HUMAN.encode()) == envelope("TV-4")


@pytest.mark.parametrize("name", sorted(VECTORS["positive"]))
def test_round_trip_is_byte_exact(name):
    e = envelope(name)
    human = Y.dump(e)
    assert Y.load(human) == e
    assert Y.dump(Y.load(human)) == human
    verify(Y.load(human), keystore())


def test_annotations_are_dropped():
    annotated = TV4_HUMAN.replace(
        "kind: attestation\n", "_note: looks fine\nkind: attestation\n"
    )
    assert Y.load(annotated.encode()) == envelope("TV-4")


def awkward(value) -> bytes:
    alice = bytes.fromhex(VECTORS["keys"]["alice"]["kid"])
    s = {
        1: 4,
        2: 1,
        3: alice,
        4: [5, value],
        6: {1: [{1: {1: bytes(32), 2: "x"}, 2: value}]},
    }
    return signer.sign(seed("alice"), s)


@pytest.mark.parametrize(
    "value",
    [
        "yes",
        "1",
        "a: b",
        "  padded ",
        "null",
        "Ünïcødé",
        "line\nbreak",
        "#hash",
        "-dash",
        "2026-10-06",
        "1.5",
        "~",
        "on",
    ],
)
def test_awkward_text_round_trips(value):
    e = awkward(value)
    assert Y.load(Y.dump(e)) == e


def test_text_that_looks_like_bytes_is_refused_in_a_value():
    with pytest.raises(EncodingError):
        Y.dump(awkward("0x12"))


def mutate(old: str, new: str) -> bytes:
    assert old in TV4_HUMAN
    return TV4_HUMAN.replace(old, new, 1).encode()


REJECT = {
    "explicit tag": mutate("kind: attestation", "kind: !!str attestation"),
    "anchor": mutate("kind: attestation", "kind: &k attestation"),
    "unquoted timestamp": mutate(
        'not before: "2026-10-06T00:00:00Z"', "not before: 2026-10-06T00:00:00Z"
    ),
    "time with a space": mutate('"2026-10-06T00:00:00Z"', '"2026-10-06 00:00:00Z"'),
    "unquoted bytes": mutate("says: '0x21fe", "says: 0x21fe").replace(
        b"b9'\nthis", b"b9\nthis"
    ),
    "upper-case hex": mutate("'0x21fe31df", "'0x21FE31DF"),
    "null value": mutate("value: reproducible", "value: null"),
    "tilde value": mutate("value: reproducible", "value: ~"),
    "float value": mutate("value: reproducible", "value: 1.5"),
    "yes value": mutate("value: reproducible", "value: yes"),
    "hex int": mutate("value: reproducible", "value: 0x1f"),
    "plus int": mutate("value: reproducible", "value: +1"),
    "leading zero": mutate("value: reproducible", "value: 012"),
    "underscore int": mutate("value: reproducible", "value: 1_000"),
    "sexagesimal": mutate("value: reproducible", "value: 1:30"),
    "minus zero": mutate("value: reproducible", "value: -0"),
    "duplicate key": mutate(
        "kind: attestation\n", "kind: attestation\nkind: attestation\n"
    ),
    "unknown field": mutate("kind: attestation\n", "kind: attestation\ncolour: blue\n"),
    "unknown kind": mutate("kind: attestation", "kind: opinion"),
    "two documents": TV4_HUMAN.encode() + b"---\nkind: attestation\n",
    "no signed": TV4_HUMAN.split("signed:")[0].encode(),
    "not utf-8": TV4_HUMAN.encode().replace(b"reproducible", b"reproducibl\xff"),
}


@pytest.mark.parametrize("name", sorted(REJECT))
def test_rejects(name):
    with pytest.raises(EncodingError):
        Y.load(REJECT[name])


def test_a_changed_value_fails_the_signature_not_the_reader():
    e = Y.load(mutate("value: reproducible", "value: attested"))
    with pytest.raises(Invalid) as x:
        verify(e, keystore())
    assert x.value.reason == "signature"


@pytest.mark.parametrize(
    "name,stem",
    [("TV-1", "tv-1-alice.pub"), ("TV-3", "tv-3-define"), ("TV-4", "tv-4-attestation")],
)
def test_fixture_yaml_reads_back_to_the_vector(name, stem):
    assert Y.load((FIXTURES / f"{stem}.stmt.yaml").read_bytes()) == envelope(name)
