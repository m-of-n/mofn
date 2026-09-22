---
schema: "archdoc/v1"
id: PROC-0002
title: "Multi-agent ingestion — fan-out, gates, and what humans actually review"
short_title: "Multi-agent ingestion"
description: "How agents find and process documents at scale while human review stays the binding constraint."
type: process
category: process
status: draft
version: "0.2.0"
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
source: "library#1 item 5; sponsor review of mofn#18"
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

Eleven stages, each a distinct agent. A human owns one of them, and that is the
point: everything else exists to make **stage 10** cheap and reliable.

| # | Stage | Who | Output |
|---|---|---|---|
| 1 | **Discover** | agent | candidates: title, locator, why it might matter |
| 2 | **Triage** | agent | in scope (`docs/scope.md`)? ingest, stub, or discard **with a recorded reason** |
| 3 | **Ingest** | agent | `bin/ingest`, digest fetched, `records/<body>/<id>/` |
| 4 | **Convert** | agent | PDF → markdown, **minimal information loss**; strip page furniture and boilerplate, keep section numbering |
| 5 | **Extract references** | agent | the document's own reference list → `cites`; unheld targets land on `index/frontier.md` |
| 6 | **Tag** | agent | `tags`, `topic`, `maturity`, draft `applicability` |
| 7 | **Distil** | agent | `distilled.md`, then `requirements/*.yaml` per `docs/requirements.md` |
| 8 | **Implement** | agent | reference code from the spec — e.g. NIST DSS → Python or C — plus **test vectors collected from the source**, in `artifacts/` |
| 9 | **Survey implementations** | agent | `implementations.open_source` / `.commercial`, with a `searched` date |
| 10 | **Adversarial review** | agent | attacks the summary, the applicability rating, and the code: *are the test vectors real, are they used, does it run?* |
| 11 | **Human review** | **human** | promotes to `summarized`, or sends back |

**Stage 10 → 11 is the gate that matters.** An agent never marks its own work
reviewed. `status: summarized` is a human signature.

### Stage 4 — conversion
Minimal information loss is the requirement, and "fluff" is precisely: running
heads and feet, page numbers, repeated legal boilerplate, and the table of
contents. **Section numbering is not fluff** — every extracted requirement
needs a locator, and page numbers do not survive conversion (`docs/requirements.md`
§1). Keep tables; they carry normative content more often than prose does.

### Stage 5 — the recursive part
Extracting a document's own references makes ingestion **self-feeding**: it is
the backward pass of Wohlin snowballing, mechanised. Unheld citations become
`index/frontier.md`, which is the queue for the next discovery run.

This is also where it runs away. **Depth is capped at 1 by default** — ingest
what our records cite, not what *those* cite — and the cap is raised only for a
named topic.

### Stage 8 — code and test vectors
Generating an implementation from a specification is the sharpest available
test of whether the spec was understood. NIST DSS is the worked example.

Three hard rules:
- **Test vectors come from the source document or its publisher, never
  generated.** A self-generated vector proves the code agrees with itself.
- **If the source publishes vectors and we did not find them, that is a stage
  10 failure**, not an acceptable outcome.
- **Generated code lives in `artifacts/` and never in `src/`.** It is evidence
  of comprehension, not project code, and `src/` remains empty until DEC-002.

### Stage 10 — adversarial review
PROC-0001 §3 argues this is the highest-leverage agent use, because it spends
agent time on the scarce resource rather than the abundant one. It checks:
the summary against the source; the applicability rating against the document's
actual content; whether test vectors exist and are used; and **whether the code
runs**.

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

- `bin/validate` — schema, typed relations, body matches directory, no
  committed third-party bytes
- `summary.md` present, YAML front matter, no template text left
- `bears_on` names a real `DEC-*`/`R-*` **or** `status: stub`
- **`bin/export && bin/reindex` regenerated and committed.** Ingestion makes
  `index/` stale — records, folded versions, crosswalk, bibliography, frontier.
  The human-visible bibliography going out of date after an ingestion run is
  the normal failure, which is why it is a gate and not a reminder.
- generated code in `artifacts/` runs, and its test vectors are cited to the
  source

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

1. **Who runs the lanes — students, or the sponsor?** L-011 through L-014 are
   large. If students drive agents they learn the material; if the sponsor does
   it is faster and they learn less. A teaching decision, not a throughput one.
   **Unchanged from v0.1 and still the sharpest question here.**
2. **Which records get stage 8?** Generating code from every spec is not
   affordable. Proposed: only where a specification defines an algorithm or a
   wire format we intend to implement or map — NIST DSS yes, a market analysis
   no.
3. **Does stage 8 code get its own review**, or does adversarial review cover
   it? "Does it run" is mechanical; "is it a faithful reading of the spec" is
   not, and that is the part worth catching.
4. **Reference-extraction depth.** Capped at 1 above. Raising it to 2 for a
   topic like `trust-management` may be right, but the frontier grows fast and
   nothing prunes it automatically.
5. **Batch size.** 6–10 per sitting is a guess; calibrate after the first real
   topic and revise this document.
6. **Design-log entries per record or per topic?** Per record is unusable at
   this volume; per topic may be too coarse to count as evidence.
7. **Does the adversarial agent see the human's prior corrections?** It would
   sharpen it considerably, and it risks training the pipeline to produce what
   this reviewer accepts rather than what is true.
