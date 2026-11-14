---
schema: "design-log/v1"
id: DL-0043
part: question
title: "Wallet release builds: release.yml, one PyInstaller file per OS, SHA256SUMS, pre-releases (mofn#127 S2, BACKLOG W-6)"
date: "2026-11-14"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "release.yml; prototype/wallet/mofn.spec, requirements-release.txt, release/; wallet README Install; demo/slice.sh MOFN_BIN; BACKLOG-0001 0.13.4; PLAN-0004 0.4.2."
status: open
---

# DL-0043 — question

The human asked for the release half of BACKLOG W-6 / mofn#127 (Chip's half;
PLAN-0001 §12 risk 10):

- a `release.yml` that builds **one self-contained PyInstaller binary per OS**
  (Linux, macOS, Windows) of the `mofn` wallet;
- `SHA256SUMS`, and GitHub **pre-releases on `wallet-v*` tags**, the first
  `wallet-v0.2.0`, no `wallet-v0.1.0`;
- each build smoke-tested in the workflow: `mofn --version`, and `mofn check`
  on a fixture;
- an Install section in `prototype/wallet/README.md`.

The human gave **zipapp as rejected** (#127 §6: a zipapp cannot load
PyNaCl's native extension), which settles #127's open "zipapp plus Python, or
a per-OS build" in favour of the per-OS build. The human told the agent **not
to push a tag or create a release**, and to update BACKLOG W-6 and PLAN-0004,
not PLAN-0001 §12.

The work was done in two sessions. The first stopped when the machine slept,
leaving the files uncommitted; the second reviewed all of it, re-ran the
build and every test below, and finished. This entry is written in the same
change as the files, not afterwards.
