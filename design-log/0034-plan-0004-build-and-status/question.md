---
schema: "design-log/v1"
id: DL-0034
part: question
title: "PLAN-0004 build-and-release section, and a Nov 9 schedule status"
date: "2026-11-09"
model: "Grok Bot"
human: nymble
outcome: "PLAN-0004 0.3.0 adds §7.1 (schedule status, 2026-11-09) and §9 (build and release). No DEC-* accepted. Decision #28 stays open."
status: open
---

# DL-0034 — question

## The brief

Paul (sponsor, GitHub `nymble`) asked what the app building plans are — CLI,
GUI, Mac and Linux — and whether a build infrastructure is set up. After being
pointed at PLAN-0004, he said to add a short "Build and release" section there
and open a PR. In the same change he asked for a dated "Schedule status, Nov 9,
2026" section next to §7, evidence-based, reviewing where the project is
behind against PLAN-0004 §7, PLAN-0003, PLAN-0001 D1–D9 and I2–I5, PLAN-0002
milestones, BACKLOG-0001, DECISIONS-0001 due dates, and issues #31, #65, #67,
#68, #69 and #127.

## Context supplied

- PLAN-0004 v0.2.0 (no build or release section; §7 dates unchanged here).
- PLAN-0001 row 10 (single-file Python zipapp), PLAN-0002 M6 (macOS and Linux
  installs from Pages), decision #28 (Tauri tentative, PySide6 fallback, due
  Oct 14).
- Main at `c84a0e7` (2026-11-09). No tags, no `release.yml`.
- `prototype/wallet/requirements.txt`, `engine/reduce.py` (last changed
  `b7600fe`, 2026-11-01), `engine/check.py`, `tests/test_delegation.py` (#148),
  `demo/slice.sh`, `.github/workflows/`.
- The sponsor's earlier direction: delegation is required for the Nov 11
  floor; the wallet maintains sets of statements for delegation.
- `ADR-0003` D5 accepts issuer revocation. DL-0025 retired `may-speak`.
- Open PR #152 already holds `DL-0032`, so this entry took `0033`; renumbered `0034` when mofn#154 merged `0033-second-domain` first.
