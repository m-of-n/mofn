---
schema: "archdoc/v1"
id: GLOSSARY-0001
title: "Glossary — terms that mean more than one thing"
short_title: "Glossary"
description: "Precise senses for the project's overloaded vocabulary. Written because term collisions have been this project's recurring defect."
type: reference
category: process
status: draft
version: "0.3.0"
version_policy: "semver; MINOR = terms added"
date: "2026-09-22"
updated: "2026-10-14"
needs_review: true
reviewed: false
canonical_path: project/GLOSSARY-0001.md
defers_to: ARCH-0001
---

# Glossary

**Term collisions have been a recurring defect** — `artifacts/` as a directory
against **Artifact** the normative term, and `DEC-P4` against principle **P4**.
Both were caught late, by a reader.

This file exists so the next one is caught early. **Before introducing a term,
check it here.**

## What counts as a collision

> Two senses collide when **both can be live in the same context** — the same
> document, the same repository, or the same sentence in ordinary use.

Reuse across separated contexts is a **homonym**, and homonyms are fine. A
codebase uses "key" for a cryptographic key and a map key without confusion,
because no passage means both.

`artifacts/` collided because the directory sat *inside the repository that
defines `ArtifactStatement`* — a reader could reasonably ask whether ARCH-0001
was itself an Artifact. `DEC-P4` collided because it appeared in the same
document as principle P4.

**Applying this test too eagerly is its own defect.** An earlier revision of
this file listed `tags` and `topic` as live collisions and proposed renaming
28 files; neither survives the test above. Recorded below so the over-correction
is visible rather than repeated.

---

## Collisions — currently live

### `persona` — resolved 2026-10-14 by writing *archetype* for the template sense ✅

Passes the test: both senses were live on one page, PLAN-0002 §2.1, where the
CS690 template's *user persona* and the wallet's *persona* would sit in the same
table.

| sense | where | is now written |
|---|---|---|
| **wallet persona** — a key-identified principal: its keys, the contexts it acts in and the contexts it trusts; controlled by a person, organisation, service, AI agent or device | ARCH-0003, APP-0001 §4b | **persona** |
| **template persona** — a representative user, for product design | the CS690 Product Spec template; PLAN-0002 §2.1 | **archetype** |

And a third thing that had been mislabelled as both: **domain author, issuer,
relying party** are **roles** — what one key does in one statement — not
personas of either kind (ARCH-0003 §1).

### `D-n` — resolved 2026-10-11 by renaming to `MD-n` ✅

The one that passed the test above, and the only one that has.

| sense | where | was | is now |
|---|---|---|---|
| **dated decision** | the weekly minutes, `project/meetings/` | `D-1 … D-7` | **`MD-1 … MD-7`** |
| **deliverable** | `PLAN-0001` §9, `PLAN-0003`, `PROC-0004`, the backlog's `del` column, issue titles | `D0 … D10` | unchanged |

**Why it collided where `tags` and `topic` did not.** Both senses were live in
*one table on one page* — `PLAN-0003` listed `D-3` (the encoding decision) two
rows above `D3` (the research reports), and `D-5` (survey defaults) against `D5`
(the Oct 28 fixture package). That is the test, met exactly.

**Why the decisions were the side that moved.** The deliverables are the
wider-used of the two: they appear in GitHub issue titles, which cannot be
rewritten cleanly, and in the backlog's `del` column on every row.

> **Redirect — older text citing `D-n` means `MD-n`.** 129 citations were
> rewritten across both repositories on 2026-10-11 (75 in `mofn`, 54 in
> `library`). Anything written before that date, including closed PRs, issue
> comments and merged design-log entries, uses the old form. **A bare `D-3` in
> older text is `MD-3`, never `D3`** — which is the hazard that made the rename
> worth doing, since the deliverable `D3` still exists.
>
> Unaffected: `JCS-D-01` and `JCS-D-02` in the RFC 8785 library record are
> Appendix D test vectors, a different family entirely.

---

## Collisions — raised and withdrawn

**Both were withdrawn on 2026-09-22** as `DECISIONS-0001` register items 6b and
6c, and neither survives the test in the section above: they are homonyms across
separated repositories and documents, not senses live in one context. They are
kept here so the over-correction stays visible rather than being re-raised.

*(An earlier revision of this file listed both under "currently live" with
"needs resolving — register item", three weeks after the register withdrew them.
That contradiction is corrected here.)*

### "Topic" — two senses, withdrawn ⊘

