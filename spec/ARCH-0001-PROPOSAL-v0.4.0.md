---
schema: "archdoc/v1"
id: ARCH-0001-PROPOSAL-v0.4.0
title: "Proposed ARCH-0001 v0.4.0: groups with a steward, enrollment by consent, group thresholds, and SPEC-0004 §6.4's open questions answered"
short_title: "ARCH-0001 v0.4.0 proposal (groups)"
description: "Proposal for the next MINOR version of ARCH-0001. It gives the Group principal (§4.1, §5.5) a form: a group is a key, a steward enrolls members, each member accepts, and a trust or anchor can trust m of a group's members. It answers the five SPEC-0004 §6.4 gaps that DL-0042 flagged. proposed.2 records the first review round (2026-11-26): a group is a field of the threshold form, not a target type, and the group content key is deferred. Open for review; nothing accepted."
type: proposal
category: security
status: proposed
version: "0.4.0-proposed.2"
version_policy: "target is a MINOR bump of ARCH-0001 (additive requirements); this proposal's own revisions are tracked in §11."
date: "2026-11-17"
updated: "2026-11-26"
authors:
  - role: proposer
    id: conversation-claude-opus-5-5
decision_makers: []
reviewers: [ndewedo-newbury]
needs_review: true
reviewed: false
iteration_of: ARCH-0001
supersedes: []
superseded_by: null
canonical_path: spec/ARCH-0001-PROPOSAL-v0.4.0.md
target: spec/ARCH-0001-authorization-attestation.md
tags:
  - proposal
  - group
  - threshold
  - enrollment
proposes:
  new_decisions: []
  withdrawn_decisions: []
  amended_decisions: []
  new_requirements: [R-M-13, R-M-14, R-M-15, R-M-16, R-O-07, R-O-08]
  model_changes:
    - "§4.1 Principal: Group gets a form (a group key; members derived at evaluation time)"
    - "§4.1 Threshold: members may be a Group, so n is the group's size at the evaluation time"
    - "§5.5: the Group row closes, owed by SPEC-0002, SPEC-0003, SPEC-0004"
  spec_changes_owed:
    - "SPEC-0002: §8.6 threshold form gains group (in place of trusts); V8 rejects a repeated kid in trusts (N-14) and a trust carrying both trusts and group (N-15)"
    - "SPEC-0003: base kind member (§6.5)"
    - "SPEC-0004: §5.4 group membership; §6.2 and §6.4 set state, threshold hop, co-issued edge; §6.4 gaps 1-5; reason code not-a-member"
