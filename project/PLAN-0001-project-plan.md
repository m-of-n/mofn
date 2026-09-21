---
schema: "archdoc/v1"
id: PLAN-0001
title: "Project plan — semester execution, repo, library, and team"
short_title: "Project plan"
description: "Execution plan for the CS690 project. Subordinate to ARCH-0001 for all architecture."
type: plan
category: process
status: draft
version: "0.4.0"
date: "2026-09-16"
updated: "2026-09-16"
authors:
  - role: planner
    id: conversation-claude-opus-5
decision_makers: []
reviewers: []
needs_review: true
reviewed: false
supersedes: ["PLAN-v1-superseded", "PLAN-v2-superseded"]
reflects: "ARCH-0001-PROPOSAL-v0.2.0 rev.2 (sponsor corrections 2026-09-16)"
canonical_path: project/PLAN-0001-project-plan.md
companion:
  - spec/ARCH-0001-authorization-attestation.md
defers_to: ARCH-0001
constraints:
  architecture_source_of_truth: ARCH-0001
  no_invented_decisions: true
agent_notes: >
  This document plans execution only. It does not decide architecture.
  Every architectural question routes to ARCH-0001 open decisions
  DEC-001..DEC-005, DEC-007 (DEC-006 withdrawn). Do not mark any DEC accepted from this file.
---

# Project plan — CS690 Fall 2026

**Owners:** Paul Lambert (sponsor & SR) + two students
**Plan date:** 2026-09-16 · **Demo:** CS Night, 2026-12-04 · **Weeks remaining:** 11
**Architecture source of truth:** `ARCH-0001` v0.1.0

---

## 0. Correction notice

Plan v2 conflicted with ARCH-0001 and is superseded. Three errors, corrected here:

1. **v2 said "not implementing SPKI/SDSI — prototype only."** Wrong. ARCH-0001
   G3/G4 and R-M-03…R-M-06 make SPKI-shaped reduction, tag intersection,
   threshold subjects, and SDSI local names **native requirements**. The correct
   statement is narrower: *we do not inherit SPKI's encoding or adopt RFC 2693 as
   our specification; the information model is SPKI-shaped by design.*
2. **v2 marked the encoding "[decided]"** as YAML + deterministic CBOR + CDDL.
   That invents an accepted decision. **DEC-002 is open** with four options.
   Reframed below as input to DEC-002, with an acceptance test.
3. **v2 invented names** ("KSA", org `legible-provenance`). **DEC-001 is open.**
   This plan uses `PROJECT` as a placeholder throughout.

**v0.3.0 → v0.4.0.** Sponsor review of 2026-09-16 produced three further
corrections, folded in below: CBOR and COSE extension points are centrally
defined and therefore not key-centric; a readable *authoring* format is not
required, though *display* forms matter and tie to UI; and RFC 9804 is
historical. §7.1 and §13 are rewritten accordingly.

Per ARCH-0001 §9, this file proposes; it does not ratify.

---

## 1. What this plan adds to ARCH-0001

ARCH-0001 defines the model, requirements, interchange matrix, open decisions,
and work packages WP0–WP7 — deliberately **not scheduled**. This plan supplies
exactly what ARCH-0001 leaves out:

- scheduling of WP0–WP7 against eleven weeks and two students
- repository and publication structure
- the bibliographic library (shared, distributed, offline)
- research reports, market research, the application, the demo
- team interaction protocol

**Goal statement** (Paul, 2026-09-16), which ARCH-0001 serves:

> Advances in trust, provenance, and attestation through **AI-assisted protocol
> design**, enabling **key-centric semantic assertions**.

Two of the three are already in ARCH-0001: key-centric principals (G1) and
statements about artifacts (G5). The two this plan must instrument:

- **AI-assisted protocol design as method** — §8. Must be captured from day one
  or it is a story told afterwards, not evidence.
- **Semantic** assertions — the human-legible meaning layer. ARCH-0001 has
  `PredicateType` and `Predicate` but does not yet specify how a predicate
  *renders to a person*. Proposed as **DEC-007** (§7.3).

---

## 2. Deliverables

Each is a GitHub milestone, lands via pull request, has one named owner.
`S1`/`S2` = students, `PL` = Paul.

