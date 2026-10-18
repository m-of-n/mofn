---
schema: "archdoc/v1"
id: UC-0001
title: "KSA Use Cases — scenarios traced to the specifications"
short_title: "KSA Use Cases"
description: "Eight scenarios — release attestation, review panels, archive records, AI agents, email delegation, IP delegation, third-party anchors, rotation and compromise — each with its personas, statements, evaluation and failure cases, traced to the sections of SPEC-0001 to SPEC-0005 they exercise."
type: specification
category: security
status: draft
version: "0.1.0"
version_policy: "semver; MINOR = scenario added; PATCH = editorial"
date: "2026-10-14"
updated: "2026-10-14"
decision_makers:
  - role: sponsor
    id: paul-lambert
reviewers: []
needs_review: true
reviewed: false
canonical_path: spec/UC-0001-ksa-use-cases.md
companion:
  - spec/SPEC-0001-ksa-architecture.md
defers_to: ARCH-0001
---

# KSA Use Cases — scenarios traced to the specifications

**UC-0001 · version 0.1.0 · draft**

## Purpose

Each use case states a goal, the personas involved (with controller and roles),
the statements exchanged, the ask a relying party poses, the expected answer, the
variants that must **fail**, and the specification sections it exercises. The
use cases are informative; the specifications they cite are normative. Together
they are the acceptance scenarios for a conforming wallet and the basis of the
CS Night demonstration (MD-1: supply chain primary, archives/library contrast).

Notation: *K says …* is a statement by key K; `kind` names the statement kind
(SPEC-0002 §8). "Wallet R" is the relying party's wallet; "context C" is the
context the ask is made in.

| UC | goal | domain | key specs |
|---|---|---|---|
| UC-1 | an artifact's provenance was asserted by a key entitled to assert it | supply chain | 0002 §8.5, 0003 §7, 0004 §6, §10 |
| UC-2 | a release is approved by two of three reviewers, checked by anyone | supply chain | 0005 |
| UC-3 | a library record was reviewed — the same engine on a second domain | archives | 0003, 0004 |
| UC-4 | an AI agent acts within delegated authority, traceable to a person | agents | 0001 §3.2, 0004 §9 |
| UC-5 | an email address is vouched for by the domain's delegate | email | 0003 §6.3, 0004 §6 |
| UC-6 | an IP address assignment is covered by narrowing delegation | network | 0003 §6.2, 0004 §6 |
| UC-7 | a third party's trust statement becomes an anchor only when a person accepts it | all | 0004 §4.4 |
| UC-8 | a key is rotated, then a key is compromised | all | 0004 §7, 0001 §9.6 |

---

## UC-1 — Release attestation, with entitlement

**Goal.** A relying party learns whether release artifact *X* was built
reproducibly, **and whether the key that says so was entitled to say it**.

**Personas.**

| persona | controller | roles |
|---|---|---|
| Maintainer (M) | person | define, delegate |
| Build-bot (B) | service | claim |
| Rogue tool (T) | software | claim |
| Relying party (R) | person | rely |

**Preconditions.** M has published definition `supply-chain` (DV-1) with
template `release-attestation` (SPEC-0003 Appendix A). Wallet R knows M's key and
has, in context *releases*, an anchor trusting M about `build-provenance`
(unbounded), delegable to depth 1.

**Flow.**

1. *M says B has controller service* (`attestation`, introduction — SPEC-0001 §9.1).
2. *M says trust B about build-provenance ∈ [reproducible, attested], for project m-of-n, until Friday* (`trust`).
3. B builds *X* and issues from the template: *B says sha-256:X has build-provenance = reproducible* (`attestation`, `template: release-attestation`, 7-day validity).
4. B presents statements 1–3 and DV-1 to R (SPEC-0001 §8.1).

**Ask.** In context *releases*: does `sha-256:X` have `build-provenance = reproducible` now?

**Expected.** **yes**. Path: anchor(M) → trust(M→B) → attestation by B; the value
is within B's scope; the attestation conforms to its template. Verdict: all six
lines pass. Rendered: *"build-bot attests that sha-256:X was built reproducibly
from published sources."*

**Must fail.**

