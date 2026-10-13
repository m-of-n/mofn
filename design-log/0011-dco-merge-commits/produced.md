# Produced

Model: Claude Opus 5 · 2026-10-12 · tooling change, no specification text.

## The change

One word in `.github/workflows/ci.yml`, plus the comment explaining it:

```diff
-          done < <(git rev-list "$base..$head")
+          done < <(git rev-list --no-merges "$base..$head")
```

## The argument

The DCO is a certification of **provenance of contributed content** — the
signer attests they have the right to submit the lines they wrote. A merge
commit introduces no lines of its own: its tree is a function of its parents.
There is nothing for its author to certify, and every commit it brings into the
range is still checked individually by the same loop. The gate's strength over
authored content is unchanged.

The practical argument is stronger than the principled one. The merge commits
in question were written by GitHub, server-side, in response to a button in the
PR UI. A gate that fails on them is unsatisfiable: the contributor cannot amend
a commit they never had. The only remedies are to rebase away a commit GitHub
just created, or to stop using the Update-branch button — both of which cost
real workflow for no provenance gained.

## External check

Verified rather than asserted. The upstream DCO app — the implementation most
projects actually run — excludes merge commits by default:

- <https://github.com/dcoapp/app> — "enforces the presence of valid DCO
  signoffs on all commits (excluding bots and merges)"
- <https://community.finos.org/docs/governance/Software-Projects/dco> — FINOS
  governance documentation of the same behaviour

A 2017 linux-kernel thread asked for `git merge --signoff` after a bot flagged
an unsigned merge; the reply was that the bot should exclude commits with no
patch contents. The app's current default is that resolution.

So `--no-merges` does not make this repo's gate laxer than the ecosystem norm —
it makes it match. The pre-existing check was *stricter* than the DCO app, and
the strictness bought nothing.

## Alternatives the model considered

1. **Rebase the three branches onto `main`** to drop the merge commits. No CI
   change. Rejected as a standalone fix: it force-pushes three open PR branches
   and the failure returns the next time anyone clicks Update branch. It treats
   the symptom.
2. **Ban the Update-branch button** in `CONTRIBUTING.md`, requiring rebase.
   Rejected: it imposes a rule on every future contributor to preserve a check
   that was never meant to cover merges.
3. **Leave CI alone; sign off every merge manually.** Not possible — see above.

## Not covered by this change

PR #87's `7aa57dd` is a real missing sign-off. `--no-merges` does not and must
not help it; it was fixed by amending the commit with `-s`.
