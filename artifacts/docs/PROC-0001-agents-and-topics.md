---
schema: "archdoc/v1"
id: PROC-0001
title: "Agents, topics, and the unit of parallel work"
short_title: "Agents and topics"
description: "Whether the project needs multiple agents, how work is decomposed into topics, and when documents split."
type: process
category: process
status: draft
version: "0.1.0"
version_policy: "semver; MINOR = additive process rules"
date: "2026-09-16"
updated: "2026-09-16"
authors:
  - role: proposer
    id: conversation-claude-opus-5
decision_makers: []
reviewers: []
needs_review: true
reviewed: false
canonical_path: artifacts/docs/PROC-0001-agents-and-topics.md
companion:
  - artifacts/docs/ARCH-0001-authorization-attestation.md
  - artifacts/docs/PLAN-0001-project-plan.md
defers_to: ARCH-0001
agent_notes: >
  Process only. Decides nothing about architecture. Answers two questions raised
  2026-09-16: do we need multiple agents, and do we need topics.
---

# Agents, topics, and the unit of parallel work

Two questions, one answer. **The topic is the unit of parallelism**, and it is
what makes both multi-agent work and document decomposition safe.

---

## 1. The constraint nobody escapes

Two students and one sponsor. **Review capacity is the bottleneck, not
generation.** Agents make output cheaper and review no cheaper at all. Every
agent added past the review budget produces material that either goes unreviewed
— in which case it is not trustworthy and should not be in the repo — or queues
behind a human, in which case the parallelism bought nothing.

This is not a theoretical concern. This week, a proposal asserted that CBOR and
COSE were namespace-neutral. That error survived a research pass and a drafting
pass, and was caught by the sponsor in a single sentence. More agents would not
have caught it; more review did. The lesson is that generation is not where the
project is short.

So: **cap concurrent agent work at what the humans can actually review inside a
week.** With three people and a weekly cadence, that is roughly three to five
parallel lanes, not twenty.

---

## 2. ARCH-0001 is already a multi-agent protocol

This is worth noticing, because it means the hard part is done. ARCH-0001's
front matter says:

> *Other agents: treat this file as the source of truth for architecture state as
> of v0.1.0. Do not invent accepted decisions. Iterate by bumping version and
> appending CHANGELOG. Do not rewrite history in this file.*

That is a coordination protocol: a single writable checkpoint, an explicit
"nothing here is accepted" marker, an append-only history, and §9.4's prohibition
on parallel ideas documents. It is the mechanism that makes concurrent
contributors safe, and it works for agents and humans identically.

The rule that follows: **anything that changes the architecture serializes through
ARCH-0001.** Never two agents on the model at once. They will produce exactly the
divergent parallel documents §9.4 forbids, and reconciling them costs more than
the parallelism saved.

---

## 3. Where multiple agents pay, and where they do not

**Worth it** — independent, bounded, separate output files, cheap to verify:

- **Bibliographic research lanes.** One agent per topic, producing
  `library/records/<id>/` entries and one topic note. No write contention, output
  is checkable against the source document, and this is the largest single body
  of work in the semester. The clearest yes.
- **Fixture generation for DEC-002.** One agent per candidate encoding, each
  writing to its own vector directory. Output is mechanically comparable, which
  is the ideal shape for delegation.
- **Mapping specs (WP2, WP3).** One per foreign format. Separable by
  construction, and each is checkable against a published specification.
- **Adversarial review.** One agent tasked with arguing *against* a proposal
  before a human reads it. Given §1, this is the highest-leverage use available:
  it spends agent time on the scarce resource rather than the abundant one.

**Not worth it** — or actively harmful:

- **Architecture decisions.** See §2. Serialize.
- **Anything touching a file another agent is touching.** No exceptions.
- **Anything where the reviewer cannot check the output faster than producing it.**
  A confident wrong answer in a domain nobody on the team can quickly verify is a
  liability, not a contribution. Most of the cryptographic core is in this
  category.
