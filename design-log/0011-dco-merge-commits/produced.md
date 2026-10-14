# Produced

Model: Claude Opus 5 · 2026-10-12 · tooling, no specification text.

## What the model proposed — and what was built

A one-word change to the `dco` job, opened as **PR #92**:

```diff
-          done < <(git rev-list "$base..$head")
+          done < <(git rev-list --no-merges "$base..$head")
```

with a comment, and a design-log entry at this number.

### The argument offered

The DCO certifies the **provenance of contributed content**. A merge commit
introduces no lines of its own — its tree is a function of its parents — so
there is nothing for its author to certify, and every commit it brings into
the range is still checked individually by the same loop.

The practical argument was held to be stronger: the merge commits were written
by GitHub, server-side, in response to a button. A gate that fails on them is
unsatisfiable, because the contributor cannot amend a commit they never had.

### External check

Verified rather than asserted. The upstream DCO app excludes merge commits by
default — "all commits (excluding bots and merges)"
([dcoapp/app](https://github.com/dcoapp/app),
[FINOS](https://community.finos.org/docs/governance/Software-Projects/dco)). A
2017 linux-kernel thread asked for `git merge --signoff` after a bot flagged an
unsigned merge; the reply was that the bot should exclude commits with no patch
contents.

### Verification run

The patched loop replayed over all four PR ranges:

```
PR #87  FAIL  (1 checked)  missing: 7aa57dd R-0004: the uptake report …
PR #83  PASS  (1 non-merge commits checked)
PR #82  PASS  (2 non-merge commits checked)
PR #78  PASS  (1 non-merge commits checked)
```

#87 still failed — the exemption did not mask a real missing sign-off.

## Alternatives the model recorded as rejected

1. **Rebase the three branches** to drop the merge commits. Dismissed at the
   time as treating the symptom.
2. **Require rebasing in `CONTRIBUTING.md`**, so the merge commit never
   appears. Dismissed at the time as "imposing a rule on every future
   contributor to preserve a check that was never meant to cover merges."
3. **Sign off merges manually** — impossible; the commit is created
   server-side.

**Alternative 2 is the one that was adopted.** See `review.md`.
