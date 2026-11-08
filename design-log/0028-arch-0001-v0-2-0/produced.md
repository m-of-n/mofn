---
schema: "design-log/v1"
id: DL-0028
part: produced
date: "2026-11-07"
---

# DL-0028 — produced

No primitive, vector, schema or code. Text only.

| file | change |
|---|---|
| `spec/ARCH-0001-authorization-attestation.md` 0.1.9 → **0.2.0** | §3 citations; §4.1 KSA-form column, three `ArtifactId` modes, `PredicateType` as `type-ref`; **§4.2 rewritten** (one form, function → KSA kind table, delegation and attestation fields); §4.3 (three procedures, names kept); R-M-07 note, R-M-08 generalised, **R-M-10 rewritten**, R-M-11/R-O-05/R-O-06 added, R-M-12 pointer; **new §5.5** gap table; §6 export losses; §7 DEC-006, DEC-007 |
| `spec/ADR-0007-dec-007-predicate-rendering.md` | new, accepted. Acceptance test: four clauses met, one owed (the DV-2 rendered-sentence test, T-049) |
| `spec/ARCH-0001-PROPOSAL-v0.2.0.md` | `status: superseded`. Kept, not deleted, because it is cited |
| `spec/ARCH-0001-CHANGELOG.md` | 0.2.0 entry |
| `project/DECISIONS-0001.md` 0.6.0 | items 4, 5d, 6 closed |
| `project/BACKLOG-0001.md` 0.12.12 | T-012a review; T-040s, T-048, T-049 added |
| issues | mofn#143 (SPEC-0004 names), mofn#144 (SPEC-0002 locator) |

**Found while drafting.** `ADR-0003` (accepted) and `SPEC-0002` cite "accepted
ARCH-0001 R-O-05", but R-O-05 existed only in the proposal. Adopting it in
v0.2.0 repairs that citation defect; the changelog records it.
