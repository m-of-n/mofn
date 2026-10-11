---
schema: "design-log/v1"
id: DL-0009
part: produced
date: "2026-10-10"
---

# DL-0009 — produced

## Artifacts

| file | what |
|---|---|
| `spec/ADR-0002-provisional-principles.md` | ADR at `status: proposed`, `decision_makers: []`, version 0.1.0 |
| `project/DECISIONS-0001.md` (mofn#80) | companion register sync — separate branch, separate PR |

## Shape of the ADR

§1 separates what D-2 granted from what it deferred — the move the whole file
rests on. §2 states the proposed decision and, as importantly, its limits: it
accepts no `DEC-*`. §3 argues the four principles. §4 explains the two held.
§5 lists consequences as *owed work*, not as work done here. §6 gives two
acceptance conditions. §7 records four rejected alternatives. §8 cites evidence.

## Two findings the ADR contributes that were not in D-2

Both arrived from the library after D-2 was taken, and neither is transcription.

**1. P2's evidence is now external.** D-2 accepted P2 on the strength of a
prototype — our own code, demonstrating our own idea, which is the weakest form
of evidence available. Since then the `artifact-statements` and `sbom` topics
found the same hole in two live specifications independently: a vCon has no
speaker and never distinguishes ASSEMBLED from ASSERTED; an SBOM is a B-has-C
payload with no A, in both the NTIA and CISA framings. **Two unrelated
standards, same missing term.** The ADR records this because it changes P2 from
a design preference into an observation about the world, and that is the
difference between a principle and a taste.

**2. Holding P4 now costs something it did not cost on 2026-09-28.** D-2 held
P4 on the grounds that it is the least tested of the six. That reasoning is
untouched. What changed is that `canonical-encoding` makes conditions (5) and
(6) **conditional on P4**, so dropping P4 would restore DEC-002 option 3 to
contention. **P4 has become an input to an encoding decision due Oct 28.** The
ADR does not propose accepting it — the evidence has not improved — but it
states that whoever takes DEC-002 is taking a position on P4 whether or not
they say so. Nothing in the repository said this before.

## The sequencing recommendation

`mofn#72` proposes extending P5 to cover non-canonical serialisation of *known*
content. P5 as drafted speaks to unknown *content*. If P5 is finalised at
today's wording and #72 lands after, a principle accepted one week is amended
the next — against the ADR's own `version_policy`, which says an accepted ADR
changes only by superseding it.

**Recommended: land #72's P5 clause first, then accept this ADR over the
amended P5.** The alternative of accepting P2, P3, P6 now and holding P5 is
recorded in §6 and argued against: P5 is the principle the prototype's
reject-don't-repair behaviour already depends on, so splitting the four leaves
the depended-on one the only one still unwritable-against.

## What was deliberately not produced

- **No edit to `ARCH-0001`.** P6 requires §4.2 to become functions-over-one-form
  and that is register item 4's change, gated on a decision not yet taken.
- **No `status: accepted`, no name in `decision_makers`.** See `review.md` §1.
- **No DEC-\* status change anywhere**, including DEC-007, which P3 arguably
  answers. That is register item 5d and stays open.
