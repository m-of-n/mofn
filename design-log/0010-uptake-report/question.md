---
schema: "design-log/v1"
id: DL-0010
part: question
title: "D3 uptake and applications report — adoption evidence, and the SPKI/PICS failure-to-adopt analysis"
date: "2026-10-10"
model: "claude-opus-5"
---

# DL-0010 — question

## What was asked

To complete the *uptake & applications* third of **mofn#37** (D3), owned by
Ndewedo per `PLAN-0003`, and tracked as **T-027** in `BACKLOG-0001` and
**mofn#84**. The ask, in the user's words, was to "complete next steps" after a
first pass had established what a research report contains and filed the
sub-issue.

## Context supplied

The session was given the repository and was pointed at nothing else; the
governing documents were found rather than handed over. In order of weight:

- **`PROC-0004` §3** — definition of done: three reports, markdown, published,
  each citing `library@<commit>`, each carrying `sources.md` **and**
  `searches.md`.
- **`PLAN-0001` §6** — the scope sentence this entry exists to honour: *"Any
  uptake story that does not confront why the last attempt died is not worth
  writing."* Plus §11 (D9), which shares the evidence base.
- **`research/README.md`** — the directory shape and the two rules: every
  source that mattered gets a library record; archive the searches, not just
  the findings.
- **Survey R-001**, merged, 2,162 lines, 155 citations resolving to library
  records. **D-4** (Sep 28) directs each D3 report to start from it;
  nymble's comment on #37 maps §5–§8 to this report specifically.
- The existing reports as worked examples — `R-0002` for register and scale,
  `R-0001` for the `unverified.md` publication gate.

## The question actually being answered

R-001 §5–§8 already contains the structural analysis of why SPKI and PICS
failed. If this report restates it, it is a copy, and nymble's comment is
explicit that *"Adapting and extending R-001 is legitimate. Copying it isn't,
because each report has to answer its own question."*

So the question had to be one R-001 does not answer:

> **What separates the ancestors that failed from the descendants that are
> being adopted now — and does this project's design sit on the failing side
> of that line?**

Two sub-questions followed from it, and both had to be answered with evidence
R-001 does not contain:

1. **How far has adoption actually reached?** R-001 §6.7 carries an explicit
   sourcing note that C2PA platform and newsroom adoption "could not be
   established from primary sources in this pass." Clearing that was the
   report's first job.
2. **Which failure modes does this design still carry?** `PLAN-0001` §6
   requires the report to confront this. It is the half that makes the report
   worth writing and the half most likely to be softened, so it was scoped as
   the payload rather than the conclusion.

## Constraints taken as binding

- **No decision may be closed.** DEC-001…DEC-005 and DEC-007 are open; nothing
  in the report may read as selecting an encoding, a tag language or an
  envelope, and no `DEC-*` may be marked accepted outside an ADR.
- **No parallel architecture document** (ARCH-0001 §9.4). The report is input;
  anything that should change the architecture goes through `propose-arch`.
- **"Artifact" is a normative term** (`ArtifactId`, `ArtifactStatement`,
  R-M-07) and is not used for files, documents or build outputs.
- **No third-party bytes committed.** The C2PA deployment guidance is a PDF;
  digest and locator only.
- Work in a worktree (`bin/wt new report/0004-uptake`), never on `main`, never
  inside `library/`.
