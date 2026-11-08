---
schema: "design-log/v1"
id: DL-0031
part: review
date: "2026-11-07"
---

# DL-0031 — review

**Human verdict:** pending (PR review).

## What the agent rejected, and why

- **Adding delegation to the wallet engine.** `engine/reduce.py` says v0 has no
  delegation. Building §6 into it (paths, thresholds onward, key lists,
  revocation on edges) is a feature, not a vector. The expectations are checked
  by a small test-only walker instead, and move to the engine unchanged when it
  gains delegation (T-065). Cost: the walker is a second, partial reading of
  §6.3 that nothing else uses.
- **Clipping a widening hop.** E-4 could have expected **yes**, by reading
  item 6 as "reduce to at most `deleg.depth − 1`" — the table row for `deleg`
  says "reduced to at most". Item 6 and "widening fails the path" say the hop
  is not followed. The vector takes item 6. R-M-10 ("reported as such, not
  intersected silently") agrees.
- **Evaluation results only in prose.** They are in `vectors.json` too, so a
  second implementation can consume them.

## Found, not fixed

- **SPEC-0004 §6.3 says two things about an over-deep `may-delegate`.** Item 6
  fails it; the state table's "`depth` reduced to at most `deleg.depth − 1`"
  reads as clipping. E-4 fixes the reading; the table row should say the
  reduction applies only when `depth` is absent. For the spec owners.
- **`may-delegate` present with `depth` absent** gives depth 0 (§6.3 item 3):
  the same effect as no `may-delegate`, so its `ranges` and key lists are
  inert. Harmless, but a writer may expect otherwise. Not exercised here.
