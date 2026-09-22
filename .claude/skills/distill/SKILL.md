---
name: Distil a reference for requirements extraction
description: Use when a long document — usually a PDF standard — needs a compacted agent-friendly rendering so requirements can be extracted from it.
---

# Distil a reference

**Secondary and optional.** `summary.md` comes first and always; this is for
documents an agent must work *through* rather than merely know about —
typically a long PDF standard.

Purpose: a compacted rendering that preserves everything needed to extract
requirements, and discards everything else. Not a summary. Not prose.

1. **Only distil what will be mined.** If nobody is going to extract
   requirements from it, it does not need a `distilled.md`. Most records never
   get one.
2. **Preserve normative language exactly** — MUST, SHALL, SHOULD, MAY, and the
   negatives. These are the payload. Never paraphrase a normative sentence.
3. **Keep the locator on every retained statement** — section number, page.
   An extracted requirement that cannot be traced back is not usable.
4. **Drop**: motivation, history, acknowledgements, examples that do not carry
   a constraint, repeated boilerplate.
5. **Preserve structure** as headings, so section numbering survives
   compaction.
6. YAML front matter, like every markdown file in a record.

Requirements extracted from it go in `requirements/` as YAML, one file per set,
each carrying the source locator and the normative verb.

## Hard rules

- **Never invent a requirement.** If the document implies rather than states,
  record it as an inference and mark it so — an invented MUST is a defect that
  propagates into our own specification.
- **Never distil from a summary.** Distil from the source document.
- Set `status: distilled` only when `summary.md` is already complete. The order
  is not negotiable: a human reviews the summary, then an agent mines the
  distillation.

A distillation that is 20% of the source and loses no normative statement is a
good one. One that is 60% has not been distilled.
