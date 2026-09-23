---
schema: "archdoc/v1"
id: RPT-0001
title: "CBOR: what a complete implementation requires, and the ecosystem around it"
short_title: "CBOR"
description: "Survey of the CBOR specification surface, the determinism problem, the open-source landscape, and the markets and bodies that drive adoption. Evidence for DEC-002 and R-M-12; it does not select an encoding."
type: research
category: encoding
status: draft
version: "0.1.0"
date: "2026-09-22"
updated: "2026-09-22"
decision_makers:
  - role: sponsor
    id: paul-lambert
reviewers: []
needs_review: true
reviewed: false
canonical_path: research/0001-cbor/report.md
library_commit: "see library/ submodule pointer at time of merge"
informs: [DEC-002, DEC-003, DEC-005, R-M-07, R-M-12]
open_decisions: [DEC-002, DEC-003, DEC-005]
---

# CBOR: what a complete implementation requires, and the ecosystem around it

> **This report does not select an encoding.** DEC-002 is open, and
> `CLAUDE.md` forbids documents that assume a selection. What follows is
> evidence: the specification surface an implementer must cover, where the
> standards actually disagree, what code exists, and who controls the
> extension points. The one place it touches a decision directly is R-M-12,
> where CBOR's tag registry is the concrete instance of the problem ADR-0001
> already settled in principle.

## 1. Summary

Five findings, in order of how much they should change what we do.

1. **"Deterministic CBOR" is not one thing.** At least four incompatible
   profiles are in production: RFC 8949 §4.2.1, RFC 8949 §4.2.3 (length-first),
   CTAP2 canonical CBOR, and DAG-CBOR — with dCBOR a fifth. They disagree on
   map-key sort order, on whether floats may be shortened, and on whether tags
   may appear at all. A specification that says "use deterministic CBOR" has
   not specified an encoding. §3.
2. **The IETF's live determinism document is not the one most write-ups
   cite.** `draft-ietf-cbor-cde-13` (Common Deterministic Encoding) **expired
   2026-04-17**; `draft-ietf-cbor-packed-19` expired 2026-08-06. The live WG
   work is `draft-ietf-cbor-serialization-08`, current to 2027-01-30. Verified
   against the datatracker API on 2026-09-22. §3.
3. **CBOR's extension point is an IANA registry, which is exactly the shape
   R-M-12 rules out.** This is a constraint on the *profile*, not an argument
   against the data model: the tag mechanism is separable, which is what "a
   reduced CBOR profile" means. §6.
4. **Determinism is not a default in the libraries.** QCBOR v1.x does not sort
   map keys on encode; kotlinx-serialization-cbor defaults to indefinite-length
   encoding. "RFC 8949 compliant" tells you nothing about whether a library can
   emit the bytes you intend to sign. §5.
5. **CBOR's footholds were assigned by standards bodies, not won
   competitively.** Where CBOR is mandated — ISO mdoc, FIDO CTAP2, COSE/EAT —
   it is entrenched by regulation and certification. Where the choice is free,
   it is generally losing to protobuf. §7.

## 2. The implementable surface

51 records were ingested into `library/` (§10). The spec surface splits into
four tiers:

| Tier | What | Records |
|---|---|---|
| Core | RFC 8949 (STD 94) + the CDDL line (8610, 9165, 9682, 9741) + sequences (8742) + stable storage (9277) + diagnostic notation | 10 |
| Determinism | serialization / CDE / dCBOR | 3 |
| Extension points | IANA tag + simple-value registries, and the six tag RFCs | 8 |
| Signing layer | COSE (STD 96: 9052 + 9338) + algorithms + CWT + receipts | 13 |

Two structural facts worth carrying:

- **RFC 9052 and RFC 9338 together are STD 96 — a full Internet Standard.**
  RFC 9053 (Initial Algorithms) and RFC 9054 (Hash Algorithms) stayed
  **Informational** and are *not* part of STD 96. A claim of "COSE standards
  compliance" should say which.
