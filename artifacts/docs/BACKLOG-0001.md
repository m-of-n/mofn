---
schema: "archdoc/v1"
id: BACKLOG-0001
title: "m-of-n backlog"
short_title: "Backlog"
description: "Task backlog. Each task becomes a GitHub issue; this file is the durable index."
type: backlog
category: process
status: draft
version: "0.1.0"
date: "2026-09-16"
updated: "2026-09-16"
needs_review: true
reviewed: false
canonical_path: artifacts/docs/BACKLOG-0001.md
defers_to: ARCH-0001
agent_notes: >
  Tasks are the execution unit; topics (PROC-0001 §4) are the assignment unit.
  A task belongs to exactly one increment and names its deliverable. Keep the
  id stable when it becomes an issue — put T-NNN in the issue title.
---

# Backlog

**Convention.** `T-NNN` is stable and survives becoming a GitHub issue — put the
id in the issue title. Status: `todo` · `doing` · `review` · `done` · `parked`.
Size: `S` <½day · `M` ~1day · `L` ~3days.

Increments are in `PLAN-0001` §9. **The demo floor is I3 (Nov 11)** — everything
after is upside.

---

## I0 — Harness · Sep 16–30 · D0

| id | task | del | own | sz | status |
|---|---|---|---|---|---|
| T-001 | Create GitHub org `m-of-n`; three Owners | D0 | PL | S | todo |
| T-002 | Create `mofn` and `library` repos; push initial branches | D0 | PL | S | todo |
| T-003 | Branch protection on both: no direct push, 1 review, CI green, linear, signed | D0 | S1 | S | todo |
| T-004 | `CODEOWNERS` → `artifacts/docs/**` and `artifacts/vectors/**` to PL | D0 | S1 | S | todo |
| T-005 | DCO check in CI | D0 | S1 | S | todo |
| T-006 | Issue + PR templates; labels; milestones I0–I5 | D0 | S2 | M | todo |
| T-007 | `bin/validate-archdoc` in CI — front matter + version/updated coupling | D0 | S1 | M | todo |
| T-008 | MkDocs Material site deploying to Pages from a merged PR | D0 | S2 | M | todo |
| T-009 | `library` wired as submodule; `bin/lib-sync` working | D0 | S1 | S | todo |
| T-010 | `bin/wt` worktree helper; document in CONTRIBUTING | D0 | S1 | S | todo |
| T-011 | Publish draft planning docs to Pages — **asap, ahead of the rest of I0** | D0 | S2 | S | todo |
| T-012 | `design-log/` opened: how ARCH-0001 v0.1.0 was produced | D0 | PL | S | todo |
| T-013 | Agree and commit the cut order (PLAN-0001 §12) | D0 | all | S | todo |

## I1 — Library & research · Oct 1–14 · D1 D2 D3

| id | task | del | own | sz | status |
|---|---|---|---|---|---|
| T-020 | D1 v0.1 — construction best practice (`library/docs/construction.md`) | D1 | S2 | L | doing |
| T-021 | Seed 10 records by hand to prove the schema before scaling | D2 | S2 | M | doing |
| T-022 | Ingest adapters verified for each type: pdf, url, ietf, xlsx, md, book, repo, consortium, hierarchy | D2 | S2 | M | doing |
| T-023 | **Shelfmark: converge requirements, then schema. No data merger.** Write the requirements diff | D2 | PL | M | todo |
| T-024 | Library to ~40 records across the 7 topics | D2 | S2 | L | todo |
| T-025 | Report: *context* | D3 | S1 | L | todo |
| T-026 | Report: *mechanism* — the evidence base for DEC-002 and DEC-004 | D3 | S1 | L | todo |
| T-027 | Report: *uptake/applications* — incl. SPKI and PICS failure-to-adopt | D3 | S2 | L | todo |
| T-028 | Topic notes answered for `namespace-governance`, `canonical-encoding` | D3 | PL/S1 | M | todo |

