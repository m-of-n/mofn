---
schema: "design-log/v1"
id: DL-0024
part: question
title: "ADR-0002 accepted — P2, P3, P5 as amended, P6"
date: "2026-11-06"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "ADR-0002 1.0.0 accepted; ARCH-0002 0.10.0 (four principles [accepted]); ARCH-0001 0.1.8 (changelog, §4.2 pointer); DECISIONS-0001 0.5.0 (4a closed); BACKLOG T-029d done. No DEC-* touched."
status: open
---

# DL-0024 — question

## The brief

The human (`ndewedo-newbury`) asked how to complete mofn#6 (T-012), read-only.
The agent's answer: close #6 and split it. Its three questions were already
answered elsewhere (P6, MD-1, PROC-0004 §8b), and the first replacement item,
**A — accept or split `ADR-0002`** (register 4a), was the one that unblocks the
others.

The human then asked whether the decisions could be completed in that thread,
and what `ADR-0002` actually accepts. The agent explained that the thread can
hold the deliberation, but only an ADR file accepts a decision (`ARCH-0001` §9).
It set out the two options from `ADR-0002` §6(a), and flagged that the human is
both the v0.7.1 reviewer and the author of P5.1/P5.2, so *as amended* means
accepting their own clauses. It recommended *split* as cleaner.

**The human answered: "accept as amended", and "go".**

## Context supplied

mofn#6 and its comment; `ARCH-0001` v0.1.7; `ADR-0002` v0.1.4; `ARCH-0002`
v0.9.1 front matter and headings; `DECISIONS-0001` v0.4.3 items 4a, 6a and T1-A/B;
`BACKLOG-0001` T-012 and T-029d; `PROC-0004` §8b. All read from `origin/main`
at `724bb4b`.
