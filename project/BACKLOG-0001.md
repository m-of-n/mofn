---
schema: "archdoc/v1"
id: BACKLOG-0001
title: "m-of-n backlog"
short_title: "Backlog"
description: "Task backlog. Each task becomes a GitHub issue; this file is the durable index."
type: backlog
category: process
status: draft
version: "0.13.0"
date: "2026-09-16"
updated: "2026-11-12"
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

## Status at 2026-11-09 — reconciliation

**The file was further behind than the work.** A sweep of both repos — issues,
merged PRs, `prototype/wallet/`, `spec/vectors/`, CI and the library's
`bin/validate` (446 records, 0 scaffolds) — found **26 rows finished but not
marked**, and about a dozen partly done or overtaken. They are corrected below;
each row names its evidence.

- **Done, was open:** T-006d, T-012a, T-012b (merged 2026-11-10, after the sweep), T-024, T-029a, T-033, T-045, T-046,
  T-055, W-1; L-001…L-007, L-011, L-013, L-018, L-021, L-031, L-032, L-033,
  L-034, L-036.
- **Closed 2026-11-09, not owed:** T-030 (ADR-0004 made the encoding concrete;
  `SPEC-0002` Appendix B CDDL is the schema) and T-032 (ADR-0004 closed MD-3's
  narrowing on P1; already stated on T-031).
- **Decided:** T-029c — Python throughout, Tauri withdrawn, the Textual app
  is the UI; W-5 rescoped into `mofn run` (`DECISIONS-0001` item 28). T-054 — #127 §6 had already rejected zipapp for PyInstaller.
- **Searched, not found:** no record that T-013's cut order was ever agreed,
  and no explicit sponsor ruling on L-035. Both rows say what exists and what
  is owed.
