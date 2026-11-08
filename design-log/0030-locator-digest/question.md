---
schema: "design-log/v1"
id: DL-0030
part: question
title: "SPEC-0002 0.6.0 — withdraw the locator target so every target binds a digest (T-048, mofn#144)"
date: "2026-11-07"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "SPEC-0002 0.6.0 (target type 5 reserved; N-11); ARCH-0001 0.2.1 (§5.5 row closed); wallet 0.2.1; DECISIONS-0001 0.6.1."
status: open
---

# DL-0030 — question

The human asked how to finish mofn#143 and mofn#144. The agent recommended doing
#144 first and resolving it by **withdrawing target type 5** from `SPEC-0002`
§7.2, so that a locator travels only as evidence. The human answered "go #144".

The issue gave three options:

1. A locator target MUST also bind a digest or description, using an
   `aliases` set.
2. The same rule, with a second target.
3. The same rule, with a body field.
4. Remove target type 5 and carry locators only as hints.

It also asked for a negative vector, in which a locator-only attestation is
rejected.

Context: `ARCH-0001` 0.2.0 R-M-07 (kept as MUST by `DL-0028`), R-M-11 and §5.5;
`SPEC-0002` 0.5.0 §7.2, §8.1, §9.2, §11.3, §12, Appendix A and B; `SPEC-0003`
§4.4 (locators for definitions are retrieval hints); `ARCH-0003` §3.7; the
`generate.py` vectors; `prototype/wallet/engine/schema.py`.
