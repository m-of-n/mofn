---
schema: "archdoc/v1"
id: PROC-0002
title: "Multi-agent ingestion — fan-out, gates, and what humans actually review"
short_title: "Multi-agent ingestion"
description: "How agents find and process documents at scale while human review stays the binding constraint."
type: process
category: process
status: draft
version: "0.1.0"
version_policy: "semver; MINOR = additive process rules"
date: "2026-09-22"
updated: "2026-09-22"
decision_makers: []
reviewers: []
needs_review: true
reviewed: false
canonical_path: project/PROC-0002-multi-agent-ingestion.md
companion:
  - project/PROC-0001-agents-and-topics.md
defers_to: ARCH-0001
backlog: L-020
source: "library#1 item 5"
---

# PROC-0002 — Multi-agent ingestion

**Status: draft. Open for review.** Decisions marked **[?]** need the sponsor.

library#1 item 5: *"deep plan should be multi agent to process and find
documents. human review is of summary md."* This is that plan.

---

## 1. The constraint, restated

PROC-0001 §1: **review capacity is the bottleneck, not generation.** Multi-agent
ingestion does not relax it — it makes it worse, faster. Fifty agents produce
fifty summaries and one human still reads them at the same rate.

So the design target is not throughput. It is **the highest ratio of accepted
records to human reading minutes.** Everything below follows from that.

## 2. The pipeline

Five stages. Agents own 1–4; a human owns 5.

| # | Stage | Who | Output |
|---|---|---|---|
| 1 | **Discover** | agent | candidate list: title, locator, why it might matter |
| 2 | **Triage** | agent | in scope? (`docs/scope.md`) → ingest or discard, with reason |
| 3 | **Ingest** | agent | `bin/ingest`, `status: stub` or `queued`, digest fetched |
| 4 | **Draft summary** | agent | `summary.md` filled, `status: read` — **never `summarized`** |
| 5 | **Review** | **human** | promotes to `summarized`, or sends back |

**Stage 4 → 5 is the gate that matters.** An agent never marks its own work
reviewed. `status: summarized` is a human signature.

## 3. Fan-out

- **The topic is the unit** (PROC-0001 §4). One agent per topic. Topics are
  sized so their records rarely collide.
- **One worktree per agent** — `bin/wt new topic/<id>`. Edits cannot collide,
  and an abandoned lane is one `bin/wt rm`.
- **Concurrency cap: three to five lanes**, the weekly human review budget.
  More lanes do not produce more accepted records; they produce a queue.
- **One PR per topic**, not per record. A reviewer reads a coherent set with a
  topic note, not fourteen disconnected diffs.

## 4. Batching — the thing that makes this work

Agents draft; humans review **in batches, by topic**, not as records arrive.

A reviewer reading eight summaries in one topic builds context once and applies
it eight times. The same eight scattered across three weeks costs eight
context rebuilds and produces less consistent judgement.

**Target batch: one topic, 6–10 records, one sitting.**

## 5. Quality gates

Mechanical, in CI, before a human sees anything:

- `bin/validate` — schema, typed relations, no committed third-party bytes
- `summary.md` present, YAML front matter, no template text left
- `bears_on` names a real `DEC-*`/`R-*` **or** `status: stub`
- `exports/` regenerated

Judgement rules the tools cannot check, from the skills:

- **Never invent relevance.** A fabricated `bears_on` corrupts the only query
  the library exists to answer. A stub is the honest alternative.
- **Never guess `maturity`.** Unset beats wrong.
- **Record disagreement.** `contradicts` is the valuable relation, and an agent
  that only ever agrees with its sources is not reading them.
- **Discards are logged.** Stage 2 rejections go in the topic note with one
  line of reason. An unlogged discard is indistinguishable from a miss, and it
  is how the same document gets re-evaluated four times.

## 6. What agents must not do

- Never set `status: summarized` or `reviewed: true`.
- Never write or amend `spec/` — architecture serializes through ARCH-0001 §9.4
  and a human (PROC-0001 §2).
- Never extract requirements into `requirements/` from a `summary.md` — only
  from `distilled.md`, which is only made from the source.
- Never ingest past the caps in `docs/scope.md` without saying so.

## 7. Where this is worth it, and where it is not

**Worth it:** discovery sweeps over a bounded question; digest fetching;
first-draft summaries of documents a human will read anyway; implementation
searches (L-015), which are mechanical and tedious.

**Not worth it:** anything where a reviewer cannot check the output faster than
producing it. Most of the cryptographic core is in this category — a confident
wrong summary of a signature scheme costs more than it saves.

**Highest leverage, per PROC-0001 §3:** an agent tasked with arguing *against* a
finished summary before a human reads it. That spends agent time on the scarce
resource rather than the abundant one.

---

## 8. Open questions **[?]**

1. **Does stage 4 need a second agent reviewing the first?** §7 argues
   adversarial review is the best available agent use. It would raise quality
   before human time is spent — at the cost of drafts that read as
   committee-written.
2. **Who runs the lanes — students, or the sponsor?** L-011 through L-014 are
   large. If students drive agents, they learn the material; if the sponsor
   does, it is faster and they learn less. This is a teaching decision, not a
   throughput one.
3. **Is `status: read` the right agent ceiling**, or should agents stop at
   `queued` and never draft a summary unprompted?
4. **Batch size.** 6–10 per sitting is a guess. It should be calibrated after
   the first real topic and this document revised.
5. **Does the design-log entry requirement apply per record or per topic?**
   Per record is unusable at this volume; per topic may be too coarse to be
   evidence.
