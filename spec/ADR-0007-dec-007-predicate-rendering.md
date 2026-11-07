---
schema: "archdoc/v1"
id: ADR-0007
title: "DEC-007 accepted: option 2 — a predicate's meaning comes from a signed, hash-identified definition by the key that defines the type"
short_title: "ADR-0007 DEC-007 rendering"
description: "Accepts DEC-007 option 2 as SPEC-0003 implements it: types carry mandatory human-readable semantics in signed definitions identified by hash, and one renderer renders any statement with no type-specific code."
type: decision
category: security
status: accepted
version: "1.0.0"
version_policy: "semver; an accepted ADR changes only by superseding it"
date: "2026-11-07"
updated: "2026-11-07"
decision_makers:
  - role: student
    id: ndewedo-newbury
    authority: >
      Delegated by the sponsor (paul-lambert) on a Zoom call in October 2026;
      ARCH-0001 v0.1.7 front matter. No written sponsor confirmation is
      recorded (DL-0021).
reviewers: []
needs_review: false
reviewed: false
canonical_path: spec/ADR-0007-dec-007-predicate-rendering.md
defers_to: ARCH-0001
decides: [DEC-007]
supersedes: []
---

# ADR-0007 — DEC-007: predicate rendering is option 2

**Status: accepted.** Decision of `ndewedo-newbury` on 2026-11-07, under the
sponsor's October 2026 delegation (`ARCH-0001` v0.1.7). It was taken in the
mofn#134 thread (T-012a), and the agent drafted the text. Recorded in
`DL-0028`.

## Context

DEC-007 was drafted in `ARCH-0001-PROPOSAL-v0.2.0` §5 and filed in `ARCH-0001`
v0.2.0 §7. Its question: *how does a predicate type convey the human-readable
meaning of the values a predicate carries, so that a user interface can render a
statement without type-specific code?* The options were:

1. out of scope; display is an application concern;
2. a signed, versioned, dereferenceable vocabulary statement by the key that
   defines the type;
3. as option 2, with rendering strings inline in each statement;
4. reuse SKOS, JSON-LD contexts or SHACL.

Register item 5d (`DECISIONS-0001`) asked whether DEC-007 survives
`ARCH-0002` P3, *a type is a schema*. `ADR-0002` accepted P3 on 2026-11-06.

## Decision

**Option 2, as `SPEC-0003` specifies it.**

- A type is defined in a **definition** published by its definer. The
  definition is identified by the SHA-256 of its canonical encoding, its
  `DefinitionId` (`SPEC-0003` §4.2; `ADR-0003` D1), and is published by a signed
  `define` statement (`SPEC-0002` §8.9).
- Every type, value, field, constraint and template carries **mandatory**
  human-readable names and descriptions in a language map (`SPEC-0003` §5.3,
  §9). A definition without them does not conform.
- A statement cites its type by `type-ref` = (DefinitionId, local label)
  (`SPEC-0002` §7.4), never by URI. This is `ARCH-0002` P1 applied to predicate
  types.
- Rendering is a function of the statement and its definition alone
  (`SPEC-0003` §10). It needs no definition-specific code, and a definition can
  never ship code.

DEC-007 is closed. **This is what `PredicateType` means in `ARCH-0001` §4.1 from
v0.2.0 on.**

## Acceptance test — what is met, and what is owed

The test as filed: *two unrelated predicate types, one build-provenance and one
non-software, render legible statements through a single renderer with no
type-specific code. Under option 2, changing a rendering must not invalidate
existing signatures and must be detectable as a vocabulary version change.*

| clause | state | evidence |
|---|---|---|
| a single renderer with no type-specific code | **met** | `prototype/wallet/engine/render.py` renders from the definition alone; `prototype/statements/` renders EN and ES with no type-specific code (`ARCH-0002` P3 evidence) |
| build-provenance type | **met** | DV-1 `supply-chain`, TV-4 |
| a second, non-software type, rendered | **owed** | DV-2 `names` and TV-13 exist as vectors, but no test asserts a rendered sentence for them. One wallet test owes it |
| changing a rendering leaves existing signatures valid | **met by construction** | a changed language map is a new body, so it gets a new DefinitionId. Statements cite the old id and their signatures cover only their own bytes |
| detectable as a version change | **met** | `test_statement_in_a_look_alike_vocabulary_fails_semantics`: one changed meaning gives a different hash, and the verdict says *"not the one the statement names"* |

## Alternatives rejected

- **Option 1, out of scope.** The project's stated objective is *semantic*
  assertions. A statement whose meaning lives only in an application cannot be
  verified for meaning, and PICS's contribution (rating systems apart from
  labels) would be dropped.
- **Option 3, inline strings.** Every statement gets larger. A bad rendering
  cannot be corrected without re-signing. Two statements of one type could
  disagree about what their own values mean.
- **Option 4, SKOS / JSON-LD / SHACL.** Their identifiers are URIs (global, and
  contrary to `ARCH-0002` P1). JSON-LD's canonicalisation would sit beside
  KSA-CBOR (`ADR-0004`) instead of under it. Reusing them would import exactly
  the namespace governance P1 rejects.
- **Leave DEC-007 open.** Recommended by the agent, and rejected by the human.
  The specification already implements option 2, `ADR-0002` P3 is accepted, and
  an open decision that the governing specification has already answered only
  misleads the reader.

## Not decided here

- **DEC-004**, the tag language. Under `ARCH-0001` §7 DEC-007, tag languages and
  rendering vocabularies stay distinct. A tag needs intersection semantics; a
  rendering vocabulary does not. This ADR selects no tag language.
- **`ARCH-0002` P4**, domains of discourse as hash-identified sets. This is
  still draft. The ADR accepts definitions, not sets of them.
- Which languages a definition must carry beyond `SPEC-0003` §10.2's selection
  rule.

## Consequences

- `ARCH-0001` §7 DEC-007 is marked accepted and points here. `open_decisions`
  is unchanged (DEC-004, DEC-005).
- `ARCH-0001` §4.1 `PredicateType` becomes the `type-ref` form.
- `DECISIONS-0001` item 5d is closed.
- Owed: the DV-2/TV-13 rendered-sentence test (see the table above).

## Evidence

- `spec/SPEC-0003-ksa-definitions.md` §1, §4, §5.3, §9, §10.
- `spec/SPEC-0002-ksa-core.md` §7.4, §8.9; vectors DV-1, DV-2, TV-4, TV-13.
- `spec/ADR-0003-ksa-core-decisions.md` D1. `spec/ADR-0002-provisional-principles.md` §9 (P3).
- `prototype/wallet/engine/render.py`; `prototype/wallet/tests/test_engine.py`.
- `ARCH-0001-PROPOSAL-v0.2.0` §5, the filed text of DEC-007 and its test.
- `draft-mih-scitt-agent-action-capsule-02`: a disposition vocabulary declared
  in prose, an instance of the gap (proposal §5.2).
