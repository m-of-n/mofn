---
# Document control (MADR + GitHub-docs + spec-schema style)
schema: "archdoc/v1"
id: ARCH-0001
title: "Authorization, local names, and artifact attestation — architecture checkpoint"
short_title: "Authz + attestation architecture"
description: "Canonical working architecture for a native model that is not X.509, with defined interchange to other formats."
type: architecture
category: security
status: draft
version: "0.1.1"
version_policy: "semver; PATCH = editorial; MINOR = additive requirements; MAJOR = breaking model change"
date: "2026-09-15"
updated: "2026-09-21"
authors:
  - role: architect
    id: conversation-brainpool256
decision_makers: []
reviewers: []
needs_review: true
reviewed: false
iteration_of: null
supersedes: []
superseded_by: null
canonical_path: spec/ARCH-0001-authorization-attestation.md
companion:
  - spec/ARCH-0001-CHANGELOG.md
tags:
  - spki
  - sdsi
  - pgp-wot
  - pics
  - attestation
  - threshold
  - interchange
  - not-x509-native
related_rfcs:
  - RFC2692
  - RFC2693
  - RFC8392
  - RFC8949
  - RFC9052
  - RFC9804
related_drafts:
  - draft-ietf-scitt-architecture
  - in-toto-attestation-v1
  - slsa-provenance-v1
open_decisions:
  - DEC-001
  - DEC-002
  - DEC-003
  - DEC-004
  - DEC-005
constraints:
  native_format_excludes:
    - X.509
    - PKIX
  interchange_required: true
scope:
  in:
    - conceptual information model
    - requirements
    - research baseline
    - interchange matrix
    - open decisions
  out:
    - product naming
    - implementation language choice
    - wire-format freeze
    - cryptographic algorithm suite freeze
agent_checkpoint: true
agent_notes: >
  Other agents: treat this file as the source of truth for architecture
  state as of v0.1.0. Do not invent accepted decisions. Open items are
  listed under Open decisions. Iterate by bumping version and appending
  CHANGELOG. Do not rewrite history in this file; use CHANGELOG.
---

# ARCH-0001 — Authorization, local names, and artifact attestation

**Status:** draft · **Version:** 0.1.1 · **Date:** 2026-09-15  
**Canonical file:** `spec/ARCH-0001-authorization-attestation.md`  
**Changelog:** `spec/ARCH-0001-CHANGELOG.md`

This document is the checkpoint. Later work edits *this* document (or a successor version of it), not a new essay.

---

## 1. Problem statement

Need a **native** authorization and attestation model whose primary objects are:

1. a **principal** identified by a public key (or a digest of a public key);
2. **local names** defined only relative to a naming key (SDSI);
3. **authorization** bound to a principal, optionally delegated, with **tag intersection** (SPKI);
4. **threshold subjects** (*k* of *n*) as first-class principals (SPKI);
5. **signed statements about artifacts** (PICS lineage; modern attestation);
6. **import and export** to existing ecosystems without making those ecosystems the native model.

X.509 / PKIX is an **interchange target**, not the information model.

PGP Web of Trust is an **interchange and introducer pattern**, not the validation algorithm.

---

## 2. Goals and non-goals

### 2.1 Goals

| ID | Goal |
|----|------|
| G1 | Key-centric principals; names are not globally unique identifiers. |
| G2 | Separate name certificates from authorization certificates. |
| G3 | Deterministic reduction of authorization chains (SPKI 5-tuple style), not unbounded WoT path search as the primary algorithm. |
| G4 | *k*-of-*n* subjects in the native model. |
| G5 | Statements about artifacts (hash-addressed) use the same principal and validity machinery as statements about rights. |
| G6 | Well-defined lossless-enough mapping **in and out** of selected foreign formats. |
| G7 | Documents and schemas versioned; decisions explicit and reversible until accepted. |

### 2.2 Non-goals (this version)

