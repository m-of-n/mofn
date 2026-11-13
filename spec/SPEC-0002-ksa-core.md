---
schema: "archdoc/v1"
id: SPEC-0002
title: "KSA Core — statements, data model, canonical encoding and cipher suites"
short_title: "KSA Core"
description: "The KSA statement: its data model, deterministic encoding, signed envelope, cipher suites, statement kinds, and the procedure for verifying one statement."
type: specification
category: security
status: draft
version: "0.9.0"
version_policy: "semver; MAJOR = any change to signed or hashed bytes; MINOR = additive registry entries or requirements; PATCH = editorial"
date: "2026-10-14"
updated: "2026-11-12"
decision_makers:
  - role: sponsor
    id: paul-lambert
  - role: student
    id: ndewedo-newbury
    authority: >
      Delegated by the sponsor on a Zoom call in October 2026 (date not
      recorded): ndewedo-newbury may decide any question in this project, on the same
      footing as the sponsor, and is accountable for what they decide.
      Relayed by david-hsiao on 2026-11-03; no written confirmation from the
      sponsor is recorded (DL-0021). Supersedes the 2026-10-25 delegation and
      its exclusion of ADR-0002. Acceptance still follows ARCH-0001 §9: a
      DEC-* is accepted only by an ADR.
  - role: student
    id: david-hsiao
    authority: >
      Delegated by the sponsor on a Zoom call in October 2026 (date not
      recorded): david-hsiao may decide any question in this project, on the same
      footing as the sponsor, and is accountable for what they decide.
      Relayed by david-hsiao on 2026-11-03; no written confirmation from the
      sponsor is recorded (DL-0021). Supersedes the 2026-10-25 delegation and
      its exclusion of ADR-0002. Acceptance still follows ARCH-0001 §9: a
      DEC-* is accepted only by an ADR.
reviewers: []
needs_review: true
reviewed: false
canonical_path: spec/SPEC-0002-ksa-core.md
companion:
  - spec/SPEC-0001-ksa-architecture.md
  - spec/SPEC-0003-ksa-definitions.md
  - spec/SPEC-0004-ksa-trust-evaluation.md
  - spec/ADR-0003-ksa-core-decisions.md
defers_to: ARCH-0001
related_rfcs: [RFC2119, RFC8174, RFC8032, RFC8610, RFC8949]
---

# KSA Core — statements, data model, canonical encoding and cipher suites

**Specification SPEC-0002 · version 0.9.0 · draft**

## Abstract

This document specifies the **KSA statement**: a signed assertion by one key
about one target. It defines the data model every statement is built from, a
single deterministic binary encoding, the envelope that carries a statement with
its signature, the cipher suites that fix the exact bytes signed, the registered
statement kinds, and the procedure a verifier follows to establish that one
statement is well-formed and was signed by the key it names. Whether a verified
statement should be *believed* is out of scope here; that is trust evaluation
(SPEC-0004).

## Status of this document

