---
schema: "design-log/v1"
id: DL-0013
part: question
title: "P5.1 and P5.2 — amending a draft principle so the instrument above it can be accepted"
date: "2026-10-13"
model: "claude-opus-5"
human: ndewedo-newbury
outcome: "ARCH-0002 v0.7.0 (P5.1, P5.2) + ARCH-0002-CHANGELOG.md (new) + ADR-0002 v0.1.2 + DECISIONS-0001 v0.3.2 + BACKLOG-0001 v0.12.0. Closes mofn#72. No DEC-* accepted; ADR-0002 stays proposed."
status: open
---

# DL-0013 — question

> **Numbering — and this entry is now the proof.** It was written as `0011`.
> While it sat in review, `main` merged **`0011-dco-merge-commits`** (#95), and
> this lane's own later branch took `0012` (#103). Renumbered to **`0013`** on
> rebase, 2026-10-15.
>
> **Sixth occurrence of the defect `DL-0009` §4 raised**, and the first where a
> *merged* entry and an *open* one both had to be stepped around. Ids are still
> allocated per branch with no reservation, so parallel lanes collide by
> construction and the loser renumbers after review has already started.

## The question asked

Verbatim, after a scoping answer about the repository's purpose:

> *"start with T-029d and T-029e and then ask me about dec-002"*

Two overdue backlog rows, both owned by the model, both from the action list of
the weekly of 2026-09-28. No further direction was given, and in particular
**no direction was given about how to read T-029d's wording**, which is where
the work actually turned.

## Context supplied

`CLAUDE.md`; `README.md`; `ARCH-0001` in full (per the `propose-arch` skill);
`ARCH-0002`; `ADR-0002`; `DECISIONS-0001`; `BACKLOG-0001`;
`project/meetings/2026-09-28.md`; `PLAN-0001` §1–§3; `PLAN-0002` front matter
and §2; `library/topics/canonical-encoding.yaml`;
`design-log/0007-rejecting-decoder-spike/`; `mofn#72` and `mofn#73` via `gh`.

## What the question did not settle, and the model had to decide

**1. T-029d says "accept P2, P3, P5, P6 provisionally (MD-2)". Is that an
instruction to accept?**

Read literally, yes. Read against the record, no — and the record wins. MD-2
*already* granted provisional standing on 2026-09-28; there is nothing left to
grant. What the row actually names is the **instrument** MD-2 deferred, and
MD-2's own condition was that each principle becomes final "only through an ADR
**after review**." The review has not happened. So the row cannot be closed by
the model at all, and the only honest question was *what is left between here
and a human being able to close it.*

**2. Is `mofn#72` in scope for a task that does not mention it?**

`ADR-0002` §6(b) names it as a sequencing prerequisite — *"land #72's P5 clause
first, then accept this ADR over the amended P5."* Doing T-029d without it means
either accepting P5 at a wording known to be about to change, or splitting the
four principles. Both are rejected in `ADR-0002` §6 and §7. The model judged #72
in scope **as the blocker**, not as an adjacent improvement, and flags the
judgement here because it is the one place the work exceeded the literal ask.

**3. Which way does the DSSE collision resolve?**

`mofn#72` states the collision and explicitly declines to resolve it: *"Either
is defensible; the silence is not."* Choosing is the work. See `produced.md` §3.
