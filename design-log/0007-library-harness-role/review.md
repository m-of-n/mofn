---
schema: "design-log/v1"
id: DL-0007
part: review
title: "What the library is for — the harness framing, and the one-way bears_on edge"
date: "2026-10-09"
model: "claude-opus-5"
human: "pending"
outcome: "no human review yet"
status: open
---

# DL-0007 — review

No human review yet. Nothing here is accepted.

A reviewer should accept or reject these separately:

1. **The framing itself.** "The evidence layer the specification cites, not a
   bibliography appended at the end." This was supplied by the sponsor in the
   question and written up, not derived. If it is wrong, both READMEs are wrong
   in the same way.
2. **"Distillation is deliberately rare."** ✅ **Resolved, and the model had
   the rule wrong.** The first draft said FX-1 applies to every in-scope record
   *a pull request moves past stub*. That is the **pre-amendment** rule.
   `docs/extraction.md` was amended 2026-10-03 (#8, PR #42) and the trigger is
   now the **intent to extract** — `status: distilled`, a declared
   `distillation` block, or a PR that changes `distilled/`.
   `bin/check-pr-extraction` enforces exactly those three and prints which bar
   each touched record was held to. So the rarity is **designed**, not
   incidental, and the corrected README says so. Fixed on library#61.
3. **The corrected shape line.** `distilled.md`, `quotes.md` and `artifacts/`
   appear in no record. Confirm they are abandoned rather than planned, since
   two files now say so in both repos.
4. **Leaving FX-1's scope untouched** while publishing the figures that
   question it (203 in-scope, 118 stub, ~37% of record bytes in four
   extractions).

## Where the wrong rule came from

`library/CLAUDE.md` **in the `mofn` submodule** still carries the
pre-amendment sentence — *"Every `rfc` / `draft` / `spec` / `ietf` record a PR
moves past stub must reach `distillation.profile: full`"*. The copy on library
`main` was corrected with the amendment. The pin is 11 commits behind, so a
session rooted at `mofn/` loads the **stale** file as project instructions and
has no way to know.

This is the same hazard as the miscounted census in `question.md`, with a
sharper edge: a wrong *count* looks like a number and invites checking, while a
wrong *rule* reads as authority. Both came from the pinned submodule in one
sitting.

## The open item this produced

The one-way `bears_on` edge is **not fixed** and no backlog entry was created
for it — creating one is a scope call. A reviewer deciding it matters should
file it against `mofn`: *nothing in `spec/` cites a `<record>#R-NNNN` id, so
FX-1 output is currently write-only.*

## Process note

The first census was run against `mofn/library`, the pinned submodule, and was
**wrong** — 280 records and one `distilled/` directory, against the real 304
and five. It was caught only because the pin was checked against the standalone
clone. This is the third incident traceable to working from the submodule
checkout (cf. library#12). The existing rule in `CLAUDE.md` says never *commit*
inside `library/`; this case says the submodule is also not safe to **read
facts from**, and the rule may need widening.
