---
schema: "design-log/v1"
id: DL-0004
title: "Canonical encoding lane B — RFC 8785 extraction and the six conditions"
date: "2026-10-03"
model: "claude-opus-5"
human: ndewedo-newbury
outcome: "library/ 79c543a — rfc-8785 FX-1 record, DSSE summary, topic split, widened canonical-encoding answer. library#43, library#44. No ADR — DEC-002 untouched."
status: complete
---

# DL-0004 — question

## Context supplied

Issue #14 (LANE B, `canonical-encoding`) in full; `mofn/CLAUDE.md`;
ARCH-0001 v0.1.1 §3.1–§3.3, §4.1–§4.3, §5 (R-M-\*/R-I-\*/R-O-\*), §7
(DEC-001…DEC-005), §9; `ARCH-0001-PROPOSAL-v0.2.0` §3.2–§3.4, §7, §9–§11;
`ARCH-0002` P1–P7; `ADR-0001`; `DECISIONS-0001` tier 1 and the T1-A/T1-B
briefs; `prototype/statements/` (`rcbor.py`, `statement.py`, `labeltype.py`,
`reduce.py`, `demo.py`); `library/CLAUDE.md`, `docs/extraction.md` (FX-1),
`schema/record.schema.yaml`, `schema/topic.schema.yaml`, and the library skills
`ingest-reference`, `summarize`, `extract`; the `close-topic` skill.

## Questions posed

Six, in sequence, each shaping the next:

> "for issue #14 in mofn/ tell me more about the canonical coding, what the
> DSSE does and how RFC 8949, RFC 8785, RFC 9804 relate to canonical coding in
> this issue"

> "what is the purpose of this decision, what does it solve?"

> "where does key digests occur, on what artifacts? How are the signed/hashed
> bytes sorted/used currently? would you suggest we conform to the DSSE critique
> and would that change a lot in our codebase/project?"

> "write the topic answer first"

> "widen the question, tell me more about decision 2 (whether it can be left
> untouched for now), do what is recommended for decision 3."

> "do as you recommend"

## How it was decomposed

**Reading was not delegated.** RFC 8785 (984 lines) and the DSSE
`background.md` and `protocol.md` were read by the author model directly before
any agent was launched, so that the topic answer's claims did not rest on an
agent's summary. This is the `DL-0003` rule applied a second time.

**Extraction was delegated**, per FX-1's requirement of multi-agent passes at
maximum effort:

- **Pass 1 — 6 parallel agents**, one per artifact kind (normative,
  requirements, schema, messages, examples, design-notes). Each was given the
  source path and told explicitly to read the source and never a summary or
  another agent's output.
- **Pass 2 — 1 adversarial agent** that did none of the extraction, briefed to
  *break* it rather than confirm it, with named targets to overturn: the
  Appendix B row count, an error verdict the source does not state, the
  non-ASCII integrity invariant, the derived ABNF's escaping production, and
  the load-bearing array-order claim.
- **Pass 3 — 1 cross-check agent** for artifact-against-artifact consistency.

`protocol.md` and `protocol.yaml` were written by the author model, not an
agent, after a judgement that RFC 8785 — unlike RFC 8949 — does contain
procedural content and must not be declared not-applicable.

## Constraints held throughout

`mofn/CLAUDE.md`: **DEC-002 … DEC-005 and DEC-007 are open.** No DEC was marked
accepted anywhere. **No parallel architecture document was written** — the two
amendments this lane recommends are named as `propose-arch` candidates and were
deliberately not drafted from the library repo. No cryptographic primitive was
generated. No third-party document bytes were committed.

`close-topic`: a topic may not be closed over records that are not distilled.
RFC 9804 is still `queued`, so the topic was left `active` with its answer
marked PROVISIONAL, rather than closed.
