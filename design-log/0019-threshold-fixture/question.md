---
schema: "design-log/v1"
id: DL-0019
part: question
title: "T-031 — the threshold fixture DEC-002's acceptance test names, and what else the row still owes"
date: "2026-11-01"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "No ADR. Vectors TV-9…13, N-7…10, DV-2; SPEC-0002 v0.3.0; ARCH-0001 v0.1.6; BACKLOG-0001 v0.12.4. ADR-0004 unchanged; no DEC-* touched."
status: open
---

# DL-0019 — question

## The question asked

Complete mofn#8. DEC-002 is already accepted (`ADR-0004`) and is not to be
re-decided; #8 stays open because no vector exercises `trust`'s threshold form.
Add positive and negative threshold cases (`k = 0`, `k > n`, `n ≠ len(members)`)
through `generate.py`, name `SPEC-0002` V8 as the owner, and read the whole
T-031 row: decide whether its option-2 comparison and `NameCert` are still owed,
and do them or say here why not.

**Stop condition:** a defect in option 5 itself is reported with bytes and the
failing step, #8 stays open, and no superseding ADR is written.

**Out of scope:** conditions (5) and (6); `demo/`, `SPEC-0003`, `SPEC-0004`
(mofn#65's thread).

## Context the model assembled

- `ADR-0004` "Acceptance test — what is met, and what is owed".
- `ARCH-0001` §4.1 (`Threshold`) and §7 (the 0.1.3 input on the invariant).
- `SPEC-0002` §7.1, §8.3, §8.6, §9.2, Appendix B; `SPEC-0004` §6.4 (read only).
- `ARCH-0002` P6; `research/0006-mechanism/report.md` §3.12–§3.13, §5.1.
- `prototype/wallet`: the verifier, `tests/test_vectors.py`, `fixtures/sync.py`.
- Baseline before any edit: `generate.py` reproduced the committed bytes, and
  198 wallet tests passed.
