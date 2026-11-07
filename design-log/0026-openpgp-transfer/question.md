---
schema: "design-log/v1"
id: DL-0026
part: question
title: "OpenPGP → m-of-n: what to take from OpenPGP into the design and the wallet"
date: "2026-11-05"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "ARCH-0001 0.1.9 §3.4 (research inputs, no requirement or DEC change); PLAN-0004 0.2.0 §6.2 (engine proposals); one engine fix, `unlock` binds the seed to its kid. mofn#128. No DEC-* touched."
status: open
---

# DL-0026 — question

## How it was asked

The session started as questions, not a task:

1. *"what is openPGP?"*
2. *"how does it compare to our wallet application? side-by-side compare them"*
3. *"so there is nothing that we can steal from openPGP that could help our wallet"*

The model answered (3) with fifteen numbered borrowings in four groups:
engine (1–5), open-DEC inputs (6–10), anti-lessons (11–13), and interop (14–15).
It proposed that the engine owner take 1–3 into PLAN-0004 §6.1, that 6–10 go to
ARCH-0001 through the `propose-arch` skill, and that the owner decide on 4.

The owner's instruction:

> *"decline #4 revocation. Complete the next steps as engine owner and
> propose-arch skill. Complete this under a issue that whose purpose is to take
> what openPGP does and transfer its skills into our design/wallet"*

## Context supplied

- No documents were handed over. The model read `ARCH-0001` (in full, per the
  skill), `ARCH-0003` §3.2–§3.3, §9, §10 and §12, `PLAN-0004`, `R-0002` §5.3
  and §10, `R-0007` §3.3 and §8, and `prototype/wallet/engine/{store,signer,unlock}.py`.
- RFC 9580 was fetched for section numbers (see `review.md` §3 for what was
  verified verbatim and what was not).
