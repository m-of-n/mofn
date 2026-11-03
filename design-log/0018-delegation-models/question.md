---
schema: "design-log/v1"
id: DL-0018
part: question
title: "D3, library L-040 — delegation and trust compared across X.509, S/MIME, OpenPGP and SDSI/SPKI (`R-0007`)"
date: "2026-11-01"
model: "claude-opus-5-5"
---

# DL-0018 — question

**Written after the fact, on 2026-11-01.** The work ran on 2026-10-26 and
2026-11-01. This entry was reconstructed from the session transcript, not from
memory, but it was not written in the same change as the report. `review.md` §5
says what that cost.

## What was asked

library#14 (L-040), quoting the sponsor on 2026-09-22, asks for a research
report comparing delegation and trust in X.509, S/MIME, OpenPGP and SDSI/SPKI.
It fixes one case as the constant (Alice trusted for `*@foo.com`, delegating to
Bob, Bob attesting Carol), a table to fill in, and five questions.

The session's four instructions, verbatim:

1. *"tell me what is necessary in order to close issue library#14"*
2. *"do what is still needed to close it"*
3. *"what is the work requiring pgp?"*
4. *"complete whatever is necessary to merge #118"*

Between 1 and 2, the model had said the report's location was the user's to
pick. Instruction 2 did not pick. The model chose (`review.md` §1).

A fifth request, relayed on 2026-11-01, asked for this entry, because mofn#118
had none.

## Context supplied

The session was pointed at the issue and nothing else. The governing material
was found in the repositories:

- **The issue**, including its last section: the claim that scoped delegation
  with a decentralised tagging language is *"poorly served by all of these"*,
  and that it *"is only worth making if the comparison is honest"*.
- **The library's `delegation-models` topic** (library#29, #55), whose answer
  already held most of the report's draft findings.
- **The FX-1 records** of library#64: `rfc-2692`, `rfc-2693`, `rfc-5280`,
  `rfc-8551`, `rfc-9580`, `rfc-9804`.
- **Reports R-001, R-0002 and R-0005**, and `ARCH-0001`, `SPEC-0003`,
  `SPEC-0004`, `UC-0001` for the "ours" row.
- **`research/README.md`** in both repositories, for where a report lives.

## The question actually being answered

The issue states that the differences lie in delegation and in where trust
starts. Its table implies that scoping is what separates the project from the
rest. So the question taken up was the sharper one:

> **Is scoped delegation actually what separates these systems, and does the
> project's claim survive when each one is made to express the same case in its
> own syntax, including the cases that must fail?**

## Constraints taken as binding

- **No decision may be closed.** No `DEC-*` marked accepted. Spec defects found
  go in as proposals, not edits.
- **The topic answer is a starting hypothesis**, not a conclusion (report §1).
- **The `unverified.md` publication gate**, inherited from R-001.
- **No third-party bytes committed.** Sources by digest and locator.
- **"Artifact" is a normative term** and is not used for files.
- **Never work inside `library/`.** Record changes went through the library
  repository, in their own PR (library#94).
