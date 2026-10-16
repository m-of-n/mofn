---
schema: "archdoc/v1"
id: SPEC-0001
title: "KSA Architecture — principals, wallets, contexts, presentations and discovery"
short_title: "KSA Architecture"
description: "The architecture of Key-centric Semantic Attestations: personas as key-identified principals controlled by people, organisations, services, agents or devices; wallets that own some personas and know others; contexts; the document set and its conformance classes; presentations and transport; the key discovery and trust lifecycle; and system-level security and privacy."
type: specification
category: security
status: draft
version: "0.1.0"
version_policy: "semver; MAJOR = a change that breaks a conformance class; MINOR = additive; PATCH = editorial"
date: "2026-10-14"
updated: "2026-10-14"
decision_makers:
  - role: sponsor
    id: paul-lambert
reviewers: []
needs_review: true
reviewed: false
canonical_path: spec/SPEC-0001-ksa-architecture.md
companion:
  - spec/SPEC-0002-ksa-core.md
  - spec/SPEC-0003-ksa-definitions.md
  - spec/SPEC-0004-ksa-trust-evaluation.md
  - spec/SPEC-0005-ksa-processes.md
  - spec/UC-0001-ksa-use-cases.md
  - spec/ADR-0003-fksa-convergence.md
defers_to: ARCH-0001
related_rfcs: [RFC2119, RFC8174, RFC9180, RFC9334]
---

# KSA Architecture — principals, wallets, contexts, presentations and discovery

**Specification SPEC-0001 · version 0.1.0 · draft**

## Abstract

KSA (Key-centric Semantic Attestations) lets any key make signed statements about
keys, artifacts, documents and other statements; lets anyone publish, by hash,
what those statements mean in words a person can read; and lets a relying party
decide — from anchors it chose, in a context it chose — whether the key that
said something was entitled to say it. This document is the entry point to the
KSA specifications. It defines the principals (personas) and their controllers,
the wallet that holds them, contexts, the conformance classes, presentations and
the transport beneath them, and the lifecycle by which a wallet discovers a key,
decides whether to trust it, and maintains that decision.

## Status of this document

Draft for review in the m-of-n project. The KSA core is based on FKSA v0.2.1
(ADR-0003). The design record is ARCH-0001, ARCH-0002 and ARCH-0003; where a
specification and an architecture document differ, the specification governs.

---

## 1. Introduction

### 1.1 The problem

A digital signature proves that a key signed some bytes. It does not say who
holds the key, whether that key was entitled to make the claim, or what the
claim means. Deployed systems answer those questions out of band — a certificate
authority's root store, a command-line flag naming the expected signer, a
specification that fixes a vocabulary — and a statement can be correctly signed
by a key with no standing to make it. KSA makes the three answers part of the
protocol.

### 1.2 Design principles

1. **A principal is a key.** Identity, authority and naming are all relative to
   keys; there is no global namespace and no global root (ARCH-0002 P1).
2. **Meaning is published, hashed and readable.** Every type a statement uses is
   defined by a key, identified by the hash of its definition, and described in
   words (SPEC-0003).
3. **Authority narrows.** Trust is extended about a scope, and every delegation
   can only narrow it (SPEC-0004 §6).
4. **Trust begins locally.** A relying party decides its anchors, per context; a
   signature never makes an anchor (SPEC-0004 §4).
5. **Verify the bytes before reading them.** Signatures are checked over the
   bytes received, and nothing is canonicalised during verification
   (SPEC-0002 §5).
6. **Unknown is an error.** What a verifier does not understand is never skipped
   (ARCH-0002 P5).
7. **The answer explains itself.** Every decision comes with its reasons and a
   verdict a person can read (SPEC-0004 §10).

### 1.3 Scope

