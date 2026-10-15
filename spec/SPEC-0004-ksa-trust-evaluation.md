---
schema: "archdoc/v1"
id: SPEC-0004
title: "KSA Trust Evaluation — contexts, anchors, delegation, revocation, rotation, and the verdict"
short_title: "KSA Trust Evaluation"
description: "How a relying party decides whether to believe a verified statement: per-context trust anchors that may be signed or unsigned and are accepted by a human-controlled persona; delegation paths with depth, range and key constraints; thresholds; issuer revocation; rotation; and the deterministic ask-and-answer with its six-line verdict."
type: specification
category: security
status: draft
version: "0.1.0"
version_policy: "semver; MAJOR = any change to an evaluation result; MINOR = additive; PATCH = editorial"
date: "2026-10-14"
updated: "2026-10-14"
decision_makers:
  - role: sponsor
    id: paul-lambert
reviewers: []
needs_review: true
reviewed: false
canonical_path: spec/SPEC-0004-ksa-trust-evaluation.md
companion:
  - spec/SPEC-0002-ksa-core.md
  - spec/SPEC-0003-ksa-definitions.md
  - spec/SPEC-0005-ksa-processes.md
  - spec/ADR-0003-fksa-convergence.md
defers_to: ARCH-0001
related_rfcs: [RFC2119, RFC8174, RFC2693]
---

# KSA Trust Evaluation — contexts, anchors, delegation, revocation, rotation, and the verdict

**Specification SPEC-0004 · version 0.1.0 · draft**

## Abstract

A verified statement proves that a key signed it; it does not say whether to
believe it. This document specifies how a relying party decides. Evaluation is
always relative to one **context** and that context's **trust anchors**. An
anchor may be a local, unsigned decision, or a signed trust statement — possibly
from a third party — that a human-controlled persona has verified and accepted.
From the anchors, trust flows along **delegation paths** whose ranges, depth and
permitted keys can only narrow. The document specifies thresholds, issuer
revocation, key rotation, the evaluation time, and the **ask** a relying party
poses and the deterministic **answer** — yes or no, with the reasons and a
six-line verdict a person can read.

## Status of this document

Draft for review in the m-of-n project. Delegation semantics are FKSA core v0.2.1
§10, adopted by ADR-0003; anchors, contexts and revocation are ADR-0003 D3–D5.

---

## 1. Introduction

Every system that rests on signatures must answer three questions a signature
leaves open: who holds this key, what may it say, and where trust begins. KSA's
answers are: **a key is a principal** (SPEC-0001); **what it may say is
delegated, narrowing at every hop** (§6); and **trust begins at anchors the
relying party chose, in the context where it chose them** (§4). There is no
global root, no default trust list, and no step at which merely discovering a key
makes it trusted.

## 2. Conventions and terminology

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when,
and only when, they appear in all capitals, as shown here.

Terms from SPEC-0002 §2 and SPEC-0003 §2 apply. In addition:

| term | meaning |
|---|---|
| **relying party** | the persona on whose behalf an evaluation is made |
| **context** | a named scope in a wallet with its own trust anchors (§4.1) |
| **anchor** | an entry in a context's anchor list from which trust flows (§4.2) |
| **statement set** | the verified statements available to an evaluation |
| **path** | a chain from an anchor to the key that made a statement (§6) |
| **scope** | the attribute ranges a key is trusted about at a point on a path |
| **evaluation time** | the instant at which validity and revocation are judged (§8) |

## 3. Overview

```
        context ── anchors (§4) ─┐
                                 │       trust statements (SPEC-0002 §8.6)
  statement set ── verified ─────┼──▶  paths, narrowing at each hop (§6)  ──▶  coverage of the ask
  definitions (SPEC-0003) ───────┤                                               (§10)
  revocations, rotations (§7) ───┘                                         answer: yes | no
  evaluation time (§8) ──────────────────────────────────────────────────  because: reasons + verdict
```

An evaluator MUST produce the same answer for the same inputs: the anchors of
one context, the statement set, the definitions, the key store, the ask and the
evaluation time. Nothing else — no network, no clock other than the evaluation
time, no ordering of inputs — may affect the result.

## 4. Contexts and anchors

### 4.1 Contexts

