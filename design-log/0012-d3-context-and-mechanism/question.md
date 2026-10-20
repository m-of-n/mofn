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

---

## The second question, 2026-10-16

> *"complete #103 … #103 is the open item. It needs more than conflict
> resolution: R-0006 is the DEC-002 evidence base, and ADR-0003 D2 landed an
> accepted decision fixing one canonical encoding while explicitly not accepting
> DEC-002. Sections 3.9 and 6 of that report are now describing a world that
> moved."*

**What it supplied:** the diagnosis. That D2 is accepted, that it fixes one
canonical encoding, that it declines DEC-002, and that §§3.9 and 6 are the two
sections affected.

**What it did not settle, and the model decided:**

- whether anything *else* in the two reports had moved — §§3.2, 3.10, 3.12, 5.2,
  7 and 8 had, and three claims in them were outright wrong (`produced.md` §7.2);
- whether to look past the two named sections at all. Doing so is what turned up
  §3.13, which was not asked for and is the most consequential thing in the
  change;
- what to do about a defect found in an accepted specification. The model chose
  to state it, cite it line by line, and not propose the diff (`review.md` §4).

**Still not settled, by anyone:** whether a research report is the right vehicle
for §3.13's finding, or whether it should be an issue against `SPEC-0002` with
only a pointer in the report. `review.md` §6 puts that to the reviewer.

## The third question, 2026-10-17

*"Complete issue #100."* Asked with nothing else. #100 is T-026's issue, and
its definition of done has eleven boxes. PR #103's body had already said #100
would stay open after merge, because R-0006 lacked the first box: the
comparative anatomy.

**What the question did not settle, and the model decided:**

- **What to do with cells the library cannot fill.** The model chose to print
  them as ∅ and register them. Filling them from general knowledge was the
  alternative. `review.md` §8 gives the reasons.
- **Whether to number the new material so as to keep v0.2.x's sections.** It
  did: the anatomy went into §2 as subsections, and §3–§8 keep their numbers.
  R-0005, this design log and PR #103 all cite them.
- **Whether the accepted core belonged in the DEC-004 evidence at all.** #100
  does not mention `SPEC-0003` or `SPEC-0004`. Reading them is what produced
  §4.6.
