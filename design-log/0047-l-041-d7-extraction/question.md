---
schema: "design-log/v1"
id: DL-0047
part: question
title: "L-041 — FX-1 extraction the I4 mappings depend on, opened ahead of the milestone"
date: "2026-11-14"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "BACKLOG-0001 0.14.0: L-041 added (library#136); T-051, T-052, T-053 point at it. No spec change, no DEC-* touched."
status: open
---

# DL-0047 — question

The human asked whether `L-` meant extraction. The agent answered that `L-`
marks the library build-out section of `BACKLOG-0001`, and that only
L-030…L-038 are FX-1 extraction.

The human then asked: *"any other extraction work mentioned, i want to get
ahead of the milestones"*. The agent read `PLAN-0003` (I4 = Nov 12–25, D7
mappings), the I4 rows of `BACKLOG-0001` (T-050…T-053) and the library
records on `m-of-n/library` main. It found that three records that T-051,
T-052 and T-053 cite normatively are at `status: summarized` and are covered
by no extraction issue: `in-toto-envelope-v1`, `slsa-provenance-1-2` and
`slsa-vsa-1-2`. `in-toto-attestation-v1` is already covered (library#89,
PR #134), and `slsa-1-2` is already distilled. It proposed opening a library
issue and adding a backlog row.

The human directed: *"complete next steps 1"*. That meant opening the issue,
adding L-041 and writing this entry.

Context: `PLAN-0003` §I4; `BACKLOG-0001` 0.13.3 T-051…T-053 and L-037; library
`docs/extraction.md`; library#89, #134, #135; the record files for the three
records on library main.
