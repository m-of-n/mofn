---
schema: "design-log/v1"
id: DL-0027
part: review
date: "2026-11-06"
---

# DL-0027: review

**Human decision:** accept DEC-001 as `m-of-n` (org, working title) and `mofn`
(repository, package, CLI).

## What the human rejected

- **Leaving DEC-001 open.** The agent's first fix was the cheaper one: correct
  `BACKLOG-0001` T-001 to say DEC-001 is open. The human chose to accept it
  instead. That makes the three earlier "accepted" lines true, rather than
  withdrawing them.
- **All five listed options** (`spki3`, `open-sdsi`, `kofn-certs`,
  `localnames`, `sudsy`). None was chosen. The ADR records reasons for each;
  **the agent wrote them, and the human did not state their own.**
- **`m-of-n` alone**, without `mofn` named as the short form. That option was
  offered and not taken.
- **Proceeding in parallel with mofn#129**, which would have broken the
  one-change rule in `propose-arch`.

## What the agent got wrong in its own draft

Two citations failed checking before commit:

- The ADR first cited `PLAN-0001` §1 for the "we do not inherit SPKI's
  encoding" text and for `legible-provenance`. Both are in §0, the correction
  notice.
- It first listed the `.gitmodules` URL as a rename cost. That URL is relative
  (`../library`), so an org rename leaves it intact. It was removed from the
  cost list.

## What stays owed

- A second reader for `ADR-0006`.
- Written sponsor confirmation of the October delegation (`DL-0021`).
- `src/mofn/__init__.py`'s docstring, at the next change to `src/`.

## Sequencing

mofn#129 was open, approved and conflicting at `ARCH-0001` 0.1.8, so this
change was held until it merged. #129 merged on 2026-11-07 at 0.1.9, so this
change takes 0.1.10. mofn#141 took `DL-0025` in the meantime, so this entry
was renumbered from `0025` to `0027` before it merged. Nothing outside this
change cited the old number.
