---
schema: "design-log/v1"
id: DL-0033
part: question
title: "W-2 (mofn#66): two scenarios, the archives domain through the same engine, --lang, the five views"
date: "2026-11-09"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "APP-0002, APP-0003, APP-0004 0.1.0; PLAN-0002 0.4.0 §2.2, §6.5; wallet 0.4.0 (--lang); prototype/wallet/domains/archives/."
status: open
---

# DL-0033 — question

The human asked what mofn#66 needed in order to close. The agent read the
issue, PLAN-0004 §3, §5 and §7, and the wallet engine, and answered with four
items. One of them was a decision: is `--lang` engine work, given the
acceptance test of "zero engine code changes"?

The human then said, in three messages:

1. "Write the two scenario pages. And I am deciding that Lang should count
   as allowed engine work (this means the engine creates a flag which allows
   the user to change which language it wants to use)."
2. "Then complete the code on request where you add an archives definition."
3. "Then complete the five sketches once the scenarios are done, then update
   plan 0002."

Context the agent had: mofn#66's body and comments (the owner is Paul,
@nymble), PLAN-0004, PLAN-0002 §2 and §6.5, the wallet README and engine at
0.2.1, the ksa-core vector generator, and DL-0031.

**Who decided `--lang`:** ndewedo-newbury, in this session. The issue is
assigned to @nymble, so the owner has not yet confirmed it.
