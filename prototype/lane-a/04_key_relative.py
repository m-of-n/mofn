"""mofn#13 sample 4 — swap each registry identifier for a key-relative one, and see what breaks.

R-M-12 says a name should be a pair: (defining key, label). For every identifier found in samples 1 and 2, this script builds one message where only that identifier is swapped, signs it, and asks two questions:

  signature   does the signature still check? (cryptography, over a Sig_structure or PAE rebuilt from the message)
  consumer    does a real library accept the message? (pycose for COSE, in-toto-attestation for the in-toto Statement)

The key-relative form here is a placeholder, not a proposal. DEC-002, DEC-004 and DEC-005 are open. In CBOR it is the array [key id, label]; in JSON it is the string "key:<key id>:<label>". The key id is the SHA-256 of the raw public key.

The real SLSA provenance from sample 3 is not used: it was signed by a Fulcio key we do not hold, so any change breaks its signature.

Results go to out/key_relative.json, and every message is kept as bytes next to it.
"""

import base64
import hashlib
import importlib
import json

import cbor2
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import ed25519
from in_toto_attestation.v1 import statement_pb2
from in_toto_attestation.v1.statement import Statement
from google.protobuf import json_format
from pycose.keys.okp import OKPKey
from pycose.messages.sign1message import Sign1Message

from common import OUT, emit, pae

cose_sample = importlib.import_module("01_cose_sign1")
dsse_sample = importlib.import_module("02_dsse_intoto")


def key_id(pub: bytes) -> bytes:
    return hashlib.sha256(pub).digest()


def signature_checks(pub: bytes, sig: bytes, signed: bytes) -> bool:
    try:
        ed25519.Ed25519PublicKey.from_public_bytes(pub).verify(sig, signed)
        return True
    except InvalidSignature:
        return False


def cose_variants(k: bytes) -> dict:
    """Each entry is (protected header, unprotected header, payload, tagged). Only one thing changes per entry. A key-relative name is the tuple (k, label), which cbor2 writes as a CBOR array. A CBOR tag number is a single unsigned integer, so it cannot hold a pair; the closest test is to leave the tag off."""
    payload = {"subject": "urn:example:thing", "claim": "reviewed"}
    return {
        "baseline": ({1: -8, 3: 60}, {4: b"lane-a-ed25519"}, payload, True),
        "header label 1 (alg)": ({(k, 1): -8, 3: 60}, {4: b"lane-a-ed25519"}, payload, True),
        "alg value -8 (EdDSA)": ({1: (k, -8), 3: 60}, {4: b"lane-a-ed25519"}, payload, True),
        "header label 3 (content type)": ({1: -8, (k, 3): 60}, {4: b"lane-a-ed25519"}, payload, True),
        "content format 60 (application/cbor)": ({1: -8, 3: (k, 60)}, {4: b"lane-a-ed25519"}, payload, True),
        "header label 4 (kid)": ({1: -8, 3: 60}, {(k, 4): b"lane-a-ed25519"}, payload, True),
        "tag 18 (COSE_Sign1), left off": ({1: -8, 3: 60}, {4: b"lane-a-ed25519"}, payload, False),
        "payload key (not a registry name)": ({1: -8, 3: 60}, {4: b"lane-a-ed25519"}, {(k, 1): "urn:example:thing", "claim": "reviewed"}, True),
    }


def build_cose(sk, phdr: dict, uhdr: dict, payload: dict, tagged: bool) -> bytes:
    """Build a COSE_Sign1 by hand, so headers pycose would refuse to write can still be tested."""
    protected = cbor2.dumps(phdr)
    body = cbor2.dumps(payload)
    sig = sk.sign(cbor2.dumps(["Signature1", protected, b"", body]))
    msg = [protected, uhdr, body, sig]
    return cbor2.dumps(cbor2.CBORTag(18, msg) if tagged else msg)


def check_cose(encoded: bytes, pub: bytes, cose_key) -> tuple:
    """Signature: rebuild the Sig_structure from the message bytes. Consumer: pycose decode, then verify. pycose keeps a header label it does not know as a plain value instead of one of its header classes; those are counted as "kept but not understood"."""
    obj = cbor2.loads(encoded)
    protected, _uhdr, body, sig = obj.value if isinstance(obj, cbor2.CBORTag) else obj
    sig_ok = signature_checks(pub, sig, cbor2.dumps(["Signature1", protected, b"", body]))
    try:
        msg = Sign1Message.decode(encoded)
        msg.key = cose_key
        accepted = bool(msg.verify_signature())
        unknown = [h for h in [*msg.phdr, *msg.uhdr] if not isinstance(h, type)]
        said = "verified" if accepted else "verify_signature() returned False"
        if unknown:
            said += f"; {len(unknown)} header label(s) kept but not understood"
    except Exception as e:
        accepted, said = False, f"{type(e).__name__}: {e}"
    return sig_ok, accepted, said


