---
schema: "design-log/v1"
id: DL-0038
part: question
title: "BACKLOG-0001 0.13.0 — reconcile the backlog with the repos; close T-030 and T-032; spell out T-029c"
date: "2026-11-09"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "BACKLOG-0001 0.13.0: 26 rows marked done with evidence, T-030 and T-032 closed, T-029c decided (Python throughout, the Textual app is the UI, W-5 rescoped; DECISIONS-0001 0.7.0 item 28, PLAN-0002 0.3.1, PLAN-0004 0.2.1), T-013 and L-035 searched and found unrecorded, T-066 and L-037…L-040 added. No spec change, no DEC-* touched."
status: open
---

# DL-0038 — question

The human asked: *"how much of the backlog is actually finished but
undocumented? Search the entire repo."* The agent swept `origin/main`
(issues, merged PRs, `prototype/wallet/`, `spec/vectors/`, CI, `demo/`) and,
through a read-only subagent, `m-of-n/library` main (`bin/validate`: 446
records, 0 scaffolds). It reported 26 of 102 rows finished but not marked, and
about a dozen partly done or overtaken.

The human then directed: *"Open a worktree, update BACKLOG-0001. T-030 and
T-032 are closed. Elaborate on T-029c."* The agent wrote T-029c up as three
options — (a) Tauri, (b) PySide6, (c) Textual as the Fall 2026 UI — and
recommended (c), arguing Tauri "would mean a second toolchain for a skin".
Asked what the problem with that was, the agent listed the costs (Rust and
TypeScript, two packaging systems, two UIs to keep in step, a new test
harness) and conceded two points against itself: the engine already has
`--format json` and `--passphrase-stdin`, so a sidecar is cheap; and W-5 asks
for a desktop window, which Textual is not.

The human then directed: *"Look for the recorded ruling on L-035 and whether
T-013's order was ever actually agreed. The decision for T-029c is we want to
keep everything Python."*

Context: `BACKLOG-0001` 0.12.15; `ADR-0004`; `SPEC-0002` Appendix B;
`PLAN-0001` §12; `PLAN-0002` stack table; `PLAN-0004` §4; `DECISIONS-0001`
item 28; `project/meetings/2026-09-28.md` MD-7; mofn#7, #65, #69, #110, #127,
#152; library#3, #5, #42, #45, #46, #48, #58, #88, #89, #69, #99, #110, #111,
#132, #133.
