---
schema: "archdoc/v1"
id: ADR-0002
title: "ARCH-0002 P2, P3, P5 and P6 — the instrument MD-2 deferred"
short_title: "ADR-0002 provisional principles"
description: "Records MD-2's provisional grant over P2, P3, P5 and P6, and proposes the finalisation it deferred. P4 and P7 stay held."
type: decision
category: security
status: proposed
version: "0.1.4"
version_policy: "semver; on acceptance this becomes 1.0.0 and thereafter changes only by superseding"
date: "2026-10-10"
updated: "2026-10-26"
decision_makers: []
reviewers: []
needs_review: true
reviewed: false
canonical_path: spec/ADR-0002-provisional-principles.md
defers_to: ARCH-0001
companion:
  - spec/ARCH-0002-key-relative-naming.md
  - spec/ARCH-0002-CHANGELOG.md
  - project/meetings/2026-09-28.md
supersedes: []
agent_notes: >
  STATUS IS PROPOSED. `decision_makers` is deliberately EMPTY. MD-2 granted
  P2/P3/P5/P6 provisional standing and said each becomes final "only through
  an ADR after review". As of 2026-10-16 that review has HAPPENED for the
  document as its author drafted it: ARCH-0002 v0.7.1 carries a reviewer and
  `reviewed: true`. One residue remains and §6(a) states it — the reviewer
  wrote P5.1 and P5.2, so the amendment half of P5 has not been read by anyone
  who did not write it. Writing a decision maker into this file before the
  sponsor acts would still be a false provenance record in a provenance
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

## 1. What MD-2 decided, and what it deferred

Weekly of **2026-09-28**, decision **MD-2**, verbatim:

> **MD-2 · T1-B — accept P2, P3, P5, P6 provisionally; hold P4, P7.**
> Accepted *for review and initial progress*: work may build on them now, but
> they are not yet normative — each becomes final only through an ADR after
> review (ARCH-0001 §9). P4 and P7 stay draft.

Two separate things, and conflating them is the error this file is written to
avoid:

| | what MD-2 did | standing today |
|---|---|---|
| **granted** | permission to build on P2, P3, P5, P6 | **in force** since 2026-09-28, and recorded nowhere normative until this file |
| **deferred** | making them normative | **not done.** Requires an ADR *after review*; the review happened on 2026-10-16 (§6(a)), the ADR has not been accepted |

As of `ARCH-0002` v0.7.1 the document carries a reviewer and `reviewed: true`,
so MD-2's condition is met for the principles as their author drafted them.
`needs_review` stays `true` for the one residue §6(a) records. This ADR is
still **proposed** rather than accepted, because acceptance is the sponsor's
act and not a consequence of the review.

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
naming and attestation take one form. **Strengthened materially since MD-2** by
two library topics that neither the sponsor nor the model had when MD-2 was
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
supply-chain profile (T1-A, now MD-1) first.

**P4 — held, and holding it now costs something it did not cost on 2026-09-28.**

MD-2 held P4 because it carries the largest downstream cost of the six and the
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
| Decoder must reject non-canonical serialisations, in one pass | **P5.1** | WP1, T-034 |
| `R-I-01` mapping table gains a DSSE envelope-exterior row | **P5.2** | WP3, R-I-03 |

None of these is done by accepting this ADR. They are the work it creates, and
they belong in the ARCH-0001 v0.2.0 change, not here. ARCH-0002's own rule
governs throughout: **where it and ARCH-0001 §4 appear to conflict, ARCH-0001
governs and ARCH-0002 is wrong.**

---

## 6. What acceptance requires — two conditions, both now met, one with a residue

**(a) The review MD-2 named — DONE 2026-10-16, with one thing it does not
cover.**

MD-2 said "final only through an ADR **after review**." A second person had to
read ARCH-0002 and say so; accepting without it would have made MD-2's own
condition decorative.

**`ARCH-0002` v0.7.1 now carries a reviewer and `reviewed: true`.** The review
is a second person's in the sense MD-2 meant: **ARCH-0002 was authored by the
sponsor** — mofn#25, #41 and #44 are the three commits that wrote P1–P7 and the
CBOR note — and the reviewer is not that author.

> **The residue, recorded rather than glossed.** The reviewer is the author of
> **P5.1 and P5.2** (this PR). §6(b) means this ADR proposes P5 **as amended**,
> so two of the clauses being accepted have not been read by anyone who did not
> write them. That is not what MD-2 was guarding against — MD-2 was guarding
> against a principle becoming final with no reader at all — but it is a gap of
> the same kind, and the honest thing is to let the sponsor see it rather than
> record condition (a) as flatly discharged.
>
> **Two ways to close it, and the choice is the sponsor's, not an agent's:**
> accept P2, P3, P6 and **P5 as drafted on 2026-09-22**, holding P5.1 and P5.2
> for a second reader; or read the two clauses — they are two sections of one
> document — and accept P5 as amended. `ARCH-0002` keeps `needs_review: true`
> until one of those happens.

