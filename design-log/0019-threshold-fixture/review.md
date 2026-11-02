---
schema: "design-log/v1"
id: DL-0019
part: review
date: "2026-11-01"
---

# DL-0019 — review

**Status: human review PENDING** on the PR. Nothing here accepts a decision.
`ADR-0004` is unchanged and stays `reviewed: false`.

## For the reviewer to decide

1. **`n ≠ len(members)` lands at V7 and V5, not V8** (`produced.md`). The
   request named V8 for the whole invariant; ARCH-0001 §7 now says V8 owns the
   range and the rest holds by construction. If you want V8 to own it, §8.6
   needs an `n` field, which is a signed-bytes change, and the model advises
   against one: a field that can disagree exists only to be checked.
2. **TV-13 rests on P6, which is `[draft]`.** `ADR-0002` is not accepted, and
   `ARCH-0001` R-M-04 still says name bindings are a distinct object kind
   (register item 6a). If P6 falls, TV-13 stays a valid attestation but stops
   being a `NameCert`, and the acceptance test reopens.
3. **Whether option-2 is really not owed.** `PLAN-0002` line 255 and `PLAN-0001`
   I2 still promise comparison fixtures, and T-032 is still `todo`. Left alone
   as outside this change; they want a sponsor's line.

## Found, not fixed

**`trusts` has no distinctness rule, and that reaches the invariant.** A scratch
statement with `trusts: [A, A]`, `threshold: 2`, signed by Carol, is **verified**
by the wallet: `k ≤ n` holds on length while `SPEC-0004` §6.4 counts distinct
kids, so the real `n` is 1. It fails closed (never satisfiable), so nothing is
over-trusted, but V8's check does not mean what ARCH-0001 means. R-0006 §3.13
already records the missing rule alongside the order. Owed to `SPEC-0002` with
condition (5), out of scope here. **No vector pins it**: a positive would bless
it, and a negative would assert a rule no document states.

`Threshold.members` is `[Principal, ...]` in ARCH-0001 §4.1 but `[2* kid]` in
§8.6: no names, no nesting. PLAN-0001 risk 7 expected that; SPKI fidelity under
thresholds is narrower than the logical type says.

## Rejected by the model

| considered | rejected because |
|---|---|
| **N-9 expecting V8**, by teaching the wallet an `n` field | invents a field on the wire to make a test match its sentence |
| **Only one spelling of `n ≠ len(members)`** | N-9 alone suggests a closed map is what saves us; N-10 shows `n` is the array head |
| **A single 2-of-3 positive** | cannot catch an off-by-one at either bound |
| **Sorting `trusts` by rule in SPEC-0002** | condition (5), out of scope. The generator lists kids bytewise so the vectors survive that rule, and says it is not required yet |
| **Adding "distinct" to §8.6** | normative, owed with (5) |
| **Editing `ADR-0004`'s "Met" list for `NameCert`** | accepted; changes only by superseding. §7 and this entry carry it |
| **Adding the name type to DV-1** | changes DV-1's id and so every existing vector |
| **Counting TV-2 as the `NameCert`** | §8.3 says `label` is not a binding |
| **Building the option-2 fixture anyway** | evidence for a closed decision, and it would lean on open DEC-005 |
| **Using `n` for the threshold, as §8.6 and SPEC-0004 §6.4 do** | clashes with ARCH-0001's `k`/`n`; the vectors use ARCH's letters and the README says so. Renaming in SPEC-0004 is out of scope |
| **Superseding ADR-0004** | no defect in option 5 |
| **Taking `0018`** | held by open mofn#118 (`0018-delegation-models`) |

## Where the model nearly went wrong

`test_negative_rejected_at_step` iterates a hand-kept dict, not the vectors. New
negatives would have left the suite green and untested, reading as coverage.
`test_every_negative_vector_has_an_expected_step` now fails if one is missed.

## Next

A second reader reviews this PR under `CONTRIBUTING.md`; merging it closes #8.
The distinctness rule goes with condition (5) to `SPEC-0002`.
