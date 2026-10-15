---
schema: "design-log/v1"
id: DL-0012
part: question
title: "R-0005 and R-0006 — writing two D3 reports as synthesis, and saying so"
date: "2026-10-14"
model: "claude-opus-5"
human: ndewedo-newbury
outcome: "research/0005-context/ and research/0006-mechanism/, each with report.md + sources.md + searches.md. BACKLOG T-025, T-026 → review. Library pin moved 31aabab → f57dcbc. No DEC-* decided."
status: open
---

# DL-0012 — question

> **Numbering.** `main` holds `0001`–`0010` with `0007` twice; `0011` is taken
> by the P5 branch (#97), which is open and unmerged. This entry takes `0012`.
> **Fifth occurrence of the collision DL-0009 §4 raised** — ids are still
> allocated per branch with no reservation.

## The question asked

Verbatim:

> *"complete this: D3's three reports are 1 of 3 done, due today. T-027 (uptake)
> landed as R-0004 (#87). T-025 (context) and T-026 (mechanism) are not started,
> and T-026 is the evidence base for DEC-002 — so D5 (Oct 28) cannot close
> without it."*

The framing came from the model's own earlier status summary, which the human
was quoting back as an instruction. Two reports, both `L` (~3 days each), both
owned by S1 in the backlog, both due **today**.

## Context supplied

`PROC-0004` §3 (the three-report scope); `BACKLOG-0001` T-025/T-026;
`research/README.md` (the two rules); `R-0004` as the house form; survey
**R-001** §§1–6, §9, §11, §12; `library@f57dcbc` —
`topics/canonical-encoding.yaml` and `records/ietf/rfc-9804/distilled/design-notes.md`
in full; `design-log/0007-rejecting-decoder-spike/`; library#46; `ARCH-0001`,
`ARCH-0002` v0.6.0, `ADR-0002`, `PLAN-0001` §13, `project/meetings/2026-09-28.md`.

## What the question did not settle

**1. Is a synthesis pass an acceptable D3 report?**

`BACKLOG-0001` scopes both tasks as drafts from existing material — T-025
*"draft from survey R-001 §1–§3 (MD-4)"*, T-026 *"R-001 §2/§4, plus the RFC 8785
R-O-05 analysis in library#46"*. So the backlog says yes. But
`research/README.md` carries two rules learned the hard way, the second of which
is *"Archive the searches, not just the findings"*, and `PROC-0004` §3 requires
`searches.md` for each report.

A `searches.md` for a pass that ran no searches is either an embarrassment or a
finding, depending on whether it is written honestly. The model took the second
reading. See `review.md` §2.

**2. Which library pin?**

The evidence base for R-0006 — RFC 9804's FX-1 extraction and the RFC 8785 pass
that library#46 landed — **does not exist** at the pin on `main` (`31aabab`).
It exists at `f57dcbc`, which was sitting **unstaged** in the working tree.
Moving the pin was a precondition for writing T-026 at all. See `produced.md`
§1.

**3. How much of MD-3 to restate.**

R-0006 is *"the evidence base for DEC-002"*, and the evidence postdates both
MD-3's narrowing and the sponsor's 2026-09-16 retirement of option 1. A
mechanism report that scored only option 5 would be useless; one that
recommended option 1 would be taking a decision. §3.9 of the report is the
resolution and is the most carefully worded section in either file.
