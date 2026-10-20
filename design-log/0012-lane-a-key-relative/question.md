---
schema: "design-log/v1"
id: DL-0012
part: question
title: "LANE A — what breaks when registry identifiers are key-relative (R-M-12)"
date: "2026-10-19"
model: "claude-opus-5-5"
human: davidhsiaotw
outcome: "prototype/lane-a/04_key_relative.py + README findings. The signature never breaks; the reader does. No ADR — DEC-002, DEC-004, DEC-005 untouched."
status: open
---

# DL-0012 — question

## The issue

mofn#13 (LANE A): build a COSE_Sign1, an in-toto Statement in DSSE, and a real
SLSA provenance, keep every byte, list every identifier taken from a central
registry, and answer: **what actually breaks if each of those has to be
key-relative instead** — a `(defining key, local label)` pair. That is R-M-12.

The scope update on the issue: because ADR-0001 accepted key-relative naming,
the answer is about the cost of export to COSE / DSSE / in-toto (R-I-03,
DEC-005). Scripts live in `prototype/lane-a/`; `src/` stays empty.

## What was asked of the model, in order

1. *"I created prototype/lane-a/ for mofn#13 — check if they are ready to
   commit."* The human had written `01`–`03`, `common.py`, `run-all.sh` and
   the README.
2. After the review: fix what was found. Constraints set by the human:
   **no PR, no work in the library repo in this session, leave everything
   uncommitted.**

## What the review found

- `01`–`03` ran, verified, and `01`/`02` were byte-identical on a rerun.
- Nothing tested the question itself: no script swapped an identifier for a
  key-relative one. README findings 2 and 3 had nothing behind them.
- The directory sat untracked in the main checkout, on an unrelated branch.
- `prototype/README.md` was deleted in the working tree (the human restored it).
- No design-log entry; `out/SHA256SUMS` and `out/ENVIRONMENT.txt` had never
  been produced.
- "Artifact" was used for files; it is a normative term here (R-M-07).
