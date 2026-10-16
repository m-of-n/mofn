#!/usr/bin/env python3
"""Generate the KSA core test vectors (SPEC-0002 Appendix A, SPEC-0003 Appendix A).

    python3 generate.py            # writes vectors.json and vectors.md beside this file

Requires `cryptography` (Ed25519, SHA-256) and `cbor2` (deterministic CBOR).
No cryptographic primitive is implemented here: signing and hashing come from
`cryptography`. Every positive vector is encoded twice — by cbor2's canonical
mode and by the independent encoder `ksa_cbor()` below — and the two MUST agree.

Keys are derived from fixed seeds so every byte is reproducible. Alice and Bob
use the RFC 8032 §7.1 TEST 1 and TEST 2 secret keys.
"""
import hashlib, json, pathlib, struct, datetime
import cbor2
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

HERE = pathlib.Path(__file__).resolve().parent
DS = b"KSA-STMT-SIG-v1\x00"          # SPEC-0002 §6.4
L = 2**252 + 27742317777372353535851937790883648493

# ---------------------------------------------------------------- encoding
def ksa_cbor(v) -> bytes:
    """Independent deterministic CBOR encoder for the KSA data model
    (SPEC-0002 §4): unsigned/negative ints, byte strings, text, arrays, maps
    with keys sorted by their encoded bytes, true/false. Nothing else."""
    def head(major, n):
        if n < 24: return bytes([major << 5 | n])
        if n < 2**8: return bytes([major << 5 | 24, n])
        if n < 2**16: return bytes([major << 5 | 25]) + struct.pack(">H", n)
        if n < 2**32: return bytes([major << 5 | 26]) + struct.pack(">I", n)
        return bytes([major << 5 | 27]) + struct.pack(">Q", n)
    if v is True: return b"\xf5"
    if v is False: return b"\xf4"
    if isinstance(v, int):
        assert -(2**53 - 1) <= v <= 2**53 - 1, "integer outside KSA range"
        return head(0, v) if v >= 0 else head(1, -1 - v)
    if isinstance(v, bytes): return head(2, len(v)) + v
    if isinstance(v, str):
        b = v.encode("utf-8"); return head(3, len(b)) + b
    if isinstance(v, list): return head(4, len(v)) + b"".join(ksa_cbor(x) for x in v)
    if isinstance(v, dict):
        items = sorted(((ksa_cbor(k), ksa_cbor(x)) for k, x in v.items()), key=lambda kv: kv[0])
        assert len({k for k, _ in items}) == len(items), "duplicate map key"
        return head(5, len(items)) + b"".join(k + x for k, x in items)
    raise TypeError(f"not in the KSA data model: {type(v).__name__}")

def enc(v) -> bytes:
    a, b = ksa_cbor(v), cbor2.dumps(v, canonical=True)
    assert a == b, "encoders disagree"
    return a

