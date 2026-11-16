---
schema: "design-log/v1"
id: DL-0045
part: question
title: "PLAN-0001 0.7.1 §12 — answer the overdue cuts by building them (T-013, mofn#7)"
date: "2026-11-14"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "PLAN-0001 0.7.1: §12 status at 2026-11-14; rows 6, 7, 10, 11 answered by PRs #167, #168, #169; row 3 closed as absorbed; #156's merge recorded as without a standing approval."
status: open
---

# DL-0045 — question

Asked: what is PLAN-0001 §12 and why does it need sign-off; then, which of
rows 6, 7 and 11 are already complete in the repository.

Finding at `main` `10e357f`: none. T-042 and T-043 were `todo`; `reduce.py`
was one hop and did not reduce thresholds; W-3 (#67) was open.

The human then rejected the agent's recommendations to move dates, and
directed: complete the risks now — not only 6, 7 and 11 — delegating each to
its own worktree, since the dates had passed. The human also stated that #156
had been approved, but the approval was dismissed when a `dco` fix was pushed,
and the PR then merged without re-approval.

Context: `PLAN-0001` 0.7.0 §12; `BACKLOG-0001` T-013, T-041…T-047, W-3, W-6;
`PLAN-0004` §7.2; `R-0006` §4.7; #67, #127, #156.
