---
schema: "design-log/v1"
id: DL-0048
part: produced
date: "2026-11-16"
---

# DL-0048 — produced

- **ARCH-0001 0.3.2**, edited in place (§9.1):
  - the §2.3.2 domain paragraph now names DV-5
  - a dated note says DV-3 is superseded by version, not edited, and stays published
  - AR-1 → TV-40, TV-41, TV-43; E-20
  - AR-2 → TV-42; E-21
  - AR-3 → TV-44; E-22
  - the closing paragraph cites the wallet demo that runs DV-5 byte for byte
  - the front matter, the header line and the `agent_notes` move to 0.3.2
  - one changelog entry
- **UC-0001 0.2.1:** UC-3's flow and must-fail case use `record-review`; the trace row cites DV-5 and keeps v1 in parentheses.

## Choices the human has not seen

- **PATCH, not MINOR.** The `propose-arch` skill says to make a MINOR bump
  for an additive clarification. ARCH-0001's own `version_policy` makes
  MINOR mean additive *requirements*, and 0.3.1 used PATCH for a change that
  added none. The document's own policy governs.
- **AR-1 asks "how far … checked", and its answer is `summarized`.** Under v2
  the in-range value is `summarized`, not a partial review. The question was
  reworded so that a yes does not read as "it was reviewed".
- **DV-3 is kept in a note, not deleted from the section,** so a reader of a
  0.3.0 citation can still find what it meant.
