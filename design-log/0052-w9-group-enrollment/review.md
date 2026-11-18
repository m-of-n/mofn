---
schema: "design-log/v1"
id: DL-0052
part: review
date: "2026-11-17"
---

# DL-0052 — review

**Human decisions** (ndewedo-newbury, 2026-11-17, in the session): the group
key gives **access, not authority** (option A); **one steward** for now; the
steward **may be a member, only by enrolling itself, and stewardship never
gives a vote** (the agent's recommendation, accepted).

**Not yet reviewed:** the proposal text, and the eight choices listed in
`produced.md` that the agent made itself. Nothing is accepted. The proposal is
`status: proposed`, `reviewed: false`.

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
  trusted" in `this`, where every other form keeps it.
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

## Owed

- Human review of the proposal, especially the eight choices in `produced.md`.
- A second reader for Part C, gap 4 (the set state). It is the rule the engine
  most depends on.
- If it is accepted: an ADR on instruction, the fold into ARCH-0001 v0.4.0, the
  SPEC-0002/0003/0004 changes, vectors G-1…G-9 and N-14, and BACKLOG rows for
  T-095 and Part B's key exchange.
- The #181 deadline: if this is not accepted by about Nov 24, the engine and app
  cannot land by Nov 26, and the issue moves milestone.
