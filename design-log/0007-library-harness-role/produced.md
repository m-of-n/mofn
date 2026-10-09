---
schema: "design-log/v1"
id: DL-0007
part: produced
title: "What the library is for — the harness framing, and the one-way bears_on edge"
date: "2026-10-09"
model: "claude-opus-5"
human: "pending"
outcome: "README.md in both repos; library CLAUDE.md shape block corrected. No ADR. No DEC touched. FX-1 unchanged."
status: open
---

# DL-0007 — produced

## 1. The answer given

`distilled/` is not universal and was never meant to be. `summary.md` is the
human layer — enough to decide whether to read the source. `distilled/` is the
machine layer defined by `library/docs/extraction.md` (FX-1): normative text,
every BCP 14 requirement with a stable id `<record>#R-NNNN`, schemas, message
formats, protocol model, state machines, test vectors, design notes.

The purpose, stated in one line: **`distilled/` makes a source citable at
requirement granularity instead of document granularity.**

That is precisely the harness framing the question supplied. A bibliography
answers *what did we read*. An evidence layer answers *which requirement in
which standard does this clause of ARCH-0001 rest on* — and only an extracted
requirement with an id can answer it.

## 2. The defect the question exposed

**The citation edge runs one way.**

Records point inward: 304 of them declare `bears_on`, concentrated on DEC-002
(25) and DEC-005 (14). Nothing points back. `spec/` and `project/` contain
**zero** occurrences of a `<record>#R-NNNN` id.

So the expensive half of the library — four fully extracted records, roughly a
third of the bytes in `records/` — produces addressable requirements that
nothing addresses. FX-1 is being satisfied as a standard rather than consumed
as a feed. This is not an argument against FX-1; it is the reason FX-1 does not
yet pay for itself, and it is invisible unless someone greps for it.

## 2b. Follow-on question: does the #45 re-ingest trigger FX-1?

Asked next: will the re-ingest (library#45) add `distilled/` to the records
missing it?

**No — and that is deliberate.** `bin/check-pr-extraction` fires on three
triggers only: `status: distilled`, a declared `distillation` block, or a PR
that changes the record's `distilled/`. Filling a scaffold into a real
`summary.md` and setting `status: summarized` hits none of them; the gate
prints those records under *"summary bar — not extracting, FX-1 not
required"*. The 2026-10-03 amendment exists precisely so that a summarising
lane does not owe four multi-agent passes.

**But #45's own `Done when` disagrees with its own gate.** Bullet 1 requires
*"169 unfilled FX-1-eligible records at `distillation.profile: full`"*, while
the load-bearing check the issue nominates — `bin/validate --scaffolds` must
report 0 — inspects summary scaffold text and says nothing about `distilled/`.
A completed re-ingest therefore drives scaffolds to zero, passes every
mechanical gate, and leaves bullet 1 unmet with nothing reporting it.

That is structurally the same blind spot already recorded on #45 for
`draft-ietf-vcon-vcon-core-04` — `status: distilled`, no `profile: full`, and
no mechanism that notices — at 169 times the scale. Raised as a comment on
#45; not resolved here, because which records genuinely need FX-1 is the scope
call this entry declines to make.

## 3. Changes made

| file | change |
|---|---|
| `library/README.md` | new **What this is for**: harness component, the three record layers, why distillation is deliberately rare |
| `library/README.md` | layout block: real shape; `index/` added as generated and untracked |
| `library/CLAUDE.md` | same stale shape line corrected |
| `mofn/README.md` | new **The library** section: evidence layer, `bears_on` as a query, requirement-level citation, the pin, and the "open `library/` as the project" warning |
| `mofn/README.md` | layout line: "the bibliographic library" → "the reference library (evidence layer)" |

No record data, schema, tooling, spec text or DEC status touched.

## 4. What the model declined to do

- **Did not narrow FX-1.** The scale figures (203 in-scope records, 118 still
  stub, a third of repo bytes in four extractions) invite a proposal to apply
  FX-1 more selectively. That is a human's call about project scope, not a
  README edit, and making it silently inside a documentation change would be
  exactly the kind of decision-by-accident `CLAUDE.md` forbids.
- **Did not write a new document.** The framing belongs in the two READMEs that
  were wrong, not in a third file explaining them.
- **Did not put counts in either README.** `5 of 304` is true this week. A
  README that carries live figures is a README that lies by March. The counts
  live here and in the PR bodies, which are dated.
- **Did not record the one-way `bears_on` gap in the READMEs.** A README states
  the design; the gap is backlog, and belongs in `BACKLOG-0001`.