| ID | Non-goal |
|----|----------|
| NG1 | Replace WebPKI for TLS server authentication. |
| NG2 | Define a commercial CA product. |
| NG3 | Freeze encoding, algorithms, or repository name. |
| NG4 | Require a blockchain or any specific transparency log. |
| NG5 | Treat email addresses as globally secure names. |

---

## 3. Research summary (inputs, not decisions)

Collected 2026-09-15. Citations are sources consulted; they do not ratify design.

### 3.1 Historic certificate models

| Model | Principal | Name scope | Trust construction | Fault tolerance | Status |
|-------|-----------|------------|--------------------|-----------------|--------|
| X.509 / PKIX | DN + key | Intended global (X.500); local in practice | Hierarchical CA, optional bridge / mesh | Path to a configured trust anchor | Dominant for TLS; not native here |
| PGP / OpenPGP | Key + UIDs | Global-ish (email) | Web of Trust; later trust-signatures (meta-introducers) | Multiple introducers; owner-defined trust | Identity and mail; weak authorization language |
| SDSI | Key | **Local to the naming key**; compound names are chains | No system-wide root | Via linked namespaces | Research / merged into SPKI |
| SPKI | Key or hash of key | Optional names; authorization does not require them | Authorization 5-tuples; delegation bit; tag ∩ validity ∩ | **Threshold subject** *k*-of-*n* | RFC 2692, RFC 2693 experimental |
| PICS | Labeling *service* + content | N/A (labels objects) | Signed labels; checksum of content; client chooses services | Multiple independent services | W3C; dormant; conceptual parent of attestations |

Sources: RFC 2693; Ellison comparison notes; RFC 9804 (SPKI S-expressions, 2025); PICS FAQ / W3C.

SPKI authorization certificate (theory) is a signed 5-tuple:

`(Issuer, Subject, Delegation, Tag, Validity)`

Reduction (RFC 2693 §6.3, paraphrase): two 5-tuples compose when the subject of the first is the issuer of the second and delegation is permitted; result tag = intersection; result validity = intersection.

SDSI basic name: `(name fred)` in *George’s* space. Compound: `(name fred sam)` meaning George’s Fred’s Sam. Fully qualified: key (or key hash) followed by the name chain.

RFC 9804 restates canonical S-expressions as a living encoding option. It is **not** selected here (see DEC-002).

### 3.2 Modern statement / envelope stack

| Layer | Role | Encoding | Notes |
|-------|------|----------|-------|
| in-toto Statement | typed predicate about subjects (artifacts) | JSON | Predicate registry: SLSA provenance, VSA, SPDX, CycloneDX, link |
| DSSE | signature envelope over a payload type | JSON | Used by Cosign / SLSA generators; PAE signing |
| COSE_Sign1 | signature envelope | CBOR | SCITT signed statements |
| CWT claims | `iss`, `sub`, `exp`, `nbf`, `iat`, … in COSE protected header 15 | CBOR | RFC 8392; SCITT profile |
| SCITT | signed statement + optional transparency receipt | COSE | Payload may be SPDX, CycloneDX, in-toto, SLSA, CoSWID |
| SLSA provenance | how an artifact was built | in-toto predicate | Not a name system |
| W3C VC / DID | issuer, subject, claims | JSON-LD / various | Parallel identity track; interchange candidate |
| OpenPGP signatures | identity and data signatures | OpenPGP packets | Introducer import candidate |

X.509 appears in this stack only as: (a) existing signer identity some tools still carry, (b) `did:x509` in some COSE toolchains. That is interchange pressure, not a reason to native-encode PKIX.

### 3.3 Implications for the native model