def run_cose() -> list:
    seed = cose_sample.ED25519_SEED
    sk = ed25519.Ed25519PrivateKey.from_private_bytes(seed)
    pub = sk.public_key().public_bytes_raw()
    cose_key = OKPKey(crv="ED25519", x=pub, d=seed)
    k = key_id(pub)

    rows = []
    for i, (what, (phdr, uhdr, payload, tagged)) in enumerate(cose_variants(k).items()):
        encoded = build_cose(sk, phdr, uhdr, payload, tagged)
        emit(f"key_relative.cose.{i}", encoded, cbor=True)
        sig_ok, accepted, said = check_cose(encoded, pub, cose_key)
        rows.append({"format": "COSE_Sign1", "file": f"key_relative.cose.{i}.bin", "identifier": what, "signature": sig_ok, "consumer": "pycose", "accepted": accepted, "said": said})

    baseline = (OUT / "key_relative.cose.0.bin").read_bytes()
    assert baseline == (OUT / "cose_sign1_eddsa.bin").read_bytes(), "hand-built baseline differs from sample 1; run 01 first"
    return rows


def dsse_variants(doc: dict, k: str) -> dict:
    """Each entry is (payloadType, Statement). Only one thing changes per entry."""

    def changed(edit):
        d = json.loads(json.dumps(doc))
        edit(d)
        return d

    def rename_digest(d):
        s = d["subject"][0]["digest"]
        s[k + ":sha256"] = s.pop("sha256")

    return {
        "baseline": (dsse_sample.PAYLOAD_TYPE, doc),
        "payloadType": (k + ":payloadType", doc),
        "_type": (dsse_sample.PAYLOAD_TYPE, changed(lambda d: d.update(_type=k + ":Statement"))),
        "predicateType": (dsse_sample.PAYLOAD_TYPE, changed(lambda d: d.update(predicateType=k + ":provenance"))),
        "digest name sha256": (dsse_sample.PAYLOAD_TYPE, changed(rename_digest)),
        "buildType": (dsse_sample.PAYLOAD_TYPE, changed(lambda d: d["predicate"]["buildDefinition"].update(buildType=k + ":buildType"))),
        "builder.id": (dsse_sample.PAYLOAD_TYPE, changed(lambda d: d["predicate"]["runDetails"]["builder"].update(id=k + ":builder"))),
    }


def check_dsse(envelope: dict, pub: bytes) -> tuple:
    """Signature: rebuild the PAE from the envelope. Consumer: in-toto-attestation parses the Statement and runs validate(). That library does not read DSSE envelopes, so it never sees payloadType."""
    body = base64.b64decode(envelope["payload"])
    sig = base64.b64decode(envelope["signatures"][0]["sig"])
    sig_ok = signature_checks(pub, sig, pae(envelope["payloadType"], body))
    try:
        stmt = Statement.copy_from_pb(json_format.Parse(body, statement_pb2.Statement()))
        stmt.validate()
        accepted, said = True, "validate() passed"
    except Exception as e:
        accepted, said = False, f"{type(e).__name__}: {e}"
    return sig_ok, accepted, said


def run_dsse() -> list:
    sk = ed25519.Ed25519PrivateKey.from_private_bytes(dsse_sample.ED25519_SEED)
    pub = sk.public_key().public_bytes_raw()
    k = "key:" + key_id(pub).hex()
    doc = json.loads(dsse_sample.statement())

    rows = []
    for i, (what, (payload_type, stmt)) in enumerate(dsse_variants(doc, k).items()):
        body = json.dumps(stmt, separators=(",", ":"), sort_keys=True).encode()
        sig = sk.sign(pae(payload_type, body))
        envelope = {
            "payload": base64.b64encode(body).decode(),
            "payloadType": payload_type,
            "signatures": [{"keyid": "", "sig": base64.b64encode(sig).decode()}],
        }
        emit(f"key_relative.dsse.{i}", json.dumps(envelope, indent=2).encode() + b"\n", pretty_json=True)
        sig_ok, accepted, said = check_dsse(envelope, pub)
        if payload_type != dsse_sample.PAYLOAD_TYPE:
            accepted, said = None, "not tested: in-toto-attestation does not read payloadType"
        rows.append({"format": "DSSE + in-toto", "file": f"key_relative.dsse.{i}.json", "identifier": what, "signature": sig_ok, "consumer": "in-toto-attestation", "accepted": accepted, "said": said})

    baseline = json.loads((OUT / "key_relative.dsse.0.json").read_bytes())
    assert base64.b64decode(baseline["payload"]) == dsse_sample.statement(), "baseline Statement differs from sample 2"
    return rows


def main():
    print("sample 4 — key-relative identifiers: what still works")
    rows = run_cose() + run_dsse()
    (OUT / "key_relative.json").write_text(json.dumps(rows, indent=2) + "\n")
    print()
    print(f"  {'format':<15} {'identifier':<38} {'sig':<4} {'consumer':<9} said")
    for r in rows:
        accepted = {True: "yes", False: "NO", None: "-"}[r["accepted"]]
        print(f"  {r['format']:<15} {r['identifier']:<38} {'yes' if r['signature'] else 'NO':<4} {accepted:<9} {r['said'][:90]}")
    print("  wrote out/key_relative.json")


if __name__ == "__main__":
    main()
