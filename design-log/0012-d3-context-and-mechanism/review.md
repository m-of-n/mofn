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
cited keys that never existed. **Not filed as a register item or an issue** —
that is not an agent's call — and proposed here for whoever next edits
`DECISIONS-0001` or touches R-001. A `library_pin` on R-001 plus the same
mechanical key check would settle it in minutes.

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
