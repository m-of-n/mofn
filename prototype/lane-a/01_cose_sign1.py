"""mofn#13 sample 1 — a COSE_Sign1 signed statement, built with pycose.

Ed25519 / alg -8, CBOR payload. Deterministic: the bytes are reproducible.

The payload is deliberately uninteresting. DEC-002 is open and ARCH-0001 §9.4 applies: nothing here may imply a native encoding. What we are looking at is the *envelope*, not the statement inside it.
"""

import cbor2
from cryptography.hazmat.primitives.asymmetric import ed25519
from pycose.algorithms import EdDSA
from pycose.headers import KID, Algorithm, ContentType
from pycose.keys.okp import OKPKey
from pycose.messages.sign1message import Sign1Message

from common import OUT, diag, emit

# Fixed seed so the sample is byte-reproducible. Test key. Not secret.
ED25519_SEED = bytes.fromhex(
    "9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60"
)  # RFC 8032 §7.1


def build_eddsa():
    """Encode a CBOR map as the payload. Build a COSE_Sign1: encode the protected header, sign the two headers and the payload, then CBOR-encode the two headers, the payload and the signature as one array. Write the COSE message and the payload to separate .bin/.hex/.edn files."""
    name = "cose_sign1_eddsa"

    sk = ed25519.Ed25519PrivateKey.from_private_bytes(ED25519_SEED)
    pub = sk.public_key().public_bytes_raw()
    key = OKPKey(crv="ED25519", x=pub, d=ED25519_SEED)

    payload = cbor2.dumps({"subject": "urn:example:thing", "claim": "reviewed"})

    msg = Sign1Message(
        phdr={Algorithm: EdDSA, ContentType: 60},
        uhdr={KID: b"lane-a-ed25519"},
        payload=payload,
    )
    msg.key = key
    encoded = msg.encode(tag=True)

    emit(name, encoded, cbor=True)
    emit(name + ".payload", payload, cbor=True)

    (OUT / (name + ".phdr.edn")).write_text(diag(cbor2.loads(msg.phdr_encoded)) + "\n")

    round_trip = Sign1Message.decode(encoded)
    round_trip.key = key
    assert round_trip.verify_signature(), "EdDSA verification failed"
    print("  verified: yes")

    tag = cbor2.loads(encoded)
    assert tag.tag == 18, f"expected COSE_Sign1 tag 18, got {tag.tag}"
    protected, _unprotected, got_payload, sig = tag.value
    assert got_payload == payload, "payload changed in the envelope"
    sig_structure = cbor2.dumps(["Signature1", protected, b"", got_payload])
    emit(name + ".sig_structure", sig_structure, cbor=True)
    sk.public_key().verify(sig, sig_structure)
    print("  Sig_structure rebuilt from the message verifies (cryptography): yes")


if __name__ == "__main__":
    print("sample 1 — COSE_Sign1 (RFC 9052), pycose, EdDSA / Ed25519")
    build_eddsa()
