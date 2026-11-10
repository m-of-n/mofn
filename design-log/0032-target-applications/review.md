---
schema: "design-log/v1"
id: DL-0032
part: review
date: "2026-11-09"
---

# DL-0032 — review

**Human verdict:** pending (PR review).

## What the agent rejected, and why

- **A new top-level section.** "§11 Target applications" would leave §1–§10
  numbered as they are, but it would sit after the references. Inserting it
  as §3 would renumber §3–§10, and §9 (the amendment protocol) and §4.3 are
  cited by number across the repository. Chosen: **§2.3**, under Goals, which
  is where scope already lives (G5, NG1…5) and which renumbers nothing.
- **Archives examples as prose only.** There was no archives vector. UC-3 was
  prose, and the issue's definition of done asks for vectors or a reason.
  Writing DV-3 and TV-21…26 is more work, but "illustrative" would have left
  the second target, the one that carries the generalisation claim, with no
  evidence at all.
- **Reusing DV-1 for the library.** That would show one vocabulary used twice,
  not two vocabularies through one renderer. DV-3 has its own definer (Dave)
  and its own types.
- **Dropping the `locator` attribute when the engine refused it.** TV-26 is the
  only example of `SPEC-0002` 0.6.0's rule that a locator rides as an attribute.
  The engine was widened instead (text assignments, wallet 0.3.0); text
  *ranges* stay unsupported.
- **Marking SC-3 as a vector.** TV-9 and TV-6 encode, but nothing computes or
  declares the two-of-three approval answer. It is marked illustrative with that
  reason rather than given an answer nothing checks.

## Found, not fixed

- **A description target renders as "a described object".** `SPEC-0003` §10
  says how to render values, not a type-6 subject. T-066.
- **§2.3.1 is not the supply-chain profile** that `DECISIONS-0001` T1-B wants
  before P7 can be accepted. A profile would say which types, templates and
  anchors a conforming supply-chain wallet must hold. Stated in §2.3 so that it
  is not mistaken for one.
