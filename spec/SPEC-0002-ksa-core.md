---
schema: "archdoc/v1"
id: SPEC-0002
title: "KSA Core — statements, data model, canonical encoding and cipher suites"
short_title: "KSA Core"
description: "The KSA statement: its data model, deterministic encoding, signed envelope, cipher suites, statement kinds, and the procedure for verifying one statement."
type: specification
category: security
status: draft
version: "0.2.0"
version_policy: "semver; MAJOR = any change to signed or hashed bytes; MINOR = additive registry entries or requirements; PATCH = editorial"
date: "2026-10-14"
updated: "2026-10-25"
decision_makers:
  - role: sponsor
    id: paul-lambert
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

**Specification SPEC-0002 · version 0.1.0 · draft**

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
signed or hashed bytes change. Nothing in this draft is final until its version leaves `0.x`.

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

A cipher suite is an immutable registry entry (§12.3). Each entry MUST define:

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
  torsion subgroup, including the identity).
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
| 5 locator | `[5, text]` | a resource identified by a URI; weaker than a digest, and SHOULD be used only where no digest exists |
| 6 description | `[6, type-ref, value]` | something identified by a typed description — the description's canonical encoding is its identity |

Subjects are not limited to keys: a statement can concern a release, a record,
a definition, or another statement.

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
| 5 | `trust` | `[1, kid]`, or absent in the threshold form | extend trust to a key about a range of attributes |
| 6 | `revoke` | MUST be `[1, says]` | withdraw one of the speaker's own statements |
| 7 | `rotate` | `[1, new-kid]`, not equal to `says` | name the speaker key's successor |
| 8 | `define` | MUST be `[4, DefinitionId]` | publish a definition, as its author |
| 9 | `review` | `[3, statement-digest]` or `[2, …]` | give an opinion on a statement or object |
| 10 | `approve` | `[3, statement-digest]` or `[2, …]` | authorise a statement or object |
| 11 | `aggregate` | any target except `[1, …]` | the result of a published process (SPEC-0005) |

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

The speaker extends trust to a key about a range of attributes. In the
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
tool converts between the two **one-to-one**:

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
- Byte strings are quoted text: `'0x'` followed by lowercase hexadecimal.
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

<!-- VECTORS:BEGIN -->
<!-- generated by spec/vectors/ksa-core/generate.py — do not edit by hand -->

### Keys

| name | seed | public key | kid = SHA-256(pub) |
|---|---|---|---|
| alice | `9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60` | `d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a` | `21fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9` |
| bob | `4ccd089b28ff96da9db6c346ec114e0f5b8a319f35aba624da8cf6ed4fb8a6fb` | `3d4017c3e843895a92b70aa74d1b7ebc9c982ccf2ec4968cc0cd55f12af4660c` | `39f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f` |
| carol | `94f0d20c5f4157e44463f03fae4d9c93c59da7c42af17014481faf7ab80c5009` | `be2809c0673894dc058c0f06f32d870c2a95b671d9df62074fcb19c0c203bf6b` | `c7b66369c87c115e8f8ab2fd27540d1a8a28cc475aab29b58ba0caf47910e207` |
| bob2 | `cfe6d5ee21b7bf722007ceb061436f23285c43dd9366d51d5d9cd978be007061` | `05da6bf466928fa468b1ecb00413a356c33502b70dc0620020fe98315cd1dfd8` | `9dcd2b600a6996b68623f46e19c60b6eb076c4a707df022e8479ef1d191b91f6` |

Domain-separation label (hex): `4b53412d53544d542d5349472d763100`

### DV-1 — definition `supply-chain` v1, definer Alice

DefinitionId = SHA-256(body) = `517007656a617b3b5ab7cc376275a46ad88d14594f6846df88a34f2c8b3a7175`

```
a401582021fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9026c737570706c792d636861696e03613105838201a701706275696c642d70726f76656e616e6365020103a262656e704275696c642070726f76656e616e6365626573781e50726f636564656e636961206465206c6120636f6d70696c616369c3b36e04a262656e781b486f772074686520617274696661637420776173206275696c742e626573781f43c3b36d6f20736520636f6d70696cc3b320656c2061727465666163746f2e0683a3016c726570726f64756369626c6502a262656e6c526570726f64756369626c656265736c526570726f64756369626c6503a262656e78296275696c7420726570726f64756369626c792066726f6d207075626c697368656420736f75726365736265737838636f6d70696c61646f20646520666f726d6120726570726f64756369626c65206465736465206675656e746573207075626c696361646173a30168617474657374656402a162656e68417474657374656403a162656e781d6275696c7420627920616e20617474657374656420706970656c696e65a3016a756e766572696669656402a162656e6a556e766572696669656403a162656e736f726967696e206e6f7420766572696669656408020981a2016a70726f76656e616e636502a162656e782e446f6573207468652070726f76656e616e6365206e616d6520746865206578706563746564206275696c6465723f8201a601676f7574636f6d65020103a162656e6e526576696577206f7574636f6d6504a162656e781a57686174206120726576696577657220636f6e636c756465642e0683a30167617070726f766502a162656e67417070726f766503a162656e7819726561647920746f207075626c697368206173206275696c74a301676368616e67657302a162656e6f52657175657374206368616e67657303a162656e78196e6f742072656164793b206368616e676573206e6565646564a3016672656a65637402a162656e6652656a65637403a162656e756d757374206e6f74206265207075626c697368656408008202a7017372656c656173652d6174746573746174696f6e020403a10181020481a201a102706275696c642d70726f76656e616e636502f5051a00278d0008a262656e78327b736179737d20617474657374732074686174207b746869737d20776173207b6275696c642d70726f76656e616e63657d2e62657378337b736179737d2061746573746967756120717565207b746869737d20667565207b6275696c642d70726f76656e616e63657d2e09a162656e7352656c65617365206174746573746174696f6e
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
       / [5, tstr]                       ; locator (URI)
       / [6, type-ref, value]            ; description
digest-alg = 1..3

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

