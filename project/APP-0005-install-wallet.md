---
schema: "archdoc/v1"
id: APP-0005
title: "Install the wallet — download, check, run"
short_title: "Install the wallet"
description: "How to download a mofn wallet pre-release for macOS or Linux, check it against SHA256SUMS and its build provenance, and run it without a checkout. The download page PLAN-0002 M6 asks for (#127 §7)."
type: design
category: product
status: draft
version: "0.1.0"
version_policy: "semver; PATCH = editorial; MINOR = a platform or check added; MAJOR = the install path changes"
date: "2026-11-15"
updated: "2026-11-15"
decision_makers: []
reviewers: []
needs_review: true
reviewed: false
canonical_path: project/APP-0005-install-wallet.md
companion:
  - project/PLAN-0004-application-plan.md
  - project/PLAN-0002-product-spec.md
  - project/BACKLOG-0001.md
defers_to: ARCH-0001
backlog: W-6
---

# Install the wallet

!!! warning "Prototype"
    DEC-004 and DEC-005 are open in ARCH-0001. Do not use real keys, and do
    not rely on a verdict.

`mofn` is the wallet's command line, and `mofn run` opens it as a terminal
app. Each release is one file per OS with its own Python and PyNaCl inside.
Nothing else needs installing, and you do not need a clone of this repository
(#127, PLAN-0004 §9, DL-0043).

## 1. Download

The releases are pre-releases tagged `wallet-vX.Y.Z`:
**[all wallet releases](https://github.com/m-of-n/mofn/releases?q=wallet-v&expanded=true)**.
(`/releases/latest` skips pre-releases, so this page does not link to it.)

From one release, download the file for your machine and `SHA256SUMS` into
one folder.

| file | for |
|---|---|
| `mofn-X.Y.Z-macos-arm64` | macOS on Apple silicon |
| `mofn-X.Y.Z-linux-x86_64` | Linux, x86-64, glibc 2.35 or later (Ubuntu 22.04 and newer) |

Windows and Intel Macs are not release targets for `wallet-v0.x` (#127 D3).
Windows builds are tested in CI but not published; on those machines, run
from a checkout (`prototype/wallet/README.md`, *Run*).

## 2. Check it

**The checksum** shows the file is the one listed in the release:

```sh
shasum -a 256 --ignore-missing -c SHA256SUMS      # macOS
sha256sum --ignore-missing -c SHA256SUMS          # Linux
```

**The build provenance** shows the file was built by this repository's
`release.yml`, from the tagged commit. With the GitHub CLI:

```sh
gh attestation verify mofn-X.Y.Z-macos-arm64 -R m-of-n/mofn
```

Both checks say where the file came from. Neither is an m-of-n statement: a
release that carries an m-of-n statement over its own digest, checked by
`mofn` itself, is #32, and waits on DEC-004 and DEC-005.

## 3. Run it

```sh
chmod +x mofn-X.Y.Z-macos-arm64
./mofn-X.Y.Z-macos-arm64 --version      # what this mofn is built from
./mofn-X.Y.Z-macos-arm64                # the menu, the same as -h
./mofn-X.Y.Z-macos-arm64 run            # the wallet as a terminal app
```

The files are not code-signed or notarized, so macOS will say the developer
is unknown. A file a browser downloaded will not open until you clear its
quarantine mark:

```sh
xattr -d com.apple.quarantine mofn-X.Y.Z-macos-arm64
```

A `curl -LO` download has no such mark. Each file unpacks itself to a
temporary folder when it starts, so the first command takes a second or two.

Rename the file to `mofn` and put it on your `PATH` if you like. On first
run, `mofn run` offers the example vocabulary, so you can sign and check
without a clone.

## Where this comes from

- **Built by** `.github/workflows/release.yml` on a `wallet-vX.Y.Z` tag. The
  tag must equal `__version__` in `prototype/wallet/engine/__init__.py`, and
  the release notes are that version's section of
  `prototype/wallet/CHANGELOG.md`.
- **Tested** on a fresh runner with no checkout and no Python packages:
  `--version`, the menu, a green `check` of TV-4 against its golden, and
  `mofn run` opening Learn.
- **Decisions** D1–D5 for the release are on #127 and in
  `design-log/0043-release-builds/`.

## What changed in v0.1.0 — 2026-11-15

- First version: download, the checksum and provenance checks, running it,
  and the macOS quarantine step. macOS arm64 and Linux x86-64 only.
