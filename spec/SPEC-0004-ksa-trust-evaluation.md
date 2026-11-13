---
schema: "archdoc/v1"
id: SPEC-0004
title: "KSA Trust Evaluation — contexts, anchors, delegation, revocation, rotation, and the verdict"
short_title: "KSA Trust Evaluation"
description: "How a relying party decides whether to believe a verified statement: per-context trust anchors that may be signed or unsigned and are accepted by a human-controlled persona; delegation paths with depth, range and key constraints; thresholds; issuer revocation; rotation; and the deterministic ask-and-answer with its six-line verdict."
type: specification
category: security
status: draft
version: "0.6.0"
version_policy: "semver; MAJOR = any change to an evaluation result; MINOR = additive; PATCH = editorial"
date: "2026-10-14"
updated: "2026-11-12"
decision_makers:
  - role: sponsor
    id: paul-lambert
  - role: student
    id: ndewedo-newbury
    authority: >
      Delegated by the sponsor on a Zoom call in October 2026 (date not
      recorded): ndewedo-newbury may decide any question in this project, on the same
      footing as the sponsor, and is accountable for what they decide.
      Relayed by david-hsiao on 2026-11-03; no written confirmation from the
      sponsor is recorded (DL-0021). Supersedes the 2026-10-25 delegation and
      its exclusion of ADR-0002. Acceptance still follows ARCH-0001 §9: a
      DEC-* is accepted only by an ADR.
  - role: student
    id: david-hsiao
    authority: >
      Delegated by the sponsor on a Zoom call in October 2026 (date not
      recorded): david-hsiao may decide any question in this project, on the same
      footing as the sponsor, and is accountable for what they decide.
      Relayed by david-hsiao on 2026-11-03; no written confirmation from the
      sponsor is recorded (DL-0021). Supersedes the 2026-10-25 delegation and
      its exclusion of ADR-0002. Acceptance still follows ARCH-0001 §9: a
      DEC-* is accepted only by an ADR.
reviewers: []
needs_review: true
reviewed: false
canonical_path: spec/SPEC-0004-ksa-trust-evaluation.md
companion:
  - spec/SPEC-0002-ksa-core.md
  - spec/SPEC-0003-ksa-definitions.md
  - spec/SPEC-0005-ksa-processes.md
  - spec/ADR-0003-ksa-core-decisions.md
defers_to: ARCH-0001
related_rfcs: [RFC2119, RFC8174, RFC2693]
---

# KSA Trust Evaluation — contexts, anchors, delegation, revocation, rotation, and the verdict

**Specification SPEC-0004 · version 0.6.0 · draft**

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

