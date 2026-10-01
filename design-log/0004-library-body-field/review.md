---
schema: "design-log/v1"
id: DL-0004
part: review
date: "2026-10-01"
---

# DL-0004 — what was accepted, rejected, and still open

**Status: human review of the output is PENDING** on
[library#34](https://github.com/m-of-n/library/pull/34),
[library#37](https://github.com/m-of-n/library/pull/37) and
[mofn#55](https://github.com/m-of-n/mofn/pull/55). This file is written in
the same change as the work, per the DL-0001 rule, and will be amended when the
PR is reviewed. What is already settled is recorded as settled; what is not is
marked open. Nothing here is a prediction of the reviewer's verdict.

## Decided by the human before the model proposed anything

| | |
|---|---|
| **Accepted** | option 1 — `body` is storage plus a coarse grouping; publisher identity to `publisher`, standing to `maturity` |
| **Rejected** | option 2, split the field (multi-valued `publishers`/`standardized_by`) |
| **Rejected** | option 3, grow the enum (`owasp`, `ecma`, `linux-foundation`, …) |
| **Rejected** | a third deferral — #24 and #25 had each already deferred it |

This is the inverse of the usual entry: the **choice** was human and the
**consequences** were delegated. The model's job was to find out what option 1
actually costs, and it cost more than the issue said.

## Where the model corrected the human-authored issue

#27 states that `publisher` is "already rendered in the bibliography" and that
what is lost is `identifiers.ecma`. **Both halves were wrong.** `publisher`
rendered in no human-visible view at all, and `rfc`/`doi` were the only
identifier schemes rendered, so `iso`, `nist`, `eo` and `draft` were invisible
too. Option 1 as written would have moved publisher identity into a field nobody
could read.

This is recorded because it is the direction of correction that does not usually
get written up: the model's contribution was **refusing to accept a premise that
was checkable in `bin/reindex`**, and the issue's option 1 is only sound because
of a change it did not ask for.

## Where the model was wrong, and what caught it

| the model's error | consequence if shipped | what caught it |
|---|---|---|
| Surveyed the repo from `topic/sbom-lane` — 83 records, `index/` and `exports/` tracked — and planned against it. Main was at **280 records** with both directories untracked since library#31 | the plan's final step was "commit the regenerated `index/` and `exports/`", which is now impossible; record counts in every document would have been wrong by a factor of three | cutting the worktree from `origin/main` rather than the local checkout, and re-running the whole survey. **The local submodule checkout being on a stale branch is a trap worth naming** |
| Considered backfilling `publisher` mechanically from `body` for the 158 records missing it | circular — it would have written the shelf back in as the publisher, which is the exact conflation #27 exists to remove | measuring before writing: 0 of the 158 is past `fetched`, so a status-gated warning binds the rule with no migration |
| Wrote the generated `SHELF_NOTE` with an unclosed `**` | a broken bold run at the top of every regenerated index page | reading `index/bibliography.md` after regenerating instead of trusting the write |
| Was about to render **both** `RFC n` and its DOI | 89 IETF bibliography lines padded with a DOI that only restates the RFC number | sampling the identifier values across all 280 records first |

## The model filed a defective issue, then was asked to act on it

`library#36` was raised by the model in the first half of the session. When the
human said *"fix #36 too"*, **two of its four claims turned out to be false**:

| #36 claimed | reality |
|---|---|
| `CLAUDE.md` "Before any PR" tells you to commit `index/` and `exports/` | already fixed by library#31; main reads *"Do not commit"* |
| `summarize/SKILL.md` may carry the same instruction | it does not, and never did |

**Both are the stale-branch error above, repeating.** The model had already
recorded that error as the first of its four and had already moved to a
worktree cut from `origin/main` for the *code*, but wrote the issue text from
the still-stale `/library` checkout sitting on `topic/sbom-lane`. Moving the
work to clean state did not move the *reading* to clean state.

The issue has been corrected in place with the original text preserved in a
`<details>` block, rather than edited silently. The lesson is narrower than
"check your sources": **a stale checkout stops being a trap for the files you
have replaced and keeps being one for every file you have not.**

The remaining two items were real, and the third was worse than filed — a live
bug that has been publishing a bibliography nobody can navigate to.

## Open for the reviewer — the two real calls

1. **Deleting `body` from `tags.yaml` instead of adding `regulator` and
   `other`.** #27 offered "made to agree **or** explicitly separated"; this
   separates, on the argument that two lists drift and one of them already had.
   The counter-argument is discoverability: an agent reading `tags.yaml` to find
   controlled vocabularies now finds a comment instead of values.
2. **`publisher: "OWASP Foundation / Ecma International"`** — two organisations
   in one free-text field, author first. It is what makes option 1 non-lossy for
   the case that raised the issue, and it is also the weakest part of option 1:
   a slash-separated string is not a queryable pair. If the reviewer wants
   CSL-JSON to carry a single publisher, that is the line to change, and it is
   the argument for reopening option 2 sooner.

## Honest assessment

Four model errors in the first half, one of them repeated in the second. The
repeat is the one worth keeping: every error in this entry is the same error —
**acting on state the model had already been told was stale** — and recording it
once did not prevent it recurring forty minutes later in a different medium.
That is more useful evidence than four unrelated mistakes would be.

Option 1 is the **cheapest correct** answer, not the best one. It is correct
because nothing is lost: every fact about CycloneDX 1.7 is recorded and now
rendered. It is not the best one because dual affiliation is represented as
prose in a free-text field, and no query can ask *"what was ratified by someone
other than its author."* §4 says this in writing and names the trigger for
revisiting it, which is the most this decision should claim.

The strongest evidence for the decision was found rather than argued:
`records/other/ecma-424/` is a duplicate stub of `cyclonedx-1-7`, created
because someone saw a second publisher and reached for a second record. That is
the failure mode #27 predicts, already in the library, and it is left in place
and raised separately rather than quietly deleted — ids are stable forever.
