---
schema: "design-log/v1"
id: DL-0043
part: question
title: "Wallet release builds: release.yml, one PyInstaller file per OS, SHA256SUMS, pre-releases (mofn#127 S2, BACKLOG W-6)"
date: "2026-11-14"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "release.yml (macOS + Linux published, Windows tested, SHA256SUMS + build provenance); mofn.spec, requirements-release.txt, release/; APP-0005 Install the wallet; README Install; demo/slice.sh MOFN_BIN; wallet 0.8.1; BACKLOG-0001 0.14.3; PLAN-0004 0.5.0."
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

**Second ask, 2026-11-15: amend the PR to the #127 decisions.** After the
PR was opened, a separate session walked the human through #127's open
questions, and the human posted the answers on #127 on 2026-11-14 (Paul
confirmed in person):
<https://github.com/m-of-n/mofn/issues/127#issuecomment-6881640771>.
The PR, written before that, differed from them on D2–D5. The human chose to
amend this PR rather than revise the comment or open a new PR:

- **D1:** one PyInstaller `--onefile` per OS; no zipapp fallback. (The PR
  already did this.)
- **D2:** `SHA256SUMS` plus `actions/attest-build-provenance`; no GPG or
  minisign; the m-of-n self-attestation stays in #32.
- **D3:** Windows is CI only, not a release target for `wallet-v0.x`.
- **D4:** the first tag is the next PATCH, with a version bump in the same
  change (the comment said 0.6.1; `main` reached 0.7.0 before this amend, so
  it is `wallet-v0.8.1`).
- **D5:** a new APP-0005 *Install the wallet* on Pages; the README Install
  section stays short and links to it.
