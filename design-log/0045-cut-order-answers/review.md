---
schema: "design-log/v1"
id: DL-0045
part: review
date: "2026-11-14"
---

# DL-0045 — review

**Human direction:** build the overdue cuts, do not re-date them. This PR is
the review: §12 is agreed when the sponsor and both students approve it, or
record approval on mofn#7.

## What was rejected, and why

- **The agent's own recommendations to re-date risk 7 and make W-3 upside**
  (risk 11). Rejected by the human: the dates had passed and the work was
  tractable, so building it was cheaper than another round of deciding.
- **Marking rows 6, 7, 10, 11 "closed" in this change.** Their PRs are in
  review, not merged; a row closes when its PR merges.
- **Writing risk 6 as "fallback taken" in the `ARCH-0001` sense.** The floor
  is met by `SPEC-0003` `delegation: 1`, not by a new opaque-tag profile, and
  DEC-004 stays open. Saying "fallback taken" would read as a DEC-004 choice.
- **"Nothing else in the floor is owed."** Drafted, then struck: `PLAN-0004`
  §7.2 still lists issuer revocation and a recorded demo as not met.
- **Treating #156's merge as a sign-off.** An approval dismissed by a later
  push is not a standing approval; the PR's own condition was unmet.
- **A second resumed W-3 delegate.** Started when the first appeared to stop
  mid-test; cancelled on finding #168 already open. It had changed nothing.

## Owed

- Approvals from `nymble`, `davidhsiaotw` and `Ndewedo-Newbury`.
- Rulings: `SPEC-0004` §6.4's two readings (#167); `delegation: 1` against
  `may-delegate` ranges (#168); first tag `wallet-v0.8.1` (#169; proposed as `wallet-v0.6.0`).
- #168's design log renumbered `0041` → `0044` (taken by #166).

## Rebase, 2026-11-16

#168, #167 and #169 merged before this did. §12 keeps its 2026-11-14 table and gains a dated note that rows 6, 7 and 11 are closed; row 10 waits on the first pre-release. **Rejected: rewriting the table's status cells** — it is a dated reading, and the approval this PR asks for is of the answers, not of the merge dates. Row 10's tag is corrected to `wallet-v0.8.1` because it was a fact, not a status. BACKLOG → 0.15.1, after #166's 0.15.0.
