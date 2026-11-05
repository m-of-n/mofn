---
schema: "design-log/v1"
id: DL-0023
part: produced
date: "2026-11-05"
---

# DL-0023 — produced

Model: Claude Opus 5.5. No primitive was added, and no spec text changed.

This is the state after the issue was updated on 2026-11-05. The first version
(two parties, then `sender/` and `receiver/`, compared with goldens) is
described in `review.md`, with what replaced it and why.

## What changed

| where | what |
|---|---|
| `cli.py` | the body of `mofn`, moved in its own commit with no change in output. `main(argv, passphrase=None)`. The `run` subcommand, with `--check` and `--dir`. The menu lists `run` first, and its first example is `mofn run` |
| `mofn` | only the path setup, the missing-dependency line and `cli.plain_streams()`. It sets up the streams so that an in-process call from the screen never reconfigures the terminal's stdin |
| `engine/unlock.py` | `passphrase(..., given=None)`: a caller in the same process may hand it over. An empty one is still refused |
| `guide/steps.py` | eight steps, 16 actions, as data. Each check names the line it is expected to decide (`decides`), its exit code, and optionally a word that sentence must contain (`reason`) |
| `guide/session.py` | copies Alice's five files into the folder. Runs each action through `cli.main` in that folder, under `redirect_stdout`, with `$MOFN_WALLET` set aside. Compares the first line whose result is `fail` with `decides`, and checks the exit code and `reason`; for an all-pass check, `answer: yes` too. `progress.json` counts the actions done |
| `guide/check.py` | `run --check`: a temporary folder and a fixed passphrase in process, `[ok]`/`[FAILED]` per action; it stops at the first failure |
| `guide/screen.py` | Textual: header with version and bar, step list, page, masked `Input`, keys `enter h r l q`. It lays out the JSON verdict, marks the first line that fails, and asks the question at steps 2 and 3 |
| `fixtures/golden/` | unchanged from `main`. The three goldens the first version added are removed |
| `tests/test_guide.py` | 15 tests |
| `requirements.txt` | `textual==8.2.8`, released 2026-06-30 |
| `ci.yml` | `mofn run --check` in the three-OS matrix |
| `CHANGELOG.md`, `README.md`, `BACKLOG-0001` 0.12.6 | 0.2.0 |

`tests/test_guide.py` covers these points:

- every argv parses, and no action carries `--wallet`;
- no argv, environment variable or file holds the passphrase;
- `$MOFN_WALLET` is set aside and restored;
- every check names a real line (or none, for all pass), and its exit code
  agrees;
- the questions are at steps 2 and 3, each before a check that fails;
- the copied files are the fixtures, byte for byte;
- a wrong expectation is caught;
- progress survives, a reset works, and a resume asks for the passphrase
  before step 7 but not at step 4;
- `run --check`, both in process and from the command line;
- the refusal with no terminal (subprocess, 30 s timeout);
- the missing-Textual message;
- a pilot run of the screen through steps 0–3, with both questions answered.

## The steps

The reader has one wallet, `./wallet` in the guide's folder. The guide copies
in what Alice sent:

- `alice.pub.stmt` (TV-1), her key;
- `dv-1.def` (DV-1) and `alice-define.stmt` (TV-3), her vocabulary and the
  statement that says it is hers;
- `alice.stmt` (TV-4), her attestation;
- `artifact.bin`, the file TV-4 is about.

`C` is `mofn check alice.stmt alice-define.stmt --artifact artifact.bin --def
dv-1.def --at 2026-10-15T00:00:00Z --format json`. TV-4 is valid from
2026-10-06 until 2026-11-01.

| step | runs | expected |
|---|---|---|
| 0 your wallet | `init`, `key gen me -o me.pub.stmt`. The screen then lists the wallet's folders, and the key with its mode and its `kdf` + `cipher` | exit 0 |
| 1 what Alice sent | `show alice.stmt` | exit 0 |
| 2 a key you lack | asks which line fails first, then `C` | authenticity, exit 1 |
| 3 not trusted yet | `key import alice.pub.stmt --label Alice`; asks, then `C` | authorization, exit 1 |
| 4 trust, check again | `root add Alice --as me … --values reproducible,attested`, `root list`, `C`; then `C` without `--at` | all six pass, exit 0; then authorization with `not-valid-at-time`, exit 1 |
| 5 change the file | writes `changed.bin` (first byte `X`), then `C` with `--artifact changed.bin` | integrity, exit 1 |
| 6 change the stmt | writes `changed.stmt` (`alice.stmt`, last bit flipped), then `C` on it | integrity with `V4`, exit 3 |
| 7 sign your own | `make --as me --subject artifact.bin --def dv-1.def --type outcome --value approve -o mine.stmt`, `show mine.stmt` | exit 0 |

**Each expected line was checked by hand** before it was written down, by
running the commands in a scratch folder. Two results worth knowing:

- **Step 2.** Integrity is *not evaluated*, and semantics also fails, because
  Alice's `define` cannot be verified without her key either. Authenticity is
  the first line that fails, and it is the line the step is about.
- **Step 7.** `outcome` / `approve` is accepted by `make`, and its sentence
  reads "me says that for sha-256:48dfc39586b0c4f9, review outcome is
  Approve."

## Verified here (Linux)

- **Tests**: pytest, 251 passed.
- **`run --check`**: exit 0, 8 steps, 16 actions.
- **No terminal**: `mofn run </dev/null` exits 2 at once.
- **Pseudo-terminal**: `script` opens the screen, draws `mofn 0.2.0 ─ run ─
  0/8`, copies Alice's five files and quits on `q`.
- **Headless pass**: a pilot drive through step 3 shows the header
  `3/8 ▓▓▓▓▓░░░░░░░░░`, as in the issue's mock-up.
- **The slice** passes.
- **Goldens**: `git diff origin/main -- prototype/wallet/fixtures/golden` is
  empty.
