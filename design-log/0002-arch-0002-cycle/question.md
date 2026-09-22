---
schema: "design-log/v1"
id: DL-0002
title: "ARCH-0002 — key-relative naming, types, domains of discourse"
date: "2026-09-22"
model: "claude-opus-5"
human: paul-lambert
outcome: "ARCH-0002 v0.3.0 + ADR-0001, PR #25"
status: complete
---

# DL-0002 — question

## Context supplied
ARCH-0001 v0.1.0 as source of truth; the v0.2.0 proposal with R-M-12 as a
requirement row; `DECISIONS-0001` tier 1.

## Question posed
> "on R-M-12: does it stand, and does it deserve ARCH-0002? #9 yes — localized
> type names is core principle! on core principles there are more — constraints
> on an object is a different object from the type and strong checking of field
> validity is important; on the parseability of a design it appears CBOR splits
> length determination from type to allow support for unknown field elements and
> size determination … can all processing be part of the local name space?"

Then, across three further rounds:
- "the parsing length stuff is not a hard issue but an observation"
- "constraints come from a 'speaker', the signing key about some statement …
  domains of discourse are a set of these schemas … hash used to identify and
  provide integrity"
- "P2 is not quite right … 'A says B has C' … delegation requires A says B can
  speak about Domain and Topic while contracts …"
