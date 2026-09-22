---
schema: "archdoc/v1"
id: DECISIONS-0001
title: "Open decision register — everything waiting on a human"
short_title: "Decision register"
description: "Every open decision across both repos, ranked by what it blocks. The sponsor review list."
type: process
category: process
status: active
version: "0.1.0"
version_policy: "semver; MINOR = decisions added or closed"
date: "2026-09-22"
updated: "2026-09-22"
decision_makers: []
reviewers: []
needs_review: false
reviewed: false
review_note: >
  The register itself is live, not under review. Its ITEMS are what
  await a decision — that is the document's whole content.
canonical_path: project/DECISIONS-0001.md
defers_to: ARCH-0001
agent_notes: >
  A register, not an authority. Accepting any DEC-* still requires an ADR plus
  a changelog line plus a status update in ARCH-0001 (§9.2). Nothing here
  accepts anything.
---

# Open decision register

**Checkpoint 2026-09-22.** Both repos clean on `main`, no open PRs, submodule
pin current. Nothing is blocked on work; everything below is blocked on a
person.

Ordered by **what it unblocks**, not by importance.

---

## Tier 1 — blocks the demo floor (I3, Nov 11)

| # | Decision | Where | Why it blocks |
|---|---|---|---|
| **1** | **Does R-M-12 stand?** Extension points are `(key, local label)`; no central registry. | proposal §3.2, §7 | Load-bearing. It constrains **DEC-002, DEC-004 and DEC-007 at once**. If it falls, three sections of the proposal need rework — about a week. Cheaper to test before fixtures exist than after. |
| **2** | **DEC-002 — the encoding.** Does R-M-12 make option 2 untenable, or does proposed option 5 (CBOR data model, no IANA tags, COSE as export only) rescue it? | ARCH-0001 §7, proposal §3.3 | Everything downstream. WP1 is encoding-neutral by design so reduction can start first, but D5 needs a target by **Oct 28**. |
| **3** | **Who drives the agent lanes — students or sponsor?** | PROC-0002 §8.1 | A teaching decision, not a throughput one. If students drive, they learn the material; if you do, it is faster and they learn less. Shapes L-011 through L-014, which are the bulk of I1. |
| **4** | **Accept the proposal as ARCH-0001 v0.2.0?** DEC-007 filed, DEC-006 withdrawn, R-M-11/12, R-O-05/06, RFC 9943 citation. | proposal | Until accepted, ARCH-0001 still cites a draft that became an RFC in June 2026, and the new requirements have no force. |

## Tier 2 — shapes the work now in flight

| # | Decision | Where |
|---|---|---|
| 5 | **Does R-M-12 deserve its own document (ARCH-0002)?** Arguably the most novel claim available — *SDSI localized principal names; nobody localized type names.* | proposal §7 |
| 6 | **Does `locator` survive R-M-12?** Proposed as non-authoritative evidence; the strict reading excludes global locators from the native model entirely. | proposal §7 |
| 7 | **Which records get PROC-0002 stage 8** (generate code from spec)? Proposed: only where a spec defines an algorithm or wire format we intend to implement or map. | PROC-0002 §8.2 |
| 8 | **Does `versions/` hold a full record per version, or metadata plus a delta note?** | scope §7.1 |
| 9 | **Should `cites` be extracted automatically from converted PDFs, or always reviewed?** Automatic is noisy; manual does not scale. | references §5.1 |
| 10 | **Requirements extracted for every summarised record, or only where we intend to conform or map?** Extraction is expensive. | requirements §5.1 |

## Tier 3 — process, decide when convenient

| # | Decision | Where |
|---|---|---|
| 11 | Who moves the submodule pin — the lane that merged, or whoever next needs it? | PROC-0003 §8.3 |
| 12 | Is three to five lanes right for four people with one reviewer? Uncalibrated. | PROC-0003 §8.2 |
| 13 | Is topic ownership exclusive? | PROC-0003 §8.4 |
| 14 | Design-log entries per record or per topic? Per record is unusable at volume. | PROC-0002 §8.6 |
| 15 | Does the adversarial agent see prior human corrections? Sharper, but risks optimising for one reviewer. | PROC-0002 §8.7 |
| 16 | Reference-extraction depth beyond 1 for a named topic? | PROC-0002 §8.4 |
| 17 | Does `usefulness` need forced re-assessment dating? | scope §7.3 |
| 18 | When does a new body directory get created (`regulator` vs `eu`/`us-federal`)? | scope §7.2 |
| 19 | Does `cited_by` belong on a record, or only in `index/`? | references §5.2 |
| 20 | Normalise `verb` SHALL → MUST? Synonymous in RFC 2119; normalising loses the source's wording. | requirements §5.3 |
| 21 | Track requirement **satisfaction** — ours against theirs? That is a conformance matrix and a much larger commitment. | requirements §5.2 |

## Tier 4 — administrative, blocking people not work

| # | Item | State |
|---|---|---|
| 22 | **Mario Lim repo access.** Invite to `mlim3@usfca.edu` pending since 2026-09-16. `mlim-usfca` is his **organisation**, not a user account — needs his personal GitHub login. | blocked on him |
| 23 | **`enforce_admins`** is `false` on both repos. Set so a single member could bootstrap; three admins now exist, so the reason has expired. | ready to flip |
| 24 | **Signed commits** — `CONTRIBUTING.md` asks for them; the requirement is off so students are not blocked on key setup. | deliberate |
| 25 | **`~/cb/.claude/rules/usf-provenance.md`** written but uncommitted — `~/cb` has your in-flight manifest work. | yours to commit |
| 26 | **Shelfmark convergence** — requirements first, then schema. No data merger. | T-023, not started |

---

## What is *not* waiting on you

Decided and merged: DEC-001 (`m-of-n`) · `summary.md` primary, `distilled.md` for
requirements extraction · stubs allowed · hierarchical `records/<body>/<id>/` ·
version folding · `usefulness` verdicts replacing caps · no record caps ·
NIST summarised not stubbed (L-011) · skills partitioned by what they act on ·
generated nav, index and crosswalk with CI staleness gates.

Students are unblocked: **#13** (David, namespace-governance), **#14** (Ndewedo,
canonical-encoding), **#23** (David, NIST set).
