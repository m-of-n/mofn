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
version: "0.3.1"
version_policy: "semver; PATCH = editorial; MINOR = additive requirements; MAJOR = breaking model change"
date: "2026-09-15"
updated: "2026-11-12"
authors:
  - role: architect
    id: conversation-brainpool256
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
  - RFC9580
  - RFC9943
related_drafts:
  - in-toto-attestation-v1
  - slsa-provenance-v1
open_decisions:
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
  state as of v0.3.1. v0.3.1 closes the SDSI-names gap in §5.5. v0.3.0 adds §2.3, the two target applications. v0.2.0 folded ARCH-0001-PROPOSAL-v0.2.0 in (now
  superseded) and carried ADR-0002, ADR-0003, ADR-0007 and the T-012c
  delegation decision into §4-§7. Where SPEC-0001..0005 and this file differ,
  §5.5 lists every known gap and which side owes the change. Do not invent accepted decisions. Open items are
  listed under Open decisions. Iterate by bumping version and appending
  CHANGELOG. Do not rewrite history in this file; use CHANGELOG.
---

# ARCH-0001 — Authorization, local names, and artifact attestation

**Status:** draft · **Version:** 0.3.1 · **Date:** 2026-09-15 · **Updated:** 2026-11-12  
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

**Motivation, not scope.** AI agents acting for people need exactly this:
authority that is delegated, bounded in scope and time, and traceable to a
person. That is cited here as motivation only. It carries **no normative
content**. `UC-0001` UC-4 stays a use case, and §2.3 says why it is not a
target.

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

### 2.3 Target applications

Added in 0.3.0 (mofn#135, T-012b, `DL-0032`). MD-1 (`DECISIONS-0001` T1-A)
scopes **two** targets. For each, an in-scope target costs a domain of
discourse, worked examples and a section; this is that section. The two are
deliberately unlike each other. One target would show that the machinery
runs. Only two unlike domains, through one engine and one renderer with no
domain-specific code, show that the vocabulary mechanism generalises
(`ARCH-0002` P3; DEC-007 by `ADR-0007`).

Every worked statement below is a published vector in `SPEC-0002` Appendix A
(`spec/vectors/ksa-core/`), and each verifier answer is an `evaluations` entry
there or a worked ask in `SPEC-0004` Appendix A. A row marked *illustrative*
says why it has no vector.

**Neutral on the open decisions.** Scopes are attribute ranges under the
`SPEC-0003` §6 base kinds, not a tag language, so DEC-004 stays open. No export
envelope is used, so DEC-005 stays open. The examples are encoded as
`ADR-0004` specifies. A definition's hash is its identity in `SPEC-0003`, but
`ARCH-0002` P4 (*a domain is a hash-identified set*) is still draft, so nothing
here makes a domain's hash identity normative.

#### 2.3.1 Software supply chain (primary)

**Domain of discourse.** Definition DV-1 `supply-chain`, by the maintainer's
key (Alice): the type `build-provenance` (`reproducible` / `attested` /
`unverified`, delegable with narrowing); the type `outcome` (`approve` /
`changes` / `reject`, not delegable); the template `release-attestation`.
Subjects are artifacts by content digest (R-M-07, R-M-11 `digest` mode).

| # | Worked statement | Vector | Verifier question | Answer | UC |
|---|---|---|---|---|---|
| SC-1 | *Alice says sha-256:artifact has build-provenance = reproducible* | TV-4 | Was this artifact built reproducibly, according to a key the relying party trusts for that? | yes (`SPEC-0004` App. A Ask 1); after Alice revokes it (TV-7), no, `revoked` (Ask 2) | UC-1 |
| SC-2 | *Carol trusts Alice about build-provenance ∈ {reproducible, attested}, may delegate depth 1 within {reproducible}*; *Alice trusts Bob about {reproducible}*; *Bob says the artifact is reproducible* | TV-5, TV-16, TV-17; E-2 | Is the build bot's claim inside the authority the maintainer delegated? | yes. Must fail: a delegation outside `ranges` (E-1, `widening`), a third hop (E-3, `depth`), an onward depth that is too large (E-4, `widening`) | UC-1 |
| SC-3 | *Carol trusts any 2 of {Alice, Bob, Dave} about build-provenance*; *Bob reviews TV-4: approve* | TV-9, TV-6 | Did enough independent reviewers approve this release? | **illustrative.** The statements are vectors; the answer is not. `SPEC-0005` (panels and processes) has no vectors yet | UC-2 |

**Interchange.** in-toto Statement: subject = the digest target;
`predicateType` URI ↔ `type-ref`, lossy (§6, `ARCH-0002` P1). SLSA provenance
v1 and SPDX/CycloneDX travel as predicates (R-I-07), not as native types.
SCITT (RFC 9943): registration is optional (R-O-04); a receipt is evidence
about a statement and does not change its meaning (§6). The mapping is WP3.

#### 2.3.2 Archives and library (contrast)

**Domain of discourse.** Definition DV-3 `library-review`, by the library
lead's key (Dave): the type `reviewed` (`yes` / `partial` / `no`, named in
English and Spanish, delegable with narrowing); the record type `work` (a
published work by its `title`), which identifies a subject that has no bytes of
its own; the text type `locator`; the template `record-reviewed`, whose targets
are a digest or a description. This is the corpus the project already runs
(`library/`).