| sense | where | means |
|---|---|---|
| **research topic** | `library/topics/<id>.yaml`, PROC-0001 §4, PROC-0003 §2 | the unit of parallel work: one bounded question, one owner, one branch |
| **delegation topic** | ARCH-0002 P2 — *A says B can speak about (Domain, Topic)* | a semantic scope within a domain of discourse |

These are unrelated — one is project management, one is authorization scope —
but no passage means both, so no rename is owed. Should they ever meet in one
document, the architectural sense has the claim on the word.

### "Tag" — two senses, withdrawn ⊘

| sense | where | means |
|---|---|---|
| **authorization tag** | ARCH-0001 §4.1 `Tag`, R-M-08, DEC-004 | the SPKI authorization value, with defined **intersection** semantics |
| **library tag** | `library/schema/tags.yaml` — subject, body, role | a classification label on a bibliographic record |

Also unrelated: one composes under reduction, the other is a filing label. Same
verdict — a homonym across two repositories, not a collision.

---

## Settled terms

**Persona** — a **key-identified principal**: the key or keys that speak as it,
the contexts it acts in, and the contexts it trusts. Its controller may be a
person, an organisation, a service or script, an AI agent, a software
implementation or a device. A wallet **owns** some personas (it holds their
private keys) and **knows** others (ARCH-0003 §1, §3.2, W-01). Not the
template's *archetype*.

**Template** — a definition entry a statement is issued from: target rules,
required and fixed attributes, constraints, who may issue, and the sentence it
renders as. A statement citing a template must conform to it (ARCH-0003 §3.6,
W-17).

**Role** — what a key does in one statement: define, claim, delegate, review,
approve, present, rely. A property of the statement, not of the person
(ARCH-0003 §4).

**Context** — where, with whom and about what a persona acts. Holds the keys
enabled there, the definitions in use, and the **trust anchors** for that
context only (ARCH-0003 §3.4).

**Definition** — a vocabulary, schema or protocol, published by a definer key.
Identified by **`DefinitionId`**, the hash of its canonical encoding; a URL is a
retrieval hint, never its identity (ARCH-0003 §3.5). Generalises *domain of
discourse* (ARCH-0002 P4).

**Capability** — what the wallet will let a key sign: a role, a signing profile
(with its domain-separation tag), and an optional scope (ARCH-0003 §3.3).

**Artifact** — RFC 9943 sense: a physical or non-physical item moving along a
supply chain; the thing a statement is *about*. `ArtifactId`,
`ArtifactStatement`. **Never** used for files, documents or build outputs — the
directory that misused it is now `spec/` and `project/`.

**Statement** — the universal form, *A says B has C* (ARCH-0002 P2).

**Speaker** — the **A** in that form. A key, a key hash, or an alias resolving to
one. Per SDSI/SPKI, the speaker *is* the key.

**Says** — the signature. Not metadata about a statement; the cryptographic act
is the saying.

**Attestation** — the basic function: *A says B has C*.

**Delegation** — *A says B can speak about (Domain, Topic)*. Scoped
semantically, not only by tag.

**Constraint** — a narrowing over a schema of tag values, expressed as a
statement. A **function over the form, not a separate kind of object**. A
constrained object is a *different* object from its type.

**Contract** — a further statement function, **not yet specified**. DEC-009.

**Type** — a **schema**: representation, constraints on usage, semantic
descriptions, and tags for human review of usage, with short descriptions that
may be multilingual (ARCH-0002 P3). Not a bare label.

**Domain of discourse** — a hash-identified **set** of types (ARCH-0002 P4). The
unit of *meaning* and, per P2, the unit of *authority scope*.

**Valid** — RFC 8949's middle level: meets the data model's own constraints.
Distinct from **well-formed** (decodable) and **expected** (what the application
requires). All three are required; failure at any is rejection, never repair.

**Record** — a library entry, `library/records/<body>/<id>/`. Unrelated to any
architectural term.

**Summary** (`summary.md`) — the primary human- and AI-facing document for a
record. **Distillation** (`distilled/`) — the FX-1 artifact set built when a
record is extracted against. They are not synonyms. (The directory was
`distilled.md`, a single file, before FX-1.)

**Requirement** — two senses, deliberately kept apart: an **extracted**
requirement comes *from a source document* (`library/.../requirements/`,
RFC 2119/8174 verb, actor, condition, locator); an **authored** requirement is
ours (`R-M-*`, `R-O-*` in ARCH-0001). Direction of travel matters: never file one
as the other.
