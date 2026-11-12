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

## 0.4.1 — 2026-11-11

Prototype: DEC-004 and DEC-005 are open; do not use real keys.

Verdict wording only (mofn#157, SPEC-0004 0.5.0 §10.4, DL-0035). No line
result, answer or exit code changes.

- When no verified attestation is about your copy of the file (golden ③,
  `tampered`), the statements' sentences are now preceded by "The statements
  handed over are about another file, not yours:". This applies to text output
  and to the `mofn run` screen. JSON gains `sentences_about_your_file`.
- A vacuous acceptance pass now reads "no template is named, so there is none
  to meet".
- Goldens updated: `fixtures/golden/` (tampered, green, unauthorized,
  expired) and `domains/archives/golden/`.

## 0.4.0 — 2026-11-09

Prototype: DEC-004 and DEC-005 are open; do not use real keys.

- `--lang TAG` picks the language of the vocabulary's own words: type and
  value names, meanings, and template sentences, in `make` and `check`, text
  and JSON (mofn#66). Lookup is RFC 4647 §3.4 (`es-MX` finds `es`); a word the
  vocabulary has no translation for is English, else its first language. The
  engine's own words, and every result and exit code, are unchanged. A tag
  not in canonical case (`ES`) is refused, exit 2.
- `domains/archives/`: the second domain (mofn#66, W-2). Vocabulary
  `archives` v1, its definer's statements, an example library record and
  three goldens, run by `tests/test_archives.py` under both codecs. It needed
  no engine change.

## 0.3.0 — 2026-11-09

Prototype: DEC-004 and DEC-005 are open; do not use real keys.

- A **text** attribute (SPEC-0003 §6 base kind 3) is a valid assignment, so a
  statement may carry one beside an enum: TV-26's `locator` (ARCH-0001 §2.3.2,
  mofn#135). Ranges over text are still not supported; trust about a text type
  is refused as before.

## 0.2.1 — 2026-11-07

Prototype: DEC-004 and DEC-005 are open; do not use real keys.

- Follows SPEC-0002 0.6.0: target type 5, the locator, is withdrawn. A
  statement about `[5, …]` is now invalid at V7 `structure` (vector N-11), and
  `{locator: …}` is no longer a target in the review form (mofn#144).

## 0.2.0 — 2026-11-05

Prototype: DEC-004 and DEC-005 are open; do not use real keys.

- `mofn run` opens your wallet as a terminal app: the wallet the commands use
  (`--wallet`, else `$MOFN_WALLET`, else `./wallet`). The tabs are Wallet,
  Keys, Trust, Sign, Check and Learn, and `o` opens a file. With no wallet
  yet, first run asks where to keep it, a name for your key and a passphrase.
- Each form runs the mofn command behind it, through the CLI in process, and
  shows that command on its Runs line as you type. Choices come from the
  wallet and the chosen vocabulary. Engine errors appear under the field they
  are about, and the form keeps what you typed.
- The passphrase goes into a masked field and reaches the engine in process,
  never on a command line or in the environment.
- Learn is the tutorial and runs nothing. Its tables are the README's own
  sections, and its example output is `fixtures/golden/`.
- The example vocabulary ships with mofn: DV-1, Alice's key, her `define`
  statement, her attestation and its file. First run offers to copy them to
  `example/` and to know Alice's key.
- Three commands from `gpg`, each with `--format json`:
  - `key list`: your keys and the keys you know, with fingerprints, and where
    a known key came from;
  - `key export LABEL`: your key-publish statement written again, with no
    passphrase;
  - `hash FILE`: a file's SHA-256 as a statement names it.

  The Keys tab's table is `key list`, it has an Export form, and Open a file
  hashes any file that is not a statement or `.def`.
- The header and the key line stay on screen; only a tab's own content
  scrolls.
- Two new goldens, `statement-changed` and `expired`, for Learn. The four
  earlier ones are unchanged.
- With no terminal, `mofn run` refuses with exit 2.
- The CLI moved into `cli.py`. `mofn` only finds it, and still says in one
  line what to install.
- Requires Textual 8.2.8 for `mofn run`. Every other command runs without it.

## 0.1.0 — 2026-11-04

Prototype: DEC-004 and DEC-005 are open; do not use real keys.

Not tagged: it reached `main` together with 0.2.0, in one PR.

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
