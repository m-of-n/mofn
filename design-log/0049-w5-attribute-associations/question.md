---
schema: "design-log/v1"
id: DL-0049
part: question
title: "W-5: attribute associations on every verdict — who signed, topic, digest, standing (`check --format json`, `mofn run` Check tab; mofn#69)"
date: "2026-11-16"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "wallet 0.9.0: `associations` in `check --format json`, rendered under every verdict in the Check tab; README *The verdict as JSON*; goldens fixtures/golden/associations-*.json; BACKLOG-0001 0.15.3 W-5 in review."
status: open
---

# DL-0049 — question

The human asked the agent to complete mofn#69 (BACKLOG W-5) as rescoped on
2026-11-09 (`DECISIONS-0001` item 28; the windowed GUI moved to W-7 #179).
Done when:

- `mofn check --format json` emits, per verdict, **who signed** (key / named
  principal), **topic** (domain + type), **the subject's digest**, and
  **standing** (root → delegation → key, or "no standing");
- `mofn run`'s Check tab shows all four on every verdict;
- for the W-4 slice cases (green, `authorization FAIL`, `integrity FAIL`) the
  TUI verdict matches the CLI;
- standing shows full chains once #173 (delegation in the TUI) lands. The
  engine already reduces chains (wallet 0.7.0, `reduce._walk`): render
  whatever the engine reports.

Constraints given: work in `prototype/wallet/`; `src/` stays empty; no
reimplemented crypto or reduction; decide neither DEC-004 nor DEC-005 and
mark no DEC-* accepted; keep the shape stable and documented, because W-7's
PySide6 app reuses the same JSON.
