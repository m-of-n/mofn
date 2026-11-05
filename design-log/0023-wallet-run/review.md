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

## Rejected by David, 2026-11-05: the executing tutorial

- **What was rejected.** `mofn run` as a guide that ran its own commands: the
  eight steps, each a fixed command run in a throwaway folder, with
  `run --check`. David: "current mofn is like a pure tutorial, I think that's
  a good stuff but not I really expect … mofn should use blocks, questions,
  etc to guide user to use the wallet … original tutorial is great to keep,
  but don't execute command".
- **Why.** Watching mofn run its own commands teaches what they do, but
  nobody gets their own wallet out of it. The user should be guided through
  using *their* wallet: choosing, filling in, and deciding.
- **Withdrawn:**
  - `guide/` (`steps.py`, `session.py`, `check.py`, `screen.py`) and
    `tests/test_guide.py`;
  - `run --check` and its CI step;
  - `run --dir`, the folder in the user cache, and `progress.json`.
- **Kept:**
  - `cli.main(argv, passphrase=)` and `unlock.passphrase(given=)`;
  - the in-process runner, now `screens/runner.py`;
  - `shown()`;
  - the guide's prose, now in the Learn pages.
- **Reversed:** "withdrawn: the three goldens". `statement-changed` and
  `expired` come back as new files, because Learn shows those cases from
  goldens (David's choice). `vocabulary-unsigned` stays out: Learn does not
  list it.

## Choices the agent made for the terminal app, and what it rejected

- **Learn reads, at load time, the README sections it explains** ("What the
  six lines mean", "The cases", "What the wallet keeps") **and the golden
  files.** *Rejected:* copying the text into Learn, which would be two
  explanations that drift. A test checks each section and each golden
  appears, and that Learn imports neither `cli` nor `runner`.
- **The example vocabulary is copied into `example/`, next to the wallet.**
  *Rejected:* pointing the forms at the bundled files where they sit. In a
  one-file build that is a temporary folder, so the *Runs* line would name a
  path that is gone after mofn exits. *Rejected:* copying them into the
  wallet directory, whose layout is ARCH-0003's.
- **Check adds `alice-define.stmt` by itself** when the vocabulary is DV-1,
  and lists it as "(added: who published the vocabulary)". *Rejected:*
  leaving the user to know that semantics needs it.
- **Claims and values are dropdowns**, filled from the vocabulary; *rejected:*
  a free-text field the engine would refuse. **Keys are dropdowns** filled
  from the wallet. "As which of yours" offers only a person or organisation,
  as `root add` requires. A sole key of your own is preselected; *whose key*
  never is, because trusting a key must be a choice.
- **Where an error goes.** It goes under the field whose value appears in the
  message. Otherwise it goes under the form's main field (the file, for
  import and open), or else under *Runs*. *Rejected:* a per-message table,
  which the engine's wording would outgrow.
- **Commands run on the event loop**, through `cli.main` with
  `redirect_stdout`. *Rejected:* a worker thread, because `redirect_stdout`
  is global to the process.
- **`q` does nothing while a field has focus**, because a passphrase or a
  label may contain it. `ctrl+q` always quits, and `escape` leaves first run
  without making anything.

## History: the guided screen this replaced

The sections below record the eight-step guide, which the section above
withdrew. They are kept because they are the record of what was tried.

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

## Changed by the updated issue, 2026-11-05

The sender/receiver form above was itself replaced when David rewrote #127 §2.
The guide no longer plays a second party: the reader has one wallet, and
Alice's published fixtures stand for everything someone else sent.

- **Withdrawn: the `sender/` and `receiver/` folders**, and the sender's own
  key, statement and `prov.stmt`. There is no second wallet to make, so
  nothing in the guide signs on anyone else's behalf. The step that does sign,
  7, signs as you.
- **Withdrawn: the three goldens** `statement-changed`, `vocabulary-unsigned`
  and `expired`, with their `test_cli.py` cases. They existed only for the
  guide, and the issue says the check goldens stay unchanged.
  `fixtures/golden/` is now byte-identical to `main`.
- **Withdrawn: comparing the guide with goldens.** The goldens use the
  slice's names (`release machine`, `prov.stmt`); the guide's checks are about
  Alice's files and run at a fixed date, so its output cannot match those
  bytes. Each check instead names the line it is expected to decide, its exit
  code, and for steps 4 and 6 a word the sentence must contain. Byte
  comparison stays with `test_cli.py` and the slice, which are unchanged.
- **Reversed: "the answer to step 2 written into `steps.py`"**, rejected
  below in the first version. The issue now asks for exactly that: "the
  deciding line each step expects is written next to the step". It is still a
  single source, the step.
- **Kept from David's change:** plain `mofn …` commands with no `--wallet`,
  `$MOFN_WALLET` set aside, and its test.

Three choices the agent made under the update:

- **"Deciding" is the first line whose result is `fail`**, not the first line
  that is not `pass`. In step 2, integrity is *not evaluated*, because there is
  no verified attestation to compare the file with. The line that fails, and
  that the step is about, is authenticity. The screen's ▶ mark follows the
  same rule.
- **The question at steps 2 and 3**, as David chose. Each has one deciding
  line: authenticity (the key is not yours) and authorization (the key is
  yours, but not trusted). Together they teach the difference.
- **Step 7 uses `outcome` / `approve`**, DV-1's reviewer type, because a
  person reviewing a file is what the reader would sign. Rejected: re-using
  `build-provenance`, which is a build machine's claim.

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
  The guide reads `check --format json` and lays out its six rows.
- **The answer to step 2 written into `steps.py`.** Rejected in the first
  version as a second source, next to the goldens. *Reversed on 2026-11-05*;
  see above.
- **A wallet in the current directory**, as the README's "Try it" does.
  Rejected: run from a clone, it would land in the repo. The folder is in the
  user cache, or `--dir`.
- **A `TemporaryDirectory` for the screen too.** Rejected: progress must
  survive quitting. `run --check` does use one.
- **Progress counted in steps.** Rejected: a quit in the middle of step 0 would
  leave a wallet that `init` refuses to overwrite. Progress counts actions, so
  a resume continues exactly where it stopped. A resume before `make` asks for
  the passphrase again, because it is never stored.
- **The file edits in steps 5 and 6 shown as shell one-liners.** Rejected: no
  one-liner is the same on bash, PowerShell and cmd. They are said in words,
  "(write changed.bin: … first byte replaced by X)", and run by the guide.
- **Running the review-yaml codec in the guide.** Rejected for v0: one codec
  keeps the commands short. `test_cli.py` and the slice test both codecs.
- **`q`, `h`, `r` and `l` while the field is focused.** Rejected as typing:
  while a field is open, those letters go into the field, because a
  passphrase may contain them.

## Not verified

- **Windows and macOS**: nothing was pushed, so neither the screen nor
  `run --check` has run there.
- **A person at the keyboard**: nobody has driven all eight steps. The
  pilot test drives steps 0–3, and `run --check` covers all eight without a
  screen.
- **PyInstaller**: the screen reads `fixtures/` next to `guide/`. A one-file
  build must include `fixtures/{artifact.bin,dv-1.def,tv-1-alice.pub.stmt,
  tv-3-define.stmt,tv-4-attestation.stmt}`. The guide no longer reads
  `fixtures/golden/`. That is Chip's to add to the build spec.
