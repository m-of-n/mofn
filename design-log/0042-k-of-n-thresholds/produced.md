---
schema: "design-log/v1"
id: DL-0042
part: produced
date: "2026-11-14"
---

# DL-0042 — produced

No primitive. TV-36 and TV-37 are signed with `cryptography` through the
existing `generate.py`.

| file | change |
|---|---|
| `prototype/wallet/engine/reduce.py` | `Threshold(keys, k)` is a value of `Anchor.trusts` (`SPEC-0004` §4.2). New functions `_thresholds` and `_threshold`. They run only when no one-key anchor covered the attribute. Each member is checked by calling the existing `_cover` with a one-key copy of the anchor (`trusts = member`, same `about`), so a member's attestation passes exactly the checks a one-key anchor applies. `Member`, `ThresholdCovered` and `ThresholdStopped` (`threshold-not-met`) carry every member, whether it counted, and why. `evaluate` gains five lines; `_cover` is unchanged |
| `prototype/wallet/engine/check.py` | `because` lists the threshold, `k`, `n` and every member with its statement and reason; the authorization line names who counted and who did not |
| `prototype/wallet/tests/test_thresholds.py` | **new**. E-11…E-19 from `vectors.json`, plus: why each member did not count, an expired member statement, rotation, `[A, A]`, scope, context, one-key anchors first, the verdict line and the JSON |
| `spec/vectors/ksa-core/generate.py`, `vectors.json`, `vectors.md`, `README.md` | TV-36 (Carol, any 2 of {Bob, bob2, Dave}), TV-37 (bob2 attests `reproducible`), `threshold_evaluations` E-11…E-19. Existing vectors are byte-identical: the `vectors.json` diff has no removed line |
| `spec/SPEC-0002-ksa-core.md` 0.10.0 → **0.10.1** | Appendix A gains TV-36 and TV-37. PATCH |
| `spec/SPEC-0004-ksa-trust-evaluation.md` 0.6.1 → **0.6.2** | Appendix A gains asks 10–18, and says which reading of §6.4 they rest on and what §6.4 leaves open. PATCH: no rule changes |
| `project/BACKLOG-0001.md` 0.14.2 | T-043 → review, with what is not yet done and what is open |
| `project/PLAN-0004-application-plan.md` 0.4.2 | §7.2 decision 3 gains a dated note. The Nov 12 table is not rewritten |
| `prototype/wallet` 0.7.0 → **0.8.0** | changelog |

## The semantics implemented

§6.4: "A statement is covered through the threshold when `n` distinct members
of `M`, each reached as the start of a sub-path with that scope, have each made
a statement that covers the ask with the same target, type and value."

For each attribute `(T, v)` of the ask, and each threshold anchor in the
context:

1. The members are the distinct kids in `trusts`. A kid listed twice is one
   member (§6.4, "distinctness is by kid").
2. A member **counts** if some attestation by it has `this` equal to the
   subject and assigns `v` to `T`, and `_cover` would cover it under a one-key
   anchor to that member with the threshold's `about`. That covers key in
   store, valid at the time, types, template, attributed definition, and
   `v` in range.
3. Two members that a rotation links (§7.2, via `names.Resolver.successor`)
   count once. The later one is reported with `same_as`.
4. The anchor is met when at least `k` members count. The first anchor met
   covers the attribute; otherwise each unmet anchor gives a
   `threshold-not-met`, placed before the one-key reasons.

## Design notes the human did not see as options

- **One-key anchors first.** A context holding both kinds answers as before
  when a one-key anchor covers. Thresholds are tried only on the `else`
  branch, so no existing answer changes.
- **Reuse `_cover` instead of factoring out its checks.** Refactoring `_cover`
  would be cleaner, but the W-3 lane is editing it. Calling it with a one-key
  copy of the anchor gives the same checks with no diff to `_cover`.
- **`threshold-not-met` is reported before the one-key reasons.** Otherwise a
  context with only a threshold anchor would lead with "no anchor in this
  context trusts the speaker", which is true but answers nothing.
- **A rotation-linked duplicate is given no reason code.** `rotated-out` means
  something else in §14.2 (the old key after its link), and no code fits, so
  the member carries a detail and `same_as` and no code.
