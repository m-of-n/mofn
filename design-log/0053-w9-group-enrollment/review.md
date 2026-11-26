---
schema: "design-log/v1"
id: DL-0053
part: review
date: "2026-11-26"
---

# DL-0053 — review

**Human decisions** (ndewedo-newbury, 2026-11-17, in the session): the group
key gives **access, not authority** (option A); **one steward** for now; the
steward **may be a member, only by enrolling itself, and stewardship never
gives a vote** (the agent's recommendation, accepted).

**Round 1 left unreviewed:** the proposal text, and the eight choices listed in
`produced.md` that the agent made itself. Round 2 (below) reviewed the eight
choices and Part B. The proposal as a whole is still not accepted: `status:
proposed`, `reviewed: false`.

## Rejected by the human

- **The agent's first design: a roster.** `G` issues a threshold trust
  statement that lists the members, and enrollment is a reissue. The human
  redirected to *"an assigned trusted persona to invite other personas into the
  group, which allows them to access the group key"*. A list carried in one
  statement became membership derived from enrollments (R-M-13).
- **Option B, the shared signing key.** Any one member could sign as `G`
  (1-of-*n*). No signature is attributable, so the issue's "missing members
  named" cannot be met. Every departure rotates `G`.
- **Option C, threshold shares (FROST), for now.** It cannot name signers or
  missing members, the dealer sees the whole key, and no vetted Python library
  is in use. Generating a primitive is forbidden. The proposal (§6) records it
  as deferred, not refused.
- **Requiring the steward to be a member, and forbidding it.** Neither: the spec
  allows both, and the verdict shows a self-enrollment.

## Rejected by the agent while drafting

- **Membership by `trust` from steward to member** (the `SPEC-0005` §4.2
  delegated-panel shape, as is). A trust statement is authority. A relying party
  that anchored the steward with `may-delegate` would let any single member
  speak, which is 1-of-*n* again. An attestation carries no authority.
- **Groups as SDSI names** (`SPEC-0004` §5.3.3). `SPEC-0004` §5.3.6 keeps names
  out of thresholds, and changing that is a larger change (proposal §4.5). A
  name's members also need no consent.
- **New statement kinds `enroll` and `accept`.** Kinds are KSA-core.
  `ADR-0008` showed that a base kind recognised structurally does the same work
  with no wire kind and no domain-specific engine code.
- **An acceptance that targets the enrollment statement (`[3, digest]`).** It
  would tie the member to one enrollment, so a renewal by the steward would
  need a new acceptance. A self-claim survives renewal.
- **A group field inside the `trust` body.** A target type keeps "who is
  trusted" in `this`, where every other form keeps it. *Overruled by the human
  in Round 2:* the field was adopted and the target type rejected.
- **A trust to `[8, G]` without a threshold, meaning each member.** It would be
  a second spelling of a name trust.
- **Converting the Ed25519 key to X25519 for HPKE.** It reuses one key for
  signing and encryption. A separate key is preferred, and the choice is left to
  a `SPEC-0002` change.
- **Writing the SPEC diffs and vectors in this change.** The plan given to the
  human in the session said the first PR would carry vectors. The agent
  changed this while drafting. `propose-arch` makes a substantive change a
  proposal until a human accepts it, and vectors for unaccepted wire forms
  (target type 8, base kind `member`) would have to be withdrawn if review
  changes them. They are listed as acceptance tests (§8) instead. **The human
  should confirm this departure from the plan.**
- **Writing `ADR-0009`.** `propose-arch`: an agent never writes an ADR
  unprompted. The proposal says where one would go (§10).
- **Editing `BACKLOG-0001` (T-095, W-9).** Left for the fold, so this change
  stays one proposal.

## Round 2 (ndewedo-newbury, 2026-11-25 to 2026-11-26)

The agent presented the eight choices with a recommendation for each where it
had one. The human's answers:

| # | Choice | Human |
|---|---|---|
| 1 | acceptance required | **accepted** |
| 2 | base kind `member` | asked for an explanation, restating the rule as *"a member is a persona/identity granted a membership to the group upon acceptance"*. The agent said this agrees, and pointed out that the proposal had no order between invitation and acceptance. **Accepted, no order enforced** |
| 3 | acceptance as a self-claim (a) vs. signing the invitation's digest (b) | asked for an explanation; **a** (the agent's recommendation) |
| 4 | target type 8 vs. a `group` field in the threshold form | asked for an explanation; **the field** (the agent's recommendation in Round 2, reversing its own drafting choice) |
| 5 | a trust to a group requires `threshold` | asked what `[8, G]` and "a threshold" meant. Moot after 4: the count is part of the form |
| 6 | gap 1, zero hops | asked for an explanation; **accepted** |
| 7 | gap 2, collapse only | asked for an explanation; **the agent's recommendation** |
| 8 | 256 members, 30 days | **accepted** |
| B | the group content key | asked for an explanation; **deferred to its own issue** (the agent's recommendation) |

### Rejected by the human in Round 2

- **Target type 8 (`[8, G]`).** The agent's own drafting choice, and the
  agent argued against it when asked. It would be a target valid only in the
  threshold form, while the anchor already names the group in a field. The
  field keeps the trust and the anchor alike and puts the count in the form.
- **Enforcing that an enrollment precedes its acceptance.** Not wanted:
  membership needs both, and the order adds nothing to consent.
- **Acceptance bound to one invitation (option b).** Every renewal or steward
  change would need the member to sign again.
- **Part B in W-9.** It needs a suite key exchange (`SPEC-0002` §6.1) and a
  vetted HPKE library, neither yet chosen, and no #181 acceptance box depends
  on it. It is deferred, not refused.

### Found by the agent in Round 2

- **mofn#195** (opened 2026-11-26, sponsor's direction) reopens `ADR-0002` and
  marks `ARCH-0002` P3 and P6 not binding. Proposal §4.2 cites P6 and
  `ADR-0008` as its precedent. The agent did not change choice 2, because its
  case is a value with a range, not P6, but recorded the dependency (§10). The
  fold into `ARCH-0001` waits for #195: `propose-arch` allows one
  architecture change in flight.
- `ARCH-0001` moved to v0.3.4 since proposed.1. No requirement id clashes
  (R-M-13 and up, R-O-07 and up are free).

## Owed

- Acceptance of the proposal as a whole (Round 2 settled the eight choices and
  Part B, not the text).
- A second reader for Part C, gap 4 (the set state). It is the rule the engine
  most depends on.
- If it is accepted: an ADR on instruction, the fold into ARCH-0001 v0.4.0, the
  SPEC-0002/0003/0004 changes, vectors G-1…G-9 and N-14, and BACKLOG rows for
  T-095.
- A new issue for Part B (group content key, R-O-09, K-1, K-2, the suite key
  exchange).
- The #181 deadline (about Nov 26) has passed with the proposal unaccepted. The
  issue moves milestone, or the human decides otherwise.
