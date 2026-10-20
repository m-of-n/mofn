# prototype/wallet — the wallet engine v0 (mofn#65, W-1)

A runnable `mofn` CLI over a local wallet directory. It **follows SPEC-0002,
SPEC-0003 and SPEC-0004** (ADR-0003) behind the codec, suite and envelope
interfaces, and **claims nothing about DEC-002, DEC-003, DEC-004 or DEC-005**,
which stay open in ARCH-0001. It lives in `prototype/` because `src/` stays
empty until DEC-002 is decided. The design input is #65 and the decisions
posted on it; the design record is `design-log/0014-wallet-engine-v0/`.

## Run

```sh
cd prototype/wallet
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/pytest -q                     # vectors, codecs, engine, CLI goldens
.venv/bin/python mofn --help
```

The green case, two wallets (`demo/slice.sh` is #68):

```sh
M=".venv/bin/python mofn"; F=fixtures
$M --wallet w/issuer init
$M --wallet w/issuer key gen build --controller service          # prompts; writes build.pub.stmt
$M --wallet w/issuer make --as build --subject $F/artifact.bin \
   --def $F/dv-1.def --type build-provenance --value reproducible -o prov.stmt
$M --wallet w/rp init
$M --wallet w/rp key gen rp -o rp.pub.stmt                       # a person: may accept anchors
$M --wallet w/rp key import $F/tv-1-alice.pub.stmt --label "Alice (definer)"
$M --wallet w/rp key import build.pub.stmt --label "release machine"
$M --wallet w/rp root add "release machine" --as rp \
   --def $F/dv-1.def --type build-provenance --values reproducible,attested
$M --wallet w/rp check prov.stmt $F/tv-3-define.stmt --artifact $F/artifact.bin --def $F/dv-1.def
```

Skip `root add` for ② (authorization fail), skip the build `key import` too
for ②b (authenticity fail), flip a byte of the artifact for ③ (integrity
fail). `--codec review-yaml` runs the same slice with the human-review form;
use the `.stmt.yaml` fixtures. `--passphrase-stdin` reads the passphrase from
the first line of stdin, for scripts.

Exit codes: `0` answer yes, `1` answer no, `2` usage or wallet error, `3` a
handed statement was invalid.

## Layout

| file | responsible for |
|---|---|
| `mofn` | arguments, printing, exit codes — nothing else |
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
| `fixtures/` | copies of the published vectors (`sync.py`; never edit by hand) and the goldens |

## Where v0 departs from the documents, and why

| | v0 | why |
|---|---|---|
| integrity line | also checks that a verified attestation is about **your** copy of the artifact | #65-c2 A1; SPEC-0004 §10.4 has no line for it, so golden ③ would pass every line. To be proposed as a SPEC-0004 diff |
| acceptance line | **pass** when no template is named | SPEC-0004 Appendix A. Supersedes "not evaluated" in #65-c2 A1 |
| answer | yes only if all six lines pass | stricter than SPEC-0004 §10.3 (coverage alone); see DL-0014 |
| second codec | the human-review YAML form, with `signed` | C1, still to be confirmed by Paul |
| base kinds | enum only; others are refused, never treated as valid | DV-1 needs only enum |
| delegation, revocation, rotation, thresholds, processes, contexts beyond one | not implemented; the answer says 0 revocations considered | out of scope for #65; #67 |
| key wiping | the seed is zeroed after signing — best effort in Python | the library and interpreter may keep copies |
| strict key rules | libsodium also rejects keys with a torsion component | stricter than SPEC-0002 §6.3; honest keys are unaffected |
