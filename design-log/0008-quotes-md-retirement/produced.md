---
schema: "design-log/v1"
id: DL-0008
part: produced
title: "quotes.md and the pre-FX-1 companion vocabulary — what the schema still described"
date: "2026-10-09"
model: "claude-opus-5"
human: "pending"
outcome: "library#63 — record schema v0.7.0, summarize skill, summary template, construction.md decision 6. No ADR. No DEC touched. FX-1 unchanged."
status: open
---

# DL-0008 — produced

## 1. The answer to the question as asked

`quotes.md` specifies **verbatim excerpts with locators, for citation** — and
the convention it holds has four parts, in descending order of how
load-bearing each is:

1. **Voice separation.** A sentence in `summary.md` is a claim *we* make and
   are accountable for; a line in `quotes.md` is one the *source* makes and we
   carry. The skill stated it directly: *"never paraphrased into `summary.md`
   as if they were ours."*
2. **Locator discipline.** Every excerpt addressable, so a claim is checkable
   without re-reading the document.
3. **The sanctioned excerpt channel.** The library commits no third-party
   bytes. `quotes.md` was the one place source text could legitimately sit —
   fragments, not the document.
4. **Evidence for disagreement.** `contradicts` is worth little without the
   source's actual words.

## 2. Why it was retired rather than reinstated

Parts 1, 2 and 4 are **already enforced elsewhere, more strictly**:
`distilled/requirements.yaml` carries `text` (verbatim) plus `locator`, and
`bin/validate`'s verbatim check asserts every `text:` is a substring of the
source. `quotes.md` had no check at all. Part 3 has no live claimant: no
record has ever needed to park an excerpt.

The practice that replaced it was already written down, by a human, in a
record — `records/ietf/rfc-9943/summary.md`:

> the section locators above are the substitute, and a reader checking a claim
> should open the RFC at the cited §.

The change **promotes that sentence to the rule** rather than inventing one.

## 3. Changes made — library#63, stacked on library#61

| file | change |
|---|---|
| `schema/record.schema.yaml` | v0.6.0 → **v0.7.0**. `quotes.md`, `requirements/`, `artifacts/` removed; `distilled/` artifact kinds replaced with FX-1's eight, deferring to `docs/extraction.md`, with extras declared rather than substituted |
| `.claude/skills/summarize/SKILL.md` | the quotes mandate → **attribute by locator, not by transcription**; a new rule asking for the declared-absence line; the retired `distilled.md` pointer and misspelled `distil` skill name corrected |
| `schema/summary.template.md` | *Artifacts in this record* prompts for the absence line, so the fill produces it by default |
| `docs/construction.md` | **decision 6** in the existing v0.1 register, with the condition that would reinstate a quote file |
| `records/ietf/rfc-9942`, `rfc-9943` | drop the `quotes.md` half of their absence line |

Nothing in `bin/` changed: nothing parses `companions:`.

## 4. What the model got wrong, and what the human's question corrected

**The model proposed the wrong default.** Asked to settle this, it recommended
*"keep optional, fix the skill's mood"* — the minimum-change option. It reached
that before reading `797ef06` and without auditing the neighbouring entries.

The human did not accept the recommendation. The question *"what is quotes.md
supposed to specify, what is the convention it holds?"* forced the design
history open, and three things followed that the recommendation would have
preserved: the convention was **already enforced twice over**, making the file
redundant rather than merely unused; `requirements/` and `artifacts/` were dead
in the same way; and the `distilled/` kind list **contradicted `docs/extraction.md`**.

The minimum-change option would have left a schema that misdescribes what an
extraction produces, immediately before 267 records are filled against it.

**Recorded as the finding of this entry:** asking what a thing is *for* found
a defect that asking whether to keep it did not. The model offered a decision
when the question had not been understood yet.

## 5. What the model declined to do

- **Did not fix three prose references to `distilled.md`** —
  `CLAUDE.md:19`, `CONTRIBUTING.md:18`, and **`docs/requirements.md:78`**
  (*"Extraction comes from `distilled.md`, never from `summary.md`"* — a
  normative doc pointing at a file that exists nowhere). They are the other
  half of the same defect and were already stale. Left out because the agreed
  scope was the four companion entries; named in the PR body instead of
  silently folded in.
- **Did not touch `versions/`**, whose open question (`docs/scope.md` §7.1)
  is still unsettled and belongs to library#1.
- **Did not change `bin/`.** The temptation was a validator rejecting a
  `quotes.md` if one appears. Nothing parses `companions:` today, and adding
  the schema's first enforcement point as a side effect of a retirement would
  be a tooling decision smuggled into a documentation change.
