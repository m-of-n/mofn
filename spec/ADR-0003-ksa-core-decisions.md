---
schema: "archdoc/v1"
id: ADR-0003
title: "KSA core design decisions"
short_title: "ADR-0003 KSA core decisions"
description: "The decisions the KSA specifications rest on: key-relative, hash-identified types; one canonical encoding; signed-or-unsigned trust anchors accepted by a human-controlled persona; trust per context; and issuer revocation."
type: decision
category: security
status: accepted
version: "1.0.1"
version_policy: "semver; an accepted ADR changes only by superseding it"
date: "2026-10-14"
updated: "2026-10-17"
decision_makers:
  - role: sponsor
    id: paul-lambert
reviewers: []
needs_review: false
reviewed: true
canonical_path: spec/ADR-0003-ksa-core-decisions.md
defers_to: ARCH-0001
supersedes: []
---

# ADR-0003 — KSA core design decisions

**Status: accepted.** Sponsor decisions of 2026-10-14. Restated editorially on
2026-10-17 to name the protocol KSA throughout; no decision changed.

## Context

Two drafts addressed the same design problem — key-centric signed statements
whose meaning a person can read — and are merged into one protocol, **KSA
(Key-centric Semantic Attestations)**, specified in SPEC-0001 to SPEC-0005 and
UC-0001. One draft was exact about bytes: an ordered statement envelope, a strict
data model, cipher suites with domain-separated signatures, schema-typed
attribute assignments and ranges, delegation with depth and range constraints,
revocation, rotation, and a verifier that answers yes or no with reasons. The
other was ahead on semantics, on subjects other than keys, on signed definitions,
and on process and dataflow. KSA keeps the best of each; these are the points on
which they had to be decided.

## Decision

| # | decision | consequence |
|---|---|---|
| **D1** | **Type identity is key-relative and hash-identified.** A type is identified by the `DefinitionId` — the hash of its definition's canonical encoding — and a label local to that definition's definer. No URN identifiers and no namespaced extension fields. | Keeps ADR-0001 (P1). All extensibility is through definition-typed attributes. |
| **D2** | **One canonical encoding** for every signed or hashed object, statements and definitions alike. | KSA-CBOR (SPEC-0002 §4). **This ADR does not accept DEC-002**; the DEC-002 ADR and its fixtures still decide the encoding. |
| **D3** | **Trust anchors may be signed or unsigned.** An anchor may be an unsigned local decision, the owner's own trust statement, or a trust statement signed by any key — including a third party — that has been **verified and then accepted** into a context's anchor list. **Acceptance is a local act by a persona whose controller is a person or organisation.** | A signature on a proposed anchor says who proposed it; it never makes an anchor. Amends ARCH-0003 W-07. Normative form: SPEC-0004 §4. |
| **D4** | **Trust is evaluated per context.** Every evaluation is relative to one context's anchors. | A key trusted for one purpose gains nothing elsewhere. |
| **D5** | **Issuer revocation**: a `revoke` statement by the issuer, naming the revoked statement's digest, effective from its `not before`. | Short validity remains recommended; revocation distribution is not solved here. |

**Adopted by the specification, under accepted ARCH-0001 R-O-05 rather than by
this ADR:** the canonical binary is what is signed and transmitted. The producer
encodes once, signs those bytes, and transmits them unchanged; the verifier checks
the signature over the bytes received before decoding them, and rejects any that
are not already canonical. The human-review form represents those bytes exactly
and converts one-to-one to them for signing (SPEC-0002 §5, §11).

## Alternatives rejected

- **Sign a re-encoded statement.** It makes the verifier canonicalise during
  verification and run its decoder on unauthenticated input (R-O-05).
- **Subjects limited to keys.** It cannot attest about an artifact or review a
  statement.
- **Unsigned vocabulary documents.** Whether to rely on a vocabulary would not be
  a trust question; KSA publishes definitions with a signed `define` statement.

## Consequences

- SPEC-0001 to SPEC-0005 and UC-0001 are the normative specifications.
  ARCH-0001/0002/0003 remain the design record; where they differ, the SPEC
  governs and the ARCH document is corrected.
- ARCH-0003 W-07 is amended by D3.
