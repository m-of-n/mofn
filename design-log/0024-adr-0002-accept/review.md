---
schema: "design-log/v1"
id: DL-0024
part: review
date: "2026-11-06"
---

# DL-0024 — review

**Human decision:** accept `ADR-0002` with **P5 as amended**.

## What the human rejected

**The agent's recommendation.** The agent recommended *split*: accept P2, P3,
P6 and P5 as drafted on 2026-09-22, and hold P5.1/P5.2 for a reader who did not
write them. It gave two reasons. First, the decision maker would be accepting
clauses they wrote. Second, the delegation they decide under was given verbally
and is unconfirmed in writing (`DL-0021`). **The human overruled it** and chose
*as amended*.

The record does not show the human's own reasoning; they gave none in the
thread. `ADR-0002` §9 lists the case for *as amended* that already stood in the
ADR: `SPEC-0002` already states P5.1's rule normatively; P5.1 rests on the
mofn#73 measurement; and splitting P5 leaves it the one principle still
unwritable-against. Those reasons were assembled by the agent from the existing
text. They are not attributed to the human.

## What stays owed

- A second reader for P5.1 and P5.2. Not a condition of acceptance; a defect
  found later is fixed by a superseding ADR.
- Written sponsor confirmation of the October delegation (`DL-0021`).
- Register item 4: the `ARCH-0001` §4.2 rewrite in v0.2.0. Register 5d:
  DEC-007 re-stated in P3's terms.

## Sequencing

Open PR mofn#129 also bumps `ARCH-0001` to 0.1.8. Whichever merges second
rebases and takes 0.1.9.
