---
schema: "archdoc/v1"
id: ADR-0001
title: "R-M-12 stands: key-relative naming is a core principle"
short_title: "ADR-0001 key-relative naming"
description: "Accepts R-M-12 and promotes it from a requirement row to ARCH-0002."
type: decision
category: security
status: accepted
version: "1.0.0"
version_policy: "semver; an accepted ADR changes only by superseding it"
date: "2026-09-22"
updated: "2026-09-22"
decision_makers:
  - role: sponsor
    id: paul-lambert
reviewers: []
needs_review: false
reviewed: true
canonical_path: spec/ADR-0001-key-relative-naming.md
defers_to: ARCH-0001
supersedes: []
---

# ADR-0001 — R-M-12 stands

**Status: accepted.** Sponsor decision, 2026-09-22, in review of
`DECISIONS-0001` tier 1 items 1 and 5.

## Decision

**R-M-12 stands.** Native extension points — type identifiers, predicate types,
tags, header parameters — are identified relative to a defining principal, as a
`(key, local label)` pair. The native model depends on no centrally allocated
registry for their meaning.

**It is promoted out of a requirement row into its own architecture document,
`ARCH-0002`**, because it is a cross-cutting principle rather than a
constraint on one mechanism, and because it is the most novel claim the project
has:

> SDSI localized **principal** names. Nobody localized **type** names.

## Consequences

- **`ARCH-0002` becomes the home** for key-relative naming and everything that
  follows from it. `ARCH-0001` references it; the requirement row is replaced by
  that reference on acceptance of v0.2.0.
- **DEC-002 is constrained.** CBOR tags and COSE header parameters are IANA
  allocated, so they are interchange, not native. Proposed option 5 — CBOR data
  model without registry dependence — remains on the table; option 2 as
  originally written does not.
- **DEC-004 and DEC-007 are constrained** the same way: a tag language and a
  rendering vocabulary are both key-relative.
- Registry identifiers **may** appear at interchange boundaries, and such
  mappings are documented as lossy per R-I-01.

## Alternatives rejected

**Keep R-M-12 as a requirement row in ARCH-0001 §5.** Rejected: it constrains
three open decisions at once and carries argument that does not fit a table
cell.

**Use registry private-use ranges instead.** Rejected: private use gives escape
from a registry, not a namespace. Two parties independently using the same
private label collide with nothing to disambiguate them, because no principal is
attached. The identifier stays global; only its allocation becomes informal.

## Evidence

- IANA allocation policies for CBOR tags (RFC 8949 §9.2) and COSE header
  parameters (RFC 9052 §11.1), verified 2026-09-16.
- The independent re-invention of a PICS-style vocabulary inside
  `draft-mih-scitt-agent-action-capsule-02`, showing the pattern is undersupplied
  rather than unwanted.
