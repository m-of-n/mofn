---
schema: "design-log/v1"
id: DL-0047
part: review
date: "2026-11-14"
---

# DL-0047 — review

**Human decision:** open the issue and add the row (*"complete next steps 1"*).
The ranking and the reasons on the rows are the agent's. The human can reject
them in PR review.

## What was rejected, and why

- **Rewriting T-052 to say SLSA v1.2.** The agent's first edit changed the
  task text. That is a scope change to S1's task, made without S1. The row was
  reverted to "v1.1", and the mismatch is now flagged in its status for the
  owner to reconcile. (The SLSA v1 provenance predicate type is shared across
  spec 1.0–1.2, so the difference may not matter. That is the owner's call.)
- **Adding `in-toto-attestation-v1` to L-041.** library#89 already owns it,
  and PR #134 is open. Two issues for one record would double-count it.
- **Adding `slsa-1-2`.** It is already `distilled`.
- **Folding the three records into library#89.** #89 is the R-0006 inventory,
  a closed list that is 3 of 5 PRs done. Widening it would delay closing it,
  and these records are driven by D7, not by R-0006.
- **Starting the extraction in this change.** Extraction runs in the
  `library` repo with its `extract` skill (`PROC-0003` §1), never in the
  submodule here.

## Owed

- S1: confirm the ranking on library#136, and settle T-052's version.
- Whoever takes library#136: extract the envelope first.