Nothing else is outstanding. `decision_makers` stays empty and this ADR stays
`proposed`: acceptance is a status flip plus a name, and it is the sponsor's
act.

**(b) P5's scope had to change first — and that condition is now MET.**

`mofn#72` proposed extending P5 to cover **non-canonical serialisation of known
content** — condition (2) from `canonical-encoding`. P5 as drafted speaks to
unknown *content*; condition (2) speaks to a non-canonical *serialisation* of
content that is perfectly well known. The library's answer judged that extending
P5 by a clause is cheaper and truer than minting an `R-O-07`, and explicitly
left the amendment to this repository.

**That amendment has landed. `ARCH-0002` v0.7.0 adds P5.1 and P5.2** (#72
closed). This ADR therefore proposes P5 **as amended**, not as drafted on
2026-09-22, and the churn the note below was written to prevent does not arise.

> **Original sequencing note, retained because the reasoning governs any future
> amendment:** land #72's P5 clause first, then accept this ADR over the amended
> P5. The alternative — accept P2, P3, P6 now and hold P5 for #72 — was
> available and was worse, because P5 is the principle the prototype's
> reject-don't-repair behaviour already depends on, and splitting the four
> leaves it the only one still unwritable-against.

**What the amendment changes about what is being accepted.** P5.1 and P5.2 are
additive; neither weakens the original clause, and the four principles proposed
here are unchanged in number and in kind. Two consequences in §5 grow, and are
recorded there: the decoder obligation now covers non-canonical *serialisations*
and not only unknown fields, and P5.2 owes the `R-I-01` mapping table a DSSE
envelope-exterior row that did not previously exist. One point is worth stating
plainly for the reviewer: **P5.1 strengthened materially between MD-2 and
today.** `mofn#73` wrote the falsifier the `canonical-encoding` answer named,
and it **did not fire** — rejection is decidable in a single pass with no
re-encoding, for both surviving DEC-002 candidates, across 60 fixtures of which
36 are negative (DL-0007). P5 was accepted provisionally on an argument; it is
now proposed on a measurement.

**Condition (a) was the only thing left, and it is now met — see §6(a).**
`ARCH-0002` v0.7.1 carries a reviewer and `reviewed: true`. Amending the
document did not and could not achieve that; a person reading it did, on
2026-10-16. What remains is not a condition this ADR sets but a judgement for
whoever accepts it: the reviewer wrote P5.1 and P5.2, so the sponsor decides
whether to accept P5 as amended or to accept the other three principles and P5
as drafted, holding the two clauses for a second reader. **This ADR stays
`proposed`, and `decision_makers` stays empty, until that person acts.**

---

## 6a. What changed on 2026-10-14, and why it strengthens this ADR

`ADR-0003` was **accepted** on 2026-10-14 and `SPEC-0001`…`SPEC-0005` landed as
normative specifications. Three consequences for this file, and the first is
the one a reviewer should weigh.

**(1) A governing specification now rests on a draft principle — and the
instance that matters is inside a conformance class.**

Stated precisely, because the loose version invites a deflection. `SPEC-0001`
…`SPEC-0005` are themselves `status: draft` with `reviewed: false`; what is
**accepted** is `ADR-0003`, whose Consequences provide that *"where a SPEC and
an ARCH document differ, the SPEC governs once this ADR is accepted, and the
ARCH document is corrected."* So the specifications govern by an accepted
decision while carrying a draft status of their own, and the asymmetry below is
about that, not about a document labelled `accepted`.

Two citations of P5 by name, and they are not equally load-bearing:

| where | what it says | inside a conformance class? |
|---|---|---|
| `SPEC-0002` §13.5 | *"A verifier MUST NOT skip what it does not understand (ARCH-0002 P5)."* | **No.** §13 is Security Considerations; `SPEC-0001` §4.2 lists §4, §5, §6, §9, §10 for a Verifier and §4–§8, §11 for a Producer |
| **`SPEC-0003` §7.1** | template non-conformance is *"a rejection at the **expected** level of ARCH-0002 P5, whatever the statement's signature or authorization"* | **Yes.** §7 falls inside `SPEC-0003` §4–§9, which a **Definition Publisher** MUST implement |

**`SPEC-0003` §7.1 is the instance to argue from.** §13.5 is the louder quote
and the weaker location: a normative `MUST NOT`, but in a section no
conformance class requires. §7.1 is quieter and binding — an implementation
claiming Definition Publisher MUST meet it, and meeting it requires knowing what
*"the expected level of ARCH-0002 P5"* is, which is a principle marked
`[draft]` and granted provisionally by MD-2.

