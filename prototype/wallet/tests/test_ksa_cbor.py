"""The validating decoder (SPEC-0002 §4.3): it accepts exactly the KSA-CBOR
encoding of a data-model value and rejects everything else, without repair.
The fixtures are those of prototype/statements/test_decode.py, changed where
KSA-CBOR differs from the reduced profile."""

import pytest

import engine.encoding.ksa_cbor as m
from engine.encoding.ksa_cbor import decode, encode
from engine.errors import EncodingError

ACCEPT = [23, 24, 256, -1, b"\x01\x02", "hello", "", [1, 2, 3], [], {"a": 1, "b": 2}, {}, False, True,
          {"z": [1, {"a": b"\xff"}], "a": "x"}, "Ünïcødé ✓", {1: "x", 2: "y"}, 2**53 - 1, -(2**53 - 1)]

REJECT = {
    "map keys out of order": bytes([0xA2]) + encode("b") + encode(2) + encode("a") + encode(1),
    "duplicate map key": bytes([0xA2]) + encode("a") + encode(1) + encode("a") + encode(2),
    "non-smallest head 24 in 2B": bytes([0x19, 0x00, 0x18]),
    "non-smallest head 0 in 1B": bytes([0x18, 0x00]),
    "non-smallest head in 4B": bytes([0x1A, 0x00, 0x00, 0xFF, 0xFF]),
    "non-smallest bstr length": bytes([0x58, 0x01, 0x41]),
    "indefinite array": bytes([0x9F, 0x01, 0xFF]),
    "indefinite bstr": bytes([0x5F, 0x41, 0x41, 0xFF]),
    "tag": bytes([0xC0]) + encode("x"),
    "float16": bytes([0xF9, 0x00, 0x00]),
    "float32": bytes([0xFA, 0, 0, 0, 0]),
    "float64": bytes([0xFB, 0, 0, 0, 0, 0, 0, 0, 0]),
    "null": bytes([0xF6]),
    "undefined": bytes([0xF7]),
    "simple value 0": bytes([0xE0]),
    "reserved ai 28": bytes([0x1C]),
    "invalid UTF-8": bytes([0x62, 0xFF, 0xFE]),
    "truncated array": bytes([0x83, 0x01]),
    "trailing bytes": encode(1) + b"\x01",
    "array as map key": bytes([0xA1, 0x80, 0x01]),
    "bytes as map key": bytes([0xA1, 0x41, 0x00, 0x01]),
    "negative map key": bytes([0xA1, 0x20, 0x01]),
    "bool as map key": bytes([0xA1, 0xF5, 0x01]),
    "integer 2^53": bytes([0x1B]) + (2**53).to_bytes(8, "big"),
    "integer -2^53": bytes([0x3B]) + (2**53 - 1).to_bytes(8, "big"),
    "deep nesting": bytes([0x81]) * 300 + bytes([0x01]),
}


@pytest.mark.parametrize("value", ACCEPT, ids=repr)
def test_accepts_canonical(value):
    assert decode(encode(value)) == value


@pytest.mark.parametrize("name", sorted(REJECT))
def test_rejects(name):
    with pytest.raises(EncodingError):
        decode(REJECT[name])


@pytest.mark.parametrize("value", [None, 1.5, 2**53, -(2**53), {b"k": 1}, {-1: 1}, {True: 1}])
def test_encoder_refuses_outside_data_model(value):
    with pytest.raises(EncodingError):
        encode(value)


def test_decoder_never_re_encodes(monkeypatch):
    good = encode({"z": [1, {"a": b"\xff"}], "a": "x"})
    monkeypatch.setattr(m, "encode", None)
    monkeypatch.setattr(m, "_head", None)
    assert m.decode(good) == {"z": [1, {"a": b"\xff"}], "a": "x"}
    with pytest.raises(EncodingError):
        m.decode(REJECT["map keys out of order"])