| # | Worked statement | Vector | Verifier question | Answer | UC |
|---|---|---|---|---|---|
| AR-1 | *Carol trusts Dave about reviewed, may delegate depth 1*; *Dave trusts Bob about reviewed ∈ {partial}*; *Bob says sha-256:record has reviewed = partial* | TV-22, TV-23, TV-25; E-5 | Has this library record been checked against its source, by someone entitled to say so? | yes | UC-3 |
| AR-2 | as AR-1, but *Bob says sha-256:record has reviewed = yes* | TV-24; E-6 | The same | no, `no-path`: Bob was delegated only `partial` | UC-3 |
| AR-3 | *Dave says the work titled "Simple Public Key Certificate" has reviewed = yes, locator = https://www.rfc-editor.org/rfc/rfc2693* | TV-26; E-7 | Has **the work** been reviewed, whatever copy one holds? | yes. The subject is a `description` target (R-M-11), and the URL is an attribute, not the subject (`SPEC-0002` §7.2) | UC-3 |

AR-1 and SC-2 are answered by the same procedure, and AR-1's sentence is
rendered from DV-3 by the renderer that renders SC-1 from DV-1 (`prototype/wallet`
tests). That is the evidence MD-1 asked the second target for.

**Found, not fixed.** AR-3's subject is rendered as "a described object": the
renderer has no rule for showing a description target (`SPEC-0003` §10 is
silent on it). Owed as T-066. No requirement here changes because of it.

**Interchange.** in-toto has no form for a description subject. Its subjects
are digest sets, so AR-3 does not export to in-toto (§6, the in-toto row,
already records this loss). No archival standard is mapped in this version.

#### 2.3.3 Not targets

| Application | Status | Why |
|---|---|---|
| AI agent attestation | **motivation only** (§1) | The target moves: NIST work began April 2026, and the SCITT agent profile is a draft. Specifying against it would date this document fastest. UC-4 stays a use case |
| AI media provenance | not scoped | Crowded and standards-led (C2PA) |
| Scientific data | not scoped | PROV-O adjacent; no partner |
| IoT onboarding | not scoped | Key-centric by nature, but needs a partner |

Adding a third target costs a domain, worked examples and interchange mapping.
MD-1's argument governs any request to add one: a third domain adds cost
without adding evidence of generalisation.

**Not proposed.** No requirement is added, amended or withdrawn. No DEC-* is
opened, ranked or accepted. P4 and P7 stay draft: §2.3.1 is not the
supply-chain *profile* that `DECISIONS-0001` T1-B asks for before P7 can be
accepted.

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

RFC 9804 restates canonical S-expressions. It is an Informational restatement of a 1990s encoding, and it is recorded here as **historical**: a reference for the WP2 mapping, not a contender. DEC-002 is accepted as option 5 (`ADR-0004`). What the SPKI lineage contributes is key-centricity (G1, R-M-02), not its syntax.

### 3.2 Modern statement / envelope stack

| Layer | Role | Encoding | Notes |
|-------|------|----------|-------|
| in-toto Statement | typed predicate about subjects (artifacts) | JSON | Predicate registry: SLSA provenance, VSA, SPDX, CycloneDX, link |
| DSSE | signature envelope over a payload type | JSON | Used by Cosign / SLSA generators; PAE signing |
| COSE_Sign1 | signature envelope | CBOR | SCITT signed statements |
| CWT claims | `iss`, `sub`, `exp`, `nbf`, `iat`, … in COSE protected header 15 | CBOR | RFC 8392; SCITT profile |
| SCITT (RFC 9943, Proposed Standard, June 2026) | signed statement + optional transparency receipt | COSE | Payload may be SPDX, CycloneDX, in-toto, SLSA, CoSWID. `iss`/`sub` mandatory, payload opaque |
| SLSA provenance | how an artifact was built | in-toto predicate | Not a name system |
| W3C VC / DID | issuer, subject, claims | JSON-LD / various | Parallel identity track; interchange candidate |
| OpenPGP signatures | identity and data signatures | OpenPGP packets | Introducer import candidate |

X.509 appears in this stack only as: (a) existing signer identity some tools still carry, (b) `did:x509` in some COSE toolchains. That is interchange pressure, not a reason to native-encode PKIX.

### 3.3 Implications for the native model

1. Historic gap: SPKI/SDSI never standardized a first-class **artifact statement** type; PICS did, without a strong principal/delegation model.
2. Modern gap: in-toto / SCITT / SLSA have strong artifact statements and weak *local-name + threshold authorization* languages. SCITT is ratified (RFC 9943), so this gap is in a published standard, not a moving draft. Vocabularies are still re-invented ad hoc *inside* SCITT: `draft-mih-scitt-agent-action-capsule-02` declares a disposition vocabulary in prose, and nothing can dereference it. That is the PICS rating-system pattern, unspecified. DEC-007 (`ADR-0007`) answers it.
3. Composition target: **SPKI-shaped rights and names** + **PICS/in-toto-shaped artifact predicates** + **COSE or DSSE envelope for bytes on the wire** (envelope is interchange, not the information model).
4. PGP remains useful as an **introducer graph import**, mapped onto name certs or weighted endorsements — not as the reducer.

