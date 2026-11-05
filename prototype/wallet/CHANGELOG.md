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
