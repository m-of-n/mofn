# Review

Human: @Ndewedo-Newbury · 2026-10-12 / 2026-10-13

## The proposal was REJECTED

**PR #92 was closed unmerged** (2026-10-13 04:21Z). `--no-merges` is not in the
`dco` job and will not be. The decision taken instead:

1. **The check stays strict.** It continues to fail on merge commits.
2. **Contributors rebase** rather than use the *Update branch* button's merge
   default.
3. **`dco` becomes a required status check** on `main`.

Applied the same day: `main`'s required contexts went from `["docs"]` to
`["docs", "dco"]`, every other protection setting unchanged. The rule is
written into `CONTRIBUTING.md` §9 in this change.

## Why the model was wrong

The model dismissed *"require rebasing in CONTRIBUTING.md"* in one line — "it
imposes a rule on every future contributor to preserve a check that was never
meant to cover merges." That framing contained the error.

- It assumed the check's scope was a mistake to be corrected. But `main`
  **already requires linear history**, so a merge commit on a PR branch is
  something this project does not want in the first place. A check that
  rejects them is consistent with that, not accidentally over-broad.
- "Imposes a rule on every future contributor" overstated the cost. The
  *Update branch* dropdown has an `Update with rebase` option one click from
  the default, and `allow_rebase_merge` is already true on this repo. The
  burden is a different menu item, not a workflow.
- The model treated the ecosystem norm (the DCO app exempts merges) as close
  to dispositive. It is evidence about the common case, not about a repo that
  has separately chosen linear history.

The diagnosis was sound and the verification was worth having. The
**recommendation** was wrong, and it was wrong in a specific way worth naming:
the model optimised for making a red check go green, and treated the check
rather than the merge commit as the defect.

## What the model got right, and should keep doing

- It did not act on the diagnosis alone. It put the alternatives to a human
  with the trade-offs stated, and the human chose one the model had argued
  against.
- It verified the supporting claim (the DCO app's default) against sources
  instead of asserting it from memory.
- It proved the exemption would not mask the real defect by replaying the
  patched check over all four ranges and showing #87 still failed.

## The guardrail fired first, and correctly

The model's first attempt to edit `.github/workflows/ci.yml` was **refused by
the harness's auto-mode classifier as a CI bypass**. The model did not route
around it; it escalated to a human. Given the change was then rejected on the
merits, the guardrail's instinct — *an agent editing the workflow that polices
its own commits deserves a human* — was vindicated. This is logged as evidence
that the escalation path works, not as a false positive.

## Known gaps this leaves open

1. **One unsigned commit is on `main`.** #87 merged at 23:52Z with `dco`
   failing on `7aa57dd`, because `dco` was not required until 2026-10-13 and
   `enforce_admins` is `false`. Not rewritten: rewriting merged history for one
   trailer costs more than it returns. `PLAN-0001`'s "DCO, CI-enforced" claim
   is true from 2026-10-13 and was advisory before it.
2. **`enforce_admins` remains `false`**, so an admin can still merge past a red
   `dco`. Making the check required does not close that path. Left as-is; not
   part of the decision taken.
3. **The two repos now disagree.** `m-of-n/library`'s own `dco` job already
   uses `--no-merges` (`ci.yml`, the `dco` job). `mofn` is strict; `library` is
   not. Whichever way it settles, it should settle deliberately rather than by
   drift. Raised for a decision; not changed here.

## Outcome

No ADR: tooling and contribution process, not architecture. No `DEC-*` touched;
`DEC-001…005` and `DEC-007` remain open, and nothing here assumes an encoding,
tag language or envelope.
