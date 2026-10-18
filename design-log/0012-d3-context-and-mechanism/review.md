---
schema: "design-log/v1"
id: DL-0012
part: review
date: "2026-10-14"
---

# DL-0012 — what a human decided, and what the model declined

**Status: human review of the output is PENDING.** Written in the same change
per the `DL-0001` rule. Nothing here predicts the reviewer's verdict.

---

## 1. Decided by the human

**That the two reports should be written, and that they were due.** Nothing
else. No direction was given on structure, on how to handle MD-3, on the
library pin, or on whether a synthesis pass counts. Everything in
`produced.md` §2–§5 is the model's judgement and is open to being overruled.

**The half this entry cannot yet carry** is the one `CLAUDE.md` says makes the
claim credible: what a human **rejected**. If the reviewer judges §3.9 of
R-0006 to be too close to advocacy, or judges a no-retrieval pass to be
insufficient for D3, that belongs here and should be written into this entry in
the same change that records it.

## 2. The judgement most likely to be wrong

**That a synthesis pass is an acceptable D3 report.**

The case for: `BACKLOG-0001` scopes both tasks as drafts from existing
material, the evidence is already at FX-1 depth, and the reports were due the
day they were asked for.

The case against, which a reviewer should weigh properly rather than take the
model's word on: `research/README.md`'s two rules exist because
`docs/construction.md` was written from research that was then discarded — *"the
conclusions survived, the basis did not."* A report with an empty `searches.md`
is structurally closer to that failure than to R-0004, which ran 15 queries and
recorded the misses. **R-0004 found things R-001 missed because it searched.**
R-0005 cannot have.

The model's mitigation was to make the limitation loud — both `searches.md`
files lead with it, R-0005's names the exposure (statutory material, §3.2), and
both reports' front matter says *synthesis pass, not a retrieval pass* in the
first screen. **That is disclosure, not remedy.** If D3 context is taken past
draft, a retrieval pass is the thing to add.

## 3. Raised, not filed

**R-001 cites at least four keys that do not resolve at `library@f57dcbc`** —
`zooko-2001-names`, `w3c-did-core`, `zcap-ld`, `wang-2006-reducing-spki`
(`produced.md` §4). R-001 carries no `library_pin` in its front matter, which
is itself the finding: its bibliography is not reproducible as
`library@<commit>`, which is the property `README.md` claims for the library.

Three possible causes and the model established none of them: the records were
renamed, they were dropped in the Threat-Radar fold-back (`c95f204`), or R-001
cited keys that never existed.

> **Resolved on the rebase, 2026-10-16.** The pin moved to `60b3284` and **all
> four resolve there**; a full re-check finds all **175** of R-001's distinct
> keys resolving, zero unresolved. So it was none of the three guesses: the
> records existed and the pin was behind them. `produced.md` §7.1.
>
> **The half that is still true** is the one that mattered: R-001 carries no
> `library_pin`, so "resolves today" is not the same as "reproducible", and the
> next pin move can break it again silently. Still **not filed** — not an
> agent's call — and still proposed for whoever next touches R-001.

**Also raised:** `DECISIONS-0001` Tier 3 item 11 is answered in practice by
this change (`produced.md` §1) and is still printed as open.

## 4. Declined as out of scope

| not done | why |
|---|---|
| **Any retrieval pass** | Both tasks are scoped as drafts from existing material. Doing fresh research would have been a different and much larger task, and would not have been finishable today |
| **Picking a DEC-002 option** | `CLAUDE.md`'s first **Never**. And §3.8 of R-0006 is the substantive reason: the rankings genuinely disagree |
| **Reopening MD-3 or the 2026-09-16 correction** | Both are human decisions. R-0006 §3.9 states where the evidence sits and routes the question to mofn#8 |
| **Reading RDF Canon 1.0** | Prior art for condition (5), deliberately unread; `library#56` owns it, and it is in `library/`, where this session must not work |
| **Updating R-001** to carry a `library_pin` | It is a merged report with its own owner. Raised in §3 instead |
| **Filing the two register items above** | Not an agent's call |
| **Writing the `SPEC-0002` §8.6 fix that §3.13 implies** | The fix looks obvious and short — invoke `SPEC-0003` kind 7's *"distinct … sorted"* on `trusts`, state an order for `about` — which is exactly when an agent should not edit a normative specification. `SPEC-0002` is governed by an accepted ADR; `ARCH-0001` §9.4 and `CLAUDE.md` route it through a proposal against the document. Stated as a finding, filed in R-0006 §8 |
| **Reading `ADR-0003` D2 as accepting DEC-002** | D2 refused it in terms. The encoding is fixed and the decision is open, and R-0006 §3.9 keeps them apart rather than collapsing them into the convenient reading |
| **Reading `SPEC-0002` §5 as settling DEC-005** | Tempting by symmetry — the core now has an envelope — but `ADR-0003` is *silent* on DEC-005 where it was explicit on DEC-002, and the difference between *decided* and *not written down* is not an agent's to infer. Raised in R-0006 §5.2 and §8 |
| **Updating `DECISIONS-0001` Tier 1 item 2 for D2** | It is the right place to record that an accepted ADR fixed the encoding, and **mofn#97 already edits that file**. Doing it here would manufacture a conflict between two open PRs for no gain. Routed as a next step instead |
| **Reopening D2, or answering mofn#8** | R-0006 §3.9 notes only that the bar moved — the request now means superseding an accepted ADR — and explicitly does not recommend it |

