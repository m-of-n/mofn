# prototype/wallet — the wallet engine v0 (mofn#65, W-1)

A runnable `mofn` CLI over a local wallet directory. It **follows SPEC-0002,
SPEC-0003 and SPEC-0004** (ADR-0003) behind the codec, suite and envelope
interfaces, with the encoding DEC-002 chose (ADR-0004, KSA-CBOR) and the key
id DEC-003 chose (ADR-0005, `kid` = SHA-256 of the public key). It **claims
nothing about DEC-004 or DEC-005**, which stay open in ARCH-0001, so it lives
in `prototype/` and `src/` stays empty. The design input is #65 and the
decisions posted on it; the design record is `design-log/0016-wallet-engine-v0/`.

## Install

> **Prototype.** DEC-004 and DEC-005 are open. Do not use real keys, and do
> not rely on a verdict.

Each pre-release (tags `wallet-vX.Y.Z`,
[releases](https://github.com/m-of-n/mofn/releases?q=wallet-v&expanded=true))
has one file each for macOS arm64 and Linux x86-64, `SHA256SUMS`, and a
build-provenance attestation. Each file is the whole of `mofn`, `mofn run`
included, with its own Python and PyNaCl inside. Windows is built and tested
but not published (#127 D3).
From 0.10.0 each release also holds the **desktop app** for macOS,
`mofn-wallet-X.Y.Z-macos-arm64.zip`: the same engine in a window
(`prototype/wallet-app/README.md`, W-7).

**How to download, check and run one:
[APP-0005 *Install the wallet*](https://m-of-n.github.io/mofn/project/APP-0005-install-wallet/)**
(`project/APP-0005-install-wallet.md`). In short:

```sh
shasum -a 256 --ignore-missing -c SHA256SUMS          # Linux: sha256sum
gh attestation verify mofn-X.Y.Z-macos-arm64 -R m-of-n/mofn
chmod +x mofn-* && ./mofn-X.Y.Z-macos-arm64 --version && ./mofn-X.Y.Z-macos-arm64
```

To build one yourself, as `release.yml` does:

```sh
cd prototype/wallet
python3 -m venv .venv && .venv/bin/pip install -r requirements-release.txt
.venv/bin/pyinstaller --clean --noconfirm mofn.spec     # dist/mofn
```

## Run

```sh
cd prototype/wallet
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/pytest -q                     # vectors, codecs, engine, CLI goldens
.venv/bin/python mofn                   # the menu; the same as mofn -h
.venv/bin/python mofn --version         # what this mofn is built from
```

Each command has its own help: `mofn check -h`. Without PyNaCl or PyYAML,
`mofn` prints one line saying what to install, and exits 2. Changes are in
[`CHANGELOG.md`](CHANGELOG.md); the version lives in `engine/__init__.py`.

`demo/slice.sh`, from the repo root, needs only that venv (or `$MOFN_PYTHON`, or
a `python3` with the requirements). It installs nothing and uses no network and
no keychain. It gives the issuer, the key-holder and the relying party one
wallet each, and compares every verdict with `fixtures/golden/` under both
codecs.

## `mofn run`: the wallet as a terminal app

```sh
.venv/bin/python mofn run               # start here
```

`mofn run` opens **your wallet**, the same one the commands use: `--wallet`,
else `$MOFN_WALLET`, else `./wallet`. You fill in forms, and it runs the mofn
command behind each one.

| tab | you fill in | it runs |
|---|---|---|
| first run | where to keep the wallet, a name for your key, a passphrase, whether to get the example vocabulary | `init`, `key gen`, `key import` (Alice) |
| Wallet | — | — : your keys, the keys you know, your anchors. `o` opens a file (`show`, or `hash` for any file that is not a statement or `.def`) |
| Keys | a name and a kind; or a `.pub.stmt` you were sent and your name for it; which of your keys to send again | `key list` (the table), `key gen`, `key import`, `key export` |
| Trust | whose key, as which of yours, the vocabulary, the claim, the values, the context | `root add` |
| Sign | as which key, the file, the vocabulary, the claim, the value, how long, where to save | `make` |
| Check | the statements you were handed, the file, the vocabulary, the context, the time | `check --format json` |
| Learn | — | **nothing** |

- **Choices come from what you have.** Every key in a list is one your wallet
  holds, and every claim and value is one the chosen vocabulary defines.
- **Every form shows its command** on a *Runs* line, as you type. Running it
  in a shell gives the same result.
- **An engine error appears under the field** it is about, and what you typed
  stays.
- **The passphrase** goes into a masked field and reaches the engine in the
  same process, never on a command line or in the environment.
- **Learn** is the tutorial: what each tab does, what the six lines mean, and
  what each failing case looks like. It runs no command and opens no wallet.
  Its tables are this README's own sections, and its example output is
  `fixtures/golden/`, read when the page opens, so neither can drift.
- With no terminal, `mofn run` refuses with exit 2. `?` opens Learn from any
  tab, and `q` or `ctrl+q` quits.

**The example vocabulary.** First run offers to copy DV-1 into `example/`,
next to your wallet, and to know Alice's key as `Alice (definer)`:

| file | fixture |
|---|---|
| `dv-1.def` | DV-1, a supply-chain vocabulary |
| `alice.pub.stmt` | TV-1, its author Alice's key |
| `alice-define.stmt` | TV-3, the statement that says DV-1 is hers |
| `alice.stmt` | TV-4, her attestation that `artifact.bin` was built reproducibly |
| `artifact.bin` | the file |

With it, a downloaded mofn can sign and check with no clone. Check adds
`alice-define.stmt` to the statements by itself when the vocabulary is DV-1,
because semantics fails without it. Alice's statement was valid from
2026-10-06 until 2026-11-01, so check it `--at 2026-10-15T00:00:00Z`.

## Try it

A sender signs a file, and you, the receiver, check it. Each has their own
wallet, and only the files named below move between them. Run it from a
scratch folder, so nothing lands in the repo.

```sh
M="$PWD/.venv/bin/python $PWD/mofn"; F=$PWD/fixtures     # from prototype/wallet
mkdir -p /tmp/mofn-try && cd /tmp/mofn-try
$M --wallet w/sender init
$M --wallet w/sender key gen sender --controller service          # prompts; writes sender.pub.stmt
$M --wallet w/sender make --as sender --subject $F/artifact.bin \
   --def $F/dv-1.def --type build-provenance --value reproducible -o prov.stmt
$M --wallet w/receiver init
$M --wallet w/receiver key gen me -o me.pub.stmt                  # you: a person, so you may decide whom to trust
$M --wallet w/receiver key import $F/tv-1-alice.pub.stmt --label "Alice (vocabulary author)"
$M --wallet w/receiver key import sender.pub.stmt --label "release machine"
$M --wallet w/receiver root add "release machine" --as me \
   --def $F/dv-1.def --type build-provenance --values reproducible,attested
$M --wallet w/receiver check prov.stmt $F/tv-3-define.stmt --artifact $F/artifact.bin --def $F/dv-1.def
```

`--wallet` can be left out: the wallet is `$MOFN_WALLET`, else `./wallet`.
`--lang es` prints the vocabulary's own words — type and value names, and the
sentence — in Spanish where the definition has them, English otherwise; the
engine's own words stay English.
`--passphrase-stdin` reads the passphrase from the first line of stdin, for
scripts. `--codec review-yaml` runs the same steps with the human-review form;
use the `.stmt.yaml` fixtures.

### The cases

Each is the run above with one thing changed. `check` always prints all six
lines, the answer and the limit line; the table gives the line that decides.

| case | change | deciding line | exit |
|---|---|---|---|
| ① green | none | all six pass, `answer: yes` | 0 |
| ② not trusted | skip `root add` | authorization fail: no anchor trusts the sender about build provenance | 1 |
| ②b key never received | also skip `key import sender.pub.stmt` | authenticity fail: the speaker's key is not in your key store | 1 |
| ③ file changed | check a copy of the file with one byte changed | integrity fail: your file is not the one described | 1 |
| ④ statement changed | flip one bit of `prov.stmt`, or change one word of `prov.stmt.yaml` | integrity fail: invalid at V4 (signature) | 3 |
| vocabulary unsigned | leave out `tv-3-define.stmt` | semantics and authorization fail (unattributed-definition) | 1 |
| expired | add `--at 2099-01-01T00:00:00Z` | authorization fail (not-valid-at-time) | 1 |

In ④ the changed statement is thrown out at once, so authorization and
acceptance are *not evaluated* and no sentence is printed. `root add` for a
key the wallet does not know is refused before anything is checked:
`no persona '…' in this wallet`, exit 2.

Exit codes: `0` answer yes, or done (a bare `mofn` too), `1` answer no, `2`
usage or wallet error, `3` a handed statement was invalid.

### What the six lines mean

| line | passes when | protects you from |
|---|---|---|
| integrity | every statement is well formed and its signature checks, and your file is the one described | a changed statement, a changed file |
| authenticity | you already have every signer's key, and each envelope agrees with its statement | a sender you have never met |
| names | every key is shown by your own name for it, or by its fingerprint | a key that calls itself "Your Bank" |
| authorization | you decided to trust this sender about this kind of claim and this answer | a valid signature by someone with no right to say it |
| acceptance | any template the statement follows is filled in correctly | a statement that breaks its form's rules |
| semantics | the vocabulary is the one named, well formed, and signed by its author | an unsigned or swapped vocabulary |

**When the subject is a key** (`--subject-key`, below) there is no copy of
yours to compare, so integrity reports verification alone and the comparison
clause does not apply — SPEC-0004 §10.4 conditions it on a digest target.
Whether any statement is about that key is then authorization's and
acceptance's question, and they say *not evaluated* when none is.

The last line of every result is the limit of what this proves: who said it
and whether they were entitled to say it, not that it is true.

### Tags a key received

A statement's subject may be a key rather than a file: `this = [1, kid]`
(SPEC-0002 §7.2, target type 1). That is how a tag *given to a persona* is
written, and what the desktop app's Personas page lists (W-8, mofn#180). The
form is not new — TV-13's own note in the published vectors reads
*"attestation about a KEY"*.

```sh
# Carrying on from "Try it": Alice says Bob's key has the name "fred".
BOB=39f713d0a644253f04529421b9f51b9b08979d08295959c4f3990ee617f5139f
$M --wallet w/receiver root add "Alice (vocabulary author)" --as me \
   --def $F/dv-2.def --type name
$M --wallet w/receiver check $F/tv-13-name.stmt $F/tv-12-define-names.stmt \
   --subject-key $BOB --def $F/dv-2.def
```

`--subject-key` takes your label for a key, a kid prefix, or a full 64-digit
kid — the last so a tag given to a key this wallet has not met can still be
checked. `make --subject-key` signs one.

`check --as LABEL` and `root list --as LABEL` use **one owned persona's**
anchors, because a context is a scope in which an owned persona acts and
relies (SPEC-0001 §6.3). Without `--as`, every owned persona's anchors are
used, as before.

### Who signed, topic, digest, standing

Under the six lines, every check shows four things for each verified
attestation it describes (W-5, mofn#69). `mofn run`'s Check tab shows them as
`check --format json` gives them; it works none of them out again.

| | what it is | where it comes from |
|---|---|---|
| who signed | the speaker's key, by your name for it or its fingerprint, and the named principal when an anchor trusts that key through a name | the verified statement's `says`; names from the reduction |
| topic | the vocabulary (domain), the claim (type) and the value | the attribute, and the definition you hold |
| digest | the full digest the statement is about, and your file's when they differ | the statement's `this`, and your copy of the file |
| standing | your root → each delegation → the signing key; or **no standing**, and why | the reduction's own path, or the link that broke |

A statement that did not verify has none of the four: what it says about who
signed it is not yet known to be true. A statement that is not about your file
shows its digest beside yours, and standing *not evaluated*.

### The verdict as JSON

`check --format json` prints one object: `answer`, `at`, `context`,
`subject`, `subject-target` (`"digest"` or `"key"`), `subject-key` (the kid,
or `null`), `because` (the §10.3 trace), `verdict` (the six lines),
`statements`, `sentences`, `sentences_about_your_file`, **`associations`** and
`limit`. `associations` is the stable surface `mofn run` and W-7 (#179)
render: one entry per attestation and attribute the answer describes, in
statement order, and `[]` when no attestation verified. W-7 reads these
names: rename or remove one only with a CHANGELOG line, and tell W-7's owner.

```json
{
  "statement": "<64 hex: the statement digest>",
  "file": "prov.stmt",
  "signed-by": {"key": "release machine", "kid": "<64 hex>", "label": "release machine", "principal": null},
  "topic": {"domain": "supply-chain 1", "definition": "<64 hex>", "type": "build-provenance",
            "type-name": "build provenance", "value": "reproducible", "value-name": "Reproducible"},
  "subject": {"digest": "sha-256:<64 hex>", "yours": "sha-256:<64 hex>", "matches": true},
  "standing": {"result": "standing", "text": "me (root, accepted by me) → key holder",
               "chain": [{"role": "root", "anchor": "local", "accepted-by": "me", "key": "me", "kid": "<64 hex>"},
                         {"role": "delegation", "trust": "<64 hex>", "key": "key holder", "kid": "<64 hex>"}],
               "reason": null, "detail": null}
}
```

| field | values |
|---|---|
| `signed-by.label` | your label for the key, or `null`; `key` falls back to `key:<16 hex>` |
| `signed-by.principal` | `"<whose>'s <name>"` when a name anchor resolved to this key (SPEC-0004 §5.3), else `null` |
| `topic.domain` | `"<name> <version>"` of the definition you hold, or `definition:<16 hex>` when it is not the one named |
| `subject.matches` | `false` is the integrity failure: `digest` is what was signed, `yours` is your file |
| `subject.target` | `"key"` when the ask was `--subject-key`; **absent for a digest ask**, so a reader written for W-5 does not move |
| `subject.key` / `.kid` / `.label` | for a key ask, the subject key in the same words `signed-by` uses; `digest` is then `null` |
| `standing.result` | `standing`, `no-standing` (with `reason`, a §10.3 code, and `detail`), or `not-evaluated` (no statement is about your file, or another statement covered the value) |
| `standing.chain` | the root first, then each delegation hop; the last `key` is the signer. A threshold root adds `threshold: {k, n}`. On a no, the hops followed before the break |
| `standing.broken` | on a no that a delegation caused: `trust` (its digest), `from`, `to` |
| `standing.text` | the line `mofn run` prints, so every renderer says the same thing |

Goldens: `fixtures/golden/associations-{green,unauthorized,tampered}.json`
(`tests/test_associations.py`), and `associations-key-subject.json` for a key
ask (`tests/test_key_subject.py`).

### A second domain

`domains/archives/` runs the same commands over a different vocabulary:
statements about a library record, and an ingestion agent that is trusted to
say *summarized* but not *reviewed*. Its README has the run.

## Reading the files

`mofn show FILE` decodes a file for reading; it does not verify (`check`
does). `mofn root list [--context NAME] [--as LABEL]` prints your anchors in
words; `--as` narrows them to one owned persona's.

**A statement and its envelope** (`mofn show prov.stmt`). The envelope is
what travels: `[suite, says, tbs, sig, ? pub]` (SPEC-0002 §5). The statement
is `tbs` decoded.

| field | what it is |
|---|---|
| `tbs` | the statement itself, as the exact KSA-CBOR bytes that were signed. Not a hash |
| `sig` | the signature over `KSA-STMT-SIG-v1\0 ‖ tbs`, checked before `tbs` is read |
| `suite`, `says` | on the envelope, hints for finding the key; in the statement, the signed values. The two must agree (V6) |
| `pub` | an optional copy of the public key; key-publish statements (`*.pub.stmt`) carry one |
| `kind` | `attestation`, `key-publish`, `define`, … (SPEC-0002 §8) |
| `says` | the speaker's key id, the SHA-256 of their public key |
| `this` | what the statement is about; for an attestation, a file by its SHA-256 |
| `valid` | when it holds; `make` signs for 30 days (`--valid-days N`) |
| `body.has` | what is said: a type, named by definition id and label, and its value |

A statement holds no names, only key ids and hashes. Its digest, the SHA-256
of `tbs`, is how other statements refer to it and the name the wallet stores
it under.

**A definition** (`mofn show dv-1.def`), in the human-review form of
SPEC-0003 Appendix A. Its id is the SHA-256 of its bytes, so the id in
`body.has` pins one exact vocabulary. It is not signed itself: its author's
`define` statement (`tv-3-define.stmt`) names it by that id, and `definer`
inside it is only a claim until that statement verifies. DV-1 has two types,
`build-provenance` (what a build machine says) and `outcome` (a reviewer's
approve / changes / reject, used by review statements; not evaluated in v0),
and one template, `release-attestation`, which gives the sentence.

**An anchor** (`wallet/personas/<you>/trusts/<context>.yaml`, or
`mofn root list`): your trust decision. *In context `default`, I trust key K
to say build-provenance is reproducible or attested, about any file.*

| field | what it means |
|---|---|
| file name | the context it applies in; trust in one context counts for nothing in another. A context name is lowercase letters, digits and `-` |
| `source` | `local`: decided in your wallet, signed by nobody |
| `trusts` | the key trusted, by key id. Authorization passes when it equals the statement's `says` |
| `about` | the type (definition id and label) and the values (`range`) the key may say |
| `accepted by` | which of your own personas decided; it must be a person or an organisation |
| `accepted at` | when you decided; a record, not an expiry |

Anchors are never sent to anyone (SPEC-0004 §4.2).

### Keys and hashes

Three commands come from `gpg`, which #127 takes as the reference for the
shape of the tool. Each prints text, or JSON with `--format json`.

| mofn | like | does |
|---|---|---|
| `mofn key list` | `gpg -k`, `-K`, `--fingerprint` | one row per key: your name for it, yours or known, its kind, its fingerprint, and for a key you imported, the file and the date. Changes nothing |
| `mofn key export LABEL [-o FILE]` | `gpg --export` | writes your key's key-publish statement again, from the copy `key gen` kept in `statements/`. Signs nothing, asks for no passphrase, and refuses a key you only know |
| `mofn hash FILE` | `gpg --print-md SHA256` | `sha-256:<64 hex>  FILE`, the file's SHA-256 as a statement's `this` names it. Verdict sentences print its first 16 digits |

The other `gpg` commands are mapped to mofn's, or left out, in #127 and in
`design-log/0022-wallet-menu-version/review.md`.

## What the wallet keeps

| | kept | how |
|---|---|---|
| your keys | private key encrypted (`keys/<kid>.key`, 0600, in a 0700 folder), public key | `key gen` |
| statements you made, your key-publish included | exact bytes in `statements/<digest>.stmt` | `key gen`, `make` |
| other people's public keys | as *known* personas: public key, your label, where and when it came from | `key import` |
| your trust decisions | `trusts/<context>.yaml` | `root add` |
| definitions | only the one named in a `root add` | `root add` |
| statements you are given, other people's key-publish statements | **not kept**; `key import` records only the digest | — |

So every `check` is given the statements and the definition again; the
wallet remembers keys and decisions, not evidence. Holding received
statements and definitions (ARCH-0003 §3.8) is what multiple definitions and
presentations would build on.

On Windows the 0600 and 0700 modes are not enforced: NTFS has no POSIX mode
bits. There the private key is protected by the encryption at rest (Argon2id
and SecretBox) and by the user profile's ACL. The test of the modes is skipped
on Windows.

## Layout

| file | responsible for |
|---|---|
| `mofn` | finds the engine; one line if PyNaCl or PyYAML is missing |
| `mofn.spec`, `requirements-release.txt` | the one-file PyInstaller build and its pins (`release.yml`) |
| `release/` | the release smoke test: `smoke.sh` and `pty_run.py`, run on a runner with no checkout |
| `cli.py` | arguments, printing, exit codes — nothing else |
| `screens/app.py`, `forms.py`, `picker.py` | `mofn run`: tabs, first run, one form per command, the file and passphrase dialogs |
| `screens/runner.py` | runs a form's argv through `cli.main` in process, and spells it as a shell would |
| `screens/data.py`, `example.py` | the choices, read from the wallet and the vocabulary; the bundled DV-1 |
| `screens/learn.py`, `screens/learn/` | the Learn pages; they run nothing |
| `engine/encoding/ksa_cbor.py` | KSA-CBOR and the validating decoder (SPEC-0002 §4) |
| `engine/encoding/review_yaml.py` | the human-review form (SPEC-0002 §11) |
| `engine/codecs.py` | the two codecs by name |
| `engine/suite.py` | suite 1 over PyNaCl; no curve math |
| `engine/envelope.py` | `[suite, says, tbs, sig, ? pub]` |
| `engine/schema.py` | SPEC-0002 Appendix B as data: V7 and the YAML names |
| `engine/verifier.py` | V1–V9 |
| `engine/statement.py`, `signer.py` | build and sign statements |
| `engine/definition.py` | DefinitionId, conformance, enum values, attribution, templates |
| `engine/reduce.py` | delegation paths (SPEC-0004 §6.2–§6.5: depth, no widening, validity ∩), *k*-of-*n* thresholds (§6.4) and coverage over one context's anchors |
| `engine/names.py` | SDSI name resolution (SPEC-0004 §5.3, ADR-0008) |
| `engine/ksatime.py` | KSA time (SPEC-0002 §4.4) |
| `engine/errors.py` | why a statement or an input was refused (SPEC-0002 §9.1, §12.9) |
| `engine/check.py`, `render.py` | the six-line verdict, text and JSON |
| `engine/store.py`, `unlock.py` | the wallet directory, key store, anchors, passphrase |
| `domains/archives/` | the second domain (mofn#66): the archives vocabulary, its author's statements, an example library record, goldens. No engine code knows it exists |
| `fixtures/` | copies of the published vectors (`sync.py`; never edit by hand) and the goldens, which are `check` outputs pinned by `test_cli.py` |

## Where v0 departs from the documents, and why

| | v0 | why |
|---|---|---|
| integrity line | also checks that a verified attestation is about **your** copy of the artifact | A1 (DL-0020); proposed in SPEC-0004 0.2.0, pending sponsor review |
| acceptance line | **pass** when no template is named, and the sentence says so | SPEC-0004 Appendix A, §10.4 (0.5.0); A1 as decided in DL-0020; mofn#157 |
| sentences about another file | framed as such when no attestation is about **your** copy | SPEC-0004 §10.4 (0.5.0); mofn#157 |
| answer | yes only if all six lines pass | stricter than SPEC-0004 §10.3 (coverage alone); kept for v0, see DL-0020 |
| second codec | the human-review YAML form, with `signed` | C1 (DL-0020) |
| base kinds | enum only; others are refused, never treated as valid | DV-1 needs only enum |
| definitions | one per `check` (`--def FILE`); `imports` are not obtained | The vectors' two vocabularies, DV-1 and DV-2, import nothing. SPEC-0003 §4.3 requires every import |
| held statements | statements and definitions you are given are not kept (see above) | ARCH-0003 §3.8 keeps them, marked made, received or accepted |
| revocation and rotation on paths and thresholds, processes, contexts beyond one | not implemented; the answer says 0 revocations considered. **Short validity is the revocation mechanism** (SPEC-0004 §7.1, §11.3). Revocation and rotation are applied to name bindings only (`names.py`). Delegation paths and *k*-of-*n* thresholds **are** implemented (`reduce.py`) | #67; revocation is a requirement (PLAN-0004 §5.3) |
| key wiping | the seed is zeroed after signing — best effort in Python | the library and interpreter may keep copies |
| strict key rules | libsodium also rejects keys with a torsion component | C4 (DL-0020); stricter than SPEC-0002 0.2.0, matches §6.3 as proposed in 0.4.0 |
