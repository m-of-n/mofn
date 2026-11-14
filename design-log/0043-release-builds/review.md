---
schema: "design-log/v1"
id: DL-0043
part: review
date: "2026-11-14"
---

# DL-0043 — review

**Owed from the human.** Review of the PR. Then the human, not the agent,
pushes the first tag (`git tag -s wallet-v0.6.0 && git push origin
wallet-v0.6.0` on the merged commit) and checks the pre-release. Linking the
release from Pages (#127 §7) is still owed. #127 stays open.

**Departure the human must accept or reverse: first tag `wallet-v0.6.0`.**
The request said `wallet-v0.2.0`. See `produced.md` for why that tag cannot
build. If a 0.2.0 file is wanted anyway, the way is a `workflow_dispatch`
input naming an old ref and a separate publish; the agent did not build it,
because nobody needs the 0.2.0 engine and it would be a second release path
to keep correct.

**Windows** is built, smoke-tested and published, as the human asked.
PLAN-0004 §9 keeps "whether Windows is a *supported* target" open, because
#127 §6 said "only if that is decided" and nothing records the decision.

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
- **Signing the files** (Sigstore, GPG, Apple notarization). Not done: how
  releases are signed is open (#127, PLAN-0004 §9), and choosing a signer
  now would decide it. The README and the release notes say the files are
  not signed.
- **Leaving `demo/slice.sh` untouched.** The resumed session was told to
  justify or revert this change. Kept: `MOFN_BIN` is how `release.yml` runs
  the five slice cases under both codecs against each build, which catches a
  codec module PyInstaller's scan missed — the smoke test checks one case
  under the default codec only. With `MOFN_BIN` unset the script takes
  exactly the old path, so #127's "the slice stays the weekly gate, run
  from source" holds.
- **Publishing on every push to `main`** or a rolling `latest`. Rejected: a
  release is a human act, a tag.
