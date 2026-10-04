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
| `0003-cbor-reference-sweep` | library CBOR record set, RPT-0001 | complete — queries not archived, `research/README.md` rule 2 unmet |
| `0004-canonical-encoding-lane-b` | `canonical-encoding` topic, `rfc-8785` FX-1 record | complete — output is `library` `79c543a`; see the cross-repo note below |

`DL-0001` is the argument for the rule: **write the entry in the same change.**
The prompts, and what the human rejected, were not recoverable a week later —
including whether ARCH-0001 §4.2's five statement kinds were proposed or
directed, which register item 6a now has to decide without that evidence.

**`DL-0004` found the rule is not satisfiable as written.** A lane whose output
lands in `library/` cannot put its design-log entry in the same commit, because
`design-log/` is in `mofn/`. DL-0004's entry names the library commit it
describes and was written minutes after it, which is the closest available
approximation — but the agreement needs amending to either allow a declared
cross-repo pair or move `design-log/` somewhere that can see both repositories.
Recorded in `0004-canonical-encoding-lane-b/review.md`.
