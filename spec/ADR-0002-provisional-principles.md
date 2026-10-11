---
schema: "archdoc/v1"
id: ADR-0002
title: "ARCH-0002 P2, P3, P5 and P6 — the instrument D-2 deferred"
short_title: "ADR-0002 provisional principles"
description: "Records D-2's provisional grant over P2, P3, P5 and P6, and proposes the finalisation it deferred. P4 and P7 stay held."
type: decision
category: security
status: proposed
version: "0.1.0"
version_policy: "semver; on acceptance this becomes 1.0.0 and thereafter changes only by superseding"
date: "2026-10-10"
updated: "2026-10-10"
decision_makers: []
reviewers: []
needs_review: true
reviewed: false
canonical_path: spec/ADR-0002-provisional-principles.md
defers_to: ARCH-0001
companion:
  - spec/ARCH-0002-key-relative-naming.md
  - project/meetings/2026-09-28.md
supersedes: []
agent_notes: >
  STATUS IS PROPOSED. `decision_makers` is deliberately EMPTY. D-2 granted
  P2/P3/P5/P6 provisional standing and said each becomes final "only through
  an ADR after review"; that review has not happened — ARCH-0002 still carries
  `reviewed: false` and zero reviewers. Writing a decision maker into this file
  before that person acts would be a false provenance record in a provenance
  project. Accepting this ADR is a status flip plus a name, by the sponsor.
---

# ADR-0002 — P2, P3, P5 and P6

**Status: proposed. Nothing here is accepted.**

This file exists because there is currently **no normative home for the four
principles the project is already building on.** `prototype/statements/`,
`APP-0001`, and three answered library topics all assume P2 and P3. ARCH-0002
marks all six of P2–P7 `[draft]`. The gap between those two facts is what this
ADR closes.

---

## 1. What D-2 decided, and what it deferred

Weekly of **2026-09-28**, decision **D-2**, verbatim:

> **D-2 · T1-B — accept P2, P3, P5, P6 provisionally; hold P4, P7.**
> Accepted *for review and initial progress*: work may build on them now, but
> they are not yet normative — each becomes final only through an ADR after
> review (ARCH-0001 §9). P4 and P7 stay draft.

Two separate things, and conflating them is the error this file is written to
avoid:

| | what D-2 did | standing today |
|---|---|---|
| **granted** | permission to build on P2, P3, P5, P6 | **in force** since 2026-09-28, and recorded nowhere normative until this file |
| **deferred** | making them normative | **not done.** Requires an ADR *after review*; the review has not happened |

`ARCH-0002` carries `needs_review: true`, `reviewed: false`, and an empty
`reviewers` list. So the condition D-2 attached is unmet, and this ADR is
**proposed** rather than accepted.

---

## 2. The decision proposed

**That P2, P3, P5 and P6 become normative, and that P4 and P7 remain draft.**

Accepting this ADR does three things and no more: it flips the four principles
from `[draft]` to `[accepted]` in ARCH-0002, it records the consequences in §5
as owed work, and it leaves DEC-002, DEC-004, DEC-007, DEC-008 and DEC-009
untouched. **It accepts no DEC-\*.**

Until it is accepted, the provisional grant of §1 stands on its own: build on
the four, do not treat them as normative, and do not cite them as settled in a
specification.

---

## 3. Why each of the four

**P2 — the statement form, *A says B has C*.** Demonstrated in the prototype:
naming and attestation take one form. **Strengthened materially since D-2** by
two library topics that neither the sponsor nor the model had when D-2 was
taken. `artifact-statements` finds that a vCon **has no speaker** — it is signed
by whoever assembled it, that signer appears nowhere in the data model, and the
`analysis[]` object records vendor, product and schema and *not who vouches for
the analysis*. `sbom` finds the identical shape in NTIA and CISA: an SBOM is a
B-has-C payload whose *A* is absent, where the signature proves a key handled
the bytes rather than that any principal asserts the composition. **Two live
specifications, found independently, with the same hole.** That is the strongest
evidence the project has that the form earns its place, and it is evidence from
the world rather than from the prototype.

**P3 — a type is a schema.** The prototype renders EN and ES with **no
type-specific code**, which is DEC-007's own acceptance test met one domain
early. Accepting P3 makes multilingual description a requirement rather than a
nicety; that cost is understood and is the point of the principle.

**P5 — validity is checked, never assumed.** RFC 8949's three levels, with
unknown-is-critical as the default. CVE-2025-59420 is the live instance:
Authlib accepted unknown `crit` parameters and produced a possible
authorization bypass. vCon's `critical` mechanism shows that producer opt-in is
the weaker arrangement. **See §6 — P5's scope is about to change, and that is a
sequencing problem for this ADR.**

**P6 — a name is an attested string.** Resolves register item 6a: ARCH-0001
§4.2's five statement *kinds* are five *functions* over one *form*,
distinguished by predicate type. §4.3's separation of the three *procedures* is
untouched and must stay untouched — that was always a claim about procedures,
not object kinds, and reading it as the latter is what made 6a look like a
contradiction.

---

## 4. Why P4 and P7 stay held — and what has changed since

**P7 — unchanged.** No profile has been written. Accepting a principle *about*
profiles before writing one asserts a shape nobody has tested. Write the
supply-chain profile (T1-A, now D-1) first.

**P4 — held, and holding it now costs something it did not cost on 2026-09-28.**

