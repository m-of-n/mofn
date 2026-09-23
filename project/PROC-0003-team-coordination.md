---
schema: "archdoc/v1"
id: PROC-0003
title: "Team coordination across repositories — lanes, skills, and who opens what"
short_title: "Team coordination"
description: "How a small distributed team splits work across two repos without colliding, and which project root to open for which task."
type: process
category: process
status: draft
version: "0.2.0"
version_policy: "semver; MINOR = additive process rules"
date: "2026-09-22"
updated: "2026-09-22"
decision_makers: []
reviewers: []
needs_review: true
reviewed: false
canonical_path: project/PROC-0003-team-coordination.md
companion:
  - project/PROC-0001-agents-and-topics.md
  - project/PROC-0002-multi-agent-ingestion.md
defers_to: ARCH-0001
---

# PROC-0003 — Team coordination across repositories

**Status: draft. Open for review.**

Four people, two repositories, several lanes running at once. PROC-0001 says the
**topic** is the unit of parallel work; PROC-0002 says how an ingestion lane
runs. This says how the lanes stay out of each other's way, and — the part that
is easy to get wrong — **which project root to open.**

---

## 1. Skill partition: open the repo you are working in

**Claude Code loads skills from the project root only. Never transitively
through a submodule, and never from a parent directory.**

This is not a detail. A session rooted at `~/cb` — the umbrella workspace —
loads `~/cb`'s skills and **none of m-of-n's**. Work done that way runs without
`ingest-reference`, `summarize`, `propose-arch` or any of the judgement they
carry, and nothing warns you.

| Working on | Open as project | Skills you get |
|---|---|---|
| library records, ingestion, summaries | **`library/`** | `ingest-reference`, `summarize`, `distill` |
| architecture, plan, spec, backlog | **`mofn/`** | `propose-arch`, `close-topic` |
| both at once, or neither | `~/cb` | the workspace skills only — **not these** |

So the skills are **partitioned by what they act on**, not gathered in one
place:

- Skills that act on **library records** are canonical in `library/.claude/skills/`.
- Skills that act on **m-of-n documents** live in `mofn/.claude/skills/`.
- Neither is duplicated. Duplicates drift, and a drifted skill is worse than a
  missing one because it looks authoritative.

**If you are unsure which root you are in, you are in the wrong one.** Check
before a long ingestion run, not after.

---

## 2. Lane assignment

A **lane** is one person or agent, one topic, one branch, one worktree, in one
repository.

| | |
|---|---|
| **Unit** | a topic (`library/topics/<id>.yaml`) — one bounded question, one owner |
| **Branch** | `topic/<id>` in whichever repo the work lands |
| **Worktree** | `bin/wt new topic/<id>` — so two lanes cannot collide on files |
| **Output** | one PR per topic, not per record |
| **Concurrency** | **three to five lanes**, the weekly human review budget |

Lanes are sized so their records rarely touch the same files. When two lanes
keep colliding, the topics were drawn wrong — split them rather than
serialising the people.

---

## 3. Which repo does a lane land in

| Work | Repo | Why |
|---|---|---|
| Ingestion, records, summaries, distillation | `library` | it owns the records |
| Topic notes and answers | `library` | topics live with what they own |
| Research reports (D3) | `mofn` (`research/`) | they cite `library@<commit>` |
| Architecture, ADRs, mappings | `mofn` (`spec/`) | serialised, sponsor-reviewed |
| Plan, backlog, process | `mofn` (`project/`) | |
| Reference implementation | `mofn` (`src/`) | empty until DEC-002 |

**A lane that spans both repos is two PRs**, and the `library` one merges first.
Then `bin/lib-sync --update` moves the pin in a separate commit, so it is
visible that the bibliography a report was written against has changed.

---

## 4. The submodule pin is the coordination point

`mofn` pins `library` at a commit. That pin is the whole synchronisation
mechanism, and it is deliberate:

- Merging in `library` changes **nothing** in `mofn` until someone moves the
  pin. A report citing `library@<commit>` cannot have its bibliography shift
  underneath it.
- **Move the pin in its own commit**, never bundled with content changes. A
  reviewer should be able to see "the library moved" as one line.
- `bin/lib-sync --check` fails a PR where the pin changed without being staged
  — so an accidental pin move cannot ride along unnoticed.

**Version skew is expected, not a bug.** The pinned library may predate a tool
that `mofn` now calls. CI and `bin/manifest` both run only what the pinned
library actually provides.

---

## 4b. Should `mofn` be only a harness? — not yet, and here is the trigger

Asked 2026-09-22. A harness-only `mofn` would hold the site generator, the
publishing manifest, CI and cross-repo coordination; `spec/`, the application
and the library would each live elsewhere.

**Not now.** The cost is concrete: the submodule pin is the coordination point
(§4), and three pins cost three times what one does. The same two people touch
spec, app and site this semester, so splitting adds review surface without
separating any audience.

**The trigger to revisit** — any one of these, and the split earns its cost:

- someone wants the **specification without the site**, or cites it independently
- the **application ships on its own cadence** rather than with the semester
- a **second implementation** appears and needs the spec and vectors alone
- the site outlives the project and needs contributors who do not touch the spec

Revisit in January, or when one of those happens.

## 5. Cadence

| When | What |
|---|---|
| Start of an increment | lanes assigned, draft PRs opened the same day |
| Daily | push to the lane branch; a draft PR is the status report |
| Review, batched | **one topic, 6–10 records, one sitting** (PROC-0002 §4) |
| Weekly, 30 min | decisions and unblocking; notes committed same day |
| End of increment | topics closed or parked with the experiment named |

**A draft PR opened on day one is worth more than a status update.** It gives
the reviewer somewhere to comment while comments are still cheap.

---

## 6. What must never run in parallel

- **Architecture.** One change to `spec/` in flight at a time. ARCH-0001 §9.4
  forbids parallel essays, and two concurrent branches touching the model
  produce exactly the divergence it exists to prevent. Check for an open PR
  touching `spec/` before starting.
- **The record schema.** It is the contract every lane depends on; changing it
  mid-increment invalidates work in flight.
- **Anything touching the same file.** No exceptions, no "small" edits.

---

## 7. Regeneration is a team obligation

Derived views go stale the moment anyone ingests:

```sh
cd library && bin/validate && bin/export && bin/reindex   # index/, exports/
cd mofn    && bin/manifest                                 # nav, PUBLISHING.md, manifest.json
```

CI gates both. The failure they prevent is the quiet one: **the human-visible
bibliography and the published site drifting out of date** while every
individual PR looked fine.

---

## 8. Open questions

1. **Does `~/cb` need a path-scoped rule** pointing at this file, so a
   workspace-rooted session is told to open the sub-repo? It would have caught
   the problem in §1 immediately.
2. **Three to five lanes** is inherited from PROC-0001 and still uncalibrated
   against a team of four with one reviewer.
3. **Who moves the submodule pin** — the lane that merged in `library`, or
   whoever next needs it in `mofn`? The first keeps it current; the second keeps
   it intentional.
4. Should topic ownership be **exclusive**? Two people on one topic is how the
   worktree discipline gets bypassed.