A context is a wallet-local scope (SPEC-0001 §6): where, with whom and about what
a persona acts and relies. **Every evaluation is relative to exactly one
context, and uses only that context's anchors** (ADR-0003 D4). A key trusted in
one context gains nothing in another.

### 4.2 Anchors

An anchor states that, in this context, a key — or a threshold set of keys — is
trusted about a scope.

```
anchor = {
  context:       local context id,
  source:        local | statement(statement-digest),
  trusts:        kid | { keys: [2* kid], threshold: uint },
  about:         [+ attribute-range],
  ? may-delegate: delegation-constraints,       ; SPEC-0002 §8.6
  accepted-by:   kid,                           ; an owned persona, §4.4
  accepted-at:   time,
  ? note:        text                           ; private
}
```

An anchor's `about` and `may-delegate` have exactly the meaning they have in a
trust statement (SPEC-0002 §8.6). An anchor with an empty `about` MUST NOT exist.

Anchors are a **local data structure**, not a wire format. They are never signed
as anchors and MUST NOT be transmitted unless the persona that owns the context
chooses to publish them, for example as a trust statement of its own (§4.3,
§12).

### 4.3 Sources of anchors

An anchor MAY come from any of three sources (ADR-0003 D3):

| source | what it is | what the anchor holds |
|---|---|---|
| **local** | an unsigned decision made in the wallet | the decision itself |
| **own statement** | a trust statement signed by a persona this wallet owns | the statement's digest; the owner may publish it |
| **accepted statement** | a trust statement signed by **any** key, including a third party, verified and then accepted under §4.4 | the statement's digest |

**A signature never makes an anchor.** A trust statement from a third party is a
*proposal* that names who proposed it. It becomes an anchor only by acceptance.

### 4.4 Accepting a signed anchor

To accept a trust statement as an anchor, a wallet MUST:

1. verify it (SPEC-0002 §9) — result **verified**;
2. obtain and check every definition its `about` and `may-delegate` refer to
   (SPEC-0003 §9), so that what it grants can be rendered;
3. present to the accepting persona's controller, in words (SPEC-0003 §10): who
   signed it and how that key is known (SPEC-0001 §9.3), whom it trusts, about
   what ranges, whether and how far it may be delegated, and until when;
4. obtain an explicit confirmation from a persona this wallet owns **whose
   controller is a person or an organisation**; and
5. record the anchor with `source: statement(digest)`, `accepted-by` and
   `accepted-at`.

A persona whose controller is an AI agent, a service, software or a device MUST
NOT accept an anchor unless the wallet's policy explicitly permits it for that
persona and context; any such permission MUST be recorded and shown wherever the
anchor is shown (§9).

An accepted statement remains **itself**: its validity window and its signer's
revocation continue to apply to the anchor. If the owner wants trust that
outlives the proposer, it issues its own trust statement and anchors that.

### 4.5 Evidence about controllers

A key's controller kind is a claim (SPEC-0002 §8.3). An evaluator MUST record,
for any controller kind it uses, where the claim came from: the key's own `self`
statement, an attestation by another key that the evaluation trusts, or a device
attestation. Where policy depends on a controller kind (§4.4, §9), a self-claim
alone SHOULD NOT suffice.

## 5. Inputs

### 5.1 Statement set

Only statements whose single-statement verification (SPEC-0002 §9) is
**verified** enter the statement set. Unverifiable statements are reported in
the answer's reasons but contribute nothing.

### 5.2 Type checks

A statement in the set is used only if every type it references is in a
conforming definition the evaluator holds (SPEC-0003 §9), every attribute value
is a valid assignment, every attribute range is a well-formed range of its type,
and — if it names a template — it conforms to that template (SPEC-0003 §7.1).
A failure is a **type error** for that statement and is reported.

## 6. Delegation paths

### 6.1 State

Walking a path, an evaluator holds, for the current key `K`:

- `scope`: the attribute ranges `K` is trusted about;
- `deleg`: the delegation constraints `K` may pass on, or none (one hop only);
- `cap`: the earliest `not-on-or-after` imposed so far;
- `allow`, `exclude`: the accumulated key constraints;
- `visited`: the keys already on the path.

### 6.2 Starting a path

For an anchor trusting key `A` (not a threshold set): `K = A`, `scope = about`,
`deleg = may-delegate` (none if absent), `cap` = the anchor's `not-on-or-after`
if it came from a statement, else unbounded, `allow` = all keys, `exclude` = ∅,
`visited = {A}`.