Draft for review in the m-of-n project. Anchors, contexts and revocation
are ADR-0003 D3–D5.
**0.2.0 (2026-11-01):** proposed by DL-0020 from W-1 (mofn#65). §10.1 takes a
digest subject from the relying party's own copy. §10.4's integrity line also
compares that copy, and a line with nothing to examine is **not evaluated**. The
**answer** of §10.2 does not change; which verdict line reports a changed
artifact does. The version policy calls a change to an evaluation result MAJOR;
a draft stays in `0.x`, so this is 0.2.0 and not 1.0.0.
**0.2.1 (2026-11-03):** process. `ndewedo-newbury` is added to
`decision_makers`, at their instruction, and accepts 0.2.0 the same day
(DL-0020); nothing normative changes.
**0.3.0 (2026-11-03):** §10.2 answers **yes** only when every verdict line
passes, as the W-1 engine already does (DL-0021). The one input whose answer
changes is a statement whose speaker is known only from its envelope `pub`:
it was **yes** beside a failed authenticity line, and is now **no**. A change to
an evaluation result is MAJOR under the version policy; for the reason given at
0.2.0 the draft stays in `0.x`. `decision_makers` records the sponsor's October
delegation.
**0.4.0 (2026-11-07):** Appendix A's Ask 3, a hypothetical, becomes asks over
real vectors: E-1…E-4 (SPEC-0002 TV-14…20) cover `widening` and `depth`
(mofn#136, DL-0031). No rule changes and no existing answer changes.
**0.5.0 (2026-11-11):** two §10.4 rules about what a verdict prints, both
found by the W-4 demo slice (mofn#157, DL-0035). First, when no verified
attestation is about the relying party's copy, the sentences shown for the
handed statements MUST say they are about another file. Second, an acceptance
line that passes because no template is named says so. No line result and no
answer changes. Additive, so MINOR.
**0.6.0 (2026-11-12):** **name resolution**, ARCH-0001 §4.3 procedure 1
(mofn#143, DL-0039, ADR-0008). §5.3 resolves a name (SPEC-0002 §7.2 type 7)
against name bindings, which are attestations under a naming type (SPEC-0003
§6.4), with SDSI semantics: no anchor is needed to bind a name, a label bound
twice denotes both keys, and names follow rotation. An anchor (§4.2) and a
trust statement (§6.3) may trust a name. The `names` line (§10.4) reports
resolution, and §14.2 gains `name-unresolved`, `name-foreign` and `name-cycle`.
Appendix A gains R-1…R-7 and asks 7–9 (E-8…E-10). No input without a name
target changes its answer, so MINOR.

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
| **name** | a key and a chain of labels, *Alice's fred's sam* (SPEC-0002 §7.2 type 7) |
| **name binding** | an attribute of a naming type in an attestation: *the speaker's label is the target* (§5.3.1) |
| **resolution** | rewriting a name to the set of keys it denotes at the evaluation time (§5.3) |

## 3. Overview

```
        context ── anchors (§4) ─┐
                                 │       trust statements (SPEC-0002 §8.6)
  statement set ── verified ─────┼──▶  paths, narrowing at each hop (§6)  ──▶  coverage of the ask
  definitions (SPEC-0003) ───────┤                                               (§10)
  revocations, rotations (§7) ───┘                                         answer: yes | no
  evaluation time (§8) ──────────────────────────────────────────────────  because: reasons + verdict
```

Names in the anchors and the trust statements are resolved first (§5.3), and
paths are then walked over keys. Resolution reads the statement set, but it
does not read paths.

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
  trusts:        kid | name | { keys: [2* kid], threshold: uint },   ; name: §5.3
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

### 5.3 Name resolution

This is the first of ARCH-0001 §4.3's three procedures. It rewrites a **name**
(SPEC-0002 §7.2 type 7) to the set of keys it denotes at the evaluation time.
It is a procedure of its own. It runs before delegation paths (§6) and takes
nothing from them, and §6 uses only its result. ARCH-0001 §4.3 forbids
collapsing the two into one graph walk, and R-M-04 keeps naming and delegation
distinct.

#### 5.3.1 Bindings

A **name binding** is an attribute `(T, L)` in the `has` of an `attestation`
`b` in the statement set, where `T` is a naming type: its base kind is `name`
(SPEC-0003 §6.4). It binds **`b.says`'s `L`** to `b.this`, which is a key
target `[1, K]` or a name target. Under any other target a naming-type
attribute binds nothing.

A binding is **usable** at evaluation time `t` if `b` passes §5.2, is valid at
`t`, is not revoked (§7.1), and is used under the rotation rules (§7.2).

**A binding needs no path from an anchor.** A label means only what its
issuer's bindings say, because the namespace is the issuer's (ARCH-0001 R-M-03,
G1; SDSI). Trust enters where a resolved key is used: a path (§6) still has to
reach that key before anything it says counts. A binding confers no trust and
no authority on the key it names.

A binding is in its **speaker's** namespace and in no other. No statement can
bind a label in another key's namespace. Bob's binding of `fred` is Bob's
`fred`, whichever key defined the naming type it uses (SPEC-0003 §6.4).

#### 5.3.2 Procedure

`resolve(I, [L₁, …, Lₙ])` at evaluation time `t` is:

1. If `n = 0`, the result is `{I}`, with `I` replaced by its successor where a
   rotation links it (§7.2).
2. Otherwise, let `B` be the usable bindings of `L₁` in `I`'s namespace. If a
   rotation links a key `J` to `I`, `I`'s namespace includes `J`'s bindings
   that §7.2 still uses. Names follow the key, as trust does.
3. For each `b` in `B`:
   - if `b.this = [1, K]`, then `R_b = resolve(K, [L₂, …, Lₙ])`;
   - if `b.this = [7, J, M]`, then `R_b` is the union of
     `resolve(K, [L₂, …, Lₙ])` over every `K` in `resolve(J, M)`.
4. The result is the union of `R_b` over `B`.

A name `[7, I, labels]` resolves to `resolve(I, labels)`. The order of the
statement set does not affect the result, and the result is a **set**.

#### 5.3.3 Several bindings: a group

Two usable bindings of one label make a name denote both keys. This is SDSI's
group (RFC 2693 §6) and is **not an error**. A trust to that name trusts each
key (§6.2, §6.3). An issuer that adds a binding adds a member. A relying party
that wants exactly one key trusts the key (SPEC-0002 §13.11).

#### 5.3.4 Failures

A resolution whose result is empty is **unresolved**. Each failing branch is
reported with one of these codes:

| code | when |
|---|---|
| `name-unresolved` | `B` is empty at some step: no usable binding of `L` in `I`'s namespace |
| `name-foreign` | as `name-unresolved`, and the statement set holds a usable binding of the same `L` by another speaker. A diagnostic: that binding is in its own speaker's namespace, never `I`'s (§5.3.1) |
| `name-cycle` | a call `resolve(I, labels)` is reached while the same call is still in progress. That branch contributes nothing |

A branch that fails does not fail a resolution whose result is non-empty, and
the failure is still reported in `because` (§10.3).

**A binding that lies outside the window is not used and not clipped.** If a
binding is not valid at `t` or is revoked, it is not in `B`. No part of a chain
is "repaired" by another binding unless that binding is itself usable.

#### 5.3.5 Bounds

An evaluator MUST NOT nest resolution more than 16 calls deep, and MAY impose a
lower bound and a bound on the number of bindings examined in one evaluation.
Exceeding a bound fails the **whole** resolution with reason `work-bound`, never
a partial set (§6.5).

#### 5.3.6 Where names are used

A name may appear as the `this` of a trust statement (SPEC-0002 §8.6), as the
key an anchor trusts (§4.2), and as the target of a binding (§5.3.1). A name is
**not** a threshold member: `trusts` lists kids (SPEC-0002 §8.6). An ask's
subject MUST NOT be a name (§10.1). An attestation about a name that assigns no
naming-type attribute has no effect in this version.

TV-13 under DV-2 is **not** a binding: DV-2's `name` has base kind text. The
bindings in SPEC-0002 Appendix A are TV-28…34, under DV-4.

## 6. Delegation paths

### 6.1 State

Walking a path, an evaluator holds, for the current key `K`:

- `scope`: the attribute ranges `K` is trusted about;
- `deleg`: the delegation constraints `K` may pass on, or none (one hop only);
- `cap`: the earliest `not-on-or-after` imposed so far;
- `allow`, `exclude`: the accumulated key constraints;
- `visited`: the keys already on the path.

### 6.2 Starting a path

For an anchor trusting a name, resolve it (§5.3). Each key `A` in the result
starts a path of its own, as below. A name that is unresolved starts none, and
the reason is its §5.3.4 code.

For an anchor trusting key `A` (not a threshold set): `K = A`, `scope = about`,
`deleg = may-delegate` (none if absent), `cap` = the anchor's `not-on-or-after`
if it came from a statement, else unbounded, `allow` = all keys, `exclude` = ∅,
`visited = {A}`.

An anchor whose source is a statement (§4.3) starts a path only if that statement
is in the statement set, valid at the evaluation time and not revoked (§7.1).

### 6.3 Following a trust statement

From state at key `K`, a trust statement `s` is followed to key `K′` if and only
if **all** of the following hold:

1. `s.says = K`; `s.this = [1, K′]`, or `s.this` is a name and `K′` is in its
   resolution (§5.3); and `K′ ∉ visited`. Each key a name resolves to is a
   separate edge. Every other condition applies to it as to a key target, so a
   name cannot carry a key that `allow` or `exclude` forbids. A name does not
   use up depth: only the trust statement does;
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
A threshold's members are kids, never names (§5.3.6).

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
  A name binding naming `K` resolves to `K′` from the link, and `K`'s
  namespace continues as `K′`'s (§5.3.2).
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
signed or transmitted as one. Where the subject is a digest target, the
evaluator computes it from the relying party's own copy of the object; it MUST
NOT take it from a statement. The subject MUST NOT be a name (SPEC-0002 §7.2
type 7): an ask about a name is not defined in this version (§5.3.6).

### 10.2 Coverage

An ask is answered **yes** if and only if every line of its verdict (§10.4) is
**pass** and, for **every** attribute `(T, v)` in `has`, there is a statement `a`
in the statement set such that:

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

> **Why the answer waits for every line.** Items 1–4 can hold while the
> authenticity line fails: a statement verifies under the key in its envelope
> `pub`, but SPEC-0002 §10 forbids adding that key to the key store, so the
> speaker is not known. A **yes** printed above a failed line tells the relying
> party two contradictory things. With the verdict as a condition, a failed line
> is always a **no**, and that line says why.

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
revocation statements considered (§7.1) and any non-default policy (§9). For
each name used, it MUST name the name, the digests of the bindings used at each
step, the keys it resolved to, and each failing branch with its code (§5.3.4).

### 10.4 The verdict

The verdict presents the same evaluation to a person, one line per dimension.
Each line is **pass**, **fail** or **not evaluated**, with a sentence. A line is
**not evaluated** when there is nothing for it to examine: integrity when no
statement was invalid and no attestation verified, and authorization and
acceptance when no verified statement is about the subject.

| line | passes when | from |
|---|---|---|
| **integrity** | every statement used decoded canonically and its signature verified, and, where the subject is a digest target and attestations verified, at least one is about the relying party's own copy | SPEC-0002 V1, V4, V5; §10.1 |
| **authenticity** | every speaker's key is in the key store by §10 of SPEC-0002, and the envelope agreed with the statement | SPEC-0002 V3, V6 |
| **names** | every key shown has been rendered by the relying party's own label or fingerprint, and every name used resolved to at least one key (§5.3) | SPEC-0001 §7.3; §5.3 |
| **authorization** | §10.2 items 1–3 hold | §6 |
| **acceptance** | every named template is conformed to and every required process is met | SPEC-0003 §7.1, SPEC-0005 |
| **semantics** | every definition used is obtained, conforming and attributed | SPEC-0003 §9, §11 |

> **Why integrity compares the relying party's copy.** The six lines say what
> was checked, and the first question a relying party has is whether the file in
> hand is the one described. Without the comparison, a changed artifact fails
> §10.2 item 1 and the verdict can report it only under authorization, which
> blames the speaker for a change to the object. With it, integrity names both
> digests, and authorization and acceptance are not evaluated.

Where the verdict shows the handed statements' own sentences, and no verified
attestation is about the relying party's copy, it MUST say before them that
they are about another file. A sentence printed after **answer: no** with no
such framing reads as a claim about the file in hand, and that file is the one
the statement is not about.

Acceptance **passes** when no template is named: there is nothing for the
statement to fail. Its sentence MUST say that no template is named, so a
relying party does not read the pass as a template that was met.

> **Why a vacuous pass and not "not evaluated".** "Not evaluated" means there
> is nothing to examine (above). A statement that names no template has been
> examined: it is about the file and it asks for no template. Reporting it as
> not evaluated would merge two cases a relying party should be able to tell
> apart: no statement about the file, and a statement about the file that
> carries no requirement. The vacuous pass was chosen in DL-0016 and DL-0020
> (A1), and Appendix A prints it.

A key reached through a name MAY also be shown by that name, its issuer
rendered under SPEC-0001 §7.3: *Dave, as your builder*. The name is a pointer to
the key, not the key. Where a name is unresolved, the `names` line fails, and
says which label had no binding, in whose namespace.

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

### 11.7 Names choose keys

A trust to a name trusts whatever keys the name's issuers bind at the
evaluation time. Each issuer along the chain can change the answer without a
statement from the relying party. That is what a name is for, and it is
bounded: a name adds no scope, does not use depth, and cannot carry a key that
`allow` or `exclude` forbids (§6.3). A relying party that wants a fixed key
trusts the key. A wallet SHOULD show, when an anchor trusts a name, the keys it
resolves to now and whose bindings they rest on.

### 11.8 Groups grow

Because a label bound twice denotes both keys (§5.3.3), an issuer, or an
attacker holding an issuer's key, can add a member to every name that passes
through that namespace. The defences are the same as for trust: revocation of
the binding, short validity, and marking a key compromised (§7.2).

## 12. Privacy considerations

Anchors reveal whom a relying party trusts and are kept local by default — as
Matrix keeps its user-signing edges private. A persona that publishes its trust statements reveals
its relationships. An ask is local and reveals nothing unless the evaluator is
remote, in which case the evaluator learns the subject and what was asked.

## 13. References

### 13.1 Normative
[RFC2119], [RFC8174]; [SPEC-0002] KSA Core; [SPEC-0003] KSA Definitions;
[SPEC-0005] KSA Processes.

### 13.2 Informative
- [RFC2693] Ellison, C. et al., "SPKI Certificate Theory", RFC 2693, September 1999.
- [Matrix] The Matrix.org Foundation, "Matrix Specification", v1.19 — for cross-signing and private trust edges.
- [ADR-0003], [ARCH-0003].

## 14. Registries

### 14.1 Verdict lines — §10.4

### 14.2 Reason codes

`not-verified`, `unverifiable`, `type-error`, `template`, `not-valid-at-time`,
`revoked`, `no-path`, `widening`, `depth`, `key-excluded`, `key-not-allowed`,
`threshold-not-met`, `rotated-out`, `compromised`, `work-bound`,
`process-not-met`, `definition-unobtainable`, `definition-non-conforming`,
`unattributed-definition`, `name-unresolved`, `name-foreign`, `name-cycle`.

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

**Asks 3–6: delegation** (§6.3). Same context and anchor; ask: is the artifact's
`build-provenance` the value shown, at 2026-10-10T12:00:00Z. TV-5 gives Alice
`may-delegate {depth: 1, ranges: [reproducible]}`. Statements: SPEC-0002
TV-14…20; machine-readable as `evaluations` in `vectors.json`.

| ask | statements | value | answer | reason | why |
|---|---|---|---|---|---|
| 3 (E-1) | TV-14, TV-15 | attested | **no** | `widening` at TV-14 | Alice→Bob `about [attested]` is not within TV-5's `ranges [reproducible]` (item 4) |
| 4 (E-2) | TV-16, TV-17 | reproducible | **yes** | — | Alice→Bob `about [reproducible]`, no `may-delegate`: one hop within ranges; Bob may attest |
| 5 (E-3) | TV-16, TV-18, TV-19 | reproducible | **no** | `depth` at TV-18 | TV-16 passed Bob no delegation, so Bob→Dave is not followed (item 3) |
| 6 (E-4) | TV-20, TV-17 | reproducible | **no** | `widening` at TV-20 | TV-20 asks `depth 1` where at most 0 remains (item 6). The hop fails; it is not clipped to 0 |

E-4 is the reason R-M-10 (ARCH-0001) says a widening is reported, not
intersected silently: clipping TV-20 to depth 0 would have answered **yes**.

**Name resolutions** (§5.3). DV-4 held. Each row resolves one name over the
statements shown, at 2026-10-10T12:00:00Z. Statements: SPEC-0002 TV-28…34;
machine-readable as `resolutions` in `vectors.json`.

| res | name | statements | keys | reason | case |
|---|---|---|---|---|---|
| R-1 | Alice's fred | TV-28 | Bob | — | one hop |
| R-2 | Alice's fred sam | TV-28, TV-29 | Dave | — | compound: Alice's fred is Bob, Bob's sam is Dave |
| R-3 | Carol's builder | TV-30, TV-28, TV-29 | Dave | — | a binding to a name: Carol's builder is Alice's fred's sam |
| R-4 | Alice's fred | TV-28, TV-34 | Bob, Dave | — | two bindings of one label: a group, not an error (§5.3.3) |
| R-5 | Alice's fred sam | TV-28 | ∅ | `name-unresolved` | missing link: Bob binds no `sam` |
| R-6 | Alice's loop | TV-33 | ∅ | `name-cycle` | Alice's loop is defined as itself |
| R-7 | Alice's fred | TV-32 | ∅ | `name-foreign` | the only `fred` binding is Bob's: Bob cannot bind a label in Alice's namespace |

R-7 is the reason §5.3.1 says a binding is in its speaker's namespace and no
other. If resolution matched on the label alone, Bob could make himself
*Alice's fred*.

**Asks 7–9: trust to a name** (§6.2). Context `releases-by-name` in Carol's
wallet; its one anchor is **TV-31**, Carol's own trust to *Carol's builder*
about `build-provenance` in `[reproducible]`, one hop. Ask: is the artifact's
`build-provenance` `reproducible`, at 2026-10-10T12:00:00Z. Machine-readable as
`name_evaluations` in `vectors.json`.

| ask | statements | answer | reason | why |
|---|---|---|---|---|
| 7 (E-8) | TV-30, TV-28, TV-29, TV-19 | **yes** | — | Carol's builder resolves to Dave (R-3); TV-31 starts a path at Dave, and Dave attests (TV-19) |
| 8 (E-9) | TV-30, TV-28, TV-19 | **no** | `name-unresolved` at TV-31 | without TV-29, Bob binds no `sam`, so the name resolves to no key and the anchor starts no path. `names` fails |
| 9 (E-10) | TV-30, TV-28, TV-29, TV-17 | **no** | `no-path` | Bob attests, and Bob is on the chain (Alice's fred), but the name denotes Dave. A name grants nothing to the keys it passes through |

```yaml
# Ask 7 (E-8)
answer: yes
at: "2026-10-10T12:00:00Z"
because:
  - names:
      - name: {issuer: carol, labels: [builder]}
        steps: [TV-30, TV-28, TV-29]
        keys: [dave]
  - used: [TV-19]
    path:
      - {anchor: TV-31, key: dave, scope: {build-provenance: [reproducible]}}
    covered: {build-provenance: reproducible}
    checks: [verified, types, resolved, valid-at-time, not-revoked, coverage]
  - revocations considered: 0
verdict:
  integrity: pass
  authenticity: pass
  names: pass          # "Dave, as your builder (Alice's fred's sam)"
  authorization: pass  # "You trust your builder about build provenance (reproducible)"
  acceptance: pass     # TV-19 names no template
  semantics: pass      # DV-1 (TV-3), DV-4 (TV-27), both published by Alice
```
