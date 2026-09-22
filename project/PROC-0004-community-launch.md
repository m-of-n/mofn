---
schema: "archdoc/v1"
id: PROC-0004
title: "Fall 2026 deliverables — definition of done"
short_title: "Fall 2026 deliverables"
description: "What ships by 2026-12-04, what done means for each deliverable, and the site structure. Aligned to the student goals in PLAN-0001."
type: process
category: process
status: draft
version: "0.2.0"
version_policy: "semver; MINOR = deliverable or criterion added"
date: "2026-09-22"
updated: "2026-09-22"
decision_makers: []
reviewers: []
needs_review: true
reviewed: false
canonical_path: project/PROC-0004-community-launch.md
companion:
  - project/PLAN-0001-project-plan.md
  - project/BACKLOG-0001.md
defers_to: ARCH-0001
backlog: T-003
---

# Fall 2026 deliverables

**Status: draft.** T-003. **Scope: what ships by CS Night, 2026-12-04.**

This defines **done** for each deliverable in `PLAN-0001` §2 (D0–D10). It is the
student-facing scope. Anything not listed here is §11, *beyond Fall 2026*, and
must not compete for semester time.

**Ordering principle:** the demo floor (D6) lands **2026-11-11**, three weeks
early, and the cut order in `PLAN-0001` §12 protects it. Everything below is
either in the floor or explicitly cuttable.

---

## 1. Harness and repository hygiene — D0

Largely complete. What remains is cheap and unglamorous.

- [x] Two repos, CI, Pages, branch protection, DCO, templates
- [x] `archdoc/v1` contract enforced mechanically
- [ ] `LICENSE` in both repos — Apache-2.0 code, CC-BY-4.0 specs and docs
- [ ] SPDX identifiers in source files
- [ ] **Third-party content audit** — confirm no third-party bytes are
      redistributed in `library/`; every `quotes.md` excerpt has a locator
- [ ] Attribution on every derived artifact: what it came from, by what

## 2. Library and bibliography — D1, D2

- [ ] **D1** `docs/construction.md` complete, revised at each increment with what
      we got wrong — exit criterion is *a second person adds a correct record
      from the document alone*
- [ ] **D2** library populated across the seven topics, `summary.md` written for
      each record — not template text
- [ ] **L-011** the NIST set summarised (FIPS 186-5, 204, 205, 180-4, 202;
      SP 800-208, 800-186, 800-57)
- [ ] `index/` regenerated and committed: records, versions, crosswalk,
      bibliography, frontier, by-decision
- [ ] `usefulness` verdicts recorded **including the negative ones**
- [ ] Ingestion skills documented and reusable

## 3. Research reports — D3

Three reports, markdown, published, each citing `library@<commit>`.

- [ ] **Context** — why provenance, why now; the historic gap
- [ ] **Mechanism** — comparative anatomy; the evidence base for DEC-002/DEC-004
- [ ] **Uptake & applications** — adoption evidence, and the **failure-to-adopt
      analysis of SPKI/SDSI and PICS**. Feeds D9
- [ ] `research/` carries `sources.md` **and `searches.md`** for each

## 4. Specification — D4, D5, D7

- [ ] **D4** encoding-neutral schema for the ARCH-0001 §4 logical types (WP1)
- [ ] **D5** DEC-002 decision package: round-trip fixtures for the surviving
      options, scored — then an `ADR`
- [ ] **D7** mapping specs: SPKI/SDSI ↔ native (WP2), in-toto ↔
      `ArtifactStatement` (WP3), with losses documented per R-I-01
- [ ] `spec/vectors/` published — **the interoperability contract**, consumable
      by an implementation that has only that directory

## 5. Implementation and demo — D6 · **the floor, 2026-11-11**

- [ ] Name resolution: `Name` → `KeyId` via `NameCert` chains
- [ ] 5-tuple reduction: tag ∩, validity ∩, delegation
- [ ] *k*-of-*n* threshold subjects, keys only
- [ ] Statement acceptance kept separate from reduction (§4.3)
- [ ] Verdict reports the three separately (R-O-06)
- [ ] **Demo scripted, rehearsed, and recorded.** A demo that exists only live
      has not shipped
- [ ] Runs from a clean clone with documented prerequisites

## 6. Application — D8

- [ ] Packaged single-file zipapp; install and quick-start docs
- [ ] **Checksums published**, release **signed**
- [ ] **Dogfood: the release carries an `m-of-n` statement over its own digest,
      and our verifier accepts it.** This is the thesis demonstrated on our own
      artifact — if we cannot attest our own release, we have not finished
