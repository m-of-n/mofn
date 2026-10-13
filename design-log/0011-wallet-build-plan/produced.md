---
schema: "design-log/v1"
id: DL-0011
part: produced
date: "2026-10-12"
---

# DL-0011 — produced

## Artifacts

| file | what |
|---|---|
| `project/PLAN-0006-wallet.md` | build plan, `status: draft`, `decision_makers: []`, v0.1.0 |
| `design-log/0011-wallet-build-plan/` | this entry |

Nothing else was touched. No spec file, no existing plan, no backlog row, no
library record, no submodule pin.

## Shape

§1 states the scheduling finding the rest follows from. §2 is the decision
surface — open `DEC-*`, the unaccepted requirement, the principles, the dated
decisions. §3 is the work in flight. §4 is the anti-requirements. §5 is the
build design, and is the only part that proposes anything technical. §6 is the
order, §7 the mechanical acceptance checks. §8 is what a human still owes, §9
is what is already settled, §10 risks, §11 the limits of the plan.

The split between §8 and §9 is deliberate and is the part most likely to be
useful next week: **a decision the corpus has already taken, and a decision
nobody has taken, look identical from inside a GitHub issue.** `DL-0009` §1
recorded a ten-day cost from exactly that confusion.

## Findings not previously recorded anywhere

Five. Each was found by cross-reading two documents that are individually
correct.

**1. The product moment cites a requirement that is not in the architecture.**
`APP-0001` §4 says "the six dimensions of **R-O-06**". R-O-06 is not in
`ARCH-0001` — it is in `ARCH-0001-PROPOSAL-v0.2.0` §6, whose acceptance is
`DECISIONS-0001` item 4, which the register itself notes is *"not on any
agenda to date"*. **And R-O-06 names three results, not six**: name
resolution, authorization reduction, statement acceptance. Integrity,
authenticity and semantics come from `PLAN-0001` §7.4 and DEC-007. So three of
the six verdict lines have no requirement id, and the other three have one with
no force. Nothing in the repository said this.

**2. `APP-0001`'s command surface cannot do two of the five things `APP-0001`
says a wallet does.** §2 lists hold · collect · make · present · evaluate. §3's
commands are `domain …`, `make`, `check`, `render`, `reduce` — no `init`, no
`key`, no `root` (so it cannot *hold*), and no `present`. `W-1` (#65) supplies
the first group without saying it is filling a gap. `present` is supplied by
nothing, while `PLAN-0004` §5 view 4 *is* Present. The plan proposes the
minimum honest form: the statement set the reducer actually used.

**3. The two wallet documents disagree about where the wallet lives.**
`PLAN-0002` §6.4 says `~/.mofn/`; `PLAN-0004` §6 says `wallet/`. Both are
cited as the on-disk layout. `demo/slice.sh` needs a disposable wallet from a
clean clone, which decides it: a profile directory, `--wallet` → `$MOFN_WALLET`
→ `~/.mofn`.

**4. The two documents also disagree about the view set.** `PLAN-0004` §5 has
five views and no Delegations view; `PLAN-0002` §6.5 sketch ③ is a Delegations
view. The plan resolves it by putting the chain in the Verdict view as
`attributes.standing`, which is also #69's "standing" attribute — so the
disagreement dissolves rather than being split.

**5. Holding P4 invalidates a published sketch.** `PLAN-0002` §6.5 sketch ④
shows `supply-chain  id 2104d6d4…` — a domain presented by hash. P4 (domains
are hash-identified sets) is **held** by MD-2, and register item 5c (is a
domain a statement by a key?) is held with it. Under P1, which *is* accepted,
the identity to display is the defining key. A UI built from that sketch would
implement a held principle.

## The one piece of real design

**Boundary A must be a verify-then-decode boundary.** `W-1` already requires
two codecs behind an interface, which is what keeps DEC-002 open. The plan adds
the constraint that the *shape* of that interface is load-bearing: R-O-05
requires verification over canonical bytes **before** decoding and forbids
canonicalising during verification. An interface shaped `object → dict → bytes`
satisfies "two codecs" and breaks R-O-05 silently, because it invites
verification of a re-encoded object. Hence the four named operations, and
acceptance check **A8** — reject a tampered byte before decode — which is the
only way to tell the two interfaces apart from outside.

This is also why the plan declines to treat the codec count as the whole guard.
Two codecs prove the encoding is swappable. They do not prove the verifier
verifies the right bytes.

## The scheduling move

**Freeze the verdict JSON before the engine exists.** `mofn check --format json`
is `APP-0001` open question 3, currently unanswered and scheduled implicitly for
December. Writing it — plus three golden files — on **Oct 19** converts the
GUI's dependency on the engine into a dependency on reviewed fixtures. It is not
new work: it is `T-045` (R-O-06 separated output) and the `W-4` slice cases
pulled forward.

The cost of not doing it is already visible: the engine owner has no commits and
three other overdue items; the GUI owner merged ~16 PRs last week and is
scheduled last.

## Where the plan recommends against a recorded decision

**MD-7 says Tauri, tentative. The plan recommends the fallback, PySide6.** This
is the output's sharpest claim and the one a reviewer should attack first — see
`review.md` §2. It is written as a proposal with a named overturning test (a
half-day packaging spike before Oct 14), not as a correction.
