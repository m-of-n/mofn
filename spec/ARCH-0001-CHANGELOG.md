---
schema: "archdoc-changelog/v1"
id: ARCH-0001-CHANGELOG
title: "ARCH-0001 changelog"
type: changelog
parent: ARCH-0001
status: active
version: "0.2.1"
date: "2026-09-15"
updated: "2026-11-07"
canonical_path: spec/ARCH-0001-CHANGELOG.md
---

# ARCH-0001 changelog

Format: newest first. Versions match the architecture document.

## 0.2.1 — 2026-11-07

PATCH. T-048 (mofn#144). No requirement changes. `SPEC-0002` 0.6.0 withdraws
target type 5, so a locator is never a target and every target binds a digest.
That meets R-M-07 as 0.2.0 kept it. The §5.5 row for locator-only subjects is
closed and removed. The notes on R-M-07 and R-M-11 and the §4.1 `ArtifactId`
and §4.2 `ArtifactStatement` rows now point to the rule. Decided by
`ndewedo-newbury`; the agent drafted the text. Recorded in `DL-0030`.

## 0.2.0 — 2026-11-07

MINOR. T-012a (mofn#134). `ARCH-0001-PROPOSAL-v0.2.0` is folded in and
**superseded**. Decisions by `ndewedo-newbury` under the October delegation; the
agent drafted the text. Recorded in `DL-0028`.

- **§4.2 rewritten: one statement form, several functions** (`ADR-0002` P2, P6).
  The v0.1 kinds map to `SPEC-0002` kinds. `AclEntry` becomes local policy, not a
  statement. `Endorse` is import-only. The KSA lifecycle kinds are listed. The
  `AuthzCert.delegate: bool` field becomes `may_delegate` constraints.
- **§4.1** gains a KSA-form column. `ArtifactId` has three modes plus aliases
  (R-M-11). `PredicateType` is a key-relative `type-ref`, not a URI (P1,
  `ADR-0003` D1, `ADR-0007`).
- **§4.3**: "two procedures" corrected to three. Name resolution is **kept** by
  decision, though no SPEC specifies it yet. Template conformance is added to
  acceptance.
- **R-M-10 rewritten**: integer depth, ranges and key lists. RFC 2693 §4.1.4 is
  carried as a stated limit (mofn#136, `DL-0025`).
- **R-M-07 kept as MUST** by decision. A bare locator does not satisfy it.
- **R-M-08 generalised** to every constrained type (`ADR-0002` §5).
- **Added:** R-M-11 (subject modes), R-O-05 (sign the bytes; no
  canonicalisation during verification), R-O-06 (separate results). R-M-12
  pointer to `ARCH-0002` P1. R-O-05 repairs a citation defect: `ADR-0003` and
  `SPEC-0002` already cited it as accepted.
- **New §5.5**: every known ARCH/SPEC gap and which side owes the change. Two
  go against `ADR-0003`'s default by decision: SDSI names (`SPEC-0004`,
  mofn#143) and locator-only subjects (`SPEC-0002` §7.2, mofn#144).
- **§7**: DEC-006 recorded as withdrawn. **DEC-007 filed and accepted, option 2**
  (`ADR-0007`). The rule that DEC-004 and DEC-007 must not be collapsed is
  stated. `open_decisions` unchanged: DEC-004, DEC-005.
- **Citations**: RFC 9943 replaces `draft-ietf-scitt-architecture` (moved to
  `related_rfcs`). RFC 9804 is recorded as historical. C2PA 2.4 and CDDL
  (RFC 8610/9165/9682) are added. The agent-action-capsule draft is §3.3's
  evidence.
- **§6**: in-toto and COSE export losses recorded (R-I-01).

## 0.1.10 — 2026-11-07

- **DEC-001 accepted by `ADR-0006`**: org and working title `m-of-n`; repository,
  Python package and CLI `mofn`. It ratifies the names in use since 2026-09-17,
  and none of the five listed options was chosen. `open_decisions` is now
  DEC-004, DEC-005. Decided by `ndewedo-newbury` under the delegation in 0.1.7
  (`DL-0027`). It corrects `PLAN-0001`, `BACKLOG-0001` T-001 and
  `DECISIONS-0001`, which had called DEC-001 accepted since 2026-09-21 with no
  ADR. NG3 unchanged: accepted, not frozen.

## 0.1.9 — 2026-11-06

- **§3.4 added: OpenPGP mechanisms read against this model** (mofn#128,
  `DL-0026`). Additive research inputs (§9.1); six rows. Four confirm items
  already accepted or drafted (`ADR-0004`/P3, `ADR-0001`, §4.3, `ARCH-0003`
  §3.2), one cross-references `R-0007` P3, and one is new evidence on DEC-003's
  open `kid`-preimage sub-question: the v6 fingerprint hashes algorithm and
  creation time. No requirement or DEC changed. A revocation certificate at
  key creation was declined by the owner; `R-0007` P5 stays open. PATCH, not
  MINOR: no requirement is added, and 0.2.0 is `ARCH-0001-PROPOSAL-v0.2.0`'s
  target (the same choice 0.1.3 made). Drafted as 0.1.8; renumbered on
  rebase after `ADR-0002` (mofn#133) took 0.1.8.
- `RFC9580` added to `related_rfcs` and §10.

## 0.1.8 — 2026-11-06

- **`ADR-0002` accepted** — `ARCH-0002` P2, P3, P5 (with P5.1, P5.2) and P6 are
  normative; P4 and P7 stay draft. Not a DEC-\*: `open_decisions` unchanged
  (DEC-001, DEC-004, DEC-005). Decided by `ndewedo-newbury` under the
  delegation in 0.1.7 (mofn#6, `DL-0024`).
- §4.2 gains a pointer note: the kinds are functions over one form (P6). The
  table itself is unchanged; the rewrite is owed to v0.2.0 (register item 4).

## 0.1.7 — 2026-11-03

- Front matter only. `decision_makers` records the sponsor's October 2026
  delegation, given on Zoom and relayed by `david-hsiao`: `ndewedo-newbury` and
  `david-hsiao` may each decide any question in the project, and are
  accountable for what they decide. It supersedes the 2026-10-25 delegation and
  its ADR-0002 exclusion, and covers `ADR-0004` and `ADR-0005`. No written
  sponsor confirmation is recorded (`DL-0021`). No DEC changed; §9 unchanged:
  a DEC-* is still accepted only by an ADR.

## 0.1.6 — 2026-11-01

- **§7 DEC-002: the threshold fixture landed** (T-031, `DL-0019`). "No threshold
  vector yet" replaced by what it found: V8 owns `1 ≤ k ≤ n`; `n = len(members)`
  holds by construction, with its negatives failing at V7 and V5. `NameCert` is
  TV-13, not TV-1/TV-2. `trusts` distinctness recorded as owed. No DEC changed;
  `ADR-0004` unchanged.

## 0.1.5 — 2026-10-25

- **DEC-002 accepted — option 5, `ADR-0004`.** Option 5 added to §7's list as
  the accepted option. Threshold fixture (T-031) and set-array order (condition
  5) recorded in the ADR as owed.
- **DEC-003 accepted — `kid` = SHA-256 of the suite's public-key encoding,
  `ADR-0005`.** §4.1 `KeyId` row narrowed: the digest is fixed, not
  parameterized.
- `open_decisions` now DEC-001, DEC-004, DEC-005. Decided by `ndewedo-newbury`
  under the delegation recorded in 0.1.4.

## 0.1.4 — 2026-10-25

- Front matter only. `decision_makers` was empty; it now names the sponsor
  (`paul-lambert`) and **`ndewedo-newbury`, by the sponsor's delegation of
  2026-10-25**, scoped to the open decisions in §7. The sponsor offered either
  adding the delegate or dropping the field; the field was kept, because §9.2
  acceptance has to name who accepted.
- No decision accepted. DEC-001 … DEC-005 remain open; accepting one is still
  an ADR, a changelog line and a §7 status update.

## 0.1.3 — 2026-10-23

- Additive only (§9.1), from the CBOR/COSE extraction handed over in mofn#112
  (library records at `bafd536`). §7 DEC-002 and DEC-003 each gain a block of
  **inputs their ADR must answer**: the omitted driver *detectability of an
  order-only divergence*; "no IANA tags" restated as a rule of our profile; the
  acceptance test's threshold invariant, which no schema language checks, owned
  by a named verifier step; RFC 9679 thumbprints not native-eligible as written;
  the IANA allocation inside a post-quantum COSE thumbprint; and the inverse
  question for a suite-free `kid`.
- No decision accepted, ranked or withdrawn. DEC-001 … DEC-005 remain open. The
  §6 matrix is untouched — that is mofn#110's lane.

## 0.1.2 — 2026-10-14

- Additive only (§9.1). New §4.4: a pointer to **ARCH-0003**, the wallet, persona,
  key and definition object model drafted from sponsor direction of 2026-10-14.
- No model, requirement or decision change in this document.

## 0.1.1 — 2026-09-21

- Editorial only. No model, requirement, or decision change.
- `canonical_path` moved from `artifacts/docs/` to `spec/`. "Artifact" is a
  normative term in this document (`ArtifactId`, `ArtifactStatement`, R-M-07,
  and RFC 9943's definition); using it for a directory of authored documents
  overloaded the most load-bearing noun in the model. Execution documents
  (PLAN, BACKLOG, PROC) moved to `project/`.

## 0.1.0 — 2026-09-15

- Initial checkpoint from research pass on X.509, PGP/WoT, SDSI, SPKI, PICS, in-toto, DSSE, COSE/CWT, SCITT, SLSA.
- Constraint recorded: native model is not X.509; interchange is required.
- Information model drafted: NameCert, AuthzCert, AclEntry, ArtifactStatement, Endorse.
- Requirements R-M-*, R-I-*, R-O-*, R-D-* written.
- Interchange matrix first cut.
- Open decisions DEC-001 … DEC-005 filed; none accepted.
- No encoding, tag language, or envelope selected.
