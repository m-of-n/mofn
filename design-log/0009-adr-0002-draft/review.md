---
schema: "design-log/v1"
id: DL-0009
part: review
date: "2026-10-10"
---

# DL-0009 — what a human decided, and what the model got wrong

**Status: human review of the output is PENDING** on mofn#80 and the companion
ADR PR. Written in the same change per the `DL-0001` rule. What is settled is
recorded as settled; what is not is marked open. Nothing here predicts the
reviewer's verdict.

---

## 1. Decided by the human, against the model's framing

**The model assigned four items to the sponsor. That was wrong, and the human
corrected it before any file was written.**

The audit had routed *accept the v0.2.0 proposal*, *the DEC-002 ADR*,
*ADR-0002* and *the register sync* to `@nymble`, reasoning from `CODEOWNERS`
and `PLAN-0003`. The human's correction — *"I am owner of the repo also. Some
of the decisions have been made and the sponsor hasn't had time to update
mofn"* — identified the actual error: **the model conflated merge authority
with decision authority, and then let the first gate work that needed only the
second, which had already been given on 2026-09-28.**

The register sync (mofn#80) had been sitting behind a sponsor who had nothing
left to decide about it. It was assigned for **Sep 30** and was carried out on
**Oct 10** partly because the model re-raised a gate that D-1 had already
opened. That is a ten-day cost attributable to the framing, and it is recorded
because the failure is cheap to repeat: *an agent that cannot tell "undecided"
from "decided and unrecorded" will always escalate, and escalation looks like
caution.*

## 2. Scope the human declined

Five items were proposed. **Two were taken — C2 and C3. C1, C4 and C5 were
not.** Recorded because the omissions are decisions, not oversights:

| | proposed | outcome |
|---|---|---|
| **C1** | split the v0.2.0 proposal into a transcription PR and a decision PR, and fold `ARCH-0001` to v0.2.0 | **not taken this round.** It is the largest change and it touches the source of truth; `CONTRIBUTING` §5 says architecture changes serialize |
| **C4** | resync the proposal §8 (the dangling `DEC-P4`, the stale P2/P3/P4 description) | **not taken** — it was folded into C1 and went with it |
| **C5** | delete or correct `src/mofn/__init__.py` | **not taken** |

So three real defects stay on the floor: `ARCH-0001` still has no reference to
`ARCH-0002` or `ADR-0001` in violation of its own `R-D-02`; the proposal still
names a `DEC-P4` that does not exist; and `src/` still contains a file whose
docstring says `src/` is empty and cites a path the 0.1.1 refactor removed.

## 3. Rejected outright — where the model would have forged a record

**The model's first instinct was an `ADR-0002` at `status: accepted` citing
D-2.** It is defensible on its face: D-2 is a committed sponsor decision, and
§1's own transcription rule says a recorded decision may be written up.

**It is wrong, and the way it is wrong is the finding.** D-2 did not say "these
are accepted." It said they become final *"only through an ADR after review."*
So citing D-2 as authority to skip the ADR **inverts the thing D-2 said.** The
transcription rule survives — the model applied it too coarsely, to a decision
that splits into a granted half and a deferred half.

Worse, and the reason this is in `review.md` rather than a footnote: an ADR
carries `decision_makers`. Filling that field with `paul-lambert` because he
chaired the meeting where D-2 was taken would be **a forged provenance record
in a project whose subject is provenance.** The field is empty. The ADR says in
its `agent_notes` why it is empty, so a future reader does not fill it in as
tidying.

**General form, offered for `PROC-0002`:** *an agent may write any field it can
cite. `decision_makers`, `reviewers` and `reviewed` are never citable from a
minute — they record that a named person acted, and only that person's action
creates them.*

## 4. Rejected — the model's own stale-checkout findings, twice in one session

**The first audit reported two defects that did not exist.** Both were
artifacts of reading local `HEAD` instead of `origin/main`:

| reported | actual |
|---|---|
| "submodule pin is five commits behind; none of the library's evidence is visible from mofn" | **already fixed.** `origin/main` carried pin bumps to `e5f5387` (#71) and `93891c9` (#77). Local `mofn` was 3 behind, local `library` 5 behind |
| "the ARCH-0002 P5 condition (2) hand-off is named and undone" | **already filed** as #72, with #73 and #79 behind it |

A third, smaller: the record count was reported as 305 from the stale checkout;
the pinned library reports **304 — 37 written, 267 scaffold, 4 fully
extracted.**

**This is the same failure `DL-0006` wrote up two days earlier**, where a stale
local `main` 22 commits behind caused a design-log misnumbering and a wrong
claim about which entries were contested. *It recurred within 48 hours of being
documented, which means writing it up did not prevent it.* A note in a design
log is not a control.

**Proposed as a rule, not merely an observation:** *before reporting that
anything is stale, missing or undone, `git fetch` and compare against
`origin/main` and the issue tracker. "Not in my checkout" is not a finding.*
This belongs in `PROC-0002` or `CLAUDE.md`, where it can bind, rather than here,
where it cannot. **Neither change is made in this PR** — `CLAUDE.md` is not this
branch's business and the rule should be reviewed before it binds anyone.

**What it cost here:** nothing merged, because both errors were caught on the
second pass and corrected to the human before any file was written. What it
would have cost unchecked: two fabricated work items on a backlog that is
already honest about being behind.

## 5. Accepted from the model, with the human's framing intact

- The **transcription test** itself (§1 of `question.md`) — proposed by the
  model, adopted by the human as the basis for taking C2 and C3 and leaving the
  rest. It survived its own misapplication in §3, which is some evidence it is
  the right rule.
- The **P5 / #72 sequencing recommendation** (§6 of the ADR). Not in D-2,
  not in the library's answer, and the kind of thing that is cheap now and
  expensive after a principle is accepted.
- The **P4 cost finding** (§4 of the ADR) — that holding P4 has moved from a
  semantic-layer deferral to a DEC-002 input.

## 6. Open — and genuinely open

1. **Does the sponsor agree P5 should wait for #72?** The ADR recommends it and
   does not assume it. If he prefers to accept all four now and amend P5 later,
   the `version_policy` line in this ADR is the thing that has to give.
2. **Has anyone reviewed `ARCH-0002`?** It is `reviewed: false` with zero
   reviewers. D-2 made review a precondition. If a review happened verbally it
   is not in the repo, and `CONTRIBUTING`'s first line applies: *if it is not in
   the repo it did not happen.*
3. **Design-log id allocation.** Third collision — `0004` claimed twice, `0007`
   claimed twice, and this entry took `0009` to avoid a fourth. `DL-0006`
   resolved its instance "by `main`"; that is a convention for cleaning up
   afterwards, not for preventing it. **Proposed as a `DECISIONS-0001` Tier 3
   item**, not filed here, because the register is being changed on a different
   branch (mofn#80) and two branches editing one file is the collision this
   whole entry is about.
