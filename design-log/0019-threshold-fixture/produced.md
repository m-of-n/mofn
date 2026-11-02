---
schema: "design-log/v1"
id: DL-0019
part: produced
date: "2026-11-01"
---

# DL-0019 — produced

| file | what |
|---|---|
| `spec/vectors/ksa-core/generate.py` | key `dave`, DV-2, TV-9…13, N-7…10; every old vector byte-identical (checked against the previous `vectors.json`) |
| `spec/vectors/ksa-core/vectors.{json,md}`, `README.md` | regenerated; README maps the vectors to the invariant and the acceptance test |
| `spec/SPEC-0002-ksa-core.md` | 0.2.0 → 0.3.0; Appendix A from `vectors.md`, and which check owns which clause. No existing signed or hashed byte changes |
| `spec/ARCH-0001-*.md` | 0.1.5 → 0.1.6; §7's "no threshold vector yet" replaced by what the fixture found |
| `project/BACKLOG-0001.md` | 0.12.3 → 0.12.4; T-031 → `review`, its "narrowed" claim corrected |
| `prototype/wallet/tests/test_vectors.py` | N-7…10 expected steps; a test that every published negative has one |
| `prototype/wallet/README.md` | DV-1 is no longer the only vocabulary in the vectors |

## The vectors

| vector | case | result |
|---|---|---|
| TV-9 | 2 of {Alice, Bob, Dave}, `this` absent | verified |
| TV-10 | `k = n = 3` | verified |
| TV-11 | `k = 1`, `n = 2` (fewest members) | verified |
| TV-12 | `define` of DV-2 | verified |
| TV-13 | Alice says Bob's key has name "fred" | verified |
| N-7 | `k = 0` | V8 `kind-rule` |
| N-8 | `k = 4`, `n = 3` | V8 `kind-rule` |
| N-9 | body field 5 = 4 beside three members | V7 `structure` |
| N-10 | array head of `trusts` says 4, three members follow | V5 `encoding` |

Boundaries are positives because one 2-of-3 cannot catch an off-by-one in
`1 ≤ k ≤ n`: `<` for `≤` would pass TV-9 and fail TV-10 or TV-11.

## `n ≠ len(members)` cannot reach V8

The task, `ADR-0004` and `ARCH-0001` §7 treat all three negatives as V8's. Two
are. `SPEC-0002` §8.6 has `threshold` and `trusts` and **no `n`**: `n` is the
array head of `trusts`. So the case has only two spellings:

- **N-9** adds a field for `n`. Well-formed, correctly signed, and the closed
  body map stops it at V7 (`body: unknown field 5`).
- **N-10** makes the head lie: TV-9's TBS with `03 83 5820…` changed to
  `03 84 5820…`, re-signed. Malformed CBOR, stopped at V5 (`map keys out of
  order at offset 241`). `cbor2`, an independent decoder, also refuses it
  (`CBORDecodeEOF`).

So V8 owns `1 ≤ k ≤ n`, and `n = len(members)` holds by construction, enforced
by V7 and V5. `test_vectors.py` asserts both steps. This narrows the sentence in
`ARCH-0001` §7; it is stated there, and `Threshold` keeps `n` as a logical field.

**Not a defect in option 5.** The invariant is unwritable because of §8.6's
body shape, not the encoding: KSA-CBOR could carry an `n` field if §8.6 had one.
All thirteen positive vectors encode identically under both encoders, and every
negative is rejected. The ADR's supersession condition is not met.

## What the T-031 row still owed

| item | decision | why |
|---|---|---|
| threshold subject | **done** | above |
| `NameCert` | **done**: TV-13, TV-12, DV-2 | the row's "covers the name-binding shape" was wrong; see below |
| round-trip | **already met**; nothing added | R-0006 §3.12 called these produce-and-verify vectors, written before the wallet. `test_encoder_reproduces_tbs` and `test_round_trip_is_byte_exact` now parametrise over every positive vector, so TV-9…13 got both automatically |
| option-2 comparison | **not owed**; not built | it was a scoring input to a decision now taken. `ADR-0004` rejected option 2 on P1, which no fixture changes, and closed MD-3's narrowing. Building COSE native bytes now would also lean on an export envelope while DEC-005 is open |

**Why `NameCert` was still owed.** R-0006 §3.12 and the T-031 row said TV-1/TV-2
cover the name-binding shape. TV-1 is a `key-publish`; TV-2 is a `self` whose
`label` is, in `SPEC-0002` §8.3's words, *"a display string, not a binding"*, and
it is about the speaker's own key. Neither has one key naming another.
`ADR-0004`'s "Met" list silently omits `NameCert` too, while `ARCH-0001` §7's
test still requires it. `Closes #8` would have overclaimed without a vector.

Under `ARCH-0002` P6 a `NameCert` is an `attestation` about a key with a name
predicate, so TV-13 is that. It needed a text-typed `name`, and DV-1 cannot take
one: its id is hashed into every existing vector. Hence DV-2, published by TV-12
so that the statement is attributable.
