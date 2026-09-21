---
name: Distil a reference
description: Use when a library record is read and needs its distilled.md written, or when a distilled note reads like a summary instead of an argument.
---

# Distil a reference

A `distilled.md` earns its place by saving the next reader from opening the
source. A table of contents does not do that.

Three sections, in this order:

1. **What it says** — the *argument*, not the structure. "Registers signed
   statements with a transparency service so a relying party can check inclusion
   without trusting the issuer" beats "Section 4 defines the architecture."
2. **Why it matters here** — name the `DEC-*` or `R-*` and say which way it
   pushes. A note that does not move a decision is not finished.
3. **What it does not settle** — the honest limits. This section is the reason
   the file exists; a distilled note with nothing here has not been read
   critically.

Rules:

- **Quotes go in `quotes.md` with a locator** (section or page), never
  paraphrased into `distilled.md` as if they were ours. We cite precisely or not
  at all.
- **Disagree in writing.** If the source is wrong, or contradicts another
  record, say so and set `contradicts`. Agreement is cheap; a recorded
  disagreement is what makes the library worth keeping.
- **Derived material goes in `artifacts/`** — an extracted grammar, generated
  code, a diagram — each with a header naming what it came from. If an agent
  generated it, that is a `design-log/` entry too.
- Set `status: distilled` and an honest `confidence` only when all three
  sections are written. CI rejects `distilled` with TODOs left in.

Length is not the measure. Four honest paragraphs beat two pages of restatement.
If the document does not bear on an open decision, say that in one line and set
`confidence: low` rather than manufacturing relevance.
