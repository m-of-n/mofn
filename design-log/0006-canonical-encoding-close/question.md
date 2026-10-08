---
schema: "design-log/v1"
id: DL-0006
part: question
title: "Canonical encoding lane B, closed — RFC 9804 scored, DSSE read out, two claims withdrawn"
date: "2026-10-08"
model: "claude-opus-5"
human: ndewedo-newbury
outcome: "library#57 — DSSE distilled, topic answered, ownership drift fixed, library#56 opened. No ADR — DEC-002 untouched. ARCH-0002 P5 amendment and the rcbor decode spike handed off, not done."
status: complete
---

# DL-0006 — question

**Predecessor: the unmerged `0004-canonical-encoding-lane-b` entry**, which
covers the first half of this same lane — the RFC 8785 extraction, the DSSE
summary, the topic split and the widened six-condition answer, on 2026-10-03.
This entry covers the session that closed the lane.

> **Numbering, resolved by `main` rather than by this entry.** An earlier draft
> took `0005` and flagged `DL-0004` as contested between two unmerged branches.
> That was read off a **stale local `main`**, 22 commits behind, whose design-log
> stopped at `0003`. On the real `main`, `0004-library-body-field` (#54) and
> `0005-cipher-suite` have both landed, so `DL-0004` and `DL-0005` are taken and
> this entry is **DL-0006**. The still-unmerged `0004-canonical-encoding-lane-b`
> branch is the one that now has to renumber — it is this entry's predecessor in
> substance, but not in id. See `review.md` §11 for how the stale base was found
> and what else it caused.

## Context supplied

Issue **#14** (LANE B, `canonical-encoding`) in full and issue **#8** (DEC-002
narrowing) in full; `mofn/CLAUDE.md` and `library/CLAUDE.md`; `ARCH-0001` §3.1,
§3.2, §8 (DEC-001…DEC-005); `ARCH-0001-PROPOSAL-v0.2.0`; the `close-topic`
skill; `library/docs/extraction.md` (FX-1), `schema/topic.schema.yaml`,
`schema/record.schema.yaml`, `bin/validate` and `bin/check-pr-extraction` as
read source rather than as commands; `topics/canonical-encoding.yaml` and its
four owned records, including the full FX-1 artifact sets for `rfc-9804` and
`rfc-8785`; the DSSE source archive at pinned commit `1d3370f`.

## Question posed

> "how to complete @/Users/nfn/Projects/mofn/ issue #14"

then, after the assessment was delivered:

> "execute with your recommendations and give summary of what was changed and how"

So the question was **not** "do lane B" — lane B was already most of the way
done. It was "what is actually left", which made the first task an audit of a
nearly-finished lane against its own issue and against `close-topic`, and the
second task the execution of that audit's findings.

## What the audit found, before any editing

Five gaps, in the order they were found:

1. The topic answer's closing paragraph said *"RFC 9804 is still queued, which
   is the one remaining blocker"* — **stale**. RFC 9804 reached FX-1 profile
   `full` in library#46 on 2026-10-04, and its `design-notes.md` already scored
   option 1 against all six conditions. The extraction had never been folded
   back into the answer it was performed for.
2. The issue's **second question** — what each candidate costs on library
   availability, native authenticated type indicator, and idempotence — was
   **unanswered anywhere**, in the note or the records. These are also three of
   the six axes #8's acceptance test names, so this was the part feeding #8.
3. `secure-systems-lab-dsse` was `status: summarized` with `envelope.md` and the
   attack notebook unread, which `close-topic` step 2 does not permit for an
   owned record.
4. **Seven** records carried `topic: canonical-encoding` while the topic's
   `records:` list named four — three drafts already owned by
   `deterministic-cbor-profiles`, and four owned by no topic at all.
5. No `design-log` entry existed for library#46's work, and none would have
   existed for this session either.

The audit also established that the **library#53 gate was lifted** on 2026-10-08,
so nothing external blocked the lane.

## Scope held deliberately narrow

Issue #14 says *"No architecture document. No implementation code."* Two items
the evidence pointed at were therefore **handed off rather than done**: the
ARCH-0002 **P5** clause extension that condition (2) needs, and the `rcbor`
single-pass decode experiment that would settle condition (2) empirically. Both
are `m-of-n` work, and both are now owned by issues — **#72** (the P5
amendment, including the newly found DSSE envelope-layer collision) and **#73**
(the single-pass rejecting decoder). Doing either inside a library PR would have
broken the issue's own instruction and ARCH-0001 §9.4.
