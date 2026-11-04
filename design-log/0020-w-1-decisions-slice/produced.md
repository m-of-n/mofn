---
schema: "design-log/v1"
id: DL-0020
part: produced
date: "2026-11-01"
---

# DL-0020 — produced

Model: Claude Opus 5.5. No primitive was added. The experiment below composes a
signature from libsodium's own operations to test a key rule; it is not
committed and nothing ships it.

## What changed

| where | what |
|---|---|
| `demo/slice.sh` | five cases under each of two codecs, one wallet per role, byte comparison with the goldens (below) |
| `spec/SPEC-0004` 0.2.0 | §10.1 digest subject comes from the relying party's copy; §10.4 integrity line and the meaning of **not evaluated** |
| `spec/SPEC-0002` 0.4.0 | §6.3 prime-order subgroup rule; §11.3 YAML version, target spelling, `0x` text; §11.1 notes the exception. The header line said 0.1.0 and now says the version |
| `spec/SPEC-0003` 0.1.1 | Appendix A quotes the `ask` value; the header line says the version |
| `engine/schema.py` | `plain_is_text` now also refuses what YAML 1.2 or a 1.1 parser reads as non-text (below) |
| `tests/` | four rejections, three text round trips, a description-target round trip; the DV-1 test no longer patches the example before comparing |
| `.github/workflows/ci.yml` | the `wallet` job runs the slice |
| `prototype/wallet/README.md`, docstrings | departures table and comments follow the decisions; `suite.py` cited the old number 0014 |

## The slice

One wallet each for issuer, key-holder and relying party, under
`demo/wallets/<codec>/`. Everything the relying party reads is in `handover/` or
its own wallet. The other two wallets are `chmod 000` before it starts, so a
check that depended on them would fail, not pass by accident.

| case | how | golden | exit |
|---|---|---|---|
| ②b | speaker's key not imported yet | `unknown-key.txt` | 1 |
| ② | key imported, no `root add` | `unauthorized.txt` | 1 |
| ① | after `root add` | `green.txt` | 0 |
| ③ | a copy with the first byte set to `X` | `tampered.txt` | 1 |
| ②′ | key-holder's valid statement, while the issuer is anchored | `unauthorized.txt`, label swapped | 1 |

②′ exists because ② alone never shows a key that stays unanchored while another
is trusted. It proves the anchor does not leak to a second key. The relying
party calls that key `key holder`, so the golden's label is swapped for the
comparison; that is the only rewrite of a golden.

**Checked by the agent, not yet by a human.** From a fresh `git clone` and a new
venv, with network denied by `sandbox-exec`, an empty `HOME` and a minimal `PATH`:
ten of ten cases pass, and the tree stays clean. The slice went red for each
planted fault, in a scratch copy: a different flipped byte, no `root add`, a wrong
expected exit code. A relying party reaching into the issuer's wallet stopped the
run with an error. Statements are made fresh each run, so the goldens do not age
out before the Nov 11 floor. TV-3's `define` was checked at later `--at` times.

**Run again 2026-11-03, at Chip's request**, by the agent: on the branch at
`1847bf3`, and from a fresh clone of it with network denied and an empty `HOME`.
Both printed `slice: 5 cases passed under each of 2 codecs`, ten of ten `[ok]`.

## Measured: a key with a torsion component (C4)

Throwaway script (PyNaCl 1.5.0, cryptography 43.0.3), run with `python -I`.
`T8` is a published order-8 point; `mixed` = `A + T8`, an honest key with a torsion
point added.

```python
a = nb.crypto_core_ed25519_scalar_reduce(hashlib.sha512(b"c4b fixed test scalar").digest())
A = nb.crypto_scalarmult_ed25519_base_noclamp(a)
mixed = nb.crypto_core_ed25519_add(A, T8)
def sign(m):                                    # RFC 8032 equations over libsodium's scalar ops
    r = nb.crypto_core_ed25519_scalar_reduce(hashlib.sha512(b"r" + a + m).digest())
    R = nb.crypto_scalarmult_ed25519_base_noclamp(r)
    h = nb.crypto_core_ed25519_scalar_reduce(hashlib.sha512(R + mixed + m).digest())
    return R + nb.crypto_core_ed25519_scalar_add(r, nb.crypto_core_ed25519_scalar_mul(h, a))
```

```
is_valid_point honest True mixed False
of 800 messages signed under the mixed key: libsodium verify accepts 100, OpenSSL verify accepts 100, both 100
```

The equation holds when the hash clears the torsion part, one message in eight
at order 8, and both verify functions then accept. So a verifier applying
SPEC-0002 0.2.0 §6.3 to the letter returns **verified** for those statements
while this engine returns **invalid** at V3. That is the split C4 asked about.

## Measured: which YAML the reader is

`plain_is_text` under PyYAML 6.0.2 (YAML 1.1), before this change:

| plain scalar | PyYAML | YAML 1.2 core | §11.3 |
|---|---|---|---|
| `yes`, `no`, `on`, `off` | boolean | text | rejected, safely |
| `1e3` | **text** | float | floats MUST be rejected; **was accepted** |
| `0o17` | **text** | integer | octal MUST be rejected; **was accepted** |
| `y`, `n` | text | text | a 1.1 parser may read a boolean, so now rejected |
| `{en: x?}` | refused | text | the DV-1 example failed here |

`1e3` and `0o17` were real gaps in the reader against §11.3 as written. They are
fixed and tested, whatever the sponsor decides about the version sentence. The
writer already quoted anything outside a narrow safe set; it quotes these too,
and they round-trip.