- **RFC 9864 (Oct 2025) updates RFC 9053** to remove polymorphic algorithm
  identifiers. Anything implementing RFC 9053 today must apply it.

## 3. The determinism problem

This is the finding that matters most for a project whose object is a signed
statement. RFC 8949 §4.2 defines deterministic encoding as an *option a
protocol selects and further constrains*, and the gap it leaves has been filled
incompatibly.

| Rule | RFC 8949 §4.2.1 | §4.2.3 length-first | CTAP2 canonical | dCBOR |
|---|---|---|---|---|
| Map key sort | bytewise-lexicographic on encoded key | length, then lexical | **major type**, then length, then lexical | inherits §4.2.1 |
| Float shortening | MUST use shortest form preserving value | same | **prohibited** — width is part of the value | stronger: floats numerically equal to an integer reduce *to* the integer |
| Tags | permitted; protocol must fix presence per position | same | **banned outright** | no blanket ban |
| Indefinite lengths | MUST NOT appear | MUST NOT appear | must be converted to definite | inherits |
| Duplicate keys | well-formed but invalid; protocol decides | same | encoders MUST NOT emit; decoders SHOULD reject | MUST reject, both sides |
| NaN | advisory: pick one pattern | same | not shortened at all | MUST reduce to `0xf97e00` |

CTAP2's float-shortening prohibition and its blanket tag ban are
**unconditional** divergences: point a generic RFC 8949 canonical encoder at
CTAP2 traffic and it breaks immediately. The map-key sort divergence is latent
— CTAP2 never uses complex-typed map keys today, so the extra major-type tier
coincides with §4.2.1 over CTAP2's actual keyspace — and will surface only if
an extension introduces one, or if a library is reused across both contexts
without a mode switch.

**Document status, verified against the datatracker API on 2026-09-22:**

| Document | Rev | State | Expires |
|---|---|---|---|
| `draft-ietf-cbor-serialization` | -08 | active, WGLC | 2027-01-30 |
| `draft-ietf-cbor-cde` | -13 | **expired**, parked | 2026-04-17 |
| `draft-mcnally-deterministic-cbor` (dCBOR) | -18 | active, **individual** — no IETF stream, no WG standing | 2027-02-11 |
| `draft-ietf-cbor-packed` | -19 | **expired** | 2026-08-06 |

Two corrections to the common account, both verified in the source text
(§9):

- `draft-ietf-cbor-serialization-08` **does not mention CDE at all** and makes
  no claim to replace it. It defines "preferred-plus serialization" and
  "deterministic serialization" over RFC 8949. Our record therefore links the
  two with `see_also`, not `supersedes` — the WG has not said it replaces CDE.
- **dCBOR at -18 does not mention CDE either.** Secondary accounts describe
  dCBOR as "layered on CDE without forking it"; that was true of earlier
  revisions. At -18 it narrows **RFC 8949 §4.2 directly**, and its normative
  references are the IANA registries, IEEE 754 and RFC 2119.

The practical consequence for DEC-002: if a reduced CBOR profile is pursued,
the profile must state its determinism rules *itself* rather than cite
"deterministic CBOR", and it should target RFC 8949 §4.2.1 plus explicit
choices on tags, floats and NaN — because the document that would have
supplied those choices as a package is expired.

## 4. Implementer's completeness checklist

What a production-grade implementation has to get right, beyond parsing the
major types. Each line is a place real implementations have failed.

**Encoding correctness**
- Shortest-form integer, length and tag encoding.
- Half-precision (binary16) codec, including ±Infinity and NaN in 16-bit form.
- Bignum tags 2/3, with fallback to native ints when the value fits.
- Text vs byte-string discipline (major type 2 vs 3), no silent coercion.
- Tag validity: admissible content type and value per tag.

