---
schema: "design-log/v1"
id: DL-0041
part: review
date: "2026-11-14"
---

# DL-0041 — review

**Pending.** No human has reviewed the code yet. The PR is the review
request; this file records what was rejected while building it.

## What was rejected, and why

- **A revocation list for delegations.** #67 says short expiry is the
  mechanism; a list would add a second one. `mofn delegate` takes
  `--valid-days` and refuses 0.
- **Clipping a widening hop to what remains** (e.g. depth 1 → 0). E-4 and
  R-M-10 forbid it: clipping would have answered **yes**. A hop is followed
  whole or not at all.
- **`delegation: 1` as set equality.** It would accept a permuted range and
  hide the canonical-encoding requirement. Bytes equality is the floor
  `R-0006` §4.7 describes, and it fails closed.
- **An `ARCH-0001`-style opaque `AuthzCert` tag for T-042.** The core carries
  no such tag; building one would have been a parallel model and a step
  toward picking a DEC-004 option.
- **`mofn make --type <k>:may-speak`** (#67's wording). `may-speak` was
  retired by DL-0025 (`trust … about`). The command is `mofn delegate`, which
  signs a `trust` statement.
- **Folding paths into `_cover`.** Kept as `_walk`/`_follow` so the sibling
  T-043 change to the same file can land beside it.
- **Dated broken-link sentences.** They would make the demo golden change
  every day.
- **Editing `PLAN-0001` §12** (risks 6 and 11). The parent thread does that
  after all risks land.

## Owed

- A human code review of `reduce.py` §6 functions against `SPEC-0004` §6.3.
- A ruling on the `delegation: 1` vs `deleg.ranges` reading (produced.md).
- `PLAN-0004` §7 status rows, `APP-0001` and `PLAN-0002`'s `may-speak` text
  are dated or outside this change and left as they are.