agent_checkpoint: false
agent_notes: >
  PROPOSAL against ARCH-0001 v0.3.4 (drafted against v0.3.2), per its §9.4. Nothing accepted, no DEC-*
  touched, no ADR written. Drafted for W-9 (mofn#181) under the human's
  choices of 2026-11-17 (DL-0053): the group key gives access, not authority
  (option A); one steward for now; stewardship never gives a vote. If
  adopted: a human instructs an ADR, the agent folds §4 to §6 into ARCH-0001
  v0.4.0 with a changelog line, the SPEC changes in §7 land with their
  vectors, and this file is marked superseded. proposed.2 applies the first
  review round (2026-11-26, DL-0053 review.md): no target type 8, the group
  is a field of the threshold form; Part B (the content key) deferred to its
  own issue, with R-O-09.
---

# Proposed ARCH-0001 v0.4.0: groups

A proposal against `ARCH-0001` v0.3.4 (first drafted against v0.3.2), offered under its §9.4: *"propose a diff
against this file."* Every change is additive, so the target is **v0.4.0**
under the stated policy (MINOR: additive requirements). No open decision is
opened, closed or ranked.

**Reviewers short on time:** read §2 (the model in one page), §6 (what is
**not** proposed) and §8 (the acceptance tests).

**Review status (proposed.2, 2026-11-26).** The reviewer (the owner of
mofn#181) went through the eight choices the agent made itself (`DL-0053`
`produced.md`). The outcome, with what was rejected, is in `DL-0053`
`review.md`. In short:

| # | Choice | Reviewer |
|---|---|---|
| 1 | acceptance is required for membership (R-M-14) | agreed |
| 2 | membership is a value of base kind `member` (§4.2) | agreed; no order between enrollment and acceptance is enforced |
| 3 | the acceptance is the member's own matching claim, not a statement about the enrollment | agreed |
| 4 | a new target type 8 for a group | **rejected**: a group is a `group` field of the threshold form (§4.4) |
| 5 | a trust to a group requires `threshold` | follows from 4: the count is part of the form |
| 6 | §6.4 gap 1: zero hops | agreed |
| 7 | §6.4 gap 2: collapse only | agreed |
| 8 | a bound of 256 members; 30-day default membership validity | agreed |
| — | Part B, the group content key | **deferred** to mofn#197 (§7) |

The proposal as a whole is **not yet accepted**: `status: proposed`,
`reviewed: false`. Part C gaps 3 to 5 and the set state (gap 4) have not had a
second reader.

---

## 1. What prompted this

`ARCH-0001` §4.1 lists `Group` as a `Principal` and §5.5 records it as a gap:
*"`Group` principal — no form — open; no consumer yet"*. W-9 (mofn#181) is the
consumer. It asks for an **enrollment protocol** for delegation groups: a
persona joins a group, and the group delegates as an *m*-of-*n* threshold. The
issue names what enrollment must settle (*who invites, what the member signs,
what the group's statement says, how a member leaves, expiry*), and it
requires that this be in the specification **before** any code.

It also depends on five gaps in `SPEC-0004` §6.4 that `DL-0042` flagged and
left open. T-095 (threshold hops) waits on them. §5 answers them.

The human set three constraints, recorded in `DL-0053`:

1. **The group key gives access, not authority** (option A). Members receive a
   group *content* key for confidentiality. Every member's say in an
   *m*-of-*n* decision still comes from that member's own signature.
2. **One steward for now.** A trusted persona, appointed by the group, invites
   other personas.
3. **Stewardship never gives a vote.** A steward may be a member, but only by
   enrolling itself like anyone else, and the verdict shows that it did.

---

## 2. The model in one page

| Role | Who | Holds | Signs |
|---|---|---|---|
| **Group** | a key `G`, an owned persona of whoever founds the group (`ARCH-0003`, W-8) | `G`'s private key, never shared | the steward appointment |
| **Steward** | a key `S` that `G` trusts about membership of `G` | its own key (a group content key is Part B, deferred) | enrollments |
| **Member** | a key `P` that is enrolled **and** has accepted | its own key | its acceptance; its own statements and delegations |
| **Relying party** | anyone | an anchor that trusts *m* of `G`'s members | nothing |

```
G ──trust about member∈{G}──▶ S            steward appointment (one hop, no may-delegate)
S ──attest [1,P] member = G──▶ P           enrollment: "P is a member of G"
P ──attest [1,P] member = G──▶ P           acceptance: P says the same of itself
R's anchor: trusts { group: G, threshold: m } about X
   P1, P2 … each attest the subject has X  →  covered when m distinct members did
   P1, P2 … each trust K′ identically      →  one edge to K′ ("the group delegates")
```

Enrollment and acceptance may be signed in either order. Membership starts
when both exist and are valid; no order is checked.

**Membership is derived, not listed.** No statement lists the members. A key
`P` is a member of `G` at time `t` when an enrollment by `G` or by a steward of
`G`, and `P`'s own acceptance, are both valid at `t` and neither is revoked.
This is the same shape as `SPEC-0005` §4.2's delegated panel (`[2, D]`), and as
`SPEC-0004` §5.3's name bindings: a fact about the statement set, not about the
relying party's anchors. Whether the relying party cares about `G` at all is
trust evaluation, through its anchor.

**Leaving is immediate where revocations are held.** A member leaves by
revoking its acceptance. A steward removes a member by revoking the
enrollment. Either ends membership at the revocation's `not-before`
(`SPEC-0004` §7.1). Short validity windows stay the backstop (R-O-02).

**A group content key, if one is added, is outside the trust model.** Part B
(§7, deferred) would let members read what is shared with the group. It would
never be an input to a verdict (R-O-07, `ARCH-0003` W-19).

---

## 3. Proposed requirements

Each extends or conflicts with an existing requirement as stated.

| ID | Pri | Requirement | Relation |
|----|-----|-------------|----------|
| R-M-13 | M | A **group** SHALL be identified by a key. Its members at an evaluation time SHALL be derived from signed statements valid at that time, and SHALL NOT be a list carried in any one statement. | Gives §4.1 `Group` a form; closes the §5.5 row. Extends R-M-02 and R-M-06 |
| R-M-14 | M | A key SHALL be a member of a group only while **both** (a) an enrollment of it by the group key, or by a key the group key trusts about that group's membership, and (b) its own acceptance are valid and unrevoked. Revoking or letting either expire SHALL end membership. | New. Membership by consent: no key is counted for a group it did not join |
| R-M-15 | M | Trust about a group's membership (stewardship) SHALL confer the right to enroll and nothing else. A steward SHALL count toward a threshold only as a member, under R-M-14. | New. Constrains R-M-14 (a) |
| R-M-16 | S | A trust statement or anchor SHALL be able to trust *m* of a group's members about a scope. Members SHALL be counted as `SPEC-0004` §6.4 counts threshold members: distinct by `kid`, rotation-linked keys once. | Extends R-M-06. Amends §4.1 `Threshold`: `n` is the group's size at the evaluation time, not a field |
| R-O-07 | M | Possession of a group content key SHALL confer no authority and SHALL NOT be an input to any verdict. | Extends `ARCH-0003` W-19 and R-O-06 |
| R-O-08 | S | Where a threshold is not met, the verdict SHALL name the members that counted, the members that did not, and, for a group, who enrolled each. | Extends R-O-06. `SPEC-0004` §10.4 authorization line |

**Acceptance test for R-M-13 to R-M-16 and R-O-08:** §8, vectors G-1 to G-9,
each giving one `SPEC-0004` §10.4 verdict that two implementations (`mofn check`
and the W-7 app) reproduce exactly. **For R-O-07:** G-1 to G-9 are evaluated
with no content key present, and give the verdicts in §8; the Part B issue adds
a test that holding a content key changes no verdict.

R-O-09 of proposed.1 (re-keying on departure) moves with Part B to its own
issue and is not proposed here.

---

## 4. Part A: groups, enrollment and group thresholds

### 4.1 Model changes (diff against `ARCH-0001` §4.1)

| Type | Now | Proposed |
|---|---|---|
| `Principal` | `` `Key` \| `KeyId` \| `Name` \| `Threshold` \| `Group` `` — **`Group` has no KSA form yet** (§5.5) | unchanged list. KSA form of `Group`: the `group` field of the threshold form of `trust` (`SPEC-0002` §8.6) and of a threshold anchor (`SPEC-0004` §4.2), holding the group key's `kid`. **No new target type** |
| `Group` | (not a row) | `{ key: KeyId }`. Its members at time `t` are derived by `SPEC-0004` §5.4 (proposed). No statement lists them |
| `Threshold` | `{ k, n, members: [Principal, ...] }`, `1 ≤ k ≤ n`, `n = len(members)` | `members` is a list of kids **or** one `Group`. For a group, `n` is the number of members at the evaluation time, and `k > n` is a failure at evaluation (`threshold-not-met`), not a decoding error |

### 4.2 Statements: no new kind

Everything below is an existing statement kind (`SPEC-0002` §8). Membership is
an **attested value**, as a name is an attested string (`ARCH-0002` P6,
`ADR-0008`).

- **Base kind `member`** (`SPEC-0003` §6.5, proposed). The value of a type of
  base kind `member` is a `kid`: *the target is a member of that key's group*.
  What makes a membership claim is the base kind, not who defined the type, as
  for base kind `name` (`SPEC-0003` §6.4). Every key may define its own
  membership type (`ARCH-0002` P1). The engine recognises the base kind and
  needs no group-specific code.
- **Steward appointment:** a `trust` by `G` with `this = [1, S]` and `about` a
  range of a `member` type whose value range is exactly `{G}`. `may-delegate` is
  absent, so a steward cannot appoint stewards. `G` itself may enroll without
  an appointment.
- **Enrollment (the invitation):** an `attestation` by `S` (or `G`) with
  `this = [1, P]` and an attribute of base kind `member`, value `G`. It is
  delivered to `P` out of band (file, QR, the mailbox in `SPEC-0001` §8.2). That
  delivery is the invitation. Its validity is the enrollment's expiry.
- **Acceptance:** an `attestation` by `P` with `this = [1, P]` and the same
  value `G`. The member says of itself what the steward said of it. The two may
  use different `member` types; only the value must match. Either may be
  signed first; no order is checked.
- **Leaving:** `P` revokes its acceptance (`revoke`, `SPEC-0002` §8.7).
  **Removal:** `S` revokes the enrollment. **Retiring a steward:** `G` revokes
  the appointment. Enrollments that steward made stop counting, because (a) no
  longer holds.

### 4.3 Membership (proposed `SPEC-0004` §5.4)

A key `P` is a **member** of group `G` at time `t` if and only if the statement
set holds:

1. an `attestation` `e` with `e.this = [1, P]` assigning a `member` attribute
   with value `G`, valid at `t`, not revoked (§7.1), whose speaker is `G`, or is
   a key `S` for which a `trust` `a` with `a.says = G`, `a.this = [1, S]`, valid
   at `t` and not revoked, has an `about` that the attribute lies within
   (`SPEC-0004` §6.3 item 4); and
2. an `attestation` `c` with `c.says = P`, `c.this = [1, P]`, assigning a
   `member` attribute with value `G`, valid at `t`, not revoked.

Membership uses only `G`'s **direct** appointments: an appointment's
`may-delegate` is ignored, as `SPEC-0005` §4.2 ignores further delegation.
Membership does not depend on the relying party's anchors. Keys that a rotation
links count once (§5 gap 2). An evaluator MUST bound the members it derives
for one group (proposed: 256) and answer `work-bound` above it (§6.5).

A key that is enrolled but has not accepted, or has accepted but is not
enrolled, is **not a member**. The verdict says which half is missing, with the
new reason code `not-a-member` (§14.2) and a sentence that names it.

### 4.4 Group thresholds

- **Anchor** (`SPEC-0004` §4.2): `trusts` gains the form
  `{ group: kid, threshold: uint }`.
- **Trust statement** (`SPEC-0002` §8.6): the threshold form, with `this`
  absent, **`group: G` in place of `trusts`**, and `threshold` present. A
  trust MUST NOT carry both `trusts` and `group`, and a `group` without
  `threshold` is not a form; either is rejected at V8 (N-15). This keeps the
  statement and the anchor alike, and a 1-of-*n* trust to a group is written
  `threshold: 1`, never by omission.
- **Why not a target type** (proposed.1 had `[8, G]`): it would be a target
  valid in one place only, the threshold form, while the anchor already names
  the group in a field. A trust to each member singly is already written as a
  name (§5.3.3), and a second spelling for it is not wanted.
- Coverage and delegation from a group threshold follow §5 gap 4 exactly as for a
  listed threshold. The member set is `members(G, t)`.

### 4.5 Why this is not a name

`SPEC-0004` §5.3.6 keeps names out of thresholds: *"A name is **not** a
threshold member: `trusts` lists kids"*. A group threshold does not reverse
that rule.

- A threshold's members are still kids. A group is one kid, `G`, and its members
  are derived by kid from statements, never by label.
- A name's members are whoever its issuer binds. A group's members are only
  keys that **also signed their own acceptance** (R-M-14), so an issuer cannot
  add a key to a group the way §11.8 lets it add one to a name. It can add only
  keys it controls (§9).
- A relying party that wants a fixed set still writes `trusts: [2* kid]`.

---

## 5. Part C: `SPEC-0004` §6.4's open questions answered

`DL-0042` `review.md` flagged five gaps and took the narrowest reading of each.
The proposal is to make each reading **normative** (two are widened), so that
T-095 builds against text instead of a reading.

| # | Gap (`DL-0042`) | Proposed answer | Change to `SPEC-0004` |
|---|---|---|---|
| 1 | "Each reached as the start of a sub-path" — a member's own statement (zero hops), or a path from the member onward? | **Zero hops.** A member counts only by its own covering statement. A group that wants a delegate uses gap 4's co-issued edge, which needs *m* members to agree on the delegate. | §6.4 first sentence rewritten: "…when *n* distinct members of `M` have each made a statement that covers the ask…". The sub-path clause is removed |
| 2 | Rotation: may a successor stand in for a listed member? | **Collapse only, for now.** Linked members count once. An unlisted successor does not count for its predecessor, and a group member's successor must be enrolled itself. Applying §7.2 to coverage as a whole is a separate task, not part of W-9. | §6.4 second paragraph gains one sentence: "A successor that is not itself a member does not count for its predecessor." |
| 3 | `trusts: [A, A]` passes V8 | **Rejected at V8.** `trusts` MUST NOT repeat a kid. | `SPEC-0002` §8.6 and V8; new negative vector N-14. This closes the item `ARCH-0001` DEC-002 records as "still owed" |
| 4 | Threshold trust statements as hops, and delegation onward from a threshold set | **Specified as a set state** (below). | §6.2 and §6.4 extended; §6.1 gains the set state |
| 5 | Which attestation kinds count | **`attestation` only**, as for one-key anchors. `review` and `approve` counting is `SPEC-0005`'s, through processes. | §6.4: "Only `attestation` statements count toward a threshold." |

**Gap 4: the set state.** A threshold anchor, or a threshold trust statement
followed under §6.3 items 2 to 6 (item 1 reads `s.says = K` only), produces a
**set state** in place of a key state: `members` (the list, or
`members(G, t)`), `n`, `scope = about`, `deleg = may-delegate` (depth reduced
as in §6.3), and `cap`, `allow`, `exclude`, `visited` as in §6.3. From a set
state:

- **Coverage:** an ask is covered when `n` distinct members have each made an
  `attestation` covering it (§10.3) with the same target, type and value, each
  within `scope`, each valid before `cap`.
- **A co-issued edge** to key `K′` is followed as one edge when `n` distinct
  members have each issued a `trust` with `this = [1, K′]` and **identical**
  `about` and `may-delegate`, and that common content satisfies §6.3 items 3
  to 6 against the set state. The new `cap` is the earliest of the `n`
  statements' bounds. `K′ ∉ visited`. The members are not added to `visited`.
- **No nesting.** A co-issued trust whose target is itself a threshold set is
  not followed. This keeps T-043's "no nesting".
- Fewer than `n` agree: `threshold-not-met`. The verdict names the members that
  did agree and the ones that did not (R-O-08).

---

## 6. What is not proposed

Each omission is a decision.

- **No DEC-\* is opened, ranked or accepted.** DEC-004 stays open: scopes are
  attribute ranges under `SPEC-0003` base kinds, not a tag language. DEC-005
  stays open: the group content key is wrapped for confidentiality, and that
  is not a signing envelope for an `ArtifactStatement`.
- **No new statement kind and no new target type.** Membership is an
  attestation of base kind `member`; a group is named by a `group` field
  (§4.4). Target type 8 (proposed.1) is withdrawn.
- **No order between enrollment and acceptance.** Membership needs both, valid
  at the evaluation time; neither has to come first.
- **No group content key** (Part B, §7). Deferred to its own issue.
- **No shared signing key (option B, rejected).** If every member held `G`'s
  private key, any one member could sign as the group, which is 1-of-*n*; no
  signature could be attributed to a member; and every departure would force a
  rotation of `G`.
- **No threshold signatures (option C, deferred).** FROST (RFC 9591) would make
  *m* shares produce one signature by `G`. The verdict could not name which
  members signed or which are missing (R-O-08), the dealer would see the whole
  key, and no vetted Python implementation is in use here. AI-generated
  primitives are forbidden (`CLAUDE.md`), so it waits for a vetted library.
- **No steward thresholds.** One steward per group is what W-9 builds. The
  text above does not forbid `G` appointing several, and it does not specify
  *m*-of-*n* stewards for an enrollment.
- **No nested groups**, and no group as a member of a group.
- **No panel form for groups.** A `SPEC-0005` panel `[3, G]` would be natural.
  It has no consumer yet.
- **No successor stand-in** (gap 2), **no online membership check**
  (R-M-09 stays as it is), **no cross-wallet signature collection.** In W-9 the
  personas that co-sign are in one wallet (W-8).
- **No change to §4.3 or §5.1 to §5.4.** Name resolution, reduction and
  acceptance stay three procedures. Membership is an input to reduction, like a
  resolved name.

---

## 7. Part B: the group content key `K` — deferred

**Deferred (proposed.2).** The reviewer moved Part B to its own issue,
mofn#197. It needs
a suite key exchange and a vetted HPKE library, neither of which exists, and no
W-9 acceptance box depends on it. The text below is kept as the starting point
for that issue; it is **not proposed here**, and R-O-09 goes with it.

Originally proposed for `SPEC-0001` §8.2 and `ARCH-0003`, not for this
document's information model, because R-O-07 keeps `K` out of evaluation.

- `K` is a symmetric key generated by the steward's wallet with a vetted
  library's CSPRNG. It carries an **epoch**: a counter the steward increases
  each time `K` is replaced.
- On enrollment, the steward wraps `K` to `P` with HPKE (RFC 9180), the
  mechanism `SPEC-0001` §8.2 already names for the mailbox. A wrapped key is
  only useful to a member, but holding it proves nothing (R-O-07).
- On leave or removal, the steward makes epoch *e + 1* and wraps it to the
  members who remain (R-O-09). Content from epoch *e* stays readable to anyone
  who held *e*: forward secrecy for past content is **not** claimed.
- **Owed, and not decided here:** the suite's key exchange (`SPEC-0002` §6.1).
  `SPEC-0001` §8.2 records that KSA's suites define none yet. Two routes:
  - a separate X25519 key per persona, published by a statement the persona
    signs (preferred);
  - converting the Ed25519 identity key to X25519 (rejected: it reuses one key
    for signing and encryption).

  Choosing between them, and choosing the vetted HPKE library, is a
  `SPEC-0002` change of its own.
- **Part B is separable.** Parts A and C stand without it, and every §8 G-vector
  is evaluated without `K`. The app ships enrollment and group delegation, and
  `K` follows under its own issue.

---

## 8. Acceptance tests

Generated as `SPEC-0002` Appendix A vectors **after** acceptance, from the
engine, never hand-written. Next free ids at the time of writing: TV-45, E-23,
N-14 (recheck against `main` when generating). Fixture: `G` founds a group and appoints `S`; `S` enrolls P1, P2 and P3;
relying party R anchors `{ group: G, threshold: 2 }` about `build-provenance`
(DV-1).

| # | Case | Expected |
|---|---|---|
| G-1 | P1, P2 and P3 accepted; P1 and P2 attest `reproducible` | **yes**: 2 of 3 counted, P3 named as not needed |
| G-2 | as G-1, only P1 attests | **no**, `threshold-not-met`: P1 counted, P2 and P3 named as missing, each with its enrolling steward |
| G-3 | P3 enrolled, never accepted; P1 and P3 attest | **no**: P3 `not-a-member` ("enrolled by S, not accepted"); 1 of 2 |
| G-4 | P2 revokes its acceptance (leaves); P1 and P2 attest | **no**: P2 `not-a-member` ("left: acceptance revoked") |
| G-5 | S enrolls and accepts itself; S and P1 attest | **yes**; the verdict says S was "enrolled by itself" |
| G-6 | a key T not appointed by `G` enrolls P4, who accepts; P1 and P4 attest | **no**: P4 `not-a-member` ("enrolled by a key G did not appoint") |
| G-7 | the group delegates: P1 and P2 each trust K′ with identical `about` and `may-delegate`; K′ attests | **yes**, through one co-issued edge |
| G-8 | as G-7, P2's `may-delegate` differs | **no**: the edge is not followed, `threshold-not-met`, the difference named |
| G-9 | threshold hop: R anchors A with `depth 1`; A trusts `group: G`, threshold 2; P1 and P2 attest | **yes** |
| N-14 | `trust` with `trusts: [A, A]`, `threshold: 2` | rejected at V8 |
| N-15 | `trust` with both `trusts` and `group`; and one with `group` but no `threshold` | each rejected at V8 |

K-1 and K-2 (proposed.1, the content key) move with Part B to its own issue.

W-9's acceptance box "app and CLI give the same verdict" is met when G-1 to G-9
produce byte-identical `mofn check --format json` output and the same app rows.

---

## 9. Security considerations (proposed `SPEC-0004` §11.9)

- **Sybil members.** A steward can enroll keys it controls, and each will
  accept. Consent (R-M-14) stops a steward from counting a key against its will.
  It does not stop a steward from creating keys. As for `SPEC-0005` §4.3,
  distinctness of the people behind a group's keys is the steward's
  responsibility. R-O-08 makes it visible: the verdict says who enrolled each
  counted member, so "every counted member enrolled by S on the same day" is
  something a relying party can see. Mitigations: `G` revokes the steward,
  enrollments expire quickly, and a future steward threshold.
- **A stolen steward key** can enroll keys, but cannot add a vote for itself
  without its own enrollment and acceptance, which the verdict shows (R-M-15).
- **A stolen `G` key** can appoint stewards. `G` should be held as an
  identity key, offline where possible (`ARCH-0003` §3.2).
- **Freshness.** Leaving depends on the evaluator holding the revocation
  (`SPEC-0004` §7.1). Membership validity SHOULD be short: proposed 30 days as
  the app default, renewed by the steward.
- **A content key gives no standing.** If Part B adds one, a member that leaks
  it leaks content, not authority (R-O-07).

---

## 10. Effect on `ARCH-0001` if adopted

- §4.1: the `Principal`, `Threshold` and new `Group` rows as in §4.1 above.
- §5.1: R-M-13 to R-M-16. §5.3: R-O-07 and R-O-08.
- §5.5: the `Group` row is **closed**, by `SPEC-0002`, `SPEC-0003` and
  `SPEC-0004` (§7 of the front matter's `spec_changes_owed`).
- §7 DEC-002: "**Still owed:** `trusts: [A, A]` …" is closed by N-14.
- Version 0.4.0, `updated` set, `ARCH-0001-CHANGELOG.md` line.
- Route: a human accepts (or edits) this proposal; on that instruction, an ADR
  (next free: `ADR-0009`) records the group model, because it is a model change
  of the same weight as `ADR-0008`'s names.
- **Dependency on mofn#195.** That open PR reopens `ADR-0002` and marks
  `ARCH-0002` P3 and P6 not binding. §4.2 cites P6 and `ADR-0008` as the
  precedent for membership as an attested value. The case for base kind
  `member` does not rest on P6 (it is a value with a range, so a steward's
  appointment can be scoped to one group), but the citation and the
  `ADR-0009` route should be rechecked once #195 is decided. Folding this
  proposal into `ARCH-0001` waits for #195, because both change `ARCH-0001`
  and `propose-arch` allows one architecture change in flight.

---

## 11. Revisions

- **proposed.1** (2026-11-17): first draft, W-9 (mofn#181), `DL-0053`.
- **proposed.2** (2026-11-26): first review round (`DL-0053` `review.md`).
  Target type 8 withdrawn; a group is a `group` field of the threshold form
  (§4.4), N-15 added. No order between enrollment and acceptance (§4.2).
  Part B deferred to its own issue with R-O-09, K-1 and K-2 (§7). Rebased
  onto `ARCH-0001` v0.3.4; dependency on mofn#195 recorded (§10).
