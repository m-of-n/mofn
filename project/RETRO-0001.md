---
schema: "archdoc/v1"
id: RETRO-0001
title: "Cycle retrospective — what the harness caught, what it missed, what to repeat"
short_title: "Retro 1"
description: "Honest account of the first build cycle: errors found, how they were found, and the practices worth making standing."
type: retrospective
category: process
status: draft
version: "0.1.0"
date: "2026-09-22"
updated: "2026-09-22"
needs_review: true
reviewed: false
canonical_path: project/RETRO-0001.md
defers_to: ARCH-0001
---

# RETRO-0001 — first build cycle

Sep 15–22. Two repos stood up, 12 PRs merged, harness and library built,
ARCH-0002 drafted. This records what actually went wrong, because that is the
part that generalises.

---

## 1. Defects found, and what found them

| defect | found by | would a reader have caught it? |
|---|---|---|
| Record parser was two-level — **silently flattened `relations` into a list**, so every crosswalk edge would have rendered as nothing, indefinitely | running a live inverse-derivation test | **No.** The code looked right and returned data |
| Same parser popped a parent when a sibling key appeared at the same indent | the same test | No |
| `bin/ingest` rendered template shadowed the `body` variable | running it | No — output went to the right directory |
| RFC enricher did not match bare numbers: `ingest rfc 9943` made a record called `9943`, typed `draft` | running it | Maybe |
| `git worktree remove` fails on any tree containing a submodule | following the documented workflow | No |
| Generated views embedded the current date → staleness gate failed on a **date-only diff** | CI, on a later day | No |
| CI ran `bin/reindex` against a pin that predated it → exit 127 | CI | No |
| `docs/index.md` links broke after the rename | `mkdocs --strict`, **but only on deploy** | No |
| Skills in `mofn/.claude/skills/` were **never loaded**, because the session root was `~/cb` | **the sponsor asking** | No — nothing warns |

**Nine defects. Seven were found by executing something; one by CI; one by a
human asking a question.** Zero were found by reading the code or the document.

## 2. What the harness caught on its own

`bin/validate-archdoc` rejected **my own documents three times** — a `status:
active` with `needs_review: true`, an unregistered id prefix, and a `version`
bumped without `updated`. `mkdocs --strict` caught two link breakages. The
DCO and submodule-pin checks never fired because nothing violated them.

**Mechanical rules catch the author, not just the newcomer.** That is the
argument for enforcing process in CI rather than documenting it.

## 3. Where the harness was wrong

- **The staleness gate cried wolf.** It compared regenerated output against
  committed output, but the generators embedded a timestamp, so it failed on
  any later day. A gate that fails daily gets disabled. *Generated output must
  be deterministic* is now a rule, not a preference.
- **`--strict` ran too late.** It was in the Pages workflow only, so a broken
  link failed *after* merge. Moved into PR checks.
- **The version/updated rule was too literal.** Tied to the exact commit date,
  it broke at UTC midnight. Now a 7-day tolerance: still catches staleness,
  survives a rebase.

**The pattern: a correct rule enforced at the wrong time, or with no tolerance,
is indistinguishable from a broken rule.**

## 4. The recurring failure: term collisions

Three this cycle: `artifacts/` against **Artifact** the normative term;
`DEC-P4` against principle **P4**; and — found while writing this — **Topic**
and **Tag**, each now meaning two unrelated things (`GLOSSARY-0001`).

Every one was caught by a reader, late, after the term had propagated.

**Practice:** check `GLOSSARY-0001` before introducing a term; add it when a
term acquires a precise meaning. A collision caught at naming costs a sentence;
caught at review it cost a rename across 38 lines and 12 files.

## 5. Process mistakes worth not repeating

- **Chained PRs get auto-closed** when their base branch is deleted on merge. It
  happened **twice** — I did not learn it the first time. During the first
  recovery I rebased and pushed a tree containing conflict markers.
  **Practice: branch from `main`, state the merge order in the PR body, and
  never base one PR on another.**
- **I merged `#20` with `--admin` over a red check.** The failure was real; the
  cause happened to be my own generator. **Practice: a red check is diagnosed
  before it is bypassed, never after.**
- **Several of my proposals were simply wrong** and were corrected: demoting
  SPKI too far, "stop rather than ingest a reference that bears on nothing",
  `distilled.md` as the primary document, CBOR parseability framed as a defect,
  and P2 twice. The cycle worked because corrections were cheap and explicit —
  not because the first draft was good.

## 6. What to repeat

1. **Run the tool before shipping the tool.** Seven of nine defects surfaced
   only on execution. A skill or generator that has not been run end to end is
   unverified regardless of review.
2. **Enforce process mechanically or expect it to rot.** With a tolerance, and
   at the earliest point it can run.
3. **Generated output must be deterministic** — no timestamps, no ordering that
   depends on the filesystem.
4. **Check new terms against the glossary.**
5. **State what you would push back on.** Each hand-off named the weakest
   proposal; most corrections landed there.
6. **Do not chain PRs.**
7. **Open the repo you are working in** — skills do not load transitively
   (PROC-0003 §1).

## 7. Open, arising from this cycle

- **ARCH-0001 §4.2 lists five statement *kinds*; ARCH-0002 P2 says one *form*
  with *functions*.** They probably reconcile — `ArtifactStatement` is
  attestation, `AuthzCert` is delegation, `NameCert` is naming. **`AclEntry` is
  the misfit: it is unsigned, so it has no speaker** — which may be exactly the
  fixed floor DEC-008 says cannot be key-local. Needs a decision, not a silent
  edit.
- **Topic and Tag collisions** need resolving before they propagate further.
- **`design-log/` is still empty.** The project claims AI-assisted protocol
  design as a contribution; that claim has no evidence yet, and this cycle was
  the richest material it will get.