| ID | Deliverable | ARCH link | Owner | Due |
|---|---|---|---|---|
| **D0** | **Harness** — org, repos, CI, Pages, library skeleton, doc schema, templates | WP0 | S1+S2 | Sep 30 |
| **D1** | **R0: library construction best practice** — iterates all semester | — | S2 | Oct 3 (v0.1) |
| **D2** | **Bibliographic library** — references, typed cross-refs, distilled artifacts | §10 refs | S2 | Oct 14 (v1) |
| **D3** | **Research reports** — *context*, *mechanism*, *uptake/applications* | §3 | S1+S2 | Oct 14 |
| **D4** | **Encoding-neutral schema** for §4 logical types | **WP1** | S1 | Oct 21 |
| **D5** | **DEC-002 decision package** — round-trip fixtures for all four options → ADR | DEC-002 | S1+PL | Oct 28 |
| **D6** | **Reduction algorithm + test vectors** — *demo floor* | **WP6**, DEC-004 min | S1+S2 | Nov 11 |
| **D7** | **Mapping specs** — SPKI↔native, in-toto↔ArtifactStatement | **WP2, WP3** | S1 | Nov 25 |
| **D8** | **Application** — packaged, downloadable from Pages | — | S2 | Dec 1 |
| **D9** | **Market & applications research** | — | PL+S2 | Dec 1 |
| **D10** | **CS Night demo + final report** | — | all | Dec 4 |

WP4 (OpenPGP) and WP5 (X.509 import) are **out of scope this semester** — named
here so the omission is deliberate. See §11 risk 5.

Architecture and implementation detail are markdown in the repo, published to
Pages, in `archdoc/v1` front-matter form. There is no design document anywhere
else.

---

## 3. Repository structure

### Organization
A GitHub **Organization**, three **Owners**. Slug blocked on **DEC-001** — do not
create the org until DEC-001 is accepted, because renaming an org breaks every
published URL, including Pages and any citation made in the interim. This is the
one decision that genuinely blocks D0, so take it first.

### Two repos — and the answer on a Pages repo

**No separate repo for web pages.** Docs versioned alongside what they document
is the point; a split site repo drifts within a month. Publish from `docs/` in
the main repo via GitHub Actions.

**Yes, a separate repo for the library** — not for size, but because the
distributed-library design (§4) requires it to be independently cloneable,
forkable, and citable by projects that are not this one.

```
github.com/<DEC-001>/
├── <DEC-001>/          monorepo: artifacts/, src/, docs/ (→ Pages)
└── library/            bibliographic library, standalone
```

`library/` is a **git submodule** in the monorepo, pinned to a commit. That pin
is not bureaucracy: a report's bibliography is reproducible because it cites
`library@<commit>`. Ship `bin/lib-sync` so neither student ever types submodule
syntax.

### Monorepo layout — conforming to ARCH-0001 `canonical_path`

```
<DEC-001>/
├── README.md                    what this is; what it does NOT prove
├── LIMITATIONS.md               the honest-problem statement
├── CONTRIBUTING.md              branch/PR rules, DCO, archdoc/v1 schema
├── artifacts/
│   ├── docs/
│   │   ├── ARCH-0001-authorization-attestation.md      ← source of truth
│   │   ├── ARCH-0001-CHANGELOG.md
│   │   ├── PLAN-0001-project-plan.md                   ← this file
│   │   ├── ADR-NNNN-*.md                               ← accepted DEC-*
│   │   └── MAP-NNNN-*.md                               ← WP2–WP5 mappings
│   ├── schema/                  WP1 output; encoding-neutral first
│   └── vectors/                 test vectors — published artifact, not fixture
│       └── NNN-name/{input,canonical,digest,notes.md}
├── src/                         model/ reduce/ names/ encode/ verify/ app/
├── prototype/                   spikes; never ships
├── design-log/                  AI-assisted design record (§8)
├── docs/                        → GitHub Pages (MkDocs Material)
├── library/                     → submodule
├── bin/                         lib-sync, vectors-gen, validate-archdoc, release
└── .github/                     workflows, ISSUE_TEMPLATE, PULL_REQUEST_TEMPLATE
```

`bin/validate-archdoc` enforces the `archdoc/v1` front matter in CI — including
ARCH-0001 §9.5, *version and updated must change together*. Process rules that
are not mechanically enforced are not followed by week 6.

