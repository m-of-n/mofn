#!/usr/bin/env python3
"""Four use cases, one statement form. SPIKE - evaluates representation.

Run:  python3 prototype/statements/demo.py
"""
import sys, pathlib, hashlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from rcbor import encode, diagnostic
from statement import (statement, ptype, keyid, sign, verify,
                       by_digest, by_locator, by_description)
from labeltype import label_type, domain, domain_id, render, in_range

PAUL, DAVID, TOOL = b"paul-pubkey", b"david-pubkey", b"buildtool-pubkey"
SEC = b"not-a-real-key"
NOW = 1758585600


def rule(t):
    print(f"\n{'─' * 66}\n{t}\n{'─' * 66}")


# ── the domain of discourse: PICS-like label types ────────────────────────
rule("1. A domain of discourse — types carry their own meaning (P3, P4)")

build_prov = label_type(
    "build-provenance", repr_="tstr", ordered=True,
    constraints={"requires": "source-uri"},
    values={
        "reproducible": {"en": "built reproducibly from published sources",
                         "es": "compilado de forma reproducible desde fuentes publicadas"},
        "attested":     {"en": "built by an attested pipeline",
                         "es": "compilado por una tubería atestiguada"},
        "unverified":   {"en": "origin not verified", "es": "origen no verificado"}})

review = label_type(
    "human-review", repr_="tstr", ordered=True,
    values={"reviewed":   {"en": "reviewed by a second person"},
            "unreviewed": {"en": "not reviewed by anyone but its author"}})

DOM = domain(keyid(PAUL), "m-of-n/supply-chain", [build_prov, review], "v1")
DID = domain_id(DOM)
print(f"  domain           m-of-n/supply-chain v1")
print(f"  hash-identified  {DID.hex()}")
print(f"  types            {[t['l'] for t in DOM['t']]}")
print(f"  bytes            {len(encode(DOM))}")
print("\n  The hash covers the SET. Change one rendering string and the whole")
print("  domain gets a new id - which is the point: a consumer citing this id")
print("  has exactly the meanings the author published, not an approximation.")

# ── use case 1: attestation ───────────────────────────────────────────────
rule("2. Attestation — A says B has C")

artifact = hashlib.sha256(b"<the built binary>").digest()[:16]
s1 = statement(TOOL, by_digest(artifact), ptype(PAUL, "build-provenance"),
               "reproducible", at=NOW)
env1 = sign(s1, SEC)
print(f"  {len(env1['payload'])} bytes signed")
print(f"  renders as: \"{render(DOM, 'build-provenance', s1['c'])}\"")
print(f"  in Spanish: \"{render(DOM, 'build-provenance', s1['c'], 'es')}\"")
print("\n  The verifier wrote no type-specific code. It resolved the domain and")
print("  read the rendering out of the type. THAT is P3 earning its place.")

# ── use case 2: naming ────────────────────────────────────────────────────
rule("3. Naming — P6: a name is just a type of attested string")

s2 = statement(PAUL, by_digest(keyid(DAVID)), ptype(PAUL, "name"), "david", at=NOW)
print(f"  {len(encode(s2))} bytes — the SAME form as the attestation above")
print("  no NameCert type, no second encoder, no second signing path")
print("\n  This is what resolves register item 6a: the five 'kinds' in")
print("  ARCH-0001 §4.2 are FUNCTIONS over one form, discriminated by")
print("  predicate type. The three PROCEDURES in §4.3 stay separate.")

# ── use case 3: delegation ────────────────────────────────────────────────
rule("4. Delegation — A says B can speak about (Domain, Topic)")

s3 = statement(PAUL, by_digest(keyid(DAVID)), ptype(PAUL, "may-speak"),
               {"dom": DID, "topic": "build-provenance"}, at=NOW)
print(f"  paul delegates to david, scoped to domain {DID.hex()[:12]}…")
print(f"  topic: build-provenance")
print("\n  Authority is scoped SEMANTICALLY. The domain of discourse is not")
print("  only the unit of meaning (P4) — it is the unit of authority scope.")
print("  One construct, so a chain narrows reach and authority together.")

# ── use case 4: a subject you cannot hash ─────────────────────────────────
rule("5. Arbitrary subjects — R-M-11 description mode")

book = {"title": "SPKI Certificate Theory", "isbn": "", "year": 1999}
s4 = statement(PAUL, by_description(book), ptype(PAUL, "human-review"),
               "unreviewed", at=NOW)
print(f"  subject is a described thing, id = digest of its canonical form")
print(f"  id: {s4['b']['v'].hex()}")
print(f"  renders as: \"{render(DOM, 'human-review', s4['c'])}\"")

# ── verification behaviour ────────────────────────────────────────────────
rule("6. Verify the bytes, then decode — R-O-05")

print(f"  signature valid:          {verify(env1, SEC)}")
tampered = dict(env1, payload=env1["payload"][:-1] + bytes([env1["payload"][-1] ^ 1]))
print(f"  one bit flipped:          {verify(tampered, SEC)}")
print("\n  The verifier never canonicalised anything to check this. It verified")
print("  the bytes it received. Canonicalisation happened once, at authoring.")

try:
    render(DOM, "build-provenance", "definitely-fine")
except KeyError as e:
    print(f"\n  value outside the type:   rejected — {e}")

# ── determinism ───────────────────────────────────────────────────────────
rule("7. Determinism is a property of the encoder, not a unique encoding")

reordered = {k: s1[k] for k in reversed(list(s1))}
print(f"  same statement, keys reversed → identical bytes: {encode(s1) == encode(reordered)}")
print("\n  Sponsor, 2026-09-22: 'deterministic does not mean just one way'.")
print("  This encoder is deterministic. Another could be too. What matters is")
print("  that the signed bytes are deterministic AND the encoding is named in")
print("  the envelope — 'typ' above — so a verifier never guesses.")

rule("What this spike does NOT settle")
print("""  - DEC-002 is open. This is one candidate, not a decision.
  - The signature is a stand-in. No generated primitives (CLAUDE.md).
  - No reduction algorithm: delegation is REPRESENTED, not yet composed.
  - No revocation, no validity windows, no threshold subjects.
  - Whether 'may-speak' is the right delegation predicate is untested.""")
