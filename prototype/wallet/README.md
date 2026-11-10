# prototype/wallet — the wallet engine v0 (mofn#65, W-1)

A runnable `mofn` CLI over a local wallet directory. It **follows SPEC-0002,
SPEC-0003 and SPEC-0004** (ADR-0003) behind the codec, suite and envelope
interfaces, with the encoding DEC-002 chose (ADR-0004, KSA-CBOR) and the key
id DEC-003 chose (ADR-0005, `kid` = SHA-256 of the public key). It **claims
nothing about DEC-004 or DEC-005**, which stay open in ARCH-0001, so it lives
in `prototype/` and `src/` stays empty. The design input is #65 and the
decisions posted on it; the design record is `design-log/0016-wallet-engine-v0/`.

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

The last line of every result is the limit of what this proves: who said it
and whether they were entitled to say it, not that it is true.

### A second domain

`domains/archives/` runs the same commands over a different vocabulary:
statements about a library record, and an ingestion agent that is trusted to
say *summarized* but not *reviewed*. Its README has the run.

## Reading the files

`mofn show FILE` decodes a file for reading; it does not verify (`check`
does). `mofn root list [--context NAME]` prints your anchors in words.

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
| `engine/reduce.py` | coverage over one context's anchors |
| `engine/check.py`, `render.py` | the six-line verdict, text and JSON |
| `engine/store.py`, `unlock.py` | the wallet directory, key store, anchors, passphrase |
| `domains/archives/` | the second domain (mofn#66): the archives vocabulary, its author's statements, an example library record, goldens. No engine code knows it exists |
| `fixtures/` | copies of the published vectors (`sync.py`; never edit by hand) and the goldens, which are `check` outputs pinned by `test_cli.py` |

## Where v0 departs from the documents, and why

| | v0 | why |
|---|---|---|
| integrity line | also checks that a verified attestation is about **your** copy of the artifact | A1 (DL-0020); proposed in SPEC-0004 0.2.0, pending sponsor review |
| acceptance line | **pass** when no template is named | SPEC-0004 Appendix A; A1 as decided in DL-0020 |
| answer | yes only if all six lines pass | stricter than SPEC-0004 §10.3 (coverage alone); kept for v0, see DL-0020 |
| second codec | the human-review YAML form, with `signed` | C1 (DL-0020) |
| base kinds | enum only; others are refused, never treated as valid | DV-1 needs only enum |
| definitions | one per `check` (`--def FILE`); `imports` are not obtained | The vectors' two vocabularies, DV-1 and DV-2, import nothing. SPEC-0003 §4.3 requires every import |
| held statements | statements and definitions you are given are not kept (see above) | ARCH-0003 §3.8 keeps them, marked made, received or accepted |
| delegation, revocation, rotation, thresholds, processes, contexts beyond one | not implemented; the answer says 0 revocations considered | out of scope for #65; #67 |
| key wiping | the seed is zeroed after signing — best effort in Python | the library and interpreter may keep copies |
| strict key rules | libsodium also rejects keys with a torsion component | C4 (DL-0020); stricter than SPEC-0002 0.2.0, matches §6.3 as proposed in 0.4.0 |
