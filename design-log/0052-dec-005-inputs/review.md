---
schema: "design-log/v1"
id: DL-0052
part: review
date: "2026-11-17"
---

# DL-0052 — review

**Human verdict:** pending (PR review).

## What the agent rejected, and why

- **Adding COSE_Sign as a numbered option 4.** See `produced.md`: numbering it
  reads as ranking it.
- **Rewording R-I-03.** The requirement pairs in-toto with DSSE and COSE_Sign1
  with CWT. That is consistent with what in-toto allows, so nothing in it is
  wrong. Whether v1 serves one ecosystem or both is DEC-005's choice, not an
  edit to make here.
- **Editing the §6 DSSE and COSE_Sign1 rows, or adding a COSE_Sign row.**
  Those rows record what we map. Adding a row would assume an option.
- **A `ARCH-0001-PROPOSAL-v0.3.3.md`.** No requirement is added, and the
  model does not change. A proposal file would be the parallel document that
  §9.4 warns against.
- **Waiting for library#141 to merge.** The human asked to proceed. The text
  names the PR head and its unreviewed state instead.
- **Touching DEC-004.** The three records say DEC-004 stays open, and they
  give evidence for none of its options. What #143 and #144 found about the
  core's range algebra (SLSA levels as integer ranges, VSA joint coverage) is
  input for T-053 and for the supply-chain profile that P7 waits on. It is
  not an option-list change.
- **Writing an ADR, or marking anything accepted.** Hard stop. DEC-005 is the
  human's to accept.
