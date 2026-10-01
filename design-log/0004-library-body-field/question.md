---
schema: "design-log/v1"
id: DL-0004
title: "library `body` — one field doing three jobs, and which two it gives up"
date: "2026-10-01"
model: "claude-opus-5"
human: ndewedo-newbury
outcome: "library#34 (open). docs/scope.md §4 v0.3.0, record schema v0.6.0, tags.yaml v0.2.0. No ADR — no DEC-* touched."
status: open
---

# DL-0004 — question

## Context supplied

`mofn/CLAUDE.md` and `library/CLAUDE.md`; `library/docs/scope.md` v0.2.0,
`docs/references.md`, `docs/generated-views.md`, `schema/record.schema.yaml` v5
(v0.5.0), `schema/tags.yaml` v0.1.0; `bin/validate`, `bin/ingest`, `bin/reindex`,
`bin/export`, `bin/_yaml.py`, `bin/check-pr-extraction`, `.github/workflows/ci.yml`;
`library` issue #27 in full and the merged PR #25 that deferred it;
`project/PROC-0003` §1–2.

## Question posed

> "for issue #27, resolve the issue using the 1. accept it option claude
> suggests in the issue comment"

**The decision was the human's, not the model's.** #27 was written with three
options and none chosen; the human picked option 1 before the model proposed
anything. What was delegated was the *consequences* of that choice, not the
choice.

## What #27 asked

`body` is single-valued and does three jobs at once: the enum of issuing
organisations, the storage directory `records/<body>/<id>/`, and the section
heading of `index/records.md` and `index/bibliography.md`. CycloneDX 1.7 is
authored by the OWASP Foundation and ratified by Ecma International as ECMA-424
2nd edition. One record gets one `body`, so one of those is always lost.

Option 1 — accept it: `body` is storage plus a coarse grouping, publisher
identity lives in `publisher`, standing lives in `maturity`. *Document the rule
and stop treating `body` as an authority claim.*

The issue also flagged, as a second item, that `schema/tags.yaml:body` and
`schema/record.schema.yaml:body` had **diverged** — the schema carried
`regulator` and `other`, the tag list carried neither — and asked they be made
to agree or explicitly separated.

## The constraint that shaped the work

Option 1 is only non-lossy **if the fields it delegates to are visible.** The
issue asserts `publisher` is "already rendered in the bibliography". The model
was asked to accept the option, not to audit its premise — but the premise was
checkable in `bin/reindex`, and checking it is what turned a documentation
change into a code change. See `produced.md`.

`library/CLAUDE.md`: never hand-create a record, never set `content.local`,
never reuse an id, never commit third-party bytes. None was violated; the
last two are why one found defect was left unfixed.
