---
schema: "archdoc/v1"
id: ARCH-0002
title: "Key-relative naming, types, and domains of discourse"
short_title: "Key-relative naming"
description: "Type names, constraints, types-as-schemas, hash-identified domains of discourse, and validity — all relative to a defining key. The principle layer beneath ARCH-0001's mechanisms."
type: architecture
category: security
status: draft
version: "0.4.0"
version_policy: "semver; PATCH = editorial; MINOR = additive principle; MAJOR = breaking"
date: "2026-09-22"
updated: "2026-09-22"
decision_makers:
  - role: sponsor
    id: paul-lambert
reviewers: []
needs_review: true
reviewed: false
canonical_path: spec/ARCH-0002-key-relative-naming.md
companion:
  - spec/ADR-0001-key-relative-naming.md
defers_to: ARCH-0001
related_rfcs: [RFC2693, RFC8949, RFC9052]
open_decisions: [DEC-008, DEC-009]
agent_checkpoint: true
agent_notes: >
  ARCH-0001 remains the source of truth for the information model. This
  document holds the principles that constrain it. Where the two appear to
  conflict, ARCH-0001's §4 model governs and this document is wrong.
  P1 is accepted (ADR-0001). P2-P7 are drafted from sponsor direction of
  2026-09-22 and are not accepted. The CBOR note is an observation, not a
  principle. DEC-008 and DEC-009 are open.
---

# ARCH-0002 — Key-relative naming and processing

**Status: draft.** P1 is accepted via `ADR-0001`. **P2–P7 are drafted from
sponsor direction of 2026-09-22 and are not accepted.** The CBOR note is an
observation recorded as context, not a principle.

ARCH-0001 defines *what the objects are*. This defines *whose meanings they
carry*.

---

## P1 — Type names are local to a defining key **[accepted]**

An extension point is a pair: **`(defining key, local label)`**.

Key *K*'s `build-provenance` and key *K′*'s `build-provenance` are different
types. They are distinguishable without coordination, and neither needs
permission from a registry to exist. Compound reference follows SDSI name
chaining exactly.

**The argument.** SDSI observed that a name means something only relative to the
key that issued it, and that a global namespace requires a global authority
nobody should have to trust. That critique was never applied one layer down.
Tag numbers, header labels, claim keys and predicate-type URIs are all global
identifiers handed out by a central party — so a model whose premise is that
principals are keys inherits, at its extension points, exactly the global
namespace it rejected above.

Private-use ranges are not the answer: they give **escape from a registry, not a
namespace**. Two parties using the same private label collide, and nothing in the
encoding can disambiguate them because no principal is attached.

**Consequence.** CBOR tags, COSE header parameters and CWT claim keys are
**interchange, not native** — the same move R-M-01 already makes for X.509.

---

## P2 — The statement form: *A says B has C* **[draft]**

Statements have various structures and perform various functions. They share one
shape:

> **A says B has C**

| part | is | identified by |
|---|---|---|
| **A** | the **speaker** | a key, a hash of a key, or an **alias** resolving to one — an SDSI local name |
| **says** | the **signature** | not metadata *about* the statement — the cryptographic act *is* the saying |
| **B** | the **subject** | any `ArtifactId` mode (R-M-11): digest, locator, or description |
| **has C** | the **claim** | a predicate in some type, per P3 |

Per SDSI and SPKI, **the speaker is the key.** There is no separate notion of
"who signed this" versus "who said it", and no authority above A that makes A's
saying meaningful.

### Functions over the form

The form is fixed; what a statement *does* varies.

| function | form | notes |
|---|---|---|
| **Attestation** | *A says B has C* | the basic case. Example: attesting that B is associated with a defined schema of tag values |
| **Delegation** | *A says B **can speak about** (Domain, Topic)* | authority is scoped **semantically**, not only by tag |
| **Constraint** | *A says* … a narrowing over a schema of tag values | a function, not a separate kind of object |
| **Contract** | — | **open.** The sponsor indicated a further form; not yet specified. See DEC-009 |

### Delegation is scoped by domain and topic

This is the consequence worth drawing out. Delegation is not *"B may make claims"*
— it is *"B may speak about **this domain of discourse**, on **this topic**."*

