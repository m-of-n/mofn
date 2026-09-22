---
schema: "archdoc/v1"
id: GLOSSARY-0001
title: "Glossary — terms that mean more than one thing"
short_title: "Glossary"
description: "Precise senses for the project's overloaded vocabulary. Written because term collisions have been this project's recurring defect."
type: reference
category: process
status: draft
version: "0.1.0"
version_policy: "semver; MINOR = terms added"
date: "2026-09-22"
updated: "2026-09-22"
needs_review: true
reviewed: false
canonical_path: project/GLOSSARY-0001.md
defers_to: ARCH-0001
---

# Glossary

**Term collisions are this project's recurring defect.** Three so far:
`artifacts/` as a directory against **Artifact** the normative term; `DEC-P4`
against principle **P4**; and the two live ones below. Each was caught late, by a
reader rather than by a check.

This file exists so the next one is caught early. **Before introducing a term,
check it here.**

---

## Collisions — currently live

### "Topic" — two senses ⚠️

| sense | where | means |
|---|---|---|
| **research topic** | `library/topics/<id>.yaml`, PROC-0001 §4, PROC-0003 §2 | the unit of parallel work: one bounded question, one owner, one branch |
| **delegation topic** | ARCH-0002 P2 — *A says B can speak about (Domain, Topic)* | a semantic scope within a domain of discourse |

These are unrelated. One is project management; one is authorization scope.
**Needs resolving** — register item. Candidates: rename the research unit to
`lane` or `question`; or rename the delegation scope to `subject-area`. The
architectural sense is the one with a claim on the word.

### "Tag" — two senses ⚠️

| sense | where | means |
|---|---|---|
| **authorization tag** | ARCH-0001 §4.1 `Tag`, R-M-08, DEC-004 | the SPKI authorization value, with defined **intersection** semantics |
| **library tag** | `library/schema/tags.yaml` — subject, body, role | a classification label on a bibliographic record |

Also unrelated: one composes under reduction, the other is a filing label.
**Needs resolving** — register item. The library sense is the cheaper one to
rename, e.g. to `labels`.

---

## Settled terms

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
record. **Distillation** (`distilled.md`) — an optional compaction for
requirements extraction. They are not synonyms.

**Requirement** — two senses, deliberately kept apart: an **extracted**
requirement comes *from a source document* (`library/.../requirements/`,
RFC 2119/8174 verb, actor, condition, locator); an **authored** requirement is
ours (`R-M-*`, `R-O-*` in ARCH-0001). Direction of travel matters: never file one
as the other.
