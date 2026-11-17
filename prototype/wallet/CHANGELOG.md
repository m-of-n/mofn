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

## 0.10.0 — 2026-11-17

Prototype: DEC-004 and DEC-005 are open; do not use real keys.

**The desktop wallet** (W-7, mofn#179, DL-0050): a macOS window over this
engine, for people who would rather not use a terminal.

- `mofn-wallet-0.10.0-macos-arm64.zip` holds **m-of-n Wallet.app** (PySide6,
  `prototype/wallet-app/`). It is not notarized: on first launch use *System
  Settings → Privacy & Security → Open Anyway* (APP-0005 §3).
- Identity sidebar (+ New identity), Overview, Keys (import, send yours),
  Trust (roots, with values and delegation depth), Sign, Verify, Show, Learn.
  Verify shows authorization, the five other checks, the subject, who signed,
  and standing as a chain or in words — read from `check --format json`.
- Every action runs the `mofn` command shown in the status bar, in the same
  process, against the same wallet folder the CLI uses. The passphrase is a
  masked field, never on argv or in the environment.
- The engine and the `mofn` CLI are unchanged; 0.9.0 was not released, so its
  notes below are new in this release too.

## 0.9.0 — 2026-11-16

Prototype: DEC-004 and DEC-005 are open; do not use real keys.

Every verdict names who signed, the topic, the subject's digest and standing
(W-5, mofn#69, DL-0049).

- `check --format json` adds `associations`: one entry per attestation and
  attribute the answer describes, with `signed-by` (key, kid, your label, the
  named principal), `topic` (domain, type, value), `subject` (the digest
  signed, yours, whether they match) and `standing` (root → delegation → key,
  or no standing and the §10.3 reason, or not evaluated). Read from the
  reduction's result; it decides nothing. The shape is in the README, *The
  verdict as JSON*, and W-7 (#179) reuses it. Every other key is unchanged.
- `mofn run`'s Check tab prints the four under every verdict.
- The text verdict and `fixtures/golden/*.txt` are unchanged.
- `tests/test_associations.py` with goldens
  `fixtures/golden/associations-*.json`; a pilot test that the Check tab
  shows the four and matches the CLI for green, authorization fail and
  integrity fail.

## 0.8.1 — 2026-11-16

Prototype: DEC-004 and DEC-005 are open; do not use real keys.

The first release you can download (#127 S2, W-6, DL-0043). No engine,
command or output change.

- `release.yml` builds one PyInstaller file each for Linux x86-64 and macOS
  arm64, smoke-tests each on a runner with no checkout, and publishes them as a
  pre-release with `SHA256SUMS` and a build-provenance attestation. Windows is
  built and tested but not published.
- How to download and check a file: APP-0005 *Install the wallet* on Pages;
  the README's Install section points there.

## 0.8.0 — 2026-11-16

Prototype: DEC-004 and DEC-005 are open; do not use real keys.

The engine reduces *k*-of-*n* threshold anchors (T-043, SPEC-0004 §6.4,
DL-0042). Keys only, no nesting.

- `reduce.Threshold(keys, k)` is an anchor's `trusts` in the threshold form
  (SPEC-0004 §4.2). An attribute is covered when *k* distinct members each
  made an attestation a one-key anchor to that member, with the threshold's
  `about`, would cover. Keys that a rotation links count as one member.
- The answer names every member: `ThresholdCovered.members` on a yes, and
  `ThresholdStopped` (`threshold-not-met`) on a no, each with the statement
  used and, where a member did not count, the reason. `check` prints them in
  `because` and in the authorization line.
- One-key anchors are tried first, unchanged. A threshold anchor's
  `may-delegate` is not followed, and a threshold *hop* is not yet reduced:
  members attest directly. Both are T-095, on top of the delegation paths
  of 0.7.0.
- `tests/test_thresholds.py`: E-11…E-19 and the member reasons.

## 0.7.0 — 2026-11-14

Prototype: DEC-004 and DEC-005 are open; do not use real keys.

The engine follows delegation paths (W-3 / mofn#67, T-065, T-041,
SPEC-0004 §6.2–§6.3, §6.5, DL-0041).

- `reduce.evaluate`: a path starts at an anchor and follows trust statements.
  Each hop must be valid at the evaluation time, within the delegator's topic
  and range (and its `may-delegate` ranges), allowed by depth and key lists,
  and must not widen. A hop that fails is kept, and the answer names it:
  `Stopped.link` is the trust statement, `Covered.path` the hops followed.
  **Short expiry is the revocation mechanism**; no revocation is read.
- `delegation: 1` hops are compared by KSA-CBOR bytes, so the same range is
  the same bytes and nothing else passes (T-042 subsumed; DEC-004 stays open).
- `check` feeds handed trust statements to the engine; the authorization line
  shows the chain, or the broken link (*the delegation me → key holder is
  broken: … (not-valid-at-time)*).
- `mofn delegate KEY --as YOU --def … --type … [--values] [--depth] [--valid-days]`
  signs a trust statement; `root add --depth N` lets an anchor delegate.
- `demo/slice.sh` ④–⑥: a chain green, the same chain expired, a widened link.
- E-1…E-7 run on the engine; the test-only walker is gone.

## 0.6.0 — 2026-11-13

Prototype: DEC-004 and DEC-005 are open; do not use real keys.

The engine resolves SDSI names (T-040, SPEC-0004 §5.3, ADR-0008, DL-0040).

- `engine/names.py`: `resolve(name, statements, definitions, at)` returns the
  set of keys, the bindings used and each failing branch (`name-unresolved`,
  `name-foreign`, `name-cycle`, `work-bound`). A binding is an attestation
  under a type of base kind `name`; it needs no anchor. Bindings are dropped
  when out of their window or revoked, and names follow a rotation whose
  successor has its own `key-publish`.
- `reduce.evaluate`: an anchor may trust a name. It is resolved first and
  trusts each resulting key; an unresolved name is reported before the
  coverage reasons. `Coverage.names` lists each resolution.
- `definition.py`: a base-kind-`name` value is valid when it is one label;
  `Definition.is_naming`.
- `tests/test_names.py`: R-1…R-10 and E-8…E-10 from the vectors.
- Not yet: `mofn check` and stored anchors take kids only.

## 0.5.0 — 2026-11-12

Prototype: DEC-004 and DEC-005 are open; do not use real keys.

The verifier reads SDSI name targets (mofn#143, SPEC-0002 0.9.0 §7.2, DL-0039).
It does **not** resolve names yet: that is T-040 (SPEC-0004 §5.3).

- Target type 7, `[7, kid, [+ label]]`, passes V7 as the `this` of an
  `attestation` or a `trust`, and has a human form:
  `{name: {issuer: '0x…', labels: [fred, sam]}}`.
- An empty label list, more than 16 labels, or a label outside
  `[a-z][a-z0-9-]{0,62}` is invalid at V7 (N-12, N-13).
- Definitions may use base kind 12, `name` (SPEC-0003 0.2.0).
- Every existing vector keeps its result.

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
