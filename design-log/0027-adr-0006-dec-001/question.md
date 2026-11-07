---
schema: "design-log/v1"
id: DL-0027
part: question
title: "ADR-0006: DEC-001 accepted, m-of-n / mofn"
date: "2026-11-06"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "ADR-0006 1.0.0 accepted; ARCH-0001 0.1.10 (DEC-001 accepted, open_decisions DEC-004, DEC-005); BACKLOG T-001, PLAN-0001 §3 and DECISIONS-0001 cite the ADR; CLAUDE.md and README status lines corrected."
status: open
---

# DL-0027: question

## The brief

The human (`ndewedo-newbury`) asked how to complete mofn#10 (T-023, Shelfmark),
read-only. While answering, the agent noticed that `BACKLOG-0001` T-001 said
"DEC-001 accepted" but `ARCH-0001` §7 and `CLAUDE.md` listed it as open. It
offered two fixes:

- correct T-001 to say DEC-001 is still open; or
- write an ADR accepting the slug.

**The human chose: "write an ADR accepting it".**

The agent then asked two questions:

1. **Sequencing.** PR mofn#129 also edits `ARCH-0001`, and `propose-arch`
   allows one architecture change in flight at a time. Options: draft now and
   hold the PR (recommended), rebase #129 first, or proceed in parallel.
   **The human chose: draft now, hold the PR.**
2. **What to accept.** None of the five listed options was ever used. Options:
   `m-of-n` org with `mofn` repo, package and CLI (recommended), or `m-of-n`
   alone. **The human chose: `m-of-n` org, `mofn` repo.**

## Context supplied

`ARCH-0001` v0.1.8, read in full; `ADR-0005`, as the template; `PLAN-0001`
§0, §3 and §12; `BACKLOG-0001` T-001; `DECISIONS-0001` "What is not waiting on
you"; `git log -S` for the first "DEC-001 accepted" line (mofn#12, `d2a91fb`);
GitHub API creation times for the org and both repos. All read from
`origin/main` after mofn#140. Rebased on `origin/main` at `e89a70c`, after mofn#129 and mofn#141 merged.