- [ ] Download page with verification instructions a stranger can follow
- [ ] **App notes** — attest an artifact, verify one, break one, read a mark

> **SBOM is not a Fall 2026 deliverable.** It is not yet defined for this project
> — what it would cover, in which format, and against which consumer is an open
> question, and inventing one to look complete would be worse than omitting it.
> Recorded in §11.

## 7. Security posture

A cybersecurity project without a disclosure policy is a liability. These are
small and they are not optional.

- [ ] **`SECURITY.md`** — private channel (GitHub Security Advisories), scope,
      and a response-time commitment we can actually meet
- [ ] **Threat model** — what we defend against and what we do not
- [ ] **`LIMITATIONS.md` final** — *proves origin and integrity, not truth*
- [ ] Dependencies pinned; **no hand-rolled primitives**, audited and stated

## 8. The site

Cross-cutting, and the most public artifact. Detail in §9.

## 9. Site structure — what best-in-class looks like

Two established patterns, adopted deliberately.

### 9.1 The landing page

Strong open-source landing pages make the thing **immediately tryable** rather
than asking a reader to absorb marketing first. Ours must carry, in order:

1. **What it is, in one plain line** — naming the category, not the cleverness.
2. **What it is *not*, within the first five lines.** *Proves origin and
   integrity, not truth.* Most projects bury this; for us it is the honest
   headline and it pre-empts the first objection.
3. **A code snippet that works** — attest something, verify it, in under ten
   lines. No signup, no service.
4. **A trust layer** — status (research prototype, one semester), licence,
   sponsor, institution. Stated plainly rather than implied by polish.
5. **One zero-friction next step** — download, or clone-and-run.

### 9.2 Documentation — Diátaxis

Four kinds, kept apart, because mixing them is what makes documentation
unusable. Each answers a different need:

| kind | need | ours |
|---|---|---|
| **Tutorial** | learning, guided | *Your first attestation* — start to verified verdict, hand-held |
| **How-to** | a task, by someone who already knows | *Verify a release* · *Define a type* · *Delegate authority* · *Add a library record* |
| **Reference** | facts, complete and undistracted | CLI reference · the specification · `spec/vectors/` · the schema |
| **Explanation** | understanding | ARCH-0001, ARCH-0002, the ADRs, *why key-centric*, *why not X.509* |

The common failure is a "guide" that is three of these at once. Reference must
be dry and complete; tutorial must not explain; explanation must not instruct.

### 9.3 Sections this project specifically needs

- **Decision register** — `DECISIONS-0001`, public, with open decisions visibly
  open. Publishing what is *undecided* is unusual and it is the honest move for
  a research prototype.
- **Limitations** — its own page, linked from the landing page.
- **Library / bibliography** — a reading path for a newcomer, not just an index.
- **Download** with verification instructions.
- **Governance** — how decisions are made. ARCH-0001 §9 already is one; say so.
- **Roadmap** — what is in this semester and what is beyond it.
- **Glossary** — `GLOSSARY-0001`, once the collisions are resolved.

### 9.4 Mechanics

- Generated nav (`bin/manifest`); **never hand-maintained** — it rotted once and
  took the site down.
- Every page states its **status**; **nothing draft reads as settled**.
- Builds `--strict` in PR checks, not only on deploy.
- Readable on a phone; no build step for a reader.

## 10. Presentation and final report — D10 · **hard date 2026-12-04**

- [ ] Final deck; **rehearsals ×3**
- [ ] Demo runs on presentation hardware, **offline**, from a clean clone
- [ ] One-page summary / poster
- [ ] Each student's contribution stated — portfolio material
- [ ] Final report, including the **P-SSCRM task mapping**
- [ ] **D9** market and applications research

---

## 11. Beyond Fall 2026 — explicitly not this semester

Listed so the omissions read as decisions, and so nobody spends student time
here. All belong to **T-012** (architecture development) or a later cycle.

- **SBOM for the release** — not yet defined (§6)
- **OpenSSF Best Practices badge** — baseline series; worth doing, not now
- **Scorecard** and dependency automation
- **Announcement to the broader community** — the IETF SCITT working group,
  OpenSSF, the capability-systems community. Requires an architecture
  specification that does not yet exist
- `CODE_OF_CONDUCT.md`, contributor on-ramp, `good-first-issue` triage
- Transparency-service receipts (R-O-04 is `Could`)
- OpenPGP and X.509 import (WP4, WP5)

## 12. What we do not claim

A **one-semester research prototype**. Not audited, not a CA, not a WebPKI
replacement. **It proves origin and integrity, not truth.** DEC-002 … DEC-009
are **open by design and marked open**.
