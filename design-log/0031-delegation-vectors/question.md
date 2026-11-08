---
schema: "design-log/v1"
id: DL-0031
part: question
title: "Delegation vectors for depth and widening (mofn#136); the DV-2/TV-13 sentence test (T-049)"
date: "2026-11-07"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "SPEC-0002 0.7.0 (TV-14…20, E-1…E-4); SPEC-0004 0.4.0 (Appendix A asks 3–6); wallet tests for E-1…E-4 and the TV-13 sentence."
status: open
---

# DL-0031 — question

After #145 merged, the human said "go" to the items the agent had listed as its
own: the #136 depth/widening vector and the T-049 sentence test.

- **#136 acceptance test, last clause:** "A vector covers depth exhaustion
  (`depth`) and widening (`widening`)." R-M-10 was rewritten in ARCH-0001 0.2.0;
  the vector was owed.
- **ADR-0007 acceptance table:** "a second, non-software type, rendered —
  owed. DV-2 `names` and TV-13 exist as vectors, but no test asserts a rendered
  sentence for them."