So P4's domains of discourse are **not only the unit of meaning — they are the
unit of authority scope.** One construct carries both, and a delegation chain
narrows semantic reach and authority together rather than as two parallel
mechanisms. That is the strongest available form of the project's thesis, and it
is why meaning and authority should compose under one reduction rather than two.

### Consequences for constraints

Because a constraint is a *function over the statement form* rather than an
annotation on a type:

1. **It is an ordinary signed statement** — subject to the same authorization,
   reduction and revocation as any other.
2. **A constrained object is a different object from its type.** Refinement by
   construction, not inheritance: no subtype relation, so no silent
   substitution in either direction.
3. **It matches SPKI tag intersection already.** The intersection of two tags is
   a *third tag*, not a narrowed first one. R-M-08 generalises from tags to
   every constrained object.
4. **Under P1 the constrained object lives in the speaker's namespace.** If *K*
   defines `T` and *K′* constrains it, the result is *K′*'s. *K* need not agree
   and cannot be bound by a constraint it did not author.
5. **Whether a constraint binds you is an authorization question**, not a typing
   one — and it reduces through the ordinary chain.

**Open:** does a constrained object record its origin (`derived_from: K:T`)?
Useful to a verifier, and a channel for claiming association with a type whose
author never agreed.

---

## P3 — A type is a schema **[draft]**

A type is not a bare label. It is a **schema** that carries, together:

| part | for |
|---|---|
| **representation** | how the data is encoded — structure, fields, cardinality |
| **constraints on usage** | what a conforming use may and may not do |
| **semantic descriptions** | what it *means*, in words |
| **tags for human review** | so a person can judge the **usage**, not just the shape |
| **short descriptions, possibly multilingual** | the text a reader actually sees |

The last three are the part every modern stack omits. A schema that validates
structure and says nothing about meaning forces every consumer to re-derive
intent from prose in a specification — which is why the same vocabulary keeps
being re-invented ad hoc (`draft-mih-scitt-agent-action-capsule-02` is a current
instance).

**PICS is the early example.** It published *rating systems* — categories,
permitted values, scales, and the words a human reads — as machine-readable
documents separate from the labels citing them. That separation is the idea, and
bundling it into the type is the generalisation.

**Multilingual descriptions are a requirement, not a nicety.** A single-language
description silently makes the type's meaning local to one readership, which is
the same failure as a global namespace, one layer up.

---

## P4 — Domains of discourse are hash-identified sets of schemas **[draft]**

A **domain of discourse** is a *set* of the schemas in P3, serialized in a form
that can be reliably and repeatably hashed. **That hash identifies the set and
provides integrity over all of it** — every type, every constraint, every
description, together.

Why the set and not each schema individually:

- **Types are not independent.** One references another, constrains another,
  shares a value scale with another. Hashing them separately lets a consumer
  assemble a combination the author never published or checked.
- **It gives one thing to cite.** A statement references its domain of discourse
  by hash. A verifier that has that domain has *exactly* the meanings the issuer
  had — not a version-skewed approximation.
- **It makes disagreement visible.** Two parties with different hashes know they
  are talking about different vocabularies, rather than discovering it through a
  misinterpretation.

