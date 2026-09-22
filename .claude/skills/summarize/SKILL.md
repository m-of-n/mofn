---
name: Summarise a reference
description: Use when a library record has been read and needs its summary.md written — the primary human- and AI-facing document for every record.
---

# Summarise a reference

`summary.md` is the **primary** document for a record and the one a human
reviews. Write it first. `schema/summary.template.md` is the shape;
`distilled.md` is a different job — see the `distil` skill.

Sections, all of them:

1. **Bibliographic header** — type, maturity, authors, date, identifier,
   source URL, digest. Enough to cite the document without opening it.
2. **Overview** — two to five sentences on the *argument*. "Registers signed
   statements with a transparency service so a relying party can check
   inclusion without trusting the issuer" beats "Section 4 defines the
   architecture."
3. **Applicability** — rate security, cryptography, and this project as
   `core` / `adjacent` / `none`, each with a one-line why. Name the `DEC-*` or
   `R-*`, or say plainly it bears on none yet.
4. **Implementations** — open source and commercial, what we could build on.
   *"Searched, none found on YYYY-MM-DD"* is a result; an empty section with no
   date is not.
5. **Artifacts in this record** — every other file in the directory and what it
   is for. The reviewer should not have to `ls`.
6. **Limits** — what it does not settle. Nothing here means it was not read
   critically.

Rules:

- **YAML front matter on every markdown file** in a record. OKF alignment;
  `bin/validate` enforces it.
- **`maturity`: do not guess.** RFC 2026 levels — `standard`, `best-practice`,
  `informational`, `experimental`, `historic`. Leave it unset rather than
  assert standing you did not check. An RFC being an RFC does not make it a
  standard.
- **Quotes go in `quotes.md` with a locator**, never paraphrased into
  `summary.md` as if they were ours.
- **Disagree in writing.** If the source is wrong or contradicts another
  record, say so and set `contradicts`. Agreement is cheap; a recorded
  disagreement is what makes the library worth keeping.
- Prefer a controlled tag from `schema/tags.yaml` when one fits.
- `status: summarized` only when all six sections are real. CI rejects
  template text left in place.

Four honest paragraphs beat two pages of restatement. If the document bears on
nothing yet, say that in one line and leave it `status: stub` — that is a
legitimate record, not a failure.
