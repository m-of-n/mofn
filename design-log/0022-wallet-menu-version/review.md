---
schema: "design-log/v1"
id: DL-0022
part: review
date: "2026-11-04"
---

# DL-0022 — review

**Human review: pending.** David chose the scope (two PRs) and the hand-off
(commit locally, no push). He has not yet read the diff. Below are what the
agent rejected and why. Each item is open to David's reversal; record his
verdict on each here, accepted or rejected, with the reason.

## Departures from the issue

- **No `run` row and no `mofn run` example in the 0.1.0 menu.** The mock-up in
  #127 §1 shows them. `run` arrives in 0.2.0 (DL-0023), and a menu that lists
  a command which then fails with `invalid choice` is worse than one row
  missing. The first example is `mofn init` until then. A test runs `-h` on
  each command the menu lists, so a row cannot get ahead of the parser again.
- **The slice is not run on Windows.** The issue says "where bash runs", and
  bash does run on `windows-latest`. But `slice.sh` locks the other roles'
  wallets with `chmod 000`, which NTFS ignores, so a pass there would not show
  what the slice claims. It also looks for `python3`. Making the slice honest
  on Windows is the slice's owner's call (#68), so this PR leaves it alone.

## What of GnuPG was not copied, and why

The shape was copied: one program over a local home directory, a help screen
in Commands / Options / Examples, and a version screen that says what the
program is built from. Rejected:

- **OpenPGP formats and key import.** WP4 is out of scope this semester.
- **"Good signature" as a headline.** R-0002 §7.2: GnuPG's trusted and
  untrusted cases share those words. The six-line verdict, with authorization
  as the deciding line, stays.
- **Ownertrust.** R-0002 §7.3: it answers whether a key may certify names, not
  whether it may say this claim. It is not added to the menu or anywhere else.
- **gpg's `Home:` line taken over word for word.** `Wallet:` prints the wallet
  in use, after `--wallet` and `$MOFN_WALLET`. That is the closest analogue,
  and it uses the project's term.

## Choices the agent made, and the alternatives it rejected

- **argparse's own `action="version"`.** Rejected: it runs while the arguments
  are still being parsed. So it cannot see `--wallet` when that comes later,
  as in `mofn --version --wallet X`, and it puts a fixed string in the parser.
  `--version` is a flag instead, handled after parsing.
- **Keeping `required=True` on the subcommands and catching the error.**
  Rejected: it would turn every usage error into the menu. Instead the
  subcommand is optional. Only "no command at all" prints the menu; `mofn key`
  with no subcommand is still exit 2, as before.
- **The menu built from argparse's help strings.** Rejected: argparse cannot
  lay out gpg's two-column form, and the commands' existing `help=` strings
  are written for per-command help. The menu is a table in `mofn`, and the
  tests check it against the parser in both directions.
- **Letting the menu and `--version` work without PyNaCl.** Rejected for
  0.1.0: the parser's `choices` come from the engine (`CODECS`,
  `CONTROLLERS`), and making those lazy touches every command for little gain.
  Every invocation prints the one line instead. Chip's builds bundle PyNaCl,
  so only someone running from source sees it.
- **Windows ACLs on the key file** (via `icacls` or pywin32). Rejected: it adds
  a dependency or a subprocess to the engine for a prototype. The key is
  encrypted at rest. The README, the test's skip reason and the CHANGELOG
  scope all say so. If David wants it, it is an engine fix for the matrix
  (#127 §4) and belongs in a follow-up.
- **`PYTHONUTF8=1` set in CI instead of reconfiguring the streams.** Rejected:
  it would make CI green while a user's Windows shell still raised on `…`.

## Not verified

- **Windows and macOS.** The matrix has not run, because nothing was pushed.
  The stream, file and `.gitattributes` changes are the agent's reading of
  where Windows fails, not an observed failure. Getpass on a Windows console
  is untested: CI uses `--passphrase-stdin`.
