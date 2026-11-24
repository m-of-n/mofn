---
schema: "design-log/v1"
id: DL-0056
part: question
title: "SPEC-0003 0.3.0: §6 pattern containment (mofn#110 part 2)"
date: "2026-11-24"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "SPEC-0003 0.3.0. Within defined once for pattern kinds; empty patterns forbidden; ip-prefix ranges maximally aggregated and sorted."
status: open
---

# DL-0056 — question

This is the same session as `DL-0054`. The human took ownership of mofn#110
and said *"Continue with next steps."* Part 2 of the issue comes from the
`R-0006` §4.6 review on #100. It has three items:

1. §6.1 and §6.2 do not say when one pattern is within another.
2. Empty patterns break antisymmetry.
3. "Equal ranges have equal bytes" is false for ip-prefix.

The agent put the two normative choices to the human as questions, each with
a recommended option:

- **Empty patterns.** Forbid them, or define them as matching nothing. The
  human chose **forbid** (the recommendation).
- **ip-prefix.** Require maximal aggregation and a sort order, or retract the
  sentence. The human chose **aggregate + sort** (the recommendation). The
  agent's argument was that `delegation: 1` compares ranges for equality
  (SPEC-0004 §6.3 item 4; `DL-0041`), so the sentence carries weight.

The context supplied: `SPEC-0003` 0.2.0 §6, `SPEC-0004` §6.3, mofn#110, and a
search of `spec/vectors/` and `prototype/wallet/domains/` for kinds 4, 5 and
11 (none found). The engine names these kinds but implements none of them
(`prototype/wallet/engine/definition.py`).
