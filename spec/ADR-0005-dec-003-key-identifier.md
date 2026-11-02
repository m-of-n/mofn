---
schema: "archdoc/v1"
id: ADR-0005
title: "DEC-003 accepted: a principal is identified on the wire by kid = SHA-256 of its suite public-key encoding"
short_title: "ADR-0005 DEC-003 kid"
description: "Accepts DEC-003: kid is SHA-256 over the suite-defined public-key encoding, fixed across suites, with a registry rule against cross-algorithm encoding collisions."
type: decision
category: security
status: accepted
version: "1.0.0"
version_policy: "semver; an accepted ADR changes only by superseding it"
date: "2026-10-25"
updated: "2026-10-25"
decision_makers:
  - role: student
    id: ndewedo-newbury
    authority: "delegated by the sponsor (paul-lambert) on 2026-10-25; ARCH-0001 v0.1.4 front matter"
reviewers: []
needs_review: false
reviewed: false
canonical_path: spec/ADR-0005-dec-003-key-identifier.md
defers_to: ARCH-0001
decides: [DEC-003]
supersedes: []
---

# ADR-0005 — DEC-003: `kid` is SHA-256 of the suite's public-key encoding

**Status: accepted.** Decision of `ndewedo-newbury`, 2026-10-25, under the
sponsor's delegation recorded in `ARCH-0001` v0.1.4. The text was drafted by an
agent from that decision (`design-log/0015-dec-002-dec-003-adrs/`) and has
**not been reviewed** by a second reader.

## Decision

1. **Form.** An issuer or subject key is identified on the wire by its
   **`kid`**: a 32-octet byte string, `SHA-256(public-key encoding)`
   (`SPEC-0002` §4.5). Text renderings are presentation only (`SPEC-0002` §11).
2. **Canonical key bytes** — the clause DEC-003 said must be specified — are the
   **public-key encoding each cipher suite defines** (`SPEC-0002` §6.1): for
   suite 1 the 32-octet RFC 8032 §5.1.2 encoding; for suite 8 the 1952-octet
   FIPS 204 encoding. No COSE structure and no registry value enters the
   preimage.
3. **The digest is fixed.** `kid` is SHA-256 under every suite. A suite's own
   digest governs statement digests only. Agility, when needed, comes from a new
   identifier version, not from a per-suite choice. `ARCH-0001` §4.1's
   *"algorithm of digest is parameterized"* is narrowed accordingly.
4. **Collisions across key algorithms are prevented by the registry, not the
   preimage.** The suite code is not hashed. Instead `SPEC-0002` §12.3 gains a
   rule: a suite whose key algorithm differs from a registered suite's MUST NOT
   be registered if a valid public-key encoding under it can equal one under the
   registered suite. Suites that **share** a key algorithm share `kid`s: the key
   is the principal (R-M-02), whichever suite it signs under.

## Why

- R-O-01 requires every signed object's issuer to be specifiable as `KeyId`;
  R-M-02 lets a principal be identified solely by key or key digest. A digest
  over raw, suite-defined key bytes does both and nothing more.
- P1 (`ADR-0001`) excludes a registry from the identifier's meaning. Every
  rejected alternative below puts a registry value — IANA's, multiformats', or
  our own — into the identifier's bytes.

## Alternatives rejected

| alternative | rejected because |
|---|---|
| **COSE key thumbprint** (RFC 9679) | preimage is a registry-labelled `COSE_Key`; for AKP keys `alg` sits inside the digest with no excluding subset; for ML-DSA the COSE Algorithms value is in the preimage (`rfc-9679`, `rfc-9964` cut B; `ARCH-0001` §7) |
| **raw COSE key** | registry-labelled map; same P1 objection |
| **RFC 8747 `kid`** | a party-relative label resolved by lookup, not derived (`ARCH-0002` P1.1) |
| **`did:key`** | the key type is named by a multicodec code, from a registry maintained outside the project — a registry in the identifier, by our reading of P1 |
| **hash-uri / text `KeyId`** | a rendering of the same digest; kept for display, never signed |
| **suite code in the preimage** | removes the collision class outright, but puts **our own** registry number into every identifier and changes every `kid` in `spec/vectors/ksa-core/` |
| **DS-label prefix** (`KSA-KID-<alg>-v1\0 ‖ pub`) | clean separation without a numeric value, but the same vector churn, to prevent a collision the registry rule already forbids |
| **per-suite digest** | `kid`s of one key would differ by suite, contradicting "the key is the principal" |

## Acceptance test

DEC-003 had none in `ARCH-0001` §7; this ADR supplies it.

- **Met:** TV-1 (`key-publish`) computes `says = SHA-256(pub)` for suite 1, and
  `SPEC-0002` V8 checks `kid(body.key) = says`.
- **Owed:** a suite-8 `kid` vector (suite 8 is provisional and ships none), and a
  negative `key-publish` vector whose `says` is not the key's `kid`, rejected at
  V8.

## Interchange

The native `kid` may be exported in COSE's `kid` header or DSSE's `keyid` as a
**hint**; the principal travels in the payload. On import, a foreign `kid` that
disagrees with the `kid` computed from the key is **rejected** (`ARCH-0002`
P1.1, amended to reject on 2026-10-25; P5.2 for DSSE).

## Consequences

- `ARCH-0001` §7 DEC-003 marked accepted; §4.1 `KeyId` row narrowed.
- `SPEC-0002` v0.2.0: §6.1's digest row no longer covers `kid`s; §12.3 carries
  the collision rule.
- `ARCH-0002` P1.1's import rule reads *reject*. P1.1 stays `[draft]`; this ADR
  decides DEC-003, not ARCH-0002.

## Evidence

- `SPEC-0002` §4.5, §6, §12; `spec/vectors/ksa-core/` TV-1.
- Library `rfc-8747`, `rfc-9679`, `rfc-9964` at `bafd536`; mofn#112,
  `design-log/0014-cbor-cose-handover/`.
