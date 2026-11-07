---
schema: "design-log/v1"
id: DL-0028
part: review
date: "2026-11-07"
---

# DL-0028 — review

**Human answers:** (1) keep names, the SPEC owes them; (2) keep R-M-07 as MUST,
fix the SPEC; (3) **close DEC-007 now by ADR**; (4) adopt all four proposal
parts.

## What the human rejected

- **The agent's recommendation on DEC-007.** The agent recommended filing it
  open, restated against SPEC-0003, and closing it later in a separate ADR.
  The human closed it now (`ADR-0007`). The reasoning recorded in the ADR
  is the agent's: the governing SPEC already answers it, so an open decision
  would mislead. The human gave no reason of their own.
- **ADR-0003's SPEC-governs default, twice.** On names and on locator-only
  subjects, the human kept the ARCH requirement and made the SPEC owe the
  change. The rejected alternatives: drop compound names (a MAJOR model change
  that would also cut T-040), and loosen R-M-07 to SHOULD.

## What the agent did not do

- No vector was written. The depth/widening vector (mofn#136) and the DV-2
  sentence test (T-049) are owed.
- No SPEC was edited. mofn#143 and #144 carry those changes, by the SPECs'
  decision makers.

## Owed

- Text review of `ADR-0007` and of the §4.2 rewrite by a second reader.
- mofn#143, mofn#144, T-049, and the mofn#136 vector.
