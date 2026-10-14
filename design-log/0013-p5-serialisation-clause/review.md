---
schema: "design-log/v1"
id: DL-0013
part: review
date: "2026-10-13"
---

# DL-0013 — what a human decided, and what the model declined

**Status: human review of the output is PENDING.** Written in the same change
per the `DL-0001` rule. What is settled is recorded as settled; what is not is
marked open. Nothing here predicts the reviewer's verdict, and nothing here
accepts anything.

---

## 1. Decided by the human

**The order of work, and only that.** *"start with T-029d and T-029e and then
ask me about dec-002."* No architecture direction was given, no position on the
DSSE collision, no instruction about `mofn#72`. Everything in §2 and §3 of
`produced.md` is the model's judgement and is open to being overruled.

**What this entry cannot yet record** is the half `CLAUDE.md` says makes the
claim credible: what a human **rejected**. The review is pending. If the
reviewer overrules the asymmetric resolution in §3, or judges `mofn#72` out of
scope for T-029d, that belongs here and the entry should be amended in the same
change that records it — not a week later.

## 2. Refused by the model, and the refusal is the point

**T-029d asked, on its face, for an acceptance. The model did not make one.**

The row reads *"ADR-0002: accept P2, P3, P5, P6 provisionally (MD-2)"*, is
owned `Claude→PL`, and was eleven days overdue. The literal reading is an
instruction to accept. It was declined, on three grounds that agree:

1. **There is nothing left to grant provisionally.** MD-2 granted exactly that
   on 2026-09-28. The row names the *instrument*, not a fresh grant.
2. **MD-2's own condition is unmet.** "Final only through an ADR **after
   review**." `ARCH-0002` v0.7.0 still carries `reviewed: false` and an empty
   `reviewers` list — amending it did not and could not change that.
3. **`decision_makers` would have to be filled with a name whose owner has not
   acted.** `ADR-0002` §7 already calls this what it is: *a forged provenance
   record in a project whose subject is provenance.* The field stays empty.

`CLAUDE.md`'s first **Never** and the `propose-arch` skill's first hard stop
both say the same thing, and they were written for this exact shape of request:
an overdue row whose wording invites an agent to close it by fiat.

**The honest state of T-029d is `review`, not `done`.** The model moved it from
`overdue` to `review` and named who is blocking: a human reader for `ARCH-0002`.
Leaving it `overdue` would have implied the model still owed work. Marking it
`done` would have been false.

## 3. Proposed for the register, not taken

**A CI check that a repository-wide identifier rename cannot be outrun by a
branch.** `produced.md` §4: item 27 rewrote 129 citations on 2026-10-11 and
missed `ADR-0002` entirely, because that branch was open across the sweep. It
was found by grep, by accident, while doing something else. The `GLOSSARY-0001`
redirect is what hid it — stale citations still resolved for a human reader, so
there was no symptom.

This is the second rename-versus-branch collision in three design-log entries
(`DL-0009` §4 is the first, on design-log ids). **Not filed as a register item
by the model**, because filing register items unprompted is not an agent's call;
proposed here for whoever next edits `DECISIONS-0001`.

## 4. Declined as out of scope — stated so the omissions read as decisions

Per the `propose-arch` skill: *a proposal states what it is not proposing.*

| not done | why |
|---|---|
| **Condition (5)** — canonical order for set-valued fields in arrays | No decoder can supply it; it depends on **P4**, which MD-2 held; `library#56` owns the ordering rule. Named in P5.1 as *not addressed* |
| **Condition (6)** — Unicode normalisation | Named in P5.1 as a **limit** that needs a profile rule, not closed |
| **`ARCH-0001` edits** for `R-O-05` and `R-I-01` | Owed, and recorded as owed in `ADR-0002` §5. They belong to the v0.2.0 change (register item 4), which is a separate decision nobody has taken |
| **Any DEC-\*** | DEC-002 and DEC-005 stay open. P5.1 is an *input* to DEC-002 and says so twice |
| **Backfilling `ARCH-0002`'s changelog 0.1.0–0.5.0** | That is the `DL-0001` failure. The new file starts at 0.6.0 — main's own change, written from its PR — and states the gap |
| **`enforce_admins`, faculty access, Tauri** (register items 22, 23, 28) | Adjacent, overdue, and not asked for |

## 5. One thing a reviewer should push on

P5.2's asymmetry is the weakest claim in the change, and it is weak in a
specific way: **it is reasoned entirely from DSSE, and DEC-005 is open.** If the
envelope turns out to be COSE_Sign1, the analysis has to be redone against
`crit` (RFC 9052 §3.1), where the default runs the *other* way and the
asymmetry may not be needed at all. P5.2 says this in its last paragraph, but a
reviewer who thinks a principle should not carry a clause shaped by one
candidate envelope has a real objection, and the model has no answer to it
beyond *the silence was worse*.


---

## 6. Added on rebase, 2026-10-15

**None of §§1–5 was overruled by a human.** The review this entry awaits still
has not happened; what changed is the ground, not the verdict.

### 6.1 One claim in §2 is now weaker, and it should be said

§2 refused to close T-029d on the grounds that MD-2's condition — *final only
through an ADR after review* — was unmet. That still holds. But §2 also implied
the cost of leaving P5 draft was confined to `prototype/`, `APP-0001` and three
library topics. **That was true on 2026-10-13 and is understated now:**
`SPEC-0002` §13.5 rests a normative MUST on P5 by name. Recorded in `ADR-0002`
§6a and in `produced.md` §7.4.

The refusal was right and the stakes were described too mildly. Both halves
belong in the record.

### 6.2 Raised, not filed — a third rename-versus-branch collision

`produced.md` §7.1: `main` and this branch both set `version: "0.6.0"` for
different changes. Git auto-merged the identical line without a conflict and
`bin/validate-archdoc` passed, because §9.5 only checks that `version` and
`updated` move together — which they did, to the wrong number.

It was caught by reading the incoming diff, not by a tool and not by the
conflict markers. **A check that a `version` bump in `spec/` or `project/` is
strictly greater than the one on `origin/main` for the same file would catch
it mechanically**, and there is nothing subtle in it.

This is the third instance of the same class in four entries — `DL-0009` §4
(design-log ids), `DL-0013` §3 (the `D-n` sweep missing an in-flight branch),
and now a version line. **Proposed for the register, not filed.**

### 6.3 The design-log numbering defect is now self-documenting

Sixth occurrence, and the first requiring an entry to step around both a
*merged* `0011` and an *open* `0012` from this same lane. The entry was
renumbered after its review had already been requested, so the PR, the branch
name and the commit message all still say `0011`.

`DL-0009` §4 proposed a fix and it was not taken. Proposing it again here would
be the fourth time of asking; it is recorded instead as evidence that the cost
is no longer hypothetical.

### 6.4 What a reviewer should check that they would not have had to before

**That P5.1 and P5.2 do not differ from `SPEC-0002`.** `ADR-0003`'s consequences
are explicit: where a SPEC and an ARCH document differ, **the SPEC governs and
the ARCH document is corrected.** This change was written to agree with
`SPEC-0002` §4.3, §5, §4.1 and §13.5 — but that is the model's reading of a
1,110-line normative document it did not write, and the reading is the thing to
check. If there is divergence, the SPEC wins and these clauses are wrong.
