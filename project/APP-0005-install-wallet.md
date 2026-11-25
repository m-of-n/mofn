---
schema: "archdoc/v1"
id: APP-0005
title: "Install the wallet — download, check, run"
short_title: "Install the wallet"
description: "How to download a mofn wallet pre-release — the macOS desktop app (a DMG, or a zip), or the CLI for macOS or Linux — check it against SHA256SUMS and its build provenance, and run it without a checkout. The download page PLAN-0002 M6 asks for (#127 §7)."
type: design
category: product
status: draft
version: "0.3.0"
version_policy: "semver; PATCH = editorial; MINOR = a platform or check added; MAJOR = the install path changes"
date: "2026-11-15"
updated: "2026-11-25"
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
backlog: [W-6, W-7]
---

# Install the wallet

!!! warning "Prototype"
    DEC-004 and DEC-005 are open in ARCH-0001. Do not use real keys, and do
    not rely on a verdict.

A release has two kinds of download, built from the same engine at the same
version:

- **the desktop app**, `m-of-n Wallet.app`, for macOS (W-7 #179, DL-0050), as
  a disk image (DMG) — start here if you want a window;
- **`mofn`**, the command line, with `mofn run` as a terminal app — one file per
  OS (#127, DL-0043).

Each has its own Python and PyNaCl inside. Nothing else needs installing, and
you do not need a clone of this repository (PLAN-0004 §9). Both use the same
wallet folders: a wallet made in one opens in the other.

## 1. Download

The releases are pre-releases tagged `wallet-vX.Y.Z`:
**[all wallet releases](https://github.com/m-of-n/mofn/releases?q=wallet-v&expanded=true)**.
(`/releases/latest` skips pre-releases, so this page does not link to it.)

From one release, download the file for your machine and `SHA256SUMS` into
one folder.

| file | for |
|---|---|
| `mofn-wallet-X.Y.Z-macos-arm64.dmg` | **the desktop app**, macOS 13 or later on Apple silicon: a disk image with the app and an Applications shortcut |
| `mofn-wallet-X.Y.Z-macos-arm64.zip` | the same app, zipped |
| `mofn-X.Y.Z-macos-arm64` | the CLI, macOS on Apple silicon |
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
gh attestation verify mofn-wallet-X.Y.Z-macos-arm64.dmg -R m-of-n/mofn
```

The checksum and the provenance are of the file as published, so check the
DMG (or zip) *before* you open it. If the app is also notarized (§3), macOS
checks Apple's side as well; that is a separate check, not a replacement.

Both checks say where the file came from. Neither is an m-of-n statement: a
release that carries an m-of-n statement over its own digest, checked by
`mofn` itself, is #32, and waits on DEC-004 and DEC-005.

## 3. Run it

### The desktop app

Open the **DMG** (double-click it), then drag **m-of-n Wallet** onto the
**Applications** shortcut in the same window, and eject the disk. Start the
app from Applications. (The `.zip` holds the same app: unzip it with a
double-click or `ditto -x -k mofn-wallet-X.Y.Z-macos-arm64.zip .`, and move
the app to Applications.)

Each release's notes say whether its app is **signed with an Apple Developer
ID and notarized**:

- **Notarized:** it opens with no warning on first launch (macOS may say it
  was downloaded from the internet and ask you to confirm).
- **Not notarized** (a build made without the signing secrets, or one that
  is signed but not notarized): macOS says it cannot verify the developer and
  will not open it. Do one of these, once:

  - open it, then **System Settings → Privacy & Security**, and at the bottom
    **Open Anyway** (macOS 15 no longer offers Control-click → Open); or
  - remove the quarantine mark the browser added:

    ```sh
    xattr -dr com.apple.quarantine "/Applications/m-of-n Wallet.app"
    ```

To see what a build is: `codesign -dv --verbose=2 "/Applications/m-of-n Wallet.app"`
(an unsigned build shows an ad-hoc signature, `Signature=adhoc`; a signed one
names its *Developer ID Application* authority and team), and
`spctl -a -t exec -vv "/Applications/m-of-n Wallet.app"` (*accepted, source=Notarized
Developer ID* when notarized).

Its first wallet is `~/Projects/wallet/mofn`; the menu at the foot of the
sidebar opens or creates others. To check a download without opening it:
`"m-of-n Wallet.app/Contents/MacOS/mofn-wallet" --self-test`.

### The CLI

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
  `mofn run` opening Learn. The app: the DMG mounted (the app and the
  Applications shortcut are there) and the zip unzipped on a fresh macOS
  runner, then `--self-test` of each (a wallet, a key, TV-4 green with who
  signed, topic, digest and standing; then every page built offscreen). A
  signed build is also checked with `codesign`, and a notarized one with
  `stapler validate` and `spctl`.
- **Signed and notarized** by the same workflow when the repository has the
  Developer ID secrets (`MACOS_CERT_P12_BASE64`, `MACOS_CERT_PASSWORD`,
  `APPLE_TEAM_ID`, and an App Store Connect API key `ASC_KEY_ID`,
  `ASC_ISSUER_ID`, `ASC_KEY_P8` or `APPLE_ID` + `APPLE_APP_PASSWORD`):
  hardened runtime, `prototype/wallet-app/entitlements.plist`, `notarytool`,
  `stapler`. Without them the files are built unsigned, and never for a pull
  request. The certificate is a *Developer ID Application* one, which is not
  the *Apple Distribution* certificate TestFlight uses.
- **Decisions** D1–D5 for the release are on #127 and in
  `design-log/0043-release-builds/`.

## What changed in v0.3.0 — 2026-11-25

- The desktop app is also a DMG (the app and an Applications shortcut): §1,
  §3. The workflow can sign and notarize it (Developer ID, hardened runtime);
  §3 says how to tell, and what to do when it is not notarized.

## What changed in v0.2.0 — 2026-11-17

- The desktop app (W-7 #179, DL-0050): the `.zip` in §1, how to open an app
  that is not notarized in §3, and its smoke test.

## What changed in v0.1.0 — 2026-11-15

- First version: download, the checksum and provenance checks, running it,
  and the macOS quarantine step. macOS arm64 and Linux x86-64 only.
