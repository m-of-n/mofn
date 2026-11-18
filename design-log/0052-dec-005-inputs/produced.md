---
schema: "design-log/v1"
id: DL-0052
part: produced
date: "2026-11-17"
---

# DL-0052 — produced

- **ARCH-0001 0.3.3**, edited in place (§9.1). Under §7 DEC-005, a new block,
  **Inputs the DEC-005 ADR must answer**, follows the precedent of the DEC-002
  and DEC-003 inputs added in 0.1.3. It holds six items:
  1. the scope is already settled as export-only, by `ADR-0004` item 4, and
     the native envelope cannot be a candidate (record X-01);
  2. COSE_Sign is an option the list omits, recorded as an input and not as
     option 4 (record A-04, C-03, Q-05);
  3. no single envelope serves both in-toto and SCITT, so picking one picks
     an ecosystem for v1;
  4. E1 (DSSE over the KSA TBS) and E2 (an in-toto Statement in DSSE) are
     different products, and R-O-05's first clause cannot hold for E2
     (record K-01, Q-10);
  5. the export's signing key: the speaker's own key or a separate export key
     (record K-02, Q-11);
  6. if import is in scope, what the ADR inherits (record C-04, C-05, C-06,
     Q-13; P5.2's interior gap, from `slsa-provenance-1-2` K-01 and
     `slsa-vsa-1-2` K-02).
- **A proposed acceptance test** for DEC-005, which had none. It is marked
  as not agreed.
- Front matter, header line, `agent_notes` and end line move to 0.3.3, with
  one changelog entry.

## Choices the human has not seen

- **PATCH, not MINOR**, as in DL-0048. ARCH-0001's `version_policy` makes
  MINOR mean additive *requirements*, and none is added.
- **COSE_Sign is an input, not option 4.** Numbering it would read as a step
  towards selecting it. DEC-002's option 5 was numbered only in the ADR that
  accepted it.
- **The citation is to an unmerged, unreviewed PR head.** This is stated in
  the text. If #141 changes before it merges, the record ids cited here must
  be re-checked.
- **An acceptance test was added, although only "the option list" was asked
  for.** The `propose-arch` skill requires one for every decision proposed.
  DEC-005 had none, and without one the inputs give the ADR nothing to meet.
