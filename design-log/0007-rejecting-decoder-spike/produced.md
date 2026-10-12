---
schema: "design-log/v1"
id: DL-0007
part: produced
date: "2026-10-10"
---

# DL-0007 — produced

All in `prototype/`. Nothing in `spec/`, nothing in `src/`, no library change.

| file | code lines | what it is |
|---|---|---|
| `statements/csexp.py` | 125 | canonical S-expression reader — DEC-002 option 1 |
| `statements/rcbor_decode.py` | 136 | reduced-CBOR reader — DEC-002 option 5; the decoder `rcbor.py` never had |
| `statements/test_decode.py` | 141 | 60 fixtures, 36 of them negative |
| `statements/DECODE-FINDINGS.md` | — | the result, written to be read before the code |

`prototype/README.md` gains a row and one entry under *"known to be
unrepresentative"*, because `rcbor_decode.py` is evidence rather than a
component and nothing in the spike round-trips through it.

## The result

**The falsifier did not fire.** Canonicality is decidable by parsing alone, for
both candidates, with no re-encoding and no second pass. 60 fixtures, all
behaving; every accepted input read exactly once front to back; neither decoder
imports any module at all, checked by `ast` and again in a fresh interpreter.

So R-O-05's separation of authoring from verification is **real, not
cosmetic** — and the topic answer's strongest surviving objection to its own
position is retired.

## The finding worth carrying — map order needs no encoder

RFC 8949 §4.2.1 orders map keys **by their encoded bytes**, which reads like a
property only an encoder can know. It is not. A decoder reading a map is
already looking at those bytes: they are the slice of input the key was just
parsed from. The check is a bytewise comparison of two buffer slices.

**The producer sorted on exactly the bytes the consumer is looking at.**

Two things fall out, and both are cheaper than expected:

- **Duplicate keys are free.** *Strictly* ascending rejects equality as a
  special case, so one comparison enforces both rules. There is no separate
  duplicate check anywhere in the decoder.
- **Smallest-form heads are purely local.** Additional info 24 must carry a
  value ≥ 24, else a shorter head would do; 25/26/27 against 2^8, 2^16, 2^32.
  It lives in `_head()`, so no call site can forget it.

## The options differ in kind, not only in cost

Option 1's equivalent of smallest-form is **in the grammar**:
`decimal = %x30 / (%x31-39 *DIGIT)` (RFC 9804 §7.1). `03:abc` is not
non-canonical, it is **ungrammatical** — it fails to parse. There is no code
path in which the rule is separable from parsing, so a conforming reader cannot
omit it.

Option 5's equivalent is a rule the implementation must state and check. This
decoder does check it. But an implementation could omit it and still parse
every valid document, which is the difference the topic answer was reaching for
with "the smallest attack surface of the three". The spike makes it concrete.

## What parsing cannot decide — recorded as a limit, not a gap

1. **Option 1's default display-hint crack.** `[24:application/octet-stream]3:abc`
   and `3:abc` are *both grammatical*, denote the same value to an application
   applying the default, and hash differently. No parser can reject either.
   `csexp.py` keeps `hint=None` distinct from an explicit hint rather than
   collapsing them — collapsing is the silent normalisation condition (2)
   forbids. A **profile** rule closes it; RFC 9804 §8 already sanctions "no
   display-hints" as a restriction an application may adopt.
2. **Unicode normalisation — condition (6).** NFC and NFD spellings are both
   valid UTF-8 and both canonical. The decoder validates UTF-8 and rejects
   invalid bytes; it has no basis to reject a validly-encoded alternative
   normalisation.

Both sit on the **identity** path rather than the signing path — the asymmetry
the topic answer already predicted: signing fails loudly, naming fails
silently.

## What it does not settle

DEC-002. Library availability, the ARCH-0001 §4 data-model mapping, and
conditions (5) and (6) are all untouched. Condition (5) is an *addition* to
both candidates and is not something a decoder can supply — #72 and
library#56 own it.
