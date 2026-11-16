---
schema: "design-log/v1"
id: DL-0043
part: produced
date: "2026-11-14"
---

# DL-0043 — produced

No primitive, no spec text, no `DEC-*`. Packaging and CI only; `src/` stays
empty.

| file | what |
|---|---|
| `.github/workflows/release.yml` | jobs `version` → `build` (×3) → `smoke` (×3) → `release` (tag only) |
| `prototype/wallet/mofn.spec` | the one-file PyInstaller build; data files at the paths the modules already compute from `__file__` |
| `prototype/wallet/requirements-release.txt` | `-r requirements.txt` plus `pyinstaller==6.22.3`, `pyinstaller-hooks-contrib==2026.10`, `cffi==2.1.1` |
| `prototype/wallet/release/smoke.sh` | the smoke test, run where there is no checkout |
| `prototype/wallet/release/pty_run.py` | opens `mofn run` in a pty, opens Learn, quits on ctrl+q |
| `project/APP-0005-install-wallet.md` | the download page on Pages: download, `SHA256SUMS`, `gh attestation verify`, run, macOS quarantine (#127 D5) |
| `prototype/wallet/README.md` | a short Install section linking APP-0005; two rows in the file table |
| `prototype/wallet/engine/__init__.py`, `CHANGELOG.md` | 0.8.1, the first release (#127 D4) |
| `demo/slice.sh` | `$MOFN_BIN`: run a built `mofn` instead of the source |
| `.gitignore` | `prototype/wallet/build/`, `dist/` |

**`release.yml`.**

1. `version` — the tag must be `wallet-v` + `__version__`
   (`engine/__init__.py`), and `CHANGELOG.md` must have a
   `## X.Y.Z — YYYY-MM-DD` heading for it.
2. `build` — on `ubuntu-22.04` (glibc 2.35, so the file runs on newer
   distributions), `macos-15` (arm64; pinned, as #127 D1 says, so the build
   does not move when `macos-latest` does) and `windows-latest`. Python 3.12,
   `pyinstaller mofn.spec`, then `--version` must print
   `mofn X.Y.Z (prototype)`, then `demo/slice.sh` runs against the build with
   `MOFN_BIN` (5 cases × 2 codecs; not on Windows, where `chmod 000` does
   nothing, as in `ci.yml`).
3. `smoke` — a **fresh runner with no checkout, no `setup-python`, no pip**
   downloads the build and a folder of fixtures and runs `release/smoke.sh`:
   `--version`; a bare `mofn` (the menu); a fresh wallet makes a key, imports
   Alice's TV-1 key, roots her for build provenance and checks TV-4 at
   2026-10-15 — exit 0 and output equal to `fixtures/golden/green.txt` with
   Alice's label in place of "release machine"; then, where Python has
   `pty` (Linux, macOS), `pty_run.py` opens `mofn run`, presses `?` for Learn
   and ctrl+q, and fails on a non-zero exit or a traceback.
4. `release` — only on a tag: downloads the **Linux and macOS** builds only
   (Windows is built and smoke-tested in 2–3 but never published, #127 D3);
   `SHA256SUMS` over exactly two files; `actions/attest-build-provenance`
   over each (`id-token: write`, `attestations: write`; Sigstore, keyless,
   #127 D2); notes = that version's CHANGELOG section plus the prototype
   warning, the two checks and the APP-0005 link;
   `gh release create --prerelease --verify-tag`.

A pull request touching the wallet, `demo/slice.sh` or `release.yml` runs
1–3; so does a manual run.

**Verified locally, 2026-11-14, macOS arm64**, PyInstaller 6.22.3, Python
from the pinned venv:

- `pyinstaller --clean --noconfirm mofn.spec` → `dist/mofn`, 15 MB.
- `smoke.sh` under `env -i PATH=/usr/bin:/bin` (no wallet venv on the path):
  all green, `pty_run: mofn run opened Learn and quit, exit 0`.
- `MOFN_BIN=dist/mofn demo/slice.sh`: 5 cases × 2 codecs passed. The source
  path (`MOFN_PYTHON=…`, no `MOFN_BIN`) still passes, unchanged.
- **Negative build**: the same spec with `datas = []` (textual's own data
  kept) builds, passes `--version`, the menu **and the TV-4 check** — then
  fails in `pty_run.py`: `mofn run` dies in `compose` with
  `IndexError: list index out of range` and a traceback, and the smoke exits
  1. So the `check` smoke alone would ship a broken `mofn run`; the pty step
  is what guards the data files.
- `pytest` in `prototype/wallet`: 386 passed. `actionlint release.yml`:
  clean.

Not verified: the Linux and Windows builds (no runner here; the PR's own
`release` run is the first). Windows gets no `mofn run` smoke (no `pty`).

**The first tag is `wallet-v0.8.1`, not `wallet-v0.2.0`.** A tag push runs
the `release.yml` *of the tagged commit*. No commit before this one has a
`release.yml`, so `wallet-v0.2.0` on its commit would run nothing; and
`wallet-v0.2.0` on today's commit fails step 1. The intent of "from 0.2.0"
was "never a 0.1.0" (BACKLOG W-6); that still holds. The first draft of this
PR said `wallet-v0.6.0`; #127 D4 made it a PATCH bump in this change, and
`main` was at 0.7.0 when the PR was amended, and at 0.8.0 (#167) when it was rebased.

**Amend, 2026-11-15.** Rebased onto `main` `dae3cfd` (conflicts in
`design-log/README.md`, `BACKLOG-0001.md` and `PUBLISHING.md`, resolved by
keeping both sides). The changes for D2–D5 are listed above. Not re-verified
locally after the amend: the attestation step and the two-file publish run
only on a tag, so the first tag is their first run.
