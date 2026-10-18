---
schema: "archdoc/v1"
id: ADR-0003
title: "KSA adopts the FKSA core, with five decisions on where they differ"
short_title: "ADR-0003 FKSA convergence"
description: "Accepts FKSA v0.2.1 as the base of the KSA core protocol, and records five sponsor decisions: key-relative type identity, one canonical encoding, signed-or-unsigned anchors accepted by a human-controlled persona, trust per context, and issuer revocation."
type: decision
category: security
status: accepted
version: "1.0.0"
version_policy: "semver; an accepted ADR changes only by superseding it"
date: "2026-10-14"
updated: "2026-10-14"
decision_makers:
  - role: sponsor
    id: paul-lambert
reviewers: []
needs_review: false
reviewed: true
canonical_path: spec/ADR-0003-fksa-convergence.md
defers_to: ARCH-0001
supersedes: []
---

# ADR-0003 — KSA adopts the FKSA core

**Status: accepted.** Sponsor decision, 2026-10-14, on the contrast between the
architecture (ARCH-0001/0002/0003) and the sponsor's FKSA draft v0.2.1
(Federated Keyed Signed Attestations; core v0.2.1, lifecycle v0.1, related work
v0.1).

## Context

FKSA is a precise, implemented wire protocol for key-centric attributes:
an ordered statement envelope, a strict data model, cipher suites with exact
signed bytes and domain-separation labels, schema-typed attribute assignments
and ranges, scoped delegation with depth and range constraints, revocation,
rotation, and a verifier that answers yes or no with structured reasons. It has
a reference verifier and an end-to-end scenario with real signatures.

The architecture documents are ahead of FKSA on semantics (human-readable,
multilingual vocabularies), on subjects other than keys, on signed definitions,
and on process and dataflow. Where the two overlap, FKSA is more exact. Five
points conflicted.

## Decision

**The KSA core protocol (`SPEC-0002`) is based on FKSA core v0.2.1.** KSA takes
FKSA's envelope discipline, data model, suite registry, domain-separation labels,
strict Ed25519 rules, time encoding, attribute assignment/range model,
delegation constraints, revocation, rotation, and ask/answer contract, and
extends them with the architecture's targets, definitions and processes.

On the five conflicts:

| # | decision | consequence |
|---|---|---|
| **D1** | **Type identity is key-relative and hash-identified.** No URN schema identifiers and no `ns:name` namespaces. A type is identified by the `DefinitionId` (the hash of its definition's canonical encoding) and a label local to that definition's definer. | Keeps ADR-0001 (P1). FKSA's own speaker-scoped bare names are the same idea and are retained in that form. |
| **D2** | **One canonical encoding** for every hashed or signed object — statements and definitions alike. | No JCS-for-schemas, CBOR-for-statements split. The encoding used is the deterministic CBOR profile of FKSA suite 1, which is MD-3's option 5. **This ADR does not accept DEC-002**; the DEC-002 ADR and its fixtures still decide it. |
| **D3** | **Trust anchors may be signed or unsigned.** An anchor may be a local, unsigned decision; or a trust statement signed by any key — including a third party — that has been **verified and then accepted** into a context's anchor list. **Acceptance is a local act by a persona whose controller is a person or organisation.** | Amends the architecture's earlier rule that anchors are always unsigned (ARCH-0003 W-07). The signature on a proposed anchor tells the wallet who proposed it; it never makes it an anchor. An agent-controlled persona does not accept anchors by default. |
| **D4** | **Trust is evaluated per context.** Every evaluation is relative to one context's anchors. | A key trusted for one purpose gains nothing elsewhere. |
| **D5** | **Issuer revocation is adopted**: a `revoke` statement by the issuer, naming the revoked statement's digest, effective from its `not before`. | Replaces "no revocation; short validity only". Short validity remains recommended; revocation distribution is not solved by this decision. |

**One further difference is recorded, not decided by the sponsor here but adopted
by the specification as consistent with accepted R-O-05:** FKSA signs the
re-encoded statement minus its signature; KSA transmits the signed bytes as they
were signed and verifies them before decoding (`SPEC-0002` §5). The decoder
spike (mofn#78) showed canonicality is checkable by a single parse, so nothing
is lost.

## Alternatives rejected

- **Adopt FKSA unchanged.** It cannot attest about artifacts or statements (its
  subject is always a key), has no human-readable semantics, and leaves schema
  documents unsigned (its open question Q12).
- **Keep the architecture and cite FKSA as related work.** That discards a
  working, exact core in favour of documents that do not yet specify bytes.

## Consequences

- `SPEC-0001`…`SPEC-0005` and `UC-0001` are written as normative specifications.
  ARCH-0001/0002/0003 remain the design record and rationale; where a SPEC and an
  ARCH document differ, the SPEC governs once this ADR is accepted, and the ARCH
  document is corrected.
- ARCH-0003 W-07 is amended by D3.
- FKSA statements are **not** wire-compatible with KSA: the target field, the
  envelope and the domain-separation label differ by design, so neither can be
  replayed as the other.