An anchor whose source is a statement (§4.3) starts a path only if that statement
is in the statement set, valid at the evaluation time and not revoked (§7.1).

### 6.3 Following a trust statement

From state at key `K`, a trust statement `s` is followed to key `K′` if and only
if **all** of the following hold:

1. `s.says = K`; `s.this = [1, K′]`; `K′ ∉ visited`;
2. `s` is in the statement set, valid at the evaluation time, and not revoked (§7.1);
3. `deleg` is present, and `deleg.depth ≥ 1` (an absent depth is 0);
4. for every attribute range in `s.about`: its type's `delegation` is not 0
   (SPEC-0003 §5.4); it is **within** some range of the same type in `scope`;
   and, if `deleg.ranges` is present, within some range of the same type in
   `deleg.ranges`. If the type's `delegation` is 1, it MUST equal that range
   rather than merely lie within it;
5. `K′` is in `allow` (and in `deleg.allow-keys` if present), and not in
   `exclude ∪ deleg.exclude-keys`;
6. if `s.may-delegate` is present, it does not widen `deleg`: its `depth` is at
   most `deleg.depth − 1`; each of its `ranges` is within a range of `deleg.ranges`
   (or of `s.about` if `deleg.ranges` is absent); its key lists do not admit a
   key the current lists forbid.

Following `s` produces the state at `K′`:

| | new value |
|---|---|
| `scope` | `s.about` |
| `deleg` | `s.may-delegate`, with `depth` reduced to at most `deleg.depth − 1`; none if `s.may-delegate` is absent |
| `cap` | the earlier of `cap`, `deleg.not-on-or-after`, `s.valid.not-on-or-after` |
| `allow` | intersected with `deleg.allow-keys` if present |
| `exclude` | united with `deleg.exclude-keys` if present |
| `visited` | `visited ∪ {K′}` |

**Widening fails the path.** If any condition fails, `s` is not followed; no
partial or repaired version of it is.

### 6.4 Thresholds

A threshold anchor or threshold trust statement trusts a set `M` of keys with
threshold `n` about a scope. A statement is **covered through the threshold**
when `n` distinct members of `M`, each reached as the start of a sub-path with
that scope, have each made a statement that covers the ask (§10.3) with **the
same target, type and value**. Delegation onward from a threshold set requires
`n` distinct members each to have issued a trust statement to the same key with
identical `about` and `may-delegate`; the resulting edge is followed as one.

Distinctness is by kid. Keys that a rotation (§7.2) links count as one member.

### 6.5 Bounds

An evaluator MUST NOT follow a path longer than 16 edges, and MAY impose lower
bounds and a bound on the total work of one evaluation. Exceeding a bound yields
the answer **no** with reason `work-bound`, never a partial **yes**.

## 7. Revocation and rotation

### 7.1 Revocation

A statement `s` is **revoked** at time `t` if and only if the statement set holds
a verified `revoke` `r` with `r.says = s.says`, `r.body.revokes` = the digest of
`s`, `r` valid at `t`, and `r.valid.not-before ≤ t` (ADR-0003 D5). A `revoke`
whose target was made by a different speaker has no effect. A `revoke` that
targets a `revoke` has no effect: revocation is permanent.

An evaluator decides with the revocations it holds. It cannot know of one it has
not received; the answer's reasons MUST state how many revocation statements were
considered, and wallets SHOULD obtain current revocations before a high-stakes
evaluation. Short validity windows remain RECOMMENDED.

### 7.2 Rotation

A verified, unrevoked `rotate` `r` from `K` to `K′`, with `K′` in the key store
by its own `key-publish`, **links** `K` to `K′` from `r.valid.not-before`.

- **The old key verifies the past only.** After the link takes effect, a
  statement by `K` is used only if its `valid.issued` is earlier than
  `r.valid.issued`. A statement by `K` with no `issued`, or a later one, is not
  used.
- **Trust follows the key.** An anchor or trust statement naming `K` as its
  subject applies to `K′` from the link, under all its original constraints.
  An evaluator MUST NOT follow more than 4 rotations from one key.
