---
schema: "design-log/v1"
id: DL-0008
part: review
title: "quotes.md and the pre-FX-1 companion vocabulary — what the schema still described"
date: "2026-10-09"
model: "claude-opus-5"
human: "pending"
outcome: "no human review yet"
status: open
---

# DL-0008 — review

No human review yet. Nothing here is accepted. The scope decision — *"all
four, branch off #61"* — was the human's; the judgements inside it were not.

A reviewer should accept or reject these separately:

1. **Retiring `quotes.md` at all.** The argument is that its convention is
   enforced more strictly in `distilled/requirements.yaml` and observed via
   locators everywhere else. **The gap in that argument is the 101 non-FX-1
   records** (`paper`, `web`, `dataset`) which will never have a `distilled/`.
   For a contested claim in a paper there is now no place for a verbatim
   excerpt with attribution. Decision 6 names this as the trigger to reinstate
   — a reviewer should decide whether it is already true rather than
   hypothetical.
2. **Removing `requirements/` and `artifacts/`.** Both unused, both duplicated
   by `distilled/` entries. The risk is that one of them was a *plan* rather
   than a leftover. Nothing in the repo says which.
3. **Rewriting the `distilled/` artifact kinds.** This is the one with reach:
   it changes what the schema tells a future extractor to produce. It now
   defers to `docs/extraction.md` rather than restating it — deliberately, so
   the two cannot drift again — but that makes the schema less self-contained.
4. **Promoting `rfc-9943`'s sentence to a rule.** It was written for one
   record. It is now the library's stated position on attribution.
5. **Schema v0.6.0 → v0.7.0.** Removing three companion entries is arguably
   breaking for anyone outside this repo consuming the schema. The library is
   standalone and citable by design, so "nobody else uses it" is an assumption,
   not a fact.

## The item that needs a decision, not a tick

`docs/requirements.md:78` still reads *"Extraction comes from `distilled.md`,
never from `summary.md`."* That document is **normative** and names a file that
exists in no record and, after library#63, in no part of the schema. It was
stale before this change. It is the most misleading of the three references
left behind, because a reader following it writes the wrong artifact.

## Process note

The model recommended the wrong option and was corrected by a question rather
than by an instruction — see `produced.md` §4. Worth recording because the
failure mode is not a factual error: the recommendation was defensible on what
had been read, and wrong because not enough had been read. Offering a ranked
decision made it look settled.

This is the **third** finding in two entries traceable to reading the pinned
`mofn/library` submodule rather than the standalone clone
([[DL-0007]] records the other two). Not causal here, but the pattern holds:
every error in this session came from answering before reading the source.
