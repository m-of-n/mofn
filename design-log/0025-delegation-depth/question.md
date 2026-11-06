---
schema: "design-log/v1"
id: DL-0025
part: question
title: "Delegation in ARCH-0001: integer depth or boolean; the predicate's name (T-012c)"
date: "2026-11-06"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "1a: integer depth, SPEC-0004 kept, R-M-10 to be rewritten. 2a: `trust … about … may-delegate` is the ARCH name and `may-speak` is retired. No ADR needed, because ADR-0003 is not superseded. The text lands with T-012a (mofn#134). No DEC-* touched."
status: open
---

# DL-0025 — question

After the split of mofn#6, the agent asked the human to decide mofn#136 (T-012c).

**Q1.** ARCH-0001 R-M-10 says *"Delegation SHALL be an explicit boolean (or
equivalent)"*. SPEC-0002 §8.6 and SPEC-0004 §6.3, which govern under
`ADR-0003`, use `may-delegate { depth: uint, ranges, allow-keys, exclude-keys,
not-on-or-after }`. The options were:
- **(a)** integer depth: keep the SPEC and rewrite R-M-10;
- **(b)** boolean: supersede ADR-0003 in part and change the SPECs, TV-5 and the
  wallet.

**Q2.** Should the ARCH delegation predicate be **(a)** the SPEC's
`trust … about … may-delegate`, retiring `may-speak` (#6), or **(b)**
`may-speak` as the normative name?

Context: R-0007 §3.6, §7.3(3) and §8 P3; library `rfc-2693` distilled design
notes, items 7 and 2; SPEC-0002 §8.6; SPEC-0004 §6.3; ADR-0003.
