---
schema: "archdoc/v1"
id: ADR-0006
title: "DEC-001 accepted: the working title and slug are m-of-n, the short form mofn"
short_title: "ADR-0006 DEC-001 slug"
description: "Accepts DEC-001: GitHub org and working title m-of-n; repository, Python package and CLI mofn. Ratifies names in use since 2026-09-17; rejects all five listed options."
type: decision
category: process
status: accepted
version: "1.0.0"
version_policy: "semver; an accepted ADR changes only by superseding it"
date: "2026-11-06"
updated: "2026-11-06"
decision_makers:
  - role: student
    id: ndewedo-newbury
    authority: "delegated by the sponsor (paul-lambert) in October 2026; ARCH-0001 v0.1.7 front matter (DL-0021)"
reviewers: []
needs_review: false
reviewed: false
canonical_path: spec/ADR-0006-dec-001-slug.md
defers_to: ARCH-0001
decides: [DEC-001]
supersedes: []
---

# ADR-0006 — DEC-001: the slug is `m-of-n`, the short form `mofn`

**Status: accepted.** Decision of `ndewedo-newbury`, 2026-11-06, under the
sponsor's October 2026 delegation recorded in `ARCH-0001` v0.1.7. An agent
drafted the text from that decision (`design-log/0027-adr-0006-dec-001/`). No
second reader has **reviewed** it.

## Decision

1. **Working title and org slug: `m-of-n`.** This is the GitHub organization
   (`github.com/m-of-n`) and the site name (`mkdocs.yml`).
2. **Short form: `mofn`.** This is the monorepo (`m-of-n/mofn`), the Python
   package (`src/mofn`) and the wallet command (`mofn`, `prototype/wallet`).
3. **The library repo keeps its functional name, `library`** (`m-of-n/library`).
   It is namespaced by the org and needs no slug of its own.

## Scope: what this does not decide

- **Not the protocol's name.** The protocol is *key-centric semantic
  assertions* (KSA), and its encoding is KSA-CBOR (`ADR-0004`). DEC-001 names
  the project and its repositories, not the protocol.
- **Not a product name.** `ARCH-0001` `scope.out` keeps product naming out of
  scope. A product name, if one is ever needed, is a new decision.
- **Not a freeze.** `ARCH-0001` NG3 lists "freeze … repository name" as a
  non-goal. This ADR records the slug as accepted so the architecture stops
  listing it as open. A rename is still possible, by a superseding ADR, at the
  rename cost described below.

## Why

- **The names have been in use since 2026-09-17.** The org was created at
  05:06Z that day and both repositories at 05:34Z (GitHub API). Seven weeks of
  issues, PRs, design-log entries, the Pages site and the
  `mofn` package all resolve against them. DEC-001 says *"Affects: packaging
  only"*, and packaging has existed since then.
- **The decision was already treated as made.** Since 2026-09-21 (mofn#12),
  `PLAN-0001` §3, `BACKLOG-0001` T-001 and `DECISIONS-0001` have all said
  "DEC-001 accepted: `m-of-n`". `ARCH-0001` §7 still listed it as open. Under
  §9.2 only an ADR accepts a DEC-\*, so those three lines were premature.
  This ADR is the acceptance they lacked.
- **`m-of-n` names the novel object.** G4 and R-M-06 make the threshold
  principal (*k* of *n*) first-class. It is the one capability neither the
  historic models nor the modern statement stack provides in this form
  (§3.3). The slug points at it without claiming a lineage.

## Alternatives rejected

The five options in `ARCH-0001` §7 and the name `PLAN-0001` v2 invented. The
reasons below were assembled by the agent; the decider gave none of their own
(`DL-0027` review).

| alternative | rejected because |
|---|---|
| `spki3` | Claims to be a version of SPKI. The project does not inherit SPKI's encoding or adopt RFC 2693 as its specification (`PLAN-0001` §0), and KSA-CBOR is not an S-expression (`ADR-0004`) |
| `open-sdsi` | Same lineage claim for SDSI. Local names (G1, R-M-03) are one of six primary objects (§1), not the whole system |
| `kofn-certs` | Nearest in meaning, but "certs" names the old object model. `ARCH-0002` P6 (`ADR-0002`) makes the kinds functions over one statement form, so "certificates" misdescribes the system |
| `localnames` | Names one of the six objects; leaves out thresholds, authorization and artifact statements |
| `sudsy` | A pun on SDSI that no stranger can decode. It carries the same lineage claim with less information |
| `legible-provenance` | Invented in `PLAN-0001` v2 and withdrawn there for exactly that reason (`PLAN-0001` §0, item 3). It was never an option |
| **any rename now** | Costs the org, two repos, the Pages URL, the `mofn` package and CLI, and every `mofn#NNN` and `library#NNN` citation in issues, PRs and the design log. GitHub redirects repo renames, but not org renames, which break every citation. Seven weeks before the semester's end, that cost buys nothing DEC-001 asked for |

## Acceptance test

DEC-001 had none in `ARCH-0001` §7. This ADR supplies one: *the accepted names
resolve, and no live document lists DEC-001 as open.*

- **Met:** `github.com/m-of-n/mofn` and `github.com/m-of-n/library` resolve.
  `.gitmodules` resolves `../library` beside `mofn`. `src/mofn` and the `mofn` CLI
  exist. `ARCH-0001` §7 marks DEC-001 accepted, and `open_decisions` no longer
  lists it. `CLAUDE.md` and `README.md` say so.
- **Owed:**
  - The `src/mofn/__init__.py` docstring still says DEC-001 … DEC-005 are open.
    It is code, so it is left for the next change to `src/`.
  - The `PLAN-0001` §3 tree diagrams keep `<DEC-001>` placeholders. They are a
    snapshot of a superseded layout and are left as written.

## Consequences

- `ARCH-0001` §7 DEC-001 is marked accepted, and DEC-001 leaves
  `open_decisions`. **DEC-004, DEC-005 and DEC-007 stay open.**
- `BACKLOG-0001` T-001, `PLAN-0001` §3 and `DECISIONS-0001` cite this ADR in
  place of the bare "accepted".
- Nothing in §4–§6 changes. DEC-001 has no effect on the information model.

## Evidence

- GitHub API: `orgs/m-of-n` created 2026-09-17T05:06:51Z, `m-of-n/mofn`
  05:34:11Z, `m-of-n/library` 05:34:07Z.
- mofn#12 (`d2a91fb`, 2026-09-21): the first "DEC-001 accepted" lines in
  `PLAN-0001` and `BACKLOG-0001`.
- `ARCH-0001` v0.1.9 §1, §2 (G4, NG3), §3.3, §5.1 (R-M-06), §7; `ADR-0002`;
  `ADR-0004`.