In scope: statements, definitions, trust evaluation, processes, wallets,
presentations, discovery. Out of scope for this version: the binary transport
codec and fragmentation (FKSA's binary/transport specification), revocation
distribution, selective disclosure, and multi-speaker contracts (ARCH-0002
DEC-009).

## 2. Conventions and terminology

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when,
and only when, they appear in all capitals, as shown here.

| term | meaning | defined in |
|---|---|---|
| **persona** | a principal identified by a key | §3 |
| **controller** | what operates a persona's key: person, organisation, service, AI agent, software, device | §3.2 |
| **wallet** | holds personas — owned and known — definitions and statements | §6 |
| **owned / known persona** | a persona whose private key the wallet holds / whose public key only it holds | §6.1 |
| **context** | a wallet-local scope with its own trust anchors | §6.3 |
| **role** | what a key does in one statement: define, claim, delegate, review, approve, present, rely | §3.3 |
| **statement**, **TBS**, **envelope**, **kid** | | SPEC-0002 |
| **definition**, **DefinitionId**, **template** | | SPEC-0003 |
| **anchor**, **path**, **verdict** | | SPEC-0004 |
| **panel**, **process**, **aggregate** | | SPEC-0005 |
| **presentation** | statements and definitions handed to a relying party | §8 |

## 3. Principals: personas and controllers

### 3.1 Personas

A **persona** is a key-identified principal: the key or keys that speak as it,
together with the contexts it acts in and the contexts it trusts. A persona is
named on the wire by the kid of its **identity key**. Further keys — per context,
per device, per protocol — are delegated from the identity key by ordinary trust
statements (SPEC-0002 §8.6), so a compromise of an operational key is bounded by
the scope and validity it was given.

A persona is visible on the wire exactly as its keys. Two personas are unlinkable
only if they share no key and no statement links them; a person who needs
unlinkable identities MUST use separate personas with separate identity keys.

### 3.2 Controllers

A persona's **controller** is whatever operates its private key:

| controller | examples |
|---|---|
| person | a maintainer, a reviewer, a reader |
| organisation | a company or project acting through delegated keys |
| service or script | a CI build system, a server, a scheduled job |
| AI agent | an agent acting on someone's behalf |
| software implementation | a tool that signs what it produces |
| hardware device | a TPM, secure enclave, HSM, or embedded device |

A persona MAY state its controller kind in its `self` statement (SPEC-0002 §8.3).
That is a **claim**. Stronger evidence is an attestation by a key the relying
party trusts, or a device attestation that the key is held in specific hardware
(RATS [RFC9334]). Evaluators record which they relied on (SPEC-0004 §4.5).

**AI agents are personas, and are never roots of authority.** An agent's
authority must reduce, through delegation, to a person or an organisation
(SPEC-0004 §9). An agent-controlled persona does not accept trust anchors by
default (SPEC-0004 §4.4).

### 3.3 Roles

A role is what a persona's key does in one statement. One persona plays every
role, in different statements and contexts; a role is never a property of the
persona.

| role | statement | specified in |
|---|---|---|
| define | `define` | SPEC-0003 §11 |
| claim | `attestation`, usually from a template | SPEC-0002 §8.5, SPEC-0003 §7 |
| delegate | `trust` | SPEC-0002 §8.6, SPEC-0004 §6 |
| introduce | `attestation` or `self` about a persona | §9.1 |
| review | `review` | SPEC-0002 §8.10 |
| approve | `approve` | SPEC-0002 §8.10, SPEC-0005 |
| aggregate | `aggregate` | SPEC-0005 §6 |
| present | a presentation | §8 |
| rely | an ask, locally | SPEC-0004 §10 |

## 4. Document set and conformance

### 4.1 Documents

| document | specifies |
|---|---|
| **SPEC-0001** (this) | architecture, personas, wallets, contexts, presentations, discovery |
| **SPEC-0002** KSA Core | data model, canonical encoding, envelope, cipher suites, statement kinds, single-statement verification |
| **SPEC-0003** KSA Definitions | definitions, types, base kinds, constraints, templates, rendering |
| **SPEC-0004** KSA Trust Evaluation | contexts and anchors, delegation paths, thresholds, revocation, rotation, ask and answer, verdict |
| **SPEC-0005** KSA Processes | panels, criteria, aggregates, downstream |
| **UC-0001** Use cases | scenarios traced to the specifications |

### 4.2 Conformance classes

An implementation claims one or more classes and MUST meet every requirement of
the sections listed for each.

| class | must implement |
|---|---|
| **Statement Producer** | SPEC-0002 §4–§8, §11 |
| **Statement Verifier** | SPEC-0002 §4, §5, §6, §9, §10; passes SPEC-0002 Appendix A |
| **Definition Publisher** | SPEC-0003 §4–§9, §11 |
| **Definition Renderer** | SPEC-0003 §4.2, §9, §10 |
| **Trust Evaluator** | Statement Verifier, Definition Renderer, SPEC-0004 |
| **Process Evaluator** | Trust Evaluator, SPEC-0005 |
| **Wallet** | all of the above, and SPEC-0001 §5–§9 |

## 5. Keys and cipher suites

### 5.1 Keys as objects

A key belongs to exactly one cipher suite (SPEC-0002 §6). A wallet records, for
each key of an owned persona, its custody (an encrypted file, hardware, derivation
from a seed, or a remote signer), the **capabilities** it may be used for — which
roles, and in which contexts — and its state (active, retired, compromised). A
wallet MUST refuse to sign with a key outside its recorded capabilities.
Externally, a key's authority is never read from this record: it is established
only by trust evaluation.

### 5.2 Suites

A wallet MUST support suite 1 (`ksa-ed25519-sha256`) and SHOULD support a
post-quantum suite once one is final in SPEC-0002. Statements that must remain
verifiable for decades SHOULD be made under a post-quantum suite or anchored to
an external timestamp (§11).

### 5.3 One key, several protocols

A key may also be used outside KSA — for TLS, email, payments, or a ledger such as
Bitcoin, whose transactions are statements in another syntax. Because every KSA
signature binds its domain-separation label (SPEC-0002 §6.4), a KSA signature
cannot be replayed in a protocol that also domain-separates. Even so, reuse
couples the risk of the protocols: a compromise in one is a compromise in all.
A wallet SHOULD use a separate key per protocol — derived from one seed where
convenient — and MUST record on the key any use outside KSA.

A wallet MAY import a signed object from another protocol as an **external
statement**, keeping its original bytes and mapping its speaker, subject and
claims through an interchange profile (ARCH-0001 §6), so that it can be reasoned
about by the same evaluation.

### 5.4 Private notes

A wallet MAY keep private notes about any key — how it was met, a reminder, a
display colour. Private notes MUST NOT appear in any statement and MUST NOT be
transmitted.

## 6. Wallets and contexts

### 6.1 Owned and known personas

A wallet holds personas. It **owns** those whose private keys it holds, and
**knows** others: people, organisations, services, agents and devices whose
public keys and statements it has met. Owned and known personas are both
principals; the only difference is that the wallet can sign for the first.

### 6.2 What a wallet holds

| item | for |
|---|---|
| owned personas | their keys, capabilities, contexts and anchors |
| known personas | their keys, controller evidence, discovery provenance (§9.3), private notes |
| key store | (suite, kid) → public key, populated only as SPEC-0002 §10 allows |
| definitions | by DefinitionId, each checked on load (SPEC-0003 §4.2) |
| statements | made, received, and accepted — each kept as its exact envelope bytes |
| acceptance records | for each statement relied on: the verdict, the context, and the anchors used |

### 6.3 Contexts

A context is a named scope in which an owned persona acts and relies: the keys
enabled there, the definitions in use, the templates offered for issuing, and
**that context's anchors** (SPEC-0004 §4). Trust in one context gains nothing in
another (ADR-0003 D4). A statement made in a context is signed only with a key
enabled for it; a presentation from a context discloses only statements held in
it.

A persona MAY publish that it acts in a context, as a `self` or `speaks`
statement. Its anchors stay local unless it chooses to publish them as its own
trust statements.

## 7. The human interface

### 7.1 Phases

A conforming wallet provides an interface for each phase, and the interface for
each MUST make the listed point unmistakable.

| phase | the interface MUST make unmistakable |
|---|---|
| set up a persona | which keys exist, under which suite, what each may sign; that private keys stay on the device |
| discover and trust (§9) | that **known is not trusted**; how and when a persona was met; who asserts its controller kind |
| define (SPEC-0003) | the DefinitionId, computed and signed on publication; that a published definition is immutable |
| claim (SPEC-0003 §7) | who is speaking — persona, context and key; the sentence the statement will render as |
| delegate (SPEC-0004 §6) | the scope, the depth, who may receive it, and the expiry, in words |
| review and approve (SPEC-0005) | that a review is not an approval; the definition's review questions as a checklist |
| present (§8) | exactly which statements and definitions will be disclosed, and to whom |
| check and accept (SPEC-0004 §10) | the six verdict lines, with **authorization** shown separately, and the limit line |
| trust settings | that anchors are this persona's own decisions, distinct from every statement |

### 7.2 Review questions

Where a type defines review questions (SPEC-0003 §5.4), a wallet presenting a
statement for review or approval SHOULD show them as a checklist before the
reviewer signs.

### 7.3 Rendering a persona

A wallet MUST render a key by the relying persona's own label for it, if it has
one, or by a fingerprint of its kid. It MUST NOT render a key by the key's
self-asserted label alone; where it shows a self-asserted label, it MUST mark it
as self-asserted.

## 8. Presentations and transport

### 8.1 Presentation

A **presentation** is what a persona hands a relying party: the statements needed
to answer an ask — the claim, its delegation path, any reviews and approvals —
and the definitions needed to render and type-check them.

```
presentation = {
  1 statements:  [+ signed-statement],          ; SPEC-0002 §5
  ? 2 definitions: [+ bstr],                    ; definition bodies, KSA-CBOR
  ? 3 audience:  kid,
  ? 4 nonce:     bstr,
  ? 5 created:   time
}
presented = [ presentation: bstr .cbor presentation, presenter: kid, sig: bstr ]
```

`presented` is OPTIONAL. When present, `sig` is a **proof of possession**: the
presenter's signature over `KSA-POP-SIG-v1\0 ‖ presentation`, under the
presenter's suite. A relying party that supplied a nonce MUST check that the
presentation carries it and that `audience` is its own kid. A presentation
without a proof of possession is still evaluable: every statement in it protects
itself.

### 8.2 Transport

Statements protect their own integrity and authenticity, so **the transport is
untrusted** and the verdict is the same however a statement arrived. A transport
provides delivery, confidentiality where needed, and request–response exchanges.

| transport | status | notes |
|---|---|---|
| file, QR code, clipboard | REQUIRED | offline; no infrastructure |
| wallet-to-wallet mailbox | OPTIONAL, provisional | store-and-forward between wallets, addressed by kid; messages encrypted to the recipient persona's key with HPKE [RFC9180]; the relay sees only ciphertext and a recipient kid |
| email | OPTIONAL | a presentation carried as an attachment of media type `application/ksa-presentation` |

A transport that encrypts requires the recipient's suite to define key exchange,
which KSA's suites do not yet do (FKSA and R-0003 leave it empty until a session
protocol exists). The mailbox is therefore provisional, and its messages — offer,
possession challenge and proof, review request and response, approval request,
introduction — will be published as a KSA definition (SPEC-0005) when it is
specified.

