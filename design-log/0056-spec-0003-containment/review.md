---
schema: "design-log/v1"
id: DL-0056
part: review
date: "2026-11-24"
---

# DL-0056 — review

**Human verdict:** two choices made before drafting, both the agent's
recommendation: forbid empty patterns, and aggregate and sort ip-prefix
ranges. The text itself is pending PR review.

## What was rejected, and why

- **Defining empty patterns as matching nothing** (rejected by the human).
  Two distinct empty patterns would each be within the other, so canonical
  form would have to choose between them. Forbidding them costs one length
  check.
- **Retracting "equal ranges have equal bytes" for ip-prefix** (rejected by
  the human). `delegation: 1` would then compare bytes where it means sets,
  and two verifiers would disagree on `[10.0.0.0/8]` against
  `[10.0.0.0/9, 10.128.0.0/9]`.
- **Aggregating silently on input** (rejected by the agent). That is
  normalising received input, which §6.1 already refuses ("rejected, not
  normalised") and P5.1 rejects.
- **Version 1.0.0** (rejected by the agent, and flagged for the reviewer).
  The policy reads MAJOR, because inputs that 0.2.0 accepted are now
  rejected. No published definition or vector uses these kinds, and 1.0.0
  would signal stability that a draft lacks. **The reviewer should overrule
  this if the policy is meant literally.**
- **Vectors for the new rules** (deferred, not rejected). The engine does not
  implement kinds 4, 5 and 11, so a vector would have no implementation to
  check it. This is owed when one of these kinds gets a consumer.