1. Historic gap: SPKI/SDSI never standardized a first-class **artifact statement** type; PICS did, without a strong principal/delegation model.
2. Modern gap: in-toto / SCITT / SLSA have strong artifact statements and weak *local-name + threshold authorization* languages.
3. Composition target: **SPKI-shaped rights and names** + **PICS/in-toto-shaped artifact predicates** + **COSE or DSSE envelope for bytes on the wire** (envelope is interchange, not the information model).
4. PGP remains useful as an **introducer graph import**, mapped onto name certs or weighted endorsements — not as the reducer.

---

## 4. Information model (working; not frozen)

Logical types. Encoding is DEC-002.

### 4.1 Primitive values

| Type | Meaning |
|------|---------|
| `Key` | Public key material + algorithm identifier |
| `KeyId` | Digest of a canonical key encoding (algorithm of digest is parameterized) |
| `Principal` | `Key` \| `KeyId` \| `Name` \| `Threshold` \| `Group` |
| `Name` | `{ issuer: Principal, labels: [string, ...] }` — SDSI compound name |
| `Threshold` | `{ k: int, n: int, members: [Principal, ...] }` with `1 ≤ k ≤ n` and `n = len(members)` |
| `Tag` | Authorization language value; opaque at this layer except for defined intersection |
| `Validity` | `{ not_before?, not_after?, online_check? }` |
| `ArtifactId` | `{ uri?: string, digest: { alg, hex } }` |
| `PredicateType` | URI naming a statement vocabulary |
| `Predicate` | Typed payload whose schema is identified by `PredicateType` |

### 4.2 Certificate and statement kinds

| Kind | Binds | Signed by | Reduction role |
|------|-------|-----------|----------------|
| `NameCert` | name labels → principal | naming key | Name resolution only |
| `AuthzCert` | principal → tag + delegation flag | issuer key | SPKI 5-tuple reduction |
| `AclEntry` | same as AuthzCert | unsigned; issuer = `Self` | Local policy root |
| `ArtifactStatement` | artifact id(s) → predicate | issuer key | Attestation; may *require* an AuthzCert to be accepted by a verifier policy |
| `Endorse` | “issuer treats subject as introducer at weight w” | issuer key | Optional PGP-shaped import; not required for AuthzCert reduction |

`AuthzCert` fields (logical):

```
issuer:       Principal     # must be Key or KeyId at signature time
subject:      Principal     # may be Name, Threshold, Key, KeyId
delegate:     bool
tag:          Tag
validity:     Validity
```

`ArtifactStatement` fields (logical):

```
issuer:       Principal
subjects:     [ArtifactId, ...]
predicate_type: PredicateType
predicate:    Predicate
validity:     Validity
```

This is the PICS analogue: issuer ≈ rating service; subjects ≈ labeled objects; predicate ≈ rating tuple; validity ≈ label lifetime; content binding is the artifact digest.

### 4.3 Verifier inputs

A decision procedure takes:

- a request (`who` wants `tag` on `resource`, or “is statement S acceptable under policy P”);
- a set of certs/statements;
- a local ACL (`Self`);
- configured trust for *artifact services* (which issuers may assert which `PredicateType`s);
- current time and optional online validity checks.

Two procedures, kept separate:

1. **Name resolution** — rewrite `Name` to `KeyId` via `NameCert` chains.
2. **Authorization reduction** — SPKI-style composition after names are resolved.
3. **Statement acceptance** — signature valid ∧ issuer authorized for that `PredicateType` ∧ subject digest matches the artifact under consideration.

(3) may call (2). They must not be collapsed into one graph walk in v0.1.

---

## 5. Requirements

Priority: **M**ust / **S**hould / **C**ould. Open decisions do not silently satisfy these.

### 5.1 Model

