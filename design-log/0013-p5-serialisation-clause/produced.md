---
schema: "design-log/v1"
id: DL-0013
part: produced
date: "2026-10-13"
---

# DL-0013 — produced

| file | change | what it is |
|---|---|---|
| `spec/ARCH-0002-key-relative-naming.md` | 0.6.0 → **0.7.0** | P5.1 and P5.2; two rows in *Relationship to ARCH-0001*; `related_rfcs` gains RFC 8785, RFC 9804 |
| `spec/ARCH-0002-CHANGELOG.md` | **new** | ARCH-0002 ran five versions without one |
| `spec/ADR-0002-provisional-principles.md` | 0.1.0 → **0.1.1** | §6(b) met; two §5 consequence rows; §8 evidence; **22 stale `D-n` citations → `MD-n`** |
| `project/DECISIONS-0001.md` | 0.3.0 → **0.3.1** | item 4a; the standing note on item 2 |
| `project/BACKLOG-0001.md` | 0.10.0 → **0.11.0** | T-029d → `review`, T-029e → `done`, T-034 gains P5.1's acceptance test |

Nothing in `src/`. Nothing in `spec/schema/` or `spec/vectors/`. `ARCH-0001`
untouched — the consequences P5.1 and P5.2 create for `R-O-05` and `R-I-01` are
recorded as **owed** in `ADR-0002` §5 and belong to the v0.2.0 change, not here.

---

## 1. T-029e was already done. Only the row was stale

`DECISIONS-0001` v0.2.0 closed T1-A citing MD-1 on **2026-10-10**, and
`PLAN-0002` §2 and §6 already carry MD-1's two in-scope targets. The backlog row
had said `**overdue**` for eleven days against work that was finished.

Flipping it quietly would have hidden the finding, so the row records *what* was
stale: **the row, not the work.** This is the second instance in three entries
of the same class — `DL-0009` §1 found the register sitting behind a sponsor who
had nothing left to decide. **An index that is not updated by the change it
indexes will lie, and it will lie in the direction of more work rather than
less.**

## 2. P5.1 — the serialisation clause

Condition (2) of the `canonical-encoding` answer: *a decoder must reject
non-canonical input rather than normalising it.* Routed to P5 by clause, per the
library's judgement and `mofn#72`, rather than to a new `R-O-07` — P5 already
binds encoder and verifier both, and splitting one rule across `ARCH-0001` §5.3
and `ARCH-0002` would put half of it in each.

Three things the clause says that the issue did not ask for, each because
leaving it out would have left the clause weaker than the evidence supports:

**(a) It is measured, not asserted.** `mofn#73` ran the falsifier the topic
answer named and **it did not fire** (DL-0007): single pass, no re-encoding,
both surviving candidates, 60 fixtures of which 36 negative. P5 was granted
provisionally on an argument; P5.1 is proposed on a measurement. That is the
strongest sentence available and it was not in the issue body.

**(b) The clause is load-bearing under one DEC-002 candidate and redundant under
the other.** RFC 9804 puts smallest-form in the *grammar* — `03:abc` is
ungrammatical, not non-canonical — so a conforming reader cannot omit the check.
Reduced CBOR makes it a rule the implementation must state, and an
implementation that omits it still parses every valid document. Stated as an
**input** to DEC-002, explicitly not a decision in it.

**(c) What rejection cannot reach.** The default display-hint crack and
condition (6) Unicode normalisation are both undecidable by parsing (DL-0007).
They need a **profile** rule, and the clause says so — because a decoder that
silently collapsed either would be performing exactly the normalisation P5.1
forbids. Omitting this would have let P5.1 read as a complete answer to
identity, which it is not.

## 3. P5.2 — the interchange boundary, resolved asymmetrically

DSSE `envelope.md` requires consumers to *"MUST ignore unrecognized fields"*.
P5 says the opposite. `mofn#72` scoped the collision to the **envelope exterior
only** — unknown siblings of `payload`, `payloadType`, `signatures` — and left
the resolution open.

Three resolutions were available. The model took the third.

| | resolution | why rejected / taken |
|---|---|---|
| i | **flat deviation** — P5 governs the envelope exterior in both directions | **rejected.** Costs interoperability on export for no security gain: the security question is only ever what *our* verifier accepts, and an export rule binds consumers we do not control |
| ii | **flat retreat** — P5 stops at the payload interior | **rejected.** Hands an attacker the envelope exterior as a place to carry meaning our verifier never evaluates. That is CVE-2025-59420's shape, which is the evidence P5 itself rests on |
| iii | **asymmetric** — import rejects unrecognised exterior fields; export emits none and requires nothing of foreign consumers | **taken.** Security on the side we control, conformance on the side we do not |

The unenforceability argument in (i) is not new: the `canonical-encoding` answer
raised exactly it against RFC 8785 §3.1, *"that MUST binds parties we do not
control and is unenforceable."* P5.2 applies the project's own existing
reasoning rather than importing a fresh one.

Recorded as bearing on **R-I-03** and owed to the **R-I-01** mapping table, with
a negative fixture as the acceptance test. **It selects no envelope** — DEC-005
is open, and the same analysis is owed for COSE `crit` if COSE is chosen.

## 4. The `D-n` rename missed ADR-0002, and the miss has a cause

Register item 27 renamed `D-1 … D-7` to `MD-1 … MD-7` on **2026-10-11** —
"129 citations rewritten, 75 in `mofn` and 54 in `library`." `ADR-0002` was
written on 2026-10-10 and merged on **2026-10-12**, so it was in flight across
the sweep and inherited none of it. It was the **only** file in `spec/` or
`project/` still carrying the old form; 22 citations, now rewritten.