**Hash-as-identity, applied to meaning.** The same move the model already makes
for artifacts (R-M-11's `description` mode) and that the project's own library
makes for documents.

**This puts canonical serialization on the critical path for the semantic layer,
not just the signing layer.** A domain of discourse cannot be identified by hash
unless it canonicalizes deterministically — so DEC-002 and R-O-05 constrain
DEC-007 directly. They are one problem, not two.

**Open:** is a domain of discourse itself a statement by a key — so it inherits
authorization and revocation — or a bare hashed artifact that any key may cite?
The first composes with everything else; the second is simpler and allows
vocabularies nobody owns.

---

## P6 — A name is an attested string **[draft]**

Sponsor direction, 2026-09-22: *"a 'name' is just a type of attested string."*

There is no distinct naming object. A name is a **statement whose predicate is a
name**:

> *A says B has name "fred"*

`NameCert` is therefore not a *kind* of object — it is P2's form with a
particular predicate type. The same holds for `AuthzCert` (delegation),
`ArtifactStatement` (attestation) and `Endorse`.

### This resolves register item 6a

ARCH-0001 §4.2 lists five statement **kinds**; P2 says one **form** with
**functions**. The tension dissolves once a name is an attested string: the five
are **functions over one form**, distinguished by predicate type, not five
object types.

**What survives unchanged is §4.3's separation of *procedures*.** Name
resolution, authorization reduction and statement acceptance remain three
distinct algorithms and must not collapse into one graph walk. That was always a
statement about *procedures*, not about *object kinds* — and reading it as the
latter is what made 6a look like a contradiction.

`AclEntry` remains the outlier, and informatively so: it is **unsigned**, so it
has no speaker and is not a statement at all. It is local policy — the fixed
floor **DEC-008** argues cannot be key-local. A model whose floor is key-relative
has no floor, and `AclEntry` is where that floor lives.

### Consequences

- One encoding, one signing path, one reduction input type. A verifier that can
  read an attestation can read a name binding.
- **Predicate type is the discriminator**, and under P1 it is key-relative — so
  *whose* notion of "name" is explicit rather than global.
- A name is revocable, delegable and constrainable **by the same machinery as
  any other claim**, because it is not special.

---

## P7 — Authorization is a family, deployed by profile **[draft]**

Sponsor direction, 2026-09-22: *"authorization is of multiple types and ways to
deploy, with different use case profiles and usage of predefined tag/label
types."*

There is no single authorization mechanism to choose. There is a **family**,
and a deployment selects a **profile**: which predefined tag/label types are in
use, how they intersect, and what a verifier must do with them.

**This reframes DEC-004.** The question is not *"which tag language?"* but
*"what does a profile have to specify, and what is the minimum profile?"* A
profile names:

| | |
|---|---|
| tag/label types in use | drawn from a domain of discourse (P4) |
| intersection semantics | per type — R-M-08 already requires this per profile |
| required verifier behaviour | what must be understood, per P5 |
| rendering | the human-readable form, per P3 |

### Where this meets DEC-007

**DEC-004 and DEC-007 share a mechanism without merging.** A "predefined
tag/label type" is a type in the P3 sense: representation, constraints,
semantics, and human-readable rendering, published in a domain of discourse.
Authorization tags and predicate vocabularies are **defined the same way**.

They still do different jobs — §5.4 stands: a tag language needs intersection,
a rendering vocabulary needs legibility, and asking either for the other is a
category error. What is now clear is that **both are types**, so one definition
mechanism serves both. That is an argument for P3 and P4 being load-bearing
rather than decorative.

---

## P5 — Validity is checked, never assumed **[draft]**

RFC 8949 gives a three-level hierarchy that this model adopts wholesale:

| level | question | who checks |
|---|---|---|
| **well-formed** | is it decodable at all? | generic decoder |
| **valid** | does it meet the data model's own constraints — unique map keys, correct tag content? | validity-checking decoder |
| **expected** | is it what this application requires? | the application |

**All three are required. None may be skipped, and a failure at any level is a
rejection, never a repair.**

Beyond the three: **an unknown field in a signed payload is an error, not
something to skip.** The default is must-understand; skippability is opt-in and
explicit, never the other way round.

**This failure mode is live, not theoretical.** CVE-2025-59420: Authlib accepted
unknown `crit` header parameters — an RFC violation — producing a possible
authorization bypass. COSE's `crit` (RFC 9052 §3.1) exists precisely to say
"reject if you do not understand this," and an implementation that ignores it
silently accepts authorization it never evaluated. **We invert the default so
that forgetting is safe:** unknown is critical unless declared otherwise.

---

## Note — how CBOR separates extent from meaning **[observation, not a principle]**

Recorded as context for P5, not as an issue. CBOR's initial byte splits the
**major type** (top 3 bits) from the **additional information** (bottom 5 bits,
a small value or a length indicator), so a decoder can determine the *extent* of
any item without understanding its *semantics*. That is what makes an unknown
element skippable and well-formedness decidable without a schema.

It is a good property and a deliberate one. It is worth writing down only
because it explains **why P5 has to be stated explicitly**: the encoding makes
walking past an unknown field easy and cheap, so "reject what you do not
understand" has to be a rule rather than a consequence of the format.

The one-line form:

> A verifier **may traverse** what it cannot interpret.
> A verifier **must never accept** what it cannot interpret.

**Much of this will be built inside CBOR wrappers regardless**, so this is a
property of the substrate we expect to work in rather than a choice to be made.
It does not constrain DEC-002 by itself — P1 does that.

---

## DEC-008 — Can all processing be key-local? **[open]**

Sponsor question, 2026-09-22. If type names are key-local, can the *processing*
be too — validation, constraints, rendering, intersection?

### Proposed answer: yes above a fixed core, never below it

**Key-local is right for declarative processing.** Constraint expressions, field
validity rules, rendering vocabularies (DEC-007), tag intersection semantics for
a profile — all of these are things a defining key can publish as ordinary
statements, and a verifier can evaluate them. They are already `ArtifactStatement`s;
nothing new is required to make them trustworthy.

**Key-local is wrong for the core.** Signature verification, canonicalization,
the reduction algorithm, and **the definition of what "valid" means** must stay
fixed. The reason is short: *if a key may define how its own statements are
validated, it may define them as always-valid.* A model whose floor is
key-relative has no floor.

### The boundary test

A processing rule may be key-local when a verifier can evaluate it:

- **totally** — it terminates on every input
- **within bounded resources** — no unbounded search or allocation
- **without side effects** — no network, no filesystem, no state
- **without privilege** — evaluating it grants nothing

That admits a declarative constraint language. It excludes arbitrary code:
executing issuer-supplied code to decide whether to trust the issuer is a
different and much worse trust model.

### Why this matters beyond elegance

If it holds, the same delegation machinery carries **authority and meaning
together**: a key delegates the right to make a claim *and* the definition of
what that claim means, in one chain, reducible by one algorithm. That is a
genuinely new position, and it is the strongest form of the project's thesis.

### To settle it

1. Write one constraint in the candidate declarative form and reduce it by hand.
2. Show a case where key-local processing gives a **different and better** answer
   than a fixed rule — otherwise the generality is unearned.
3. Show the failure: a key that attempts to define itself valid, and exactly which
   fixed core rule stops it.

---

## DEC-009 — What is the contract form? **[open]**

The sponsor named a further statement function alongside attestation and
delegation, and the note is incomplete: *"…while contracts …"*.

Attestation and delegation are both **unilateral**: A says something, and
nothing is required of B for the statement to be well formed. A contract reads
as the case where that is not true — mutual obligation, or a statement whose
meaning depends on more than one speaker.

**Not specified here on purpose.** The open questions are what it is for, whether
it needs multiple speakers over one statement (which threshold subjects already
partly provide), and whether it is a third function over the same *A says B has
C* form or a genuinely different structure. Answering it by guessing would put a
shape in the model that nobody asked for.

---

## Relationship to DEC-007

P3 and P4 largely **answer** DEC-007 (predicate rendering) rather than merely
constraining it. DEC-007 option 2 proposed "a signed, versioned, dereferenceable
vocabulary document". P3 and P4 say what that document actually is:

- not a vocabulary *alongside* the type — **the type is the schema**, semantics
  and human-review tags included (P3);
- not one document per type — **a hash-identified set** whose hash covers every
  type and description in it (P4).

If P3 and P4 are accepted, DEC-007 should be re-stated in their terms or closed
as answered by them.

---

## Relationship to ARCH-0001

| ARCH-0001 | constrained by |
|---|---|
| `Tag`, R-M-08 intersection | P1, P2 |
| `AuthzCert` delegation | **P2 — scoped by (Domain, Topic)** |
| `PredicateType`, `Predicate` | P1, P3, P4, DEC-007 |
| DEC-002 encoding | P1 — registry dependence is native-disqualifying; **P4 — the domain-of-discourse hash needs deterministic canonicalization** |
| DEC-004 tag language | P1, P2, P3 |
| §4.3 statement acceptance | P5 |
| §4.2 statement kinds | **P6 — functions over one form, not five object types** |
| DEC-004 tag language | **P7 — a profile question, not a language choice** |

Where this document and ARCH-0001 §4 appear to conflict, **ARCH-0001 governs**
and this document is wrong.
