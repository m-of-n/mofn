# Question

**Asked (2026-10-12):** "for PR's in mofn, most of them aren't passing dco"

No further context. The task was to diagnose, then fix if the diagnosis
warranted it.

## What the diagnosis found

All four open PRs were failing the `dco` job:

| PR | offending commit | kind |
|---|---|---|
| #87 | `7aa57dd R-0004: the uptake report…` | a genuine missing sign-off |
| #83 | `f053240 Merge branch 'main' into doc/ADR-0002-v2` | Update-branch button |
| #82 | `60b6607 Merge branch 'main' into doc/DECISIONS-0001-v2` | same |
| #78 | `9b0c789 Merge branch 'main' into spike/0073-rejecting-decoder` | same |

The check (`.github/workflows/ci.yml`, job `dco`, added under T-005) walks
`git rev-list "$base..$head"` — every commit, merge commits included.

Verified per-commit across all four branches: on #83, #82 and #78 **every
authored commit was correctly signed off**. The sole failure on each was a
`Merge branch 'main' into <x>` commit written by GitHub's *Update branch*
button, server-side. It never exists in the contributor's local history, so no
`git commit -s` can reach it.

So "most of them aren't passing dco" was **three false positives and one true
positive** — not a lapse in contributor discipline.

## The question that needed deciding

Is exempting merge commits the check's correct scope, or a weakening of it?

`CONTRIBUTING.md` §9 said only that contributions are under the DCO; it was
silent on merge commits, on how to update a branch, and on whether `dco` was
advisory or blocking. `project/RETRO-0001.md` had noted the check "never fired
because nothing violated them" — this was its first real firing, and three
quarters of it was noise.
