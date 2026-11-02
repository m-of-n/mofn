---
schema: "design-log/v1"
id: DL-0015
part: review
date: "2026-10-25"
---

# DL-0015 — what the human decided and rejected, and what was left open

**Status:** the four decisions are the human's and are taken. **Review of the
ADR text is PENDING** — both ADRs are `reviewed: false`.

## 1. Rejected by the human

| decision | rejected | reason recorded in |
|---|---|---|
| DEC-002 | option 1 (S-expressions) | poorer data model and libraries, despite winning governance — ADR-0004 |
| DEC-002 | option 2 (COSE native) | fails P1 — ADR-0001, ADR-0004 |
| DEC-002 | *not yet* | — the human chose to decide with T-031 outstanding; ADR-0004 says what happens if the fixture breaks option 5 |
| DEC-003 | suite code in the preimage | our own registry number in every identifier; vector churn — ADR-0005 |
| DEC-003 | DS-label prefix | vector churn for a collision the registry rule forbids — ADR-0005 |
| DEC-003 | per-suite digest | one key would have several `kid`s — ADR-0005 |
| P1.1 | report and keep | inconsistent with P5 / P5.2 — ARCH-0002 0.9.0 changelog |

Options 3 and 4 of DEC-002 were not offered: option 3 had been argued for
withdrawal in `DECISIONS-0001`, and option 4 had no proponent. **Recorded
because the human therefore never chose against them explicitly.**

## 2. Rejected by the model

| considered | rejected because |
|---|---|
| **Remove `decision_makers`** (the sponsor's second option) | §9.2 acceptance must name who accepted; the human agreed (mofn#116) |
| **Decide condition (5)** — sort set-valued arrays | not asked; a SPEC-0002 byte-level change; owed |
| **Decide that SPEC-0002 §4.1 discharges condition (6)** | not asked; left to the ADR's reviewer |
| **`reviewed: true` on the ADRs** | agents never set it (`propose-arch`) |
| **Promote P1.1 out of draft** | outside the delegation, which covers ARCH-0001 §7 only |
| **Bump ARCH-0001 to 0.2.0** | 0.2.0 is held by the proposal; 0.1.5 follows the PATCH precedent. Flagged for the reviewer |

## 3. Open

1. The **delegation** is relayed verbally; the sponsor is asked to confirm on
   mofn#116, which this change stacks on. If the sponsor does not confirm, both
   ADRs revert to `proposed`.
2. **T-031** — the threshold fixture — is the outstanding half of DEC-002's
   acceptance test.
3. A **second reader** for ADR-0004 and ADR-0005.