Draft for review in the m-of-n project. Design decisions are recorded in
ADR-0003, ADR-0004 (the encoding, DEC-002) and ADR-0005 (`kid`, DEC-003).
**0.2.0 (2026-10-25):** §6.1's digest row no longer covers `kid`s, which are
SHA-256 under every suite; §12.3 gains the key-encoding collision rule. No
signed or hashed bytes change. **0.3.0 (2026-11-01):** Appendix A gains the
threshold form (TV-9…11, N-7…10), a name binding (TV-12, TV-13, DV-2) and key
`dave`; every existing vector is byte-identical.
**0.4.0 (2026-11-01):** proposed by DL-0020 from what building W-1 (mofn#65)
found. §6.3 rejects a key outside the prime-order subgroup. §11.3 says which
YAML the human form is, how a target is spelled, and that text reading as bytes
has no human form; §11.1 notes that exception. No signed or hashed bytes
change, and every published vector keeps its result.
**0.4.1 (2026-11-03):** process. `ndewedo-newbury` is added to
`decision_makers`, at their instruction, and accepts 0.4.0 the same day
(DL-0020); nothing normative changes.
**0.5.0 (2026-11-03):** §6.1 says when a suite becomes immutable: once this
specification leaves `0.x`. Until then a suite's entry may be revised, as suite
1's verification rules were in 0.4.0. `decision_makers` records the sponsor's
October delegation (DL-0021). No signed or hashed bytes change.
**0.6.0 (2026-11-07):** target type 5, the locator, is **withdrawn** (§7.2;
mofn#144, DL-0030). A locator alone binds no digest, and ARCH-0001 R-M-07 and
R-M-11 require one. A statement whose target is `[5, …]` is now invalid at V7
(N-11). A locator for a subject is carried as an attribute (§7.2). No signed or
hashed bytes change and every published vector keeps its result, but a
statement that verified under 0.5.0 can now fail: this is permitted only
because the document is `0.x`.
**0.7.0 (2026-11-08):** Appendix A gains delegation vectors TV-14…20 and the
expected SPEC-0004 answers E-1…E-4 over them (mofn#136, DL-0031); every
existing vector is byte-identical.
**0.8.0 (2026-11-09):** Appendix A gains DV-3 `library-review` and TV-21…26,
the archives target of ARCH-0001 §2.3.2 (mofn#135, DL-0032): a description
target (TV-26) with a locator carried as an attribute, and evaluations
E-5…E-7. Every existing vector is byte-identical.
**0.9.0 (2026-11-12):** SDSI names (mofn#143, DL-0039, ADR-0008). §7.2
registers target type 7, the **name** `[7, kid, [+ label]]`: the issuer's
first label's second label, and so on (ARCH-0001 §3.1). It may be the `this` of
an `attestation`, which then binds a name to a name, and of a `trust`, which
then trusts whatever keys the name resolves to (§8.6). SPEC-0004 §5.3 says how a
name resolves. Appendix A gains DV-4 `naming`, TV-27…34, N-12 and N-13. Every
existing vector is byte-identical and keeps its result. Additive, so MINOR.
Nothing in this draft is final until its version leaves `0.x`.

---

## Table of contents

1. Introduction · 2. Conventions and terminology · 3. Overview · 4. Data model
and canonical encoding · 5. The signed statement envelope · 6. Cipher suites ·
7. Statement structure · 8. Statement kinds · 9. Verifying one statement ·
10. Key store · 11. Human-review form · 12. Registries · 13. Security
considerations · 14. Privacy considerations · 15. References ·
Appendix A. Test vectors · Appendix B. CDDL

---

## 1. Introduction

KSA (Key-centric Semantic Attestations) is a protocol of **statements**: signed
messages in which a key says something about a target. Every exchange that
asserts or transfers trust — publishing a key, making a claim about an artifact,
delegating authority, reviewing, revoking — is a statement with one shared
structure.

This document fixes three things exactly, because everything else depends on
them:

- **the bytes that are signed**, so that any two conforming implementations
  produce and verify identical signatures;
- **the bytes that are hashed**, so that statements and definitions can be
  referenced by digest without ambiguity;
- **the order of verification**: a signature is checked over the bytes as
  received, before those bytes are decoded.

The meaning of the values inside a statement — what a type is, which values it
permits, how it renders for a person — is defined by **definitions** (SPEC-0003).
How statements combine into a decision is **trust evaluation** (SPEC-0004).

## 2. Conventions and terminology

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when,
and only when, they appear in all capitals, as shown here.

| term | meaning |
|---|---|
| **key** | a public key under a cipher suite: an opaque octet string whose layout the suite fixes |
| **kid** | key identifier: the 32-octet SHA-256 digest of the key's encoding (§4.5) |
| **persona** | a principal identified by a key (SPEC-0001 §3). On the wire a persona appears only as kids |
| **statement** | the signed object of §7: a kind, a suite, a speaker (`says`), a target (`this`), a validity window and a kind-specific body |
| **TBS** | "to be signed": the canonical encoding (§4) of a statement |
| **envelope** | the array that carries a TBS with its signature (§5) |
| **statement digest** | SHA-256 of the TBS (§6.3); how one statement refers to another |
| **definition** | a hash-identified document that defines types, templates and processes (SPEC-0003) |
| **DefinitionId** | SHA-256 of a definition body's canonical encoding (SPEC-0003 §4) |
| **verifier** | an implementation that performs the procedure of §9 |

Byte strings are written as lowercase hexadecimal. `‖` denotes concatenation.

## 3. Overview

```
            ┌────────────────────── envelope (§5) ───────────────────────┐
            │ suite │ says (kid) │ TBS (bytes, exactly as signed) │ sig │ ? pub │
            └────────────────────────────┬───────────────────────────────┘
                                         │ decoded only after the signature verifies
                                         ▼
                 statement (§7):  kind · suite · says · this · valid · body
```

A producer builds a statement, encodes it canonically (§4) to obtain the TBS,
signs `DS ‖ TBS` under its suite (§6), and transmits the envelope. A verifier
reads the envelope, resolves the key named by `says`, **verifies the signature
over the received TBS**, and only then decodes the TBS with a validating decoder
and checks its structure (§9).

Three properties follow:

1. **No canonicalisation during verification.** The verifier never re-encodes.
   It checks that the received bytes are already canonical (§4.3); if they are
   not, the statement is rejected — never repaired.
2. **Domain separation.** Every signature covers a label naming what is being
   signed (§6.4), so a signature over a statement cannot be presented as a
   signature over anything else.
3. **Content addressing.** A statement is referred to by the SHA-256 of its TBS;
   a definition by the SHA-256 of its body. Both are stable across transports.

## 4. Data model and canonical encoding

### 4.1 Data model

Every TBS and every definition body MUST consist only of the following values.

| type | rule |
|---|---|
| **integer** | in the range −(2^53 − 1) … 2^53 − 1 inclusive |
| **byte string** | any length, subject to §13.6 |
| **text string** | valid UTF-8. Preserved byte-exact; MUST NOT be normalised (no Unicode normalisation, no case folding, no whitespace trimming) by any producer or verifier |
| **boolean** | true or false |
| **array** | ordered; order is significant and signed |
| **map** | keys are unsigned integers in protocol structures (§7, SPEC-0003 §5) and text strings inside values and language maps; no duplicate keys |

The following MUST NOT appear anywhere in a TBS or definition body: floating-point
numbers, `null`, `undefined`, any other simple value, CBOR tags (major type 6),
and indefinite-length items.

### 4.2 Deterministic encoding

A TBS or definition body MUST be encoded as CBOR [RFC8949] satisfying the core
deterministic encoding requirements of [RFC8949] §4.2.1, restricted to the data
model of §4.1:

1. every integer, length and count uses the shortest possible head (preferred
   serialization);
2. every array, map, byte string and text string has a definite length;
3. the keys of every map are sorted in bytewise lexicographic order of their
   deterministic encodings;
4. no tags, no floating-point values, and no simple values other than `true`
   (0xf5) and `false` (0xf4).

This is the encoding called **KSA-CBOR** in this specification and in
SPEC-0003. It is the single canonical encoding for every signed or hashed object
(ADR-0003 D2).

### 4.3 Validating decoder

A verifier MUST decode a TBS (and a definition body, SPEC-0003 §4) with a
decoder that **rejects** any input that is not exactly the KSA-CBOR encoding of
some value in the data model. In particular it MUST reject:

- a head longer than necessary (e.g. `0x1817` for the integer 23);
- an indefinite-length item;
- map keys not in sorted order, or a duplicated key;
- a tag, a floating-point value, `null`, `undefined`, or any simple value other
  than `true` and `false`;
- an integer outside the range of §4.1;
- a text string that is not valid UTF-8;
- bytes remaining after the top-level item.

Rejection MUST NOT be replaced by repair: a decoder MUST NOT re-sort, re-encode
or otherwise normalise and then accept. Every check above can be made in a
single forward pass without re-encoding (mofn#78).

### 4.4 Time

A time is an integer `T` derived from `s`, the number of seconds since
2026-01-01T00:00:00Z (negative before it):

- if `s mod 86400 = 0`: `T = 2·(s / 86400) + 1` (odd: the day form);
- otherwise: `T = 2·s` (even: the seconds form).

To decode: an odd `T` gives `s = ((T − 1) / 2) · 86400`; an even `T` gives
`s = T / 2`. An even `T` whose `s` is a multiple of 86400 MUST be rejected, so
every instant has exactly one encoding. Leap seconds are not represented.

In the human-review form (§11) a time is written exactly as
`YYYY-MM-DDTHH:MM:SSZ`: upper-case `T` and `Z`, no fraction, no offset, seconds
`00`–`59`. Any other spelling MUST be rejected, not normalised.

### 4.5 Identifiers

| identifier | definition | size |
|---|---|---|
| **kid** | SHA-256 of the key's public-key encoding under its suite (§6) | 32 octets |
| **statement digest** | SHA-256 of the statement's TBS, under the statement's own suite | 32 octets |
| **DefinitionId** | SHA-256 of the definition body's KSA-CBOR encoding (SPEC-0003 §4) | 32 octets |

Identifiers MUST appear in full in every TBS and every definition body.
A transport MAY abbreviate them on the wire, provided the receiver reconstructs
the full TBS before verification (§13.7).

## 5. The signed statement envelope

A statement is transmitted as a **signed statement**: a KSA-CBOR array of four or
five elements.

```
signed-statement = [ suite, says, tbs, sig, ? pub ]
```

| # | element | type | authenticated? |
|---|---|---|---|
| 0 | `suite` | unsigned integer | no — a hint; checked against the TBS in step V6 |
| 1 | `says` | kid (32-octet byte string) | no — a hint; checked against the TBS in step V6 |
| 2 | `tbs` | byte string: the TBS exactly as signed | yes |
| 3 | `sig` | byte string: the signature over `DS ‖ tbs` (§6) | — |
| 4 | `pub` | byte string: the speaker's public-key encoding | no — OPTIONAL; checked against `says` in V3 |

The envelope exists so that a verifier can **verify before it decodes**.
`suite` and `says` tell it which key and which algorithm to use; `tbs` is
verified as received; only then is it decoded. `pub` lets a verifier check a
statement from a key it does not yet hold — REQUIRED for the bootstrap kinds
(`key-publish`, and `self` when it carries a key), OPTIONAL otherwise.

A producer MUST place the canonical TBS in `tbs` and MUST set `suite` and `says`
to the values inside it. An envelope is not itself hashed or signed; the
statement digest is computed over `tbs` only.

> **Why carry the signed bytes, rather than signing a re-encoded statement?**
> Because otherwise a verifier would have to decode, remove the signature, and
> re-encode before it could check it — canonicalising during verification, exposing
> its decoder to unauthenticated input, and creating a second encoder whose
> output must match the producer's byte for byte. Carrying the signed bytes
> intact removes all three (ARCH-0001 R-O-05).

## 6. Cipher suites

### 6.1 What a suite defines

A cipher suite is a registry entry (§12.3), and it is immutable once this
specification leaves `0.x`. Until then an entry MAY be revised, and each
revision is recorded in this document's status section; 0.4.0 revised suite 1's
verification rules (§6.3). Each entry MUST define:

| item | meaning |
|---|---|
| suite code | an unsigned integer; never reused |
| name | a stable text name |
| key algorithm | the signature algorithm and its parameters |
| public-key encoding | the exact octets of a public key — the input to `kid` |
| signature input | the exact octets signed: `DS ‖ TBS`, with its DS label (§6.4) |
| signature encoding | the exact octets of `sig` |
| verification rules | including any strictness beyond the base algorithm |
| digest | the hash used for statement digests. `kid`s are SHA-256 under every suite (§4.5, ADR-0005) |

A statement's suite is inside its TBS and is therefore covered by its signature.
A verifier MUST report a statement under an unregistered or unsupported suite as
**unverifiable** (§9), which is distinct from invalid.

### 6.2 Suite codes

| code | name | status |
|---|---|---|
| 0 | — | reserved; never valid |
| 1 | `ksa-ed25519-sha256` | **default** (§6.3) |
| 2 | `ksa-p256-sha256` | reserved; not yet specified |
| 3–7 | — | reserved: classical suites |
| 8 | `ksa-mldsa65-sha256` | provisional (§6.5) |
| 9–15 | — | reserved: post-quantum and hybrid suites |
| 16–255 | — | Specification Required (§12) |
| 256–65535 | — | experimental and private use; MUST NOT be used outside a closed deployment |

### 6.3 Suite 1 — `ksa-ed25519-sha256`

- **Key algorithm:** Ed25519, PureEdDSA [RFC8032].
- **Public-key encoding:** the 32-octet encoding of [RFC8032] §5.1.2.
  `kid = SHA-256(public key)`.
- **Signature input:** `DS ‖ TBS`, where `DS` is the label `KSA-STMT-SIG-v1`
  followed by one zero octet (16 octets; hex `4b53412d53544d542d5349472d763100`).
  The TBS octets are signed directly, not a digest of them.
- **Signature encoding:** the 64-octet `R ‖ S` of [RFC8032] §5.1.6.
- **Statement digest:** SHA-256(TBS), without `DS`.
- **Strict key rules.** A verifier MUST reject a public key — when it is
  ingested (§10) and again before any verification under it — if its encoding is
  non-canonical (the encoded y ≥ p, with p = 2^255 − 19, or x = 0 with the sign
  bit set), if it does not decode to a curve point, or if it decodes to a point
  of small order (\[8\]A is the identity; this covers all eight points of the
  torsion subgroup, including the identity), or if it lies outside the
  prime-order subgroup (\[L\]A is not the identity, as for an honest key with a
  torsion point added). An honestly generated key always passes. The last rule
  keeps verifiers in agreement: under such a key the equation of [RFC8032]
  §5.1.7 holds for about one message in eight at order 8, and a library's verify
  function accepts those (DL-0020).
- **Strict signature rules.** A verifier MUST reject a signature if
  S ≥ L, where L = 2^252 + 27742317777372353535851937790883648493; if R is
  non-canonical or not on the curve; or if R is of small order. Only then does it
  evaluate the verification equation of [RFC8032] §5.1.7. A library verify
  function that accepts small-order keys or S ≥ L MUST NOT be relied on alone;
  implementations SHOULD use one documented to enforce these rules.

### 6.4 Domain-separation labels

A DS label is a fixed ASCII string followed by one zero octet. It is prepended
to the bytes being signed and is never transmitted.

| label | signs |
|---|---|
| `KSA-STMT-SIG-v1\0` | a KSA statement, in every suite that prepends a label |
| `KSA-POP-SIG-v1\0` | a proof of possession over a presentation (SPEC-0001 §8) |
| `KSA-<OBJECT>-SIG-v<n>\0` | any future signed object; each MUST register its own label, and reusing another's is forbidden |

For suites whose algorithm has a context parameter (ML-DSA), the label without
its zero octet is passed as that context, and is not prepended (§6.5).

### 6.5 Suite 8 — `ksa-mldsa65-sha256` (provisional)

- **Key algorithm:** ML-DSA-65 [FIPS204], pure (not HashML-DSA).
- **Public-key encoding:** the 1952-octet encoding of [FIPS204].
  `kid = SHA-256(public key)`.
- **Signature input:** the TBS, with context string `ctx = "KSA-STMT-SIG-v1"`
  (15 octets).
- **Signature encoding:** the 3309-octet signature of [FIPS204].
- **Statement digest:** SHA-256(TBS).

Provisional: no test vectors are published for it yet, and it MUST NOT be the
only suite a wallet offers until they are. It is specified now because a
statement verified decades after signing must survive the post-quantum
transition (ARCH survey R-001 §10).

## 7. Statement structure

### 7.1 Fields

A statement is a KSA-CBOR map with these keys. Absent optional fields MUST be
omitted; they MUST NOT be present with an empty or placeholder value.

| key | name | type | presence |
|---|---|---|---|
| 1 | `kind` | unsigned integer (§8) | REQUIRED |
| 2 | `suite` | unsigned integer (§6.2) | REQUIRED |
| 3 | `says` | kid — the speaker | REQUIRED |
| 4 | `this` | target (§7.2) | REQUIRED except as §8 allows |
| 5 | `valid` | validity (§7.3) | RECOMMENDED; REQUIRED for `rotate` and `revoke` |
| 6 | `body` | map — kind-specific (§8) | REQUIRED |

The statement map is **closed**: a key not listed above MUST cause rejection.
Every map inside a statement defined by this specification is closed in the same
way. KSA has no namespaced extension fields: **all extensibility is through
attributes whose types are defined in definitions** (§7.4; ADR-0003 D1), so an
unrecognised field is always an error.

### 7.2 Targets

`this` names what the statement is about. It is an array whose first element is
a target type.

| type | form | names |
|---|---|---|
| 1 key | `[1, kid]` | a key — a persona |
| 2 digest | `[2, digest-alg, bytes]` | an object identified by its digest; `digest-alg` 1 = SHA-256 (32 octets) |
| 3 statement | `[3, statement-digest]` | another statement |
| 4 definition | `[4, DefinitionId]` | a definition |
| 5 | — | **reserved, never assigned.** Was the locator, `[5, text]`; withdrawn in 0.6.0 |
| 6 description | `[6, type-ref, value]` | something identified by a typed description — the description's canonical encoding is its identity |
| 7 name | `[7, kid, [+ label]]` | a **name**: the issuer `kid`'s first label's second label, and so on — an SDSI compound name (ARCH-0001 §3.1, §4.1) |

Subjects are not limited to keys: a statement can concern a release, a record,
a definition, or another statement.

**A name** (type 7) names a principal **relative to a key**, never globally
(ARCH-0001 R-M-03). `[7, alice, ["fred", "sam"]]` is *Alice's fred's sam*: the
key that Alice calls `fred` calls `sam`. Each label matches
`[a-z][a-z0-9-]{0,62}`, the label grammar of SPEC-0003 §5.2, and a name has one
to 16 labels. Anything else MUST be rejected at V7 (N-12, N-13). A name is
interpreted only by resolution against name bindings at an evaluation time
(SPEC-0004 §5.3). It is not a key, and a verifier MUST NOT treat it as one:
single-statement verification (§9) never resolves a name.

**Every target binds a digest** (ARCH-0001 R-M-07, R-M-11). Types 1, 3 and 4
are digests; type 2 is a content digest; type 6 is identified by the canonical
encoding of its description; type 7 binds the issuer's `kid`, the namespace in
which its labels mean anything. A statement whose target is not one of the types
above MUST be rejected at V7 (§9.2).

**A locator is evidence, never a target.** A URI, URN, ISBN, serial number or
file path names a *place* or a *label*, not content: what it resolves to can
change while the name stays the same. Where a statement needs to say where its
subject can be found, it targets the subject by digest (type 2) or by
description (type 6) and carries the locator as an attribute whose type a
definition defines (§7.4). A relying party MUST NOT treat content fetched from
a locator as the subject unless that content matches the target (compare
SPEC-0003 §4.4).

### 7.3 Validity

```
valid = { ? 1 not-before: time, ? 2 not-on-or-after: time, ? 3 issued: time }
```

A statement is **valid at time t** if and only if `not-before ≤ t` when
`not-before` is present and `t < not-on-or-after` when `not-on-or-after` is
present. A missing bound is unbounded on that side.

`issued` is the speaker's statement of when it signed. It is REQUIRED for
`rotate` and `revoke`, and RECOMMENDED for every other kind, because rotation
semantics depend on it (SPEC-0004 §7). Whether a statement is valid at a given
time is evaluated by trust evaluation, not by single-statement verification (§9).

### 7.4 Attributes and type references

```
type-ref        = { 1 definition: DefinitionId, 2 label: text }
attribute       = { 1 type: type-ref, 2 value: value }
attribute-range = { 1 type: type-ref, ? 3 range: value }
```

A **type reference** names a type by the hash of the definition that defines it
and a label local to that definition. Inside a statement, `definition` is
REQUIRED. (Inside a definition it MAY be omitted to mean "this definition";
SPEC-0003 §5.2.)

An **attribute** assigns a value; an **attribute range** states a set of values —
the scope of a trust statement or of a delegation constraint. An attribute range
with no `range` means the unbounded range of its type. Whether a value is an
acceptable assignment, whether a range is well-formed, and whether one range is
within another are defined by the type's base kind (SPEC-0003 §6). Supplying a
range where an assignment is required, or the reverse, is a type error.

## 8. Statement kinds

### 8.1 Registry of kinds

| code | kind | `this` | purpose |
|---|---|---|---|
| 1 | `key-publish` | MUST be `[1, says]` | publish the speaker's public key |
| 2 | `self` | MUST be `[1, says]` | the speaker's public claims about itself |
| 3 | `speaks` | MUST be `[1, says]` | the definitions the speaker can produce and understand |
| 4 | `attestation` | any target | assign attributes to the target |
| 5 | `trust` | `[1, kid]` or `[7, …]`, or absent in the threshold form | extend trust to a key, or to the keys a name resolves to, about a range of attributes |
| 6 | `revoke` | MUST be `[1, says]` | withdraw one of the speaker's own statements |
| 7 | `rotate` | `[1, new-kid]`, not equal to `says` | name the speaker key's successor |
| 8 | `define` | MUST be `[4, DefinitionId]` | publish a definition, as its author |
| 9 | `review` | `[3, statement-digest]` or `[2, …]` | give an opinion on a statement or object |
| 10 | `approve` | `[3, statement-digest]` or `[2, …]` | authorise a statement or object |
| 11 | `aggregate` | any target except `[1, …]` and `[7, …]` | the result of a published process (SPEC-0005) |

A verifier MUST reject a statement whose kind is not registered.

### 8.2 `key-publish` (1)

```
body = { 1 key: public-key }
public-key = { 1 alg: key-alg, 2 pub: bytes }
```

`kid(body.key)` MUST equal `says`. The envelope MUST carry `pub`, and it MUST
equal `body.key.pub`. A verified `key-publish` is one of the two ways a key
enters a key store (§10).

### 8.3 `self` (2)

```
body = { ? 1 key: public-key, ? 2 label: text, ? 3 uses: [+ usage],
         ? 4 created: time, ? 5 controller: controller-kind }
```

The speaker's public self-description. `label` is a display string, not a
binding. `uses` lists usage codes (§12.7). `controller` states what kind of
entity controls the key (§12.8) — **a self-claim**, worth what a self-claim is
worth; SPEC-0004 §5 says how stronger evidence is weighed. If `key` is present
the rules of §8.2 apply to it. Private notes about a key (SPEC-0001 §5.4) are
never carried in a `self` statement.

### 8.4 `speaks` (3)

```
body = { 1 definitions: [+ DefinitionId] }
```

The speaker claims it can produce and understand statements using these
definitions. A relying party SHOULD check that an attester speaks a definition
before relying on its attestations under it; whether a missing `speaks` is a
warning or a failure is policy (SPEC-0004 §9).

### 8.5 `attestation` (4)

```
body = { 1 has: [+ attribute], ? 3 template: type-ref }
```

The speaker asserts that the target has each attribute. Each attribute's value
MUST be a valid assignment for its type (SPEC-0003 §6). `template`, when present,
names the template the statement was issued from (SPEC-0003 §7); a statement
that names a template MUST conform to it, and conformance is checked by trust
evaluation, where the definition is available.

### 8.6 `trust` (5)

```
body = { 1 about: [+ attribute-range],
         ? 2 may-delegate: delegation-constraints,
         ? 3 trusts: [2* kid], ? 4 threshold: uint }
delegation-constraints = { ? 1 depth: uint, ? 2 ranges: [+ attribute-range],
                           ? 3 allow-keys: [+ kid], ? 4 exclude-keys: [+ kid],
                           ? 5 not-on-or-after: time }
```

The speaker extends trust to a key about a range of attributes. Where `this` is
a name (§7.2), the trust is extended to each key the name resolves to at the
evaluation time (SPEC-0004 §5.3), as if a statement to that key had been made:
the speaker delegates the choice of key to the name's issuer. In the
**threshold form**, `this` is absent, `trusts` lists two or more keys, and
`threshold` is an integer `n` with 1 ≤ n ≤ the number of keys: the trust is
extended to any `n` of them acting together (SPEC-0004 §6.4). Otherwise `this`
MUST be present and `trusts` and `threshold` MUST be absent.

`about` MUST NOT be empty: unlimited trust is written as an attribute range with
no `range` for each type concerned. Without `may-delegate`, trust is **one hop**:
the trusted key may attest, but trust statements it issues are not followed.
With it, `depth` counts further hops; `ranges` is an allow-list that every
further delegation must fall within; `allow-keys` and `exclude-keys` constrain
who may be delegated to; `not-on-or-after` caps validity, and the earlier bound
wins. SPEC-0004 §6 is normative for how these are applied.

### 8.7 `revoke` (6)

```
body = { 1 revokes: statement-digest }
```

Withdraws the statement with that digest. **Only that statement's speaker may
revoke it** (ADR-0003 D5); a `revoke` naming a statement by another speaker has
no effect. Revocation takes effect at `valid.not-before`.

### 8.8 `rotate` (7)

```
body = { ? 1 note: text }
```

Signed by the old key (`says`), naming the new key (`this`). `valid.issued` is
REQUIRED. A `rotate` does not bind the new key's public key; the new key MUST be
published by its own `key-publish`. SPEC-0004 §7 defines how statements before
and after a rotation are evaluated.

### 8.9 `define` (8)

```
body = { 1 name: text, 2 version: text, ? 3 supersedes: DefinitionId }
```

Publishes the definition named by `this` as the speaker's. The speaker MUST
equal the definition body's `definer` (SPEC-0003 §4); a verifier holding the
definition MUST check this, and `name` and `version` MUST equal the body's.
`supersedes` names an earlier definition this one replaces; it is honoured only
if the earlier definition has the same definer (SPEC-0003 §8.3).

### 8.10 `review` (9) and `approve` (10)

```
review-body  = { 1 has: [+ attribute], ? 2 comment: text, ? 3 template: type-ref }
approve-body = { ? 1 has: [+ attribute], ? 2 comment: text, ? 3 template: type-ref }
```

A **review** is an opinion; its attributes (e.g. an outcome) are typed by a
definition. An **approval** is an authorization: it counts towards a requirement
only if its speaker is entitled to approve, which SPEC-0004 and SPEC-0005
determine. A review never satisfies an approval requirement.

### 8.11 `aggregate` (11)

```
body = { 1 process: process-ref, 2 inputs: [+ statement-digest], 3 result: bool }
process-ref = { 1 definition: DefinitionId, 2 label: text }
```

The outcome of evaluating a published process over the cited input statements.
An aggregate is believed only if it **recomputes** (SPEC-0005 §6).

## 9. Verifying one statement

### 9.1 Results

| result | meaning |
|---|---|
| **verified** | the statement is well-formed and was signed by the key named by `says` |
| **invalid** | it is malformed, or its signature does not verify; it MUST NOT be used |
| **unverifiable** | it may be valid, but this verifier cannot tell: unsupported suite, or no key for `says` |

An invalid statement carries a reason code (§12.9).

### 9.2 Procedure

A verifier MUST perform these steps in this order, stopping at the first that
fails.

| step | check | on failure |
|---|---|---|
| **V1** envelope | the input decodes, under §4.3, as an array of 4 or 5 elements of types (uint, 32-octet bytes, bytes, bytes, ? bytes) with no trailing bytes | invalid `envelope` |
| **V2** suite | `suite` is registered and supported | unverifiable `suite` |
| **V3** key | obtain the public key: from the key store by (`suite`, `says`); or, if the envelope carries `pub`, from `pub` after checking `kid(pub) = says`. Apply the suite's strict key rules (§6.3) | unverifiable `unknown-key` if none; invalid `key` if the strict rules or the kid check fail |
| **V4** signature | verify `sig` over the suite's signature input built from the received `tbs`, under the suite's strict signature rules | invalid `signature` |
| **V5** canonical | decode `tbs` with the validating decoder of §4.3 | invalid `encoding` |
| **V6** agreement | the decoded `suite` and `says` equal the envelope's | invalid `envelope-mismatch` |
| **V7** structure | the statement and every map in it conform to §7 and §8 and Appendix B: closed maps, registered kind, required fields present, `this` as the kind requires, every `type-ref` carries a `definition` | invalid `structure` |
| **V8** kind rules | the kind-specific checks of §8 that need only this statement (e.g. `key-publish`: `kid(body.key) = says`; `rotate`: `this ≠ [1, says]`; `trust`: target and threshold form) | invalid `kind-rule` |
| **V9** result | the statement is **verified**; its digest is SHA-256(`tbs`) | — |

Checks that need other statements, definitions or time — revocation, validity
at a time, whether a type exists, whether a value is in range, authorization —
are **not** part of single-statement verification. They are trust evaluation
(SPEC-0004).

## 10. Key store

A verifier keeps a key store mapping (suite, kid) to a public key. It MUST add a
binding only from:

1. a **verified** `key-publish`, or a verified `self` that carries a key, whose
   key hashes to its `says`; or
2. an **out-of-band import** — for example a scanned code or a file — followed by
   the same check that the kid is the SHA-256 of the key.

Before storing, the suite's strict key rules MUST be applied. A key MUST NOT be
added because a statement merely names it, because it appears as an envelope
`pub` on a statement of another kind, or because a `rotate` names it.

**A key in the key store is known, not trusted.** Trust is decided by trust
evaluation, per context (SPEC-0004).

## 11. Human-review form

### 11.1 One statement, two forms

A statement has exactly one **binary form** — its KSA-CBOR TBS, which is what is
signed, hashed and transmitted — and one **human-review form**, written in YAML,
which is what people read, write and review. The human form represents the
binary form exactly: every field, every value, and the signature. A conforming
tool converts between the two **one-to-one**, with the one exception of §11.3
(text that reads as bytes):

- **human → binary, for signing:** a producer writes or edits the human form; the
  tool encodes it into the TBS (§4.2); the TBS is signed; the signature is added
  to the human form as `signed`.
- **binary → human, for review:** a reader receives an envelope (§5); the tool
  verifies it (§9) and decodes the TBS into the human form, with the signature as
  `signed`.

Converting the human form of a signed statement back to binary MUST reproduce
**exactly** the TBS that was signed, and converting that TBS to human form MUST
reproduce the same human form, apart from annotations (§11.3). A human form that does not convert to bytes whose
signature verifies is rejected; a tool MUST NOT adjust either form to make them
agree. The human form is never itself signed or hashed — the bytes are the
statement, and the YAML is an exact view of them.

### 11.2 A signed statement in human form

The human form of a signed statement is the statement's fields (§7) followed by
`signed`, which carries the signature and, optionally, the public-key hint of
the envelope (§5):

```yaml
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
```

This is test vector TV-4 (Appendix A). Encoding everything above `signed`
yields TV-4's TBS byte for byte; `signed.value` is its signature over `DS ‖ TBS`;
and the envelope is `[suite, says, TBS, signed.value]` — with `signed.pub`
appended as the fifth element when present.

Fields SHOULD appear in the order `kind`, `suite`, `says`, `this`, `valid`,
`body`, `signed`. Order in the human form does not affect the binary form, whose
map keys are always sorted (§4.2).

### 11.3 Lexical rules

- Field names are the names of §7–§8, with `-` written as a space.
- Codes are written by name: `suite: ksa-ed25519-sha256`, `kind: attestation`,
  `alg: sha-256`. A tool maps each name to its registered code (§12).
- The form is YAML 1.2, core schema, restricted to what a YAML 1.1 parser reads
  the same way. Text that either version resolves to something else MUST be
  quoted (`yes`, `no`, `on`, `off`, `y`, `n`, `1e3`, `0o17`), and a plain scalar
  inside a flow collection MUST NOT contain `?`. A reader MUST reject such a
  plain scalar rather than guess.
- Byte strings are quoted text: `'0x'` followed by lowercase hexadecimal.
- Where a field's type does not say bytes or text — a `value` of §4.1, as in
  `body.has` or a description target — a quoted `'0x…'` is bytes. Text of exactly
  that shape has no human form there: a tool MUST refuse to convert the statement
  and MUST NOT alter the text. The statement stays valid in its binary form.
- A target (§7.2) is a map with one key, the name of its type: `{key: '0x…'}`,
  `{digest: {alg: sha-256, value: '0x…'}}`, `{statement: '0x…'}`,
  `{definition: '0x…'}`,
  `{description: {type: {definition: '0x…', label: text}, value: …}}`, and
  `{name: {issuer: '0x…', labels: [text, …]}}`. A label that a YAML 1.1 parser
  reads as non-text — `yes`, `no`, `on`, `off`, `y`, `n` — is quoted, as above.
- Times are quoted text in the exact form of §4.4. A YAML loader MUST NOT resolve
  YAML timestamps.
- Integers are decimal only: `0`, or an optional `-` followed by a non-zero digit
  and further digits. Hexadecimal, octal, binary, a leading `+`, leading zeros,
  `-0`, `_` separators and sexagesimal forms MUST be rejected, whether implicit
  or tagged.
- Floats, `null` and YAML-only types MUST be rejected.
- Text is taken byte-exact (§4.1); a tool MUST NOT fold, trim or normalise it.
- The human form MAY carry annotations whose keys begin with `_`. They are not
  part of the statement: they are discarded before encoding, never signed, and
  absent when the binary form is converted back.

## 12. Registries

Every registry in this section is **append-only**. A code or name, once
assigned, MUST NOT be reassigned or reused; a withdrawn entry becomes
"reserved, never assigned". Code 0 is reserved in every numeric registry.
"Specification Required" means: added by a revision of this specification
accepted through an ADR. Registering an entry MUST NOT change the canonical
bytes of any existing statement.

### 12.1 Statement kinds — §8.1
### 12.2 Target types — §7.2

Code 5 is reserved, never assigned: the locator was withdrawn in 0.6.0 (§7.2).
A new target type MUST bind a digest (ARCH-0001 R-M-07). Code 7, the name, was
registered in 0.9.0 (ADR-0008).

### 12.3 Cipher suites — §6.2

A suite whose key algorithm differs from that of a registered suite MUST NOT be
registered if a valid public-key encoding under it can equal a valid
public-key encoding under the registered suite: `kid` does not hash the suite
(§4.5), so equal encodings would give two keys one identifier. Suites that
share a key algorithm share `kid`s, because the key is the principal
(ADR-0005).

### 12.4 Key algorithms (`public-key.alg`)

| code | algorithm | suites |
|---|---|---|
| 1 | Ed25519 | 1 |
| 2 | ECDSA P-256 (reserved) | 2 |
| 8 | ML-DSA-65 (provisional) | 8 |

### 12.5 Digest algorithms (target type 2)

| code | algorithm | length |
|---|---|---|
| 1 | SHA-256 | 32 |
| 2 | SHA-384 | 48 |
| 3 | SHA-512 | 64 |

### 12.6 DS labels — §6.4

### 12.7 Usage codes (`self.uses`)

| code | usage | | code | usage |
|---|---|---|---|---|
| 1 | statements | | 4 | email |
| 2 | tls | | 5 | payments |
| 3 | ipsec | | 6 | transport (SPEC-0001 §8) |

Usage codes are declarative. Wallets SHOULD vary their interface by usage —
payments SHOULD require stronger confirmation — and enforcement at evaluation
time is policy (SPEC-0004 §9).

### 12.8 Controller kinds (`self.controller`)

| code | controller |
|---|---|
| 1 | person |
| 2 | organisation |
| 3 | service or script |
| 4 | AI agent |
| 5 | software implementation |
| 6 | hardware device |

### 12.9 Verification reason codes — §9.2

`envelope`, `suite`, `unknown-key`, `key`, `signature`, `encoding`,
`envelope-mismatch`, `structure`, `kind-rule`.

## 13. Security considerations

### 13.1 Canonicalisation

Signing a re-encoded form invites two encoders to
disagree and lets a verifier's decoder run on unauthenticated input. KSA signs
and verifies the received bytes (§5) and rejects any non-canonical encoding
(§4.3), so there is exactly one encoding of each statement and no repair path.

### 13.2 Cross-protocol use

A signature binds its DS label (§6.4). A key that is
also used in another protocol cannot have a KSA signature replayed there, or a
signature from there replayed as KSA, provided that protocol also domain-separates.
Wallets SHOULD NOT use one key in more than one protocol even so
(SPEC-0001 §5.3).

### 13.3 Malleability

Without the strict rules of §6.3, Ed25519 admits more than
one valid signature on a message (S + L) and keys of small order that verify
forged signatures. Statements are content-addressed by the digest of their TBS,
not of their signature, so signature malleability cannot change a statement's
identity — but the strict rules are still REQUIRED, because some downstream
systems key on signatures.

### 13.4 Key substitution

`kid` is the hash of the full public key, so two keys
cannot share a kid without a SHA-256 collision. Identifiers MUST NOT be truncated
in signed or hashed bytes.

### 13.5 Unknown suites and kinds

An unknown suite is unverifiable, never
silently accepted; an unknown kind or field is invalid. A verifier MUST NOT skip
what it does not understand (ARCH-0002 P5).

### 13.6 Resource limits

A verifier MUST accept a TBS of at least 65 536 octets
and nesting depth of at least 16, and MAY reject larger or deeper inputs as
`encoding`. It MUST bound the work it performs on any input before V4 succeeds.

### 13.7 Abbreviated transport forms

A transport that abbreviates identifiers
(§4.5) MUST NOT be trusted to reconstruct them; the reconstructed TBS is verified
in full, and an abbreviation that reconstructs to the wrong bytes simply fails V4.

### 13.8 Replay

A statement is a durable assertion; replaying it is not an
attack on it. Freshness, where needed, comes from validity windows and from a
proof of possession bound to a presentation and a nonce (SPEC-0001 §8).

### 13.9 Time

Validity depends on the evaluator's clock. SPEC-0004 §8 says how a
time is chosen.

### 13.10 Locators as subjects

A statement about a locator would be about whatever the locator resolves to
when someone looks, so one signature could vouch for different content on
different days. That is why type 5 was withdrawn (§7.2). A description target
(type 6) whose value is only a URI does not reintroduce the problem: its
identity is the description, so it is a statement about the name, not about
content found under it. A definer SHOULD NOT define a description type that a
reader would take for a statement about the content at a locator.

### 13.11 Names as subjects

A trust statement to a name (§8.6) trusts whichever keys the name's issuer —
and every issuer along its chain — binds the labels to at the evaluation time.
That is the point of a name: Carol can trust *Alice's release signer* and let
Alice change who that is. It is also a delegation of the choice of key that no
`may-delegate` constrains. A speaker that wants to fix the key trusts the key
(`[1, kid]`), not a name. SPEC-0004 §11.7 discusses the evaluation side.

## 14. Privacy considerations

Statements are designed to be shown to others. A kid is a stable identifier and
links every statement made with that key; personas that need to be unlinkable
MUST use separate keys. `self.label` and `self.controller` are published. Trust
statements reveal relationships; SPEC-0004 §4 keeps trust anchors local unless
their owner chooses to publish them.

## 15. References

### 15.1 Normative

- [RFC2119] Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", BCP 14, RFC 2119, March 1997.
- [RFC8174] Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words", BCP 14, RFC 8174, May 2017.
- [RFC8032] Josefsson, S. and I. Liusvaara, "Edwards-Curve Digital Signature Algorithm (EdDSA)", RFC 8032, January 2017.
- [RFC8949] Bormann, C. and P. Hoffman, "Concise Binary Object Representation (CBOR)", STD 94, RFC 8949, December 2020.
- [FIPS180-4] NIST, "Secure Hash Standard (SHS)", FIPS 180-4, August 2015.
- [FIPS204] NIST, "Module-Lattice-Based Digital Signature Standard", FIPS 204, August 2024.

### 15.2 Informative

- [RFC8610] Birkholz, H., Vigano, C. and C. Bormann, "Concise Data Definition Language (CDDL)", RFC 8610, June 2019.
- [RFC8785] Rundgren, A., Jordan, B. and S. Erdtman, "JSON Canonicalization Scheme (JCS)", RFC 8785, June 2020.
- [ADR-0003] "KSA core design decisions", m-of-n, October 2026.
- [ARCH-0001], [ARCH-0002], [ARCH-0003] — the design record for this specification.

---

## Appendix A. Test vectors

Generated by `spec/vectors/ksa-core/generate.py` with the `cryptography` and
`cbor2` libraries; every positive vector is encoded by two independent encoders
that agree byte for byte, and every signature verifies with a third, separate
check. Machine-readable form: `spec/vectors/ksa-core/vectors.json`. A conforming
verifier MUST return **verified** for every positive vector and **invalid** at
the stated step for every negative vector.

The threshold vectors use `ARCH-0001`'s letters: `k` is `threshold` (the `n` of
§8.6) and `n` is the length of `trusts`. **V8 owns `1 ≤ k ≤ n`** (N-7, N-8).
`n = len(members)` holds by construction, because §8.6 has no `n` field: `n` is
the array head of `trusts`. Writing a disagreement takes a field the closed map
refuses (N-9, V7) or a head the decoder refuses (N-10, V5).

<!-- VECTORS:BEGIN -->
<!-- generated by spec/vectors/ksa-core/generate.py — do not edit by hand -->

### Keys

| name | seed | public key | kid = SHA-256(pub) |
|---|---|---|---|
| alice | `9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60` | `d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a` | `21fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9` |
| bob | `4ccd089b28ff96da9db6c346ec114e0f5b8a319f35aba624da8cf6ed4fb8a6fb` | `3d4017c3e843895a92b70aa74d1b7ebc9c982ccf2ec4968cc0cd55f12af4660c` | `39f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f` |
| carol | `94f0d20c5f4157e44463f03fae4d9c93c59da7c42af17014481faf7ab80c5009` | `be2809c0673894dc058c0f06f32d870c2a95b671d9df62074fcb19c0c203bf6b` | `c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e207` |
| bob2 | `cfe6d5ee21b7bf722007ceb061436f23285c43dd9366d51d5d9cd978be007061` | `05da6bf466928fa468b1ecb00413a356c33502b70dc0620020fe98315cd1dfd8` | `9dcd2b600a6996b68623f46e19c60b6eb076c4a707df022e8479ef1d191b91f6` |
| dave | `dbc609cad15d4aabefe042cb34464bf44c5de7b1d334110b56e63d85bdc36d30` | `12c774f6da3f108cfff39ce54595fdd2159b0e2d2d6487c01d8154e14bb355ea` | `d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c7` |

Domain-separation label (hex): `4b53412d53544d542d5349472d763100`

### DV-1 — definition `supply-chain` v1, definer Alice

DefinitionId = SHA-256(body) = `517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a7175`

```
a401582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9026c737570706c792d636861696e03613105838201a701706275696c642d70726f76656e616e6365020103a262656e704275696c642070726f76656e616e6365626573781e50726f636564656e636961206465206c6120636f6d70696c616369c3b36e04a262656e781b486f772074686520617274696661637420776173206275696c742e626573781f43c3b36d6f20736520636f6d70696cc3b320656c2061727465666163746f2e0683a3016c726570726f64756369626c6502a262656e6c526570726f64756369626c656265736c526570726f64756369626c6503a262656e78296275696c7420726570726f64756369626c792066726f6d207075626c697368656420736f75726365736265737838636f6d70696c61646f20646520666f726d6120726570726f64756369626c65206465736465206675656e746573207075626c696361646173a30168617474657374656402a162656e68417474657374656403a162656e781d6275696c7420627920616e20617474657374656420706970656c696e65a3016a756e766572696669656402a162656e6a556e766572696669656403a162656e736f726967696e206e6f7420766572696669656408020981a2016a70726f76656e616e636502a162656e782e446f6573207468652070726f76656e616e6365206e616d6520746865206578706563746564206275696c6465723f8201a601676f7574636f6d65020103a162656e6e526576696577206f7574636f6d6504a162656e781a57686174206120726576696577657220636f6e636c756465642e0683a30167617070726f766502a162656e67417070726f766503a162656e7819726561647920746f207075626c697368206173206275696c74a301676368616e67657302a162656e6f52657175657374206368616e67657303a162656e78196e6f742072656164793b206368616e676573206e6565646564a3016672656a65637402a162656e6652656a65637403a162656e756d757374206e6f74206265207075626c697368656408008202a7017372656c656173652d6174746573746174696f6e020403a10181020481a201a102706275696c642d70726f76656e616e636502f5051a00278d0008a262656e78327b736179737d20617474657374732074686174207b746869737d20776173207b6275696c642d70726f76656e616e63657d2e62657378337b736179737d2061746573746967756120717565207b746869737d20667565207b6275696c642d70726f76656e616e63657d2e09a162656e7352656c65617365206174746573746174696f6e
```

### DV-2 — definition `names` v1, definer Alice

DefinitionId = SHA-256(body) = `de31bf2eb08018aa6a24175a240a6d1fc5d56561bef8b45201b6b075064cf741`

```
a401582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b902656e616d657303613105818201a501646e616d65020303a162656e644e616d6504a162656e7822576861742074686520737065616b65722063616c6c7320746865207461726765742e0800
```

### DV-3 — definition `library-review` v1, definer Dave

DefinitionId = SHA-256(body) = `bf49683b008a99fcdd3e2d2068b14b56b5cdca3c08d8724613ff5969d4f6f73f`

```
a4015820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c7026e6c6962726172792d72657669657703613105858201a601687265766965776564020103a262656e68526576696577656462657368526576697361646f04a262656e783b57686574686572206120706572736f6e2068617320636865636b656420746865207265636f726420616761696e73742069747320736f757263652e6265737835536920756e6120706572736f6e6120686120636f74656a61646f20656c20726567697374726f20636f6e207375206675656e74652e0683a3016379657302a262656e635965736265736353c3ad03a262656e7822636865636b656420696e2066756c6c20616761696e73742069747320736f757263656265737823636f74656a61646f20706f7220636f6d706c65746f20636f6e207375206675656e7465a301677061727469616c02a262656e66506172746c7962657368456e20706172746503a262656e7822636865636b656420696e207061727420616761696e73742069747320736f75726365626573781f636f74656a61646f20656e20706172746520636f6e207375206675656e7465a301626e6f02a262656e624e6f626573624e6f03a262656e781e6e6f7420636865636b656420616761696e73742069747320736f7572636562657378196e6f20636f74656a61646f20636f6e207375206675656e746508028201a501657469746c65020303a162656e655469746c6504a162656e781e54686520776f726b2773207469746c65206173207075626c69736865642e08008201a60164776f726b020903a262656e64576f726b626573644f62726104a262656e783041207075626c697368656420776f726b2c206964656e74696669656420627920697473206465736372697074696f6e2e6265737835556e61206f627261207075626c69636164612c206964656e746966696361646120706f7220737520646573637269706369c3b36e2e08000b81a501657469746c6502a102657469746c6503f504a162656e655469746c6505a162656e77546865207469746c65206173207075626c69736865642e8201a501676c6f6361746f72020303a262656e674c6f6361746f726265736b4c6f63616c697a61646f7204a262656e78325768657265206120636f7079206d617920626520666f756e642e2045766964656e63652c206e6f74206964656e746974792e626573783744c3b36e64652070756564652068616c6c6172736520756e6120636f7069612e20496e646963696f2c206e6f206964656e74696461642e08008202a6016f7265636f72642d7265766965776564020403a1018202060482a201a10268726576696577656402f5a201a102676c6f6361746f7202f408a262656e782b7b736179737d2073617973207b746869737d2069732072657669657765643a207b72657669657765647d2e62657378327b736179737d206469636520717565207b746869737d20657374c3a120726576697361646f3a207b72657669657765647d2e09a262656e6f5265636f726420726576696577656462657371526567697374726f20726576697361646f
```

### DV-4 — definition `naming` v1, definer Alice; `name` has base kind 12

DefinitionId = SHA-256(body) = `eaf0ec4440c9c9bfbead12db82f44d1bd4ad74472f6c6014673c25f62a296729`

```
a401582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b902666e616d696e6703613105818201a501646e616d65020c03a262656e644e616d65626573664e6f6d62726504a262656e7842576861742074686520737065616b65722063616c6c7320746865207461726765742c20696e2074686520737065616b65722773206f776e206e616d6573706163652e626573784443c3b36d6f206c6c616d6120656c206861626c616e746520616c2064657374696e6f2c20656e2073752070726f70696f206573706163696f206465206e6f6d627265732e0800
```

### TV-1 — key-publish: Alice publishes her Ed25519 key; this = says = SHA-256(pub); the envelope carries pub

- signer: alice
- statement digest = SHA-256(TBS): `66127ad345e8575fcb7d626b4171e6f26e94cc4bb24dfa6478fbebd24f6f89ed`
- TBS:
```
a60101020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9048201582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b905a20119022b031a02dc210006a101a20101025820d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a
```
- signature over DS ‖ TBS:
```
87401657335ec9c1754ea381abc7c0b084c80583afce4e4ef9e21c01b8bc77e029480bfafc51a456109f3ed9541a0c9fa54c1c39f3bb56bfa9c4ea6c570ef101
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
8501582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b95882a60101020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9048201582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b905a20119022b031a02dc210006a101a20101025820d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a584087401657335ec9c1754ea381abc7c0b084c80583afce4e4ef9e21c01b8bc77e029480bfafc51a456109f3ed9541a0c9fa54c1c39f3bb56bfa9c4ea6c570ef1015820d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a
```
- expected: **accept**

### TV-2 — self: label Alice, uses [statements], controller person (a self-claim)

- signer: alice
- statement digest = SHA-256(TBS): `91877221d7ea2743d9d802bce179aaaac9ff1e818d07a4a2d42ef7cee35efb8b`
- TBS:
```
a60102020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9048201582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b905a20119022b031a02dc210006a30265416c6963650381010501
```
- signature over DS ‖ TBS:
```
3ff5e983aeefc3d5d451aa05493d843e6a22eaeefeefea2066fd4e5bf40b86f974cfc626c97a03bb8b2e4cb7b70aefb3199595d0b2c597881ff5f56ae4a0630c
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
8401582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b95867a60102020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9048201582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b905a20119022b031a02dc210006a30265416c696365038101050158403ff5e983aeefc3d5d451aa05493d843e6a22eaeefeefea2066fd4e5bf40b86f974cfc626c97a03bb8b2e4cb7b70aefb3199595d0b2c597881ff5f56ae4a0630c
```
- expected: **accept**

### TV-3 — define: Alice publishes definition DV-1 by its DefinitionId

- signer: alice
- statement digest = SHA-256(TBS): `2d200d1936d1d69945774e0c02662f25263fe4a07b11636643cfd0336fbaa97c`
- TBS:
```
a60108020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b90482045820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717505a20119022d031a02ddff2006a2016c737570706c792d636861696e026131
```
- signature over DS ‖ TBS:
```
8e08134764f37f17a2042ef965a74e5d46464db9d154772a78cb8a1c8e4bd3c4809709efef19b94bf621ca9cf6510b73f90585d3cb5a704b6303801b27513f06
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
8401582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9586ca60108020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b90482045820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717505a20119022d031a02ddff2006a2016c737570706c792d636861696e02613158408e08134764f37f17a2042ef965a74e5d46464db9d154772a78cb8a1c8e4bd3c4809709efef19b94bf621ca9cf6510b73f90585d3cb5a704b6303801b27513f06
```
- expected: **accept**

### TV-4 — attestation about an ARTIFACT digest (not a key): build-provenance = reproducible

- signer: alice
- statement digest = SHA-256(TBS): `c539ace6b96e917b73074266f4ec46c69d07348c8d75d1660cbbaa6a1aaf6922`
- TBS:
```
a60104020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b904830201582048dfc39586b0c4f9e905b3b60f59a30b7c0c7408e44f7cb4df2a09fbf3e67ba705a30119022d02190261031a02de295006a10181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e6365026c726570726f64756369626c65
```
- signature over DS ‖ TBS:
```
8f30ee4ef039d81813703a2b629bb60e5abfc5b82a07432594a2add6fb77d24ccb9a41d744022af89e5ce0ead553131929e2f66fbd1c2ec1869b2c4c91319c0f
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
8401582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b958a8a60104020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b904830201582048dfc39586b0c4f9e905b3b60f59a30b7c0c7408e44f7cb4df2a09fbf3e67ba705a30119022d02190261031a02de295006a10181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e6365026c726570726f64756369626c6558408f30ee4ef039d81813703a2b629bb60e5abfc5b82a07432594a2add6fb77d24ccb9a41d744022af89e5ce0ead553131929e2f66fbd1c2ec1869b2c4c91319c0f
```
- expected: **accept**

### TV-5 — trust: Carol trusts Alice about build-provenance in {reproducible, attested}; may delegate depth 1 within {reproducible}

- signer: carol
- statement digest = SHA-256(TBS): `723436bf3ca419bc57fdea0f2b6518f65d280d04c1928b618e9f70a58ce785e6`
- TBS:
```
a601050201035820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e207048201582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b905a20119022d031a02de376006a20181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e636503826c726570726f64756369626c6568617474657374656402a301010281a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e636503816c726570726f64756369626c650519029d
```
- signature over DS ‖ TBS:
```
be4ed1ab94e2cc7ee4cef5af3936334a5bc5307b8c47e07b0e847b4e7b83e973cee0ec8b787626aae9c55d24c1d2812fd42473297a9763d384a980d62f773b0c
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
84015820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e20758fea601050201035820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e207048201582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b905a20119022d031a02de376006a20181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e636503826c726570726f64756369626c6568617474657374656402a301010281a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e636503816c726570726f64756369626c650519029d5840be4ed1ab94e2cc7ee4cef5af3936334a5bc5307b8c47e07b0e847b4e7b83e973cee0ec8b787626aae9c55d24c1d2812fd42473297a9763d384a980d62f773b0c
```
- expected: **accept**

### TV-6 — review: Bob reviews statement TV-4 (target is a statement digest): outcome approve

- signer: bob
- statement digest = SHA-256(TBS): `2f983d3949a31904a1ca69c22f77d42de3dafe5fb415cd577770a9dc49cd153e`
- TBS:
```
a60109020103582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f0482035820c539ace6b96e917b73074266f4ec46c69d07348c8d75d1660cbbaa6a1aaf692205a3011a02de538002190249031a02de538006a20181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502676f7574636f6d650267617070726f766502782570726f76656e616e6365206e616d657320746865206578706563746564206275696c646572
```
- signature over DS ‖ TBS:
```
c44ebdbb53321947f14d0fa3ecdcfbe543a2cdbeb52a42ce5402a32b4a4a20cf09ff11c4e966e508d53e353ec27f21a3d088e54c01f36be6d679cb2eb4f3cc0b
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
8401582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f58c3a60109020103582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f0482035820c539ace6b96e917b73074266f4ec46c69d07348c8d75d1660cbbaa6a1aaf692205a3011a02de538002190249031a02de538006a20181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502676f7574636f6d650267617070726f766502782570726f76656e616e6365206e616d657320746865206578706563746564206275696c6465725840c44ebdbb53321947f14d0fa3ecdcfbe543a2cdbeb52a42ce5402a32b4a4a20cf09ff11c4e966e508d53e353ec27f21a3d088e54c01f36be6d679cb2eb4f3cc0b
```
- expected: **accept**

### TV-7 — revoke: Alice revokes TV-4 by digest, effective 2026-10-21

- signer: alice
- statement digest = SHA-256(TBS): `ff6ea7c3945253db6eceb654775c432214d44b7e7414f33ae366e108eda5a766`
- TBS:
```
a60106020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9048201582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b905a20119024b031a0302cd0006a1015820c539ace6b96e917b73074266f4ec46c69d07348c8d75d1660cbbaa6a1aaf6922
```
- signature over DS ‖ TBS:
```
01c19179c78a6b07811281b2661f40c2c6aff34899f91a990b6d0be0a19f5cca38bf31a9e31a62591384cf4493792b7438b935fd5d17515dc8017cd6b0e7b001
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
8401582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9587ea60106020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9048201582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b905a20119024b031a0302cd0006a1015820c539ace6b96e917b73074266f4ec46c69d07348c8d75d1660cbbaa6a1aaf6922584001c19179c78a6b07811281b2661f40c2c6aff34899f91a990b6d0be0a19f5cca38bf31a9e31a62591384cf4493792b7438b935fd5d17515dc8017cd6b0e7b001
```
- expected: **accept**

### TV-8 — rotate: Bob's old key names its successor; valid.issued orders statements around the rotation

- signer: bob
- statement digest = SHA-256(TBS): `2e5a65d97ae602151edf080639d4683fd3e3169a00ea44a1cdaf8048a7eac479`
- TBS:
```
a60107020103582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f04820158209dcd2b600a6996b68623f46e19c60b6eb076c4a707df022e8479ef1d191b91f605a201190249031a0301434006a101706c6170746f70207265696e7374616c6c
```
- signature over DS ‖ TBS:
```
d03a7aee59a7e03d6d3d17df3b424d67bddef5b372aab58604cb2adb778a26bbdc0c9b87ae2f70bd26d05f23018375a4f0167ea2b2157b6f6c3e7304dd2e3f04
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
8401582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f586da60107020103582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f04820158209dcd2b600a6996b68623f46e19c60b6eb076c4a707df022e8479ef1d191b91f605a201190249031a0301434006a101706c6170746f70207265696e7374616c6c5840d03a7aee59a7e03d6d3d17df3b424d67bddef5b372aab58604cb2adb778a26bbdc0c9b87ae2f70bd26d05f23018375a4f0167ea2b2157b6f6c3e7304dd2e3f04
```
- expected: **accept**

### TV-9 — trust, threshold form: Carol trusts any 2 of {Alice, Bob, Dave}; this is absent; k = 2, n = 3

- signer: carol
- statement digest = SHA-256(TBS): `df30374857ae84d9085c2d19c36132d37206c804c10224c039e1d85fcd288137`
- TBS:
```
a501050201035820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e20705a20119022d031a02de457006a30181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e636503826c726570726f64756369626c656861747465737465640383582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f5820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c70402
```
- signature over DS ‖ TBS:
```
5ec34bb160dff6c0a5be6ca8e2855a660afbb6584692c80c6184bb2ddc7f1913a1c6f954f84751d0b61ff4269eb4b5f2e27b3d2eb138bfb976f7520ecc596a05
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
84015820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e20758f2a501050201035820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e20705a20119022d031a02de457006a30181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e636503826c726570726f64756369626c656861747465737465640383582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f5820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c7040258405ec34bb160dff6c0a5be6ca8e2855a660afbb6584692c80c6184bb2ddc7f1913a1c6f954f84751d0b61ff4269eb4b5f2e27b3d2eb138bfb976f7520ecc596a05
```
- expected: **accept**

### TV-10 — trust, threshold form at the upper bound: k = n = 3

- signer: carol
- statement digest = SHA-256(TBS): `0c53192a46fb496deb0b98b975ee494b1d47897780051c403af83fe1bc83c40f`
- TBS:
```
a501050201035820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e20705a20119022d031a02de457006a30181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e636503826c726570726f64756369626c656861747465737465640383582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f5820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c70403
```
- signature over DS ‖ TBS:
```
83a35968d1addde122a186f791c9cf0a9f2ba6aa592d6237515305ef80a337552e4cae9224614c3f809c6ea2d63ec2afe7def423003730913cef6e72f3687e00
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
84015820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e20758f2a501050201035820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e20705a20119022d031a02de457006a30181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e636503826c726570726f64756369626c656861747465737465640383582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f5820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c70403584083a35968d1addde122a186f791c9cf0a9f2ba6aa592d6237515305ef80a337552e4cae9224614c3f809c6ea2d63ec2afe7def423003730913cef6e72f3687e00
```
- expected: **accept**

### TV-11 — trust, threshold form at the lower bound: k = 1, and the fewest members allowed, n = 2

- signer: carol
- statement digest = SHA-256(TBS): `fe1578fca57f124acc4f89bb4b9dc5ac879bd63773800385c965b5ee4ff6b4e1`
- TBS:
```
a501050201035820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e20705a20119022d031a02de457006a30181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e636503826c726570726f64756369626c656861747465737465640382582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f0401
```
- signature over DS ‖ TBS:
```
64484941d89c9e23863cd67a86c20a3d99aa495a5c7c4c2d0a4bf664146594ec7e4e37b0a0036386f9a9229ab1005ace789d06716febd7e16d89b9b26983b10d
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
84015820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e20758d0a501050201035820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e20705a20119022d031a02de457006a30181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e636503826c726570726f64756369626c656861747465737465640382582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f0401584064484941d89c9e23863cd67a86c20a3d99aa495a5c7c4c2d0a4bf664146594ec7e4e37b0a0036386f9a9229ab1005ace789d06716febd7e16d89b9b26983b10d
```
- expected: **accept**

### TV-12 — define: Alice publishes definition DV-2 by its DefinitionId

- signer: alice
- statement digest = SHA-256(TBS): `7eff2232fc8f286f62da04e35d05a4998bf2b281270256f85e119abb97cfd93d`
- TBS:
```
a60108020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b90482045820de31bf2eb08018aa6a24175a240a6d1fc5d56561bef8b45201b6b075064cf74105a20119022d031a02de619006a201656e616d6573026131
```
- signature over DS ‖ TBS:
```
cf7a47cc54397d7c735a580b5da442eac9fa9c2b94f366669258e18b0a3120b5b99437d89cee6a6118fefe7687b609656823e36ea11e401829b4a2757904c107
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
8401582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b95865a60108020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b90482045820de31bf2eb08018aa6a24175a240a6d1fc5d56561bef8b45201b6b075064cf74105a20119022d031a02de619006a201656e616d65730261315840cf7a47cc54397d7c735a580b5da442eac9fa9c2b94f366669258e18b0a3120b5b99437d89cee6a6118fefe7687b609656823e36ea11e401829b4a2757904c107
```
- expected: **accept**

### TV-13 — attestation about a KEY: Alice says Bob's key has name "fred" (the NameCert role, ARCH-0002 P6)

- signer: alice
- statement digest = SHA-256(TBS): `95eda0cbbc8359b12f136b81f002806b04b8bdfbcd4a4484c635a9bb68e48ceb`
- TBS:
```
a60104020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9048201582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f05a20119022d031a02de6fa006a10181a201a2015820de31bf2eb08018aa6a24175a240a6d1fc5d56561bef8b45201b6b075064cf74102646e616d65026466726564
```
- signature over DS ‖ TBS:
```
1f880dd24d488638117b37af44659458dcce10d412811398f2fd8e6c7990d35c60708ad0470dbaf2e7eb18ebc83392bd55463983cacdc000c516012d5e64d30b
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
8401582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9588fa60104020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9048201582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f05a20119022d031a02de6fa006a10181a201a2015820de31bf2eb08018aa6a24175a240a6d1fc5d56561bef8b45201b6b075064cf74102646e616d6502646672656458401f880dd24d488638117b37af44659458dcce10d412811398f2fd8e6c7990d35c60708ad0470dbaf2e7eb18ebc83392bd55463983cacdc000c516012d5e64d30b
```
- expected: **accept**

### TV-14 — trust: Alice trusts Bob about build-provenance in {attested}; outside TV-5's may-delegate ranges, so widening (SPEC-0004 §6.3 item 4)

- signer: alice
- statement digest = SHA-256(TBS): `f9760edd43873a1aa89090c49f73653c7e3e1ecc49f4819d416aa04d794741d6`
- TBS:
```
a60105020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9048201582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f05a30119022d02190261031a02e0a22006a10181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e63650381686174746573746564
```
- signature over DS ‖ TBS:
```
f33097633532b17ff5c7ef61377093c334dec35b65550b932553c4b9cfa03c7f9b6ad7756f6cc2f10f0e7b5fb615648d40d51d6fb683bb1aedb1c8cf48314602
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
8401582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b958a4a60105020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9048201582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f05a30119022d02190261031a02e0a22006a10181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e636503816861747465737465645840f33097633532b17ff5c7ef61377093c334dec35b65550b932553c4b9cfa03c7f9b6ad7756f6cc2f10f0e7b5fb615648d40d51d6fb683bb1aedb1c8cf48314602
```
- expected: **accept**

### TV-15 — attestation: Bob says the artifact's build-provenance is attested

- signer: bob
- statement digest = SHA-256(TBS): `301b2f78438e1d64903d5e25e541df06aca28148c95b75550dc7e84c3265afde`
- TBS:
```
a60104020103582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f04830201582048dfc39586b0c4f9e905b3b60f59a30b7c0c7408e44f7cb4df2a09fbf3e67ba705a30119022d02190261031a02e0be4006a10181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e636502686174746573746564
```
- signature over DS ‖ TBS:
```
5af2cb3507de8db280c61401d93210a2e1b144721cb31812f9bd7cb3d59609fbed2f4c19a68b302b74c8064dd1e5a66046a53ab1ebd029ab62cb1641ec15c101
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
8401582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f58a4a60104020103582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f04830201582048dfc39586b0c4f9e905b3b60f59a30b7c0c7408e44f7cb4df2a09fbf3e67ba705a30119022d02190261031a02e0be4006a10181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e63650268617474657374656458405af2cb3507de8db280c61401d93210a2e1b144721cb31812f9bd7cb3d59609fbed2f4c19a68b302b74c8064dd1e5a66046a53ab1ebd029ab62cb1641ec15c101
```
- expected: **accept**

### TV-16 — trust: Alice trusts Bob about build-provenance in {reproducible}, no may-delegate: within TV-5, one hop only

- signer: alice
- statement digest = SHA-256(TBS): `91a3a2ae9b1d5dd1abfaf20add65860b6a780244d58d325a2b5001f936b6c5d1`
- TBS:
```
a60105020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9048201582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f05a30119022d02190261031a02e0b03006a10181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e636503816c726570726f64756369626c65
```
- signature over DS ‖ TBS:
```
1e13a18450e9c23749fb42e5c4e57077dcda687982f45f2840ad9467bdfe28ab0d54de53a5b643f7aa91d21ba13a26cdcfc1877fa9feb0093a9574d86f789e06
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
8401582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b958a8a60105020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9048201582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f05a30119022d02190261031a02e0b03006a10181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e636503816c726570726f64756369626c6558401e13a18450e9c23749fb42e5c4e57077dcda687982f45f2840ad9467bdfe28ab0d54de53a5b643f7aa91d21ba13a26cdcfc1877fa9feb0093a9574d86f789e06
```
- expected: **accept**

### TV-17 — attestation: Bob says the artifact's build-provenance is reproducible

- signer: bob
- statement digest = SHA-256(TBS): `f989c563610a233bb88537324c9b3cfd9f95e0582c09778e4f5a4f8b80927eb2`
- TBS:
```
a60104020103582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f04830201582048dfc39586b0c4f9e905b3b60f59a30b7c0c7408e44f7cb4df2a09fbf3e67ba705a30119022d02190261031a02e0cc5006a10181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e6365026c726570726f64756369626c65
```
- signature over DS ‖ TBS:
```
aa2c6d5bece36a873b84419b6f927dd3ccb873dbe19aee14a20ae7156699f4af43383defbbaef0b54a49ac6c8862819194352f27763bc144f31687bf62b9de0c
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
8401582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f58a8a60104020103582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f04830201582048dfc39586b0c4f9e905b3b60f59a30b7c0c7408e44f7cb4df2a09fbf3e67ba705a30119022d02190261031a02e0cc5006a10181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e6365026c726570726f64756369626c655840aa2c6d5bece36a873b84419b6f927dd3ccb873dbe19aee14a20ae7156699f4af43383defbbaef0b54a49ac6c8862819194352f27763bc144f31687bf62b9de0c
```
- expected: **accept**

### TV-18 — trust: Bob trusts Dave about build-provenance in {reproducible}; Bob holds no delegation, so depth (§6.3 item 3)

- signer: bob
- statement digest = SHA-256(TBS): `945f160a7b396c7946e1eee931c0ba353d3d3549f397a1a5a0d958eca0165785`
- TBS:
```
a60105020103582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f0482015820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c705a30119022d02190261031a02e0da6006a10181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e636503816c726570726f64756369626c65
```
- signature over DS ‖ TBS:
```
1c8bd2d23d0bfbfd45e78dfe1e52abb86f54ea7aaa0aa749c6b8a54a18af30296d1a731a6bc604eab221d7768112da77a06a7bda725407d51207f2b011282f01
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
8401582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f58a8a60105020103582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f0482015820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c705a30119022d02190261031a02e0da6006a10181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e636503816c726570726f64756369626c6558401c8bd2d23d0bfbfd45e78dfe1e52abb86f54ea7aaa0aa749c6b8a54a18af30296d1a731a6bc604eab221d7768112da77a06a7bda725407d51207f2b011282f01
```
- expected: **accept**

### TV-19 — attestation: Dave says the artifact's build-provenance is reproducible

- signer: dave
- statement digest = SHA-256(TBS): `887fc4b19da9fe1ffca8eb37bbd988c35b9ab4f3d10276fff6660afc1b5dd860`
- TBS:
```
a601040201035820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c704830201582048dfc39586b0c4f9e905b3b60f59a30b7c0c7408e44f7cb4df2a09fbf3e67ba705a30119022d02190261031a02e0e87006a10181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e6365026c726570726f64756369626c65
```
- signature over DS ‖ TBS:
```
a2b92707c466829186749934b63edb87ef50e713952a6ace1d260a8a3bb6ad3279136dbec59ddd3afb419e73073cfb5a8077b0affef0b18d2707fd276a7aae04
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
84015820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c758a8a601040201035820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c704830201582048dfc39586b0c4f9e905b3b60f59a30b7c0c7408e44f7cb4df2a09fbf3e67ba705a30119022d02190261031a02e0e87006a10181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e6365026c726570726f64756369626c655840a2b92707c466829186749934b63edb87ef50e713952a6ace1d260a8a3bb6ad3279136dbec59ddd3afb419e73073cfb5a8077b0affef0b18d2707fd276a7aae04
```
- expected: **accept**

### TV-20 — trust: Alice trusts Bob about {reproducible} with may-delegate depth 1; TV-5 left Alice depth 1, so at most 0 may pass on: widening (§6.3 item 6)

- signer: alice
- statement digest = SHA-256(TBS): `c481e1c3ea5bec415ee0483f5c706d0d72015634e207c9aa9497a8cea60b1279`
- TBS:
```
a60105020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9048201582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f05a30119022d02190261031a02e0f68006a20181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e636503816c726570726f64756369626c6502a10101
```
- signature over DS ‖ TBS:
```
a40aa8f3d2fc416b2108c6b93eaf732719db7a6bf94fc979f054a3028f5ff2cfd5a87844f8c1d1f2a2c3b3f6503be5eb83db2f90f1a2b094f639c874543c8702
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
8401582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b958aca60105020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9048201582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f05a30119022d02190261031a02e0f68006a20181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e636503816c726570726f64756369626c6502a101015840a40aa8f3d2fc416b2108c6b93eaf732719db7a6bf94fc979f054a3028f5ff2cfd5a87844f8c1d1f2a2c3b3f6503be5eb83db2f90f1a2b094f639c874543c8702
```
- expected: **accept**

### TV-21 — define: Dave, the library lead, publishes definition DV-3 `library-review`

- signer: dave
- statement digest = SHA-256(TBS): `556f357b90a68515972ec97a6d8fb4193ef576cb0e4b8f9dcd5ac4791542db81`
- TBS:
```
a601080201035820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c70482045820bf49683b008a99fcdd3e2d2068b14b56b5cdca3c08d8724613ff5969d4f6f73f05a201190231031a02e3452006a2016e6c6962726172792d726576696577026131
```
- signature over DS ‖ TBS:
```
09f743fca2b1f21b5154945188a96cc736bc0396b21c38b38756c2be80afea8cb8bd68887705f74ccd4c8647f91c36724e0d835e381ebacb81d920ce95695c01
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
84015820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c7586ea601080201035820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c70482045820bf49683b008a99fcdd3e2d2068b14b56b5cdca3c08d8724613ff5969d4f6f73f05a201190231031a02e3452006a2016e6c6962726172792d726576696577026131584009f743fca2b1f21b5154945188a96cc736bc0396b21c38b38756c2be80afea8cb8bd68887705f74ccd4c8647f91c36724e0d835e381ebacb81d920ce95695c01
```
- expected: **accept**

### TV-22 — trust: Carol, a reader, trusts Dave about reviewed (unbounded), may delegate depth 1; her anchor in context `library`

- signer: carol
- statement digest = SHA-256(TBS): `11c3cc6e9e39114481115e2b66ff8a8f7428a50f47758c8c89b6c2ab44cdf07d`
- TBS:
```
a601050201035820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e2070482015820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c705a3011902310219029d031a02e3533006a20181a101a2015820bf49683b008a99fcdd3e2d2068b14b56b5cdca3c08d8724613ff5969d4f6f73f0268726576696577656402a10101
```
- signature over DS ‖ TBS:
```
b1067edfa45f0d8c3ddf82e316f95fe247217631ff858b31032a30a8d89736eb9ed21173ae75cdae4be17e1507bcc130943d10488f51a9de0e4d30ab589d3305
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
84015820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e2075895a601050201035820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e2070482015820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c705a3011902310219029d031a02e3533006a20181a101a2015820bf49683b008a99fcdd3e2d2068b14b56b5cdca3c08d8724613ff5969d4f6f73f0268726576696577656402a101015840b1067edfa45f0d8c3ddf82e316f95fe247217631ff858b31032a30a8d89736eb9ed21173ae75cdae4be17e1507bcc130943d10488f51a9de0e4d30ab589d3305
```
- expected: **accept**

### TV-23 — trust: Dave delegates reviewed in {partial} to Bob, a student reviewer

- signer: dave
- statement digest = SHA-256(TBS): `2c9429693877eedd69bf198d8c5d47ec23f905cc949e0e722fc2cbc312e52746`
- TBS:
```
a601050201035820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c7048201582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f05a3011902310219029d031a02e3614006a10181a201a2015820bf49683b008a99fcdd3e2d2068b14b56b5cdca3c08d8724613ff5969d4f6f73f026872657669657765640381677061727469616c
```
- signature over DS ‖ TBS:
```
6c0cdbc09eeae6b8d5299b7a0e9d7a6e9b177c1af2b3c39615342e991013d74aae8c5ebd76ea9e5307b40e2a6a4eeb717ca6fc2225a83f025e28596dd8ffdd0d
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
84015820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c7589ba601050201035820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c7048201582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f05a3011902310219029d031a02e3614006a10181a201a2015820bf49683b008a99fcdd3e2d2068b14b56b5cdca3c08d8724613ff5969d4f6f73f026872657669657765640381677061727469616c58406c0cdbc09eeae6b8d5299b7a0e9d7a6e9b177c1af2b3c39615342e991013d74aae8c5ebd76ea9e5307b40e2a6a4eeb717ca6fc2225a83f025e28596dd8ffdd0d
```
- expected: **accept**

### TV-24 — attestation: Bob says the record has reviewed = yes, from template record-reviewed; outside his scope

- signer: bob
- statement digest = SHA-256(TBS): `17ce8512505a92385201daf0205366ba6e27fa62a64016e609b0f4f93f7deaf0`
- TBS:
```
a60104020103582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f04830201582060cec9d66dd8f1f2fbc27dcbe11e21b8c8c916f978ad4fdf1ec8195a58baf5ee05a3011902310219029d031a02e37d6006a20181a201a2015820bf49683b008a99fcdd3e2d2068b14b56b5cdca3c08d8724613ff5969d4f6f73f02687265766965776564026379657303a2015820bf49683b008a99fcdd3e2d2068b14b56b5cdca3c08d8724613ff5969d4f6f73f026f7265636f72642d7265766965776564
```
- signature over DS ‖ TBS:
```
6ca2bc971441b37be5faf362ad3b4f685c9113ba59deb85a88f9eb6089ff347dafdba3f8301a8153b6d22adf85aee4a936dd4e82abaf856514730f2874d2980d
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
8401582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f58cda60104020103582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f04830201582060cec9d66dd8f1f2fbc27dcbe11e21b8c8c916f978ad4fdf1ec8195a58baf5ee05a3011902310219029d031a02e37d6006a20181a201a2015820bf49683b008a99fcdd3e2d2068b14b56b5cdca3c08d8724613ff5969d4f6f73f02687265766965776564026379657303a2015820bf49683b008a99fcdd3e2d2068b14b56b5cdca3c08d8724613ff5969d4f6f73f026f7265636f72642d726576696577656458406ca2bc971441b37be5faf362ad3b4f685c9113ba59deb85a88f9eb6089ff347dafdba3f8301a8153b6d22adf85aee4a936dd4e82abaf856514730f2874d2980d
```
- expected: **accept**

### TV-25 — attestation: Bob says the record has reviewed = partial, from template record-reviewed

- signer: bob
- statement digest = SHA-256(TBS): `0490ffd0d97f24d095d05eb5504eeeee4626ab43050726cb13f718a94a3d8865`
- TBS:
```
a60104020103582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f04830201582060cec9d66dd8f1f2fbc27dcbe11e21b8c8c916f978ad4fdf1ec8195a58baf5ee05a3011902310219029d031a02e38b7006a20181a201a2015820bf49683b008a99fcdd3e2d2068b14b56b5cdca3c08d8724613ff5969d4f6f73f0268726576696577656402677061727469616c03a2015820bf49683b008a99fcdd3e2d2068b14b56b5cdca3c08d8724613ff5969d4f6f73f026f7265636f72642d7265766965776564
```
- signature over DS ‖ TBS:
```
e492362deb150be79b2c216d1c8aa53a9e867c13b7248ed5d49011aee52043d8295d95bc08ab76ee8725b3875f2433a2989360f71073c49da9da4cf7b6e72a07
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
8401582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f58d1a60104020103582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f04830201582060cec9d66dd8f1f2fbc27dcbe11e21b8c8c916f978ad4fdf1ec8195a58baf5ee05a3011902310219029d031a02e38b7006a20181a201a2015820bf49683b008a99fcdd3e2d2068b14b56b5cdca3c08d8724613ff5969d4f6f73f0268726576696577656402677061727469616c03a2015820bf49683b008a99fcdd3e2d2068b14b56b5cdca3c08d8724613ff5969d4f6f73f026f7265636f72642d72657669657765645840e492362deb150be79b2c216d1c8aa53a9e867c13b7248ed5d49011aee52043d8295d95bc08ab76ee8725b3875f2433a2989360f71073c49da9da4cf7b6e72a07
```
- expected: **accept**

### TV-26 — attestation about a DESCRIPTION target (R-M-11): Dave says the work titled "Simple Public Key Certificate" is reviewed = yes; its locator rides as an attribute

- signer: dave
- statement digest = SHA-256(TBS): `578c1c1ffbcf3a41e21e475af7a2b06d0dc17a02b42e287deb72fbfb0b623bd3`
- TBS:
```
a601040201035820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c7048306a2015820bf49683b008a99fcdd3e2d2068b14b56b5cdca3c08d8724613ff5969d4f6f73f0264776f726ba1657469746c65781d53696d706c65205075626c6963204b657920436572746966696361746505a3011902310219029d031a02e3998006a20182a201a2015820bf49683b008a99fcdd3e2d2068b14b56b5cdca3c08d8724613ff5969d4f6f73f026872657669657765640263796573a201a2015820bf49683b008a99fcdd3e2d2068b14b56b5cdca3c08d8724613ff5969d4f6f73f02676c6f6361746f7202782668747470733a2f2f7777772e7266632d656469746f722e6f72672f7266632f7266633236393303a2015820bf49683b008a99fcdd3e2d2068b14b56b5cdca3c08d8724613ff5969d4f6f73f026f7265636f72642d7265766965776564
```
- signature over DS ‖ TBS:
```
ca62e37cd3c07c045b3bf4095fd79d678f9565ce305e4fb2bf54c72d396930516ef7ae7b467b5d9f054acdfda1093078b7e1b3a545890034aded9354294b1c07
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
84015820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c7590152a601040201035820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c7048306a2015820bf49683b008a99fcdd3e2d2068b14b56b5cdca3c08d8724613ff5969d4f6f73f0264776f726ba1657469746c65781d53696d706c65205075626c6963204b657920436572746966696361746505a3011902310219029d031a02e3998006a20182a201a2015820bf49683b008a99fcdd3e2d2068b14b56b5cdca3c08d8724613ff5969d4f6f73f026872657669657765640263796573a201a2015820bf49683b008a99fcdd3e2d2068b14b56b5cdca3c08d8724613ff5969d4f6f73f02676c6f6361746f7202782668747470733a2f2f7777772e7266632d656469746f722e6f72672f7266632f7266633236393303a2015820bf49683b008a99fcdd3e2d2068b14b56b5cdca3c08d8724613ff5969d4f6f73f026f7265636f72642d72657669657765645840ca62e37cd3c07c045b3bf4095fd79d678f9565ce305e4fb2bf54c72d396930516ef7ae7b467b5d9f054acdfda1093078b7e1b3a545890034aded9354294b1c07
```
- expected: **accept**

### TV-27 — define: Alice publishes definition DV-4 `naming`, whose `name` type has base kind name

- signer: alice
- statement digest = SHA-256(TBS): `a884f193e183a125baa876452ab2ed9627ac1500c3f4df2e5e4e2174ffe005bb`
- TBS:
```
a60108020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b90482045820eaf0ec4440c9c9bfbead12db82f44d1bd4ad74472f6c6014673c25f62a29672905a201190231031a02e3b5a006a201666e616d696e67026131
```
- signature over DS ‖ TBS:
```
e932527c724154f50891010484a2377c43e71f1fc374cd2d1ac613f44a55db37471323e73365df049af69c5421ce47c78a9d31b6bbb9a1805938bf4c90de4309
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
8401582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b95866a60108020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b90482045820eaf0ec4440c9c9bfbead12db82f44d1bd4ad74472f6c6014673c25f62a29672905a201190231031a02e3b5a006a201666e616d696e670261315840e932527c724154f50891010484a2377c43e71f1fc374cd2d1ac613f44a55db37471323e73365df049af69c5421ce47c78a9d31b6bbb9a1805938bf4c90de4309
```
- expected: **accept**

### TV-28 — name binding: Alice's fred is Bob's key (one hop; SPEC-0004 §5.3)

- signer: alice
- statement digest = SHA-256(TBS): `d5adcbf09c384196ce99a361382bd0ecb17b979415f449145303418fa9f2cb9c`
- TBS:
```
a60104020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9048201582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f05a3011902310219029d031a02e3c3b006a10181a201a2015820eaf0ec4440c9c9bfbead12db82f44d1bd4ad74472f6c6014673c25f62a29672902646e616d65026466726564
```
- signature over DS ‖ TBS:
```
1264c85a04ce62806b7900b9cafd6f29434870bf61fa45cf0949cc4df7172439f2fc57ff32468fcaa2ef22f1cd89b25a331e0eea3e41c0cb57e35cf44a0dbe0c
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
8401582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b95893a60104020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9048201582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f05a3011902310219029d031a02e3c3b006a10181a201a2015820eaf0ec4440c9c9bfbead12db82f44d1bd4ad74472f6c6014673c25f62a29672902646e616d6502646672656458401264c85a04ce62806b7900b9cafd6f29434870bf61fa45cf0949cc4df7172439f2fc57ff32468fcaa2ef22f1cd89b25a331e0eea3e41c0cb57e35cf44a0dbe0c
```
- expected: **accept**

### TV-29 — name binding: Bob's sam is Dave's key; with TV-28, Alice's fred's sam is Dave (a compound name)

- signer: bob
- statement digest = SHA-256(TBS): `6d978fc48a64c39064c00b16b573839c102af3f0f9fb9a88d7cabfcf8d4c624f`
- TBS:
```
a60104020103582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f0482015820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c705a3011902310219029d031a02e3d1c006a10181a201a2015820eaf0ec4440c9c9bfbead12db82f44d1bd4ad74472f6c6014673c25f62a29672902646e616d65026373616d
```
- signature over DS ‖ TBS:
```
b10599f3e341febaa8bbd8b5ce321b12515250d08a9c72b1d6e2ea067457b94a7cd68d78e43a04cfeff8b5c4f049a60b9bdebb0af470f7812df0a85b4d16d40a
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
8401582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f5892a60104020103582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f0482015820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c705a3011902310219029d031a02e3d1c006a10181a201a2015820eaf0ec4440c9c9bfbead12db82f44d1bd4ad74472f6c6014673c25f62a29672902646e616d65026373616d5840b10599f3e341febaa8bbd8b5ce321b12515250d08a9c72b1d6e2ea067457b94a7cd68d78e43a04cfeff8b5c4f049a60b9bdebb0af470f7812df0a85b4d16d40a
```
- expected: **accept**

### TV-30 — name binding to a NAME target (SPEC-0002 §7.2 type 7): Carol's builder is Alice's fred's sam

- signer: carol
- statement digest = SHA-256(TBS): `e80919072666942c5328ab14f13d2029eb867dbf1b1e5b8db973121633c8b8e6`
- TBS:
```
a601040201035820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e207048307582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b98264667265646373616d05a3011902310219029d031a02e3dfd006a10181a201a2015820eaf0ec4440c9c9bfbead12db82f44d1bd4ad74472f6c6014673c25f62a29672902646e616d6502676275696c646572
```
- signature over DS ‖ TBS:
```
9921306044cff886eaf576229502fda724c4cd86a70f8419f4738ad361f4dcc27eb3757ca552113bba9c55a7b370db3a36c1034d7d03bb86ab8230c0f8e29f0a
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
84015820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e20758a0a601040201035820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e207048307582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b98264667265646373616d05a3011902310219029d031a02e3dfd006a10181a201a2015820eaf0ec4440c9c9bfbead12db82f44d1bd4ad74472f6c6014673c25f62a29672902646e616d6502676275696c64657258409921306044cff886eaf576229502fda724c4cd86a70f8419f4738ad361f4dcc27eb3757ca552113bba9c55a7b370db3a36c1034d7d03bb86ab8230c0f8e29f0a
```
- expected: **accept**

### TV-31 — trust to a NAME: Carol trusts Carol's builder about build-provenance in {reproducible}, one hop

- signer: carol
- statement digest = SHA-256(TBS): `0402e38ceccd94dc111ff890dbe991262158058e3ac16910af6ce616a3914984`
- TBS:
```
a601050201035820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e2070483075820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e20781676275696c64657205a3011902310219029d031a02e3ede006a10181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e636503816c726570726f64756369626c65
```
- signature over DS ‖ TBS:
```
15a85e030cd43758e18e930752af312c4e4cfa82334acef6a23d8404f7027b86196dcb1f2699030ce6aea88000c43e67dfc3d83f488053f2e7d26ddc31d1a70f
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
84015820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e20758b1a601050201035820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e2070483075820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e20781676275696c64657205a3011902310219029d031a02e3ede006a10181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e636503816c726570726f64756369626c65584015a85e030cd43758e18e930752af312c4e4cfa82334acef6a23d8404f7027b86196dcb1f2699030ce6aea88000c43e67dfc3d83f488053f2e7d26ddc31d1a70f
```
- expected: **accept**

### TV-32 — name binding: Bob's fred is Dave's key. It is in Bob's namespace, never Alice's

- signer: bob
- statement digest = SHA-256(TBS): `7967211024814b996de2c1756d40bb7e09533299edf5781ebc487bf08f062554`
- TBS:
```
a60104020103582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f0482015820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c705a3011902310219029d031a02e3fbf006a10181a201a2015820eaf0ec4440c9c9bfbead12db82f44d1bd4ad74472f6c6014673c25f62a29672902646e616d65026466726564
```
- signature over DS ‖ TBS:
```
f05bb70c2d0bd0372c0853fd6483b4e4ec81863e861e3cea88be8b0a076e84621cc0a279eb64ee6fc98488e0d199653da7a2afe61205f7c33918d2291136e403
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
8401582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f5893a60104020103582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f0482015820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c705a3011902310219029d031a02e3fbf006a10181a201a2015820eaf0ec4440c9c9bfbead12db82f44d1bd4ad74472f6c6014673c25f62a29672902646e616d650264667265645840f05bb70c2d0bd0372c0853fd6483b4e4ec81863e861e3cea88be8b0a076e84621cc0a279eb64ee6fc98488e0d199653da7a2afe61205f7c33918d2291136e403
```
- expected: **accept**

### TV-33 — name binding: Alice's loop is Alice's loop, a cycle

- signer: alice
- statement digest = SHA-256(TBS): `c0410cb0d0279cc9af2c2150f8d76c6e03fcd2fcc279f6c5743577f14c1a8311`
- TBS:
```
a60104020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9048307582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b981646c6f6f7005a3011902310219029d031a02e40a0006a10181a201a2015820eaf0ec4440c9c9bfbead12db82f44d1bd4ad74472f6c6014673c25f62a29672902646e616d6502646c6f6f70
```
- signature over DS ‖ TBS:
```
d4d2cf2126e72b3c041cd14a71ad66e1666255900aeb9aac61872d0faf2ec6a285e2e0ae442157a1dad9eba54e6f63ac0eca993e306f023fef91e34d2a042403
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
8401582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b95899a60104020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9048307582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b981646c6f6f7005a3011902310219029d031a02e40a0006a10181a201a2015820eaf0ec4440c9c9bfbead12db82f44d1bd4ad74472f6c6014673c25f62a29672902646e616d6502646c6f6f705840d4d2cf2126e72b3c041cd14a71ad66e1666255900aeb9aac61872d0faf2ec6a285e2e0ae442157a1dad9eba54e6f63ac0eca993e306f023fef91e34d2a042403
```
- expected: **accept**

### TV-34 — name binding: Alice's fred is also Dave's key; with TV-28, Alice's fred is the set {Bob, Dave}

- signer: alice
- statement digest = SHA-256(TBS): `9217aa27e60a61d1d07b54c3fbef2f09060f060e25626200c7dd5b3deebaa0e2`
- TBS:
```
a60104020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b90482015820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c705a3011902310219029d031a02e4181006a10181a201a2015820eaf0ec4440c9c9bfbead12db82f44d1bd4ad74472f6c6014673c25f62a29672902646e616d65026466726564
```
- signature over DS ‖ TBS:
```
2f339a835a529747b7fdb0582b467833215578bf0da2f82828f286c4b303c09b12b8095806c9c8a335393c54906d2b75acd5fa6f4f69b37dd46ac4aa89c0820a
```
- envelope `[suite, says, tbs, sig, ? pub]`:
```
8401582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b95893a60104020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b90482015820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c705a3011902310219029d031a02e4181006a10181a201a2015820eaf0ec4440c9c9bfbead12db82f44d1bd4ad74472f6c6014673c25f62a29672902646e616d6502646672656458402f339a835a529747b7fdb0582b467833215578bf0da2f82828f286c4b303c09b12b8095806c9c8a335393c54906d2b75acd5fa6f4f69b37dd46ac4aa89c0820a
```
- expected: **accept**

### Negative vectors

#### N-1 — reject at V5 canonical decode

TBS map keys are not in deterministic order; the signature over those bytes is valid.
```
8401582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b958a8a60104020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b906a10181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e6365026c726570726f64756369626c6504830201582048dfc39586b0c4f9e905b3b60f59a30b7c0c7408e44f7cb4df2a09fbf3e67ba705a30119022d02190261031a02de295058408712c0fb82a423a79da9d0e02676cf6426b343a6482af0c2ad9cb5cd28d5f89a15dbcfa18e7d7eeddf123225fcfaef8bfd143792495d75540393365e60558e0b
```

#### N-2 — reject at V4 signature

TBS altered after signing.
```
8401582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b958a8a60104020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b904830201582048dfc39586b0c4f9e905b3b60f59a30b7c0c7408e44f7cb4df2a09fbf3e67ba705a30119022d02190261031a02de295006a10181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e6365026c726570726f64756369626c6458408f30ee4ef039d81813703a2b629bb60e5abfc5b82a07432594a2add6fb77d24ccb9a41d744022af89e5ce0ead553131929e2f66fbd1c2ec1869b2c4c91319c0f
```

#### N-3 — reject at V6 outer/inner agreement

outer says (Bob) does not equal inner says (Alice).
```
8401582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f58a8a60104020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b904830201582048dfc39586b0c4f9e905b3b60f59a30b7c0c7408e44f7cb4df2a09fbf3e67ba705a30119022d02190261031a02de295006a10181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e6365026c726570726f64756369626c6558407a0fc00a0ced5c69f263838ccbed020ce1d22abe6a7059525e4afd3b2d3a04db2def0bfafa7a177e8f0fa4115168a6e59afbdd612dca81753d5709785222380f
```

#### N-4 — reject at V3 strict key check

public key is a small-order point (the identity); MUST be rejected before any verification.
```
8501582001d0fabd251fcbbe2b93b4b927b26ad2a1a99077152e45ded1e678afa45dbec55876a50101020103582001d0fabd251fcbbe2b93b4b927b26ad2a1a99077152e45ded1e678afa45dbec5048201582001d0fabd251fcbbe2b93b4b927b26ad2a1a99077152e45ded1e678afa45dbec506a101a20101025820010000000000000000000000000000000000000000000000000000000000000058400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000058200100000000000000000000000000000000000000000000000000000000000000
```

#### N-5 — reject at V4 strict signature

signature S >= L (malleated); MUST be rejected even though R and the equation may verify.
```
8401582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b958a8a60104020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b904830201582048dfc39586b0c4f9e905b3b60f59a30b7c0c7408e44f7cb4df2a09fbf3e67ba705a30119022d02190261031a02de295006a10181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e6365026c726570726f64756369626c6558408f30ee4ef039d81813703a2b629bb60e5abfc5b82a07432594a2add6fb77d24cb86e37345f653c5075f9d78db44df22d29e2f66fbd1c2ec1869b2c4c91319c1f
```

#### N-6 — reject at V5 canonical decode

TBS contains a floating-point value; outside the KSA data model.
```
8401582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9589ea60104020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b904830201582048dfc39586b0c4f9e905b3b60f59a30b7c0c7408e44f7cb4df2a09fbf3e67ba705a30119022d02190261031a02de295006a10181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e636502f93e005840b2b03f999c33b988e29f03162d44813dc36235f8de8cc002dd76f8fc7fbeccf9e864c20f591da1ea73df2c725f40df103ac50f3221d88a6e20127e409692230a
```

#### N-7 — reject at V8 threshold form

threshold form with k = 0, below the range 1 <= k <= n.
```
84015820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e20758f2a501050201035820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e20705a20119022d031a02de457006a30181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e636503826c726570726f64756369626c656861747465737465640383582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f5820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c704005840e5afe03d2043a28fda51207061180205753a72557f359347eb24d20e72ca2f377220b7aa4b8708920d4db739f8b5d24e0150f1867bc2577382fbddb3d80beb07
```

#### N-8 — reject at V8 threshold form

threshold form with k = 4 and n = 3, above the range 1 <= k <= n.
```
84015820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e20758f2a501050201035820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e20705a20119022d031a02de457006a30181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e636503826c726570726f64756369626c656861747465737465640383582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f5820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c704045840b5caaf21be163ea24292b129e95c3b83e01c362e7c8e85e1492e366f298f9763cc813c818e95486630f7c98817e7c7261b0b70123cda1ead58ba37d72130b50d
```

#### N-9 — reject at V7 closed map

n = 4 beside three members needs a body field that does not exist; closed map.
```
84015820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e20758f4a501050201035820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e20705a20119022d031a02de457006a40181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e636503826c726570726f64756369626c656861747465737465640383582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f5820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c704020504584022e6d05d2836fd93c315e8ad87c664bee502a819497cf3da00e4658d968face5ec04d890a7afb81952dad9b24af8eb9e7329a2f14929e5db68874b17cdc2fd06
```

#### N-10 — reject at V5 canonical decode

the array head of trusts says n = 4 and three members follow; not well-formed CBOR, correctly signed.
```
84015820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e20758f2a501050201035820c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e20705a20119022d031a02de457006a30181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e636503826c726570726f64756369626c656861747465737465640384582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9582039f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f5820d5f0b21718b21f79648f7f4a0325288209e6fd37fa2f90f9d29c4229e371f8c704025840d246f570ca29eae769b4ac250659a76cd5505bc5024542cbd2e3f93d8e499d84cbdaecf5af95e7253761325cb9ecb4e633353d20e8104c2f8a20c9d2a15b8d00
```

#### N-11 — reject at V7 structure

attestation whose target is a bare locator [5, uri]; target type 5 is reserved, so no digest is bound.
```
8401582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b958b3a60104020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9048205782c68747470733a2f2f6578616d706c652e6f72672f72656c65617365732f64656d6f2d312e302e7461722e677a05a30119022d02190261031a02de295006a10181a201a2015820517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a717502706275696c642d70726f76656e616e6365026c726570726f64756369626c655840952ede3f1f82c70ee53a5e557691e652496e225771b5d5187a8e9035d395f94eb80087ca38ed9cfd7b7f2126f7f7ca9b9291fa245407135cd415aa2a89302606
```

#### N-12 — reject at V7 structure

name target with an empty label list; a name has at least one label.
```
8401582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b95894a60104020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9048307582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b98005a3011902310219029d031a02e3c3b006a10181a201a2015820eaf0ec4440c9c9bfbead12db82f44d1bd4ad74472f6c6014673c25f62a29672902646e616d650264667265645840f850366037232cb46abaf3347a091366a2a99319ace847f6d5d2f8943dd948e27787ede500aaef4d0b908998964850ae219feb6dde070456414aa2c17d99de0b
```

#### N-13 — reject at V7 structure

name target whose label "Fred" is outside [a-z][a-z0-9-]{0,62}.
```
8401582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b95899a60104020103582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9048307582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b981644672656405a3011902310219029d031a02e3c3b006a10181a201a2015820eaf0ec4440c9c9bfbead12db82f44d1bd4ad74472f6c6014673c25f62a29672902646e616d6502646672656458406b2798887a415afd4bfd34b4e70e7b2e4855c8e587b9c3fafbdb949106636742e9b8006871a6e2724b81087ac8cb620d64294afa54b8c140844c3054a78dc906
```

### Delegation evaluations (SPEC-0004 Appendix A)

Anchor TV-5 in context `releases`; ask: is the artifact's build-provenance the value shown, at 2026-10-10T12:00:00Z.

| eval | statements | value | answer | reason | at |
|---|---|---|---|---|---|
| E-1 | TV-14, TV-15 | attested | **no** | widening | TV-14 |
| E-2 | TV-16, TV-17 | reproducible | **yes** | — | — |
| E-3 | TV-16, TV-18, TV-19 | reproducible | **no** | depth | TV-18 |
| E-4 | TV-20, TV-17 | reproducible | **no** | widening | TV-20 |

### Archives evaluations (ARCH-0001 §2.3.2; UC-3)

Anchor TV-22 in context `library`; ask: does the subject have `reviewed` = the value shown, at 2026-10-15T12:00:00Z. `record` is the digest target `sha-256:` of the record; `work` is TV-26's description target.

| eval | statements | subject | value | answer | reason | at |
|---|---|---|---|---|---|---|
| E-5 | TV-23, TV-25 | record | partial | **yes** | — | — |
| E-6 | TV-23, TV-24 | record | yes | **no** | no-path | TV-24 |
| E-7 | TV-26 | work | yes | **yes** | — | — |

### Name resolutions (SPEC-0004 §5.3; mofn#143)

DV-4 held; every statement listed is in the statement set, at 2026-10-10T12:00:00Z.

| res | name | statements | keys | reason | case |
|---|---|---|---|---|---|
| R-1 | alice's fred | TV-28 | bob | — | one hop |
| R-2 | alice's fred sam | TV-28, TV-29 | dave | — | a compound name: Alice's fred is Bob, Bob's sam is Dave |
| R-3 | carol's builder | TV-30, TV-28, TV-29 | dave | — | a binding to a name: Carol's builder is Alice's fred's sam |
| R-4 | alice's fred | TV-28, TV-34 | bob, dave | — | two bindings of one label: the name is a set (SDSI group), not an error |
| R-5 | alice's fred sam | TV-28 | ∅ | name-unresolved | missing link: Bob binds no sam |
| R-6 | alice's loop | TV-33 | ∅ | name-cycle | Alice's loop is defined as itself |
| R-7 | alice's fred | TV-32 | ∅ | name-foreign | the only fred binding is Bob's; Bob cannot bind a label in Alice's namespace |

### Name evaluations (SPEC-0004 Appendix A)

Anchor TV-31 (Carol's own trust to Carol's builder) in context `releases-by-name`; ask: is the artifact's build-provenance the value shown, at 2026-10-10T12:00:00Z.

| eval | statements | value | answer | reason | at |
|---|---|---|---|---|---|
| E-8 | TV-30, TV-28, TV-29, TV-19 | reproducible | **yes** | — | — |
| E-9 | TV-30, TV-28, TV-19 | reproducible | **no** | name-unresolved | TV-31 |
| E-10 | TV-30, TV-28, TV-29, TV-17 | reproducible | **no** | no-path | TV-17 |
<!-- VECTORS:END -->

## Appendix B. CDDL

```cddl
signed-statement = [
  suite: suite-code,
  says: kid,
  tbs: bstr .cbor statement,          ; the octets exactly as signed
  sig: bstr,
  ? pub: bstr                         ; unauthenticated; REQUIRED for key-publish
]

statement = {
  1 => kind-code,
  2 => suite-code,
  3 => kid,                           ; says
  ? 4 => target,                      ; this
  ? 5 => validity,
  6 => body
}

kind-code  = 1..11
suite-code = uint
kid        = bstr .size 32
digest     = bstr .size 32
definition-id = bstr .size 32
time       = int

target = [1, kid]                        ; key
       / [2, digest-alg, bstr]           ; object digest
       / [3, digest]                     ; statement
       / [4, definition-id]              ; definition
                                         ; 5: reserved (locator, withdrawn 0.6.0)
       / [6, type-ref, value]            ; description
       / [7, kid, [1*16 name-label]]     ; name (0.9.0)
digest-alg = 1..3
name-label = tstr .regexp "[a-z][a-z0-9-]{0,62}"

validity = { ? 1 => time, ? 2 => time, ? 3 => time }   ; not-before, not-on-or-after, issued

type-ref        = { 1 => definition-id, 2 => label }
process-ref     = { 1 => definition-id, 2 => label }
label           = tstr
attribute       = { 1 => type-ref, 2 => value }
attribute-range = { 1 => type-ref, ? 3 => value }

value = int / bool / bstr / tstr / [* value] / { * tstr => value }

public-key = { 1 => key-alg, 2 => bstr }
key-alg    = 1 / 2 / 8

body = key-publish-body / self-body / speaks-body / attestation-body / trust-body
     / revoke-body / rotate-body / define-body / review-body / approve-body / aggregate-body

key-publish-body = { 1 => public-key }
self-body        = { ? 1 => public-key, ? 2 => tstr, ? 3 => [+ uint], ? 4 => time, ? 5 => uint }
speaks-body      = { 1 => [+ definition-id] }
attestation-body = { 1 => [+ attribute], ? 3 => type-ref }        ; 3: template
trust-body       = { 1 => [+ attribute-range], ? 2 => delegation-constraints,
                     ? 3 => [2* kid], ? 4 => uint }
delegation-constraints = { ? 1 => uint, ? 2 => [+ attribute-range],
                           ? 3 => [+ kid], ? 4 => [+ kid], ? 5 => time }
revoke-body      = { 1 => digest }
rotate-body      = { ? 1 => tstr }
define-body      = { 1 => tstr, 2 => tstr, ? 3 => definition-id }  ; 3: supersedes
review-body      = { 1 => [+ attribute], ? 2 => tstr, ? 3 => type-ref }
approve-body     = { ? 1 => [+ attribute], ? 2 => tstr, ? 3 => type-ref }
aggregate-body   = { 1 => process-ref, 2 => [+ digest], 3 => bool }
```

The CDDL describes structure. The kind-specific constraints of §8 and the
encoding rules of §4 are additional and normative.

