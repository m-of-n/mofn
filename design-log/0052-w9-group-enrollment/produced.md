---
schema: "design-log/v1"
id: DL-0052
part: produced
date: "2026-11-17"
---

# DL-0052 — produced

| File | Change |
|---|---|
| `spec/ARCH-0001-PROPOSAL-v0.4.0.md` | **new**, `status: proposed`, `reviewed: false`. Targets ARCH-0001 v0.4.0 (MINOR) |
| `design-log/0052-w9-group-enrollment/` | this entry |
| `design-log/README.md` | row for 0052; next id 0053 |

Nothing else. `ARCH-0001`, the SPECs, `BACKLOG-0001` and the vectors are not
edited: under `propose-arch` a substantive change is a proposal file until a
human accepts it.

## What the proposal says

- **Part A, groups.** A group is a key `G` (R-M-13). A **steward** is a key `G`
  trusts about membership of `G`, with no `may-delegate`. An **enrollment** is
  the steward's `attestation` about `[1, P]` with a value of the new base kind
  `member` (value `G`). The **acceptance** is `P`'s own attestation of the same
  value. Membership needs both, valid and unrevoked (R-M-14). Stewardship gives
  the right to enroll and nothing else (R-M-15). A trust or anchor can trust
  *m* of a group's members through target type 8 `[8, G]` with `threshold`
  (R-M-16). Below *m*, the verdict names who counted, who did not, and who
  enrolled each (R-O-08). New reason code `not-a-member`. No new statement
  kind.
- **Part C, `SPEC-0004` §6.4.** Gap 1: a member counts only through its own
  statement (zero hops). Gap 2: collapse only; a successor does not stand in.
  Gap 3: `trusts: [A, A]` is rejected at V8 (N-14). Gap 4: the **set state**,
  with coverage, a co-issued edge, and no nesting. Gap 5: `attestation` only.
- **Part B, the content key `K`.** Generated with a vetted CSPRNG, wrapped to
  each member with HPKE, a new epoch on every leave (R-O-09), and never an
  input to a verdict (R-O-07). The suite key exchange it needs is left owed,
  with a preference for a separate X25519 key per persona. Part B is separable
  from A and C.
- **Acceptance tests:** G-1 to G-9, N-14, K-1, K-2 (§8), to be generated from
  the engine after acceptance.
- **Not proposed** (§6): no DEC-\*, no new kind, options B and C, steward
  thresholds, nesting, a panel form, successor stand-in, online checks, and
  cross-wallet collection.

## Choices the agent made that the human did not state

The human chose A, one steward, and the member rule. The agent then made these
choices itself, and each is **flagged for review** in `review.md`:

1. Acceptance is **required** for membership (R-M-14). Without it, leaving
   could only take effect by expiry.
2. Membership as an **attested value of a new base kind**, modelled on `name`
   (`ADR-0008`), not a new statement kind.
3. The acceptance is **the same claim made by the member about itself**, not a
   statement that targets the enrollment.
4. A **new target type 8** for a group, rather than a new field in `trust`.
5. A trust to `[8, G]` **requires** `threshold`.
6. Gap 1 made normative as **zero hops** (the narrow reading).
7. Gap 2 kept as **collapse only**.
8. A group size bound of **256**, and a **30-day** default membership validity.
