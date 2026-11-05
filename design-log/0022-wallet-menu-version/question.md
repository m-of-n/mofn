---
schema: "design-log/v1"
id: DL-0022
part: question
title: "W-6 (mofn#127), wallet 0.1.0: the menu, --version, the CHANGELOG and the three-OS CI matrix"
date: "2026-11-04"
model: "claude-opus-5-5"
human: davidhsiaotw
outcome: "A bare mofn prints the menu (= mofn -h), mofn --version, a one-line missing-dependency message, UTF-8/LF output and wallet files, CHANGELOG 0.1.0, ci.yml on Linux, macOS and Windows; then key list, key export and hash from gpg, with every other gpg command mapped or left out. No spec change, no DEC-* touched."
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

- **one PR, `feat/w6-tui`**, for David's whole half. The agent first asked
  whether to plan "Both, as two PRs": 0.1.0, then 0.2.0 stacked on it. David
  picked it, reading "two PRs" as his and Chip's. Once he saw two branches, he
  corrected it to one. The work keeps two versions and two entries: this one
  covers 0.1.0 (menu, version, CHANGELOG and matrix), and DL-0023 covers
  0.2.0 (`mofn run`). They land together, in one squash merge;
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

## Update, 2026-11-05: three commands from `gpg`

David edited #127 once more and told the agent: "sorry, I update issue
again, but I don't know what's the different this time / may be additional
features copied from `gpg`".

The agent diffed the issue's two last versions through GitHub's edit history
(`userContentEdits`, 02:19 against 02:42, 2026-11-05). Only one thing changed:

- **Three new commands:** `key list` (like `gpg -k`, `-K`,
  `--fingerprint`; "Paul asked for key listing"), `key export LABEL` (like
  `--export`) and `hash FILE` (like `--print-md SHA256`). Each prints text
  and takes `--format json`.
- **Their menu rows.**
- **`mofn run`:** the Keys screen gains *Export* and runs `key list` and
  `key export`; Open a file runs `hash` for any other file.
- **A table of every other `gpg` command**, mapped to an existing mofn
  command or left out, each with its reason.
- **Version:** they belong to 0.2.0.
- **Acceptance:** "work from the CLI and from `mofn run`, with tests for
  each"; the design log names the `gpg` commands left out, and why.

In the same session David also asked that only the inner frame of
`mofn run` scroll; that is in DL-0023.

