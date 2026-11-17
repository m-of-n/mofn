---
schema: "design-log/v1"
id: DL-0041
part: question
title: "Delegation paths in the wallet engine, and T-042 against delegation: 1 (W-3 / mofn#67, T-065, T-041)"
date: "2026-11-14"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "wallet 0.7.0 (engine/reduce.py delegation paths, mofn delegate, root add --depth); demo/slice.sh ④–⑥; BACKLOG-0001 0.14.0."
status: closed
---

# DL-0041 — question

The parent thread asked an implementation agent to close `PLAN-0001` §12
risk 11 (*multi-hop delegation not in the engine*) and with it risk 6
(*tag-language fallback*). The Nov 11 date had passed; the human wanted the
work built, not the date moved. The brief:

1. implement `SPEC-0004` §6.3 delegation paths in `engine/reduce.py`, so a
   chain intersects topic, range **and** validity, and an expired or
   out-of-scope link gives `authorization FAIL` naming the broken link;
   short expiry is the revocation mechanism;
2. move E-1…E-4 from the test-only walker onto the engine;
3. test whether `SPEC-0003` `delegation: 1` realises the `bytes-equal` floor
   `ARCH-0001` DEC-004 offers (`R-0006` §4.7), and if so mark T-042
   subsumed, **without selecting a DEC-004 option**;
4. show a chain and a broken link in `demo/slice.sh` (T-047), if in reach;
5. update BACKLOG W-3, T-065, T-041, T-042, T-047 and W-2b; leave
   `PLAN-0001` §12 to the parent thread.

Before starting, the agent checked for in-flight W-3 work by #67's assignee:
no open PR, and the only delegation branch (`delegation-vectors`) was #148,
already merged. A sibling agent was writing T-043 (thresholds) in the same
file, so the new code is in separate functions.
