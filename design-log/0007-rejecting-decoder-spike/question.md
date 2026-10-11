---
schema: "design-log/v1"
id: DL-0007
part: question
title: "The rejecting-decoder spike — testing the canonical-encoding falsifier"
date: "2026-10-10"
model: "claude-opus-5"
human: ndewedo-newbury
outcome: "prototype/statements/{csexp,rcbor_decode,test_decode}.py + DECODE-FINDINGS.md. Falsifier did not fire: condition (2) is reachable for DEC-002 options 1 and 5. No ADR — DEC-002 untouched."
status: complete
---

# DL-0007 — question

## Context supplied

Issue **#73** in full; `mofn/CLAUDE.md` and `prototype/README.md`;
`prototype/statements/rcbor.py` (the encoder with no decoder);
`library/topics/canonical-encoding.yaml` (`status: answered`, DL-0006) and its
recorded falsifier; the RFC 9804 FX-1 extraction, specifically
`distilled/schema/canonical.abnf`, `distilled/schema/advanced-transport.abnf`
and `distilled/design-notes.md` §1 condition 2; the RFC 8949 extraction's
determinism rows.

## Question posed

> "proceed with #73"

#73 is the spike the `canonical-encoding` close handed off, because #14
forbade implementation code. It exists to test one sentence the topic answer
committed to and then marked untested:

> If checking canonicality on decode cannot be done without re-encoding, then
> condition (2) drags the canonicaliser of the producer back into the verifier,
> the R-O-05 separation is cosmetic, and **DSSE is simply right** — meaning
> abandon canonical form, sign received bytes, and identify subjects by content
> digest only.

Condition (2): *the decoder REJECTS non-canonical input rather than normalising
it.* The answer said the two hard CBOR rules — bytewise map-key order and
smallest-form integer heads — "appear to be" checkable inline, and that this
was **untested**. That qualifier is what the spike removes or confirms.

## What makes this answerable by code at all

The claim is narrow and empirical, which is why it was worth building rather
than arguing. It is not "is CBOR a good choice" — it is "can a reader decide
canonicality while going forwards once, without encoding anything". Three
properties had to be *enforced*, not asserted, or the experiment would beg its
own question:

1. **single-pass** — the read position only increases; bytes consumed must
   equal input length on success.
2. **no re-encoding** — the decoders must not import an encoder. If a decoder
   may canonicalise-and-compare, it answers "yes" trivially and tells us
   nothing.
3. **no normalising** — every rejection raises; nothing is repaired, defaulted,
   reordered or coerced.

## Scope held

`src/` stays empty while DEC-002 is open (`CLAUDE.md`), so this is
`prototype/` — throwaway, never ships. No architecture document: the
condition (2) clause belongs to ARCH-0002 P5 and is **#72**'s, not this
spike's. Nothing here accepts a DEC.

#73 recommended doing option 1 first because RFC 9804 makes it cheap. Both
were done, and `review.md` §5 says why stopping at one would not have answered
the question actually asked.
