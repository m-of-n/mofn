---
schema: "design-log/v1"
id: DL-0023
part: produced
date: "2026-11-04"
---

# DL-0023 — produced

Model: Claude Opus 5.5. No primitive was added, and no spec text changed.

## What changed

| where | what |
|---|---|
| `cli.py` | the body of `mofn`, moved in its own commit with no change in output. `main(argv, passphrase=None)`. The `run` subcommand, with `--check` and `--dir`. The menu lists `run` first, and its first example is `mofn run` |
| `mofn` | only the path setup, the missing-dependency line and `cli.plain_streams()`. It sets up the streams so that an in-process call from the screen never reconfigures the terminal's stdin |
| `engine/unlock.py` | `passphrase(..., given=None)`: a caller in the same process may hand it over. An empty one is still refused |
| `guide/steps.py` | seven steps, 18 actions, as data |
| `guide/session.py` | copies four fixtures into the folder. Runs each action through `cli.main` under `chdir` and `redirect_stdout`. Parses the golden's six rows and its `answer:`, and compares them with `verdict[line]` and `answer` from the JSON and with the exit code. `progress.json` counts the actions done |
| `guide/check.py` | `run --check`: a temporary folder and a fixed passphrase in process, `[ok]`/`[FAILED]` per action; it stops at the first failure |
| `guide/screen.py` | Textual: header with version and bar, step list, page, masked `Input`, keys `enter h r l q`. It lays out the JSON verdict and marks the first line that is not `pass` |
| `fixtures/golden/` | `statement-changed.txt` (exit 3), `vocabulary-unsigned.txt` and `expired.txt` (exit 1) |
| `tests/test_cli.py` | the three new goldens, under both codecs |
| `tests/test_guide.py` | 13 tests |
| `requirements.txt` | `textual==8.2.8`, released 2026-06-30 |
| `ci.yml` | `mofn run --check` in the three-OS matrix |
| `CHANGELOG.md`, `README.md`, `BACKLOG-0001` 0.12.6 | 0.2.0 |

`tests/test_guide.py` covers these points:

- every argv parses;
- no argv, environment variable or file holds the passphrase;
- each golden exists, and the question's answer is read from the golden;
- a wrong golden is caught;
- progress survives, and a reset works;
- `run --check`, both in process and from the command line;
- the refusal with no terminal (subprocess, 30 s timeout);
- the missing-Textual message;
- a pilot run of the screen through steps 0–2.

## The steps

| step | runs | compared with |
|---|---|---|
| 0 two wallets | `init` and `key gen` for the sender and for `me`; import Alice as `Alice (definer)`. The screen then lists each `.key` with its mode and its `kdf` + `cipher` | exit 0 |
| 1 sign a file | `make … -o prov.stmt`, `show prov.stmt`, import the sender as `release machine` | exit 0 |
| 2 not trusted yet | asks which line fails first, then `check` | `unauthorized`, 1; the answer, 4, comes from the golden |
| 3 trust, check again | `root add`, `root list`, `check` | `green`, 0 |
| 4 change the file | writes `changed.bin` (first byte `X`), then `check --artifact changed.bin` | `tampered`, 1 |
| 5 change the stmt | writes `changed.stmt` (last bit flipped), then `check changed.stmt` | `statement-changed`, 3 |
| 6 vocabulary, expiry | `check` without `tv-3-define.stmt`; `check --at 2099-01-01T00:00:00Z` | `vocabulary-unsigned`, 1; `expired`, 1 |

The labels are the goldens' labels, so the comparison needs no substitution.

## The new goldens

Each is the engine's own output, made the way `test_cli.py` makes them. They
were run twice under each codec, and the output was the same in all four runs.
Neither a digest nor a clock time appears in them: `--at` is fixed, and the
artifact is the fixture.

## Verified here (Linux)

- **Tests**: pytest, 254 passed.
- **`run --check`**: exit 0, 18 actions.
- **No terminal**: `mofn run </dev/null` exits 2 at once.
- **Pseudo-terminal**: `script` opens the screen, draws `mofn 0.2.0 ─ run ─
  0/7`, copies the fixtures and quits on `q`.
- **The slice** passes, and the four earlier goldens are byte-identical to
  `origin/main`.
