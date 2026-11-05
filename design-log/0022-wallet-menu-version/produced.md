---
schema: "design-log/v1"
id: DL-0022
part: produced
date: "2026-11-04"
---

# DL-0022 — produced

Model: Claude Opus 5.5. No primitive was added, and no spec text changed.

## What changed

| where | what |
|---|---|
| `engine/__init__.py` | `__version__ = "0.1.0"`, `FOLLOWS`, `ADRS` and `OPEN`. It imports nothing, so a release job can read the version without PyNaCl |
| `engine/suite.py` | `library()`: `PyNaCl <version>`, for `--version` |
| `mofn` | a bare `mofn` prints the menu and exits 0, the same as `-h` and `--help`. `--version` prints six lines. A missing `nacl` or `yaml` prints one line naming `requirements.txt`, exit 2. stdin, stdout and stderr are UTF-8 with `\n` |
| `engine/store.py` | wallet YAML is written as UTF-8 with `\n` (`O_BINARY` where it exists) and read as UTF-8 |
| `.gitattributes` | `prototype/wallet/fixtures/** -text` |
| `tests/test_menu.py` | 9 tests: menu, help, drift both ways, version, CHANGELOG entry, missing PyNaCl |
| `tests/` | `run_mofn` and the golden reads decode UTF-8; `test_key_permissions` is skipped on Windows, with the reason |
| `ci.yml` | `wallet` runs on `ubuntu-latest`, `macos-latest` and `windows-latest`, `fail-fast: false`; a step runs `--version` and the bare menu; the slice is skipped on Windows |
| `CHANGELOG.md` | new: the conventions and `## 0.1.0 — 2026-11-04` |
| `README.md` (wallet) | Run block, exit codes, a Windows key-mode note; the expired case uses `--at 2099-01-01T00:00:00Z` |
| `BACKLOG-0001` 0.12.5 | W-6 row |

## Output that did not change

- **Command help.** `mofn C -h` was compared with `origin/main` for all ten
  commands and command groups: identical.
- **Command output.** The four goldens are untouched. pytest: 235 passed
  (226 before, plus 9). `demo/slice.sh`: 5 cases under each of 2 codecs.

## Why each change was needed

- **The `.gitattributes` line.** `git ls-files --eol` reports `artifact.bin`
  and the `.stmt.yaml` fixtures as text (`i/lf`). On a Windows runner,
  `actions/checkout` honours `core.autocrlf=true`, so it would write those
  files with CR. That changes `artifact.bin`'s SHA-256, which is printed in
  every golden. It would also break the YAML fixtures' round trip.
- **`_write`.** It opened the file as `os.fdopen(fd, "w")`, which means the
  locale encoding (cp1252 on Windows) and CRLF line ends. A label outside
  cp1252 would raise, and the file bytes would differ by OS.
- **The streams.** On Windows, a piped stdout is cp1252, and the verdict
  prints `…`, `∈` and `—`. Text-mode CRLF would also make every golden
  comparison fail. On Linux and macOS, reconfiguring to UTF-8 and `\n`
  changes no byte, as the unchanged goldens show.
- **The `--at` date.** `make` signs for 30 days from now. So
  `--at 2027-01-01` stops showing expiry for a statement made after
  2026-12-02. The case was run at 2099-01-01: authorization fails with
  `not-valid-at-time`, and the other five lines pass.

## The menu, as printed

```
mofn 0.1.0 (prototype: DEC-004 and DEC-005 are open; do not use real keys)

Syntax: mofn [options] COMMAND [args]
Sign a file, and check what you were handed: who said it, and whether you trust them to say it

Commands:
  init                             create an empty wallet
  key gen LABEL                    create a persona with one key
  ...
  show FILE                        print a statement or definition, decoded

Options:
  -h, --help                       show this menu (same as mofn with no command)
      --version                    show what this mofn is built from
      --wallet DIR                 wallet directory (default: $MOFN_WALLET, else ./wallet)
      --codec NAME                 statement file form: ksa-cbor (default), review-yaml

Examples:
  mofn init                                   make an empty wallet in ./wallet
  ...
Report problems at https://github.com/m-of-n/mofn/issues
```
