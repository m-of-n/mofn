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
| ~~1~~ | ~~**Does R-M-12 stand?**~~ **DECIDED 2026-09-22 — yes.** `ADR-0001`; now `ARCH-0002` P1. | ADR-0001 | closed |
| **2** | **DEC-002 — the encoding.** *Direction 2026-09-22: determinism is not uniqueness; start with a reduced CBOR profile. Prototyped in `prototype/statements/`.* Does R-M-12 make option 2 untenable, or does proposed option 5 (CBOR data model, no IANA tags, COSE as export only) rescue it? | ARCH-0001 §7, proposal §3.3 | Everything downstream. WP1 is encoding-neutral by design so reduction can start first, but D5 needs a target by **Oct 28**. |
| **3** | **Who drives the agent lanes — students or sponsor?** | PROC-0002 §8.1 | A teaching decision, not a throughput one. If students drive, they learn the material; if you do, it is faster and they learn less. Shapes L-011 through L-014, which are the bulk of I1. |
| **4** | **Accept the proposal as ARCH-0001 v0.2.0?** DEC-007 filed, DEC-006 withdrawn, R-M-11/12, R-O-05/06, RFC 9943 citation. | proposal | Until accepted, ARCH-0001 still cites a draft that became an RFC in June 2026, and the new requirements have no force. |

## Tier 2 — shapes the work now in flight

| # | Decision | Where |
|---|---|---|
| ~~5~~ | ~~**ARCH-0002?**~~ **DECIDED 2026-09-22 — yes.** | ADR-0001 |
| **5a** | **ARCH-0002 P2–P5**, all draft: constraints are **speech acts by a signing key** · **a type is a schema** carrying representation, constraints, semantics and multilingual human-review tags · **domains of discourse** are hash-identified *sets* of schemas · validity checked at all three RFC 8949 levels with unknown fields rejected | ARCH-0002 |
| **5e** | **DEC-009 — what is the contract form?** A third statement function beside attestation and delegation; the sponsor's note is incomplete. Deliberately unspecified rather than guessed. | ARCH-0002 |
| **5b** | **DEC-008 — can all processing be key-local?** Proposed: yes above a fixed core, never below it. A key that may define its own validity may define itself valid. | ARCH-0002 |
| **5c** | **Is a domain of discourse itself a statement by a key**, inheriting authorization and revocation — or a bare hashed artifact any key may cite? First composes; second allows vocabularies nobody owns. | ARCH-0002 P4 |
| **5d** | **Does DEC-007 survive?** P3 and P4 arguably *answer* it rather than constrain it. Re-state in their terms, or close as answered. | ARCH-0002 |
| 6 | **Does `locator` survive R-M-12?** Proposed as non-authoritative evidence; the strict reading excludes global locators from the native model entirely. | proposal §7 |
| 7 | **Which records get PROC-0002 stage 8** (generate code from spec)? Proposed: only where a spec defines an algorithm or wire format we intend to implement or map. | PROC-0002 §8.2 |
| 8 | **Does `versions/` hold a full record per version, or metadata plus a delta note?** | scope §7.1 |
| 9 | **Should `cites` be extracted automatically from converted PDFs, or always reviewed?** Automatic is noisy; manual does not scale. | references §5.1 |
| 10 | **Requirements extracted for every summarised record, or only where we intend to conform or map?** Extraction is expensive. | requirements §5.1 |

## Tier 2b — arising from ARCH-0002 and the retro

| # | Decision | Where |
|---|---|---|
| ~~6a~~ | ~~Five *kinds* or one *form*?~~ **ANSWERED 2026-09-22 by ARCH-0002 P6** — a name is an attested string, so the five are functions over one form. §4.3's three *procedures* stay separate; that was never about object kinds. `AclEntry` is the informative outlier: unsigned, so no speaker, so not a statement — it is the fixed floor DEC-008 needs. | ~~ARCH-0001 §4.2~~ |
| ~~6a-old~~ | ~~**Five statement *kinds* or one *form* with *functions*?**~~ ARCH-0001 §4.2 lists `NameCert`/`AuthzCert`/`AclEntry`/`ArtifactStatement`/`Endorse`; ARCH-0002 P2 says one form. They likely reconcile — but **`AclEntry` is unsigned, so it has no speaker**, and may be exactly the fixed floor DEC-008 says cannot be key-local. Needs a decision, not a silent edit. | ARCH-0001 §4.2, ARCH-0002 P2 |
| ~~6b~~ | ~~"Topic" collides~~ · ~~6c~~ ~~"Tag" collides~~ — **WITHDRAWN 2026-09-22.** Neither survives the collision test now stated in `GLOSSARY-0001`: two senses collide only when both can be live in the same context. Both are homonyms across separated repos and documents. Raising them was over-correction after three genuine collisions. | GLOSSARY-0001 |

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
