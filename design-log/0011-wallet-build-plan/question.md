---
schema: "design-log/v1"
id: DL-0011
part: question
title: "How is the wallet to be built? — reading the project corpus for what is decided, what is in flight, and what is still owed"
date: "2026-10-12"
model: "claude-opus-5"
human: ndewedo-newbury
outcome: "project/PLAN-0006-wallet.md at status: draft, decision_makers empty. No DEC-* accepted, no principle accepted, no framework chosen. Five findings not previously recorded anywhere (produced.md §2)."
status: open
---

# DL-0011 — question

> **Numbering.** `origin/main` carries entries through `0010`. `0007` is
> claimed twice on `main` and `DL-0009` §6.3 proposed id allocation as a
> `DECISIONS-0001` Tier 3 item; that is still unfiled. `0011` was taken after
> `git fetch` and a check of open PRs and remote branches — zero open PRs at
> the time of writing, so no branch can be holding `0011`.

## The question as asked

> "Using the `project` directory, search through all the `.md` files excluding
> the `PROC-*` files and determine how the wallet application is to be built.
> Create a `PLAN-****-wallet.md` file that contains the decisions that the
> wallet app bears on, the current issues/tasks that bear on it, suggested
> steps and how you think you should build it, as well as decisions that should
> be made by us or inferred from the project spec."

Four outputs, and the fourth is the one with teeth: *decisions that should be
made by us* means the plan is expected to **recommend**, not only to inventory.

## Context supplied

Read in full: `APP-0001`, `PLAN-0001` … `PLAN-0005`, `BACKLOG-0001`,
`DECISIONS-0001`, `RETRO-0001`, `GLOSSARY-0001`, both files in
`project/meetings/`. The `PROC-*` files were excluded as instructed.

Read beyond the instruction, because the corpus pointed at them and a plan
written without them would have been wrong rather than merely incomplete:

| source | why it was needed |
|---|---|
| `spec/ARCH-0001` (full) | the source of truth, and the only way to discover that **R-O-06 is not in it** |
| `spec/ARCH-0001-PROPOSAL-v0.2.0` §6 | where R-O-05 / R-O-06 actually live, and their exact text |
| `research/0002-wallets/report.md` (R-0002) | 63k of market survey §7 copy/change/refuse and §10.7 private keys — the wallet's anti-requirements exist nowhere else |
| GitHub issues #65–#69 | the `W-*` lane's acceptance criteria, which `BACKLOG-0001` compresses to one line each |
| `prototype/statements/`, `src/`, `design-log/` | what exists, versus what the documents say exists |

## Constraints taken as binding

From `CLAUDE.md` and `ARCH-0001` §9, treated as hard limits on the output
rather than as advice:

1. **No `DEC-*` may be marked accepted** outside an `ADR-NNNN`.
2. **No parallel architecture document** (`ARCH-0001` §9.4). This forced the
   shape of the output: the plan may *propose diffs* against `APP-0001` and
   `PLAN-0004` but may not restate or supersede them. §1–§2 of `PLAN-0006`
   are deliberately pointers rather than prose.
3. **`src/` is empty on purpose.** Any build recommendation that puts code
   there needs an argument, not a preference.
4. **Never generate cryptographic primitives.**
5. The design-log entry is written **in the same change**, per `DL-0001`'s
   permanent degradation.

## The question behind the question

The corpus already contains two wallet documents, five `W-*` issues, a 63k
market survey and a schedule. So the useful output is **not** a third
description of a wallet. It is the three things none of those contain:

- which open decisions the wallet would **close by accident**, and the guard
  for each;
- which single artifact, built first, lets the two owners work **in parallel**
  rather than in series;
- where the existing documents **contradict each other**, since a build plan
  that averages two conflicting sources produces a third conflicting source.

## What was explicitly not attempted

- No edit to `APP-0001`, `PLAN-0004`, `BACKLOG-0001` or `DECISIONS-0001`.
  `PLAN-0004` §8 already lists four fixes owed in `APP-0001` and they are still
  owed; adding a fifth source of truth would be the `§9.4` failure.
- No code. The engine is `W-1`'s and it has an owner.
- No library records, no `bears_on` edges, no submodule change.