### Decided-now, low-cost
- Code **Apache-2.0** (patent grant matters for a protocol); specs and docs
  **CC-BY-4.0**; library notes **CC-BY-4.0**. Third-party PDFs never committed.
- **DCO** (`Signed-off-by`), not a CLA — one line, CI-enforced.
- `main` protected: no direct pushes, one approving review, CI green, linear
  history, signed commits. `CODEOWNERS` routes `project/**` and
  `spec/vectors/**` to Paul.
- Pages via **MkDocs Material**, Python not Node — matches the project and spares
  a toolchain nobody needs.

---

## 4. The bibliographic library

Requirement: all technical references, typed cross-references, local distilled
artifacts (including code generated from an associated specification), shared by
the team, scalable to distributed libraries, working offline.

### Core decision: git is already the answer
Git is distributed, offline-first, content-addressed, and the team already knows
its merge semantics. **We are not building a sync engine.** We define a *record
format* and a *federation manifest*; git does transport. Anything else spends the
semester on infrastructure instead of provenance.

### Record shape
One directory per reference, stable kebab-case ID, YAML and markdown throughout.

```
library/
├── MANIFEST.yaml        library id, federation peers, schema version
├── records/<id>/
│   ├── record.yaml      metadata, identifiers, content hash, typed relations
│   ├── distilled.md     our summary — what it says, why it matters here
│   ├── artifacts/       generated: schema fragments, code, diagrams, vectors
│   └── quotes.md        verbatim excerpts with locators, for citation
├── topics/              cross-cutting notes linking many records
├── exports/             generated: references.json (CSL-JSON), .bib
└── bin/                 validate, export, resolve, fetch
```

Five points D1 must defend:

1. **CSL-JSON is the interchange format, not the source of truth.** `record.yaml`
   is authored; `exports/` is generated. CSL-JSON round-trips through Zotero,
   Citation.js, and pandoc, so nobody is locked in. BibTeX is generated, never
   edited.
2. **Cross-references are typed**, not tag soup: `supersedes`, `cited-by`,
   `see-also`, `implements-concept`, `contradicts`. Typed edges make the library
   queryable and let it answer questions like *"every normative reference bearing
   on DEC-002."*
3. **Distilled artifacts are first-class.** `artifacts/` holds derived material —
   a CDDL or S-expression grammar extracted from a spec, code generated from it,
   a diagram. Each records what it was generated from and by what. This is where
   "code generated from associated specification" lives, and it is the natural
   corpus for §8.
4. **Never commit third-party PDFs.** Record hash and URL; `bin/fetch` populates a
   gitignored cache. Small repo, clean licensing, integrity preserved.
5. **Content hash is identity.** Two libraries that never sync still agree on
   what document they are discussing.

### Distributed and offline, scalably
- A library is a git repo. N libraries = N repos. Offline is free.
- `MANIFEST.yaml` lists **federation peers** by ID and URL.
- Record IDs are namespaced by library ID, so `usf-lp:rfc-9943` and
  `shelfmark:rfc-9943` never collide and can merge.
- Cross-library references resolve by `(library-id, record-id, content-hash)`.
  Hash mismatch is *detectable divergence*, not silent corruption.
- **Designed-for, not built now:** a library publishes a signed
  `ArtifactStatement` over its own manifest digest — federation then inherits the
  system's own integrity guarantees, and the library becomes a worked example of
  the protocol instead of a side tool.

> **Open question for Paul:** does `library/` converge with Shelfmark? Same
> hash-as-identity model. Cheap to align now, expensive in November.

---

## 5. D1 — first reference search: construction best practice

Per instruction, the first search is meta: *before we collect references, decide
how.*

**Scope.** Reference formats (CSL-JSON, BibTeX/BibLaTeX, RIS) and what survives a
decade. Citation-key stability. Git-based vs database-based libraries; why Zotero
is an import/export peer and not our source of truth. Distillation practice —
what a useful summary contains. Typed cross-reference vocabularies (SKOS, PROV).
Search methodology: **Kitchenham & Charters** three-stage SLR structure (protocol
→ conduct → report), **Wohlin snowballing** (backward and forward, iterated to
closure), **PRISMA 2020** for transparent reporting. Provenance of the library
itself.

**Output.** `library/docs/construction.md` plus the normative `record.yaml`
schema. Revised at the end of every increment with what we got wrong — an
honestly-revised methodology report is a more credible artifact than a clean one
written at the end.

