---
schema: "design-log/v1"
id: DL-0043
part: review
date: "2026-11-14"
---

# DL-0043 — review

**Owed from the human** (done 2026-11-16, see *Released* below). Review of
the PR. Then the human, not the agent, pushes the first tag (`git tag -s wallet-v0.8.1 && git push origin
wallet-v0.8.1` on the merged commit), checks the pre-release and runs
`gh attestation verify` on both files from a machine with no checkout. Then
the BACKLOG W-6 row goes to done and #127 can close.

**Accepted by the human, 2026-11-14 (#127 comment, Paul confirmed):** D1–D5
as listed in `question.md`. The first draft of this PR was written before
them and was amended to match; what changed is below.

**First tag `wallet-v0.8.1`, not `wallet-v0.2.0`** (#127 D4). See
`produced.md` for why the original tag cannot build. If a 0.2.0 file is wanted anyway, the way is a `workflow_dispatch`
input naming an old ref and a separate publish; the agent did not build it,
because nobody needs the 0.2.0 engine and it would be a second release path
to keep correct.

**Windows.** The first draft built, smoke-tested *and published* Windows, as
the first ask said. #127 D3 then decided it is CI only, so the amend keeps
the build and smoke jobs (they catch a Windows regression for free) and
drops the file from the publish.

**Design-log id.** The #127 comment named `design-log/0041-wallet-release/`;
0041 was taken by W-3 before this landed, and this PR already held 0043, so
the record stays here.

## What was rejected, and why

- **zipapp** (PLAN-0001 row 10). Rejected by the human (#127 §6): it cannot
  load PyNaCl's extension, so an install would still need Python 3.12 and
  pip, which is not "self-contained".
- **PyInstaller one-folder builds.** Faster start, but a folder to unzip per
  OS; #127 asks for one file to download and check against `SHA256SUMS`. The
  cost — a second or two unpacking on each start — is in the README.
- **Nuitka, shiv/pex, Briefcase.** Nuitka needs a C toolchain per runner and
  is slower to build; shiv/pex are zipapps with the same PyNaCl problem;
  Briefcase is an app bundler aimed at the GUI, which is decision #28's
  business, not this one.
- **A frozen-aware code path** (`sys._MEIPASS` checks in the modules).
  Rejected: `mofn.spec` places the data files where `screens/learn.py` and
  `screens/example.py` already look, relative to `__file__`, so no module
  knows it is frozen and the tests cover the frozen layout for free.
- **Smoke-testing on the build runner only.** Rejected: that runner has the
  checkout and a Python with every dependency, so a build that silently
  imports from the checkout would pass. The `smoke` job runs on a fresh
  runner with neither.
- **`--version` and `check` as the whole smoke test** (the request's
  minimum). Kept, and extended with `mofn run` in a pty, because the negative
  build showed `check` passes on a build with no data files while `mofn run`
  crashes.
- **`ubuntu-latest` for the Linux build.** Rejected for 22.04: a PyInstaller
  file needs the build machine's glibc or newer, and 22.04 has the older one.
- **No signature at all** (the first draft). Reversed by #127 D2: build
  provenance is free on a public repository and protects against a
  compromised release, which `SHA256SUMS` alone does not.
- **GPG or minisign** (#127 D2). Students would hold a project key, and no
  one has decided who holds it.
- **An m-of-n statement over the release now** (#127 D2). It would bind to
  prototype encoding choices while DEC-004 and DEC-005 are open, and read as
  if they were settled. It stays in #32.
- **Apple notarization.** Needs a paid Apple developer identity; not needed
  for a prototype. APP-0005 gives the quarantine step instead.
- **Publishing the Windows `.exe`** (#127 D3, reversing the first draft). The
  key-mode test and the slice are skipped on Windows, an unsigned one-file
  build trips SmartScreen and antivirus, and PLAN-0002 M6 is macOS + Linux.
- **Dropping Windows from the build and smoke jobs.** They catch regressions
  for the cost of a runner.
- **macOS x86-64 or universal2.** Another runner; M6 does not need it.
- **A zipapp fallback beside the build** (#127 D1). Same PyNaCl problem;
  running from a checkout is already the fallback.
- **Tagging `wallet-v0.7.0` at the merge** (#127 D4). The bundled README
  differs from 0.7.0, so two different builds would carry one version.
- **`wallet-v0.8.0`.** The release adds no engine behaviour; PATCH is enough.
- **Backfilling 0.2.0–0.7.0 with `workflow_dispatch`.** It would build old
  trees with today's recipe, which is not what was tested then, and no one
  needs those builds.
- **The download page as a section of PLAN-0004 §9** (#127 D5). A plan tracks
  work; a stranger looking for install steps should not land in one.
- **Staging the wallet README on Pages.** It has no archdoc front-matter,
  needs `build-site` and manifest changes, and a second copy of the steps
  would drift. APP-0005 holds the steps; the README links to it.
- **Leaving `demo/slice.sh` untouched.** The resumed session was told to
  justify or revert this change. Kept: `MOFN_BIN` is how `release.yml` runs
  the five slice cases under both codecs against each build, which catches a
  codec module PyInstaller's scan missed — the smoke test checks one case
  under the default codec only. With `MOFN_BIN` unset the script takes
  exactly the old path, so #127's "the slice stays the weekly gate, run
  from source" holds.
- **Publishing on every push to `main`** or a rolling `latest`. Rejected: a
  release is a human act, a tag.

## CI on #169, 2026-11-15

The first run of `release.yml` on the PR failed in two places, both fixed in
the same PR:

- **`macos-14` is no longer offered** ("configuration
  'macos-14-arm64-us-default' is not supported"). Pinned to `macos-15`
  instead. **Rejected: `macos-latest`** — #127 D1 asks for a pin so the
  build does not move under us; a retired pin is replaced by a newer pin.
- **`demo/slice.sh` ④–⑥ died with "`: command not found`"** under
  `MOFN_BIN`: `in_days` calls `$PY`, which the `MOFN_BIN` path leaves empty.
  `in_days` now falls back to `python3` (stdlib only). **Rejected: `date -d`
  / `date -v`** — GNU and BSD `date` differ, and the slice runs on both.
  **Rejected: setting `PY` under `MOFN_BIN`** — `PY` would then be
  half-meaningful (no `nacl`/`yaml` check), and the import guard keys on it.
  This was missed locally because the slice was only run from source.

## Rebase onto #167, 2026-11-16

#167 (T-043, k-of-n thresholds) merged first and took wallet **0.8.0**. #127
D4's rule is "a PATCH on whatever `main` is when this merges", so the first
tag moves from `wallet-v0.7.1` to **`wallet-v0.8.1`**: `__version__`, the
`CHANGELOG.md` heading `release.yml` reads, APP-0005, PLAN-0004 and the
lines above. The rejected options above are left as written; they were
right for the `main` of their date. **Rejected: keeping 0.7.1** — a version
below `main`'s would make the release older than the code it ships.
BACKLOG → 0.14.3. Rebased, not merged; rerere was off, because a cached
resolution from a dry run had silently dropped #167's rows.

## Released, 2026-11-16

#169 merged as `98a89b0`. The human pushed `wallet-v0.8.1` on it; the tag
run of `release.yml` passed (version gate, three builds, three smokes on
fresh runners, publish). The pre-release, by `github-actions[bot]`, holds
`mofn-0.8.1-linux-x86_64`, `mofn-0.8.1-macos-arm64` and `SHA256SUMS`, and no
Windows file (D3). Its notes are the 0.8.1 CHANGELOG section plus the
prototype warning and the APP-0005 link. APP-0005 is live on Pages.

Checked by the agent on a Mac (arm64), in a scratch folder with no checkout,
under `env -i PATH=/usr/bin:/bin`: `shasum -a 256 --ignore-missing -c
SHA256SUMS` → OK; `gh attestation verify mofn-0.8.1-macos-arm64 -R
m-of-n/mofn` → exit 0, one attestation on record; `--version` → `mofn 0.8.1
(prototype)`; a bare `mofn` → the menu, exit 0. **Not checked by hand: the
Linux file** (no Linux machine here); its only evidence is the tag run's
smoke job on a fresh `ubuntu-latest` runner.

The release half of #127 is complete. #32 (the self-attested release) is
unchanged by it.
