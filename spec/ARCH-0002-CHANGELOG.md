---
schema: "archdoc-changelog/v1"
id: ARCH-0002-CHANGELOG
title: "ARCH-0002 changelog"
type: changelog
parent: ARCH-0002
status: active
version: "0.8.1"
date: "2026-10-15"
updated: "2026-10-26"
canonical_path: spec/ARCH-0002-CHANGELOG.md
---

# ARCH-0002 changelog

Format: newest first. Versions match the principle document.

> **This file starts at 0.6.0.** ARCH-0002 ran from 0.1.0 to 0.5.0 without a
> changelog. Those versions are **not** reconstructed here — a changelog
> written from the diff weeks later is the `DL-0001` failure, and inventing
> entries is worse than admitting the gap. `ADR-0001` and
> `design-log/0002-arch-0002-cycle/` hold the history of 0.1.0–0.5.0.
>
> The 0.6.0 entry below is written **from its own merge commit and PR (#102)**,
> not reconstructed from the diff, and says so for the same reason.

## 0.8.1 — 2026-10-26

Editorial. The R-O-05 rationale no longer contrasts KSA with an earlier draft,
and now cites `SPEC-0002`, which applies the verify-before-decode rule, rather
than `ADR-0003`, which does not decide it. No principle changed.

## 0.8.0 — 2026-10-23

Additive. One clause under **P1**, `[draft]`. P1 itself is unchanged and stays
accepted by `ADR-0001`.

- **P1.1 — what a foreign `kid` is not.** From the CBOR/COSE extraction handed
  over in mofn#112 (library `rfc-8747` at `bafd536`). RFC 8747 §3.4 defines a
  COSE `kid` as a party-relative label resolved by lookup, the contrast case to
  P1's derived identifier. Three boundary rules: neither of two embedded `kid`s
  wins over the one computed from the key; a derived `kid` makes §6's
  intentional collision impossible; export emits no `cnf`. Mirrors P5.2's DSSE
  `KEYID` row. The §6 matrix rows are left to mofn#110.
- **Not reviewed.** The v0.7.1 pass recorded in `reviewers` covers P1–P7 as
  they stood; P1.1 postdates it. `reviewed` is left as the pass set it, with
  the scope stated in `agent_notes`.

## 0.7.1 — 2026-10-16

**The review MD-2 named, recorded.** No principle text changed; this is a
front-matter and provenance change only, which is why it is a PATCH.

- `reviewers` populated and `reviewed` set to `true`: P1–P7 and the CBOR note
  read on 2026-10-16 by a second person relative to the document's author —
  `ARCH-0002` was authored by the sponsor across mofn#25, #41 and #44 — which
  is what MD-2 required and what `ADR-0002` §6(a) was waiting on.
- `needs_review` stays `true`, deliberately. The reviewer authored P5.1 and
  P5.2, so the two clauses added in 0.7.0 have not been read by anyone who did
  not write them. `ADR-0002` §6(a) states that residue; whether it blocks
  acceptance is a human judgement and not a bookkeeping step.

## 0.7.0 — 2026-10-15

Additive. Two clauses on **P5**, which remains `[draft]` — `ADR-0002` is the
instrument that would make it normative and it is `proposed`, not accepted.
Closes `mofn#72`.

- **P5.1 — a non-canonical serialisation of known content is also a rejection.**
  Condition (2) of the `canonical-encoding` topic answer, routed to P5 rather
  than to a new `R-O-07` because P5 already binds encoder and verifier both.
  **Now instantiated rather than proposed:** `SPEC-0002` §4.3 states the rule
  normatively for KSA-CBOR and §13.5 cites P5 by name, so an accepted
  specification already rests on the half of P5 that was never written down.
  Records that `mofn#73`'s falsifier did not fire (DL-0007), which `SPEC-0002`
  §4.3 also cites, and that `spec/vectors/ksa-core/` N-1 and N-6 are its
  negative vectors.
- **P5.2 — P5's scope at the interchange boundary.** Resolves the collision
  with DSSE's *"consumers MUST ignore unrecognized fields"* asymmetrically:
  import rejects unrecognised envelope-exterior fields, export emits none.
  Narrowed in this revision to **export and import only**, because `SPEC-0002`
  §3 now specifies the native envelope and §13.5 settles the interior. Adds the
  `KEYID` / `says` collision as a second row owed to the `R-I-01` table.
- **Condition (6) recorded as closed** for KSA-CBOR: `SPEC-0002` §4.1 takes the
  explicit-refusal route — text preserved byte-exact, MUST NOT be normalised by
  any producer or verifier. P5.1 previously carried it as an open limit.
- `related_rfcs` gains RFC 8785 and RFC 9804, both cited in the text.
- Two rows added to *Relationship to ARCH-0001*.

**Nothing accepted.** No `DEC-*` is selected or narrowed. `ADR-0003` D2 fixes
one canonical encoding for the KSA specifications and states explicitly that it
**does not accept DEC-002**; DEC-002 and DEC-005 remain open and P5.1 is an
input to the first. Condition (5) is explicitly **not** addressed — it depends
on P4, which is held, and `library#56` owns it.

## 0.6.0 — 2026-10-14

Not this lane's change; recorded here from PR **#102** so the 0.7.0 entry above
has something to stack on. Sponsor direction of 2026-10-14, drafted alongside
`ARCH-0003`.

- **Review** and **Approval** added as statement functions over the one form —
  a review is an opinion any key may give; an approval is an authorization that
  counts only if the key reduces to a delegation for `approve`, and a review
  never satisfies it (`ARCH-0003` W-08).
- **P4's open question answered provisionally** — a definition is identified by
  the hash of its canonical encoding *and* published by a signed statement from
  its definer; locators are retrieval hints. Drafted in `ARCH-0003` §3.5, not
  accepted.
- First concrete case recorded for key-local processing: published processes
  with a declared review panel and a k-of-n criteria rule (`ARCH-0003` §3.9).
