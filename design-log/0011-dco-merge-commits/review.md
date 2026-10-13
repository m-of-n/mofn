# Review

Human: @Ndewedo-Newbury · 2026-10-12

## The model did not get to make this change unilaterally

The first attempt to edit `.github/workflows/ci.yml` was **refused by the
harness's auto-mode classifier**, which flagged it as a potential *CI bypass*.
That refusal was correct in kind: the change does relax a CI gate, and an agent
editing the workflow that polices its own commits is precisely the shape worth
stopping. The model did not route around it. It verified the supporting claim
against the upstream DCO app, then put the decision to the human with the
alternatives stated.

This is worth logging as evidence in its own right: the guardrail fired on a
**correct** change, and the cost of that false positive was one round trip. We
would rather have that than the converse.

## What was accepted

Both recommendations, **as proposed, unedited**:

1. `--no-merges` on the `dco` job, PR'd rather than pushed to `main`.
2. PR #87 amended with `git commit --amend -s --no-edit` and force-pushed —
   explicitly *not* papered over by the CI change.

The human was shown the rejected alternatives from `produced.md` (rebase the
three branches; ban the Update-branch button) and chose neither.

## What was rejected

Nothing in the diff. One thing in the model's framing:

- The model's first draft of the workflow comment cited
  `design-log/0009-dco-merge-commits/`. **0009 and 0010 are already claimed**
  by open PRs #83 and #87 respectively. Corrected to `0011` before commit. The
  model had assumed the numbers visible on `main` were the whole sequence.

## The four PRs merged before this one was opened

Between the diagnosis and the push, **all four PRs were merged**. #83, #82 and
#78 now report `dco` **pass**; #87 was merged with `dco` still **failing** on
its unsigned `7aa57dd`, which means the check is not a required status.

The model had already amended `7aa57dd` with `-s` as agreed. That amend was
**discarded unpushed** — the branch was merged and deleted remotely, and the
PR's final head (`f5d4953`) is not the commit that was amended. Pushing it
would have recreated a deleted branch to no purpose. `report/0004-uptake` was
reset to `7aa57dd`, its pre-amend state.

**This does not make the change unnecessary — it makes it preventive.**
`ci.yml` is unchanged by those merges: the next contributor to press Update
branch hits the same unsatisfiable failure. What the episode does show is the
cost of the defect, which is that it trains people to merge past a red `dco`.
#87 merging while genuinely unsigned is that habit already forming, and it is
the stronger argument for fixing the check than any of the three false
positives.

## Not a defect after all

The model drafted a finding here that design-log numbering had collided at
`0007` with nothing enforcing uniqueness. `main` had already documented it —
`design-log/README.md` names both `0007` entries, explains that neither is
renamed because an id is cited from PRs and must not silently retarget, and
states that the next entry takes `0011`. The finding was withdrawn. The model
had read the design log from a commit four merges stale.

## Outcome

No ADR: this is tooling, not architecture. DEC-001…DEC-005 and DEC-007 are
untouched, and no encoding, tag language or envelope is assumed or implied by
this change.
