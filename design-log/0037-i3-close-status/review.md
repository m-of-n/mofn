---
schema: "design-log/v1"
id: DL-0037
part: review
date: "2026-11-12"
---

# DL-0037 — review

**Human input:** Chip caught the agent's error (the floor read as an event)
and chose option (b). Chip has not reviewed §7.2 line by line. **Review
pending:** the sponsor (Paul, `nymble`), who owns mofn#31 and the plans.

## Rejected

- **(c) Delete the Nov 11 milestone from the plans.** Chip's first instinct,
  because "it did not happen". But what did not happen is an event that was
  never planned. The milestone was a real deadline, and it was partly missed.
  Deleting it would erase the record of what was planned and when. That is
  the same failure the design log exists to prevent.
- **The agent re-dating delegation or cutting it.** That is a schedule
  decision for the sponsor. §7.2 recommends (a), re-dating to I4, and decides
  nothing.
- **Writing the decisions into PLAN-0001 §12 here.** §12 already holds risks
  7 and 11. #156 merged them as open "At sign-off" questions while this PR was
  open. A second place for the same answers would drift, so §7.2 points at
  §12.
- **A separate status document.** PLAN-0004 §7.1 is already the place for
  schedule status. §7.2 continues it.

## The agent's own error, recorded

The agent read mofn#68's "the slice is the floor demo script" as a live demo
on Nov 11, and did not check PLAN-0001 §9 or PROC-0004 §5. It wrote of a
"rehearsal" and a "run order", and asked for a "floor outcome". The
corrections are in DL-0029 session 3 (mofn#160) and in edited comments on
mofn#68 and #157.
