---
schema: "design-log/v1"
id: DL-0022
part: question
title: "W-6 (mofn#127), wallet 0.1.0: the menu, --version, the CHANGELOG and the three-OS CI matrix"
date: "2026-11-04"
model: "claude-opus-5-5"
human: davidhsiaotw
outcome: "A bare mofn prints the menu (= mofn -h), mofn --version, a one-line missing-dependency message, UTF-8/LF output and wallet files, CHANGELOG 0.1.0, ci.yml on Linux, macOS and Windows. No spec change, no DEC-* touched."
status: open
---

# DL-0022 — question

## The brief

Paul's comment on the W-1 engine: there is no guide, and nothing to download.
David opened mofn#127 (W-6) from it, then told the agent: "I created an issue
#127, need to update previous wallet engine as it is not completed said by
Paul".

#127 splits the work. David owns the engine: the menu, `--version`, `mofn run`
and the `ci.yml` matrix. Chip owns `release.yml`, the builds and the README
install section. The agent wrote a plan, and David chose two things on it:

- **two PRs**, one per release. This one is `wallet-v0.1.0`: menu, version,
  CHANGELOG and matrix. `mofn run` is `wallet-v0.2.0`, in DL-0023, on a branch
  stacked on this one. 0.1.0 goes first, because Chip's `release.yml` reads
  `__version__` from it;
- **commit locally only**. No push and no PR. So the Windows and macOS changes
  below are not yet run on those systems.

The agent was held to these constraints:

- every subcommand's output stays byte for byte the same, because
  `demo/slice.sh` and the goldens depend on it;
- `src/` stays empty;
- no primitive is added;
- GnuPG supplies the shape of the tool and its help screen only.

## Context supplied

- mofn#127 in full;
- `prototype/wallet/` and `demo/slice.sh` as #125 merged them;
- `.github/workflows/ci.yml`;
- APP-0001 `version_policy`;
- R-0002 §7.2–7.3;
- the branch protection of `main`, which shows that only `docs` and `dco` are
  required checks.