### 3.4 OpenPGP mechanisms read against this model

Additive, 0.1.9 (mofn#128, `DL-0026`). These are inputs, not decisions. Each
row says which item the mechanism bears on and whether that item is still
open. Most rows **confirm** something already decided or drafted. They are
recorded so the next reader does not re-derive them, and so that WP4 starts
from them. One row is new evidence on a question still open: the `kid`
preimage.

| OpenPGP mechanism (RFC 9580) | Bears on | Item's state | Reading |
|---|---|---|---|
| Critical bit on signature subpackets (§5.2.3.7; §5.2.5): an unknown critical subpacket in the hashed area makes the signature unusable for validation; an unknown non-critical one is ignored | `ARCH-0002` P3, `SPEC-0002` V7 (closed map) | accepted (`ADR-0004`) | Our profile is **stricter**: every unknown field is rejected, so nothing is "non-critical". OpenPGP pays for its split: a verifier that ignores a non-critical field may not see a meaning the issuer intended. Under our profile a new field is a new definition (`ARCH-0003` W-12), not a field that old verifiers ignore. No change. |
| Notation Data (§5.2.3.24): user names are `tag@domain`; names without `@` are the IETF namespace | R-M-03, `ADR-0001` (key-relative naming) | accepted | A **counter-example**. Notation names are scoped by DNS domain or by IETF registry: both are global namespaces, and `ADR-0001` rejected both. It is prior art for *namespacing* types, not for *key-relative* types. No change. |
| v6 fingerprint (§5.5.4.3): SHA-256 over `0x9B`, a 4-octet length, and the public-key packet from the version field on. That covers version, creation time, algorithm and key material | DEC-003 (`ADR-0005`); the open sub-question in §7 DEC-003, "whether a future suite … needs the suite in the preimage" | DEC-003 accepted; sub-question **open** | **New evidence for the open sub-question.** OpenPGP puts the algorithm inside the preimage, so one set of key octets under two algorithms yields two fingerprints. That is the opposite of `SPEC-0002` §4.5. It also puts in the **creation time**, so one key yields different fingerprints at different times. `ADR-0005` avoids that, and this row records the avoidance as deliberate. Evidence only; the sub-question stays with `ADR-0005`. |
| Trust Signature depth (§5.2.3.21): an integer, minimised along the chain in GnuPG | R-M-10 (delegation boolean) vs `SPEC-0004` (integer depth) | open, as `R-0007` P3 — **decided 0.2.0**: integer depth (R-M-10, `DL-0025`) | Nothing new. `R-0007` §3.3 and P3 already carry it; cross-referenced here so WP4 does not raise it a second time. |
| Ownertrust vs validity (GnuPG trustdb; RFC 9580 §5.10 leaves Trust packets to the implementation) | §4.3 (local ACL `Self` kept apart from reduction); `ARCH-0003` W-07, W-14 | drafted | A **confirmation**. OpenPGP keeps "I trust this key to introduce" (local, unsigned) apart from "this key is valid" (computed). We make the same separation, and unlike OpenPGP we specify the computation (G3). No change. |
| Key flags and subkey binding (§5.2.3.29): certify (`0x01`) and sign (`0x02`) on separate keys; the primary can be held offline | `ARCH-0003` §3.2 identity and operational keys; `capabilities` | drafted | A **confirmation** of `ARCH-0003` §3.2: there, a delegation does the work of a subkey binding. The engine consequences are in `PLAN-0004` §6.2. No change here. |

**Not proposed.** No requirement is added, amended or withdrawn. No DEC-* is
opened, ranked or accepted. Neither the OpenPGP packet format nor its
algorithm registry enters the native model (R-M-01 spirit; `ARCH-0002` P1).
**Revocation certificates generated at key creation were considered and
declined by the owner on 2026-11-05.** That is consistent with R-O-02 and
leaves `R-0007` P5 (escrowed revocation) open.

---

## 4. Information model (working; not frozen)

Logical types. Encoding is DEC-002, accepted as KSA-CBOR (`ADR-0004`). The right-hand column gives the KSA form that `SPEC-0002` specifies (`ADR-0003`: where the two differ, the SPEC governs, unless §5.5 records the gap as owed by the SPEC).

### 4.1 Primitive values

| Type | Meaning | KSA form (`SPEC-0002`) |
|------|---------|------------------------|
| `Key` | Public key material + algorithm identifier | `public-key = { alg, pub }` (§8.2), suite per §6 |
| `KeyId` | Digest of a canonical key encoding — **narrowed by `ADR-0005`:** SHA-256 of the key's public-key encoding under its suite | `kid` (§4.5) |
| `Principal` | `Key` \| `KeyId` \| `Name` \| `Threshold` \| `Group` | `kid`; name target (§7.2 type 7); threshold form of `trust` (§8.6). **`Group` has no KSA form yet** (§5.5) |
| `Name` | `{ issuer: Principal, labels: [string, ...] }` — SDSI compound name | target type 7 `[7, kid, [+ label]]` (`SPEC-0002` 0.9.0 §7.2). A binding is an `attestation` with a naming-type attribute (`SPEC-0003` §6.4; `ARCH-0002` P6; TV-28…34), and `SPEC-0004` §5.3 resolves it (`ADR-0008`). The issuer is a kid |
| `Threshold` | `{ k: int, n: int, members: [Principal, ...] }` with `1 ≤ k ≤ n` and `n = len(members)` | `trust` with `trusts: [2* kid]`, `threshold: k`; `n` is the array length (§8.6) |
| `Tag` | Authorization scope; opaque at this layer except for defined intersection | `attribute-range` (§7.4). Its *within* relation is the type's base kind (`SPEC-0003` §6). DEC-004 still open |
| `Validity` | `{ not_before?, not_after?, online_check? }` | `valid = { not-before, not-on-or-after, issued }` (§7.3); no online check |
| `ArtifactId` | A subject, identified by **one of three modes** (R-M-11): `digest` for bytes in hand; `locator` for a subject with an external name (**non-authoritative**, a hint, never a definition); `description`, the canonical digest of a structured description, for subjects that cannot be hashed (a physical object, a work, an event, a role). Plus an `aliases` set binding several identifiers to one subject. At least one content digest is bound in every case (R-M-07) | target types 2 digest and 6 description (§7.2). **A locator is not a target:** type 5 was withdrawn in `SPEC-0002` 0.6.0 (mofn#144), and a locator travels as an attribute on a digest or description target. Aliases: no KSA form yet |
| `PredicateType` | The type a statement assigns, identified **relative to its defining key** (`ARCH-0002` P1), never by URI. Its meaning (names, descriptions and rendering in a language map) is carried by a signed definition (DEC-007, `ADR-0007`) | `type-ref = { definition: DefinitionId, label }` (§7.4; `SPEC-0003`) |
| `Predicate` | Typed payload whose schema is identified by `PredicateType` | `attribute = { type: type-ref, value }` (§7.4) |

### 4.2 One statement form, several functions

**Rewritten in 0.2.0** under `ADR-0002`, which accepted `ARCH-0002` P2 (*A says
B has C*) and P6 (*a name is an attested string*). v0.1 listed five object
*kinds*. They are **functions over one signed statement form**, distinguished by
what the statement asserts. KSA spells the form as `SPEC-0002` §7: `kind`,
`suite`, `says` (the speaker, *A*), `this` (the target, *B*), `valid`, and a
kind-specific `body` (*C*).

| v0.1 kind | Function | KSA kind (`SPEC-0002` §8) | Notes |
|---|---|---|---|
| `NameCert` | **naming**: bind a local name to a principal | `attestation` (4) about a key or a name, assigning an attribute of base kind `name` (`SPEC-0003` §6.4; DV-4, TV-28…34) | Compound names resolve by `SPEC-0004` §5.3 (`ADR-0008`). TV-13 under DV-2 is a plain text attribute, not a binding. G2 and R-M-04 still hold: naming and delegation are different functions with different verifier procedures |
| `AuthzCert` | **delegation**: extend authority to a principal over a scope | `trust` (5): `about` is the scope; `may-delegate` constrains onward delegation | Replaces `delegate: bool` (R-M-10, below) |
| `AclEntry` | **local policy**: the relying party's own root | not a statement. An unsigned local anchor in a context (`SPEC-0004` §4). A signed `trust` becomes an anchor only by a local act of acceptance (`ADR-0003` D3) | The anchor list is unsigned, so it has no speaker and is not a statement (P6). It is the fixed floor that `ARCH-0002` DEC-008 says cannot be key-local |
| `ArtifactStatement` | **attestation**: assert that a subject has attributes | `attestation` (4) about a digest or description target, a locator riding as an attribute; `review` (9), `approve` (10) and `aggregate` (11) about a statement or object | Acceptance may still require a delegation (§4.3 step 3). An `approve` counts only if its speaker reduces to a delegation for approval; a `review` never does |
| `Endorse` | **introducer weight**, PGP-shaped | none native. Import only (R-I-04, WP4) | An imported introducer becomes a `trust` only under an explicit import profile; otherwise it is evidence |
| — | **key lifecycle and vocabulary** | `key-publish` (1), `self` (2), `speaks` (3), `revoke` (6), `rotate` (7), `define` (8) | New in 0.2.0, from `SPEC-0002`. `define` publishes the definitions that DEC-007 relies on |

Delegation fields (logical), replacing v0.1's `AuthzCert`:

```
issuer:        Principal            # says; a KeyId at signature time (R-O-01)
subject:       Principal            # this = [1, kid], or the threshold form
scope:         [attribute-range]    # about; never empty. Was `tag`
may_delegate?: { depth?: uint,      # absent: one hop, no onward delegation
                 ranges?: [attribute-range],   # onward scope allow-list
                 allow_keys?, exclude_keys?,   # who may be delegated to
                 not_on_or_after? }            # earlier bound wins
validity:      Validity
```

Attestation fields (logical), replacing v0.1's `ArtifactStatement`:

```
issuer:       Principal            # says
subject:      ArtifactId | Key | Statement | Definition    # this
has:          [attribute]          # each attribute's type is a PredicateType
template?:    type-ref
validity:     Validity
```

This is the PICS analogue: issuer ≈ rating service; subjects ≈ labeled objects; predicate ≈ rating tuple; validity ≈ label lifetime; content binding is the artifact digest. The rating system, which v0.1 left out, is the definition (DEC-007).

### 4.3 Verifier inputs

A decision procedure takes:

- a request (`who` wants `tag` on `resource`, or “is statement S acceptable under policy P”);
- a set of certs/statements;
- a local ACL (`Self`);
- configured trust for *artifact services* (which issuers may assert which `PredicateType`s), held as per-context anchors (`SPEC-0004` §4; `ADR-0003` D4);
- current time and optional online validity checks.

Three procedures, kept separate (v0.1 said "two" and listed three):

1. **Name resolution** — rewrite `Name` to `KeyId` via chains of naming statements. Kept in 0.2.0 by decision (`DL-0028`); specified by `SPEC-0004` 0.6.0 §5.3 (mofn#143, `ADR-0008`).
2. **Authorization reduction** — SPKI-style composition after names are resolved. In KSA: delegation paths (`SPEC-0004` §6), scope narrowing by typed range, depth by `may-delegate`.
3. **Statement acceptance** — signature valid ∧ issuer authorized for that `PredicateType` ∧ subject digest matches the artifact under consideration ∧ every named template is conformed to (`SPEC-0003` §7.1).

(3) may call (2). They must not be collapsed into one graph walk. That held for v0.1 and still holds; `ADR-0002` §5 makes it explicit. Their results are reported separately (R-O-06), as `SPEC-0004` §10.4's `names`, `authorization` and `acceptance` lines.

---

### 4.4 The layer above — wallet, persona, definition

Additive pointer, 2026-10-14. The objects above are what a **statement** is. What
a person **holds and does** — a wallet of personas, each acting through keys in
contexts with their own trust anchors, and definitions identified by the hash of
their canonical encoding — is drafted in **ARCH-0003**. Nothing in §4.1–§4.3
changes; ARCH-0003 defers to this section.

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
| R-M-07 | M | Artifact statements SHALL bind at least one content digest. *0.2.0: kept as MUST by decision (`DL-0028`); a description digest (R-M-11) satisfies it, a locator alone does not. `SPEC-0002` 0.6.0 §7.2 meets it: every target type binds a digest, and the locator target is withdrawn (mofn#144, `DL-0030`).* |
| R-M-08 | M | Intersection (*within*) semantics SHALL be defined for every tag profile the implementation claims, and for every constrained type it accepts. *0.2.0: generalised from tags to every constrained object (`ADR-0002` §5, P2); `SPEC-0003` §6 base kinds meet it for the types they cover.* |
| R-M-09 | S | Validity intersection SHALL be defined (time window ∩ optional online checks). |
| R-M-10 | S | Delegation SHALL be explicit and bounded on the delegation statement: absent means one hop with no onward delegation; present, it SHALL state an integer `depth` and MAY state an onward scope allow-list (`ranges`), key allow/exclude lists, and a validity cap. Each hop's scope SHALL be within the previous hop's, and a widening SHALL be reported as such, not intersected silently to empty. *0.2.0: was "an explicit boolean (or equivalent)". Rewritten to match `SPEC-0002` §8.6 and `SPEC-0004` §6.3 by decision on mofn#136 (`DL-0025`). **Stated limit:** RFC 2693 §4.1.3–§4.1.4 rejected integer depth because the right depth cannot be predicted ("one can always need to go one more level down, by creating a temporary signing key") and because depth does not bound the width of the delegation tree. Both points stand. Depth is therefore **not a security bound**: it limits what a relying party will follow, not what a key holder can do. Width is limited by `ranges` and the key lists, which SPKI did not have. OpenPGP trust-signature levels (RFC 9580 §5.2.3.21) are the deployed precedent.* |
| R-M-11 | M | An `ArtifactId` SHALL support identification by content digest, by external locator, or by the canonical digest of a structured description. At least one content digest SHALL be bound in all cases, per R-M-07. A locator SHALL be treated as non-authoritative evidence about a subject, not as its definition. *Added 0.2.0 from the proposal. `SPEC-0002` §7.2 implements the modes as target 2 (digest), target 6 (description) and, for the locator, an attribute on either (0.6.0, mofn#144).* |
| R-M-12 | — | *Relocated: native extension points are key-relative. Accepted as `ARCH-0002` P1 by `ADR-0001`; not restated here.* |

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
| R-O-04 | C | Optional registration of statements with a SCITT-like transparency service (RFC 9943). |
| R-O-05 | M | The signed payload SHALL be the canonical encoding verbatim, carried with an authenticated type indicator. A verifier SHALL verify the signature before decoding and SHALL NOT canonicalize input as part of verification. Any human-facing form SHALL be regenerated from verified canonical bytes. *Added 0.2.0. Extends R-O-03: R-O-03 governs which algorithm, R-O-05 when it runs. `ADR-0003` and `SPEC-0002` §5 already cited it as accepted before this version carried it. That is a citation defect this version repairs.* |
| R-O-06 | S | Verifier output SHALL report name resolution, authorization reduction, and statement acceptance as distinct results, per §4.3, rather than a single combined outcome. *Added 0.2.0. `SPEC-0004` §10.4's six-line verdict meets it.* |

### 5.4 Documentation / process

| ID | Pri | Requirement |
|----|-----|-------------|
| R-D-01 | M | Architecture lives in this file (or a numbered successor). |
| R-D-02 | M | Accepted decisions move from “Open decisions” to an ADR file; this document then references them. |
| R-D-03 | M | Version bumps recorded in `ARCH-0001-CHANGELOG.md`. |

### 5.5 Where this document and the specifications differ

`ADR-0003`: where a SPEC and an ARCH document differ, the SPEC governs and the
ARCH document is corrected. 0.2.0 makes those corrections in §4 and §5. Two
differences went the **other** way by decision (`DL-0028`). In those cases this
document keeps its requirement, and the SPEC owes the change. Both are closed:
locator-only subjects, by `SPEC-0002` 0.6.0 (mofn#144, `DL-0030`); SDSI names,
by `SPEC-0002` 0.9.0, `SPEC-0003` 0.2.0 and `SPEC-0004` 0.6.0 (mofn#143,
`DL-0039`).

| Gap | ARCH-0001 | SPEC | Owed by | Issue |
|---|---|---|---|---|
| `Group` principal | §4.1 | no form | open; no consumer yet | — |
| `aliases` set | §4.1, R-M-11 | no form | `SPEC-0002`, when a consumer needs it | — |
| Online validity check | §4.1 `Validity.online_check`, R-M-09 | none; `valid` is time only | open; R-O-02 prefers short validity | — |

---

## 6. Interchange matrix (working)

Legend: **I** import, **E** export, **—** out of scope this version, **P** partial (lossy, must be flagged).

| Foreign object | I | E | Maps to native | Loss / notes |
|----------------|---|---|----------------|--------------|
| SPKI/SDSI S-exp cert (RFC 2693 / 9804) | I | E | NameCert, AuthzCert, Threshold | Closest peer; preferred reference mapping |
| OpenPGP key + UIDs + sigs | I | P | Key, NameCert, Endorse | No tag language; trust values are local to importer |
| X.509 EE / CA cert | I | — | Key + NameCert (DN as labels under a `x509:` namespace of the *importer*, not of the CA) + provenance | Do not treat CA bit as AuthzCert |
| X.509 attribute certificate | I | P | AuthzCert (tag profile TBD) | Attributes ≠ SPKI tags |
| in-toto Statement | I | E | attestation | Subjects = artifacts. **Export loss:** a `description` subject (R-M-11) has no in-toto digest-set form. `predicateType` URI ↔ `type-ref` is a lossy mapping (`ARCH-0002` P1) |
| DSSE envelope | I | E | wire only | Not an information-model type |
| COSE_Sign1 + CWT | I | E | wire + issuer/sub/exp | `kid` per `ADR-0005`. **Export loss:** key-relative identifiers map to registry-allocated COSE labels and CWT claim keys only lossily (`ADR-0004`; `ARCH-0002` P1) |
| SLSA provenance v1 | I | E | ArtifactStatement predicate | |
| SPDX / CycloneDX | I | E | ArtifactStatement predicate | |
| PICS label | I | — | ArtifactStatement | Historic; import profile only if needed |
| W3C VC | I | C | ArtifactStatement or NameCert depending on type | Context must be pinned |
| SCITT receipt (RFC 9943) | I | C | evidence attached to an attestation | Does not change meaning of statement |

**Forbidden native mapping:** X.509 certificate path validation as the native reducer.

---

## 7. Open decisions

Do not treat any option below as selected.

### DEC-001 — Working title / repo slug

**Status: accepted 2026-11-06 — org and working title `m-of-n`, repository, package and CLI `mofn`, by [`ADR-0006`](ADR-0006-dec-001-slug.md).** None of the options below was chosen. The text is kept as the record of what was decided between. NG3 still holds: the slug is accepted, not frozen.

Options: `spki3`, `open-sdsi`, `kofn-certs`, `localnames`, `sudsy`.  
Blocked on: none.  
Affects: packaging only.

### DEC-002 — Concrete native encoding

**Status: accepted 2026-10-25 — option 5, by [`ADR-0004`](ADR-0004-dec-002-encoding.md).** The text below is kept as the record of what was decided between.

Options:

1. Canonical S-expressions (RFC 9804) as canonical; JSON as diagnostic.
2. CBOR + CDDL as canonical; COSE for signed form.
3. JSON + RFC 8785 JCS as canonical; DSSE for signed form.
4. Dual canonical (CBOR and JSON) with a documented bijection.
5. *(Added with `ADR-0004`; drafted in `ARCH-0001-PROPOSAL-v0.2.0` §3.3.)* CBOR data model under RFC 8949 §4.2.1, restricted and decoder-enforced, with no IANA registry native; COSE and DSSE as export envelopes only.

Drivers: library availability, SCITT alignment, SPKI fidelity, human debug.  
Acceptance test: round-trip fixtures for NameCert, AuthzCert (including threshold subject), ArtifactStatement.

**Inputs the DEC-002 ADR must answer** — added 0.1.3 from the CBOR/COSE
extraction (mofn#112; library records at `bafd536`). Additive. No option is
selected, ranked or withdrawn here.

- **A driver the list above omits: detectability of an order-only divergence.**
  RFC 8747 §3.3's worked example does not reproduce, and the cause is map order
  alone: the ciphertext authenticates and re-encrypts to every printed octet,
  but its plaintext is ordered `3, 1, -1` where the document prints the
  RFC 8949 §4.2.1 order `1, 3, -1` (library `rfc-8747` cut B). The record ranks
  option 1 ahead of option 3 ahead of option 5 on this ground — the reverse of
  MD-3's narrowing. Under option 5 as `SPEC-0002` §4.2–§4.3 profiles it, an
  order-only divergence **is** a rejection (V5, `encoding`), but only because
  the profile states the rule; a decoder that omits it still parses every valid
  document. That is the difference in kind `DECISIONS-0001` item 2 already
  records for condition (2). The ADR scores this driver by name.
- **"No IANA tags" is a rule of our profile, not a property of the format.**
  The COSE_Encrypt0 tag is optional — 71 octets untagged against 72 tagged
  (`rfc-8747` cut A, corroborating `rfc-8392` cut 3) — so the property holds
  only because `SPEC-0002` §4.1 forbids major type 6 and §4.3 rejects it. Nor
  does it reach registry dependence outside the tag space: COSE algorithm
  identifiers, CWT claim keys, confirmation methods. The ADR states option 5's
  no-registry property as the list of registries it excludes, not as "no tags".
- **The acceptance test names an invariant no schema language checks.**
  `Threshold`'s `1 ≤ k ≤ n` and `n = len(members)` (§4.1) are not expressible
  in CDDL (`rfc-8610`); options 1 and 3 ship no schema language, so this scores
  against no option. It is a defect in the **test**: the threshold fixture's
  expected-results file carries the invariant as positive and negative cases
  (`k = 0`, `k > n`, `n ≠ len(members)`), and the component that owns the check
  is named — `SPEC-0002` V8, *"`trust`: target and threshold form"* (§8.6
  writes `k` as `threshold` and `n` as the length of `trusts`).

  **Fixture landed 0.1.6** (T-031, `DL-0019`). TV-9…11 are the positives; N-7
  (`k = 0`) and N-8 (`k > n`) fail at V8, which owns `1 ≤ k ≤ n`. V8 cannot own
  `n = len(members)`: §8.6 has no `n` field, because `n` *is* the array head of
  `trusts`, so that clause holds by construction. Its two possible spellings
  fail earlier: N-9, an added field, at V7 (closed map); N-10, a head that
  disagrees with its items, at V5. This comes from §8.6's shape, not the
  encoding, so it is not a defect in option 5.

  The other roles of the acceptance test: `ArtifactStatement` is TV-4;
  `NameCert` is TV-13, an `attestation` about a key (`ARCH-0002` P6, `[draft]`).
  `ADR-0004`'s "met" list omits `NameCert`, and TV-1 and TV-2 do not supply it:
  `self.label` is *"not a binding"* (`SPEC-0002` §8.3). Every positive vector
  round-trips in `prototype/wallet/tests`. **Still owed:** `trusts: [A, A]` with
  `threshold: 2` passes V8, since `SPEC-0002` has no distinctness rule and
  `SPEC-0004` §6.4 counts distinct kids. It fails closed; it goes to `SPEC-0002`
  with condition (5).

### DEC-003 — Issuer / subject identifiers on the wire

**Status: accepted 2026-10-25 — `kid` = SHA-256 of the suite's public-key encoding, by [`ADR-0005`](ADR-0005-dec-003-key-identifier.md).** The text below is kept as the record of what was decided between.

Options: raw COSE key; COSE key thumbprint; `did:key`; hash-uri (`sha256:…`); text KeyId.

Must specify: canonical key bytes before hashing.

**Inputs the DEC-003 ADR must answer** — added 0.1.3 from the CBOR/COSE
extraction (mofn#112). Additive. No option is selected.

`SPEC-0002` §4.5 specifies `kid = SHA-256(public-key encoding under the
suite)`, the encoding fixed per suite (§6.3: RFC 8032 §5.1.2; §6.5: FIPS 204).
`ADR-0003` makes the SPECs govern; it does not accept this decision, and the
findings below are what the ADR weighs that derivation against.

- **COSE key thumbprint (RFC 9679) is not native-eligible as written.** Its
  preimage is a registry-labelled `COSE_Key`, which `ARCH-0002` P1 places at
  interchange. For RSA, Symmetric and HSS-LMS a single representation must be
  pinned — RFC 8230 §4 and RFC 8778 §2.1–§2.2 already pin two, and Symmetric
  `k` has nothing to normalise. For AKP, the only post-quantum key type, `alg`
  is inside the digest and RFC 9679 offers no subset that excludes it; that is
  not ours to fix (library `rfc-9679`).
- **A post-quantum COSE thumbprint contains an IANA allocation.** For ML-DSA
  the COSE Algorithms values −48/−49/−50 sit inside the preimage at offsets
  4–5, offset 5 being the allocation itself (`2f`, `30`, `31`; `rfc-9964`
  cut B). That is `ADR-0001`'s rejected private-use escape arriving by another
  route: the identifier carries a registry number in its bytes. Hashing the
  suite's raw key encoding, as `SPEC-0002` does, avoids it.
- **The inverse question, which RFC 9679 does not reach.** Its AKP defect is an
  algorithm *inside* the preimage; `SPEC-0002`'s `kid` has none, so identical
  key octets under two suites yield one `kid`. Today's suites cannot collide
  (32 against 1952 octets). Whether a future suite with an equal-length
  encoding needs the suite in the preimage is for this ADR; not answered here.
- **RFC 8747 §3.4 is not an option.** It names a hash of the public key with no
  algorithm, encoding, parameter subset or truncation, and its own example
  `kid` is not SHA-256 of its key under six encodings tried (`rfc-8747`). It is
  evidence about what a COSE `kid` is — `ARCH-0002` P1.1 — not a derivation.

### DEC-004 — Tag language (authorization)

Options:

1. SPKI tag S-expressions as-is (byte-string sets + intersection).
2. Constrained JSON tags with explicit ∩ operator.
3. Embed a small policy subset (e.g. in-toto layout step names, or SPDX purpose).

v0.1 may ship **tag as opaque byte string** plus one profile (`urn:…:tag:bytes-equal`) so reduction can be implemented before the language is rich.

### DEC-005 — Envelope for ArtifactStatement

Options: DSSE (in-toto world), COSE_Sign1 (SCITT world), both with a single unsigned payload schema.

### DEC-006 — withdrawn before filing

Drafted in `ARCH-0001-PROPOSAL-v0.2.0` rev.1 as "authoring and display surface".
Withdrawn on sponsor review, 2026-09-16: no human authoring format is
required, since statements are produced by tools. Display was folded into
DEC-007. Recorded so the number is not reused.

### DEC-007 — Predicate rendering, vocabulary resolution, and display

**Status: accepted 2026-11-07 — option 2, by [`ADR-0007`](ADR-0007-dec-007-predicate-rendering.md),
as `SPEC-0003` implements it.** Filed and accepted in the same version (0.2.0).
The text below is the record of what was decided between.

Question: how does a `PredicateType` convey the human-readable meaning of the
values a `Predicate` carries, so that a user interface can render a statement
without type-specific code?

Options:

1. Out of scope. `PredicateType` identifies a schema; display is an application concern.
2. A signed, versioned, dereferenceable **vocabulary statement**, itself a
   statement by the key that defines the type, declaring categories, permitted
   values, scales and a human-readable rendering for each value. Statements cite
   it by identifier and digest.
3. As option 2, with rendering strings carried inline in each statement.
4. Reuse an existing vocabulary mechanism (SKOS, JSON-LD contexts, SHACL).

Acceptance test: two unrelated predicate types, one build-provenance and one
non-software, render legible statements through a single renderer with no
type-specific code. Under option 2, changing a rendering must not invalidate
existing signatures and must be detectable as a vocabulary version change.
`ADR-0007` records which clauses are met and which are owed.

**DEC-007 and DEC-004 must not be collapsed.** A tag language (DEC-004) needs an
intersection operation, because that is what reduction composes; it need not be
legible. A rendering vocabulary needs legibility and versioning; it has no
intersection semantics, and asking for one is a category error. Both are
key-relative under `ARCH-0002` P1, and both are *types* in the P3 sense. That is
their common principle. It is not a reason to merge them.

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
- RFC 9943 — SCITT architecture (Proposed Standard, June 2026); was `draft-ietf-scitt-architecture`  
- in-toto Attestation Framework v1  
- SLSA provenance v1  
- W3C PICS (label format, signed labels, content checksum)  
- Ellison, “SPKI/SDSI and the Web of Trust” comparison notes  
- OpenPGP / GnuPG trust-signature model (meta-introducers)  
- C2PA 2.4 (April 2026) — where C2PA is cited downstream (§2.3.3)  
- CDDL, if reached: RFC 8610 as updated by RFC 9165 and RFC 9682  
- `draft-mih-scitt-agent-action-capsule-02` — ad hoc vocabulary inside SCITT (§3.3)  
- RFC 9580 — OpenPGP (2024): §3.7, §5.2.3.7, §5.2.3.21, §5.2.3.24, §5.2.3.29, §5.2.5, §5.5.3, §5.5.4.3 (read for §3.4)

End of ARCH-0001 v0.3.1
