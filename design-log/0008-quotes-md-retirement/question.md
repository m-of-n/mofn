---
schema: "design-log/v1"
id: DL-0008
part: question
title: "quotes.md and the pre-FX-1 companion vocabulary — what the schema still described"
date: "2026-10-09"
model: "claude-opus-5"
human: "pending"
outcome: "library#63 — record schema v0.7.0, summarize skill, summary template, construction.md decision 6. No ADR. No DEC touched. FX-1 unchanged."
status: open
---

# DL-0008 — question

## Context supplied

Follow-on from [`DL-0007`](../0007-library-harness-role/question.md), in the
same session. That entry corrected the FX-1 trigger and flagged, in passing,
that `.claude/skills/summarize/SKILL.md` directs a summariser to write a
`quotes.md` that no record holds — with 267 scaffolds due to be filled through
that skill.

## Questions posed, in order

1. *"what is quotes.md supposed to specify, what is the convention it holds?"*
2. *"what changes need to be made in order to complete the latter option"* —
   the latter of two framings offered: **retire the file and make the locator
   substitute official**, rather than keep it as the non-FX-1 vehicle.

The first question is the one that mattered. It was asked **instead of**
accepting a recommendation, and it changed the answer.

## What the first question turned up

The model's initial framing was *"is `quotes.md` real or abandoned?"* — a
disposal question. Reading the original schema showed that to be the wrong
shape. `797ef06` (2026-09-16) introduced it as **half of a deliberate pair**:

```yaml
companions:
  distilled.md: {required_at_status: distilled, note: "our summary: what it says, why it matters here"}
  quotes.md:    {required: false, note: "verbatim excerpts WITH locators, for citation"}
```

Two companions split by **voice**: our words about the source, and the
source's own words with a locator. Not a feature that failed — a convention,
stated once and never given a template, a validator or a single user.

| | |
|---|---|
| records holding `quotes.md` | **0 of 304** |
| specification it carries | `required: false` + a one-line note. No template, no structure, no check beyond the universal front-matter rule |
| what enforces the convention instead | locators cited in `summary.md`; `distilled/normative.md` under FX-1, where the verbatim check reaches it |

So the discipline is alive and observed; only the file is unused.

## What the question exposed beyond itself

Auditing every reference to `quotes.md` showed it was not an isolated stub.
The `companions:` block still describes the library **as it was before FX-1**:

| entry | state |
|---|---|
| `quotes.md` | 0 records; convention absorbed elsewhere |
| `requirements/` | 0 records; duplicates `distilled/requirements.yaml`; note derives it from `distilled.md`, a file in no record |
| `artifacts/` | 0 records; duplicates `distilled/code\|schema\|examples` |
| `distilled/` artifact kinds | lists `fields.yaml`, `state-machines.md`, `code/` — the **old `docs/distillation.md` vocabulary**, not FX-1's eight kinds |

The fourth is the consequential one: **the schema and `docs/extraction.md`
disagreed about what a `distilled/` contains**, and the schema is what an
extractor reads. It is the same mismatch already recorded on library#45
against `draft-ietf-vcon-vcon-core-04`, found there as a symptom and here at
its source.

## Checked before answering

`grep` for every `quotes.md` reference (6 on `main`); `git log -S` to the
introducing commit; whether any tool parses `companions:` (**none does** —
`bin/validate` never reads it, so the block is documentation and carries no
tooling risk); and the two written records that declare its absence.
