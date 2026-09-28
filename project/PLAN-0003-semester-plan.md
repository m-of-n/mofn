---
schema: "archdoc/v1"
id: PLAN-0003
title: "Key-centric Semantic Attestations — Fall 2026 plan"
short_title: "Semester plan"
description: "One-page plan from now to demo day, Dec 4: what ships, who owns it, when, and what it depends on."
type: plan
category: process
status: draft
version: "0.1.0"
date: "2026-09-28"
updated: "2026-09-28"
needs_review: true
reviewed: false
canonical_path: project/PLAN-0003-semester-plan.md
companion:
  - project/PLAN-0001-project-plan.md
  - project/meetings/2026-09-28.md
defers_to: ARCH-0001
---

# Key-centric Semantic Attestations — Fall 2026 plan

**Goal.** By **Dec 4 (CS Night demo day)**: a specification, protocol
definitions and a wallet application that let a key make typed, human-readable
statements — *A says B has C* — and let a verifier reduce a delegation chain
and explain the result in English.

This page is the plan. PLAN-0001 holds the detail and rationale; where they
differ, this page and the dated decisions (D-n) win until PLAN-0001 is updated.

## Fixed decisions (2026-09-28)

| | |
|---|---|
| **Targets** (D-1) | Software supply chain + archives/library. Short scenarios (email delegation, …) feed schema design only. |
| **Principles** (D-2) | ARCH-0002 P1 accepted; P2, P3, P5, P6 provisional; P4, P7 held. |
| **Encoding** (D-3) | Option 5: reduced CBOR, no IANA tags, COSE export only; YAML is the human form. |
| **Name / due** (D-6) | *Key-centric Semantic Attestations* · instructor Mario Lin · Dec 4 |

## Schedule

| Inc | Dates | Ships | Owner | Demo at the end |
|---|---|---|---|---|
| **I1** | Sep 29 – Oct 14 | Schema scenarios (Oct 5) · D1 library method · D2 library v1 · D3 reports (from survey R-001) · archives vocabulary v0 | David, Ndewedo | Query the library for everything bearing on DEC-002 |
| **I2** | Oct 15 – Oct 28 | D4 encoding-neutral schema (Oct 21) · D5 option-5 fixtures + option-2 comparison → ADR | David | One statement round-tripped YAML ↔ option 5, side by side with option 2 |
| **I3** | Oct 29 – Nov 11 | **D6 reduction + test vectors — the demo floor** | David, Ndewedo | Delegation chain reduces; break a link; verifier explains it in English |
| **I4** | Nov 12 – Nov 25 | D7 mappings: in-toto/SLSA ↔ statement; statements about library records | David | A real SLSA attestation imports and round-trips |
| **I5** | Nov 26 – Dec 4 | D8 wallet app on Pages · D9 market research · D10 final report, rehearsal | Ndewedo, Paul, all | CS Night |

**The floor is I3.** If everything after Nov 11 slips, the D6 demo still
stands on its own. Everything before it exists to make D6 possible.

## Critical path

`scenarios → schema (D4) → option-5 encoding (D5) → reduction (D6) → mappings (D7) → app (D8)`

Nothing downstream of D5 can freeze until the encoding ADR is accepted, so
**Oct 28 is the date to protect.**

## Owners

| | owns |
|---|---|
| **Paul** | decisions, reviews and merges; ADR acceptance; market research (D9) |
| **David** | encoding and fixtures (D4, D5), reduction (D6), mappings (D7) |
| **Ndewedo** | library and method (D1, D2), archives vocabulary, site, wallet app (D8) |
| **Claude** | ADR-0002 draft (Oct 2), PLAN-0002/Product Spec fill-in (Sep 30), library upkeep, research support |

## Risks

| risk | response |
|---|---|
| Encoding ADR slips past Oct 28 | D6 builds on the encoding-neutral schema; encoding swaps in later |
| Wallet GUI eats I4–I5 | ship a minimal GUI over the D6 verifier; CLI is not an acceptable substitute |
| P4 / P7 still open in November | the demo uses one domain and one authorization profile, stated as such |
| Review bottleneck (every merge needs Paul) | weekly Monday review; students approve each other's PRs |

## Cadence

Weekly Monday 16:00 PT, 30 min: decisions and unblocking. Notes are committed
the same day under `project/meetings/`, and each meeting updates this page's
status column when a milestone moves.