## 9. Discovery and the key lifecycle

A wallet cannot believe a statement from a key it has never met, and MUST NOT
believe one because it has now met it. **Discovery never confers trust.**

### 9.1 Encounter

A public key reaches a wallet by: direct exchange (scanned in person, a file);
inside a presentation; an **introduction** — a statement by a persona already
known, naming the new key; a directory, `.well-known` location or transparency
log; the transport; or a device attestation. A directory, location or log is a
locator only (SPEC-0003 §4.4).

### 9.2 Verify the binding

The wallet verifies the key's `key-publish` and `self` (SPEC-0002 §9). It SHOULD
obtain a **proof of possession** over a fresh nonce (§8.1). The persons involved
MAY compare fingerprints out of band; an interactive comparison with a hash
commitment (as Matrix's SAS does) is RECOMMENDED over reading raw fingerprints.
This establishes that the key is controlled by whoever answered — not who that is.

### 9.3 Record, with provenance

The key is stored in the key store (SPEC-0002 §10) and the persona as **known**,
with its provenance: how, when and from whom it was learned, and whether
possession and fingerprints were checked. Known is not trusted.

### 9.4 Decide trust

Trust enters only through an anchor in a context, or a path from one
(SPEC-0004 §4, §6). An anchor is made locally, from the owner's own trust
statement, or by accepting a third party's signed trust statement under
SPEC-0004 §4.4.

### 9.5 Use

Statements from the key are evaluated by SPEC-0004, and every one relied on is
recorded with its verdict and the anchors used.

### 9.6 Maintain

- **Rotation.** A `rotate` from a trusted key moves trust to its successor
  (SPEC-0004 §7.2).
- **Expiry.** Statements and anchors lapse with their validity windows.
- **Revocation.** A speaker withdraws its own statements (SPEC-0004 §7.1).
- **Compromise.** A wallet owner MAY mark a key compromised. From the mark, the
  key's rotations are ignored, its later statements are not used, anchors naming
  it are suspended, and every acceptance record that relied on it is re-evaluated.

## 10. Security considerations

The detailed considerations are in each specification. At system level:

- **No global root.** A compromise of any one key compromises only what that key
  was trusted about, in the contexts that trusted it.
- **Anchor injection** is defeated by acceptance (SPEC-0004 §4.4), not by
  signatures.
- **Social engineering of delegation** — a patient attacker who earns a
  delegation, as in the 2024 xz-utils incident — is limited by narrow scope,
  shallow depth, short validity and approval processes, not prevented.
- **Correct signatures by an entitled key on false claims** are not detected: the
  verdict's limit line says so.
- **Agents**: an agent's statements are only as trusted as the human or
  organisational delegation they reduce to.

## 11. Long-term verification

A statement verified decades after signing must withstand the cryptanalysis of
the intervening years, including a cryptographically relevant quantum computer.
For such statements a wallet SHOULD use a post-quantum suite, or obtain an
independent timestamp — a transparency-log receipt or a timestamp token — proving
the statement existed before its suite was weakened. `valid.issued` is the
speaker's own claim and is not such evidence.

## 12. Privacy considerations

- A kid links every statement made with that key.
- `self` statements publish a label and a controller kind.
- Trust statements published by a persona reveal its relationships; anchors are
  local by default.
- A presentation discloses exactly its contents; wallets show it before sending.
- Directory and `.well-known` discovery trade reach for exposure; a persona
  chooses which of its keys and statements to publish.

## 13. References

### 13.1 Normative
- [RFC2119], [RFC8174] — BCP 14.
- [SPEC-0002], [SPEC-0003], [SPEC-0004], [SPEC-0005].

### 13.2 Informative
- [RFC9180] Barnes, R. et al., "Hybrid Public Key Encryption", RFC 9180, February 2022.
- [RFC9334] Birkholz, H. et al., "Remote ATtestation procedureS (RATS) Architecture", RFC 9334, January 2023.
- [FKSA] Lambert, P., "FKSA Core Specification v0.2.1", "FKSA Lifecycle v0.1", "Related Work: Matrix and FKSA v0.1", sponsor drafts, October 2026.
- [ARCH-0001], [ARCH-0002], [ARCH-0003] — design record.
- [R-001] "What a Signature Proves: A Survey of Digital Signatures and Attestation", m-of-n, 2026.

---

## Appendix A. Relationship to FKSA and to the design record

| | FKSA v0.2.1 | KSA |
|---|---|---|
| core statement, data model, suites, time, delegation, revocation, rotation, ask/answer | specified | adopted, with the changes listed in SPEC-0002 Appendix C |
| subjects | keys only | keys, artifacts, statements, definitions, locators, descriptions |
| vocabularies | schemas by URN or JCS hash, unsigned, no human-readable semantics | definitions by KSA-CBOR hash, signed, mandatory multilingual semantics (SPEC-0003) |
| trust roots | the relying party's signed trust statements | per-context anchors: local, own, or accepted third-party (SPEC-0004 §4) |
| processes | none | panels, criteria, aggregates (SPEC-0005) |
| lifecycle | phases 0–9 for four people | §9, generalised to any controller |

ARCH-0001 records the original information model and requirements; ARCH-0002 the
principles (P1 accepted by ADR-0001); ARCH-0003 the wallet and process design.
ARCH-0003 W-07 is amended by ADR-0003 D3.
