# Single-pass rejecting decoders — what #73 found

**SPIKE. Nothing here decides anything.** DEC-002 is open and only an
`ADR-NNNN` closes it (ARCH-0001 §9.2). This records an experiment and its
result.

Run it: `python3 prototype/statements/test_decode.py`

## The question

The `canonical-encoding` topic answer closed with a falsifier:

> If checking canonicality on decode cannot be done without re-encoding, then
> condition (2) drags the canonicaliser of the producer back into the verifier,
> the R-O-05 separation is cosmetic, and DSSE is simply right — meaning abandon
> canonical form, sign received bytes, and identify subjects by content digest
> only.

Condition (2) is *the decoder rejects non-canonical input rather than
normalising it*. The answer said the two hard rules "appear to be" checkable
inline **and that it was untested**. This is the test.

## The result

**The falsifier does not fire.** Canonicality is decidable by parsing alone,
for both candidates, with no re-encoding and no second pass.

| | option 1 — canonical S-expressions | option 5 — reduced CBOR |
|---|---|---|
| reader | `csexp.py`, 125 lines of code | `rcbor_decode.py`, 136 lines of code |
| single pass | yes — bytes read == input length | yes — same |
| re-encoding | none; the module imports nothing | none; does not import `rcbor` |
| lookahead | 1 byte, to find `)` | none |
| fixtures | 8 accepted, 16 rejected | 16 accepted, 20 rejected |

60 fixtures, every one behaving. The negative fixtures are the evidence; the
positive ones are the control.

## Why map order does not need the encoder — the crux

This is the finding worth carrying forward, because the rule *sounds* like it
needs an encoder and does not.

RFC 8949 §4.2.1 orders map keys **by their encoded bytes**. Phrased that way it
reads as a property only an encoder can know. But a decoder reading a map is
looking at those encoded bytes already — they are the slice of the input the key
was just parsed from. So the check is:

```python
before, now = self._buf[prev[0]:prev[1]], self._buf[start:end]
if before >= now: reject
```

Two slices of the buffer, compared bytewise. **The producer sorted on exactly
the bytes the consumer is looking at.** Nothing is re-encoded because nothing
needs to be.

Two consequences fall out:

- **Duplicate keys come free.** *Strictly* ascending rejects equality as a
  special case, so one comparison enforces both rules. They are not checked
  separately anywhere in the decoder.
- **Smallest-form heads are purely local.** A head with additional info 24 must
  carry a value ≥ 24, or a shorter head would have done; likewise 25/26/27
  against 2^8, 2^16, 2^32. One comparison, no context. It lives in `_head()`
  so no call site can forget it.

## The options differ in kind, not just in cost

Option 1's equivalent of the smallest-form rule is **in the grammar**:

```abnf
decimal = %x30 / (%x31-39 *DIGIT)      ; RFC 9804 §7.1
```

"Zero, or a nonzero digit followed by digits." `03:abc` is not *non-canonical* —
it is **ungrammatical**, and fails to parse. A conforming reader cannot forget
the rule because there is no code path in which the rule is separate from
parsing.

Option 5's equivalent is a rule the decoder must *state and check*. This
decoder does check it, which is the whole point — but the obligation lives in
the implementation rather than in the grammar, and an implementation can omit
it and still parse every valid document. That difference is what the topic
answer meant by option 1 having "the smallest attack surface of the three",
and the spike makes it concrete rather than rhetorical.

## What parsing CANNOT decide — the honest limit

Condition (2) is reachable. Two things next to it are not, and a decoder is the
wrong tool for both:

1. **Option 1's default display-hint crack.** RFC 9804 §4.6 neither writes out
   nor strips a default hint, and §4.7 makes the hint part of equality. So
   `[24:application/octet-stream]3:abc` and `3:abc` are **both grammatical**,
   denote the same value to an application applying the default, and have
   different bytes and therefore different digests. No parser can reject one,
   because nothing is wrong with either. `csexp.py` keeps `hint=None` and
   `hint=b"..."` distinct rather than collapsing them — collapsing would be the
   silent normalisation condition (2) forbids. **A profile rule closes this**
   (RFC 9804 §8 already sanctions "no display-hints" as a restriction an
   application may adopt); a decoder cannot.

2. **Unicode normalisation — condition (6).** Two spellings of the same text
   differing by NFC/NFD are both valid UTF-8 and both canonical under either
   candidate. The decoder validates UTF-8 and rejects invalid bytes; it has no
   basis to reject a validly-encoded alternative normalisation. This is the
   hazard the topic answer documents against U+FB33, and it remains exactly
   where the answer put it: normalise at authoring, reject at decode, as a
   profile rule.

Both limits sit on the **identity** path, not the signing path — which is the
shape the topic answer already predicted: signing fails loudly, naming fails
silently.

## A bug the fixtures caught, kept on the record

The first draft of `rcbor_decode.py` returned `(major, argument)` from `_head()`
and applied the smallest-form rule to major type 7 as well. For major 7,
additional info 25/26/27 mean float16/32/64 and the following bytes are a float
payload, not an integer argument.

Every float was still rejected, so a looser fixture set would have passed. But
they were rejected **for the wrong reason** — "non-smallest head", because a
float's bits happened to look like a non-minimal integer — and the float branch
was testing the argument *value* against 25/26/27 rather than the additional
info, which is meaningless. `_head()` now returns `(major, ai, arg)` and major 7
is decided on `ai` alone.

Recorded because *a decoder that rejects correctly by accident is not evidence
of anything*, and this spike exists to produce evidence. The fixture that
exposed it was the one asserting the diagnostic, not merely the rejection.

(The fixture suite's own import check had the mirror-image defect: it grepped
for lines starting with `import`, and caught `csexp.py`'s docstring explaining
that it does *not* import an encoder. It now parses with `ast`.)

## What this does and does not settle

**Settles:** condition (2) is reachable from the cited documents for both
candidates, so R-O-05's separation of authoring from verification is real and
not cosmetic. DSSE's objection — that canonicalisation forces a verifier to
parse untrusted input before authenticating it — is answered by R-O-05's
ordering, and nothing in the experiment weakens that answer.

**Does not settle:** DEC-002. Library availability, the data-model mapping in
ARCH-0001 §4, and conditions (5) and (6) are untouched here. Condition (5) in
particular is an *addition* to both candidates, not something a decoder can
supply — see #72 and library#56.

**Does not propose:** any change to ARCH-0001 or ARCH-0002. The condition (2)
clause belongs to ARCH-0002 P5 and is #72's to write; this spike only removes
the "untested" qualifier from the argument for it.
