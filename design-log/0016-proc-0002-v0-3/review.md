---
schema: "design-log/v1"
id: DL-0016
part: review
date: "2026-10-29"
---

# DL-0016 — review

**Status: human review PENDING** on the PR. PROC-0002 stays `status: draft`,
`needs_review: true`, `reviewers: []` — the model does not fill them (§6, the
rule this change adds).

## For the reviewer to decide

- **The stage 8 reversal is the substantive change.** It narrows what the
  sponsor asked for on mofn#18 (*"agent run to create python or C code"*). If
  the sponsor meant a from-scratch primitive deliberately, as a teaching
  exercise kept in `prototype/`, that is a guardrail exception and must be
  written as one — not left implicit in a process doc.
- **`harness/` is a library layout name proposed from mofn.** The library owns
  its record layout; it should be confirmed there (library `docs/`) before any
  stage 8 code is written.
- **The two DL-0009 rules now bind agents.** DL-0009 asked that they be
  reviewed before binding anyone; this PR is that review.

## Rejected by the model, before any file was written

- **Reporting "mofn#18 is already done, nothing to do."** True of the PR, but it
  would have left three contradictions with main standing (the primitive
  guardrail, the normative term, the stale `src/` clause) and a closed question
  still marked open.
- **Editing DECISIONS-0001** to annotate rows 7/14/15/16. mofn#119 has it open;
  the pointer was put in PROC-0002 instead.
- **Answering §8.2–8.7.** They are the sponsor's; the register carries them.
- **Reading local `main`** (20 behind). Worked from `origin/main` throughout.

## Accepted / rejected by a human

*Pending — fill on review. Record rejections and why.*
