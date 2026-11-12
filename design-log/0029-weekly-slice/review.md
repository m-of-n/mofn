---
schema: "design-log/v1"
id: DL-0029
part: review
date: "2026-11-07"
---

# DL-0029 — review

**Human input:** Chip asked the question, asked for a recommendation, and
accepted it ("go"). David reviewed the workflow and approved it on mofn#147
(2026-11-08), and it merged 2026-11-09. **DL-0029 is closed.** Session 2,
below, records how the first automated run's notes were actually written.

## Options the agent laid out

| # | option | outcome |
|---|---|---|
| 1 | Cron CI plus the Claude GitHub Action, which reads the output, writes the verdict notes and files findings against mofn#65 | **rejected** |
| 2 | A scheduled Claude routine outside CI, which clones, runs and posts the note as the 2026-11-01 run did | **rejected** |
| 3 | Cron CI posts the raw run and the pass/fail; the slice owner adds the notes by hand | **accepted** |

## Why

- *Rejected 1:* it needs an `ANTHROPIC_API_KEY` repo secret and a running cost,
  and it puts AI judgement about the verdict wording — the part of mofn#68 that
  asks whether a *relying party* can read it — into the record unreviewed. The
  project's AI-assisted design claim rests on recording what a human accepted
  or rejected; a bot that files its own findings erodes that evidence.
- *Rejected 2:* it runs outside the repo's CI, so a broken run is not red
  anywhere a reviewer looks, and it depends on one person's Claude account.
- *Accepted 3:* the mechanical half (clean clone, no network, both codecs,
  goldens byte-identical, post the output) is fully automated and free; the
  judgement half costs the owner a few lines a week and stays human.

## Also considered

- *Rejected:* relying on the existing `ci.yml` `wallet` job alone. It already
  catches golden drift on every PR, but leaves no weekly record on mofn#68 and
  does not catch drift in dependencies or the runner between pushes.
- *Rejected:* `unshare -rn` (unprivileged). Ubuntu 24.04 runners restrict
  unprivileged user namespaces via AppArmor; `sudo unshare --net` then dropping
  back to the runner user avoids that.
- The mofn#68 due window ("every Monday through Oct 28") has passed; the cron
  keeps running because the slice is the Nov 11 floor demo (mofn#31). Disable
  the workflow, or narrow it, when the floor is done.

## Session 2 (2026-11-10): the first automated run

The cron ran on 2026-11-09 (`c84a0e7`). It was green, 10/10, and it posted on
mofn#68 with the notes left as a placeholder, as designed.

**What happened:** Chip told the agent to do every next step "as Chip". So
the agent wrote the verdict notes for the 2026-11-09 run and posted them on
mofn#68 from Chip's account. It also filed the findings as mofn#157, and
dispatched a rehearsal run for the Nov 11 floor. Chip did not read the notes
line by line before they were posted. Both posts say they were drafted by
Claude Code at Chip's instruction.

**This departs from option 3 as accepted.** Option 3 kept the judgement half
human. This week the judgement half was AI-drafted and posted with only a
blanket human instruction behind it. That is weaker than option 1 in one
respect: option 1 at least ran under the repo's own token, where it was
plainly a bot. What makes it acceptable here:

- the posts say who drafted them;
- the findings went to a human owner (David, mofn#157) rather than being acted on;
- this entry records it.

It should not become the weekly pattern. If it does, the honest move is to
revisit option 1, not to keep posting AI notes under a person's name.

**What the agent judged** (open to Chip's or David's correction on mofn#157):

- *F-1, kept.* ③ prints the attestation sentence after `answer: no` under a
  failed integrity line. SPEC-0004 §10.4 is silent on this, so it is wording.
- *F-2, kept but downgraded.* The vacuous `acceptance pass` conforms to
  §10.4 and to DL-0020 A1. The agent leans to explaining it in the spec,
  not changing the result.
- *Rejected as a finding: `fail` vs `FAIL`.* The 2026-11-01 note listed it.
  On checking, SPEC-0004 §10.4 specifies lowercase, so the engine is right and
  only the issue text drifted. The 2026-11-01 finding was the agent's own and
  was wrong.
- *Rejected: adding the archives domain and `--lang` (mofn#154) to the slice
  before the floor.* #154 is unmerged and overlaps mofn#152 (DV-3). Changing
  the floor script two days out risks the demo for coverage the floor does not
  require.

**Still owed:** the cron should be disabled or narrowed after the Nov 11 floor
(see *Also considered*). That is left for its own change, after the floor.

## Session 3 (2026-11-11): the cron is retired, and a correction

**Correction (caught by the human).** Session 1, session 2 and the agent's
posts on mofn#68 and mofn#157 treated "the Nov 11 floor" as a demo
*event*. They spoke of a rehearsal, a run order for the floor, and a "floor
outcome" for mofn#31. Chip asked whether the floor was an event, and it is
not. The **demo floor** is the I3 milestone (Oct 29 – Nov 11): the minimum
scope, D6, that must land if everything after it slips (PLAN-0001 §9,
PLAN-0003). PROC-0004 §5 asks for its demo to be *scripted, rehearsed and
recorded*, which means a recording, not a live showing. No event was held on
Nov 11 and none will be. The one scheduled event is CS Night, Dec 4. The
agent read "the slice is the floor demo script" (mofn#68) as an event without
checking the plans. The dispatched run of 2026-11-10 was a manual workflow run
and nothing more.

**The cron.** mofn#68 asked for weekly runs through I3, which ended Nov 11,
and the issue is closing. So the `schedule:` trigger is removed, as *Also
considered* said it would be. `workflow_dispatch` and the dry run on
`pull_request` stay, and the dispatch still posts on mofn#68. `ci.yml` still
runs the slice on every PR.

*Rejected:* deleting the workflow. A manual clean-clone run, with no network,
is still the cheapest proof before a recorded demo or CS Night, and nothing
else in CI gives one.

*Rejected:* keeping the weekly cron. The issue it posts to is closing, and
weekly posts with no owner notes would contradict option 3.
