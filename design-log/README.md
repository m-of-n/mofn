# Design log

The project claims **AI-assisted protocol design** as part of its contribution.
That is only a contribution if it is instrumented from day one — retrofitted in
November it produces a narrative, not evidence.

One entry per design decision:

```
NNNN-slug/
  question.md   what was asked, and the context supplied
  produced.md   what the model produced (spec text, schema, code, vectors)
  review.md     what a human accepted, edited, or REJECTED — and why
  → outcome: the ADR, or the reason there is none
```

Every generated artifact elsewhere in the repo carries a header naming its
source: which document section, which prompt, which model, which date.

**Write up the failures.** The half where a human overruled the model is what
makes the claim credible, and it is the half nobody else publishes. A design log
containing only successes is evidence of poor record-keeping, not of good design.

**Guardrail:** no generated cryptographic primitives, ever. Vetted libraries
only. AI assistance applies to specification, schema, encoding, mappings, test
vectors, and tooling.

## Entries

| id | subject | status |
|---|---|---|
| `0001-arch-0001-genesis` | ARCH-0001 v0.1.0 | **partial** — reconstructed a week late, and permanently degraded as a result |
| `0002-arch-0002-cycle` | ARCH-0002, ADR-0001 | complete |
| `0003-cbor-reference-sweep` | library +51 records, 2 topics; RPT-0001 | complete |
| `0004-library-body-field` | library `body` — scope §4, record schema v0.6.0; the three defects it turned up | **open** — human review pending on library#34, #37, mofn#55 |
| `0005-cipher-suite` | what a cipher suite is, critique of the external `cipher_suite.py` | **open** — human review pending; no code change; DEC-002 untouched |
| `0007-library-harness-role` | what the library is for — README in both repos; the one-way `bears_on` edge | **open** — human review pending; no spec change; FX-1 untouched |
| `0008-quotes-md-retirement` | `quotes.md` and the pre-FX-1 companion vocabulary — record schema v0.7.0 | **open** — human review pending; no spec change; library#63 |

**`0006` is reserved** by the canonical-encoding lane B entry on mofn#74, which
is open and not yet merged. The gap closes when that PR lands.

`DL-0001` is the argument for the rule: **write the entry in the same change.**
The prompts, and what the human rejected, were not recoverable a week later —
including whether ARCH-0001 §4.2's five statement kinds were proposed or
directed, which register item 6a now has to decide without that evidence.
