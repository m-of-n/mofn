---
schema: "design-log/v1"
id: DL-0011
part: review
date: "2026-10-12"
---

# DL-0011 — what a human decided, and what the model should be attacked on

**Status: human review PENDING.** Written in the same change per the `DL-0001`
rule. Nothing below predicts a verdict. §2 is the model's own list of its
weakest claims, written before review rather than after, because a review that
has to find them unaided is a worse control.

---

## 1. Rejected by the model, against the easier output

**A wallet design document was the obvious thing to write, and it would have
been a violation.** The request — *"determine how the wallet application is to
be built"* — reads as an invitation to describe a wallet. The corpus already
has two such documents (`APP-0001` behaviour, `PLAN-0004` plan), five issues
with acceptance criteria, and a 63k market survey. A third description would be
the `ARCH-0001` §9.4 failure wearing a product heading: *do not append parallel
documents that diverge; propose a diff.*

So `PLAN-0006` §1–§2 are pointers, not prose, and every fix the plan wants in
another file is listed in §8 as **owed to that file's owner** rather than
performed. Four such fixes were already owed before this plan (`PLAN-0004` §8,
unactioned since Oct 2); the plan adds three more rather than silently doing
any of the seven.

**The restraint has a cost and it should be named:** a reader who opens only
`PLAN-0006` does not get a self-contained description of the wallet. That is
the correct trade here, and it is the trade `CLAUDE.md` already made.

## 2. The three claims to attack first

Listed by the model because, per `RETRO-0001` §6.5, naming the weakest proposal
is where most corrections land.

**2.1 Recommending against MD-7 (Tauri → PySide6).** This is a recorded
sponsor decision, tentative, with a confirmation date two days out. The
argument is one criterion — toolchain count between verdict and screen — and
one piece of evidence — the owner's load. **What the argument does not have:**
anyone has actually packaged and notarized either kind of app for #32. The
recommendation therefore carries its own overturning test (a half-day spike)
rather than asking to be believed. If the sponsor's reason for Tauri was web
skills on the team, or a future web surface, the model does not have that
context and the recommendation should lose.

**2.2 Proposing `present` as a command.** It is a gap in `APP-0001` §3 against
`APP-0001` §2 — that part is a finding, not a proposal. But *filling* it is
scope, in a semester already carrying an unstarted engine. A reviewer may
reasonably say: record the gap, cut the command, drop `PLAN-0004` view 4 to the
ceiling. The plan would survive that cut unchanged everywhere else.

**2.3 The PKCS#8 private-key recommendation.** `PLAN-0004` §6.1 deliberately
leaves the mechanism open between RFC 9580 S2K+AEAD and a modern KDF+AEAD, and
says "this plan does not pick one". §5.5 picks one. The justification — that a
private key file is local, never interchanged, not a statement, and therefore
outside DEC-002 — is believed to be correct, and it uses a vetted library so no
primitive is generated. **But it closes something a prior plan explicitly left
open**, which is exactly the move this project treats as a defect when it
happens to a `DEC-*`. If the reviewer disagrees, the fix is one line: the plan
reverts to naming the two candidates and the engine ships whichever `W-1`
implements first.

## 3. Rejected — three things the model wanted to do and did not

| | wanted | why not |
|---|---|---|
| mark the backlog double-count resolved | `BACKLOG-0001` flags it and declines to resolve it | it is a planning call with an owner. §3.2 proposes a resolution; it does not edit the backlog |
| delete `src/mofn/__init__.py` | `DL-0009` §2 already lists it as an unfixed defect and it contradicts `CLAUDE.md` | it is not this branch's business, and a one-file cleanup inside a planning PR is how unrelated changes get merged unreviewed. Raised in §8.4 instead |
| close `APP-0001` open question 1 (the command name) | it is cosmetic and the cost rises daily | a recommendation with a date is the most a plan may do; closing it is `APP-0001`'s edit |

## 4. Process — what was done to avoid the two failures already on record

`DL-0009` §4 recorded a stale-checkout failure that recurred within 48 hours of
being documented, and proposed a rule that was never filed anywhere binding.
Applied here voluntarily:

- `git fetch` before any claim about state. Local `main` was **1 behind**
  `origin/main` (the #93 pin bump); the worktree was fast-forwarded to
  `origin/main` before anything was written.
- Open PRs checked (**zero**) and remote branches listed before claiming
  `PLAN-0006` and `DL-0011` were free ids.
- Every "not started" and "no commits" in `PLAN-0006` §3.1 is sourced to the
  **2026-10-12 weekly**, not to the absence of something in a checkout.

**The rule is still unfiled.** `DL-0009` §4 proposed it for `PROC-0002` or
`CLAUDE.md`, where it would bind. It remains a note in a design log, which that
same entry observed is not a control. Flagged again, not filed again — a third
design-log note would be evidence that notes do not work, which is already the
finding.

## 5. Open — genuinely

1. **Does `PLAN-0006` survive contact with `W-1`'s owner?** The plan reorders
   that owner's week (contract on Oct 19, engine after) and he has not seen it.
   The §5.3 contract is co-owned by design — written by the engine owner,
   reviewed by the consumer — and neither has agreed to that.
2. **Is the Oct 19 date real, or is it the model moving a date it does not
   own?** The weekly already set "David: W-1 first commit, Oct 19". The plan
   reinterprets that commit as *the contract* rather than *the engine*. That is
   a substitution, and it is the sponsor's to make.
3. **Register item 4 (accept the v0.2.0 proposal) is recommended for
   scheduling before Oct 28** on the grounds that the wallet implements R-O-05
   and R-O-06. The register says it has never been on an agenda. The model does
   not know whether that is backlog or intent.
4. **Does anything here belong in `APP-0001` instead?** Findings 1–5 in
   `produced.md` are all defects in other documents. The plan records them; it
   does not fix them. If the reviewer would rather have the fixes than the
   record, the record is the wrong artifact and §8 should become a PR against
   `APP-0001` and `PLAN-0002`.