- **A compromised key cannot rotate.** If the wallet has marked `K` compromised
  (SPEC-0001 §9.6), every `rotate` by `K` is ignored, and every statement by `K` is
  used only if issued before the time of the compromise mark.

`issued` is the speaker's own claim. It orders a key's statements relative to its
rotation; it is not evidence of when a statement existed. Where that matters, an
external timestamp is required (SPEC-0001 §11).

## 8. Evaluation time

The evaluation time is the ask's `at` if present, otherwise the evaluator's
current time. Every validity check, revocation check and rotation check in one
evaluation uses that one instant. An evaluator MUST report the evaluation time in
its answer.

## 9. Policy

These are the points at which a relying party's policy may change a result. Each
has a default; an evaluator MUST report every non-default policy that affected
an answer.

| policy | default |
|---|---|
| attester lacks a `speaks` for the definition (SPEC-0002 §8.4) | warning in reasons; does not change the answer |
| a key's `self.uses` excludes the use being evaluated | warning |
| statements under an **unattributed** definition (SPEC-0003 §11.2) | not used for authorization; rendered with a warning |
| statements under a **superseded** definition | used; marked deprecated |
| a non-human controller accepting an anchor (§4.4) | forbidden |
| an anchor whose trusted key is evidenced as an AI agent | forbidden: agents are never roots of authority; their authority must reduce to a person or organisation (ARCH-0003 W-15) |
| work bounds (§6.5) | 16 edges, implementation-defined total |

## 10. Ask and answer

### 10.1 Ask

```
ask = {
  1 context: text,                       ; the local context id
  2 subject: target,                     ; SPEC-0002 §7.2
  3 has:     [+ attribute],              ; what is asked about the subject
  ? 4 at:    time
}
```

An ask is a query to a local evaluator. It is not a statement and is never
signed or transmitted as one.

### 10.2 Coverage

An ask is answered **yes** if and only if, for **every** attribute `(T, v)` in
`has`, there is a statement `a` in the statement set such that:

1. `a` is an `attestation` (or, where the ask concerns a review or approval, the
   corresponding kind), `a.this` equals the ask's subject, and `a` assigns `v` to
   type `T`;
2. `a` is valid at the evaluation time, not revoked, and passes §5.2;
3. there is a path (§6) — or, for a threshold, the paths of §6.4 — from one of the
   context's anchors to `a.says`, whose final `scope` contains a range of type `T`
   in which `v` lies (an absent range is unbounded), and whose `cap` is later than
   the evaluation time; and
4. if `a` names a template with an `approval` process, that process is met
   (SPEC-0005 §6).

Otherwise the answer is **no**.

### 10.3 Answer

```
answer = {
  answer: yes | no,
  at: time,
  because: [+ reason],
  verdict: verdict
}
```

`because` MUST name: the digests of the statements used; for each covered
attribute, the path as the sequence of anchor and trust-statement digests with
the scope after each hop; the checks performed; and, for a **no**, every reason
that stopped coverage, with its code (§14.2). It MUST state the number of
revocation statements considered (§7.1) and any non-default policy (§9).

### 10.4 The verdict

The verdict presents the same evaluation to a person, one line per dimension.
Each line is **pass**, **fail** or **not evaluated**, with a sentence.

| line | passes when | from |
|---|---|---|
| **integrity** | every statement used decoded canonically and its signature verified | SPEC-0002 V1, V4, V5 |
| **authenticity** | every speaker's key is in the key store by §10 of SPEC-0002, and the envelope agreed with the statement | SPEC-0002 V3, V6 |
| **names** | every key shown has been rendered by the relying party's own label or fingerprint, and any name statements used are covered | SPEC-0001 §7.3 |
| **authorization** | §10.2 items 1–3 hold | §6 |
| **acceptance** | every named template is conformed to and every required process is met | SPEC-0003 §7.1, SPEC-0005 |
| **semantics** | every definition used is obtained, conforming and attributed | SPEC-0003 §9, §11 |

A line that fails MUST give its reason in words: where the reason is a failed
constraint or an unmet process, the sentence is that rule's or process's
`explain` text (SPEC-0003 §8.1, SPEC-0005 §5). The verdict MUST end with the
limit line: *this establishes who said it and whether they were entitled to say
it; it does not establish that it is true.*

## 11. Security considerations

### 11.1 Anchor injection