| ID | Pri | Requirement |
|----|-----|-------------|
| R-M-01 | M | Native encoding SHALL NOT be X.509 / PKIX. |
| R-M-02 | M | A principal MAY be identified solely by key or key digest. |
| R-M-03 | M | Names SHALL be interpreted only relative to an issuing principal. |
| R-M-04 | M | Name bindings and authorization bindings SHALL be distinct object kinds. |
| R-M-05 | M | Authorization composition SHALL be deterministic given an ordered cert set and ACL. |
| R-M-06 | M | Threshold principals SHALL be representable without encoding them as a CA hierarchy. |
| R-M-07 | M | Artifact statements SHALL bind at least one content digest. |
| R-M-08 | M | Tag intersection semantics SHALL be defined for every tag profile the implementation claims. |
| R-M-09 | S | Validity intersection SHALL be defined (time window ∩ optional online checks). |
| R-M-10 | S | Delegation SHALL be an explicit boolean (or equivalent) on `AuthzCert`. |

### 5.2 Interchange

| ID | Pri | Requirement |
|----|-----|-------------|
| R-I-01 | M | Publish a mapping table for each supported foreign format: what is preserved, dropped, or inferred. |
| R-I-02 | M | Import SHALL NOT require the foreign object to become a native trust anchor. |
| R-I-03 | S | Export to in-toto Statement + DSSE OR COSE_Sign1 + CWT claims (at least one envelope in v1). |
| R-I-04 | S | Import OpenPGP identity signatures as `NameCert` and/or `Endorse`, never as `AuthzCert` unless an explicit profile says so. |
| R-I-05 | S | Import X.509 only as a foreign identity assertion about a key (name or attribute), marked `provenance: x509`. |
| R-I-06 | C | Export a subset of `AuthzCert` as a W3C Verifiable Credential using a documented context. |
| R-I-07 | C | Emit SPDX or CycloneDX *inside* an `ArtifactStatement` predicate rather than inventing a third SBOM syntax. |

### 5.3 Operations

| ID | Pri | Requirement |
|----|-----|-------------|
| R-O-01 | M | Every signed object SHALL have an issuer key that can be specified as `KeyId`. |
| R-O-02 | S | Short-lived validity preferred over revocation-heavy design; revocation still representable. |
| R-O-03 | S | Canonicalization algorithm for each concrete encoding SHALL be cited, not invented silently. |
| R-O-04 | C | Optional registration of statements with a SCITT-like transparency service. |

### 5.4 Documentation / process

| ID | Pri | Requirement |
|----|-----|-------------|
| R-D-01 | M | Architecture lives in this file (or a numbered successor). |
| R-D-02 | M | Accepted decisions move from “Open decisions” to an ADR file; this document then references them. |
| R-D-03 | M | Version bumps recorded in `ARCH-0001-CHANGELOG.md`. |

---

## 6. Interchange matrix (working)

Legend: **I** import, **E** export, **—** out of scope this version, **P** partial (lossy, must be flagged).

| Foreign object | I | E | Maps to native | Loss / notes |
|----------------|---|---|----------------|--------------|
| SPKI/SDSI S-exp cert (RFC 2693 / 9804) | I | E | NameCert, AuthzCert, Threshold | Closest peer; preferred reference mapping |
| OpenPGP key + UIDs + sigs | I | P | Key, NameCert, Endorse | No tag language; trust values are local to importer |
| X.509 EE / CA cert | I | — | Key + NameCert (DN as labels under a `x509:` namespace of the *importer*, not of the CA) + provenance | Do not treat CA bit as AuthzCert |
| X.509 attribute certificate | I | P | AuthzCert (tag profile TBD) | Attributes ≠ SPKI tags |
| in-toto Statement | I | E | ArtifactStatement | Subjects = artifacts; predicate_type preserved |
| DSSE envelope | I | E | wire only | Not an information-model type |
| COSE_Sign1 + CWT | I | E | wire + issuer/sub/exp | Align `iss`/`sub` with KeyId profile (DEC-003) |
| SLSA provenance v1 | I | E | ArtifactStatement predicate | |
| SPDX / CycloneDX | I | E | ArtifactStatement predicate | |
| PICS label | I | — | ArtifactStatement | Historic; import profile only if needed |
| W3C VC | I | C | ArtifactStatement or NameCert depending on type | Context must be pinned |
| SCITT receipt | I | C | evidence attached to ArtifactStatement | Does not change meaning of statement |

