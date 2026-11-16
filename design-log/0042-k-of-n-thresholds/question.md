---
schema: "design-log/v1"
id: DL-0042
part: question
title: "k-of-n threshold anchors in the wallet engine, keys only, no nesting (T-043, PLAN-0001 §12 risk 7)"
date: "2026-11-14"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "wallet 0.8.0 (threshold reduction in engine/reduce.py); SPEC-0002 0.10.1 (TV-36, TV-37); SPEC-0004 0.6.2 (asks 10–18, E-11…E-19); BACKLOG-0001 0.14.2; PLAN-0004 0.4.2. No ADR: no rule was changed."
status: open
---

# DL-0042 — question

The human, through a parent agent thread, asked for BACKLOG T-043 to be
**built, not deferred**: "*k*-of-*n* threshold subjects, keys only, no
nesting". It closes PLAN-0001 §12 risk 7. Its date, Nov 11, had passed. The
brief set these constraints:

- Read `SPEC-0004` for the normative semantics. A threshold subject is
  satisfied when at least *k* distinct listed keys each have a valid path.
  Keys only, no nested thresholds.
- The verdict must say which keys counted, and why it passed or failed.
- **Where the text is ambiguous, do not invent.** Record the gap here and take
  the narrowest reading, and flag it.
- Put the threshold logic in functions of its own. A sibling agent is adding
  multi-hop delegation (W-3) to `reduce.py` at the same time.
- Do not edit PLAN-0001 §12. The parent thread does that once every risk has
  landed.

The agent read `SPEC-0004` §4.2, §6.2–6.5, §7.2, §10.2–10.3, §11.5 and §14.2;
`SPEC-0002` §8.6 and its threshold notes; `ARCH-0001` §7 (the threshold
acceptance test and the distinctness rule still owed); `engine/reduce.py`,
`names.py`, `check.py` and `verifier.py`; `DL-0019` and `DL-0040`. It asked
the human no design questions. Each choice is listed in `produced.md`, and
each choice the text did not settle is listed in `review.md` as open.

`0041` is held by mofn#166 (`0041-l-041-d7-extraction`), open at the time.
