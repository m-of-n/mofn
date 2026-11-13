---
schema: "design-log/v1"
id: DL-0036
part: question
title: "PLAN-0001 0.7.0 §12 — put the cut order to all three for sign-off (T-013, mofn#7)"
date: "2026-11-09"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "PLAN-0001 0.7.0: §12 keeps the original ten risks, adds a status column and risks 11 and 12, and states that the order is agreed only when all three approve the PR. mofn#7 reopened."
status: open
---

# DL-0036 — question

The search in `DL-0038` found no record that the cut order was ever agreed:
mofn#7's done-when ("all three have signed off in the PR") was never met, and
the issue was closed on 2026-10-28. The human said the closure was their
mistake and directed the agent to complete the next steps: reopen #7, and open
a PR on `PLAN-0001` §12 for all three to approve.

Context: `PLAN-0001` 0.6.4 §12; `BACKLOG-0001` 0.13.0 (PR #155); `ADR-0004`,
`ADR-0006`; `DECISIONS-0001` item 28; #127 §6; `prototype/wallet/engine/reduce.py`.
