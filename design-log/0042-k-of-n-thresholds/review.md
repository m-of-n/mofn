---
schema: "design-log/v1"
id: DL-0042
part: review
date: "2026-11-14"
---

# DL-0042 — review

**No human has reviewed this yet.** The brief accepted the outcome in advance
("built, not deferred"). It did not accept any reading of §6.4. Every gap
below is flagged for the human, and none is decided.

## Gaps in SPEC-0004 §6.4: the reading taken, flagged

1. **"Each reached as the start of a sub-path with that scope."** This could
   mean either:
   - (a) the member's own attestation, so the sub-path has zero hops; or
   - (b) a path that starts at the member and may continue by delegation.

   If (b), it is not stated whose `may-delegate` governs the sub-path. It
   could be the threshold anchor's, or nothing, since §6.2 defines start
   state only for "an anchor trusting key `A` (not a threshold set)".
   **Taken: (a)**, the narrowest. The threshold anchor's `may-delegate` is not
   followed. This matches the one-hop engine, and W-3 can widen it once §6.4
   says what governs a member's sub-path. Owed: a `SPEC-0004` clarification.
2. **Rotation.** §6.4 says "keys that a rotation links count as one member".
   §7.2 says "trust follows the key", so a member's successor may stand in
   for it. **Taken:** collapsing only. Two linked members count once.
   A successor that is *not* listed does not count for its predecessor,
   because the engine does not apply §7.2 to one-key anchors either. E-18 and
   E-19 hold under both readings. A vector in which bob2 alone stands in for a
   listed Bob would separate them, and none is written. Owed: apply §7.2 to
   coverage as a whole, not only to thresholds.
3. **`trusts: [A, A]`.** `SPEC-0002` has no distinctness rule (`ARCH-0001` §7,
   still owed). §6.4 counts by kid, so the engine treats `[A, A]` as one
   member, and 2 of it can never be met. That is tested, not added as a
   vector: if `SPEC-0002` later rejects it at V8, a vector would have to be
   withdrawn.
4. **Threshold trust statements as hops,** and "delegation onward from a
   threshold set" (§6.4, second sentence). Neither is implemented: the engine
   has no delegation. They belong to W-3, or to a task after it.
5. **Which attestation kinds count.** §10.2 item 1 allows "the corresponding
   kind" for reviews and approvals, and SC-3 (`ARCH-0001` §2.3) is a review
   panel. Only `attestation` counts here, as for one-key anchors. SC-3 stays
   illustrative, because `SPEC-0005` panels have no vectors.

## What was rejected, and why

The agent rejected these:

- **Expanding a threshold anchor into *n* one-key anchors**, the way name
  anchors are expanded. That would make each member alone sufficient, which
  is 1-of-*n*.
- **Requiring the same *k* members across every attribute of the ask.** §10.2
  is per attribute, and §6.4 counts per covered statement. The stricter rule
  has no text behind it.
- **Counting statements instead of keys.** One member with two attestations
  would then meet 2-of-*n*. §11.5 is the reason this is wrong.
- **Allowing a counted member to vouch through `may-delegate`.** This is
  gap 1. It was deferred, not decided.
- **Using `rotated-out` for the collapsed member.** That code has another
  meaning in §14.2.
- **Rewriting the PLAN-0004 §7.2 row.** It is a dated snapshot (`DL-0040` gave
  the same reason). A dated note was added under decision 3 instead.
- **Editing PLAN-0001 §12 risk 7.** The parent thread does that.

## Owed

- A human review of gaps 1 and 2, and a `SPEC-0004` clarification of §6.4 for
  each.
- A code review of `_threshold` against §6.4. T-043 is in review.
- Threshold hops and delegation from a threshold set, after W-3 (#67).
- `mofn check` and stored anchors in the threshold form. Like name anchors
  (T-040), the store and CLI take kids only.

## Rebase onto #168 and #172, 2026-11-16

`main` gained W-3 (#168, delegation paths, wallet 0.7.0) and W-2b (#172,
SPEC-0002 0.10.0, TV-38…44) after this was written. Rebased, not merged.

- **`_threshold` called the old `_cover(…, anchors, …)`.** #168 changed it to
  `_cover(…, reached, broken, …)`, fed by `_walk`. No textual conflict, so a
  silent wrong-arity call. Fixed by walking the one-key anchor to each member
  with no trust statements: `_walk([alone], [], …)`. That reaches the member
  exactly as a one-key anchor would (anchor expiry included) and follows no
  hop, so members still attest directly. **Rejected: building the `Reach` by
  hand** — it would copy `_walk`'s anchor handling and drift from it.
  **Rejected: walking the handed trust statements from each member** — that
  is a member counting through delegates, which §6.4 leaves open (above).
- **"Waits on W-3" is stale.** W-3 has landed; threshold hops and a threshold
  anchor's `may-delegate` are now **T-095**, a separate task. **Rejected:
  doing them here** — it needs §6.4's open questions answered, and it would
  turn a reviewed PR into a new one.
- **Versions moved:** wallet 0.7.0 → **0.8.0** (MINOR, #168 took 0.7.0),
  SPEC-0002 → **0.10.1**, BACKLOG → **0.14.2**. TV-36, TV-37, E-11…E-19 and
  DL-0042 were still free; nothing renumbered.
- **Vectors regenerated**, not hand-merged; every existing vector is
  byte-identical. SPEC-0002 Appendix A re-spliced from `vectors.md`.
- 460 wallet tests pass.