## 5. What a reviewer should push on hardest

**R-0005 §8 and R-0006 §3.9 are the two places the model argued rather than
reported**, and they are the two places to read adversarially.

§8 of R-0005 says three of the five reasons SPKI failed are structural
properties of this design today, cites R-0004 §8 for it, and declines to assert
that the project will fare better. That is the strongest available statement of
the risk — but it is also *the model writing the project's own obituary in the
project's own deliverable*, and a human should decide whether a context report
is the right place for it or whether it belongs only in R-0004.

§3.9 of R-0006 is the one the sponsor will care about. It is written to state a
fact — the scoring postdates both decisions — without asserting a conclusion.
Whether it succeeds at that is a judgement the model cannot make about its own
prose.

---

## 6. The second pass, and what a reviewer should check first

Added 2026-10-16 with the `ADR-0003` reconciliation (`produced.md` §7).

**Decided by the human:** that #103 should be completed and that §§3.9 and 6 of
R-0006 were describing a world that moved. The §3.13 finding was not asked for
and was not anticipated; it came out of reading `SPEC-0002` §8.6 against the
report's own condition (5). Whether it belongs in a research report at all —
rather than as an issue against `SPEC-0002` — is a human judgement and the
model has taken the conservative option of stating it and not acting on it.

**The thing to check first, because everything else rests on it.** §3.13's
central claim is checkable in four lookups and a reviewer should do them rather
than trust the report:

1. `SPEC-0002` §8.6 — `trusts: [2* kid]`. No `distinct`, no sort rule.
2. `SPEC-0002` §4.1 — array: *"ordered; order is significant and signed"*.
3. `SPEC-0002` §4.5 — statement digest = SHA-256 of the TBS.
4. `SPEC-0004` §6.4 — *"trusts a set `M` of keys"*, *"Distinctness is by kid."*

If those four read as quoted, one semantic trust statement has many digests and
the rest of §3.13 follows. If any is misquoted, **§3.13 should be struck** and
the model got it wrong; it is a claim about four documents, not an argument, and
it should be treated as falsifiable in exactly that way.

**Where the model may have overreached.** §3.13's closing paragraph says the
specifications are not wrong and that `SPEC-0003` §6 is the best treatment
condition (5) has had in this project. That is a judgement, it is favourable to
documents the sponsor authored last week, and a reviewer entitled to be
suspicious of a model complimenting the thing it just audited should read it as
such. The underlying observation — eleven base kinds, eight with set-valued
array ranges, all eight given an order — is countable and does not depend on the
compliment. (The first draft of §3.13 said *seven*; `SPEC-0003` §6's email kind
was miscounted and the figure was corrected before this change was committed.)

**What is still owed and is not in this change.** `DECISIONS-0001` Tier 1 item
2 still reads as though MD-3's narrowing were the latest word on the encoding;
it is not, and `ADR-0003` D2 belongs in that row. It was left out on purpose
because mofn#97 edits the same file (§4).

## 7. Third pass — closing #99's checklist (2026-10-17)

Asked: *what is required to complete #99*, then *complete the next steps*.
Done:

- **`PLAN-0001` §6** "Regulatory forcing functions (§9)" → "(§11; seed
  sources §15)". §9 is *Increments*; the regulation material is in §11 and the
  seed list in §15. `PLAN-0001` 0.6.0 → 0.6.1.
- **`sources.md` §5** states why there is no `unverified.md`, and records a
  check that no item in R-001's or R-0004's register is stated as fact in
  `report.md`. Five near-miss passages were read; all stay inside their caveats.
- **`BACKLOG-0001`** — the 2026-10-05 snapshot's "D3 … not started" line gets a
  dated supersession note rather than an edit, because the snapshot is a record
  of what was true on that date.

**Declined, and why.**

- **Choosing the T-025 owner.** #99's assignment note says `PLAN-0003` names
  David, while the issue is assigned to Ndewedo and the backlog owner column
  reads `S1`. Who owns a report is a team decision, and the model does not
  make it.
- **Doing a retrieval pass to fill in retrieval dates.** #99 §7 asks for
  "every source, with retrieval dates". R-0005 is a synthesis pass and says so.
  Whether that is enough is the reviewer's call; quietly adding retrievals
  would answer that question on the reviewer's behalf.
- **Rewriting the snapshot line in place** — see above.