**Exit criterion.** A second person adds a correct record from the document
alone, without asking.

---

## 6. Research reports (D3)

Three, each ~6–10 pages, markdown, published to Pages, citing `library@<commit>`.

**Context** — why provenance, why now. Artifact trust collapse. What the field
converged on and where it stops. The historic gap ARCH-0001 §3.3 names: SPKI/SDSI
never standardised a first-class artifact statement; PICS did, without a
principal or delegation model. Regulatory forcing functions (§9).

**Mechanism** — how these systems actually work: hashing, canonicalization,
signatures, reduction, Merkle structures, receipts. Comparative anatomy of
in-toto/DSSE, SCITT/COSE, SPKI, PICS, VC/DID. Where each places trust and what
each leaves undefined. **This report is the evidence base for DEC-002 and
DEC-004** — write it with that job in mind.

**Uptake & applications** — who adopts, why, what stops them. Adoption evidence
for SLSA, Sigstore, C2PA, SBOM mandates. Then the section that matters most: a
**failure-to-adopt analysis of SPKI/SDSI and PICS**. Both are direct ancestors of
this design and both failed to take hold. Any uptake story that does not confront
why is not worth writing. Feeds D9.

---

## 7. Inputs to open decisions

Proposals only. None is accepted; each carries an acceptance test so it can be
*settled* rather than argued.

### 7.1 DEC-002 — the criterion that was missing

Detail is in `ARCH-0001-PROPOSAL-v0.2.0` §3. Summary of what changed and what it
means for scheduling:

**RFC 9804 is historical.** An Informational restatement of a 1990s encoding,
published so the format is citable. Option 1 stays as a mapping reference for
WP2; it is not a contender. What survives from that lineage is key-centricity,
not S-expression syntax.

**CBOR and COSE extension points are centrally defined.** CBOR tags come from an
IANA registry; so do COSE header parameters, algorithm identifiers, and CWT
claim keys. Private-use ranges are an escape from the registry, not a namespace —
two parties using the same private label collide with no principal to
disambiguate them. A model whose premise is that principals are keys should not
inherit a global allocator at its extension points. Proposed as **R-M-12**:
extension points are `(defining key, local label)` pairs, and registry
identifiers live at interchange boundaries only. This is the natural completion
of R-M-01 — that rejects a central identity authority, R-M-12 rejects a central
vocabulary authority.

**A proposed fifth DEC-002 option** separates CBOR-the-encoding from
COSE-the-governed-type-space: CBOR data model and deterministic encoding, no
IANA tag or COSE header dependence natively, COSE and DSSE as export envelopes
under R-I-03.

**Scheduling consequence, and it is good news.** All four original options were
scored on fidelity, tooling, and ergonomics; none on namespace governance. With
option 1 out and R-M-12 constraining the rest, the practical field narrows to two
— CBOR with key-relative types, or JSON/JCS with key-relative types. **D5 should
build fixtures for two options, not four.** That returns roughly a week to I2 and
removes the risk flagged in v0.3.0 §13 that students would spend real time on an
option that was never going to win.

**The rule that holds regardless — sign the bytes.** The signed payload is the
canonical encoding verbatim, with an authenticated type indicator. The verifier
verifies before decoding and never canonicalizes during verification;
canonicalization happens once, at authoring time, on trusted input. This keeps
the project clear of the DSSE canonicalization critique. Proposed as **R-O-05**.

### 7.1b DEC-006 withdrawn — display is a UI concern

A human *authoring* format is not required; certificates and statements are
produced by tools. Display forms do matter, and they belong with the mechanism
that says what a predicate value means in words — which is DEC-007, not the
encoding decision. DEC-006 is withdrawn before filing, which also brings the open
decision count back down.

### 7.2 Subject identification — proposed extension to `ArtifactId`
ARCH-0001 §4.1 has `ArtifactId = { uri?, digest }`. Attesting to *arbitrary*
objects needs one more mode, because some subjects cannot be hashed:

| Mode | For | Identity |
|---|---|---|
| `digest` | bytes you hold | as today |
| `locator` | things with a name | URI, URN, ISBN, serial |
| `description` | things you cannot hash | canonical digest of a **structured description** |

