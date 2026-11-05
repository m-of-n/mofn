---
schema: "design-log/v1"
id: DL-0021
part: produced
date: "2026-11-03"
---

# DL-0021 — produced

No primitive, vector, schema or code. Text only.

| file | version | change |
|---|---|---|
| `ARCH-0001` | 0.1.6 → 0.1.7 | `decision_makers`: Chip's authority rewritten to the October delegation; `david-hsiao` added. Changelog line |
| `DECISIONS-0001` | 0.4.2 → 0.4.3 | same entries; change note: item 4a is no longer the sponsor's alone, and stays open |
| `SPEC-0002` | 0.4.1 → 0.5.0 | same entries; §6.1: a suite is immutable once the spec leaves `0.x`, and may be revised until then |
| `SPEC-0003` | 0.1.2 → 0.1.3 | same entries only |
| `SPEC-0004` | 0.2.1 → 0.3.0 | same entries; §10.2: **yes** requires every verdict line to pass, with the reason |

The `authority` text, identical in each file but for the name:

> Delegated by the sponsor on a Zoom call in October 2026 (date not recorded):
> *name* may decide any question in this project, on the same footing as the
> sponsor, and is accountable for what they decide. Relayed by david-hsiao on
> 2026-11-03; no written confirmation from the sponsor is recorded (DL-0021).
> Supersedes the 2026-10-25 delegation and its exclusion of ADR-0002.
> Acceptance still follows ARCH-0001 §9: a DEC-* is accepted only by an ADR.

The engine needs no change: `prototype/wallet/engine/check.py` already answers
yes only when every line is `pass`.