A trust statement from an unknown party arriving in a
wallet is inert until accepted (§4.4), and acceptance requires a human or
organisational controller. The proposer's signature is shown as provenance, never
as authority.

### 11.2 Path explosion

Delegation graphs can be large and adversarial. Paths
cannot revisit a key (§6.3), are bounded (§6.5), and a bound yields **no**.

### 11.3 Revocation freshness

An evaluator cannot honour a revocation it has not
received. Short validity limits the window; the answer states what was
considered.

### 11.4 Rotation by an attacker

A stolen key can sign a `rotate` to a key the
attacker holds. Marking a key compromised (§7.2) defeats this from the mark
onward; anchors scoped narrowly and short validity limit what a stolen key can do
before it.

### 11.5 Collusion and Sybil keys

A threshold counts distinct keys. A party
controlling several keys is several members unless the party that set the
threshold prevented it; SPEC-0005 §4.3 discusses panels.

### 11.6 Time

A wrong evaluation time gives wrong answers about validity and
revocation. The time is an explicit input and is reported.

## 12. Privacy considerations

Anchors reveal whom a relying party trusts and are kept local by default (FKSA
related-work lesson RW-11). A persona that publishes its trust statements reveals
its relationships. An ask is local and reveals nothing unless the evaluator is
remote, in which case the evaluator learns the subject and what was asked.

## 13. References

### 13.1 Normative
[RFC2119], [RFC8174]; [SPEC-0002] KSA Core; [SPEC-0003] KSA Definitions;
[SPEC-0005] KSA Processes.

### 13.2 Informative
- [RFC2693] Ellison, C. et al., "SPKI Certificate Theory", RFC 2693, September 1999.
- [FKSA] — §10 trust, delegation, revocation, thresholds; §12 ask and answer; related work (Matrix) §4–§5.
- [ADR-0003], [ARCH-0003].

## 14. Registries

### 14.1 Verdict lines — §10.4

### 14.2 Reason codes

`not-verified`, `unverifiable`, `type-error`, `template`, `not-valid-at-time`,
`revoked`, `no-path`, `widening`, `depth`, `key-excluded`, `key-not-allowed`,
`threshold-not-met`, `rotated-out`, `compromised`, `work-bound`,
`process-not-met`, `definition-unobtainable`, `definition-non-conforming`,
`unattributed-definition`.

---

## Appendix A. Worked evaluation

Inputs: the statements of SPEC-0002 Appendix A, definition DV-1, and a context
`releases` in Carol's wallet whose one anchor is **TV-5** — Carol's own trust
statement (§4.3 "own statement") trusting Alice about `build-provenance` in
`[reproducible, attested]`.

**Ask 1** — is the artifact `sha-256:48dfc395…` `reproducible`, at
2026-10-10T12:00:00Z?

```yaml
answer: yes
at: "2026-10-10T12:00:00Z"
because:
  - used: [TV-4]
    path:
      - {anchor: TV-5, key: alice, scope: {build-provenance: [reproducible, attested]}}
    covered: {build-provenance: reproducible}
    checks: [verified, types, valid-at-time, not-revoked, coverage]
  - revocations considered: 1
verdict:
  integrity: pass
  authenticity: pass
  names: pass          # Carol's wallet labels Alice's key "Alice"
  authorization: pass  # "Carol trusts Alice about build provenance (reproducible or attested)"
  acceptance: pass     # TV-4 names no template
  semantics: pass      # DV-1, published by Alice (TV-3)
```

**Ask 2** — the same, at 2026-10-22T12:00:00Z. TV-7 (Alice revokes TV-4,
effective 2026-10-21) is in the statement set.

```yaml
answer: no
at: "2026-10-22T12:00:00Z"
because:
  - candidate: TV-4
    reason: revoked
    by: TV-7
  - revocations considered: 1
verdict:
  authorization: fail  # "Alice withdrew this attestation on 2026-10-21."
```

**Ask 3** — had Alice delegated to Bob with `about: [attested]`, a Bob attestation
of `reproducible` would not be covered: TV-5's `may-delegate.ranges` is
`[reproducible]`, so the delegation `[attested]` is not within it and the edge is
not followed (§6.3 item 4) — reason `widening`. A delegation of `[reproducible]`
would be followed, and Bob's `reproducible` attestation covered.