The third costs nothing new: describe the object in the native model,
canonicalize, and its digest is its identity. A book, a physical part, a dataset,
an event, a person's role. R-M-07 ("SHALL bind at least one content digest") is
still satisfied — the description's digest *is* a content digest. Worth filing as
an additive MINOR against ARCH-0001 §4.1.

### 7.3 Proposed DEC-007 — predicate rendering (the semantic layer)
ARCH-0001 has `PredicateType` and `Predicate` but does not say how a predicate
*renders to a person*. Every system in this space reinvents that ad hoc.

**Proposal:** a `PredicateType` dereferences to a signed, versioned **vocabulary**
declaring claim categories, permitted values, ordinal scales where they apply,
and **the exact human-readable rendering string for each value**. Statements cite
it by URI plus digest. This is PICS's rating-system/label split — the part
ARCH-0001 §3.1 credits PICS with and that nothing since has generalised.

**Independent validation, found 2026-09-16:** the IETF draft *Agent Action Capsule
Profile for SCITT* defines a disposition vocabulary — `executed`, `blocked`,
`denied`, `timeout`, `errored`, `deferred`, `expired`, `escalated`. A PICS rating
system, arrived at independently, in 2026, inside SCITT. The pattern is being
reinvented because nobody specified it generally. **That is the gap, now
evidenced rather than asserted** — and it is the "semantic" in the goal statement.

Note the interaction with **DEC-004**: a tag language needs intersection (R-M-08);
a rendering vocabulary needs legibility. They are different jobs and should not
be collapsed into one construct.

### 7.4 Verdict shape — proposed, feeds WP6
ARCH-0001 §4.3 keeps name resolution, authorization reduction, and statement
acceptance **separate** and says they must not collapse into one graph walk.
The output should preserve that separation rather than flatten it to a boolean:

```
integrity      digests re-derive
authenticity   signature valid under a key
names          name chain resolved to KeyId          ← §4.3(1)
authorization  reduction yields the required tag     ← §4.3(2)
acceptance     issuer authorized for this PredicateType ← §4.3(3)
semantics      vocabulary resolved, values in range  ← DEC-007
```

plus an explicit `unknowns` list, and a closing statement of what is **not**
proven. A statement can be **authentic but unauthorized** — a real key making a
claim it has no standing to make. That distinction is invisible in mainstream
tooling and it is the sharpest thing this project can show.

---

## 8. AI-assisted protocol design as method

Named in the goal, so it must be instrumented, not merely used. ARCH-0001 already
models this — its `authors:` field records `conversation-brainpool256` as the
architect, and §9 defines an iteration protocol. Generalise that into
`design-log/`, capturing per decision:

- the question posed and the context supplied
- what the model produced (spec text, schema, code, vectors)
- what a human accepted, edited, or **rejected — and why**
- the resulting ADR

Every generated artifact carries a header naming its source: which document
section, which prompt, which model, which date. Then the recursive part: **those
artifacts become `ArtifactStatement` subjects** under §7.2's `description` mode,
attested by the system being built.

Write up the failures. The half where a human had to overrule the model is what
makes the claim credible, and it is the half nobody else publishes.

**Guardrail:** no generated cryptographic primitives. Vetted libraries only. AI
assistance applies to specification, schema, encoding, mappings, test vectors,
and tooling — never to primitives.

---

## 9. Increments

Harness first. **Every increment ends in a demo.** The student demo is the
*minimum*, and it lands at I3 — three weeks before CS Night, deliberately.

| Inc | Dates | Theme | WP | Demo at the end |
|---|---|---|---|---|
| **I0** | Sep 16–30 | **Harness** — DEC-001 first, then org, 2 repos, CI, Pages, doc-schema validator, library skeleton | WP0 | Site deploys from a merged PR; `validate-archdoc` blocks a bad front matter |
| **I1** | Oct 1–14 | **Library & research** — D1 v0.1, library populated, three reports drafted | — | Query the library: *"every normative reference bearing on DEC-002"* |
| **I2** | Oct 15–28 | **Schema + DEC-002 package** — encoding-neutral types, then fixtures in all four options | **WP1**, DEC-002 | Same `AuthzCert` with a threshold subject, round-tripped in four encodings, side by side |
| **I3** | Oct 29–Nov 11 | **Reduction — DEMO FLOOR** — name resolution, 5-tuple reduction, minimal tag profile | **WP6**, DEC-004 min | **Delegation chain reduces to a tag; break a link; verifier explains it in English** |
| **I4** | Nov 12–25 | **Mappings** — SPKI↔native, in-toto↔ArtifactStatement; app packaging | **WP2, WP3** | A real SLSA attestation imports as an `ArtifactStatement` and round-trips |
| **I5** | Nov 26–Dec 4 | **Polish** — app download on Pages, market report, rehearsals | — | CS Night, Dec 4 |

