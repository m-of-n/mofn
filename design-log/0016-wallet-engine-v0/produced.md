---
schema: "design-log/v1"
id: DL-0016
part: produced
date: "2026-10-20"
---

# DL-0016 — produced

All in `prototype/wallet/`, plus a `wallet` job in `.github/workflows/ci.yml`.
Model: Claude Opus 5.5. Signing, verification, hashing and key encryption are
PyNaCl (libsodium) and `hashlib`; no primitive is implemented.

## What exists

| part | what it does | evidence |
|---|---|---|
| `encoding/ksa_cbor.py` | KSA-CBOR encoder (from `generate.py`) and single-pass validating decoder (from DL-0007's `rcbor_decode.py`, now rejecting `null`, integers past ±(2^53−1), non-uint/text keys) | TV-1…8 re-encode byte for byte; 26 rejection fixtures; a test that the decoder works with the encoder removed |
| `suite.py` | suite 1 over PyNaCl: strict key check `crypto_core_ed25519_is_valid_point`, verify `crypto_sign_verify_detached` | N-4 rejected at V3, N-5 at V4, unaided |
| `verifier.py` | V1–V9 in order, signature over the raw `tbs` before decoding | TV-1…8 verified; N-1…6 invalid at exactly the step `vectors.json` names |
| `schema.py` | SPEC-0002 Appendix B as one table, used both for V7 and for the YAML codec's names | closed-map rejection (test ⑥) |
| `encoding/review_yaml.py` | the human-review form of SPEC-0002 §11, `signed` included | TV-4's output equals #107's printed example **character for character**; TV-1…8 round-trip binary → YAML → binary identically; 22 lexical rejections |
| `definition.py` | DefinitionId recomputed, SPEC-0003 §9 conformance for what DV-1 uses, enum algebra, `define` attribution, §7.1 template conformance | DV-1 loads; four non-conforming variants fail semantics |
| `reduce.py` | SPEC-0004 §10.2 coverage, one hop, one context, validity at `at` | `no-path`, `not-valid-at-time`, `unattributed-definition`, `template` each tested |
| `render.py`, `check.py` | six lines, the template sentence, the limit line; text and §10.3-shaped JSON | ⑧: TV-4 renders the SPEC-0003 §10.1 sentence exactly |
| `store.py`, `unlock.py`, `mofn` | ARCH-0003 §9 subset, Argon2id + SecretBox at rest, `keys/` 0700, `.key` 0600, `--passphrase-stdin` | permissions and "passphrase never in any output or file" tested |
| `mofn show`, `definition.to_h` | prints a statement as envelope plus decoded statement, and a `.def` in the human-review form; decodes, never verifies | DV-1's form equals SPEC-0003 Appendix A as data; TV-4 shown under both codecs |
| `mofn root list` | prints a context's anchors in the words `root add` uses, with when each was accepted and its note | the listed line equals what `root add` printed |
| context names | a context must be a lowercase label (`[a-z][a-z0-9-]{0,62}`), because it becomes the anchor file's name; `../../../escaped` had written `wallet/escaped.yaml` | `root add` and `root list` refuse `../../../escaped`, `a/b`, `Default` and the empty name, exit 2, and nothing is written |
| `fixtures/` | DV-1, TV-1, TV-3, TV-4, the artifact, in both codecs, written by `sync.py` from `vectors.json` | drift test |
| `fixtures/golden/` | green, unauthorized, unknown-key (②b), tampered | the CLI test runs init → key gen → make → key import → root add → check with separate wallets per role, under **both** codecs, and diffs stdout against these |

## The library experiment (C4)

Both candidates against the two vectors C4 names (N-4, N-5), run with `python -I c4.py spec/vectors/ksa-core/vectors.json`
(PyNaCl 1.5.0, cryptography 43.0.3). The script, which was not committed:

```python
import json, sys, hashlib
import nacl.bindings as nb, nacl.signing, nacl.exceptions
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature
V = json.load(open(sys.argv[1]))
DS = bytes.fromhex(V["ds_label"])
alice = bytes.fromhex(V["keys"]["alice"]["pub"])
ident = bytes([1]) + bytes(31)
tv4 = V["positive"]["TV-4"]; tbs = bytes.fromhex(tv4["tbs"]); sig = bytes.fromhex(tv4["sig"])
L = 2**252 + 27742317777372353535851937790883648493
S = int.from_bytes(sig[32:], "little") + L
mal = sig[:32] + S.to_bytes(32, "little")
print("libsodium is_valid_point(alice)", nb.crypto_core_ed25519_is_valid_point(alice))
print("libsodium is_valid_point(identity)", nb.crypto_core_ed25519_is_valid_point(ident))
def nacl_verify(pub, m, s):
    try: nacl.signing.VerifyKey(pub).verify(m, s); return True
    except nacl.exceptions.BadSignatureError: return False
def ossl_verify(pub, m, s):
    try: Ed25519PublicKey.from_public_bytes(pub).verify(s, m); return True
    except InvalidSignature: return False
for name, f in [("pynacl", nacl_verify), ("cryptography", ossl_verify)]:
    print(name, "TV-4 good:", f(alice, DS+tbs, sig), " N-5 S+L:", f(alice, DS+tbs, mal))
try:
    k = Ed25519PublicKey.from_public_bytes(ident); print("cryptography loads identity point as a public key: yes (no point check exposed)")
except Exception as e: print("cryptography rejects identity:", e)
import cryptography; from cryptography.hazmat.backends.openssl import backend
print("versions: pynacl", nacl.__version__, "libsodium", nb.sodium_version_string() if hasattr(nb,'sodium_version_string') else '?', "cryptography", cryptography.__version__, backend.openssl_version_text())
```

Output:

```
libsodium is_valid_point(alice) True
libsodium is_valid_point(identity) False
pynacl TV-4 good: True  N-5 S+L: False
cryptography TV-4 good: True  N-5 S+L: False
cryptography loads identity point as a public key: yes (no point check exposed)
versions: pynacl 1.5.0 libsodium ? cryptography 43.0.3 OpenSSL 3.3.2 3 Sep 2024
```

Both reject N-5 (S + L). Only libsodium exposes a point check, so only it can
reject N-4 at V3 without our writing one. `cryptography` loads the identity
point as a public key.

## Goldens, as `check` prints them

① green — all six lines pass, answer yes, exit 0. ② unauthorized —
`authorization fail  release machine was never given the right to say this…`,
exit 1. ②b unknown key — `authenticity fail`, integrity / authorization /
acceptance not evaluated, exit 1. ③ tampered artifact — `integrity fail  your
file is not the one described…`, authorization not evaluated, exit 1.
