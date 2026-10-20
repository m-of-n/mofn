"""mofn#13 sample 2 — an in-toto Statement v1 inside a DSSE envelope.

Hand-rolled on purpose. A DSSE library would hide the two things worth looking
at: the PAE pre-authentication encoding, and the fact that `payloadType` is a
registered media type that is *inside the signature* and therefore cannot be
renegotiated after the fact.

Signing key: Ed25519 with a fixed seed, so the bytes are reproducible.
"""

import base64
import hashlib
import json

from cryptography.hazmat.primitives.asymmetric import ed25519

from common import OUT, emit, pae

ED25519_SEED = bytes.fromhex(
    "4ccd089b28ff96da9db6c346ec114e0f5b8a319f35aba624da8cf6ed4fb8a6fb"
)  # RFC 8032 §7.1, TEST 2

PAYLOAD_TYPE = "application/vnd.in-toto+json"


def statement() -> bytes:
    """An in-toto Statement v1. The exact bytes matter: DSSE signs the payload octets, so any re-serialisation by a consumer breaks verification. There is no canonicalisation step in DSSE — that is deliberate, and it is the counterpart to the R-O-05 question on our side."""
    blob = b"lane-a subject bytes"
    doc = {
        "_type": "https://in-toto.io/Statement/v1",
        "subject": [
            {
                "name": "lane-a-subject",
                "digest": {"sha256": hashlib.sha256(blob).hexdigest()},
            }
        ],
        "predicateType": "https://slsa.dev/provenance/v1",
        "predicate": {
            "buildDefinition": {
                "buildType": "https://example.invalid/lane-a/buildtype/v1",
                "externalParameters": {},
            },
            "runDetails": {
                "builder": {"id": "https://example.invalid/lane-a/builder"},
            },
        },
    }
    return json.dumps(doc, separators=(",", ":"), sort_keys=True).encode()


def main():
    tag = "dsse_intoto"

    sk = ed25519.Ed25519PrivateKey.from_private_bytes(ED25519_SEED)
    pub = sk.public_key().public_bytes_raw()
    # DSSE's keyid is opaque and unspecified — one of the few identifiers in
    # this sample that nobody allocates.
    keyid = "SHA256:" + base64.b64encode(hashlib.sha256(pub).digest()).decode()

    body = statement()
    to_sign = pae(PAYLOAD_TYPE, body)
    sig = sk.sign(to_sign)

    envelope = {
        "payload": base64.b64encode(body).decode(),
        "payloadType": PAYLOAD_TYPE,
        "signatures": [{"keyid": keyid, "sig": base64.b64encode(sig).decode()}],
    }
    env_bytes = json.dumps(envelope, indent=2).encode() + b"\n"

    emit(tag + ".statement", body, pretty_json=True)
    emit(tag + ".pae", to_sign)
    emit(tag + ".envelope", env_bytes, pretty_json=True)
    (OUT / (tag + ".pubkey.hex")).write_text(pub.hex() + "\n")

    # Verify the way a consumer must: rebuild the PAE from the envelope.
    got = json.loads(env_bytes)
    rebuilt = pae(got["payloadType"], base64.b64decode(got["payload"]))
    assert rebuilt == to_sign, "PAE mismatch"
    ed25519.Ed25519PublicKey.from_public_bytes(pub).verify(
        base64.b64decode(got["signatures"][0]["sig"]), rebuilt
    )
    print("  verified: yes (PAE rebuilt from the envelope, Ed25519)")
    print(f"  PAE prefix: {to_sign[:40]!r}...")


if __name__ == "__main__":
    print("sample 2 — in-toto Statement v1 in a DSSE envelope")
    main()