**Why I3 is the floor.** It demonstrates the thing ARCH-0001 says is missing from
every modern stack — local names plus threshold authorization reduction — using
the library as its corpus. It does **not** need a build pipeline, a transparency
log, or foreign-format mappings. Those are I4 upside. With eleven weeks and two
students, the floor must not depend on infrastructure.

### CS Night demo (4–5 min, rehearse from I4)
1. Show a `NameCert` and an `AuthzCert` in the human form. Read them aloud —
   legible because the vocabulary rendered them, not because someone wrote a nice
   sentence.
2. Reduce a delegation chain; the requested tag is granted. Six dimensions green.
3. Break one link. The verifier names *which* and explains why.
4. Re-sign with a valid but **unauthorized** key. Signature valid, authorization
   denied — a different verdict, and one nothing on the market shows you.
5. *k*-of-*n* threshold subject: 2 of 3 signs, 1 of 3 does not. First-class, not
   a CA hierarchy pretending.

Close on: **this proves origin and integrity. It does not prove truth.**

---

## 10. Team interaction

Two students plus a sponsor, mostly async. Escalate only when the rung below has
failed.

| Channel | For | Expectation |
|---|---|---|
| **Issues** | All work. One per task, labelled, on a milestone | Every task is an issue before it is code |
| **Pull requests** | All changes. No direct pushes to `main` | Review within 24h on weekdays |
| **Discussions** | Open design questions, DEC-* debates | Resolved into an ADR, then closed |
| **Weekly Zoom** | Decisions, unblocking, increment demo | 30 min, agenda = the board, notes committed same day |
| **SMS** | Blocked >24h, or a schedule change | Escalation only — **never content** |

- **If it is not in the repo, it did not happen.** SMS and Zoom decide; the repo
  records.
- **DEC-* decisions follow ARCH-0001 §9**: accepted → `ADR-NNNN`, changelog line,
  status updated in ARCH-0001 with a pointer. Never marked accepted in a PR
  description or a Zoom note.
- **One PR per deliverable slice.** Small and reviewable beats big and correct.
- Students are both Owners and review each other; Paul reviews
  `project/**` and `spec/vectors/**` via `CODEOWNERS`.
- **Draft PRs opened on day one of an increment** are the progress signal.
- The **CS690 weekly progress page is generated from the repo** — merged PRs,
  closed issues, plus a short reflection. A course requirement made a byproduct.

---

## 11. Market and applications research (D9)

An **uptake analysis**, not a business plan: who adopts, what forces them, what
stops them.

**Forcing functions, dated and verified:**
- **EU Cyber Resilience Act Art. 14** vulnerability reporting applies from
  **11 September 2026 — five days ago** — to all products with digital elements
  already on the market. Full obligations, including machine-readable SBOM
  (Annex I, Part II), from **11 December 2027**. You cannot report what you cannot
  inventory, so the pressure is live now.
- **EU AI Act Art. 50** and **California SB 942** — machine-readable disclosure of
  AI-generated content.
- US federal SSDF attestation (EO 14028 lineage).

**Segments** — for each: pain, current practice, what this adds, barrier, buyer.
1. Regulated software supply chain — CRA/SSDF driven.
2. AI media provenance — newsrooms, platforms, C2PA adopters.
3. **AI agent attestation** — fastest-moving, least served. NIST's AI agent
   standards work began April 2026; the SCITT agent-action-capsule draft exists;
   DID-based agent identity methods are appearing. Delegation, attenuation, and
   threshold authority are exactly what agent chains need and exactly what
   ARCH-0001 models natively. **This is where the contribution lands hardest.**
4. Scientific and research data provenance.
5. Archives and cultural heritage — arbitrary non-software objects; the segment
   our own library work exercises directly.