The cause is the same one `DL-0009` §4 raised about design-log numbering: **a
repository-wide rewrite and a long-lived branch do not compose, and nothing in
CI notices.** `GLOSSARY-0001`'s redirect note meant the stale citations still
resolved for a human, which is precisely why nobody caught it. Proposed as a
register item in `review.md` §3.

## 5. ARCH-0002 had no changelog

Five versions, no changelog, and `R-D-03` names only `ARCH-0001-CHANGELOG.md`.
A MINOR bump to a principle document with no changelog leaves the amendment
traceable only by diff. `spec/ARCH-0002-CHANGELOG.md` is new and **starts at
0.6.0**: 0.1.0–0.5.0 are not reconstructed, and the file says so and says why.
Reconstructing them from the diff three weeks later is the `DL-0001` failure
exactly, and `CLAUDE.md` names `DL-0001` as permanently degraded for it.


---

## 7. Rebased onto five merges, 2026-10-15 — what changed and what was kept

This entry was written on 2026-10-13 against `7668eab`. Between then and the
rebase, `main` took **#93, #95, #96, #98, #101, #102 and #104** — library pin
bumps, the DCO rebase rule, `ARCH-0003`, and **`ADR-0003` plus five normative
`SPEC` documents and a vector set.** That is not a context refresh; it moved the
ground this change stands on.

### 7.1 The conflicts, and which were real

| file | conflict | resolution |
|---|---|---|
| `spec/ARCH-0002-…md` | `updated:` only | **the dangerous one was the line that did *not* conflict** — see below |
| `mkdocs.nav.yml`, `project/PUBLISHING.md` | both sides regenerated | generated; resolved by `bin/manifest` |
| `DECISIONS-0001`, `BACKLOG-0001` | none — `main` never touched them | applied clean |

**The near-miss.** `main` had already bumped ARCH-0002 to **0.6.0** for an
unrelated change (Review/Approval statement functions, the P4 sponsor
direction). This branch also set `0.6.0`. Git saw the *same* line on both sides,
auto-merged it silently, and produced a file at `0.6.0` containing **both**
changes. Only `updated:` conflicted and drew attention to it.

Caught by reading the incoming diff rather than the conflict markers. The
amendment is now **0.7.0**, stacked on main's 0.6.0. **A version line is exactly
the kind of field two lanes set to the same value for different reasons**, and
`bin/validate-archdoc` cannot catch it — §9.5 only checks that `version` and
`updated` move together, which they did.

### 7.2 `SPEC-0002` instantiates P5.1, so the clause was rewritten rather than rebased

The substantive find. `SPEC-0002` §4.3 now states P5.1's rule **normatively**
for KSA-CBOR — *"Rejection MUST NOT be replaced by repair: a decoder MUST NOT
re-sort, re-encode or otherwise normalise and then accept"* — enumerates seven
conditions, and **cites `mofn#78`**, this project's own decoder spike, for the
single-pass claim. §5 states the verification ordering. `ADR-0003` records the
same reasoning in choosing to verify before decoding where FKSA re-encoded.

So P5.1 stopped being a proposal. Rewritten accordingly:

- It now **points at `SPEC-0002` §4.3 as the instance** and states the principle
  the SPEC instantiates, which is what `ADR-0003`'s consequences assign ARCH
  documents to do.
- **Condition (6) is recorded as closed**, not open. `SPEC-0002` §4.1 takes the
  explicit-refusal route — text *"preserved byte-exact; MUST NOT be normalised
  … by any producer or verifier"*. The previous draft carried it as a live
  limit; that was true on 10-13 and false on 10-15.
- The **option 1 / option 5 asymmetry was kept and resharpened.** `ADR-0003` D2
  fixes the deterministic CBOR profile while explicitly **not** accepting
  DEC-002, and that profile is precisely the one where the grammar does not
  enforce smallest-form. The clause now says *why* `SPEC-0002` §4.3 has to
  enumerate seven conditions where a grammar would have enumerated none.
- The **display-hint crack was demoted** to a conditional note. It is
  option-1-specific and not a live hazard under D2.

### 7.3 P5.2 narrowed, and gained a row

`SPEC-0002` §3 specifies the native envelope and §13.5 settles the interior —
*"an unknown kind or field is invalid. A verifier MUST NOT skip what it does not
understand (ARCH-0002 P5)."* So P5.2 is now **purely about export and import
against a foreign envelope**, which is where it always belonged, and the clause
says so.

Added: the **`KEYID` / `says` collision** as a second row owed to the `R-I-01`
table. DSSE's `KEYID` is unauthenticated and MUST NOT be used for security
decisions; our `says`/`kid` *is* the principal. A mapping that lined them up
because they share a name would put the principal in the one field DSSE forbids
relying on.

### 7.4 The finding that strengthens `ADR-0002`, recorded in it as §6a

`SPEC-0002` §13.5 cites **`ARCH-0002` P5 by name**, in a normative MUST, in an
**accepted** document. P5's own status is `[draft]` and MD-2's grant was
explicitly provisional.

The gap `ADR-0002` exists to close has therefore **widened**. Its §2 opened by
noting that `prototype/`, `APP-0001` and three library topics built on P2 and P3
with no normative basis; `SPEC-0002` is a stronger instance, because it is
normative and is cited by conformance classes. That is the best argument for
accepting `ADR-0002` that has appeared so far, and it arrived from another lane.
