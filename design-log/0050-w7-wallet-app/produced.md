---
schema: "design-log/v1"
id: DL-0050
part: produced
date: "2026-11-17"
---

# DL-0050 — produced

## Before code: three mockup rounds (HTML, in the thread)

- **v1** — navy theme; sidebar with the wallet switcher on top; Overview as
  six stat cards with a context switcher; Verify with the five other checks as
  five cards, attribute cards in three columns, and standing as a horizontal
  node graph.
- **v2** — graphite theme; identity first in the sidebar; Verify as rows;
  four standing options (A timeline rows, B breadcrumb pills, C plain
  sentences, D node graph).
- **v3** — Keys, Trust, Sign, Show, Learn; standing as A with a C toggle.
  Approved with one change: the sidebar folds.

## Code — `prototype/wallet-app/`

- **`mofn_app/core.py`** — the only door to the engine, no Qt. Every action
  that changes the wallet, signs or checks runs the `mofn` command it names
  through `cli.main` in this process, via `screens/runner.py` (as `mofn run`
  does): the app's verdict *is* the CLI's, and the status bar can print the
  command. Read-only views open the wallet through `engine.store` (as
  `screens/data.py`). `standing_words()` turns the engine's chain into the
  *In words* sentences — presentation only. `self_test()` for the release.
  No file under `prototype/wallet/engine/` changes.
- **`mofn_app/window.py`** — sidebar: identity and switcher (+ New identity =
  `key gen`, passphrase twice), Wallet (Overview, Keys, Trust), Act (Sign,
  Verify, Show, Learn), wallet switcher (recent folders, open, create), the
  prototype badge; folds to icons. Light / System / Dark. Status bar: the last
  command.
- **`mofn_app/pages/`** — one file per page. Verify renders the JSON as rows:
  authorization (YES/NO), the five checks in one row, subject, signed by,
  standing (`widgets.Chain`: root → delegations → signer, broken link dashed
  red), limit line.
- **Passphrase** — `QLineEdit` in password mode; `.encode()` handed to
  `cli.main(passphrase=)`, field cleared at once; never argv, environment,
  QSettings or status bar (`test_the_passphrase_is_never_on_argv_or_in_the_environment`).
- **`mofn-wallet.spec`** — onedir `BUNDLE` → `m-of-n Wallet.app`, ~76 MB with
  PySide6-Essentials; engine, `cli`, `screens.{runner,data,learn}`, README,
  `screens/learn/`, `fixtures/` at the bundle root; Textual not bundled.
  `--self-test`: engine end to end (TV-4 green with the four attributes), then
  every page built offscreen.
- **Tests** — `tests/test_core.py` (14): the three slice cases equal `mofn`
  run in its own process, `associations` against W-5's goldens; sign → verify
  green; wrong passphrase; passphrase leak; one wallet shared with the CLI.
  `tests/test_ui.py` (17, pytest-qt, offscreen): every page; create a wallet;
  New identity; Sign clears the passphrase; Trust adds a root; Verify shows
  the CLI verdict and all four attributes per slice case; the standing toggle;
  sign → *Verify it*; Keys import; Show; Learn; fold; theme; the badge.

## Release and CI

- **`release.yml`** — the same `wallet-v*` tag: an `app` job on macOS 15
  (tests, build, `ditto` zip, version check), `app-smoke` on a fresh macOS
  runner (unzip, `--self-test`), and the release publishes the zip beside the
  two CLIs under one `SHA256SUMS` (3 lines) with build provenance.
- **`ci.yml`** — `wallet-app` job on macOS: tests and self-test.
- Wallet **0.10.0** (MINOR: the app is added). 0.9.0 was never tagged.

## Documents

- `DECISIONS-0001` 0.8.0: item 28 amended (the window is built, in Python;
  same tag).
- `PLAN-0002` 0.5.0: §5.1 Deployment and UI framework rows.
- `PLAN-0004` 0.6.0: §4 (two UIs, one engine), **§5.1 the desktop window**
  (the layout decided from the mockups), §9 (GUI, outputs table, CI).
- `APP-0005` 0.2.0: the `.zip`, opening an app that is not notarized.
- `BACKLOG-0001` 0.16.0: W-7 row.
