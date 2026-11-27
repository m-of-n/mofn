---
schema: "design-log/v1"
id: DL-0057
part: question
title: "ADR-0002 reopened by the sponsor — P2, P3, P6 not binding; gap analysis and a plan"
date: "2026-11-25"
model: "Grok Bot (AI agent)"
human: sponsor
outcome: "ADR-0002 1.1.0, status proposed (reopened). ARCH-0002 0.11.0 marks P2, P3, P6 reopened. ARCH-0001 0.3.5, SPEC-0003 0.3.1, GLOSSARY-0001 0.3.1, DECISIONS-0001 0.9.0, BACKLOG-0001 0.17.2 annotated. Gap analysis and a proposed order of work in analysis.md. No other ADR changed status. No DEC-* touched."
status: open
---

# DL-0057 — question

## The brief

The sponsor reviewed `ADR-0002` (accepted 2026-11-06 by the student decision
maker under the October delegation, DL-0024) while stepping through the ADRs
that rest on that delegation. The sponsor's message, verbatim:

> p2 ... there are more forms ... we had time limitations etc, we had a richer
> vocabulary ... so this process is broken and the ADRs are not consistent and
> following original goals;  P6 ... a name is a signed string ... that's
> nonsense ...   open ADR-0002 for review in my browser   ... a type is a
> schema ???  we need a consistent base arch and definitions and not random
> questions   reopen this

The agent was asked to:

1. open a PR that reopens `ADR-0002`, records the objections in neutral form,
   marks P2, P3 and P6 not binding, leaves P5's standing unchanged pending
   review, and updates what cites the ADR as binding;
2. produce a gap analysis tracing the original goals and vocabulary against
   ARCH-0002 P1–P7, `ADR-0002`, `ADR-0004`…`ADR-0008` and `SPEC-0001`…`SPEC-0005`
   and the engine, and propose an order of work toward one consistent base
   architecture and one canonical set of definitions;
3. not merge, not contact the students, and not change any other ADR's status.

## Context supplied

`origin/main` at `5b2e1bf`. Read in full or by section: `ADR-0002`, `ADR-0003`,
`ADR-0004`…`ADR-0008`, `ARCH-0001` (and its v0.1.0 from the first commit,
`2a79b1f`), `ARCH-0002` and changelog, `GLOSSARY-0001`, `PLAN-0001` §0–§1 and
§8, `DECISIONS-0001` items 4a and 6a, `DL-0002`, `DL-0021`, `DL-0024`,
`SPEC-0001`…`SPEC-0004`, `spec/vectors/ksa-core/vectors.json`, and
`prototype/wallet/engine/`. The weekly minutes are not published and were not
available; the "original goals" below are what the repository records, and the
analysis says where that is thin.
