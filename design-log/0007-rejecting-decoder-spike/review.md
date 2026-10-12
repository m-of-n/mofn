---
schema: "design-log/v1"
id: DL-0007
part: review
date: "2026-10-10"
---

# DL-0007 — review

A spike's rejections are mostly its own, because there is no prior text to
overturn. The two that matter are defects the fixtures caught in the code
written to run them.

## Rejected — the decoder's own first draft, caught by its fixtures

1. **Floats were rejected for the wrong reason.** `_head()` originally returned
   `(major, argument)` and applied the smallest-form rule to **every** major
   type. For major type 7, additional info 25/26/27 mean float16/32/64 and the
   following bytes are a **float payload, not an integer argument**.

   Every float was still rejected, so a fixture set that only asserted
   *rejection* would have passed and the bug would have shipped. They were
   rejected because a float's bit pattern happened to look like a non-minimal
   integer — and the float branch itself was comparing the argument *value*
   against 25/26/27, which is meaningless. `_head()` now returns
   `(major, ai, arg)` and major 7 is decided on `ai` alone.

   *A decoder that rejects correctly by accident is not evidence of anything*,
   and evidence is the only reason this spike exists. The fixture that exposed
   it was the one printing the diagnostic rather than only the verdict — which
   is an argument for fixtures asserting *why*, not just *whether*.

2. **The fixture suite's no-re-encoding check read prose as code.** It scanned
   for lines beginning `import`, and matched a line of `csexp.py`'s own
   docstring — the sentence explaining that the module does *not* import an
   encoder. It now parses with `ast`.

   The mirror image of finding 1: a check that passes for the wrong reason, in
   the thing doing the checking. Both were found in the same run, which is the
   argument for writing the negative fixtures before believing the positive
   result.

## Rejected — designs that would have made the experiment answer itself

3. **Letting the decoders import the encoder.** The obvious way to check
   canonicality is to decode, re-encode, and compare bytes. It is also the
   thing the falsifier is *about*: if that is the only way, condition (2)
   drags the producer's canonicaliser into the verifier and the R-O-05
   separation is cosmetic. Importing an encoder would have answered "yes"
   trivially and proved nothing. **The no-import constraint is what makes this
   a test**, which is why it is enforced twice — by `ast` over the source, and
   by loading both modules in a fresh interpreter and asserting the encoder is
   absent from `sys.modules`.

4. **Collapsing `hint=None` with an explicit default display hint in `Atom`.**
   Tempting: it makes equality behave the way an application expects, and it
   makes the crack disappear. It is also precisely the **silent normalisation**
   condition (2) forbids, and it would have hidden option 1's one real defect
   on the identity path inside the very tool built to look for defects. Kept
   distinct, with the reason in the class docstring.

5. **Doing only the `c-sexp` half.** #73 recommends option 1 first, correctly,
   because RFC 9804 makes it ~50 lines and the extraction already argues the
   result. But the falsifier in the topic answer is phrased about **rcbor**:
   *"write the decode path in rcbor as single-pass rejection and see whether
   bytewise key order and smallest-form heads are checkable inline."* Stopping
   at option 1 would have produced a true result about the candidate DEC-002 is
   **less** likely to pick, while leaving the sentence that actually threatens
   R-O-05 untested. Both were written.

## Rejected — a repeat of DL-0006's own mistake, caught this time

6. **Working from a stale base, again.** `bin/wt new` branched from local `main`
   at `cf866be`, one commit behind `origin/main` at `a5270ad` — which is the
   merge of DL-0006. Caught before a single commit, by listing `design-log/`
   and seeing `0006-canonical-encoding-close` missing, which would have made
   this entry DL-0006 for the second time in two days.

   DL-0006 §11 recorded the rule — *"branch from `origin/main` after a fetch,
   not from whatever `main` points at locally"* — and the very next task broke
   it anyway, because `bin/wt new` reads local `main` and says nothing about
   its age. **The lesson did not survive one day**, which says the fix belongs
   in the tool rather than in a design-log entry: `bin/wt new` could fetch, or
   warn when `main` is behind its upstream. Not changed here; that is a
   tooling PR, and this branch is a spike.

## What would overturn the result

Stated because an answer with no falsifier was not tested — the same discipline
`close-topic` applies to a topic.

- **Both decoders are ours, and so are the fixtures.** The result shows that
  *a* single-pass rejecting reader exists for each profile. It does not show
  that an independent implementation rejects the same inputs, which is the
  property interoperability actually needs. Differential testing against a
  mainstream CBOR library — decode with `fxamacker/cbor` or `cbor2` in a
  deterministic mode and compare verdicts on the negative fixtures — would be
  materially stronger, and is the obvious next step if DEC-002 lands on CBOR.
- **No fuzzing.** 36 negative fixtures are hand-written from the rules, so they
  test the rules we knew to write down. A fuzzer mutating valid encodings and
  asserting rejection would probe the rules we did not.
- **Python recursion, not a flat parser.** Both readers recurse, guarded at
  depth 256. A hostile input is therefore bounded by a hand-rolled limit rather
  than by the structure of the parser. An iterative reader would be a stronger
  claim about resource safety; this spike makes no such claim.
- **No performance claim whatsoever.** `rcbor.py` says it is "written to be read
  rather than fast" and these follow it.

## Accepted by the human

The instruction was two words, *"proceed with #73"*, with no constraint on
scope — so the judgement calls above are the model's, and #5 in particular
(doing both halves rather than the recommended cheap one) widened the work
beyond what the issue put first. **Nothing in this spike has been reviewed by a
person yet.** `DECODE-FINDINGS.md` is the document to read first if the result
is to be relied on; the code is short enough to check against it.
