---
schema: "design-log/v1"
id: DL-0040
part: review
date: "2026-11-13"
---

# DL-0040 — review

**The human's act: accepting `ADR-0008`.** In `DL-0039` the agent said it
would not mark `ADR-0008` accepted, and named the edit as the human's. The
human then told the agent to complete "the paperwork as you described it". The
agent read that as the decision maker accepting, and made the edit on the
human's behalf. The ADR says so. If the human did not mean to accept,
reverting `spec/ADR-0008-sdsi-names.md` to `proposed` undoes only that.
`CLAUDE.md`'s rule is about `DEC-*`, and `ADR-0008` decides none.

## What was rejected, and why

The human was offered no new forks. The agent rejected these:

- **Resolving names inside `_cover`.** That would have joined name resolution
  to coverage, which `ARCH-0001` §4.3 forbids.
- **Putting E-8…E-10 into `test_delegation.py`'s walker.** The walker is
  test-only, and T-040 asks for the engine.
- **Requiring only the successor key in the key store.** R-10 could then not
  be written.
- **Editing `PLAN-0004` §7.2.** It is a dated snapshot.

## Owed

- A second reader's review of `SPEC-0004` §5.3 (still owed from `DL-0039`).
- A review of `engine/names.py` against §5.3. T-040 is in review.
- `mofn check` with name anchors, and the `names` line showing a resolved name.