**Method.** Desk research plus 3–5 short practitioner conversations if reachable.
Then the honest part, shared with D3's uptake report: why SPKI and PICS failed,
and which of those failure modes this design still carries.

---

## 12. Risks and cut order

Agree in writing during I0, so cutting under pressure is a decision already made.

| # | Risk | Fallback | Cut by |
|---|---|---|---|
| 1 | **DEC-001 blocks org creation** | Pick a placeholder slug, accept the rename cost, move | Sep 19 |
| 2 | Harness work eats the semester | Timebox I0 hard at two weeks. Ship an ugly site | Sep 30 |
| 3 | Library scope unbounded | Cap at ~40 records for D2 v1. Depth over breadth | Oct 14 |
| 4 | **DEC-002 deadlocks** | Ship WP1 encoding-neutral; implement reduction against the logical model; decide encoding later | Oct 28 |
| 5 | WP4/WP5 (PGP, X.509 import) creep in | Already out of scope. Say no | ongoing |
| 6 | Tag language over-scopes | ARCH-0001 DEC-004 already offers the out: opaque byte string + `bytes-equal` profile | Nov 4 |
| 7 | Threshold subjects prove hard | Implement *k*-of-*n* over keys only; no nested thresholds | Nov 11 |
| 8 | Transparency log / receipts | Defer to v2 (R-O-04 is already **C**). **Not in the demo floor** | Nov 11 |
| 9 | Federation across libraries | Design and document only; do not build | Oct 14 |
| 10 | App packaging | Single-file Python zipapp, not an installer | Dec 1 |

**Hard floor that still passes:** D0–D6, done by **November 11** — harness,
library, three reports, encoding-neutral schema, DEC-002 package, and a working
reduction with test vectors. Everything after is upside.

---

## 13. Plan review — the double-check

**Verified this session.** SCITT architecture is **RFC 9943**, Proposed Standard,
**June 2026** — ARCH-0001 §10 and its `related_drafts` still cite
`draft-ietf-scitt-architecture`; **worth updating to the RFC.** SCRAPI (draft-11)
is in the RFC Editor queue. COSE Receipts is at draft-18. **RFC 9804** confirmed as
Rivest & Eastlake, June 2025, **Informational** — recorded as historical, not a
DEC-002 contender. **CBOR tag allocation** confirmed as IANA-governed (Standards
Action 0–23, Specification Required 24–32767, FCFS above); **COSE header
parameters** likewise, with private use below −65536 — escape, not namespace. SD-JWT is **RFC 9901** (Nov
2025). C2PA is at **2.4** (April 2026) — the pitch deck's 2.2 is stale. CDDL is
RFC 8610, updated by 9165 and 9682. dCBOR is at draft-14, still an individual
draft — correct to cite, wrong to depend on. CRA Art. 14 began 11 Sept 2026.

**Genuine risks in *this plan*, stated plainly:**

- **Eleven weeks, two students, eleven deliverables is aggressive.** The floor
  lands Nov 11 and the cut order protects it. But if I0 slips past Sep 30, cut
  the library to 25 records immediately rather than compressing I2 — the schema
  and the DEC-002 package are what cannot be rushed.
- **DEC-002 is on the critical path, but the field has narrowed.** R-M-12 and the
  retirement of RFC 9804 cut D5 from four options to two. WP1 stays
  encoding-neutral, so reduction can be built before the encoding is chosen. The
  residual risk is that R-M-12 itself is contested — if it is judged too strong,
  §3.2, §5.1, and §5.4 of the proposal all need rework, and that is a week.
- **The library could quietly become the project.** It is interesting, tractable,
  and infinitely expandable. Cap it; treat post-Oct-14 additions as opportunistic.
- **"AI-assisted protocol design" is only a contribution if instrumented from day
  one.** Retrofitting `design-log/` in November yields a narrative, not evidence.
- **Dropping transparency/receipts from the floor is a real trade** — arguably the
  thing SCITT is *about*. I think it is right, because receipts are the most
  infrastructure-heavy piece and the name/threshold/reduction contribution is the
  novel one. It is a defensible disagreement; Paul's call.
- **Scope tension worth naming:** ARCH-0001 is an ambitious research architecture;
  CS690 is one semester with two students. This plan resolves that by scheduling
  only WP0–WP3 and WP6, and saying so. If Paul wants WP4/WP5 in scope, something
  in the floor comes out.

