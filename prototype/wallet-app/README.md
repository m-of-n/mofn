# m-of-n Wallet — the desktop app

> **Prototype. DEC-004 and DEC-005 are open; do not use real keys.** The tag
> language and the export envelope are undecided, so every statement this app
> writes may stop verifying when they are decided.

A macOS window over the same engine as the `mofn` command line
(`prototype/wallet/`). It signs a statement about a file, and checks the
statements you were handed: who said it, whether you trust them to say it, and
why. It runs locally, with no server and no network (W-7, mofn#179).

The app and the CLI are one wallet and one engine. Every action runs the `mofn`
command it shows in the status bar, in the same process (as `mofn run` does),
so a verdict in the window is the verdict `mofn check` prints, and a wallet made
in one opens in the other: `mofn --wallet ~/Projects/wallet/mofn …`.

## Install

Download `mofn-wallet-X.Y.Z-macos-arm64.zip` from a
[`wallet-v*` pre-release](https://github.com/m-of-n/mofn/releases?q=wallet-v&expanded=true),
check it against `SHA256SUMS` and its build provenance, unzip it, and move
**m-of-n Wallet.app** to Applications. Steps:
[APP-0005 *Install the wallet*](https://m-of-n.github.io/mofn/project/APP-0005-install-wallet/).

The app is **not signed with an Apple Developer ID and not notarized**, so
macOS blocks it on first launch ("Apple could not verify…"). Either:

- open it once, then **System Settings → Privacy & Security → Open Anyway**; or
- remove the download's quarantine mark in Terminal:

  ```sh
  xattr -dr com.apple.quarantine "/Applications/m-of-n Wallet.app"
  ```

Apple Silicon (arm64) only. macOS 13 or later.

## Use

| Page | What it does | Command |
|---|---|---|
| Identity (sidebar) | your identity; switch, or **+ New identity** (name, kind, passphrase twice) | `mofn key gen` |
| Overview | what the wallet holds | — |
| Personas | every persona this wallet is and knows: its identity key, the controller kind it claims, and the tags it received — each with its six-line verdict | `mofn key gen / key list`, `mofn check --subject-key … --as …` |
| Keys | the keys you hold and know; import a key someone sent you; send yours | `mofn key list / import / export` |
| Trust | the roots you trust; trust a key about one kind of claim | `mofn root add / list` |
| Communities | the contexts (SPEC-0004 §4.1) the active persona relies in — this app calls them communities — their anchors, and the members derived from them | `mofn root list --as` |
| Sign | sign one statement about one file, as your identity | `mofn make` |
| Verify | the verdict: authorization, the five other checks, the subject, the signer, standing — computed **as the active persona** | `mofn check --as … --format json` |
| Show | decode a statement or vocabulary; hash any file | `mofn show`, `mofn hash` |
| Learn | the six pages `mofn run` ships | — |

The first wallet is `~/Projects/wallet/mofn` (or `$MOFN_WALLET`). The wallet
menu at the foot of the sidebar opens or creates others. The sidebar folds to
icons with the button at the top left; the theme is Light, System or Dark.

**Personas and communities.** One wallet holds several personas, each with its
own identity key: two personas are unlinkable only if they share no key and no
statement links them (SPEC-0001 §3.1), so *+ New identity* makes a whole new
key. Switching the active persona in the sidebar changes the key that signs
**and** the anchors that decide a verdict — `check --as` uses only that
persona's. A **community** is this app's word for a SPEC-0004 **context**: a
wallet-local scope with its own trust anchors. It is not a term in the
specification, and the page says so. A context has no roster, so its members
are *derived* from the anchors you accepted in it, never declared.

A **tag** a persona received is a statement whose subject is its identity key
(`this = [1, kid]`). The engine gained `make/check --subject-key` for W-8;
`prototype/wallet/CHANGELOG.md` 0.11.0 has the detail.

**The passphrase** is typed into a masked field, handed to the engine as bytes
in this process, and the field is cleared at once. It is never a command-line
argument, an environment variable, a setting, or in the status bar.

## Run from a checkout

```sh
cd prototype/wallet-app
python -m pip install -r requirements.txt
./mofn-wallet                 # the window
./mofn-wallet --self-test     # engine and window, no screen needed
```

Tests (`pytest-qt`, headless):

```sh
python -m pip install -r requirements-test.txt
QT_QPA_PLATFORM=offscreen pytest -q
```

Build the `.app` (what `release.yml` runs on macOS):

```sh
python -m pip install -r requirements-release.txt
pyinstaller --clean --noconfirm mofn-wallet.spec    # dist/m-of-n Wallet.app
```

## Layout

| | |
|---|---|
| `mofn_app/core.py` | the only door to the engine; no Qt |
| `mofn_app/window.py` | sidebar, identity and wallet switchers, status bar |
| `mofn_app/pages/` | one file per page |
| `mofn_app/verdict.py` | one renderer for the CLI's verdict JSON, shared by Verify and Personas |
| `mofn_app/widgets.py` | cards, rows, file field, toggle, the Standing timeline |
| `mofn_app/theme.py` | graphite dark and light tokens, the stylesheet, icons |
| `tests/` | `test_core.py` (app = CLI), `test_personas.py` (W-8, by acceptance box), `test_ui.py` (the window) |

It reimplements no cryptography, encoding or reduction. Decisions:
`DECISIONS-0001` item 28 (amended 2026-11-17), `PLAN-0004` §4–§5, `DL-0050`;
several personas, received tags and communities are W-8 (#180, `DL-0054`).
