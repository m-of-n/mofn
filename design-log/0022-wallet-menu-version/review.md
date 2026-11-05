---
schema: "design-log/v1"
id: DL-0022
part: review
date: "2026-11-04"
---

# DL-0022 — review

**Human review: pending.** David chose the scope and the hand-off (commit
locally, no push). He has not yet read the diff. Below are what the
agent rejected and why. Each item is open to David's reversal; record his
verdict on each here, accepted or rejected, with the reason.

## Departures from the issue

- **Rejected by David: two PRs.** The agent's question said "Both, as two
  PRs", meaning a stacked PR for each release. David took "two PRs" to mean
  his and Chip's. He rejected the stack once he saw it: "I though two PRs mean
  my PR and chip's PR". So his half is one branch, `feat/w6-tui`.
  - *What it costs.* `main` squash-merges, so it never holds a commit where
    `__version__` is `0.1.0`. `release.yml` requires the tag to equal
    `__version__`, so `wallet-v0.1.0` cannot be cut from `main`. #127's
    acceptance asks for both pre-releases.
  - *What is kept.* The `0.1.0` entry stays in `CHANGELOG.md`, as the record
    of what the first half added. The first tag is `wallet-v0.2.0`.
  - *Still open, for David and Chip:* drop the `wallet-v0.1.0` line from
    #127's acceptance, or tag 0.1.0 another way.
  - *The agent's own error.* The question gave both options short labels that
    did not say whose PRs they were. It should have named the branches.

- **No `run` row and no `mofn run` example in the 0.1.0 menu**: moot. The
  agent left them out because `run` arrived only in 0.2.0. David's half is one
  PR, so `run` exists whenever the menu does, and the menu now carries the
  issue's own wording: `open the wallet as a terminal app (start here)` and
  `mofn run  use your wallet through forms`. A test still runs `-h` on each
  command the menu lists, so no row can get ahead of the parser.
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

## The `gpg` commands, 2026-11-05: three added, the rest mapped or left out

The issue gives the table; the reasons are restated here as the record.

| `gpg` | in mofn | why |
|---|---|---|
| `-k`, `-K`, `--fingerprint` | **added: `key list`** | Paul asked for key listing |
| `--export` | **added: `key export`** | sending your key again after the first time |
| `--print-md` | **added: `hash`** | comparing a file by reading its hash aloud |
| `--detach-sign`, `-s`, `-u` | `make --as` | a statement is always separate from its file |
| `--verify` | `check` | |
| `--generate-key` and its variants | `key gen`, or first run | |
| `--import` | `key import` | |
| `--lsign-key` | `root add` | a local, unexported decision is an anchor |
| `--edit-key` | the Keys and Trust screens | |
| `-o`, `--armor` | `-o`; `--codec review-yaml` | the text form |
| `-e`, `-d`, `-c`, `-r` | **left out** | mofn says who said what; it does not keep secrets |
| `--clear-sign` | **left out** | a statement names a file by hash and does not carry it |
| `--sign-key`, `--quick-sign-key` | **left out** | vouching for a key is delegation (W-3, #67) or naming |
| `--update-trustdb`, `--tofu-policy` | **left out** | ownertrust; anchors replace it (R-0002 §7.3) |
| `--generate-revocation`, `--quick-revoke-*` | **left out** | short expiry is the revocation mechanism (W-3) |
| `--send-keys`, `--receive-keys`, `--search-keys`, `--refresh-keys`, `--auto-key-locate` | **left out** | no network (#65) |
| `--card-status`, `--edit-card`, `--change-pin` | **left out** | hardware keys are out of scope (PLAN-0004 §6.1) |
| `--delete-keys`, `--change-passphrase`, `--quick-set-expire` | **left out** | key management is out of scope (PLAN-0002 §4.3) |
| `--auto-key-import` | **left out** | authenticity passes only for a key you already hold |
| `--quick-add-uid`, `--group` | **left out** | a mofn key has no user IDs; its name is your own label |

The agent's own choices in building them, and what it rejected:

- **`key export` exports only your own keys.** Of a statement you import,
  the wallet keeps the key and the statement's digest, not the statement
  (README, "What the wallet keeps"). *Rejected:* building a new key-publish
  statement around a known key's public key. That would mean signing in
  someone else's name, and only they can.
- **`key export` writes the stored statement.** *Rejected:* signing a fresh
  key-publish, which would need the passphrase; the issue says it asks for
  none.
- **`key export` writes to `LABEL.pub{suffix}`** unless `-o` says otherwise,
  and overwrites, exactly as `key gen` does. *Rejected:* a different rule for
  the same file.
- **`hash` prints all 64 hex digits.** *Rejected:* the 16-digit form verdict
  sentences use, which is too short to compare a file by. The README and
  Learn say the sentence shows the first 16.
- **`hash` takes one file**, as the issue writes it. *Rejected:* a
  multi-file form like `sha256sum`.
- **Open a file picks `show` or `hash` by suffix** (`.stmt`, `.stmt.yaml`,
  `.def`). *Rejected:* trying `show` and falling back to `hash` on an error,
  which would hide a real decode error in a damaged statement.
- **The Keys table runs `key list --format json` on every reload.** It is
  read-only, so the Learn test lets it run at start-up and refuses any
  command only once Learn is open. *Rejected:* filling the table from the
  wallet directly, which would leave `key list` unused by the screen it
  belongs to (#127 §2 names it).

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
