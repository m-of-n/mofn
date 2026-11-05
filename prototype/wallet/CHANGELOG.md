# mofn changelog

The wallet engine and its `mofn` command line, `prototype/wallet/` (#65, #127).

- **Versions** follow semver under APP-0001's `version_policy`: MINOR is a
  command or behaviour added. `0.x` promises no stability.
- **The single source** of the version is `__version__` in
  `engine/__init__.py`. `mofn --version` prints it.
- **Tags** are `wallet-vX.Y.Z`. The prefix keeps them apart from the version
  fields of the documents.
- **One `## X.Y.Z — YYYY-MM-DD` heading per release.** The section under it is
  that release's notes, and `release.yml` reads it from there. Do not change
  this heading form without telling whoever owns `release.yml`.

Every release is a prototype: DEC-004 and DEC-005 are open; do not use real
keys.

## 0.2.0 — 2026-11-04

Prototype: DEC-004 and DEC-005 are open; do not use real keys.

- `mofn run` opens a guided screen with seven steps over the README's cases:
  the sender and you, sign a file, not trusted yet, trust and check again,
  change the file, change the statement, vocabulary and expiry. mofn keeps one
  wallet per folder, so the sender is mofn in `sender/` and you are
  `receiver/`. Every command is a plain `mofn …` in one of them, shown before
  it runs. It all lives in its own folder in the user cache, or `--dir DIR`,
  and `$MOFN_WALLET` is set aside, so it never touches a real wallet.
  Progress survives quitting.
- The passphrase goes into a masked field and reaches the engine in process,
  never on a command line or in the environment.
- `mofn run --check` runs every step without a screen and compares each check
  with its golden. With no terminal, `mofn run` refuses with exit 2.
- Three new goldens: `statement-changed`, `vocabulary-unsigned` and
  `expired`. The four earlier ones are unchanged.
- The CLI moved into `cli.py`. `mofn` only finds it, and still says in one
  line what to install.
- Requires Textual 8.2.8 for the screen. `run --check` and every other
  command run without it.

## 0.1.0 — 2026-11-04

Prototype: DEC-004 and DEC-005 are open; do not use real keys.

The engine as #122 and #125 merged it (W-1), plus a way in:

- `init`, `key gen`, `key import`, `root add`, `root list`, `make`, `check`
  and `show`, over a local wallet directory (ARCH-0003 §9). The encoding is
  KSA-CBOR (ADR-0004), with the human-review YAML form as a second codec.
  Suite 1 runs over PyNaCl. Checks V1–V9 run, then coverage over one
  context's anchors, and `check` prints the six-line verdict.
- A bare `mofn` prints the same menu as `mofn -h` and exits 0. Before this it
  exited 2 with an argparse error. Each command keeps its own `-h`, and every
  command's output is unchanged.
- `mofn --version` says what this mofn is built from: the documents it
  follows, the decisions still open, the codecs, the suite and its library,
  and the wallet in use.
- Running from source without PyNaCl or PyYAML prints one line saying what to
  install, not a traceback. Exit 2.
- Output is UTF-8 with `\n` line ends on every OS, and so are the wallet's
  YAML files. The goldens are therefore the same bytes on Windows.
