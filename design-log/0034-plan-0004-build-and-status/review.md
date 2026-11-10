---
schema: "design-log/v1"
id: DL-0034
part: review
date: "2026-11-09"
---

# DL-0034 — review

**Human input:** Paul asked for the build-and-release section ("yes — do it")
and for the dated schedule-status reading in the same PR. Human review of the
text is pending on the PR. No DEC-* is accepted here.

## Options considered

| # | option | outcome |
|---|---|---|
| 1 | Add only a "Build and release" section | **superseded** by the second ask, which required §7.1 in the same change |
| 2 | Mark decision #28 accepted, or pick Tauri / PySide6 / SwiftUI in this PR | **rejected** — only an ADR accepts a decision; #28 stays open |
| 3 | Rewrite #67 and #31, or edit BACKLOG W-3, in this PR | **rejected** — the recover list asks Paul to rewrite those issues; this file only records that they are stale (`may-speak`, short-expiry-only revocation) |
| 4 | Treat #148's delegation vectors and `test_delegation.py` as engine work done | **rejected** — the test file itself says it is a test-only walker and "is not the engine" |
| 5 | Put the status reading in BACKLOG-0001 instead of PLAN-0004 | **rejected** — Paul asked for it next to PLAN-0004 §7 |
| 6 | Renumber existing §8, or edit §4 | **rejected** — keep the §8 anchor; §4 is left as it was (it still says "DEC-002 stays open", which is stale relative to `ADR-0004`, and is not fixed here) |
| 7 | Claim a zipapp is a self-contained download | **rejected** — `pynacl` is a native extension and cannot be bundled portably; the text states the install requirement and leaves the packaging choice open |

The recover list and the status table are the parts a reviewer should check
against the repo. If a row is wrong, correct the document, not this entry.
