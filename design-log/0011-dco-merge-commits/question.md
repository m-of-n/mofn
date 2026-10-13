# Question

**Asked (2026-10-12):** "for PR's in mofn, most of them aren't passing dco"

No further context supplied. The task was to diagnose, then — if the diagnosis
warranted it — fix.

## Context the model gathered

All four open PRs were failing the `dco` job:

| PR | branch | offending commit |
|---|---|---|
| #87 | `report/0004-uptake` | `7aa57dd R-0004: the uptake report…` |
| #83 | `doc/ADR-0002-v2` | `f053240 Merge branch 'main' into doc/ADR-0002-v2` |
| #82 | `doc/DECISIONS-0001-v2` | `60b6607 Merge branch 'main' into doc/DECISIONS-0001-v2` |
| #78 | `spike/0073-rejecting-decoder` | `9b0c789 Merge branch 'main' into spike/0073-rejecting-decoder` |

The check (`.github/workflows/ci.yml`, job `dco`, added under T-005):

```sh
while read -r sha; do
  git log -1 --format=%B "$sha" | grep -qi '^Signed-off-by: .\+ <.\+@.\+>' \
    || { echo "::error::missing Signed-off-by: $(git log -1 --oneline "$sha")"; fail=1; }
done < <(git rev-list "$base..$head")
```

Every commit in `base..head`, merge commits included.

## The two populations

Verified per-commit across all four branches: on #83, #82 and #78 **every
authored commit is correctly signed off**. The sole failure on each is a
`Merge branch 'main' into <x>` commit written by GitHub's **Update branch**
button. That commit is created server-side and never exists in the
contributor's local history, so no `git commit -s` can reach it and no
contributor action can fix it.

#87 is different and genuinely non-compliant: a single authored commit with no
trailer.

So "most of them aren't passing dco" was **three false positives and one true
positive**, not a lapse in contributor discipline.

## The question that actually needed deciding

Is exempting merge commits a weakening of the DCO gate, or its correct scope?

`CONTRIBUTING.md` §9 says only that contributions are under the DCO; it is
silent on merge commits. `project/RETRO-0001.md` notes the DCO check "never
fired because nothing violated them" — this is its first real firing, and three
quarters of it is noise.
