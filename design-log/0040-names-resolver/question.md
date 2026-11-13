---
schema: "design-log/v1"
id: DL-0040
part: question
title: "Name resolver in the wallet engine, names across a rotation, and ADR-0008 accepted (T-040, after mofn#164)"
date: "2026-11-13"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "wallet 0.6.0 (engine/names.py); SPEC-0002 0.9.1 (TV-35); SPEC-0004 0.6.1 (R-8…R-10); ADR-0008 accepted; BACKLOG-0001 0.13.3."
status: open
---

# DL-0040 — question

After mofn#164 merged, the human asked the agent to "complete the owed after
merge from this PR, the paperwork as you described it", and asked what the
resolver is. `DL-0039` review.md listed three things as owed:

1. `ADR-0008` acceptance by a decision maker, and a second reader's review
   of `SPEC-0004` §5.3;
2. T-040: a resolver in the engine that passes R-1…R-7 and E-8…E-10;
3. a name-rotation vector, which needs a `key-publish` for bob2.

The agent read `SPEC-0004` §5.3, §7 and §10.3; `engine/reduce.py`,
`verifier.py`, `definition.py` and `check.py`; and
`tests/test_delegation.py`. It asked no new design questions. Every choice
below either follows the text of §5.3 or §7.2, or is recorded in
`produced.md` as a choice the human has not seen.
