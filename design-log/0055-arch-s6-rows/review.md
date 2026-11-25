---
schema: "design-log/v1"
id: DL-0055
part: review
date: "2026-11-23"
---

# DL-0055 — review

**Human verdict:** pending (PR review).

## What the agent rejected, and why

- **A table row for the KSA envelope.** `R-0006` §2.5 asked for one. §6 maps
  *foreign* objects, and the native envelope is not one, so a row would
  misclassify it. A row would also invite an *E* cell that names an envelope,
  which is DEC-005. A paragraph under the table says the same thing without
  either problem.
- **Leaving VC and PICS for later**, as mofn#110 planned. The condition the
  issue set has been met: the records exist. Waiting would have left #110
  open for no reason.
- **Deciding the Data Integrity import.** Refusing it would give up most
  deployed VCs. Carving out an exception would weaken R-O-05, a Must. Either
  choice is a human's, so the note records it as owed.
- **Restating a `KeyId` profile in the COSE row.** The #112 sequencing comment
  says to defer to DEC-003. The cell cites `ADR-0005` and P1.1 and does not
  restate them.
- **A proposal file, `ARCH-0001-PROPOSAL-v0.3.4.md`.** No requirement is
  added and the model does not change, the same ground as `DL-0052`. A
  proposal file would be the parallel document that §9.4 forbids.
- **Marking P1.1 accepted.** It is draft. The cell names it as draft.
- **Touching `SPEC-0003` here.** That is mofn#110 part 2, and the issue asks
  for it in a separate PR.
