---
schema: "design-log/v1"
id: DL-0015
part: question
title: "Recording DEC-002 and DEC-003 as accepted ADRs, under a delegation taken the same day"
date: "2026-10-25"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "ADR-0004 (DEC-002, option 5) and ADR-0005 (DEC-003, kid) at status: accepted, reviewed: false. ARCH-0001 v0.1.5, SPEC-0002 v0.2.0, ARCH-0002 v0.9.0, DECISIONS-0001 v0.4.0. Stacked on mofn#116 (the delegation)."
status: open
---

# DL-0015 — question

## The questions asked

1. *"what is meant to go into the DEC-002/3 ADRs, I am also a code owner and
   thus can do it myself."* — answered in chat with an outline per ADR, which
   flagged that code ownership is merge authority, not decision authority.
2. The human consulted the sponsor, who said the human could **add themselves
   to `decision_makers` or remove the field entirely**, whichever is cleanest.
   *"If that is acceptable, make those changes and then we can proceed with
   answering certain decisions."* → mofn#116.
3. The model put **four decisions** to the human as a structured question, each
   with a recommended option first. The human chose all four recommendations.

## The four decisions, as put

| question | options offered | chosen |
|---|---|---|
| DEC-002 — native encoding | option 5 · option 1 · option 2 · not yet | **option 5** |
| DEC-003 — equal key bytes under two suites | registry rule · suite in preimage · DS-label prefix | **registry rule** |
| DEC-003 — `kid` digest | fixed SHA-256 · per suite | **fixed SHA-256** |
| ARCH-0002 P1.1 — disagreeing foreign `kid` on import | reject · report and keep | **reject** |
