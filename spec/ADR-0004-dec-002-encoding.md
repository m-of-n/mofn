---
schema: "archdoc/v1"
id: ADR-0004
title: "DEC-002 accepted: option 5 — reduced deterministic CBOR (KSA-CBOR) is the native encoding"
short_title: "ADR-0004 DEC-002 encoding"
description: "Accepts DEC-002 option 5: the CBOR data model under RFC 8949 §4.2.1 deterministic encoding, restricted and decoder-enforced, with no IANA registry native; COSE and DSSE are export envelopes only."
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
canonical_path: spec/ADR-0004-dec-002-encoding.md
defers_to: ARCH-0001
decides: [DEC-002]
supersedes: []
---

# ADR-0004 — DEC-002: the native encoding is option 5

**Status: accepted.** Decision of `ndewedo-newbury`, 2026-10-25, under the
sponsor's delegation recorded in `ARCH-0001` v0.1.4. The text of this ADR was
drafted by an agent from that decision (`design-log/0015-dec-002-dec-003-adrs/`)
and has **not been reviewed** by a second reader; `reviewed: false` says so.

## Decision

**DEC-002 is decided for option 5** (`ARCH-0001-PROPOSAL-v0.2.0` §3.3, rev.5):

1. **Data model and encoding.** The CBOR data model, encoded under the core
   deterministic requirements of RFC 8949 §4.2.1 and restricted as `SPEC-0002`
   §4.1–§4.2 specify — shortest heads, definite lengths, map keys in **bytewise
   lexicographic order** of their encodings, and no tags, floating-point values,
   `null`, `undefined` or other simple values. This is **KSA-CBOR**.
2. **A rejecting decoder.** Canonicality is enforced by the decoder, not
   assumed: any input that is not exactly the KSA-CBOR encoding of a value is
   rejected, never repaired (`SPEC-0002` §4.3, `ARCH-0002` P5.1).
3. **No IANA registry is native.** Named, because "no tags" was too narrow
   (`ARCH-0001` §7, inputs since v0.1.3): the native model depends on none of
   CBOR Tags, COSE Header Parameters, COSE Algorithms, CWT Claims, or CWT
   Confirmation Methods. Each may appear at an interchange boundary, mapped
   lossily per R-I-01.
4. **COSE_Sign1 and DSSE are export envelopes only.** *Which* envelope remains
   DEC-005, which this ADR does not decide.

`ADR-0003` D2 adopted KSA-CBOR for the specifications while stating that it did
not accept DEC-002. **This ADR is that acceptance**; D2 and DEC-002 now say the
same thing.

## Scoring

Against `ARCH-0001` §7's drivers, the criterion the proposal §3.3 added, and the
one `ARCH-0001` v0.1.3 added. Sources are cited per cell; where a cell is our
reasoning rather than a cited finding it says so.

| criterion | 1 S-exp | 2 CBOR + COSE | 3 JSON + JCS | 4 dual | **5 KSA-CBOR** |
|---|---|---|---|---|---|
| library availability | poor (proposal §3.1) | good | good | both sets, plus a bijection (ours) | good |
| SCITT alignment | none | native | via DSSE | partial | at the export boundary |
| SPKI fidelity | highest | low | low | low | low; mapped by WP2 |
| human debug | RFC 9804 advanced form | diagnostic notation | native | — | `SPEC-0002` §11 human-review form |
| namespace governance (P1) | **wins** | **fails** as written (`ADR-0001`) | key-relative if constrained | fails through its option-2 half (ours) | holds by stated rule (item 3 above) |
| order-only divergence detectable | in the grammar | §4.2.1 optional | RFC 8785 sorts keys | — | **stated rule + rejecting decoder** |
| canonical-encoding conditions | right side of all four grounds | — | **withdrawn**, four grounds | — | (1)–(4) met; (5) owed; (6) see below |

