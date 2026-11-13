---
schema: "design-log/v1"
id: DL-0039
part: question
title: "SDSI names in the SPECs — a name target, a naming base kind, and resolution (T-040s, mofn#143)"
date: "2026-11-12"
model: "claude-opus-5-5"
human: ndewedo-newbury
outcome: "SPEC-0002 0.9.0, SPEC-0003 0.2.0, SPEC-0004 0.6.0; ADR-0008 (proposed); ARCH-0001 0.3.1 (§5.5 row closed); wallet 0.5.0; BACKLOG-0001 0.13.2."
status: open
---

# DL-0039 — question

The human asked to work through what mofn#143 requires. The issue owes four
things:

1. a `Name` form, an issuer kid plus a label chain, "a target type, a principal
   in `trust.trusts`, or both";
2. a resolution procedure in `SPEC-0004`, kept apart from delegation paths
   (`ARCH-0001` §4.3);
3. name statements as attestations under a names definition (`ARCH-0002` P6,
   TV-13, DV-2);
4. vectors: one hop, a compound chain, and failures (missing link, cycle,
   widening).

`DL-0028` had already decided that names stay in `ARCH-0001` and that the SPEC
owes them. Whether to have names was not reopened.

The agent read `ARCH-0001` §3.1, §4.1–§4.3, §5.5; `ARCH-0002` P1, P2, P6;
`SPEC-0001` §7.3; `SPEC-0002` §7–§12 and Appendices A and B; `SPEC-0003` §5–§6
and §12; `SPEC-0004` in full; `DL-0028` and `DL-0030`; `generate.py`; and
`prototype/wallet/engine/schema.py`. It then put the design forks to the human
in two rounds, with a recommendation on each.

**Round 1.**

| fork | options offered (recommendation first) | answer |
|---|---|---|
| where the name lives on the wire | target type 7, usable in `trust` and `attestation` · trust subject only · no wire form | type 7 |
| how resolution knows a binding | new base kind `name` · per-context list of name types · DV-2's `name` only | base kind |
| whether a binding needs an anchor path | no (SDSI) · yes, covered like any claim | no |
| one label bound to two keys | a set (SDSI group) · `name-ambiguous` failure | set |

**Round 2.**

| fork | options offered (recommendation first) | answer |
|---|---|---|
| what the issue's "widening" vector tests | foreign-namespace binding · `widening` on a trust to a name · drop it | foreign |
| whether a name follows rotation | follows, like trust · fixed to the old key | follows |
| PR scope | spec and vectors in one PR · text first, vectors after | one PR |

The human took every recommendation and gave no reasons of their own.
