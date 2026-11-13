---
schema: "design-log/v1"
id: DL-0036
part: review
date: "2026-11-09"
---

# DL-0036 — review

**Human direction:** reopen #7 and put §12 to all three. The PR itself is the
review: it is agreed when the sponsor and both students approve.

## What was rejected, and why

- **Taking the DEC-004 fallback (risk 6) in the document.** The cut date has
  passed, but taking it would decide how the demo treats tags. CLAUDE.md
  forbids documents that assume a tag language, and a cut is the signers'
  call. Written as a question.
- **Moving threshold reduction (risk 7) or chain delegation (risk 11) out of
  the floor.** Both are cuts that fall due Nov 11. The agent states the
  fallback and leaves the choice to sign-off.
- **Rewriting the original rows.** They are kept, with status beside them, so
  the signers can see what was planned against what happened. Only risk 10's
  fallback changes, because #127 §6 already rejected zipapp.
- **Calling risk 3 "held".** The library cap was never applied; 446 records is
  the risk absorbed, not cut.

## Owed

- Approvals from `nymble`, `davidhsiaotw` and `Ndewedo-Newbury` (the author's
  approval is the PR itself, since GitHub does not let an author approve).
- Answers on rows 6, 7 and 11, recorded in §12 before merge.
