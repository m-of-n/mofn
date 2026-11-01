---
schema: "design-log/v1"
id: DL-0016
part: question
title: "W-1 wallet engine v0 (#65) — the mofn CLI over KSA, under SPEC-0002…0004"
date: "2026-10-20"
model: "claude-opus-5-5"
human: davidhsiaotw
outcome: "prototype/wallet/: engine, thin store and CLI, 198 tests. No ADR — DEC-004, DEC-005 untouched; follows ADR-0004 and ADR-0005 (DEC-002, DEC-003), accepted on main after this entry opened; A1 and C1–C5 still with Paul."
status: open
---

# DL-0016 — question

## The issue

mofn#65 (W-1): a runnable `mofn` CLI over a local wallet — `init`, `key gen`,
`root add`, `make`, `check` — where `check` prints the six-line verdict and
signature checking happens inside reduction. Acceptance: the three golden
verdicts (authorized → all green; signed by a key with no anchor →
authorization fail; one flipped byte in the artifact → integrity fail), two
codecs behind one interface, no network.

## Context supplied

- The human's own working notes on #65 (v4; supplied as context, not
  committed — the human kept them out of the repo): file layout, terms, commands and flags, engine flow, goldens, the A1–A3 /
  B1–B4 comment posted on #65, the unposted C1–C5.
- On `origin/main`: SPEC-0001…0005 and ADR-0003 (#104), ARCH-0003 (#102),
  `spec/vectors/ksa-core/` (generator and `vectors.json`).
- `prototype/statements/rcbor_decode.py` (the DL-0007 rejecting decoder).
- PR #107 (open at the time; merged later the same day with §11 unchanged):
  the rewritten SPEC-0002 §11 human-review form.

## Question posed

"implement the wallet" — with the notes and the issue as the brief.

## Scope held

Chosen by the human when asked (see review): **the engine in full (tracks
A0 and A of the human's plan) plus a thin store, unlock and CLI**, so the goldens run end
to end in pytest. Chip's track B (#68) may replace or harden the thin parts;
`demo/slice.sh` stays his. Nothing in `spec/`, nothing in `src/`.

The local checkout was on a stale `main` without the SPEC documents; the work
was done in a worktree branched from `origin/main`.
