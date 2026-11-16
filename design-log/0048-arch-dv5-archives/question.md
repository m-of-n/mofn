---
schema: "design-log/v1"
id: DL-0048
part: question
title: "ARCH-0001 0.3.2: §2.3.2 cites DV-5 `library-review` v2 (W-2b follow-up)"
date: "2026-11-16"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "ARCH-0001 0.3.2 (PATCH); UC-0001 0.2.1. No requirement or DEC-* moves."
status: open
---

# DL-0048 — question

After mofn#172 merged, the human said "yes" to three next steps the agent had
listed. The third was: move ARCH-0001 §2.3.2 AR-1…AR-3 from DV-3 to DV-5,
using the `propose-arch` skill. DL-0046 had left this open on purpose,
because ARCH-0001 changes only by proposal (§9.4).

The agent read ARCH-0001 in full, plus its changelog, UC-0001 UC-3 and its
trace table, and `spec/vectors/ksa-core` (DV-5, TV-38…44, E-20…E-22). It
checked that no open PR touched `spec/`.
