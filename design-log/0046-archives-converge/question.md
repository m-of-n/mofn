---
schema: "design-log/v1"
id: DL-0046
part: question
title: "W-2b: one archives vocabulary — DV-5 `library-review` v2, and the demo moves to it with a delegation path"
date: "2026-11-15"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "SPEC-0002 0.10.0 (DV-5, TV-38…44, E-20…22); `domains/archives/` copies DV-5; APP-0003 0.2.0; APP-0004 0.1.1; BACKLOG-0001 0.14.1. No engine change. No ADR: no rule changed."
status: open
---

# DL-0046 — question

The human asked what the second deliverable domain is, then asked the agent
to "complete next steps archives domain file".

The agent found that the archives domain file v0 had already landed (W-2,
mofn#66 closed; `prototype/wallet/domains/archives/`, DL-0033), on an
`origin/main` that the local checkout had not fetched. What was left was
BACKLOG W-2b. DL-0033 had decided on 2026-11-09 to converge DV-3 `library-review`
v1 (the vector) and `archives` v1 (the demo) once W-3 merged. W-3 was mofn#168,
approved with green checks but not merged.

The agent asked two questions, and the human answered both:

1. **Merge #168 now?** Yes. The agent merged it (`dae3cfd`) and branched from
   it.
2. **Which values does the one vocabulary keep?** The agent offered DV-3's
   `yes · partial · no` with a separate `summarized` type (DL-0033's example),
   the demo's `reviewed · summarized · unverified`, or DV-3's values alone. The
   human chose **the demo's values**.

The agent read `spec/vectors/ksa-core/generate.py`, `vectors/README.md`,
SPEC-0002 Appendix A, ARCH-0001 §2.3.2, APP-0003, APP-0004,
`domains/archives/`, `tests/test_archives.py`, `tests/test_delegation.py`,
`fixtures/sync.py`, `cli.py` (`delegate`, `root add --depth`) and
`demo/slice.sh` ④–⑥.
