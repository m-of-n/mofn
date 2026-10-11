---
schema: "design-log/v1"
id: DL-0009
part: question
title: "ADR-0002 — writing the instrument D-2 deferred, without taking the decision it reserved"
date: "2026-10-10"
model: "claude-opus-5"
human: ndewedo-newbury
outcome: "spec/ADR-0002-provisional-principles.md at status: proposed, decision_makers empty. Companion to mofn#80 (DECISIONS-0001 v0.2.0). No DEC-* accepted; ARCH-0001 untouched."
status: open
---

# DL-0009 — question

> **Numbering.** On `main` the design log stops at `0006`. Three unmerged
> branches already claim `0007` twice (`0007-library-harness-role`,
> `0007-rejecting-decoder-spike`) and `0008` once. `DL-0006` resolved the same
> collision "by `main` rather than by this entry" — last to land renumbers.
> This entry takes **`0009`** to add no further pressure to a number already
> contested twice. **The underlying defect is unfixed: design-log ids are
> allocated per branch with no reservation, so parallel lanes collide by
> construction.** Third occurrence. Proposed as a register item in §4 of
> `review.md`.

## The question asked

The session began as an audit — *where do `mofn` and `library` not align, what
has already been answered and not written down* — and turned on a correction
from the human:

> *"tell me if there are issues for the first four items seeing as i am owner
> of the repo also. Some of the decisions have been made and the sponsor hasn't
> had time to update mofn"*

That reframes the whole task. The audit had assigned four items to the sponsor
on the grounds that `CODEOWNERS` puts `/spec/` and `/project/` on `@nymble` and
`PLAN-0003` gives him ADR acceptance. The human is also an Owner, so the
assignment was wrong in a specific way: **it confused merge authority with
decision authority, and then used the first to gate work that needed only the
second — which had already been given.**

## Context supplied

- `ARCH-0001` v0.1.1, unchanged since 2026-09-21; `ARCH-0002` v0.5.0, all of
  P2–P7 `[draft]`; `ADR-0001`, accepted.
- `project/meetings/2026-09-28.md` — D-1 … D-7, committed, with D-2 the one at
  issue.
- `DECISIONS-0001` v0.1.0, eighteen days behind that meeting.
- `CONTRIBUTING` §5, `CLAUDE.md`'s "Never" list, `PLAN-0003` owners table.
- The three `answered` library topics and the FX-1 design notes that cite `D-3`.

## What was asked for

Two of five proposed items, selected by the human: **C2**, the register sync
(shipped as mofn#80), and **C3**, this ADR. **C1 (splitting the ARCH-0001
v0.2.0 proposal), C4 and C5 were not taken** — see `review.md` §2.

## The constraint that shaped the output

A rule, derived in-session and then applied rather than assumed:

> **A decision the sponsor already made, in a committed artifact, is not his to
> make twice. Writing it down is transcription, not deciding.** Test: is there a
> committed artifact where he already decided this? If yes — transcribe, cite it
> by id and date, merge. If no — draft `status: proposed`, `decision_makers: []`.

Applied to D-2, that rule **splits**, and the split is the entire content of
this ADR: D-2 *granted* provisional standing (transcribable, and recorded
nowhere until now) and *deferred* finalisation to "an ADR after review"
(not transcribable — it is the step D-2 reserved).