**Determinism**
- Bytewise-lexicographic map-key sort **on the encoded key**.
- The length-first variant (§4.2.3) for legacy interop.
- Suppression of indefinite lengths under a deterministic mode.
- NaN canonicalisation to a single bit pattern.
- A byte-exact "keep original bytes" round-trip mode — re-encoding a parsed
  model can silently change bytes and invalidate a signature. Cardano does not
  enforce canonical encoding at the ledger, which makes this load-bearing
  there.

**Structure**
- Indefinite-length arrays, maps and strings with `break`.
- Rejection of nested indefinite-length string chunks (§3.2.3).
- `bstr`-wrapping / tag 24 embedded CBOR — the COSE protected header, the mdoc
  MSO and the C2PA claim signature all depend on it.
- CBOR Sequences (RFC 8742) decode mode: one item, no error on trailing bytes.

**Security — every one of these has a shipped CVE behind it**
- Bounded recursion/nesting depth. *CVE-2026-26209* (Python `cbor2`,
  uncontrolled recursion, sub-100KB payload crashes a worker, fixed 5.9.0);
  *CVE-2025-24302* / *CVE-2025-20025* (TinyCBOR, fixed 0.6.1+);
  *RUSTSEC-2019-0025* (`serde_cbor` stack overflow). CTAP2 mandates exactly 4
  levels.
- 64-bit length fields must not overflow `size_t` on 32-bit targets.
- Duplicate map key detection with documented behaviour. Divergent handling is
  a parser-differential bug class: the signature covers one interpretation and
  the business logic uses another.
- Decoder state must not leak across calls. *CVE-2025-68131* (`cbor2`): the
  tag 28/29 shareable-reference table was not cleared between decodes on a
  reused decoder, leaking values from an earlier message across a trust
  boundary.
- The full non-well-formedness taxonomy of RFC 8949 Appendix F.

**Schema and tooling**
- CDDL (RFC 8610) *with* RFC 9682's grammar corrections, plus the 9165 and
  9741 control operators.
- Diagnostic notation / EDN for test vectors and debugging.

## 5. Open source

| Language | Default to reach for | Caveat |
|---|---|---|
| Go | `fxamacker/cbor` v2.9.2, MIT | Ships both Core Deterministic and a CTAP2-canonical preset — rare. Public NCC Group assessment. |
| Python | `agronholm/cbor2` v6.1.4, MIT | Native backend moved **C → Rust**; building from source now needs a Rust toolchain. Two fixed CVEs. |
| Rust | `ciborium` or `minicbor` | **`serde_cbor` is deprecated and unpatched** (RUSTSEC-2021-0127, repo archived). |
| C (constrained) | QCBOR, NanoCBOR, TinyCBOR, libcbor | QCBOR v1.x **does not sort map keys on encode**. TinyCBOR carries two fixed recursion CVEs. |
| C (schema-driven) | `zcbor`, Apache-2.0 | The most production-grade CDDL consumer found: generates C from CDDL. Embedded-C scope only. |
| .NET | `System.Formats.Cbor` (BCL) | Low-level reader/writer with conformance modes; no object mapping. |
| JVM | `jackson-dataformat-cbor` | Not CDDL- or COSE-aware. |
| JS | `cbor2` (npm, hildjj) or `cbor-x` | `cbor-x`'s optional native addon had a heap over-read reachable through `fido2-lib`'s WebAuthn path (GHSA-g3qj-j598-cxmq), fixed 1.6.3. |
| Swift, Erlang/Elixir | — | **No default exists.** Swift is fragmented across 4+ forks; Erlang/Elixir has three small packages, none dominant. |

Three ecosystem-level gaps:

- **CDDL tooling is the weakest link.** The most-used Rust CDDL validator
  self-describes as "a personal learning exercise". `zcbor` is solid but
  embedded-C only. WP1 should not assume mature tooling exists.