**Why 5 over 1.** Option 1 wins governance and makes smallest-form a property
of the grammar, so a conforming reader cannot omit the check. Under option 5 the
same property is a rule an implementation must state; one that omits it still
parses every valid document (`DECISIONS-0001` item 2; `rfc-8747` cut B). That
cost is accepted and paid for by making the rejecting decoder a conformance
requirement (item 2) rather than by changing encoding. Option 1 loses on the
data model and on library availability, which DEC-002 names as a driver.

**The cost of reopening was weighed, not used as the argument.** Five SPEC
documents and `spec/vectors/ksa-core/` are written against option 5
(`DECISIONS-0001`, standing note on item 2). That would have been a reason to
look harder at option 1, had option 1 won on the drivers; it did not.

## Acceptance test — what is met, and what is owed

`ARCH-0001` §7: round-trip fixtures for NameCert, AuthzCert including a
threshold subject, and ArtifactStatement.

- **Met:** `spec/vectors/ksa-core/` round-trips KSA statements whose kinds carry
  the AuthzCert role (`trust`, TV-5) and the ArtifactStatement role
  (`attestation`, TV-4), and carries negative vectors for the rejecting decoder
  (P5.1).
- **Owed — the threshold fixture (T-031).** No vector exercises `trust`'s
  threshold form. Per `ARCH-0001` §7 since v0.1.3, it carries the invariant as
  positive and negative cases (`k = 0`, `k > n`, `n ≠ len(members)`) and names
  `SPEC-0002` V8 as the check that owns it. **This decision was taken with that
  fixture outstanding.** If the fixture exposes a defect in option 5 itself —
  not in a vector — this ADR is superseded, not patched.

## Not decided here

- **Condition (5), the order of set-valued arrays.** `SPEC-0003` sorts range
  values; `SPEC-0002`'s `trusts`, `allow-keys` and `exclude-keys` are arrays
  whose order is signed and unstated, so two producers can emit one set as two
  byte strings. Owed to `SPEC-0002`.
- **Condition (6), Unicode normalisation.** `SPEC-0002` §4.1 now declares text
  byte-exact and never normalised. Whether a declared *no-normalisation* rule
  discharges condition (6) is left for the reviewer of this ADR.
- **DEC-005**, the export envelope. **DEC-004**, the tag language.

## Alternatives rejected

- **Option 1, canonical S-expressions (RFC 9804).** Poorer data model and
  library support; RFC 9804 is historical (proposal §3.1). Retained as WP2's
  mapping reference.
- **Option 2, CBOR + CDDL with COSE native.** Registry-allocated tags and
  header parameters are native under it; fails P1 (`ADR-0001`).
- **Option 3, JSON + RFC 8785 JCS.** Withdrawn on the four grounds of
  `DECISIONS-0001` item 2; the strongest is that RFC 8785 §3.2.3 prohibits the
  array reordering we need, so we would ship a modified JCS — a partly invented
  algorithm under R-O-03.
- **Option 4, dual canonical.** Two canonical forms and a bijection nobody has
  specified, for no driver the single form does not meet.

## Consequences

- `ARCH-0001` §7 DEC-002 is marked accepted, pointing here; the proposal's
  option 5 is the accepted text.
- MD-3's narrowing is closed by acceptance; `DECISIONS-0001` items 2 and 4b
  close.
- `src/` is no longer blocked by DEC-002. It is still blocked from assuming a
  tag language (DEC-004) or an export envelope (DEC-005).

## Evidence

- `library/topics/canonical-encoding.yaml` (answered), mofn#8.
- `design-log/0006-canonical-encoding-close/`; `design-log/0007-rejecting-decoder-spike/`
  (mofn#78 — canonicality decidable in a single pass).
- Library `rfc-8747` (cuts A, B), `rfc-8392` (cut 3), `rfc-8610`, at `bafd536`;
  mofn#112, `design-log/0014-cbor-cose-handover/`.
