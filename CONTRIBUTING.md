# Contributing to m-of-n

Two students and a sponsor, mostly async. The repo is the record: **if it is not
in the repo, it did not happen.** Zoom and SMS decide; the repo remembers.

---

## 1. The ladder

Escalate only when the rung below has failed.

| Channel | For | Expectation |
|---|---|---|
| **Issues** | All work. One per task, labelled, on a milestone | Every task is an issue before it is code |
| **Pull requests** | All changes. No direct pushes to `main` | Review within 24h on weekdays |
| **Discussions** | Open design questions, DEC-* debates | Resolved into an ADR, then closed |
| **Weekly Zoom** | Decisions, unblocking, increment demo | 30 min; notes committed the same day |
| **SMS** | Blocked >24h, or a schedule change | Escalation only — **never content** |

---

## 2. Branches

```
main                     protected. no direct pushes, ever
topic/<topic-id>         research and library work
feat/<short-name>        implementation
doc/<doc-id>             architecture and planning documents
fix/<short-name>         corrections
```

Branch names carry the topic or document id so a reviewer knows the blast radius
before opening the diff. One topic per branch — topics are sized (PROC-0001 §4)
so branches do not collide on files.

---

## 3. Worktrees — how two people work jointly without stepping on each other

A worktree is a second checkout of the same repo on a different branch, in a
different directory. You keep one clone, one object store, and as many
simultaneous working copies as you have parallel threads. No stashing, no
branch-switching mid-task, no "sorry, I had uncommitted changes."

```sh
bin/wt new topic/namespace-governance    # create + cd path printed
bin/wt list                              # what is checked out where
bin/wt rm  topic/namespace-governance    # remove when merged
```

Under the hood that is `git worktree add ../mofn-wt/<branch> -b <branch>`.

When to use one:
- **Reviewing a PR while your own branch is dirty.** Make a worktree at the PR
  branch, run it, comment, delete it. Your work is untouched.
- **Two topics in flight.** One per worktree.
- **A long-running agent lane.** Give the agent its own worktree so its edits can
  never collide with yours.

Rules:
- Worktrees live in `../mofn-wt/` — outside the repo, so they never get committed.
- One branch per worktree; git enforces this.
- `bin/wt rm` when the branch merges. Stale worktrees hold locks and confuse
  `git status`.
- The `library/` submodule is per-worktree. `bin/lib-sync` after creating one.

---

## 4. Pull requests

Open a **draft PR on day one of an increment.** A draft PR is the progress
signal; a status update is not. It gives the reviewer somewhere to comment early,
when comments are still cheap.

Every PR states: **what changed / why / how tested / which deliverable**. The
template asks for exactly that.

**Review:**
- One approving review to merge. The students are both Owners and review each
  other.
- `CODEOWNERS` routes `spec/**` and `spec/vectors/**` to Paul —
  the normative surfaces.
- Comment on the line, not in Slack or SMS. A line comment survives; a text does
  not.
- **Suggested changes** for anything under ~5 lines — it is one click to accept
  and it keeps the thread short.
- Resolve a thread only when the change is pushed, not when you agree with it.
- Small and reviewable beats big and correct. One PR per deliverable slice.

**Merging:** squash merge, linear history, signed commits. Delete the branch.
Run `bin/wt rm <branch>`.

---

## 5. Architecture changes serialize

`spec/ARCH-0001-*.md` is the source of truth. Per its §9:

- Edit **in place** for additive clarification; bump `version` and `updated`
  **together**, and append to the changelog. CI enforces this.
- An accepted decision becomes `ADR-NNNN-*.md`, a changelog line, and a status
  update in ARCH-0001 pointing at the ADR.
- **Never mark a DEC-* accepted in a PR description, a Zoom note, or a commit
  message.** Only an ADR accepts a decision.
- Never open two PRs that both change the model. Serialize. Parallel architecture
  branches produce exactly the divergent ideas documents §9.4 forbids.
- Propose against the document (`ARCH-NNNN-PROPOSAL-*.md`), do not write a
  parallel essay.

---

## 6. Document conventions

Every document under `spec/` and `project/` carries `archdoc/v1` front matter and is
validated by `bin/validate-archdoc` in CI.

```
ARCH-NNNN   architecture          ADR-NNNN   accepted decisions
MAP-NNNN    interchange mappings  PLAN-NNNN  execution
PROC-NNNN   process               BACKLOG    tasks
```

`bin/new-doc <kind> <slug> "<title>"` scaffolds correct front matter.

---

## 7. Before you open a PR

```sh
bin/validate-archdoc      # front matter, version/updated coupling
bin/lib-sync --check      # submodule pin is intentional, not accidental
cd library && bin/validate && bin/export
```

CI runs all of it. Running it locally means you find out in 3 seconds instead
of 3 minutes.

---

## 8. First-time setup

Do this once per clone, before your first commit.

```sh
git clone --recurse-submodules https://github.com/m-of-n/mofn
cd mofn && bin/lib-sync --init
```

**Set your git identity to an address GitHub will accept.** If *Block command
line pushes that expose my email* is on in your GitHub settings — it is on by
default — a push is rejected with `email privacy restrictions` when your commit
email is a private one. The error names the setting, not the fix, and it stops
your first push rather than your first PR.

```sh
git config user.email "<id>+<login>@users.noreply.github.com"   # from GitHub → Settings → Emails
git config user.name  "Your Name"
```

Use a repo-local setting (no `--global`) so it does not disturb your other work.
Check it took:

```sh
git commit --allow-empty -m "probe" && git log -1 --format='%an <%ae>' && git reset --hard HEAD~1
```

## 9. Sign-off

Contributions are under the **DCO**. One line, and `git commit -s` adds it:

```
Signed-off-by: Your Name <you@example.com>
```

Code is Apache-2.0. Specifications and documents are CC-BY-4.0.