## I2 — Schema + DEC-002 · Oct 15–28 · D4 D5

| id | task | del | own | sz | status |
|---|---|---|---|---|---|
| T-030 | WP1 — encoding-neutral schema for ARCH-0001 §4 logical types | D4 | S1 | L | todo |
| T-031 | Fixtures: `NameCert`, `AuthzCert` **with threshold subject**, `ArtifactStatement` | D5 | S1 | L | todo |
| T-032 | Score the two surviving DEC-002 options incl. namespace governance | D5 | S1 | M | todo |
| T-033 | `ADR-0001` — DEC-002 accepted; ARCH-0001 status updated + changelog | D5 | PL | M | todo |
| T-034 | Canonicalization idempotence + round-trip tests in CI | D5 | S2 | M | todo |
| T-035 | Resolve R-M-12: requirement row, or **ARCH-0002**? | — | PL | M | todo |

## I3 — Reduction · Oct 29–Nov 11 · D6 · **DEMO FLOOR**

| id | task | del | own | sz | status |
|---|---|---|---|---|---|
| T-040 | Name resolution: `Name` → `KeyId` via `NameCert` chains (§4.3 step 1) | D6 | S1 | L | todo |
| T-041 | 5-tuple reduction: tag ∩, validity ∩, delegation (§4.3 step 2) | D6 | S1 | L | todo |
| T-042 | Minimal tag profile — opaque bytes + `bytes-equal` (DEC-004 minimum) | D6 | S1 | M | todo |
| T-043 | *k*-of-*n* threshold subjects, keys only, no nesting | D6 | S2 | L | todo |
| T-044 | Statement acceptance (§4.3 step 3), kept separate from reduction | D6 | S2 | M | todo |
| T-045 | Verifier output reports the three separately (R-O-06) | D6 | S2 | M | todo |
| T-046 | Published test vectors under `artifacts/vectors/` | D6 | S1 | M | todo |
| T-047 | **Demo: chain reduces; break a link; verifier explains which and why** | D6 | all | M | todo |

## I4 — Mappings & app · Nov 12–25 · D7

| id | task | del | own | sz | status |
|---|---|---|---|---|---|
| T-050 | WP2 — `MAP-0001` SPKI/SDSI S-expression ↔ native | D7 | S1 | L | todo |
| T-051 | WP3 — `MAP-0002` in-toto Statement ↔ `ArtifactStatement` | D7 | S1 | L | todo |
| T-052 | Round-trip a real SLSA v1.1 provenance from a public release | D7 | S1 | M | todo |
| T-053 | Record interchange losses in the §6 matrix (R-I-01) | D7 | S1 | M | todo |
| T-054 | App packaging — single-file zipapp | D8 | S2 | M | todo |
| T-055 | Demo: valid-but-**unauthorized** key → distinct verdict | D7 | S2 | M | todo |

## I5 — Polish · Nov 26–Dec 4 · D8 D9 D10

| id | task | del | own | sz | status |
|---|---|---|---|---|---|
| T-060 | App download live on Pages, with install docs | D8 | S2 | M | todo |
| T-061 | Market & applications research | D9 | PL/S2 | L | todo |
| T-062 | `LIMITATIONS.md` final — what this does not prove | D10 | all | S | todo |
| T-063 | Final report | D10 | all | L | todo |
| T-064 | Demo rehearsals ×3 | D10 | all | M | todo |

---

## Parked — deliberately out of scope

| id | task | why |
|---|---|---|
| T-090 | WP4 — OpenPGP introducer import | Out of scope this semester (PLAN-0001 §2) |
| T-091 | WP5 — X.509 import | Out of scope this semester |
| T-092 | Transparency service / receipts | R-O-04 is `Could`; not in the demo floor |
| T-093 | Library federation across peers | Design and document only; do not build |
| T-094 | Nested threshold subjects | v2 |
