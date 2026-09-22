---
schema: "design-log/v1"
id: DL-0002
part: review
date: "2026-09-22"
---

# DL-0002 — what was accepted, edited, and rejected

**Four rounds. The model was wrong in three of them.** That is the entry's value.

## Rejected outright

| model proposed | human corrected to | why the model was wrong |
|---|---|---|
| CBOR's major-type/length split framed as a **defect in tension with validity**, with a "resolution" | **an observation, not a principle** — "not a hard issue", and "much will be built within CBOR wrappers" | Dramatised a neutral encoding property into a problem. Manufactured tension makes a document look rigorous while adding nothing |
| **P2: "constraints come from a speaker"** as the principle | **P2 is the statement form** — *A says B has C* — of which constraint is one *function* | Took the human's example for the category. The example was about constraints; the principle was about statements |
| ARCH-0002 as four principles with P4 = parseability | five principles, parseability demoted to a note | Consequence of the first two |

## Accepted with significant addition by the human

| model had | human added | effect |
|---|---|---|
| a "vocabulary document" per type (DEC-007 option 2) | **a type IS a schema** — representation, constraints, semantics, human-review tags, multilingual descriptions | Collapsed two concepts into one; arguably closes DEC-007 |
| nothing | **domains of discourse: hash-identified *sets* of schemas** | New concept. Puts canonical serialization on the critical path for the *semantic* layer |
| delegation scoped by tag | **delegation scoped by (Domain, Topic)** | Makes domains the unit of *authority scope* as well as meaning — the strongest form of the thesis, and the model did not see it |

## Accepted as proposed
- P1 / R-M-12 and the ADR-0001 split — the human's own prior direction.
- P5 validity at RFC 8949's three levels; unknown fields rejected.
- **CVE-2025-59420** as live evidence — model-supplied, from a search, and it
  converted "strong checking matters" from an assertion into a demonstrated
  failure mode.
- DEC-008's proposed answer: key-local above a fixed core, never below it,
  because a key that defines its own validity can define itself valid.

## Model contributions that survived
Finding RFC 9804 and reading it as *historical*; finding
`draft-mih-scitt-agent-action-capsule-02` as an independent PICS rediscovery;
verifying IANA allocation policy for CBOR tags and COSE headers; declining to
invent the contract form (DEC-009).

## Honest assessment
The model was useful for **retrieval, verification, and drafting structure**, and
consistently wrong about **which idea was the principle and which was the
example**. Three of four rounds corrected exactly that error.

It also over-dramatised twice — the CBOR "tension", and an earlier "stop rather
than ingest" rule the human reversed. **The failure mode is manufacturing
significance**, not missing detail.

**Guardrail held:** no cryptographic primitives generated.