# ---------------------------------------------------------------- time (SPEC-0002 §4.4)
EPOCH = datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc)
def t(text: str) -> int:
    d = datetime.datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
    s = int((d - EPOCH).total_seconds())
    return 2 * (s // 86400) + 1 if s % 86400 == 0 else 2 * s

# ---------------------------------------------------------------- keys
def key(seed_hex):
    sk = Ed25519PrivateKey.from_private_bytes(bytes.fromhex(seed_hex))
    pub = sk.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    return sk, pub, hashlib.sha256(pub).digest()

SEEDS = {
    "alice": "9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60",  # RFC 8032 TEST 1
    "bob":   "4ccd089b28ff96da9db6c346ec114e0f5b8a319f35aba624da8cf6ed4fb8a6fb",  # RFC 8032 TEST 2
    "carol": hashlib.sha256(b"ksa-test-carol").hexdigest(),
    "bob2":  hashlib.sha256(b"ksa-test-bob2").hexdigest(),
}
K = {n: key(s) for n, s in SEEDS.items()}
kid = lambda n: K[n][2]

# ---------------------------------------------------------------- codes (SPEC-0002 §7, SPEC-0003 §5)
KIND = {"key-publish": 1, "self": 2, "speaks": 3, "attestation": 4, "trust": 5,
        "revoke": 6, "rotate": 7, "define": 8, "review": 9, "approve": 10, "aggregate": 11}
SUITE_ED25519 = 1
T_KEY, T_DIGEST, T_STATEMENT, T_DEFINITION = 1, 2, 3, 4
SHA256 = 1

def statement(kind, says, this, body, valid):
    s = {1: KIND[kind], 2: SUITE_ED25519, 3: kid(says), 6: body}
    if this is not None: s[4] = this
    if valid: s[5] = valid
    return s

def sign(signer, tbs: bytes) -> bytes:
    return K[signer][0].sign(DS + tbs)

def envelope(says_kid, tbs, sig, suite=SUITE_ED25519, pub=None):
    """SPEC-0002 §5: [suite, says, tbs, sig, ? pub]. `pub` is an unauthenticated
    hint so that verify-before-decode works even for key-publish."""
    return enc([suite, says_kid, tbs, sig] + ([pub] if pub is not None else []))

# ---------------------------------------------------------------- definition DV-1 (SPEC-0003)
DV1 = {
    1: kid("alice"), 2: "supply-chain", 3: "1",
    5: [
        [1, {1: "build-provenance", 2: 1,
             3: {"en": "Build provenance", "es": "Procedencia de la compilación"},
             4: {"en": "How the artifact was built.", "es": "Cómo se compiló el artefacto."},
             6: [{1: "reproducible", 2: {"en": "Reproducible", "es": "Reproducible"},
                  3: {"en": "built reproducibly from published sources",
                      "es": "compilado de forma reproducible desde fuentes publicadas"}},
                 {1: "attested", 2: {"en": "Attested"},
                  3: {"en": "built by an attested pipeline"}},
                 {1: "unverified", 2: {"en": "Unverified"},
                  3: {"en": "origin not verified"}}],
             8: 2,
             9: [{1: "provenance", 2: {"en": "Does the provenance name the expected builder?"}}]}],
        [1, {1: "outcome", 2: 1,
             3: {"en": "Review outcome"},
             4: {"en": "What a reviewer concluded."},
             6: [{1: "approve", 2: {"en": "Approve"}, 3: {"en": "ready to publish as built"}},
                 {1: "changes", 2: {"en": "Request changes"}, 3: {"en": "not ready; changes needed"}},
                 {1: "reject", 2: {"en": "Reject"}, 3: {"en": "must not be published"}}],
             8: 0}],
        [2, {1: "release-attestation", 2: 4,
             3: {1: [T_DIGEST]},
             4: [{1: {2: "build-provenance"}, 2: True}],
             5: 2592000,
             8: {"en": "{says} attests that {this} was {build-provenance}.",
                 "es": "{says} atestigua que {this} fue {build-provenance}."},
             9: {"en": "Release attestation"}}],
    ],
}
DV1_BYTES = enc(DV1)
DV1_ID = hashlib.sha256(DV1_BYTES).digest()
tref = lambda label: {1: DV1_ID, 2: label}

ARTIFACT = hashlib.sha256(b"ksa example artifact\n").digest()

# ---------------------------------------------------------------- positive vectors
V = {}
def add(name, signer, stmt, note, carry_pub=False):
    tbs = enc(stmt)
    sig = sign(signer, tbs)
    V[name] = {"note": note, "signer": signer, "tbs": tbs, "sig": sig,
               "envelope": envelope(kid(signer), tbs, sig, pub=K[signer][1] if carry_pub else None),
               "digest": hashlib.sha256(tbs).digest(), "expect": "accept"}
    return V[name]

add("TV-1", "alice", statement("key-publish", "alice", [T_KEY, kid("alice")],
    {1: {1: 1, 2: K["alice"][1]}},
    {1: t("2026-10-05T00:00:00Z"), 3: t("2026-10-05T16:00:00Z")}),
    "key-publish: Alice publishes her Ed25519 key; this = says = SHA-256(pub); the envelope carries pub", carry_pub=True)
add("TV-2", "alice", statement("self", "alice", [T_KEY, kid("alice")],
    {2: "Alice", 3: [1], 5: 1},
    {1: t("2026-10-05T00:00:00Z"), 3: t("2026-10-05T16:00:00Z")}),
    "self: label Alice, uses [statements], controller person (a self-claim)")
add("TV-3", "alice", statement("define", "alice", [T_DEFINITION, DV1_ID],
    {1: "supply-chain", 2: "1"},
    {1: t("2026-10-06T00:00:00Z"), 3: t("2026-10-06T09:00:00Z")}),
    "define: Alice publishes definition DV-1 by its DefinitionId")
tv4 = add("TV-4", "alice", statement("attestation", "alice", [T_DIGEST, SHA256, ARTIFACT],
    {1: [{1: tref("build-provenance"), 2: "reproducible"}]},
    {1: t("2026-10-06T00:00:00Z"), 2: t("2026-11-01T00:00:00Z"), 3: t("2026-10-06T10:30:00Z")}),
    "attestation about an ARTIFACT digest (not a key): build-provenance = reproducible")
add("TV-5", "carol", statement("trust", "carol", [T_KEY, kid("alice")],
    {1: [{1: tref("build-provenance"), 3: ["reproducible", "attested"]}],
     2: {1: 1, 2: [{1: tref("build-provenance"), 3: ["reproducible"]}],
         5: t("2026-12-01T00:00:00Z")}},
    {1: t("2026-10-06T00:00:00Z"), 3: t("2026-10-06T11:00:00Z")}),
    "trust: Carol trusts Alice about build-provenance in {reproducible, attested}; may delegate depth 1 within {reproducible}")
add("TV-6", "bob", statement("review", "bob", [T_STATEMENT, tv4["digest"]],
    {1: [{1: tref("outcome"), 2: "approve"}], 2: "provenance names the expected builder"},
    {1: t("2026-10-06T12:00:00Z"), 2: t("2026-10-20T00:00:00Z"), 3: t("2026-10-06T12:00:00Z")}),
    "review: Bob reviews statement TV-4 (target is a statement digest): outcome approve")
add("TV-7", "alice", statement("revoke", "alice", [T_KEY, kid("alice")],
    {1: tv4["digest"]},
    {1: t("2026-10-21T00:00:00Z"), 3: t("2026-10-20T08:00:00Z")}),
    "revoke: Alice revokes TV-4 by digest, effective 2026-10-21")
add("TV-8", "bob", statement("rotate", "bob", [T_KEY, kid("bob2")],
    {1: "laptop reinstall"},
    {1: t("2026-10-20T00:00:00Z"), 3: t("2026-10-19T18:00:00Z")}),
    "rotate: Bob's old key names its successor; valid.issued orders statements around the rotation")

# ---------------------------------------------------------------- negative vectors
N = {}
def bad(name, env, why, step):
    N[name] = {"envelope": env, "expect": "reject", "why": why, "step": step}

# N-1: non-canonical TBS (map keys out of order), correctly signed over those bytes
good = V["TV-4"]
noncanon = bytearray(good["tbs"])
# re-encode the same statement with keys 6 and 4 swapped in position: hand-built, deliberately non-deterministic
s4 = statement("attestation", "alice", [T_DIGEST, SHA256, ARTIFACT],
               {1: [{1: tref("build-provenance"), 2: "reproducible"}]},
               {1: t("2026-10-06T00:00:00Z"), 2: t("2026-11-01T00:00:00Z"), 3: t("2026-10-06T10:30:00Z")})
items = [(1, s4[1]), (2, s4[2]), (3, s4[3]), (6, s4[6]), (4, s4[4]), (5, s4[5])]   # 6 before 4: not sorted
nc = bytes([0xa0 | len(items)]) + b"".join(ksa_cbor(k) + ksa_cbor(v) for k, v in items)
bad("N-1", envelope(kid("alice"), nc, sign("alice", nc)),
    "TBS map keys are not in deterministic order; the signature over those bytes is valid", "V5 canonical decode")
# N-2: one byte of TBS changed after signing
t2 = bytearray(good["tbs"]); t2[-1] ^= 0x01
bad("N-2", envelope(kid("alice"), bytes(t2), good["sig"]), "TBS altered after signing", "V4 signature")
# N-3: outer says names Bob and Bob signs, but the inner says is Alice
bad("N-3", envelope(kid("bob"), good["tbs"], sign("bob", good["tbs"])),
    "outer says (Bob) does not equal inner says (Alice)", "V6 outer/inner agreement")
# N-4: key-publish of a small-order public key (the identity point)
ident = bytes([1]) + bytes(31)
s = {1: KIND["key-publish"], 2: 1, 3: hashlib.sha256(ident).digest(),
     4: [T_KEY, hashlib.sha256(ident).digest()], 6: {1: {1: 1, 2: ident}}}
tb = enc(s)
bad("N-4", envelope(hashlib.sha256(ident).digest(), tb, bytes(64), pub=ident),
    "public key is a small-order point (the identity); MUST be rejected before any verification", "V3 strict key check")
# N-5: S + L — a malleated signature that a lax verifier accepts
sig = good["sig"]; S = int.from_bytes(sig[32:], "little") + L
bad("N-5", envelope(kid("alice"), good["tbs"], sig[:32] + S.to_bytes(32, "little")),
    "signature S >= L (malleated); MUST be rejected even though R and the equation may verify", "V4 strict signature")
# N-6: a float in the TBS
fl = good["tbs"][:-1] + b""   # placeholder replaced below
s6 = dict(s4); s6[6] = {1: [{1: tref("build-provenance"), 2: 1.5}]}
fb = cbor2.dumps(s6, canonical=True)
bad("N-6", envelope(kid("alice"), fb, sign("alice", fb)),
    "TBS contains a floating-point value; outside the KSA data model", "V5 canonical decode")

# ---------------------------------------------------------------- output
hx = lambda b: b.hex()
out = {
    "ds_label": hx(DS),
    "time_epoch": "2026-01-01T00:00:00Z",
    "keys": {n: {"seed": SEEDS[n], "pub": hx(K[n][1]), "kid": hx(K[n][2])} for n in K},
    "definitions": {"DV-1": {"body": hx(DV1_BYTES), "id": hx(DV1_ID)}},
    "artifact_sha256": hx(ARTIFACT),
    "positive": {n: {"note": v["note"], "signer": v["signer"], "tbs": hx(v["tbs"]), "sig": hx(v["sig"]),
                     "envelope": hx(v["envelope"]), "digest": hx(v["digest"]), "expect": "accept"} for n, v in V.items()},
    "negative": {n: {"why": v["why"], "step": v["step"], "envelope": hx(v["envelope"]), "expect": "reject"} for n, v in N.items()},
}
(HERE / "vectors.json").write_text(json.dumps(out, indent=2) + "\n")

md = ["<!-- generated by spec/vectors/ksa-core/generate.py — do not edit by hand -->", ""]
md += ["### Keys", "", "| name | seed | public key | kid = SHA-256(pub) |", "|---|---|---|---|"]
md += [f"| {n} | `{SEEDS[n]}` | `{hx(K[n][1])}` | `{hx(K[n][2])}` |" for n in K]
md += ["", f"Domain-separation label (hex): `{hx(DS)}`", "",
       "### DV-1 — definition `supply-chain` v1, definer Alice", "",
       f"DefinitionId = SHA-256(body) = `{hx(DV1_ID)}`", "", "```", hx(DV1_BYTES), "```", ""]
for n, v in V.items():
    md += [f"### {n} — {v['note']}", "", f"- signer: {v['signer']}",
           f"- statement digest = SHA-256(TBS): `{hx(v['digest'])}`", "- TBS:", "```", hx(v["tbs"]), "```",
           "- signature over DS ‖ TBS:", "```", hx(v["sig"]), "```",
           "- envelope `[suite, says, tbs, sig, ? pub]`:", "```", hx(v["envelope"]), "```", "- expected: **accept**", ""]
md += ["### Negative vectors", ""]
for n, v in N.items():
    md += [f"#### {n} — reject at {v['step']}", "", v["why"] + ".", "```", hx(v["envelope"]), "```", ""]
(HERE / "vectors.md").write_text("\n".join(md) + "\n")
print(f"{len(V)} positive, {len(N)} negative; DV-1 id {hx(DV1_ID)[:16]}…; encoders agree on all positive vectors")
