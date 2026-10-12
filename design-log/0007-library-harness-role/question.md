---
schema: "design-log/v1"
id: DL-0007
part: question
title: "What the library is for — the harness framing, and the one-way bears_on edge"
date: "2026-10-09"
model: "claude-opus-5"
human: "pending"
outcome: "README.md in both repos; library CLAUDE.md shape block corrected. No ADR. No DEC touched. FX-1 unchanged."
status: open
---

# DL-0007 — question

## Context supplied

A session rooted at `mofn/library` — the submodule, pinned at `31aabab`,
**11 commits behind** library `main` at `4857223`. No spec text was in scope.

## Question posed

Verbatim:

> What is the purpose of all the records having distilled/ directories? I want
> to remind you that the library's purpose is to act as a library part of a
> project harness. Perhaps that should be put into the README.md of both this
> repo and `mofn/`.

Two things, one implicit:

1. **A question** — what is `distilled/` for?
2. **A correction** — the framing offered ("library part of a project harness")
   was supplied as a reminder, i.e. as something the repos should already say
   and do not.
3. **Implicit**: the question presupposes *all* records have a `distilled/`
   directory. The presupposition is false and that is itself the finding.

## What was checked before answering

| check | result |
|---|---|
| records with `distilled/` | **5 of 304** — RFC 8949, 9052, 9804, 8785, `draft-ietf-vcon-vcon-core-04` |
| record statuses | 210 stub, 29 summarized, 5 distilled, 54 fetched, 6 queued |
| FX-1 in-scope by type (`rfc`/`draft`/`spec`) | 203, of which **118 still stub** |
| bytes | the 5 `distilled/` trees are ~1.5 MB of 4.0 MB in `records/` |
| `bears_on` targets | DEC-002 ×25, DEC-005 ×14, R-M-12 ×13, R-M-11 ×7, R-M-07 ×7 |
| **`<record>#R-NNNN` citations in `spec/` and `project/`** | **zero** |
| stated shape in `library/README.md` and `library/CLAUDE.md` | `record.yaml · distilled.md · quotes.md · artifacts/` — **none of those three exist in any record** |

The census was run twice. The first run, against the pinned submodule, gave
280 records and **one** `distilled/` directory. Only the standalone clone at
`~/Projects/library` gives the real figures. An agent that answers this
question from `mofn/library` answers it wrong.