| variant | answer | verdict line | reason (SPEC-0004 §14.2) |
|---|---|---|---|
| T, never delegated, signs the same attestation | no | authorization | `no-path` — *signed, but no standing to say so* |
| B attests after Friday | no | authorization | `not-valid-at-time` (the delegation's cap) |
| B's statement omits the required attribute | no | acceptance | `template` — *does not conform to release attestation* |
| one byte of the TBS changed | no | integrity | `not-verified` (SPEC-0002 V4) |
| DV-1 unobtainable | no | semantics | `definition-unobtainable` — rendered *unresolved vocabulary* |

---

## UC-2 — Review panel and approval process

**Goal.** A release is approved only when two of three reviewers approve and none
rejects within 48 hours — and any observer can check it.

**Personas.** Maintainer M (person: define, delegate); reviewers V1, V2, V3
(persons: review); observers O1, O2 (any controller: aggregate); relying party R.

**Preconditions.** M publishes `release-review` (SPEC-0005 Appendix A): a review
template, a panel `release-reviewers` delegated by M, and the process
`release-approval`. M delegates review to V1–V3 (`trust` about `outcome`).
`release-attestation`'s template names `release-approval` as its `approval`.

**Flow.** V1 and V2 sign `review` of `sha-256:X` with `outcome = approve`; V3 with
`outcome = changes`. O1 and O2 each evaluate `release-approval` and sign an
`aggregate` citing the three review digests, `result: true`.

**Ask.** As UC-1, now requiring the approval process.

**Expected.** **yes**; the acceptance line reads *"Approved: 2 approvals from
release reviewers, no rejection, within 48 hours."* R recomputes the process
itself (SPEC-0005 §6.4); the aggregates are provenance only.

**Must fail.**

| variant | outcome |
|---|---|
| an aggregate cites only V1's review but reports `true` | aggregate not accepted (SPEC-0005 §6.3 cond. 2) |
| V3 rejects; an aggregate cites only V1 and V2 | not accepted when R holds V3's review (cond. 3) |
| V1 approves twice from two keys linked by rotation | counts once (SPEC-0005 §4.3) |
| a non-member approves | not an input; process not met |
| V1's review of release Y | does not count for X (SPEC-0005 §6.1 item 3) |

---

## UC-3 — An archive record reviewed

**Goal.** Readers can tell a reviewed library record from an unreviewed stub —
with the same screens and engine as UC-1.

**Personas.** Library lead L (person: define, delegate); student reviewer S
(person: claim); reader R (person: rely).

**Flow.** L publishes `library-review` with type `reviewed`
(`yes / partial / no`, each with names and meanings in English and Spanish) and
template `record-reviewed` (target: digest of the record's `record.yaml`). L
delegates `reviewed` to S. S issues *S says sha-256:record has reviewed = yes*.

**Ask.** Has this record been reviewed?

**Expected.** **yes**, rendered from `library-review` in the reader's language, by
the **same** wallet code that rendered UC-1 — no domain-specific code (SPEC-0003
§7.2). This is the evidence that the vocabulary mechanism generalises.

**Must fail.** A reviewer delegated only for `reviewed ∈ [partial]` asserting
`yes` → `no-path` (value outside scope).

---

## UC-4 — An AI agent within delegated authority

**Goal.** An agent acts for a person, within scope and time, and every action
traces back to the person.

**Personas.** Owner P (person: delegate); release agent A (AI agent: claim);
relying party R.

**Flow.** P's wallet holds A as an owned persona whose controller is `agent`.
*P says trust A about release-tag ∈ [m-of-n/*] until 17:00, depth 0.* A signs
attestations within that scope.

**Ask.** Was this tag created under authority?

**Expected.** **yes**, with the path ending at P — the verdict names the person.

**Must fail.**

| variant | outcome |
|---|---|
| R's context anchors A directly | forbidden by default policy: agents are never roots (SPEC-0004 §9) |
| A delegates onward | not followed: depth 0 (SPEC-0004 §6.3 item 3) |
| A tries to accept a third-party anchor into P's context | refused: agent controller (SPEC-0004 §4.4) |
| after 17:00 | `not-valid-at-time` |

---

## UC-5 — Email delegation (Alice, Bob, Carol, Dave)

**Goal.** The sponsor's original scenario: a relying party believes an address
belongs to a key because the domain's delegate says so.

**Personas.** Alice (person: delegate) — trusted for the domain; Bob (person:
delegate) — runs `eng.foo.com`; Carol (person: claim subject); Dave (person: rely).

**Preconditions.** A definition with type `mailbox` of base kind **email**
(SPEC-0003 §6.3), `delegation: scoped`. Dave's context *mail* anchors Alice about
`mailbox ∈ [*@foo.com]`, depth 1.

**Flow.** *Alice says trust Bob about mailbox ∈ [*@eng.foo.com]* (narrowing).
*Bob says key(Carol) has mailbox = carol@eng.foo.com.*

**Ask.** Does Carol's key have `mailbox = carol@eng.foo.com`?

**Expected.** **yes**: anchor(Alice, `*@foo.com`) → Bob (`*@eng.foo.com`, within)
→ Bob's attestation (within).

**Must fail.** Bob attesting `carol@bar.com` → `no-path`. Alice delegating
`*@bar.com` → `widening`. **The attestation for delegation is a different type
from the base type** (the sponsor's note): `trust` about `mailbox` is not an
attestation *of* a `mailbox`, and holding one never implies the other.

---

## UC-6 — IP address delegation

**Goal.** A relying party learns whether an address assignment is covered by a chain of narrowing delegations.

**Flow.** Carol's context anchors Alice about `ip ∈ [10.0.0.0/8]`, may delegate
depth 1 within `[10.1.0.0/16]`. *Alice says trust Dave about ip ∈ [10.1.0.0/16].*
*Dave says key(Bob) has ip = 10.1.2.3.*

**Ask.** Does Bob have `10.1.2.3` at 2026-10-07T12:00:00Z?

**Expected.** **yes**, with the path Carol → Alice (10/8) → Dave (10.1/16) and the
narrowed ranges at each hop in the reasons.

**Must fail.** Alice delegating `10.2.0.0/16` → `widening` (outside the
allow-list). After Alice revokes Dave's delegation → `revoked`.

---

## UC-7 — A third-party trust statement becomes an anchor

**Goal.** ADR-0003 D3: anchors may come in signed by a third party, and become
anchors only when a person accepts them.

**Personas.** Security vendor V (organisation: delegate); wallet owner P (person:
rely); P's assistant agent G (AI agent).

**Flow.** V publishes *V says trust key(K) about build-provenance ∈ [attested]*.
The statement arrives in P's wallet in a presentation.

1. The wallet verifies it and renders: *"Security vendor V proposes that you trust
   K about build provenance (attested), not delegable, until 2026-12-31."*
2. P, a person, confirms in context *releases*. The anchor is recorded with
   `source: statement(digest)`, `accepted-by: P`.

**Expected.** K's `attested` attestations are covered in *releases*; nowhere else.

**Must fail.**

| variant | outcome |
|---|---|
| the statement is merely received, not accepted | inert: `no-path` |
| G tries to accept it | refused (SPEC-0004 §4.4 step 4) |
| V revokes its statement | the anchor lapses (SPEC-0004 §4.4) |
| asked in context *mail* | not covered: anchors are per context |

---

## UC-8 — Rotation, then compromise

**Flow.** Bob rotates: *Bob(old) says rotate to Bob(new)*, `issued` 2026-10-19T18:00Z,
effective 2026-10-20 (test vector TV-8), and publishes the new key. Later Bob's
new key is stolen; Bob's wallet owner marks it compromised.

**Expected.**

| ask | answer |
|---|---|
| a review by Bob(old) issued 2026-10-06 | still used: issued before the rotation |
| a review by Bob(old) issued 2026-10-21 | not used: `rotated-out` |
| an anchor naming Bob(old) | applies to Bob(new) from 2026-10-20 |
| a `rotate` by the stolen key to an attacker's key, after the compromise mark | ignored (`compromised`) |

---

## Traceability

| spec section | exercised by |
|---|---|
| SPEC-0002 §8.5 attestation, §8.6 trust | all |
| SPEC-0002 §8.7 revoke, §8.8 rotate | UC-6, UC-8 |
| SPEC-0002 §8.10 review/approve, §8.11 aggregate | UC-2 |
| SPEC-0003 §6 base kinds: enum, ip-prefix, email | UC-1, UC-3, UC-6, UC-5 |
| SPEC-0003 §7 templates and conformance | UC-1, UC-2, UC-3 |
| SPEC-0003 §10 rendering, multilingual | UC-1, UC-3 |
| SPEC-0004 §4 anchors and acceptance | UC-7, UC-4 |
| SPEC-0004 §6 paths, narrowing, depth | UC-1, UC-4, UC-5, UC-6 |
| SPEC-0004 §7 revocation, rotation | UC-6, UC-7, UC-8 |
| SPEC-0004 §9 policy (agents) | UC-4 |
| SPEC-0005 panels, processes, aggregates | UC-2 |
| SPEC-0001 §3.2 controllers, §9 discovery | UC-1, UC-4, UC-7, UC-8 |
