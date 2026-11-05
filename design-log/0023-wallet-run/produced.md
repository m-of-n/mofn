---
schema: "design-log/v1"
id: DL-0023
part: produced
date: "2026-11-05"
---

# DL-0023 — produced

Model: Claude Opus 5.5. No primitive was added, and no spec text changed.

This is the state after the second update of 2026-11-05: `mofn run` is the
wallet as a terminal app. The eight-step guide it replaced, and why, is in
`review.md`.

## What changed

| where | what |
|---|---|
| `screens/runner.py` | `run(argv, passphrase)`: `cli.main` in process under `redirect_stdout/stderr`. `Place`: which wallet is open, and the `--wallet`/`--codec` prefix a shell would need. `shown()` |
| `screens/data.py` | choices, read through the engine: owned and known personas, acceptors (person or organisation), contexts, anchors in words (`cli.anchor_line`), a vocabulary's enum types and values |
| `screens/example.py` | DV-1, TV-1, TV-3, TV-4 and `artifact.bin` from `fixtures/`, copied on request into `example/` next to the wallet |
| `screens/forms.py` | `KeyGen`, `KeyImport`, `Trust`, `Sign`, `Check`, `Show`. Each builds one argv, shows it on its *Runs* line as fields change, runs exactly it, and puts an engine error under the field it names |
| `screens/picker.py` | the file dialog (`DirectoryTree`), and the passphrase dialog: masked, with a confirm field for `key gen` |
| `screens/app.py` | the App and its tabs: Wallet, Keys, Trust, Sign, Check, Learn. First run. `o` opens a file. `?` opens Learn. `ctrl+s` runs the form in focus |
| `screens/learn.py`, `screens/learn/*.md` | six pages. Directives insert README sections and golden files at load time |
| `engine/store.py` | `Wallet.contexts()`, read-only: the names of the `trusts/*.yaml` files |
| `cli.py` | `run` has no options of its own; it opens `--wallet`/`$MOFN_WALLET`/`./wallet`. The menu row and example take the issue's wording. No terminal: `run needs a terminal`, exit 2 |
| `fixtures/golden/` | `statement-changed.txt` (exit 3) and `expired.txt` (exit 1) added. The four earlier ones are byte-identical to `main` |
| `tests/test_cli.py` | the two new goldens, under both codecs |
| `tests/test_screens.py` | 16 tests; replaces `tests/test_guide.py` |
| `guide/`, `run --check`, `run --dir` | removed |
| `ci.yml` | the `run --check` step removed. pytest runs the pilot tests on all three OS |
| `CHANGELOG.md` 0.2.0, `README.md`, `BACKLOG-0001` 0.12.7 | follow |

## What the tests drive

All of them run headless, through `App.run_test()`, on a temporary wallet.

- **First run** makes the wallet, your key and `me.pub.stmt`, and copies the
  example and imports Alice. The commands run are exactly `init`,
  `key gen me -o me.pub.stmt`, and `key import example/alice.pub.stmt
  --label "Alice (definer)"`. Passphrases that differ are refused, and
  nothing is made. `escape` leaves without making anything.
- **Choices**: *whose key* lists only known keys, *as* only acceptors, and
  *claim* and *value* only DV-1's.
- **The *Runs* line is the command that ran**, compared with the argv
  `runner.run` received.
- **Check** shows six lines with ▶ on authorization, the answer and the limit
  line. It adds `alice-define.stmt` by itself.
- **An engine error** appears under the file field, and both fields keep what
  was typed.
- **Open a file** decodes `dv-1.def`.
- **The hand-off**, two people with two wallets in two folders:
  1. David signs `artifact.bin` (`outcome` = `approve`).
  2. Chip imports `david.pub.stmt`, trusts David about `outcome` = `approve`,
     and checks.
  3. Chip gets `answer: yes`.
  4. No argv, environment variable or file holds the passphrase.
- **Learn** runs nothing: with `runner.run` and `cli.main` replaced by a
  function that fails, every page opens, the *Go to* button switches tab,
  and no file changes. Each golden and each README section it cites appears
  in its page. Learn imports no command code.
- **No terminal** gives exit 2 at once. **Without Textual**, one line says
  what to install. **The menu** lists `run` first, in the issue's wording.

## Verified here (Linux)

- **pytest**: 255 passed.
- **The slice**: 5 cases under each of 2 codecs.
- **`mofn run </dev/null`**: exit 2.
- **A pseudo-terminal** (`script`): `mofn run` draws first run and quits on
  `ctrl+q`, leaving the folder empty.
- **Screenshots** of first run, Wallet, Sign, Check and Learn were rendered
  and read. Fields were made one line high after the first look.