- **No shared cross-language fuzz corpus or adversarial vector suite.**
  Conformance testing mostly stops at RFC 8949's small, well-formed Appendix A
  vectors — which is precisely the gap the TinyCBOR and `cbor2` recursion CVEs
  fell into.
- **Packed CBOR has essentially one real implementation** (`cbor-x`, JS), and
  its draft is expired.

## 6. Extension points and who controls them

CBOR's extensibility is delegated to IANA registries: **CBOR Tags** and
**CBOR Simple Values**, plus the COSE registries for the signing layer. Both
CBOR registries are held as `dataset` records with digests.

This is the concrete instance of **R-M-12**. ADR-0001 settled the principle —
native extension points must be key-relative, not registry-dependent — and
CBOR's tag mechanism is the archetype of what that rules out. Two observations
that matter for how the constraint is applied:

- **The registry is separable from the data model.** Maps, arrays, strings and
  integers carry no registry dependence. A profile that excludes tags gets
  CBOR's data model without CBOR's naming authority. This is what the
  2026-09-22 direction's "reduced CBOR profile" appears to mean, and the
  research supports that it is coherent.
- **Tag 24 is the awkward case.** `bstr`-wrapped embedded CBOR is a registry
  code point, and it is structurally required by COSE's protected header. A
  profile that bans all tags cannot use COSE as specified. DEC-005 and R-M-12
  interact here and the interaction is not yet written down anywhere.

Governance, ranked by actual influence over CBOR: IETF CBOR WG and the IANA
registries (free, low barrier, a handful of overlapping designated experts);
then the IETF COSE/RATS/ACE/CoRE/SCITT WGs; then ISO/IEC JTC1/SC17 for mdoc —
**paywalled** (18013-5 at CHF 227/part) and reachable only through national
bodies, which is a poor fit for a library that does not redistribute bytes;
then FIDO (specs free, influence dues-gated).

## 7. Markets and applications

CBOR has no market of its own; it rides the systems that mandate it.

| Domain | Driver | Evidence strength |
|---|---|---|
| EU Digital Identity / mDL | Reg. (EU) 2024/1183: in force 20 May 2024; member states must offer a wallet ~24 Dec 2026; obligated relying parties must accept by Nov 2027. ISO 18013-5 mandates CBOR + COSE. | **Strongest** — primary regulation, explicit mandate |
| FIDO2 / passkeys | CTAP2 mandates canonical CBOR | Strong |
| Cardano | CBOR/CDDL *is* the ledger encoding | Strong on mechanism; no market sizing applies |
| RATS / EAT / confidential computing | EAT is a CWT (RFC 9711); Arm CCA/PSA and AWS Nitro use CBOR/COSE | Strong on standards, weak on sizing |
| C2PA | Claims and most assertions are deterministic CBOR in JUMBF boxes | Good on mechanism, weak on usage numbers |
| IoT | LwM2M uses SenML-CBOR; OCF mandates CBOR | Mixed |
| Automotive telemetry | — | **Weakest** — protobuf is the incumbent |

