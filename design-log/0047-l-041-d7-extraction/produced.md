---
schema: "design-log/v1"
id: DL-0047
part: produced
date: "2026-11-14"
---

# DL-0047 — produced

| where | change |
|---|---|
| library#136 | Opened: FX-1 extraction of `in-toto-envelope-v1`, `slsa-provenance-1-2` and `slsa-vsa-1-2`, ranked by the mofn task that blocks on each (envelope first). One PR per record. `slsa-1-2` and `in-toto-attestation-v1` are explicitly out of scope. |
| `project/BACKLOG-0001.md` 0.13.3 → **0.14.0** | L-041 added. T-051 now names L-041 and library#134 as its inputs, T-052 names L-041 and flags the 1.1/1.2 version mismatch, and T-053 names `slsa-vsa-1-2` as an input. |
| `design-log/README.md` | This entry's row. |

MINOR bump, because a row was added. Nothing in `spec/` changes.