A third instance is adjacent and worth naming, because it shows the direction of
travel: `SPEC-0002` §4.3 and §4.1 state **P5.1's rule and condition (6)'s
refusal normatively**, inside both the Producer and Verifier classes, and cite
**no principle at all**. The specification did not wait for the principle; it
restated it and dropped the attribution.

The gap this ADR was written to close has therefore widened rather than
narrowed. §2 opened by observing that `prototype/`, `APP-0001` and three library
topics already built on P2 and P3 with no normative basis. **The SPEC set is a
stronger instance of the same problem**, because unlike a prototype it governs
by an accepted ADR, and unlike a topic answer one of its citations sits inside a
conformance class an implementer is asked to claim.

**(2) P5 is the principle this most affects, and its content has moved.**
`SPEC-0002` §4.3 states P5.1's rule normatively for KSA-CBOR; §5 states the
verification ordering; §4.1 closes the Unicode question by explicit refusal.
This ADR therefore proposes P5 **as amended to v0.7.0**, and the amended text
points at the SPEC as the instance rather than proposing a rule nobody has
written.

**(3) It does not change what is being accepted.** `ADR-0003` accepts five
decisions about the KSA core and keeps `ADR-0001` (P1). It does **not** accept
P2, P3, P5 or P6, and it does not accept DEC-002. The four principles proposed
here are unchanged in number and in kind.

> **Sequencing note.** `ADR-0003`'s consequences say that where a SPEC and an
> ARCH document differ, **the SPEC governs and the ARCH document is corrected.**
> P5.1 and P5.2 do not differ from `SPEC-0002`; they agree with it and state the
> principle it instantiates. If a reviewer reads any divergence, the SPEC wins
> and this ADR should be amended before acceptance, not after.

---

## 7. Alternatives rejected

**Accept all six.** Rejected: P4 and P7 have the evidence MD-2 found wanting, and
nothing since has improved it. §4 records that P4's *cost* has changed, which is
not the same as its evidence changing.

**Accept nothing until ARCH-0001 v0.2.0 lands.** Rejected: that is the status
quo, and the status quo is the problem. Work already in the repository builds on
P2 and P3 with no normative basis — `prototype/statements/`, `APP-0001`,
`PLAN-0004`, and the `artifact-statements`, `sbom` and `scitt` topic answers.
Leaving them unbacked does not make them not depend on the principles; it only
makes the dependency undocumented.

**Mark this ADR `accepted` now, citing MD-2 as the authority.** Rejected, and
this is the central judgement in the file. MD-2 is a minute. `CONTRIBUTING` §5:
*"Never mark a DEC-\* accepted in a PR description, a Zoom note, or a commit
message. Only an ADR accepts a decision."* More pointedly, MD-2 *itself* said
these become final only through an ADR after review — so citing MD-2 to skip the
ADR inverts the thing MD-2 said. An ADR carries `decision_makers`; filling that
field with a name whose owner has not acted would be **a forged provenance
record in a project whose subject is provenance.** The field is left empty.

**Write the four principles into ARCH-0001 §5 as requirements instead.**
Rejected for the reason `ADR-0001` already gave for R-M-12: a cross-cutting
principle that constrains three open decisions at once does not fit a table
cell, and ARCH-0002 is the home the project chose for exactly this.

---

## 8. Evidence

- `project/meetings/2026-09-28.md` — MD-2, verbatim in §1.
- `spec/ARCH-0002-key-relative-naming.md` v0.5.0 — the six principles as drafted.
- `design-log/0002-arch-0002-cycle/review.md` — P2 and P4 were both **model
  proposals the human overruled**; P2 as drafted is the human's correction, not
  the model's. Relevant to how much weight §3's prototype evidence carries.
- `library/topics/artifact-statements.yaml`, `topics/sbom.yaml` — the two
  independent instances of the missing *A* (§3).
- `library/topics/canonical-encoding.yaml` — conditions (5) and (6), and their
  dependence on P4 (§4).
- `spec/ARCH-0002-CHANGELOG.md` 0.7.0 and `ARCH-0002` P5.1/P5.2 — the P5
  amendment this ADR proposes P5 *as amended* by (§6b). `mofn#72`, closed.
- `spec/ADR-0003-ksa-core-decisions.md` (**accepted**), `SPEC-0002` §4.3, §5,
  §4.1 and §13.5 — the normative instance of P5.1, and §13.5's citation of P5
  by name (§6a).
- `design-log/0007-rejecting-decoder-spike/` and `prototype/statements/` —
  `mofn#73`, the falsifier that did not fire. The measurement behind P5.1.
- CVE-2025-59420 — Authlib `crit` handling (§3).