**Forbidden native mapping:** X.509 certificate path validation as the native reducer.

---

## 7. Open decisions

Do not treat any option below as selected.

### DEC-001 — Working title / repo slug

Options: `spki3`, `open-sdsi`, `kofn-certs`, `localnames`, `sudsy`.  
Blocked on: none.  
Affects: packaging only.

### DEC-002 — Concrete native encoding

Options:

1. Canonical S-expressions (RFC 9804) as canonical; JSON as diagnostic.
2. CBOR + CDDL as canonical; COSE for signed form.
3. JSON + RFC 8785 JCS as canonical; DSSE for signed form.
4. Dual canonical (CBOR and JSON) with a documented bijection.

Drivers: library availability, SCITT alignment, SPKI fidelity, human debug.  
Acceptance test: round-trip fixtures for NameCert, AuthzCert (including threshold subject), ArtifactStatement.

### DEC-003 — Issuer / subject identifiers on the wire

Options: raw COSE key; COSE key thumbprint; `did:key`; hash-uri (`sha256:…`); text KeyId.

Must specify: canonical key bytes before hashing.

### DEC-004 — Tag language (authorization)

Options:

1. SPKI tag S-expressions as-is (byte-string sets + intersection).
2. Constrained JSON tags with explicit ∩ operator.
3. Embed a small policy subset (e.g. in-toto layout step names, or SPDX purpose).

v0.1 may ship **tag as opaque byte string** plus one profile (`urn:…:tag:bytes-equal`) so reduction can be implemented before the language is rich.

### DEC-005 — Envelope for ArtifactStatement

Options: DSSE (in-toto world), COSE_Sign1 (SCITT world), both with a single unsigned payload schema.

---

## 8. Work packages (not scheduled)

| WP | Output | Depends |
|----|--------|---------|
| WP0 | This document + changelog (done as v0.1.0) | — |
| WP1 | JSON Schema or CDDL for logical types in §4 | DEC-002 may wait; schema can be encoding-neutral first |
| WP2 | Mapping spec: SPKI S-exp ↔ native | — |
| WP3 | Mapping spec: in-toto Statement ↔ ArtifactStatement | — |
| WP4 | Mapping spec: OpenPGP introducers ↔ NameCert/Endorse | — |
| WP5 | Mapping spec: X.509 → annotated NameCert (import only) | — |
| WP6 | Reduction algorithm + test vectors | DEC-004 minimum profile |
| WP7 | First ADR when any DEC-* is accepted | review |

---

## 9. Agent / iteration protocol

1. Edit this file in place for additive clarification.
2. Any accepted decision is a new `spec/ADR-NNNN-….md` and a line in the changelog; then set `status` on that decision here to `accepted` with a pointer.
3. Breaking model changes increment MAJOR and set `superseded_by` on the old file if the file is split.
4. Do not append parallel “ideas” documents that diverge from §4–§5. Propose a diff against this file.
5. Front matter `version` and `updated` must change together.

---

## 10. References (consulted)

- RFC 2692 — SPKI Requirements  
- RFC 2693 — SPKI Certificate Theory  
- RFC 9804 — SPKI S-Expressions (2025)  
- RFC 8392 — CWT  
- RFC 8949 — CBOR  
- RFC 9052 — COSE  
- draft-ietf-scitt-architecture — SCITT  
- in-toto Attestation Framework v1  
- SLSA provenance v1  
- W3C PICS (label format, signed labels, content checksum)  
- Ellison, “SPKI/SDSI and the Web of Trust” comparison notes  
- OpenPGP / GnuPG trust-signature model (meta-introducers)

End of ARCH-0001 v0.1.0
