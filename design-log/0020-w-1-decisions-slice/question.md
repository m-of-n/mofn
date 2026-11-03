---
schema: "design-log/v1"
id: DL-0020
part: question
title: "Finishing W-1 (mofn#65): the open decisions, demo/slice.sh, the spec diffs"
date: "2026-11-01"
model: "claude-opus-5-5"
human: Ndewedo-Newbury
outcome: "A1, C1, C4 and DL-0016's open items decided as W-1 implementation decisions; C2, C3, C5 unidentified; demo/slice.sh; SPEC-0002 0.4.0, SPEC-0003 0.1.1, SPEC-0004 0.2.0 accepted by ndewedo-newbury on 2026-11-03, as a decision maker added at their own instruction. No ADR: no DEC-* touched."
status: open
---

# DL-0020 — question

## The brief

The engine merged in mofn#122, and three things kept mofn#65 open: the decisions
in the 2026-10-20 comment and the unposted C1–C5, `demo/slice.sh`, and the spec
diffs DL-0016 raised. The human (Chip, GitHub `Ndewedo-Newbury`) said to answer
as recommended, from the records and the evidence, without waiting for Paul, and
to post the answers on #65 as Chip's decisions. The agent was told to:

- give each decision's answer, evidence and rejections, in this entry as well as
  the comment;
- check what the delegation in the ARCH-0001 front matter covers, and report any
  answer outside it;
- say so if a C-item cannot be identified, rather than invent it;
- leave `spec/vectors/`, ADR-0004 and T-031 alone (the mofn#8 thread), add no
  primitive, keep `src/` empty.

## Context supplied

mofn#65 with all comments, including the A1–A3/B1–B4 comment of 2026-10-20 and
the update of 2026-11-01; mofn#68; DL-0016; SPEC-0002, SPEC-0003, SPEC-0004;
ARCH-0003; the goldens in `prototype/wallet/fixtures/golden/`.

The human's notes behind DL-0016, the only place C1–C5 were written out, were
David's and were never committed. They were not available.
