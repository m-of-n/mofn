---
schema: "design-log/v1"
id: DL-0033
part: review
date: "2026-11-09"
---

# DL-0033 — review

**Human decisions:** T-030 and T-032 are closed. T-029c: keep everything
Python (`DECISIONS-0001` item 28); then, asked whether D8 needs a desktop
window: *"We shall use the Textual app."* W-5 is rescoped into `mofn run`. The reasons on the rows are
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
- **Tauri (T-029c option a).** Rejected by the human: keep everything Python.
  The agent's argument for it — small installers, a modern UI, a sidecar the
  engine's JSON output already supports — did not outweigh one language.
- **PySide6 (option b).** Rejected by the human: the Textual app is the UI.
  A windowed GUI would have been a second UI to keep in step with the engine,
  four weeks before Dec 4.
- **Cutting W-5 outright.** The agent rescoped it instead: #69's attribute
  associations (signer, topic, digest, standing) are not yet in `mofn run`'s
  Check tab, and they are the part of #69 that is not about a window.
- **The agent's own "a second toolchain for a skin".** Withdrawn as stated: W-5
  asks for a desktop window, so the comparison was never Tauri against
  nothing.
- **Treating the sponsor's merge of library#42 as L-035's ruling.** A merge
  with no review and no comment is not a recorded decision. Left `review`.
- **Closing T-013 on the strength of #7 being closed.** The issue's own
  done-when was not met. Left `todo`, with "reopen #7".
- **Resolving the W-/T- overlap.** Still flagged, still a planning call.

## Owed

- L-035: one line from the sponsor accepting library#42's rule.
- T-013: a §12 PR all three approve, or a decision to drop it.
- `spec/schema/README.md` and `spec/vectors/README.md` are stale; both are
  noted on T-030 and T-046 and left for a `spec/` PATCH.
