---
schema: "design-log/v1"
id: DL-0028
part: question
title: "ARCH-0001 v0.2.0 — fold the proposal in, rewrite §4.2, reconcile with the SPECs; DEC-007"
date: "2026-11-07"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "ARCH-0001 0.2.0; ADR-0007 (DEC-007 option 2) accepted; proposal superseded; DECISIONS-0001 0.6.0 (items 4, 5d, 6 closed); mofn#143 and mofn#144 filed for gaps owed by the SPECs."
status: open
---

# DL-0028 — question

The human said "continue" after #129 merged; the next step was T-012a (mofn#134). The
agent read ARCH-0001 0.1.9, the v0.2.0 proposal, SPEC-0002/0003/0004 and
ADR-0003. Before drafting, it asked four questions:

1. **SDSI names.** ARCH §1, G1, R-M-03 and §4.3 step 1 require compound names.
   The SPECs have none. ADR-0003 says the SPEC governs; the propose-arch skill
   says §4.3 governs. Which wins?
2. **R-M-07 vs SPEC-0002 §7.2.** A locator-only target binds no digest.
   Keep the MUST and fix the SPEC, or loosen R-M-07?
3. **DEC-007.** SPEC-0003 already implements option 2. File it open, or close
   it now by ADR?
4. **Which proposal parts to adopt:** R-M-11, R-O-05, R-O-06, citations and
   DEC-006.

Context: ARCH-0001 at `e89a70c`; ARCH-0001-PROPOSAL-v0.2.0 proposed.6;
SPEC-0002 §7–§8; SPEC-0003 §1, §10; SPEC-0004 §6, §10.4; ADR-0003; wallet
`render.py` and `test_engine.py`.
