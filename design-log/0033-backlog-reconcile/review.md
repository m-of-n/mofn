---
schema: "design-log/v1"
id: DL-0033
part: review
date: "2026-11-09"
---

# DL-0033 — review

**Human decisions:** T-030 and T-032 are closed. The reasons on the rows are
the agent's, and the human can reject them in PR review: T-030's neutral schema
was the hedge for a deadlocked DEC-002 (`PLAN-0001` §12 risk 4), and
`ADR-0004` made it unnecessary; T-032's comparison was already declared not
owed on T-031 (`DL-0019`).

## What was rejected, and why

- **Marking T-013 done.** mofn#7 closed 2026-10-28, but its only comment
  records no agreement, and `PLAN-0001` §12 says the cut order must be agreed
  in writing. Closing the issue is not that agreement. Kept `todo`.
- **Marking T-047 done.** `demo/slice.sh` breaks a link and the verdict names
  it, but only for one hop. The row says *chain*; the engine has no delegation
  (`engine/reduce.py`). Marked `doing`.
- **Marking T-034 done.** N-1…N-11 and the no-re-encode test run in CI, but
  P5.1's acceptance test (the full RFC 8949 FX-1 negative set) does not.
- **Marking L-035 done.** The carve-out is in effect, but the row is a sponsor
  decision and no ruling is recorded. Moved to `review — ruling to record`.
- **Deciding T-029c.** The agent laid out three options and their costs. Which
  framework to use is the human's call, and it belongs in `DECISIONS-0001`
  item 28, not the backlog.
- **Resolving the W-/T- overlap.** Still flagged, still a planning call.

## Owed

- T-029c's decision, recorded in `DECISIONS-0001` item 28 and the `PLAN-0002`
  stack table.
- `spec/schema/README.md` and `spec/vectors/README.md` are stale; both are
  noted on T-030 and T-046 and left for a `spec/` PATCH.
