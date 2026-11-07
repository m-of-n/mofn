---
schema: "design-log/v1"
id: DL-0026
part: review
date: "2026-11-05"
---

# DL-0026 — review

**Status: human review of the output is PENDING** on the PR for mofn#128.
Written in the same change. What the owner decided is recorded as decided.
Nothing here predicts the reviewer's verdict.

## 1. Rejected by the human

**#4, a revocation certificate generated with every key, is declined**
(owner, 2026-11-05, before any file was written). The model had flagged it as
the one item that conflicts with PLAN-0004's "no revocation product". The
decline is recorded in ARCH-0001 §3.4 and PLAN-0004 §6.2, and it is kept
apart from `R-0007` P5 (escrowed revocation), which stays open. The two are
different: #4 is a default for every key, while P5 is a pattern a user may
choose.

## 2. Where the model's own framing was wrong, caught before commit

These count as rejections too. The model's chat answer was overruled by the
repository.

1. **It worked from a stale checkout.** The session's local `main` was
   ~25 commits behind `origin/main`. The first full read of ARCH-0001 was
   v0.1.1, which has DEC-002 and DEC-003 open. On `origin/main` both are
   accepted (`ADR-0004`, `ADR-0005`), the wallet engine exists, and so do
   ARCH-0003 and R-0007. The model noticed while checking design-log numbers
   on remote branches and re-read everything from `origin/main` before
   writing. **Had it not, §3.4 would have offered "inputs" to two decisions
   that are already closed.** Agents should branch from `origin/main`
   after a fetch, never from local `main`.
2. **"Inputs to the open DECs" was mostly wrong.** In chat, items 6–10 were
   pitched as evidence for open decisions. Against `origin/main`, four of
   the six rows confirm items that are already accepted or drafted. One
   (trust-signature depth) duplicates `R-0007` P3. Only one, the v6
   fingerprint, bears on a question still open, the `kid`-preimage
   sub-question under DEC-003. §3.4 says this in its first paragraph rather
   than dressing confirmations up as inputs.
3. **#3 (primary key + subkeys) was pitched as new. It is not.** ARCH-0003
   §3.2 already has an identity key that delegates operational keys, and
   `capabilities` do the work of key flags. PLAN-0004 §6.2 cites it and adds
   only what ARCH-0003 lacks: the offline identity key, and the dependency
   on W-3.
4. **#1 and #2 were pitched as work to do. Engine v0 had already done
   them.** It uses Argon2id + SecretBox at rest, and it unlocks per
   operation with no cache. The real transfer was one gap that the chat
   answer had not named: the AEAD additional-data binding (`produced.md`).

## 3. Open for the reviewer

- **Version bump: PATCH (0.1.9; drafted as 0.1.8), not MINOR.** The `propose-arch` skill
  says an additive clarification is a MINOR bump. The model chose PATCH for
  two reasons. Precedent: 0.1.3 added DEC inputs as a PATCH. Collision:
  0.2.0 is the stated target of `ARCH-0001-PROPOSAL-v0.2.0`. §3.4 adds no
  requirement, and `version_policy` reserves MINOR for "additive
  requirements". **A reviewer who reads the skill literally should say
  so.** The skill and the policy disagree, and this PR does not settle
  that.
- **RFC 9580 citations: some were not verified verbatim.** These were
  checked against the RFC text: §5.5.3 (the AEAD additional data), §5.5.4.3
  (v6 fingerprint contents), §5.2.5 (the unknown-critical rule) and the
  §5.2.3.21 section number. These came from a fetched summary and were not
  read verbatim: the §5.2.3.7 and §5.2.3.24 section numbers, the `@` rule
  for notation names, and the key-flag values `0x01` and `0x02`. They match
  `R-0002`'s numbering, but they should be checked before WP4 cites them.
- **Should the AD binding become a requirement?** It is a fix in the
  prototype, not a W-* requirement in ARCH-0003. A candidate: *"Opening a
  private key MUST confirm it is the private key of the persona's kid."*
  That is the reviewer's call.

## 4. Not taken

#5 (ASCII armor), #11–13 (anti-lessons), #14 (OpenPGP import, WP4) and #15
(an interop test suite) are listed as out of scope in mofn#128. They are not
rejected; each can become its own issue.
