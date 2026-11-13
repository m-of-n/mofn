---
schema: "archdoc/v1"
id: ADR-0008
title: "SDSI names in KSA: a name target, a naming base kind, and resolution without anchors"
short_title: "ADR-0008 SDSI names"
description: "Registers SPEC-0002 target type 7 (name) and SPEC-0003 base kind 12 (name), and fixes the semantics SPEC-0004 §5.3 specifies: bindings need no anchor, a label bound twice is a group, names follow rotation, and a binding is only ever in its speaker's namespace."
type: decision
category: security
status: proposed
version: "0.1.0"
version_policy: "semver; an accepted ADR changes only by superseding it"
date: "2026-11-12"
updated: "2026-11-12"
decision_makers:
  - role: student
    id: ndewedo-newbury
    authority: >
      Delegated by the sponsor (paul-lambert) on a Zoom call in October 2026;
      ARCH-0001 v0.1.7 front matter. No written sponsor confirmation is
      recorded (DL-0021).
reviewers: []
needs_review: true
reviewed: false
canonical_path: spec/ADR-0008-sdsi-names.md
defers_to: ARCH-0001
decides: []
supersedes: []
---

# ADR-0008 — SDSI names in KSA

**Status: proposed.** The six choices below were made by `ndewedo-newbury` on
2026-11-12 in the mofn#143 session; the agent drafted the text. This ADR
becomes **accepted** when a decision maker changes `status` to `accepted` and
`needs_review` to `false` (`ARCH-0001` §9). The agent does not do that. Recorded
in `DL-0039`. No `DEC-*` is decided here: names were kept in `ARCH-0001` 0.2.0
by decision (`DL-0028`), and this ADR records how the SPECs meet that.

It is an ADR because `SPEC-0002` §12 and `SPEC-0003` §12 say a registry entry is
added "by a revision of this specification accepted through an ADR".

## Context

`ARCH-0001` §1 item 2, G1, R-M-03 and §4.3 procedure 1 require SDSI names:
compound names, relative to a key, that resolve to keys (*George's Fred's Sam*,
§3.1). `ARCH-0002` P6 makes a name an attested string, and `SPEC-0002` TV-13
shows one label bound by an attestation. The SPECs had no name form, no
compound names and no resolution step. `ARCH-0001` §5.5 recorded the gap as
owed by `SPEC-0004` (mofn#143).

## Decision

1. **A name is a target, type 7: `[7, kid, [+ label]]`** (`SPEC-0002` §7.2). It
   may be the `this` of an `attestation`, which binds a name to a name, and of
   a `trust`, which trusts the keys the name resolves to. An anchor may trust a
   name. A threshold's members stay kids.
   *Rejected:* a name only as a trust subject, with no name-to-name bindings,
   which loses SDSI's linked namespaces. Also rejected: a name with no wire
   form, existing only inside the evaluator, so that nothing on the wire could
   delegate to a name.
2. **A naming type is one of base kind 12, `name`** (`SPEC-0003` §6.4). The
   base kind decides what a binding is, not the type's definer.
   *Rejected:* a per-context list of honoured name types, which every relying
   party would have to configure and which defaults to no names. Also
   rejected: hard-wiring DV-2's `name`, which is a global type and breaks
   `ARCH-0002` P1.
3. **A binding needs no path from an anchor** (`SPEC-0004` §5.3.1). The
   namespace is the issuer's. Trust enters where a resolved key is used.
   *Rejected:* covering bindings like any other claim. That joins name
   resolution to authorization reduction, which `ARCH-0001` §4.3 forbids.
4. **A label bound twice denotes both keys**, as an SDSI group (RFC 2693 §6)
   (`SPEC-0004` §5.3.3).
   *Rejected:* treating it as an error (`name-ambiguous`). That differs from
   SDSI, and it lets an issuer disable a name by adding a binding.
5. **Names follow rotation**, as trust does (`SPEC-0004` §7.2).
   *Rejected:* bindings fixed to the old key, so that every rotation leaves the
   names stale.
6. **The name failures are a missing link, a cycle and a foreign binding.**
   SDSI names have no scope, so §6.3's `widening` has nothing to apply to. The
   nearest equivalent is an attempt to bind a label in another key's
   namespace. It cannot be expressed, because a binding is always in its
   speaker's namespace, and `name-foreign` reports it as a diagnostic
   (R-7).
   *Rejected:* reusing `widening` for a trust to a name. That vector would test
   §6.3, not names.

## Consequences

- `SPEC-0002` 0.9.0, `SPEC-0003` 0.2.0 and `SPEC-0004` 0.6.0. Every existing
  vector is byte-identical and keeps its result.
- TV-13 is **not** a binding: DV-2's `name` has base kind text. TV-28…34 under
  DV-4 are the name vectors.
- A trust to a name hands the choice of key to the name's issuers
  (`SPEC-0002` §13.11, `SPEC-0004` §11.7–§11.8).
- `ARCH-0001` §5.5's SDSI row is closed (0.3.1).
- The engine work is T-040. It is unblocked, and it is not done.

## Acceptance test

A resolver that implements `SPEC-0004` §5.3 returns R-1…R-7 of `vectors.json`
→ `resolutions`, and an evaluator returns E-8…E-10 of `name_evaluations`.
The `prototype/wallet` verifier already accepts TV-27…34 and rejects N-12 and
N-13 at V7.
