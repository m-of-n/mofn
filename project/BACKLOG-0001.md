---
schema: "archdoc/v1"
id: BACKLOG-0001
title: "m-of-n backlog"
short_title: "Backlog"
description: "Task backlog. Each task becomes a GitHub issue; this file is the durable index."
type: backlog
category: process
status: draft
version: "0.11.3"
date: "2026-09-16"
updated: "2026-10-17"
needs_review: true
reviewed: false
canonical_path: project/BACKLOG-0001.md
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

Increments are in `PLAN-0001` §9 and the one-page `PLAN-0003`. **The demo floor
is I3 (Nov 11)** — everything after is upside.

## Status at 2026-10-11

**Added since 2026-10-05:** the **`W-*` wallet and demo-slice lane** (issues
#65–#69, opened 2026-10-05) had no backlog entry at all — five tasks, three
owners and the whole `PLAN-0004` application plan, tracked only in GitHub.
A lane that exists only as issues is invisible to the one file that is supposed
to be the durable index. They are now §*Wallet and demo slice* below.

**Ids:** the 2026-09-28 decisions are now **`MD-1 … MD-7`**, not `D-n`
(`GLOSSARY-0001`; `DECISIONS-0001` item 27). `D0 … D10` deliverables are
unchanged, which is the point of the rename.

**In review:** mofn#82 (`DECISIONS-0001` v0.2.0, the MD-1…MD-7 transcription),
mofn#83 (`ADR-0002` proposed, T-029d), library#65 (the rename + FX-1 mandate),
library#66 (`gaps.md` refresh). T-029e closes with #82.

## Status at 2026-10-05 — I1 closes Oct 14

This file had not moved since 2026-09-22. Brought up to date from the repos,
merged PRs and the 2026-09-28 decisions (MD-1…MD-7, `project/meetings/`).

**At risk for Oct 14 (I1):**
- **D3 research reports (T-025–T-027) — not started.** No student report exists
  in `research/`. MD-4 says draft them from survey R-001 (§2/§4 mechanism, §5–§8
  uptake); the material is there, the reports are not.
  *Superseded 2026-10-17: all three are drafted — T-025 `R-0005`, T-026
  `R-0006`, T-027 `R-0004` — and in `review`; see their rows below.*
- **D1 construction method (T-020)** — `library/docs/construction.md` last
  edited 2026-09-16.
- **Library quality (T-024)** — 280 records, but **16 written and 264 unwritten
  scaffolds** (library#45). The count was reading as progress.
- **Lane issues mofn#13, #14, #23** — no activity since 2026-09-21/22.

**Overdue sponsor-side and agent actions:** ADR-0002 draft (Claude, was Oct 2);
DECISIONS-0001 T1-A closure (Claude); Product Spec GAP-6 dates (Paul).

**Process:** every merge needs one approval and `enforce_admins` is off in both
repos, so the sponsor is the only path to `main`. Neither student has reviewed
the other's PRs (0 reviews). See T-006c, T-006d.

**Pending sponsor decision:** library#42 narrows FX-1 from "every spec record a
PR moves past stub" to "every record a PR *extracts*" (summaries held to the
summary bar). Accept or keep #32's rule — L-035.

---

## I0 — Harness · Sep 16–30 · D0

| id | task | del | own | sz | status |
|---|---|---|---|---|---|
| T-001 | ~~Create GitHub org `m-of-n`~~ — done; DEC-001 accepted | D0 | PL | S | done |
| T-002 | ~~Create `mofn` and `library` repos~~ — done, both public and pushed | D0 | PL | S | done |
| T-003 | **Fall 2026 deliverables — definition of done.** `PROC-0004`, aligned to D0–D10. Parent issue mofn#28 with sub-issues | D0–D10 | all | L | doing |
| T-003x | ~~Branch protection~~ — done; residual settings are T-006c | D0 | S1 | S | done |
| T-004 | `CODEOWNERS` → `/spec/` and `/project/` to PL; both students on the catch-all | D0 | S1 | S | done |
| T-005 | ~~DCO check in CI~~ — done, both repos | D0 | S1 | S | done |
| T-006 | ~~Issue + PR templates; labels; milestones~~ — done | D0 | S2 | M | done |
| T-006a | ~~Repo `admin` for both students~~ — done, both repos and the org | D0 | PL | S | done |
| T-006b | Decide faculty access for Mario Lin (read? admin?) — not yet a collaborator or invitee | D0 | PL | S | todo |
| T-006c | Turn on `enforce_admins` now a second reviewer exists — still off in both repos (2026-10-05) | D0 | PL | S | todo |
| T-006d | **Students review each other's PRs** — 0 cross-reviews to date; every merge currently waits on the sponsor | D0 | S1+S2 | S | todo |
| T-007 | ~~`bin/validate-archdoc` in CI~~ — done | D0 | S1 | M | done |
| T-008 | ~~MkDocs Material site deploying to Pages~~ — done; live at m-of-n.github.io/mofn | D0 | S2 | M | done |
| T-009 | ~~`library` wired as submodule; `bin/lib-sync` working~~ — done | D0 | S1 | S | done |
| T-010 | ~~`bin/wt` worktree helper; document in CONTRIBUTING~~ — done | D0 | S1 | S | done |
| T-011 | ~~Publish draft planning docs to Pages~~ — done | D0 | S2 | S | done |
| T-012 | **Architecture development** — market research, technology background, bibliography, base design of both protocols and the application. **Scope extends beyond the student project.** Deliverable: the architecture specification. Iterated in-issue. Inputs so far: ARCH-0002, survey R-001, wallet survey R-002, cipher suite R-0003 (mofn#60) | — | PL | XL | doing |
| T-012x | ~~`design-log/` opened~~ — done; DL-0001 and DL-0002 written | D0 | PL | S | done |
| T-013 | Agree and commit the cut order (PLAN-0001 §12) — mofn#7, no discussion yet | D0 | all | S | todo |

## I1 — Library & research · Oct 1–14 · D1 D2 D3

| id | task | del | own | sz | status |
|---|---|---|---|---|---|
| T-020 | D1 v0.1 — construction best practice (`library/docs/construction.md`) — **at risk**: last edit 2026-09-16; FX-1 (`docs/extraction.md`) now carries much of it | D1 | S2 | L | doing |
| T-021 | ~~Seed 10 records by hand to prove the schema~~ — done | D2 | S2 | M | done |
| T-022 | Ingest adapters verified for each type: pdf, url, ietf, xlsx, md, book, repo, consortium, hierarchy | D2 | S2 | M | doing |
| T-023 | **Shelfmark: converge requirements, then schema. No data merger.** Write the requirements diff | D2 | PL | M | todo |
| T-024 | Library to ~40 records across the topics — **count met (280), quality not**: 16 written, 264 scaffolds. Fill tracked in library#45 | D2 | S2 | L | doing |
| T-025 | Report: *context* — **drafted** as `R-0005` (research/0005-context). Synthesis pass over R-001 §1–§6/§11/§12 and R-0004 §8; **no retrieval pass**, stated as a limitation in its `searches.md` | D3 | S1 | L | review |
| T-026 | Report: *mechanism* — **drafted** as `R-0006` (research/0006-mechanism), v0.3.0. The comparative anatomy of in-toto/DSSE, SCITT/COSE, SPKI, PICS and VC/DID in one frame (§2.2–§2.5; PICS and VC cells marked unsourced, `unverified.md`), the six conditions, all four DEC-002 candidates scored, DEC-004's meet-vs-accumulation evidence. Decides nothing; §3.9 states where the evidence sits relative to MD-3 **and `ADR-0003` D2**, and §3.13 reads conditions (5) and (6) against `SPEC-0002`/`SPEC-0003`. §4.6–§4.7: the accepted core's range algebra, and whether T-042 is subsumed by it — **raised for T-042's owner, not decided** | D3 | S1 | L | review |
| T-027 | Report: *uptake/applications* — incl. SPKI and PICS failure-to-adopt — **drafted** as `R-0004` (research/0004-uptake-and-applications), merged in mofn#87 on 2026-10-12. **The row was stale, not the work** | D3 | S2 | L | review |
| T-028 | Topic notes answered for `namespace-governance`, `canonical-encoding` — canonical-encoding in review (library#46); 3 of 17 topics answered overall | D3 | PL/S1 | M | doing |
| T-029a | Schema scenarios (3–5, incl. email delegation) and Product Spec personas, GAP-1 (MD-1) | D3 | S1+S2 | M | todo — was due Oct 5 |
| T-029b | Product Spec, PLAN-0002 v0.2 — GAP-4 real sketches (Ndewedo, Oct 14), GAP-6 course dates (PL) | — | PL+S2 | M | doing |
| T-029c | Confirm Tauri for the wallet GUI (MD-7) before GUI work starts | D8 | S2 | S | todo — Oct 14 |
| T-029d | ADR-0002: accept P2, P3, P5, P6 provisionally (MD-2) | — | Claude→PL | M | **overdue** (was Oct 2) |
| T-029e | Close T1-A in DECISIONS-0001 citing MD-1 | — | Claude | S | **overdue** |

## I2 — Schema + DEC-002 · Oct 15–28 · D4 D5

| id | task | del | own | sz | status |
|---|---|---|---|---|---|
| T-030 | WP1 — encoding-neutral schema for ARCH-0001 §4 logical types | D4 | S1 | L | todo |
| T-031 | Fixtures: `NameCert`, `AuthzCert` **with threshold subject**, `ArtifactStatement` — in **option 5** (MD-3) plus the option-2 comparison. **Narrowed by `spec/vectors/ksa-core/`**, which covers the name-binding and artifact shapes under `ADR-0003` D2's encoding; **the threshold subject has no vector** and is the remaining gap — R-0006 §3.12, §3.13 | D5 | S1 | L | todo |
| T-032 | Score option 5 against option 2 incl. namespace governance (MD-3 narrowed DEC-002 to these) — needs library#39 Tier 1 extracted first | D5 | S1 | M | todo |
| T-033 | ADR for DEC-002 (ADR-0001 is taken by key-relative naming) — accepted; ARCH-0001 status updated + changelog | D5 | PL | M | todo |
| T-034 | Canonicalization idempotence + round-trip tests in CI | D5 | S2 | M | todo |
| T-035 | ~~Resolve R-M-12: requirement row, or ARCH-0002?~~ — ARCH-0002, accepted as P1 via ADR-0001 | — | PL | M | done |

## I3 — Reduction · Oct 29–Nov 11 · D6 · **DEMO FLOOR**

| id | task | del | own | sz | status |
|---|---|---|---|---|---|
| T-040 | Name resolution: `Name` → `KeyId` via `NameCert` chains (§4.3 step 1) | D6 | S1 | L | todo |
| T-041 | 5-tuple reduction: tag ∩, validity ∩, delegation (§4.3 step 2) | D6 | S1 | L | todo |
| T-042 | Minimal tag profile — opaque bytes + `bytes-equal` (DEC-004 minimum). *Possibly subsumed by `SPEC-0003` `delegation: 1` — `R-0006` §4.7; owner's call* | D6 | S1 | M | todo |
| T-043 | *k*-of-*n* threshold subjects, keys only, no nesting | D6 | S2 | L | todo |
| T-044 | Statement acceptance (§4.3 step 3), kept separate from reduction | D6 | S2 | M | todo |
| T-045 | Verifier output reports the three separately (R-O-06) | D6 | S2 | M | todo |
| T-046 | Published test vectors under `spec/vectors/` | D6 | S1 | M | todo |
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

## Wallet and demo slice — `W-*` · issues #65–#69

Opened 2026-10-05 against `PLAN-0004` and parent #31 (T-003.5, the demo floor).
Tracked here from 2026-10-11; before that they existed only as issues.
`W-1` is the engine everything else calls — **nothing in this lane starts
before it runs.**

| id | task | issue | del | own | sz | status |
|---|---|---|---|---|---|---|
| W-1 | **Wallet engine v0** — `mofn` CLI over a local `wallet/` (`roots/ keys/ domains/ statements/`); `init`, `key gen` (private key `0600`, encrypted at rest, passphrase prompted, **never an argument**), `root add`, `make`, `check` printing the six-line verdict. **Signature checking moves inside reduction** — `reduce` stops trusting its inputs | #65 | D6 | S1 | XL | todo — Oct 28 |
| W-2 | **Second domain** — one-page scenario per MD-1 target (supply chain, archives/library) incl. the fail-authorization case and three personas; archives domain file v0 (`record-review`, renderings table, `--lang es`); five-view sketches replacing Product Spec §6.5 | #66 | D6/D8 | PL | L | todo — Oct 14, then Nov 25 |
| W-3 | **Delegation with short expiry** — `may-speak` chains in `reduce`, intersecting topic *and* validity; expired or out-of-topic → `authorization FAIL` naming the broken link. **Short expiry is the revocation mechanism**; there is no revocation list | #67 | D6 | PL | L | todo — Nov 11 |
| W-4 | **Weekly demo slice owner** — grow and run `demo/slice.sh` every Monday, post the output on the issue. Three cases minimum: green, `authorization FAIL`, `integrity FAIL` | #68 | D6 | S2 | M | doing — weekly |
| W-5 | **Mac GUI** — local desktop app (not a web server) for signing and verify/validate display with attribute associations; calls the W-1 engine, reimplements no crypto. Sign and Verify screens first | #69 | D8 | S2 | L | todo — Dec |

**Overlap to resolve.** W-1 and W-3 restate T-041/T-044/T-045 (reduction,
statement acceptance, separated verifier output) as application work, and W-2
restates T-029a/T-029b. They are the same deliverables seen from the
application side. **Either the `T-` rows or the `W-` rows should become
pointers, not both live** — otherwise I3 is double-counted. Flagged, not
resolved: it is a planning call, not a transcription.

## Library build-out — from library#1 and sponsor direction 2026-09-21

`L-` tasks run in `m-of-n/library`. Most are I1; they gate #13 and #14.

| id | task | src | own | sz | status |
|---|---|---|---|---|---|
| L-001 | ~~`summary.md` primary; `distilled.md` = requirements extraction~~ | #1.1 | — | L | review |
| L-002 | ~~`status: stub` for references that bear on nothing yet~~ | sponsor | — | S | review |
| L-003 | ~~Controlled tag vocabulary: subject / body / role~~ | #1.6,10 | — | M | review |
| L-004 | ~~`maturity` on RFC 2026 levels~~ | sponsor | — | S | review |
| L-005 | ~~OKF alignment — YAML front matter, documented extensions~~ | #1.11,12 | — | M | review |
| L-006 | ~~`implementations` field — open source + commercial~~ | #1.3 | — | S | review |
| L-007 | ~~`research/` for archived method research~~ | sponsor | — | S | review |
| L-010 | ~~Fill out the 9 existing records~~ — superseded by library#45 (264 scaffolds) | #1.2 | S2 | L | parked |
| L-011 | **NIST cryptographic algorithms — summarised records, not stubs** (sponsor 2026-09-22). Document set below; expanded scope in library#8; Ndewedo's library#42 in review | #1.4 | S1 | L | review |
| L-012 | ~~NIST digital signature specifics~~ — folded into L-011 | #1.2 | S1 | — | done |
| L-013 | Attestation specifications sweep — RATS, EAT, CoRIM, TPM, Confidential Computing — **ingested** by the survey (topic `device-attestation`, 26 records), **not written** (#45) | #1.2,7 | S1 | L | doing |
| L-014 | Trust management publications — deep research gather | #1.7 | S2 | L | todo |
| L-015 | Implementation search across all records — open source + commercial | #1.3 | S2 | M | todo |
| L-016 | Organised bibliography for review; confirm the schema supports it | #1.6 | S2 | M | todo |
| L-017 | Applicability review pass over all records after first summarisation | #1.8 | PL | M | todo |
| L-018 | Define ingestion **scope**: standards, specs, recommendations, white papers, sites, repos | #1.10 | PL | S | todo |
| L-019 | Archive the method research behind `docs/construction.md` — sources were discarded | sponsor | S2 | M | todo |
| L-020 | ~~Multi-agent ingestion plan~~ — done: PROC-0002, and FX-1 `docs/extraction.md` for spec records | #1.5 | PL | M | done |
| L-021 | `mofn/research/` — D3 reports with `sources.md` and `searches.md` | sponsor | S1 | S | todo |
| L-022 | Promote recurring free tags into `schema/tags.yaml` (rule of three) | #1.6 | S2 | S | todo |
| L-030 | ~~FX-1 full extraction standard — enforced in CI~~ — library#32 | sponsor | Claude | M | done |
| L-031 | FX-1 extraction of the CBOR/COSE set, ranked — **Tier 1 needed for D5 by Oct 28** | library#39 | S1 | XL | todo |
| L-032 | SCITT full extraction (#30 merged as summaries only) | library#40 | S1 | L | todo |
| L-033 | Fill the 264 unwritten scaffolds, batched by topic | library#45 | S2 | XL | todo |
| L-034 | YAML reader block scalars, scaffold inventory, duplicate detection | library#43/#35/#45 → #48 | Claude | M | review |
| L-035 | **Sponsor decision:** accept library#42's FX-1 carve-out (summaries held to the summary bar), or keep #32's rule | library#42 | PL | S | todo |
| L-036 | First student FX-1 extractions — RFC 9804, RFC 8785; independent review posted, one item open (9804 verify pass not independent) | library#46 | S2 | L | review |

### L-011 — the NIST set

**Sponsor decision 2026-09-22: summarised records, not a stub cluster.** We
implement cryptography, so these are core even though ARCH-0001 NG3 defers the
algorithm suite and none of them bears on an open `DEC-*`. This is the worked
example of scope §1: *the "bears on a decision" test is a prompt for judgement,
not a gate.*

All `body: nist`. Each gets a full `summary.md` — bibliographic header,
`maturity`, applicability, implementations searched, limits.

| document | what | maturity |
|---|---|---|
| **FIPS 186-5** | Digital Signature Standard — ECDSA, EdDSA, RSA | `standard` |
| **FIPS 204** | ML-DSA (Module-Lattice) — approved 2024-08-13 | `standard` |
| **FIPS 205** | SLH-DSA (Stateless Hash-Based) — approved 2024-08-13 | `standard` |
| **FIPS 180-4** | Secure Hash Standard, SHA-2 | `standard` |
| **FIPS 202** | SHA-3 and SHAKE — ML-DSA and SLH-DSA depend on it | `standard` |
| **SP 800-208** | Stateful hash-based signatures, LMS/XMSS | `recommendation` |
| **SP 800-186** | Elliptic curve domain parameters | `recommendation` |
| **SP 800-57 Pt 1 Rev 5** | Key management | `recommendation` |
| NISTIR 8610 | Additional signature schemes, round 2 status | `informational` — stub is fine |
| FN-DSA (FALCON) | forthcoming FIPS | stub with locator; nothing to summarise yet |

**FIPS 186-5 is the PROC-0002 stage 8 worked example** the sponsor named: generate
an implementation from the specification, then verify it. Its test vectors have a
real publisher source — **NIST CAVP/ACVP** — which satisfies the stage 8 rule that
vectors come from the source or its publisher and are never generated. If the
student cannot find CAVP vectors for the scheme they implemented, that is a stage
10 failure, not an acceptable outcome.

Post-quantum signatures are in the set deliberately. A signature-centric project
in 2026 that has not read FIPS 204 and 205 will be asked why.

## Parked — deliberately out of scope

| id | task | why |
|---|---|---|
| T-090 | WP4 — OpenPGP introducer import | Out of scope this semester (PLAN-0001 §2) |
| T-091 | WP5 — X.509 import | Out of scope this semester |
| T-092 | Transparency service / receipts | R-O-04 is `Could`; not in the demo floor |
| T-093 | Library federation across peers | Design and document only; do not build |
| T-094 | Nested threshold subjects | v2 |
