---
schema: "design-log/v1"
id: DL-0029
part: review
date: "2026-11-07"
---

# DL-0029 — review

**Human input:** Chip asked the question, asked for a recommendation, and
accepted it ("go"). Human review of the workflow itself is pending on its PR
(David reviews Chip's slice PRs, per mofn#68).

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
