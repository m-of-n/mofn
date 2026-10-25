---
schema: "design-log/v1"
id: DL-0014
part: question
title: "mofn#112 — does each decision's current text survive the CBOR/COSE extraction?"
date: "2026-10-23"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "ARCH-0001 v0.1.3 (§7 DEC-002/DEC-003 ADR inputs), ARCH-0002 v0.8.0 (P1.1, draft), ARCH-0001-PROPOSAL rev.5 (option 5 pins map order). No DEC-* accepted, ranked or withdrawn."
status: open
---

# DL-0014 — question

## The question asked

Two turns, in order:

1. *"are mofn#112 and mofn#110 related in some way, do the issues overlap in
   any sort?"* — answered in chat and then, at the human's direction ("complete
   next steps for me"), as cross-link comments on both issues. The model drafted
   them; the auto-mode classifier refused the `gh issue comment` write and the
   **human posted them**.
2. *"now complete #112"*.

## The context supplied

mofn#112 is the library's handover of the CBOR/COSE extraction (library#39,
library PR #88, 23 records at `profile: full`). Its framing, which the issue
asks to keep: each checkbox is *"check whether this decision's current text
survives this finding"*, **not** *"this decision is wrong"*.

The model read, in this order: `ARCH-0001` in full (per `propose-arch`), the
v0.2.0 proposal in full, `DECISIONS-0001` Tier 1, `ADR-0003`, `SPEC-0002`
§4–§6 and §8.6/§9, `ARCH-0002` P1 and P5.2, `ADR-0001`, and the `rfc-8747`
record at library `bafd536` — the pin mofn#113 proposes, because the pin on
`main` (`022af11`) still holds these records at `status: fetched`.

## What "complete" could and could not mean

The instrument that would close DEC-002 or DEC-003 is an ADR, and an agent may
not write or accept one (`CLAUDE.md`, `propose-arch` hard stops). So
"complete" was read as: **give every checkbox a verdict against the governing
text, and put each verdict that needs text into the architecture document**,
not into the PR body or the issue.