**Where CBOR loses:** gRPC/microservices (protobuf outright), connected-vehicle
telemetry, big-data pipelines (Avro/Parquet), legacy PKI and telecom
(ASN.1/DER entrenched), browser-facing APIs (JSON+JWS by inertia), real-time
and gaming (FlatBuffers/Cap'n Proto for zero-copy).

**Corrections to claims commonly made about CBOR** — each checked against a
primary source and each a trap for a report that repeated the received view:

- **Matter (CSA) does not use CBOR.** It has its own TLV encoding. This is the
  most frequent conflation in the space.
- **Intel TDX and AMD SEV-SNP attestation are not CBOR** — proprietary fixed
  binary structures. Arm CCA/PSA and AWS Nitro *are* CBOR/COSE.
- **in-toto/DSSE is JSON**, not CBOR (`application/vnd.in-toto+json`), despite
  being lumped in with SCITT/COSE tooling. We hold a DSSE record already.
- **Android's core hardware key attestation is ASN.1/DER in X.509**, not CBOR.
- **IOTA's ledger uses a bespoke "packable" format**, not CBOR.
- **AUTOSAR and Uptane: no confirmed CBOR use.**

Market-size figures in this space are unreliable and are recorded as such in
`sources.md`: confidential-computing estimates span $5.7B–$54B across analysts
(~10× disagreement), and the passwordless figures span $16.85B–$27.66B with no
shared methodology. None is cited as fact here.

## 8. What this bears on

| Decision | What the research supplies | What it does **not** do |
|---|---|---|
| **DEC-002** encoding | The full cost of "implement CBOR completely" (§4); the determinism gap a profile must close itself (§3); library maturity per language (§5) | Does not select option 2, or any option |
| **DEC-003** identifiers | RFC 9679 (COSE Key Thumbprint) specifies canonical key bytes before hashing — the thing DEC-003 says must be specified | Does not choose an identifier form |
| **DEC-005** envelope | COSE_Sign1 is STD 96; receipts (RFC 9942) and hash envelope (RFC 9995) now exist as standards-track | Does not choose between DSSE and COSE_Sign1 |
| **R-M-12** | The IANA tag registry as the concrete instance; the tag-24/COSE interaction as an unresolved corner (§6) | — |
| **R-M-07** | RFC 9054 supplies COSE hash algorithm identifiers; RFC 9995 supplies detached-payload digest signing | — |

## 9. Method, and where it is weak

Six parallel agents surveyed specifications, open source, products, markets,
applications and consortiums. Their outputs were not taken at face value:
every specification identifier in this report was re-verified by the author
against `rfc-editor.org/rfc-index.txt` (index of 2026-09-21) and the
datatracker API, and three substantive agent claims were **rejected**:

1. That `draft-ietf-cbor-serialization` supersedes CDE — the draft makes no
   such claim; `grep -ci cde` over `-08` returns 0. Downgraded to `see_also`.
2. That dCBOR is "layered on CDE" — not true at `-18`; CDE appears nowhere in
   it. Corrected to: narrows RFC 8949 §4.2 directly.
3. That RFC 9165 and RFC 9741 formally "Update" RFC 8610 — the RFC index shows
   only RFC 9682 with an Updates relation. Recorded as `see_also`.

Known weaknesses, in descending order of how much they should worry a reader:

- **Search queries were not archived verbatim.** `research/README.md` rule 2
  requires it, and this pass does not meet it: agents recorded sources and
  retrieval dates but not the queries that produced them. `searches.md`
  records what is reconstructable and marks the rest as a gap. This is a real
  process failure, not a footnote — it is the exact failure
  `docs/construction.md` was written about.
- **No record here is `summarized`.** 51 records are at `fetched` — digested
  and assessed, not read. Only `rfc-8949` was taken to `read`, and its own
  Limits section states what was not read (Appendix F).
- **ISO 18013-5 is paywalled** and was assessed only through secondary
  sources. Any claim about mdoc's normative CBOR usage in this report is
  second-hand.
- **JPEG Trust's normative encoding could not be confirmed** from a primary
  source; do not assume it inherits C2PA's CBOR-in-JUMBF.
- **Market figures** are analyst estimates, flagged in `sources.md`, and none
  is load-bearing for any conclusion above.

## 10. Bibliography

51 records ingested into `library/` on 2026-09-22, under topics
`cbor-implementation`, `canonical-encoding` and `cbor-ecosystem`. Every record
carries a sha-256 of the retrieved bytes; per library policy no third-party
document is committed.

#### A. CBOR core and CDDL — the encoding itself

| record | title | type | maturity | date | verdict |
|---|---|---|---|---|---|
| [`rfc-8949`](https://www.rfc-editor.org/rfc/rfc8949.txt) | Concise Binary Object Representation (CBOR) | rfc | standard | 2020-12 | useful |
| [`rfc-7049`](https://www.rfc-editor.org/rfc/rfc7049.txt) | Concise Binary Object Representation (CBOR) | rfc | standard | 2013-10 | marginal |
| [`rfc-8610`](https://www.rfc-editor.org/rfc/rfc8610.txt) | Concise Data Definition Language (CDDL): A Notational Convention to… | rfc | standard | 2019-06 | useful |
| [`rfc-9165`](https://www.rfc-editor.org/rfc/rfc9165.txt) | Additional Control Operators for the Concise Data Definition Langua… | rfc | standard | 2021-12 | useful |
| [`rfc-9682`](https://www.rfc-editor.org/rfc/rfc9682.txt) | Updates to the Concise Data Definition Language (CDDL) Grammar | rfc | standard | 2024-11 | useful |
| [`rfc-9741`](https://www.rfc-editor.org/rfc/rfc9741.txt) | Concise Data Definition Language (CDDL): Additional Control Operato… | rfc | standard | 2025-03 | useful |
| [`rfc-8742`](https://www.rfc-editor.org/rfc/rfc8742.txt) | Concise Binary Object Representation (CBOR) Sequences | rfc | standard | 2020-02 | useful |
| [`rfc-9277`](https://www.rfc-editor.org/rfc/rfc9277.txt) | On Stable Storage for Items in Concise Binary Object Representation… | rfc | standard | 2022-08 | useful |
| [`draft-ietf-cbor-edn-literals`](https://www.ietf.org/archive/id/draft-ietf-cbor-edn-literals-27.txt) | Concise Diagnostic Notation (CDN) | draft -27 | draft | 2026-07-20 | useful |
| [`draft-ietf-cbor-cddl-modules`](https://www.ietf.org/archive/id/draft-ietf-cbor-cddl-modules-07.txt) | CDDL Module Structure | draft -07 | draft | 2026-09-02 | useful |

#### B. Determinism and canonical form

| record | title | type | maturity | date | verdict |
|---|---|---|---|---|---|
| [`draft-ietf-cbor-serialization`](https://www.ietf.org/archive/id/draft-ietf-cbor-serialization-08.txt) | CBOR Serialization and Determinism | draft -08 | draft | 2026-07-30 | useful |
| [`draft-ietf-cbor-cde`](https://www.ietf.org/archive/id/draft-ietf-cbor-cde-13.txt) | CBOR Common Deterministic Encoding (CDE) | draft -13 | draft | 2026-04-16 | marginal |
| [`draft-mcnally-deterministic-cbor`](https://www.ietf.org/archive/id/draft-mcnally-deterministic-cbor-18.txt) | dCBOR: Deterministic CBOR | draft -18 | draft | 2026-08-10 | marginal |

#### C. Tag extension points — the R-M-12 evidence set

| record | title | type | maturity | date | verdict |
|---|---|---|---|---|---|
| [`iana-cbor-tags`](https://www.iana.org/assignments/cbor-tags/cbor-tags.xhtml) | IANA Concise Binary Object Representation (CBOR) Tags Registry | dataset | — |  | useful |
| [`iana-cbor-simple-values`](https://www.iana.org/assignments/cbor-simple-values/cbor-simple-values.xhtml) | IANA Concise Binary Object Representation (CBOR) Simple Values Regi… | dataset | — |  | useful |
| [`rfc-8746`](https://www.rfc-editor.org/rfc/rfc8746.txt) | Concise Binary Object Representation (CBOR) Tags for Typed Arrays | rfc | standard | 2020-02 | useful |
| [`rfc-8943`](https://www.rfc-editor.org/rfc/rfc8943.txt) | Concise Binary Object Representation (CBOR) Tags for Date | rfc | standard | 2020-11 | useful |
| [`rfc-9090`](https://www.rfc-editor.org/rfc/rfc9090.txt) | Concise Binary Object Representation (CBOR) Tags for Object Identif… | rfc | standard | 2021-07 | useful |
| [`rfc-9164`](https://www.rfc-editor.org/rfc/rfc9164.txt) | Concise Binary Object Representation (CBOR) Tags for IPv4 and IPv6 … | rfc | standard | 2021-12 | marginal |
| [`rfc-9581`](https://www.rfc-editor.org/rfc/rfc9581.txt) | Concise Binary Object Representation (CBOR) Tags for Time, Duration… | rfc | standard | 2024-08 | useful |
| [`rfc-9781`](https://www.rfc-editor.org/rfc/rfc9781.txt) | A Concise Binary Object Representation (CBOR) Tag for Unprotected C… | rfc | standard | 2025-05 | marginal |

#### D. COSE and CWT — the signing layer

| record | title | type | maturity | date | verdict |
|---|---|---|---|---|---|
| [`rfc-9052`](https://www.rfc-editor.org/rfc/rfc9052.txt) | CBOR Object Signing and Encryption (COSE): Structures and Process | rfc | standard | 2022-08 | useful |
| [`rfc-8152`](https://www.rfc-editor.org/rfc/rfc8152.txt) | CBOR Object Signing and Encryption (COSE) | rfc | standard | 2017-07 | marginal |
| [`rfc-9053`](https://www.rfc-editor.org/rfc/rfc9053.txt) | CBOR Object Signing and Encryption (COSE): Initial Algorithms | rfc | informational | 2022-08 | useful |
| [`rfc-9054`](https://www.rfc-editor.org/rfc/rfc9054.txt) | CBOR Object Signing and Encryption (COSE): Hash Algorithms | rfc | informational | 2022-08 | useful |
| [`rfc-9338`](https://www.rfc-editor.org/rfc/rfc9338.txt) | CBOR Object Signing and Encryption (COSE): Countersignatures | rfc | standard | 2022-12 | useful |
| [`rfc-9360`](https://www.rfc-editor.org/rfc/rfc9360.txt) | CBOR Object Signing and Encryption (COSE): Header Parameters for Ca… | rfc | standard | 2023-02 | marginal |
| [`rfc-8392`](https://www.rfc-editor.org/rfc/rfc8392.txt) | CBOR Web Token (CWT) | rfc | standard | 2018-05 | useful |
| [`rfc-9597`](https://www.rfc-editor.org/rfc/rfc9597.txt) | CBOR Web Token (CWT) Claims in COSE Headers | rfc | standard | 2024-06 | useful |
| [`rfc-9596`](https://www.rfc-editor.org/rfc/rfc9596.txt) | CBOR Object Signing and Encryption (COSE) "typ" (type) Header Param… | rfc | standard | 2024-06 | useful |
| [`rfc-9679`](https://www.rfc-editor.org/rfc/rfc9679.txt) | CBOR Object Signing and Encryption (COSE) Key Thumbprint | rfc | standard | 2024-12 | useful |
| [`rfc-9864`](https://www.rfc-editor.org/rfc/rfc9864.txt) | Fully-Specified Algorithms for JSON Object Signing and Encryption (… | rfc | standard | 2025-10 | useful |
| [`rfc-9942`](https://www.rfc-editor.org/rfc/rfc9942.txt) | CBOR Object Signing and Encryption (COSE) Receipts | rfc | standard | 2026-06 | useful |
| [`rfc-9995`](https://www.rfc-editor.org/rfc/rfc9995.txt) | CBOR Object Signing and Encryption (COSE) Hash Envelope | rfc | standard | 2026-07 | useful |

#### E. Standards bodies

| record | title | type | maturity | date | verdict |
|---|---|---|---|---|---|
| [`ietf-cbor-wg`](https://datatracker.ietf.org/wg/cbor/about/) | IETF Concise Binary Object Representation Maintenance and Extension… | consortium | — |  | useful |
| [`ietf-cose-wg`](https://datatracker.ietf.org/wg/cose/about/) | IETF CBOR Object Signing and Encryption (COSE) Working Group | consortium | — |  | useful |

#### F. Recorded and judged out of scope for a CBOR product

| record | title | type | maturity | date | verdict |
|---|---|---|---|---|---|
| [`rfc-9254`](https://www.rfc-editor.org/rfc/rfc9254.txt) | Encoding of Data Modeled with YANG in the Concise Binary Object Rep… | rfc | standard | 2022-07 | marginal |
| [`rfc-9997`](https://www.rfc-editor.org/rfc/rfc9997.txt) | YANG-CBOR: Allocating SID Ranges for Private Enterprise Number (PEN… | rfc | standard | 2026-07 | marginal |
| [`rfc-8230`](https://www.rfc-editor.org/rfc/rfc8230.txt) | Using RSA Algorithms with CBOR Object Signing and Encryption (COSE)… | rfc | standard | 2017-09 | marginal |
| [`rfc-8778`](https://www.rfc-editor.org/rfc/rfc8778.txt) | Use of the HSS/LMS Hash-Based Signature Algorithm with CBOR Object … | rfc | standard | 2020-04 | marginal |
| [`rfc-9964`](https://www.rfc-editor.org/rfc/rfc9964.txt) | ML-DSA for JSON Object Signing and Encryption (JOSE) and CBOR Objec… | rfc | standard | 2026-05 | marginal |
| [`rfc-9459`](https://www.rfc-editor.org/rfc/rfc9459.txt) | CBOR Object Signing and Encryption (COSE): AES-CTR and AES-CBC | rfc | standard | 2023-09 | marginal |
| [`rfc-8812`](https://www.rfc-editor.org/rfc/rfc8812.txt) | CBOR Object Signing and Encryption (COSE) and JSON Object Signing a… | rfc | standard | 2020-08 | marginal |
| [`rfc-9021`](https://www.rfc-editor.org/rfc/rfc9021.txt) | Use of the Walnut Digital Signature Algorithm with CBOR Object Sign… | rfc | informational | 2021-05 | not-useful |
| [`rfc-8747`](https://www.rfc-editor.org/rfc/rfc8747.txt) | Proof-of-Possession Key Semantics for CBOR Web Tokens (CWTs) | rfc | standard | 2020-03 | marginal |
| [`rfc-9921`](https://www.rfc-editor.org/rfc/rfc9921.txt) | CBOR Object Signing and Encryption (COSE) Header Parameter for Time… | rfc | standard | 2026-02 | marginal |
| [`rfc-8769`](https://www.rfc-editor.org/rfc/rfc8769.txt) | Cryptographic Message Syntax (CMS) Content Types for Concise Binary… | rfc | informational | 2020-03 | not-useful |
| [`rfc-9528`](https://www.rfc-editor.org/rfc/rfc9528.txt) | Ephemeral Diffie-Hellman Over COSE (EDHOC) | rfc | standard | 2024-03 | marginal |
| [`rfc-9529`](https://www.rfc-editor.org/rfc/rfc9529.txt) | Traces of Ephemeral Diffie-Hellman Over COSE (EDHOC) | rfc | informational | 2024-03 | not-useful |
| [`rfc-9668`](https://www.rfc-editor.org/rfc/rfc9668.txt) | Using Ephemeral Diffie-Hellman Over COSE (EDHOC) with the Constrain… | rfc | standard | 2024-11 | not-useful |
| [`draft-ietf-cbor-packed`](https://www.ietf.org/archive/id/draft-ietf-cbor-packed-19.txt) | Packed CBOR | draft -19 | draft | 2026-08-06 | marginal |

**51 records.** Every entry carries a sha-256 of the bytes retrieved on 2026-09-22 in its `record.yaml`; no third-party document is committed.
