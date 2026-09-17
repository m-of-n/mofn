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

- `0001-arch-0001-genesis/` — how ARCH-0001 v0.1.0 was produced (**T-012**, todo)