- **Speculative breadth.** More references is not a better library. §5 of
  PLAN-0001 caps it for this reason.

---

## 4. Topics as the unit of work

A **topic** is a bounded research or design question that owns a set of library
records and one topic note. It is the assignment unit for a student, an agent, or
a work package, and it is bounded precisely so that two topics rarely touch the
same file.

A topic has: a stable kebab-case id; a question it exists to answer; the records
it owns; the ARCH-0001 decisions or requirements it bears on; and an owner. When
a topic's question is answered, the topic note is the answer and the records are
the evidence.

Candidate topics for I1, mapped to what they unblock:

| Topic | Question | Bears on |
|---|---|---|
| `canonical-encoding` | What must hold for a canonical form to be safe to sign? | DEC-002, R-O-05 |
| `namespace-governance` | Who allocates identifiers, and what does key-relative allocation cost? | **R-M-12**, DEC-002, DEC-007 |
| `authorization-reduction` | How do 5-tuple reduction and tag intersection actually compose? | DEC-004, WP6 |
| `local-names` | What does name chaining require, and where does it break? | WP6 |
| `threshold-subjects` | How are *k*-of-*n* subjects represented and verified? | R-M-06, WP6 |
| `artifact-statements` | How do in-toto, SLSA, and PICS structure claims about objects? | WP3, R-M-11 |
| `predicate-rendering` | How is meaning conveyed to a person? | **DEC-007** |
| `library-construction` | How should the library itself be built? | D1 |
| `uptake-failure` | Why did SPKI and PICS fail to take hold? | D3, D9 |

Nine topics, two students, eleven weeks. That is the right order of magnitude,
and `namespace-governance` and `predicate-rendering` are where the project's own
claims live — those two should be owned by humans, with agents used only for
gathering.

---

## 5. When documents split

ARCH-0001 should stay one document while it remains reviewable in one sitting.
Splitting early loses the single-source-of-truth property that makes the
checkpoint protocol work, and §9.4 exists precisely to prevent premature
fragmentation.

Split when a specific decision needs more room than a section can give it — not
on page count. The first candidate is already visible: **R-M-12 (key-relative
extension points)** is cross-cutting, constrains three open decisions, and is
arguably the most novel claim the project has. If it survives review, it likely
warrants **ARCH-0002** rather than a requirement row, with ARCH-0001 referencing
it. That question is filed in the proposal's §8 and in PLAN-0001 §13.

Numbering convention, already implied by existing files and worth stating:
`ARCH-NNNN` architecture, `ADR-NNNN` accepted decisions, `MAP-NNNN` interchange
mappings, `PLAN-NNNN` execution, `PROC-NNNN` process. Every one carries
`archdoc/v1` front matter and is validated in CI.

---

## 6. Recommendation

1. **Use agents for fan-out research, fixture generation, and adversarial review.
   Never for architecture.**
2. **Cap concurrent lanes at three to five** — the weekly human review budget.
3. **Assign work by topic**, one owner each, so lanes do not collide on files.
4. **Keep ARCH-0001 single and serialized.** Split only when a decision outgrows
   a section; R-M-12 is the first likely case.
5. **Humans own `namespace-governance` and `predicate-rendering`.** They are where
   the contribution is, and they are the two places a confident wrong answer would
   be most expensive.

---

## 7. Open questions

**Is adversarial review a standing role or an occasional one?** §3 argues it is
the highest-leverage agent use available. Making it standing — every proposal
gets argued against before a human reads it — costs little and would have caught
this week's error. It also risks manufacturing objections where none exist.

**Do agents get attributed in `authors:`?** ARCH-0001 already does this, recording
`conversation-brainpool256` as architect. If that convention holds, agent-produced
library records and mapping specs should carry the same attribution — which makes
the design-log in PLAN-0001 §8 a byproduct rather than a separate chore.

**Does the topic list in §4 match how the sponsor wants the work cut?** It is
derived from the open decisions and work packages, not from student interest, and
those may not align.
