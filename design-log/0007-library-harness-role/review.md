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
2. **"Distillation is deliberately rare."** The model asserts that a stub is a
   legitimate resting state and that FX-1 is reserved for documents we build
   against. `library/docs/extraction.md` says FX-1 applies to every in-scope
   record *a pull request moves past stub*, which is consistent — but the
   README now makes the rarity sound intended rather than incidental. **If the
   intent is that all 203 in-scope records eventually reach `profile: full`,
   this sentence is a misstatement and must come out.**
3. **The corrected shape line.** `distilled.md`, `quotes.md` and `artifacts/`
   appear in no record. Confirm they are abandoned rather than planned, since
   two files now say so in both repos.
4. **Leaving FX-1's scope untouched** while publishing the figures that
   question it (203 in-scope, 118 stub, ~37% of record bytes in four
   extractions).

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
