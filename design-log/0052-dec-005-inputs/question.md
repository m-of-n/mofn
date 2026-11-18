---
schema: "design-log/v1"
id: DL-0052
part: question
title: "ARCH-0001 0.3.3: DEC-005 inputs from the in-toto envelope extraction"
date: "2026-11-17"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "ARCH-0001 0.3.3 (PATCH). DEC-005 gets inputs and a proposed acceptance test. No option selected; no requirement or other DEC-* moves."
status: open
---

# DL-0052 — question

The human asked the agent to explain DEC-004, DEC-005 and DEC-007, and then
asked whether the unmerged library PRs for library#136 (#141 `in-toto-envelope-v1`,
#143 `slsa-provenance-1-2`, #144 `slsa-vsa-1-2`) changed the next steps. The
agent answered yes for DEC-005 and proposed, as its step three, to "amend
DEC-005's option list in ARCH-0001 via `propose-arch`: add COSE_Sign, cite C-03
and ADR-0004 item 4". The human said: "Proceed with step three."

The context supplied:

- ARCH-0001 0.3.2, read in full;
- `ADR-0004` items 3 and 4;
- `R-0006` §4.6–§4.7 and §5.2;
- `ARCH-0002` P5.2 and P7;
- the design notes of all three library records, at their PR heads (#141 at
  `23c0d40`).

The agent checked first that no open mofn PR touched `spec/`.

**A correction the agent made to its own earlier answer.** It had told the
human that DEC-005 waited on the question "is DEC-005 export-only?", and it
had taken that question from `R-0006` §5.2. `ADR-0004` item 4 answered it on
2026-10-25. The agent missed this until #141's design notes cited
`ADR-0004:51-52`.
