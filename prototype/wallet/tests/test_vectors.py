"""SPEC-0002 Appendix A: a conforming verifier returns verified for TV-1…8
and invalid at the stated step for N-1…6."""

import pytest

from conftest import VECTORS, keystore
from engine.encoding.ksa_cbor import decode, encode
from engine.errors import Invalid
from engine.verifier import verify

NEGATIVE = {
    "N-1": ("V5", "encoding"),
    "N-2": ("V4", "signature"),
    "N-3": ("V6", "envelope-mismatch"),
    "N-4": ("V3", "key"),
    "N-5": ("V4", "signature"),
    "N-6": ("V5", "encoding"),
}


@pytest.mark.parametrize("name", sorted(VECTORS["positive"]))
def test_positive_verifies(name):
    v = VECTORS["positive"][name]
    got = verify(bytes.fromhex(v["envelope"]), keystore())
    assert got.digest.hex() == v["digest"]
    assert got.tbs.hex() == v["tbs"]


@pytest.mark.parametrize("name", sorted(VECTORS["positive"]))
def test_encoder_reproduces_tbs(name):
    tbs = bytes.fromhex(VECTORS["positive"][name]["tbs"])
    assert encode(decode(tbs)) == tbs


@pytest.mark.parametrize("name", sorted(NEGATIVE))
def test_negative_rejected_at_step(name):
    with pytest.raises(Invalid) as e:
        verify(bytes.fromhex(VECTORS["negative"][name]["envelope"]), keystore())
    assert (e.value.step, e.value.reason) == NEGATIVE[name]
    assert VECTORS["negative"][name]["step"].startswith(NEGATIVE[name][0])


def test_key_publish_verifies_from_its_own_pub():
    assert verify(bytes.fromhex(VECTORS["positive"]["TV-1"]["envelope"]), {}).kind == 1
