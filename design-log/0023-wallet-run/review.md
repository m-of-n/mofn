---
schema: "design-log/v1"
id: DL-0023
part: review
date: "2026-11-04"
---

# DL-0023 — review

**Human review: pending.** David has not yet read this diff or driven the
screen. Below are what the agent rejected and why; record David's verdict on
each here.

## Rejected by David

- **"Two wallets"** (the first version of step 0). The guide gave each party a
  wallet with `--wallet w/sender` and `--wallet w/receiver`, titled the step
  "two wallets", and the agent explained it as if mofn held two wallets.
  David rejected that, on 2026-11-04: mofn has one wallet, and another party is
  "just mofn opened in a different directory".
  - **What changed.** Step 0 is now "sender and you". Every command is a plain
    `mofn …` run in `sender/` or `receiver/`, each with its own `./wallet`.
    Handed files are read as `../sender/…`. A test fails if any action carries
    `--wallet`.
  - **The goldens did not change**, so the verdicts are the same either way.
    The framing was the defect, not the engine.
  - **A consequence the agent added.** With no `--wallet`, a `$MOFN_WALLET` in
    the reader's shell would point the guide at their real wallet. The session
    sets it aside for each command and restores it, and a test checks both.

## The options #127 §6 already rejected, confirmed

- **curses**: missing on Windows.
- **prompt_toolkit**: the layout would be built by hand.
- **A line-by-line prompt**: no screen.

Textual was taken as the issue says. It was pinned to 8.2.8, the newest
release, which is more than two weeks old. Its own dependencies (rich and
others) are not pinned. That is enough for a prototype; Chip's PyInstaller
build may want a lock file.

## Choices the agent made, and the alternatives it rejected

- **The screen runs `python mofn …` as a subprocess.** Rejected: the passphrase
  would have to cross by `--passphrase-stdin`, a pipe that #127 rules out
  ("reaches the engine in process"). It would also start a Python for each of
  18 commands. Instead `cli.main` takes the passphrase as an argument.
  Nothing else in the CLI changed.
- **A thread or worker for each command.** Rejected: `chdir` and
  `redirect_stdout` are global to the process. A worker could catch Textual's
  own output, or race it. Each command runs on the event loop, and the screen
  pauses for Argon2id (well under a second per key).
- **Rendering the text verdict in the guide.** Rejected as reimplementing.
  The guide reads `check --format json` and lays out its six rows. The golden
  is parsed only for comparison: the six fixed-width rows and `answer:`.
  `run --check` compares those, not the bytes. The byte comparison is still
  `test_cli.py`'s and the slice's, so the two kinds of check cannot drift
  apart without a test failing.
- **The answer to step 2 written into `steps.py`.** Rejected: it would be a
  second source. It is read from the golden as the first line that is not
  `pass`.
- **A wallet in the current directory**, as the README's "Try it" does.
  Rejected: run from a clone, it would land in the repo. The folder is in the
  user cache, or `--dir`.
- **A `TemporaryDirectory` for the screen too.** Rejected: progress must
  survive quitting. `run --check` does use one.
- **Progress counted in steps.** Rejected: a quit in the middle of step 0 would
  leave a wallet that `init` refuses to overwrite. Progress counts actions, so
  a resume continues exactly where it stopped. A resume before `make` asks for
  the passphrase again, because it is never stored.
- **The file edits in steps 4 and 5 shown as shell one-liners.** Rejected: no
  one-liner is the same on bash, PowerShell and cmd. They are said in words,
  "(write changed.bin: … first byte replaced by X)", and run by the guide.
- **Running the review-yaml codec in the guide.** Rejected for v0: one codec
  keeps the commands short. The new goldens are the same under both codecs,
  and `test_cli.py` tests both.
- **`q`, `h`, `r` and `l` while the field is focused.** Rejected as typing:
  while a field is open, those letters go into the field, because a
  passphrase may contain them.

## Not verified

- **Windows and macOS**: nothing was pushed, so neither the screen nor
  `run --check` has run there.
- **A person at the keyboard**: nobody has driven the full seven steps. The
  pilot test drives steps 0–2, and `run --check` covers all seven without a
  screen.
- **PyInstaller**: the screen reads `fixtures/` next to `guide/`. A one-file
  build must include `fixtures/{artifact.bin,dv-1.def,tv-1-alice.pub.stmt,
  tv-3-define.stmt}` and `fixtures/golden/`. That is Chip's to add to the build
  spec.
