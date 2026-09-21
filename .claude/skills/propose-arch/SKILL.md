---
name: Propose an architecture change
description: Use when something should change in ARCH-0001 — a new requirement, an amended decision, a citation correction — or when a DEC-* looks ready to accept.
---

# Propose an architecture change

`spec/ARCH-0001-authorization-attestation.md` is the source of truth and §9 is
its amendment protocol. Follow it exactly; it is what keeps concurrent work from
diverging.

**Never write a parallel essay.** §9.4 forbids it. Propose a diff against the
file.

1. **Read ARCH-0001 first, in full.** Not the summary, not the plan. Proposals
   that restate what is already there are the common failure.
2. **Decide which you are doing:**
   - *Additive clarification* → edit in place, MINOR bump, changelog line.
   - *Substantive proposal* → a `spec/ARCH-0001-PROPOSAL-vX.Y.Z.md`, `type:
     proposal`, `status: proposed`, `reviewed: false`, `iteration_of: ARCH-0001`.
   - *Accepting an open decision* → `bin/new-doc ADR <slug> "<title>"`, then a
     changelog line, then set that DEC's status in ARCH-0001 pointing at the ADR.
3. **A proposal states what it is not proposing.** Omissions must read as
   decisions, not oversights.
4. **Every proposed requirement gets an id and a priority** — `R-M-*`, `R-O-*`,
   `R-I-*`, `R-D-*`, Must/Should/Could — and says which existing requirement it
   extends or conflicts with.
5. **Every proposed decision gets an acceptance test.** "What evidence would
   settle this?" If you cannot write one, it is an opinion, not a decision.
6. **Version and `updated` change together.** §9.5, enforced by
   `bin/validate-archdoc`.

## Hard stops

- **Nothing is accepted without a human.** An agent never sets a DEC to
  `accepted`, never sets `reviewed: true`, never writes an ADR unprompted.
- **One architecture change in flight at a time.** Serialize. Two concurrent
  branches touching the model produce exactly the divergence §9.4 exists to
  prevent — check for an open PR touching `spec/` before starting.
- If a proposal contradicts §4.3 or §5 of ARCH-0001, **the existing text
  governs and the proposal is wrong.** Say so and stop.

Write a `design-log/` entry for anything an agent drafted, including what a
human rejected.