D-2 held P4 because it carries the largest downstream cost of the six and the
least testing: one domain hash-identified in a spike, nobody has versioned a
domain or had two reference each other, and those are where a set-hash gets
hard. That reasoning stands.

What has changed is that P4 **is now an input to DEC-002**, which it was not
understood to be when it was held. The `canonical-encoding` answer makes
conditions (5) — a canonical order for set-valued fields carried in arrays — and
(6) — a declared Unicode normalisation rule — **conditional on P4** and on
`Threshold` members being a set rather than a sequence. Dropping P4 would shrink
that answer to its original four conditions and **restore DEC-002 option 3 to
contention**.

So P4 is no longer only a semantic-layer question deferrable to the spring. It
is load-bearing for an encoding decision due **Oct 28**. This ADR does not
propose accepting it — the evidence has not improved — but it records that
**the cost of leaving it open has moved from the semantic layer to the critical
path**, and that whoever takes DEC-002 is taking a position on P4 whether or not
they say so.

---

## 5. Consequences if accepted

| consequence | owed to | owner |
|---|---|---|
| ARCH-0001 §4.2 rewritten — five kinds become functions over one form | P6, register 6a | register item 4 |
| ARCH-0001 §4.3's three procedures stay separate, explicitly | P6 | same change |
| DEC-007 re-stated in P3's terms, or closed as answered by it | P3 | register item 5d |
| R-M-08 generalises from tags to every constrained object | P2 | ARCH-0001 v0.2.0 |
| Multilingual description becomes a requirement | P3 | WP1 schema |
| Encoder *and* verifier must reject unknown fields | P5 | WP1, T-034 |

None of these is done by accepting this ADR. They are the work it creates, and
they belong in the ARCH-0001 v0.2.0 change, not here. ARCH-0002's own rule
governs throughout: **where it and ARCH-0001 §4 appear to conflict, ARCH-0001
governs and ARCH-0002 is wrong.**

---

## 6. What acceptance requires — two conditions, one of them sequencing

**(a) The review D-2 named.** ARCH-0002 is `reviewed: false` with no reviewers.
D-2 said "final only through an ADR **after review**." A second person must read
ARCH-0002 and say so. Accepting without it would make D-2's own condition
decorative.

**(b) P5's scope is about to change, and accepting it first would churn it.**

`mofn#72` proposes extending P5 to cover **non-canonical serialisation of known
content** — condition (2) from `canonical-encoding`. P5 as drafted speaks to
unknown *content*; condition (2) speaks to a non-canonical *serialisation* of
content that is perfectly well known. The library's answer judged that extending
P5 by a clause is cheaper and truer than minting an `R-O-07`, and explicitly
left the amendment to this repository.

If P5 is finalised at today's wording and #72 lands afterwards, a principle
accepted one week is amended the next — which is exactly the churn an ADR
exists to prevent, and the reason `version_policy` says an accepted ADR changes
only by superseding it.

> **Recommended sequencing: land #72's P5 clause first, then accept this ADR
> over the amended P5.** The alternative — accept P2, P3, P6 now and hold P5
> for #72 — is available and is worse, because P5 is the principle the
> prototype's reject-don't-repair behaviour already depends on, and splitting
> the four leaves it the only one still unwritable-against.

---

## 7. Alternatives rejected

**Accept all six.** Rejected: P4 and P7 have the evidence D-2 found wanting, and
nothing since has improved it. §4 records that P4's *cost* has changed, which is
not the same as its evidence changing.

**Accept nothing until ARCH-0001 v0.2.0 lands.** Rejected: that is the status
quo, and the status quo is the problem. Work already in the repository builds on
P2 and P3 with no normative basis — `prototype/statements/`, `APP-0001`,
`PLAN-0004`, and the `artifact-statements`, `sbom` and `scitt` topic answers.
Leaving them unbacked does not make them not depend on the principles; it only
makes the dependency undocumented.

**Mark this ADR `accepted` now, citing D-2 as the authority.** Rejected, and
this is the central judgement in the file. D-2 is a minute. `CONTRIBUTING` §5:
*"Never mark a DEC-\* accepted in a PR description, a Zoom note, or a commit
message. Only an ADR accepts a decision."* More pointedly, D-2 *itself* said
these become final only through an ADR after review — so citing D-2 to skip the
ADR inverts the thing D-2 said. An ADR carries `decision_makers`; filling that
field with a name whose owner has not acted would be **a forged provenance
record in a project whose subject is provenance.** The field is left empty.

**Write the four principles into ARCH-0001 §5 as requirements instead.**
Rejected for the reason `ADR-0001` already gave for R-M-12: a cross-cutting
principle that constrains three open decisions at once does not fit a table
cell, and ARCH-0002 is the home the project chose for exactly this.

---

## 8. Evidence

- `project/meetings/2026-09-28.md` — D-2, verbatim in §1.
- `spec/ARCH-0002-key-relative-naming.md` v0.5.0 — the six principles as drafted.
- `design-log/0002-arch-0002-cycle/review.md` — P2 and P4 were both **model
  proposals the human overruled**; P2 as drafted is the human's correction, not
  the model's. Relevant to how much weight §3's prototype evidence carries.
- `library/topics/artifact-statements.yaml`, `topics/sbom.yaml` — the two
  independent instances of the missing *A* (§3).
- `library/topics/canonical-encoding.yaml` — conditions (5) and (6), and their
  dependence on P4 (§4).
- `mofn#72` — the P5 amendment (§6).
- CVE-2025-59420 — Authlib `crit` handling (§3).