- **Newly tracked:** L-037…L-040 (library#89, #69, #110, #133); T-067
  (mofn#110).

**What actually stands between today and the demo floor (Nov 11):** the
engine has no delegation, threshold reduction or name resolution
(`engine/reduce.py` is one hop). T-047's "chain reduces" needs T-041 / W-3.

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
| T-001 | ~~Create GitHub org `m-of-n`~~ — done; DEC-001 accepted 2026-11-06 by `ADR-0006` (it was marked accepted here since 2026-09-21, without an ADR) | D0 | PL | S | done |
| T-002 | ~~Create `mofn` and `library` repos~~ — done, both public and pushed | D0 | PL | S | done |
| T-003 | **Fall 2026 deliverables — definition of done.** `PROC-0004`, aligned to D0–D10. Parent issue mofn#28 with sub-issues | D0–D10 | all | L | doing |
| T-003x | ~~Branch protection~~ — done; residual settings are T-006c | D0 | S1 | S | done |
| T-004 | `CODEOWNERS` → `/spec/` and `/project/` to PL; both students on the catch-all | D0 | S1 | S | done |
| T-005 | ~~DCO check in CI~~ — done, both repos | D0 | S1 | S | done |
| T-006 | ~~Issue + PR templates; labels; milestones~~ — done | D0 | S2 | M | done |
| T-006a | ~~Repo `admin` for both students~~ — done, both repos and the org | D0 | PL | S | done |
| T-006b | Decide faculty access for Mario Lin (read? admin?) — not yet a collaborator or invitee | D0 | PL | S | todo |
| T-006c | Turn on `enforce_admins` now a second reviewer exists — still off in both repos (2026-10-05) | D0 | PL | S | todo |
| T-006d | ~~**Students review each other's PRs**~~ — done: cross-approvals on #122, #124, #131, #145, #147, #149 (2026-11) | D0 | S1+S2 | S | done |
| T-007 | ~~`bin/validate-archdoc` in CI~~ — done | D0 | S1 | M | done |
| T-008 | ~~MkDocs Material site deploying to Pages~~ — done; live at m-of-n.github.io/mofn | D0 | S2 | M | done |
| T-009 | ~~`library` wired as submodule; `bin/lib-sync` working~~ — done | D0 | S1 | S | done |
| T-010 | ~~`bin/wt` worktree helper; document in CONTRIBUTING~~ — done | D0 | S1 | S | done |
| T-011 | ~~Publish draft planning docs to Pages~~ — done | D0 | S2 | S | done |
| T-012 | ~~**Architecture development** — umbrella~~ — **split 2026-11-06** (mofn#6 closed). Its three questions were answered by ARCH-0002 P6, MD-1 and PROC-0004 §8b; strands 1–3 continue as T-027, T-026 and the library. ADR-0002 accepted (T-029d). The remainder is T-012a/b/c | — | PL | XL | done (split) |
| T-012a | ~~ARCH-0001 v0.2.0: proposal folded in; §4.2 one form; ARCH corrected to the SPECs, two gaps kept (§5.5)~~ — done: mofn#145 merged 2026-11-08, #134 closed; `DL-0028`, `ADR-0007` | — | Claude→PL | L | done |
| T-012b | ~~ARCH-0001 target section: supply chain + archives/library (MD-1); AI agents as motivation only~~ — done: ARCH-0001 0.3.0 §2.3 (mofn#152, DL-0032); #135 closed 2026-11-10 | — | S1+S2 | L | done |
| T-012c | Delegation: reconcile R-M-10 (boolean) with SPEC-0004 (integer depth + ranges); `may-speak` vs `trust … about` — mofn#136 | — | PL | M | **decided** 2026-11-06 (1a integer depth, 2a `trust … about`; DL-0025); R-M-10 text landed in ARCH-0001 v0.2.0; **done** 2026-11-07: vectors TV-14…20, E-1…E-4 (DL-0031) |
| T-012x | ~~`design-log/` opened~~ — done; DL-0001 and DL-0002 written | D0 | PL | S | done |
| T-013 | Agree and commit the cut order (PLAN-0001 §12) — **still not agreed.** mofn#7's done-when was "all three have signed off in the PR". PLAN-0001 0.7.0 §12 (#156, `DL-0036`) put the order to all three and says it is agreed "when the sponsor and both students approve the PR that carries it". #156 merged 2026-11-13 **with no approvals**, and #7 closed with it. §12 is on `main`, but its own condition is unmet, and rows 6, 7 and 11 are still unanswered. **Owed:** approvals from the sponsor and David, recorded on #7 or in a §12 PATCH, plus the three answers | D0 | all | S | review — sign-off owed |

## I1 — Library & research · Oct 1–14 · D1 D2 D3

| id | task | del | own | sz | status |
|---|---|---|---|---|---|
| T-020 | D1 v0.1 — construction best practice (`library/docs/construction.md`) — **at risk**: last edit 2026-09-16; FX-1 (`docs/extraction.md`) now carries much of it | D1 | S2 | L | doing |
| T-021 | ~~Seed 10 records by hand to prove the schema~~ — done | D2 | S2 | M | done |
| T-022 | Ingest adapters verified for each type: pdf, url, ietf, xlsx, md, book, repo, consortium, hierarchy | D2 | S2 | M | doing |
| T-024 | ~~Library to ~40 records across the topics~~ — done: 446 records, 0 scaffolds (library `bin/validate`, 2026-11-09); library#45 closed 2026-11-06 via #95–#124 | D2 | S2 | L | done |
| T-025 | Report: *context* — **drafted** as `R-0005` (research/0005-context). Synthesis pass over R-001 §1–§6/§11/§12 and R-0004 §8; **no retrieval pass**, stated as a limitation in its `searches.md` | D3 | S1 | L | review |
| T-026 | Report: *mechanism* — **drafted** as `R-0006` (research/0006-mechanism), v0.3.0. The comparative anatomy of in-toto/DSSE, SCITT/COSE, SPKI, PICS and VC/DID in one frame (§2.2–§2.5; PICS and VC cells marked unsourced, `unverified.md`), the six conditions, all four DEC-002 candidates scored, DEC-004's meet-vs-accumulation evidence. Decides nothing; §3.9 states where the evidence sits relative to MD-3 **and `ADR-0003` D2**, and §3.13 reads conditions (5) and (6) against `SPEC-0002`/`SPEC-0003`. §4.6–§4.7: the accepted core's range algebra, and whether T-042 is subsumed by it — **raised for T-042's owner, not decided**. Owned jointly (#100 assigned to both, 2026-10-20) | D3 | S1+S2 | L | review |
| T-027 | Report: *uptake/applications* — incl. SPKI and PICS failure-to-adopt — **drafted** as `R-0004` (research/0004-uptake-and-applications), merged in mofn#87 on 2026-10-12. **The row was stale, not the work** | D3 | S2 | L | review |
| T-028 | Topic notes answered for `namespace-governance`, `canonical-encoding` — canonical-encoding answered; namespace-governance partial (library#128). **5 of 22 topics answered** (artifact-statements, canonical-encoding, delegation-models, sbom, scitt); 12 partial | D3 | PL/S1 | M | doing |
| T-029a | ~~Schema scenarios (3–5, incl. email delegation) and Product Spec personas, GAP-1 (MD-1)~~ — done: `UC-0001`, eight scenarios each with personas, statements, evaluation and failure cases, incl. email delegation (mofn#104, 2026-10-16) | D3 | S1+S2 | M | done |
| T-029b | Product Spec, PLAN-0002 v0.2 — GAP-4 real sketches (Ndewedo, Oct 14), GAP-6 course dates (PL) | — | PL+S2 | M | doing |
| T-029c | ~~Confirm Tauri for the wallet GUI (MD-7)~~ — **decided 2026-11-09: Python throughout, Tauri withdrawn** (`DECISIONS-0001` item 28, `DL-0038`). MD-7 was never confirmed, and W-6 had already shipped Textual + PyInstaller (#127 §6). `PLAN-0002` §5.1 and `PLAN-0004` §4 updated. **The Textual app is the UI** (`mofn run`); no windowed GUI, W-5 rescoped | D8 | S2 | S | done |
| T-029d | ADR-0002: accept P2, P3, P5, P6 provisionally (MD-2) — **drafted** (#83, `proposed`); condition 6(b) **met** by ARCH-0002 v0.7.0, condition 6(a) **met** 2026-10-16 (v0.7.1 carries a reviewer, `reviewed: true`). **`SPEC-0003` §7.1 cites P5 by name inside the Definition Publisher conformance class** (ADR-0002 §6a), so a governing spec rests on a draft principle. What is left is the sponsor's call: accept P5 **as amended**, or accept P2/P3/P6 and P5 **as drafted**, holding P5.1/P5.2 for a reader who did not write them | — | ~~Claude~~→**PL** | M | **done** — accepted 2026-11-06 by `ndewedo-newbury`, P5 as amended (`ADR-0002` §9, `DL-0024`); second reader for P5.1/P5.2 still owed |
| T-029e | ~~Close T1-A in DECISIONS-0001 citing MD-1~~ — done 2026-10-10 in DECISIONS-0001 v0.2.0; PLAN-0002 §2 carries MD-1. The row, not the work, was stale | — | Claude | S | done |

## I2 — Schema + DEC-002 · Oct 15–28 · D4 D5

| id | task | del | own | sz | status |
|---|---|---|---|---|---|
| T-030 | ~~WP1 — encoding-neutral schema for ARCH-0001 §4 logical types~~ — **closed 2026-11-09, not owed.** The neutral schema was the hedge for a deadlocked DEC-002 (`PLAN-0001` §12 risk 4); ADR-0004 accepted option 5, and `SPEC-0002` Appendix B (CDDL) is the schema. `spec/schema/README.md` is stale | D4 | S1 | L | done (closed) |
| T-031 | Fixtures: `NameCert`, `AuthzCert` **with threshold subject**, `ArtifactStatement` — in **option 5** (`ADR-0004`). In `spec/vectors/ksa-core/`: threshold TV-9…11 and N-7…10, `NameCert` TV-13 (TV-1/TV-2 never covered it, `SPEC-0002` §8.3), `ArtifactStatement` TV-4; all round-trip in `prototype/wallet/tests`. **The option-2 comparison is not owed** — `ADR-0004` closed MD-3's narrowing on P1. `trusts` distinctness goes to `SPEC-0002` with condition (5) — `DL-0019` | D5 | S1 | L | **review** — waiting on a second reader |
| T-032 | ~~Score option 5 against option 2 incl. namespace governance~~ — **closed 2026-11-09, not owed:** `ADR-0004` closed MD-3's narrowing on P1 (see T-031) | D5 | S1 | M | done (closed) |
| T-033 | ~~ADR for DEC-002~~ — done: `ADR-0004` (option 5, KSA-CBOR), ARCH-0001 updated, mofn#117 (2026-10-26) | D5 | PL | M | done |
| T-034 | Canonicalization idempotence + round-trip tests in CI — **now also carries P5.1's acceptance test**: reject every RFC 8949 FX-1 negative fixture in one pass, no re-encoding (ARCH-0002 v0.7.0). **In CI already:** N-1…N-11 rejected at their stated step (`tests/test_vectors.py`), encoder reproduces every TBS, decoder never re-encodes, non-canonical inputs rejected (`tests/test_ksa_cbor.py`). **Left:** the full RFC 8949 FX-1 negative set | D5 | S2 | M | doing |
| T-035 | ~~Resolve R-M-12: requirement row, or ARCH-0002?~~ — ARCH-0002, accepted as P1 via ADR-0001 | — | PL | M | done |

## I3 — Reduction · Oct 29–Nov 11 · D6 · **DEMO FLOOR**

| id | task | del | own | sz | status |
|---|---|---|---|---|---|
| T-040 | Name resolution: `Name` → `KeyId` via `NameCert` chains (§4.3 step 1) | D6 | S1 | L | todo |
| T-040s | SPEC-0004: specify SDSI name resolution — `Name` principals, compound names (ARCH-0001 §5.5) — mofn#143. Blocks T-040 | D6 | S1 | L | todo |
| T-048 | ~~SPEC-0002 §7.2: a locator target must travel with a digest or description (R-M-07)~~ — done: SPEC-0002 0.6.0 withdraws target type 5; N-11; DL-0030 — mofn#144 | D6 | S2 | S | done |
| T-049 | Wallet test: DV-2/TV-13 rendered sentence — the clause `ADR-0007`'s acceptance test still owes | D6 | S2 | S | **done** 2026-11-07 (`test_delegation.py`, DL-0031) |
| T-066 | Renderer: show a description target (`SPEC-0002` §7.2 type 6) by its description, not as "a described object"; `SPEC-0003` §10 is silent — ARCH-0001 §2.3.2 | D6 | S2 | S | todo |
| T-067 | Spec lane: propose ARCH-0001 §6 rows (R-0006 §2.5) and `SPEC-0003` §6 pattern containment — mofn#110, unassigned | D6 | — | M | todo |
| T-065 | Wallet engine: delegation paths (SPEC-0004 §6.3); move E-1…E-4 from the test walker to the engine | D6 | S2 | M | todo |
| T-041 | 5-tuple reduction: tag ∩, validity ∩, delegation (§4.3 step 2) | D6 | S1 | L | todo |
| T-042 | Minimal tag profile — opaque bytes + `bytes-equal` (DEC-004 minimum). *Possibly subsumed by `SPEC-0003` `delegation: 1` — `R-0006` §4.7; owner's call* | D6 | S1 | M | todo |
| T-043 | *k*-of-*n* threshold subjects, keys only, no nesting | D6 | S2 | L | todo |
| T-044 | Statement acceptance (§4.3 step 3), kept separate from reduction — the verdict's `acceptance` line is already separate (W-1); template conformance only | D6 | S2 | M | doing |
| T-045 | ~~Verifier output reports the three separately (R-O-06)~~ — done: the six-line verdict (integrity, authenticity, names, authorization, acceptance, semantics), W-1; `fixtures/golden/` | D6 | S2 | M | done |
| T-046 | ~~Published test vectors under `spec/vectors/`~~ — done: `spec/vectors/ksa-core/` TV-1…20, N-1…11, E-1…4, checked in CI. `spec/vectors/README.md` still says "empty until DEC-002" | D6 | S1 | M | done |
| T-047 | **Demo: chain reduces; break a link; verifier explains which and why** — `demo/slice.sh` breaks a link and the verdict names it, **for one hop**; a chain needs delegation in the engine (T-041 / W-3) | D6 | all | M | doing |

## I4 — Mappings & app · Nov 12–25 · D7

| id | task | del | own | sz | status |
|---|---|---|---|---|---|
| T-050 | WP2 — `MAP-0001` SPKI/SDSI S-expression ↔ native | D7 | S1 | L | todo |
| T-051 | WP3 — `MAP-0002` in-toto Statement ↔ `ArtifactStatement` | D7 | S1 | L | todo |
| T-052 | Round-trip a real SLSA v1.1 provenance from a public release | D7 | S1 | M | todo |
| T-053 | Record interchange losses in the §6 matrix (R-I-01) | D7 | S1 | M | todo |
| T-054 | App packaging — ~~single-file zipapp~~ **one PyInstaller build per OS**: #127 §6 rejected zipapp (cannot load PyNaCl's extension). Lands as W-6's `release.yml` | D8 | S2 | M | todo |
| T-055 | ~~Demo: valid-but-**unauthorized** key → distinct verdict~~ — done: `fixtures/golden/unauthorized.txt`; slice case ②′ | D7 | S2 | M | done |

## I5 — Polish · Nov 26–Dec 4 · D8 D9 D10

| id | task | del | own | sz | status |
|---|---|---|---|---|---|
| T-060 | App download live on Pages, with install docs | D8 | S2 | M | todo |
| T-061 | Market & applications research | D9 | PL/S2 | L | todo |
| T-062 | `LIMITATIONS.md` final — what this does not prove | D10 | all | S | todo |
| T-063 | Final report | D10 | all | L | todo |
| T-064 | Demo rehearsals ×3 | D10 | all | M | todo |

---

## Wallet and demo slice — `W-*` · issues #65–#69, #127

Opened 2026-10-05 against `PLAN-0004` and parent #31 (T-003.5, the demo floor).
Tracked here from 2026-10-11; before that they existed only as issues.
`W-1` is the engine everything else calls — **nothing in this lane starts
before it runs.**

| id | task | issue | del | own | sz | status |
|---|---|---|---|---|---|---|
| W-1 | ~~**Wallet engine v0**~~ — done: #65 closed 2026-11-04 (PRs #122, #125); `mofn` CLI, KSA-CBOR, V1–V9, six-line verdict, signature checking inside `check` | #65 | D6 | S1 | XL | done |
| W-2 | **Second domain** — one-page scenario per MD-1 target (supply chain, archives/library) incl. the fail-authorization case and three personas; archives domain file v0 (`record-review`, renderings table, `--lang es`); five-view sketches replacing Product Spec §6.5 | #66 | D6/D8 | PL | L | review — APP-0002/0003 scenarios, `domains/archives/` through the same `make`/`check` with no engine change, `--lang` (wallet 0.4.0), APP-0004 sketches, PLAN-0002 0.4.0 §6.5 (DL-0032). Oct 14 part was 4 weeks late |
| W-2b | **Converge the archives vocabularies — starts when W-3 merges.** DV-3 `library-review` (#152, vector) and `archives` v1 (#154, demo) become one published vocabulary (e.g. `library-review` v2 + `summarized`); the demo moves to it with its delegation path; `domains/archives/` retired or regenerated; APP-0003 § Setup/Steps and goldens updated (APP-0003 § *Two archives vocabularies*, DL-0033) | #66 | D6/D8 | PL | M | blocked — on W-3 (#67) |
| W-3 | **Delegation with short expiry** — `may-speak` chains in `reduce`, intersecting topic *and* validity; expired or out-of-topic → `authorization FAIL` naming the broken link. **Short expiry is the revocation mechanism**; there is no revocation list | #67 | D6 | PL | L | todo — Nov 11 |
| W-4 | **Weekly demo slice owner** — grow and run `demo/slice.sh` every Monday, post the output on the issue. Three cases minimum: green, `authorization FAIL`, `integrity FAIL` | #68 | D6 | S2 | M | doing — weekly |
| W-5 | ~~**Mac GUI** — local desktop app~~ **Rescoped 2026-11-09 into `mofn run`** (`DECISIONS-0001` item 28: Textual is the UI). What #69 adds beyond W-6: on every verdict in the Check tab, the **attribute associations** — who signed (key / named principal), topic (domain + type), the subject's digest, and standing (root → delegation → key, or "no standing"). Calls the engine; reimplements no crypto | #69 | D8 | S2 | M | todo — Dec |
| W-6 | **A way in to the engine** — a bare `mofn` prints the menu (= `mofn -h`), `mofn --version`, one line for a missing dependency; `mofn run`, the wallet as a terminal app — forms for keys, trust, sign and check, each showing the command it runs, and a Learn tab that runs nothing; DV-1 ships as the example vocabulary (0.2.0, DL-0023); `key list`, `key export`, `hash` from `gpg`, the rest of `gpg` mapped or left out (DL-0022); `ci.yml` on Linux, macOS and Windows. Chip: `release.yml`, one self-contained build per OS, `SHA256SUMS`, pre-releases from `wallet-v0.2.0` (David's half lands as one PR, `feat/w6-tui`, so `main` never holds 0.1.0 and there is no `wallet-v0.1.0`). Prototype only; `src/` stays empty | #127 | D6 | S1 engine, S2 release | L | doing — Nov 11 |

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
| L-001 | ~~`summary.md` primary; `distilled.md` = requirements extraction~~ | #1.1 | — | L | done — library#3 merged 2026-09-21 |
| L-002 | ~~`status: stub` for references that bear on nothing yet~~ | sponsor | — | S | done — library#3 merged 2026-09-21 |
| L-003 | ~~Controlled tag vocabulary: subject / body / role~~ | #1.6,10 | — | M | done — library#3 merged 2026-09-21 |
| L-004 | ~~`maturity` on RFC 2026 levels~~ | sponsor | — | S | done — library#3 merged 2026-09-21 |
| L-005 | ~~OKF alignment — YAML front matter, documented extensions~~ | #1.11,12 | — | M | done — library#3 merged 2026-09-21 |
| L-006 | ~~`implementations` field — open source + commercial~~ | #1.3 | — | S | done — library#3 merged 2026-09-21 |
| L-007 | ~~`research/` for archived method research~~ | sponsor | — | S | done — library#3 merged 2026-09-21 |
| L-010 | ~~Fill out the 9 existing records~~ — superseded by library#45 (264 scaffolds) | #1.2 | S2 | L | parked |
| L-011 | ~~**NIST cryptographic algorithms — summarised records, not stubs**~~ — done: library#42 merged 2026-10-05, library#8 closed | #1.4 | S1 | L | done |
| L-012 | ~~NIST digital signature specifics~~ — folded into L-011 | #1.2 | S1 | — | done |
| L-013 | ~~Attestation specifications sweep — RATS, EAT, CoRIM, TPM, Confidential Computing~~ — done: 25 of 26 written, library#99 merged 2026-11-02 | #1.2,7 | S1 | L | done |
| L-014 | Trust management publications — deep research gather | #1.7 | S2 | L | todo |
| L-015 | Implementation search across all records — open source + commercial — 280 of 446 records carry `implementations`, filled in the #45 sweep; no standalone pass yet | #1.3 | S2 | M | doing |
| L-016 | Organised bibliography for review; confirm the schema supports it — `bin/export` already emits `index/bibliography.md`, CSL-JSON, BibTeX; not organised for review, unpublished (`docs/gaps.md`) | #1.6 | S2 | M | doing |
| L-017 | Applicability review pass over all records after first summarisation — library#111 merged (partial), **library#132 open** | #1.8 | PL | M | doing |
| L-018 | ~~Define ingestion **scope**~~ — done: `docs/scope.md`, library#5 merged 2026-09-22 | #1.10 | PL | S | done |
| L-019 | Archive the method research behind `docs/construction.md` — sources were discarded | sponsor | S2 | M | todo |
| L-020 | ~~Multi-agent ingestion plan~~ — done: PROC-0002, and FX-1 `docs/extraction.md` for spec records | #1.5 | PL | M | done |
| L-021 | ~~`mofn/research/` — D3 reports with `sources.md` and `searches.md`~~ — done: R-0001…R-0007, each with both | sponsor | S1 | S | done |
| L-022 | Promote recurring free tags into `schema/tags.yaml` (rule of three) | #1.6 | S2 | S | todo |
| L-030 | ~~FX-1 full extraction standard — enforced in CI~~ — library#32 | sponsor | Claude | M | done |
| L-031 | ~~FX-1 extraction of the CBOR/COSE set, ranked~~ — done: library#88 merged 2026-10-23 (23 records at `profile: full`); #39 closed | library#39 | S1 | XL | done |
| L-032 | ~~SCITT full extraction~~ — done: library#58 merged 2026-10-11; #40 closed | library#40 | S1 | L | done |
| L-033 | ~~Fill the 264 unwritten scaffolds~~ — done: library#45 closed 2026-11-06 (#95–#124); 0 scaffolds | library#45 | S2 | XL | done |
| L-034 | ~~YAML reader block scalars, scaffold inventory, duplicate detection~~ — done: library#48 merged 2026-10-05; #43, #35 closed | library#43/#35/#45 → #48 | Claude | M | done |
| L-035 | **Sponsor decision:** accept library#42's FX-1 carve-out, or keep #32's rule — **in force, never explicitly ruled.** The carve-out is in library `docs/extraction.md` ("Scope amended 2026-10-03 (#8, PR #42)": FX-1 fires on intent to extract, not on contact). library#42 was written by Ndewedo-Newbury and merged 2026-10-05 by the sponsor (`nymble`) **with no review and no comment**. Later work relies on it (DL-0006, DL-0007). The merge is the only act; **owed:** one line from the sponsor accepting it | library#42 | PL | S | review — sponsor to confirm |
| L-036 | ~~First student FX-1 extractions — RFC 9804, RFC 8785~~ — done: library#46 merged 2026-10-05 | library#46 | S2 | L | done |
| L-037 | FX-1 extraction of the R-0006 inventory (VC ×3, DSig, PICS labels, in-toto attestation, RFC 9162, SPKI structure) — 3 of 5 PRs merged | library#89 | — | L | doing |
| L-038 | FX-1 debt: 19 spec records from the Threat-Radar fold-back | library#69 | — | L | todo |
| L-039 | Paywalled records: source text not held | library#110 | — | M | todo |
| L-040 | `bears_on` mixes two decision registers (mofn and tmodel) under colliding ids | library#133 | — | S | todo |

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

**FIPS 186-5 is the PROC-0002 stage 8 worked example** the sponsor named: build a
harness that drives a vetted library through the specification, then verify it —
never a generated primitive (PROC-0002 v0.3 §2). Its test vectors have a
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