**Open items for Paul** — each blocks or reshapes work below it:
1. **DEC-001** (naming/slug) — blocks org creation, blocks D0. Take it first.
2. Library standalone repo — yes/no (§3 recommends yes).
3. Does `library/` converge with Shelfmark (§4)?
4. Transparency log in the demo floor, or deferred (§12 risk 8)?
5. **Does R-M-12 stand?** It is the load-bearing addition and it constrains
   DEC-002, DEC-004, and DEC-007 at once. If it is too strong, say so now.
6. Does R-M-12 belong as a requirement row, or does it deserve **ARCH-0002**?
   It is arguably the most novel claim available — SDSI localized principal
   names; nobody localized type names.
7. Accept **DEC-007** (predicate rendering and display) as a filed open decision?
8. Accept `ArtifactId.description` (§7.2) as an additive MINOR to §4.1, and does
   `locator` survive R-M-12?
9. Confirm WP4/WP5 out of scope this semester.

---

## 14. Next actions

**Paul, this week**
1. **DEC-001.** Everything downstream waits on the slug.
2. Answer open items 2–7 above.
3. Bump ARCH-0001 to v0.2.0 if the proposal is accepted — per §9, changelog and
   `updated` together. The §9 entry is pre-drafted in the proposal.

**Students, I0 (by Sep 30)**
4. Both repos, branch protection, `CODEOWNERS`, DCO check, issue/PR templates.
5. `bin/validate-archdoc` in CI — the `archdoc/v1` schema enforced mechanically.
6. MkDocs Material deploying to Pages from a merged PR.
7. `library/` skeleton: `MANIFEST.yaml`, `record.yaml` schema, `bin/validate`.
8. **D1 v0.1** — construction best practice. The first real search of the semester.
9. Seed 10 records by hand, to prove the schema before scaling it.
10. `design-log/` opened with the first entry: *how ARCH-0001 v0.1.0 was produced.*
    It is already an AI-assisted design artifact; capture that while it is fresh.

**Everyone**
11. Read **ARCH-0001** and **RFC 9943** before the first Zoom. They are the shared
    vocabulary for the semester.

---

## 15. Bibliography seed

First records for `library/`, verified current as of 2026-09-16. ARCH-0001 §10
plus what this plan adds.

**ARCH-0001 §10 baseline** — RFC 2692, RFC 2693 (SPKI) · **RFC 9804** (SPKI
S-Expressions, 2025) · RFC 8392 (CWT) · RFC 8949 (CBOR) · RFC 9052 (COSE) ·
in-toto Attestation Framework v1 · SLSA Provenance v1 · W3C PICS · Ellison,
*SPKI/SDSI and the Web of Trust* · OpenPGP trust-signature model

**Corrections and additions**
- **RFC 9943** — SCITT Architecture, Proposed Standard, June 2026. *Replaces the
  draft citation in ARCH-0001.*
- draft-ietf-scitt-scrapi-11 · draft-ietf-cose-merkle-tree-proofs-18
- RFC 8610 + **9165** + **9682** (CDDL) · RFC 9334 (RATS) · RFC 9711 (EAT) ·
  RFC 9162 (CT v2)
- RFC 8785 (JCS) · draft-mcnally-deterministic-cbor-14 · IPLD DAG-CBOR ·
  YAML 1.2 · StrictYAML
- **DSSE `background.md` and `protocol.md`** — the canonicalization critique.
  Required reading before DEC-002.
- Rivest & Lampson, *SDSI* · Macaroons · Biscuit · UCAN
- W3C PROV-DM / PROV-O · RDFC-1.0 · SHACL · CSL-JSON
- C2PA 2.4 + UX Recommendations · *Signals of Provenance* (arXiv 2505.16057) ·
  *Content Authenticities* (ACM C&C 2025) · NSA/CISA Content Credentials (2025)
- **draft-mih-scitt-agent-action-capsule-02** — the independent PICS rediscovery ·
  *AI Identity: Standards, Gaps* (arXiv 2604.23280) · NIST AI Agent Standards
- Kitchenham & Charters (2007) · Wohlin (EASE 2014) · PRISMA 2020
- Williams et al., *P-SSCRM v1* (arXiv 2404.12300)
- EU CRA (Art. 14, Annex I Pt II) · EU AI Act Art. 50 · California SB 942
