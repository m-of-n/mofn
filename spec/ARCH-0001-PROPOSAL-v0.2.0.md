---
schema: "archdoc/v1"
id: ARCH-0001-PROPOSAL-v0.2.0
title: "Proposed ARCH-0001 v0.2.0 — key-relative extension points, predicate rendering, subject identity, citation corrections"
short_title: "ARCH-0001 v0.2.0 proposal"
description: "Prose proposal for the next MINOR version of ARCH-0001. Additive only. Open for review; nothing accepted."
type: proposal
category: security
status: proposed
version: "0.2.0-proposed.3"
version_policy: "target is a MINOR bump of ARCH-0001; all changes additive. This proposal's own revisions tracked in §10."
date: "2026-09-16"
updated: "2026-09-22"
authors:
  - role: proposer
    id: conversation-claude-opus-5
decision_makers: []
reviewers:
  - role: sponsor
    id: paul-lambert
    pass: "rev.1 reviewed 2026-09-16; three corrections applied in rev.2"
needs_review: true
reviewed: false
iteration_of: ARCH-0001
supersedes: []
superseded_by: null
canonical_path: spec/ARCH-0001-PROPOSAL-v0.2.0.md
target: spec/ARCH-0001-authorization-attestation.md
tags:
  - proposal
  - dec-002
  - dec-007
  - key-relative-namespaces
  - artifact-identity
  - citations
proposes:
  new_decisions: [DEC-007]
  withdrawn_decisions: [DEC-006]
  amended_decisions: [DEC-002]
  new_requirements: [R-M-11, R-O-05, R-O-06]
  relocated: ["R-M-12 -> ARCH-0002 P1, accepted by ADR-0001"]
  model_changes: ["§4.1 ArtifactId — additive third identification mode"]
  citation_corrections: ["draft-ietf-scitt-architecture → RFC 9943", "RFC 9804 recorded as historical", "C2PA 2.4"]
agent_checkpoint: false
agent_notes: >
  PROPOSAL against ARCH-0001 v0.1.0, per its §9.4. Nothing accepted. No DEC-*
  status changes until a human decision maker acts. Revision 2 incorporates
  sponsor corrections of 2026-09-16 — see §10. If adopted, fold into ARCH-0001,
  bump to v0.2.0, append the §8 changelog entry, and delete this file.
---

# Proposed ARCH-0001 v0.2.0

**Status: proposed. Nothing in this document is accepted.**

A prose proposal against ARCH-0001 v0.1.0, offered under its §9.4 — *"propose a
diff against this file."* All changes are additive, so the target is **v0.2.0**
under the stated policy. No open decision is closed here.

**Revision 2.** Sponsor review of revision 1 produced three corrections, one of
which is structural and is now the centre of this document. Revision history is
§10. Reviewers short on time should read §3.2 and §7.

---

## 1. What prompted this

A verification pass against current standards found one citation that has moved
and one that was over-weighted in revision 1. Separately, the sponsor's goal
statement names **semantic** assertions as the objective, and ARCH-0001 carries
`PredicateType` and `Predicate` without saying how a predicate renders to a
person — a gap in the model rather than an implementation detail.

Revision 1 also proposed a human authoring format and argued that RFC 9804 was a
live encoding contender. Sponsor review rejected both and raised an objection to
CBOR/COSE that revision 1 had missed entirely. That objection reframes DEC-002
and is §3.2.

---

## 2. Citation corrections

**`draft-ietf-scitt-architecture` is now RFC 9943**, a Proposed Standard
published **June 2026**. ARCH-0001 lists it under `related_drafts` and cites it
as a draft in §3.2 and §10. It should move to `related_rfcs` and be cited as an
RFC throughout.

This is not housekeeping. ARCH-0001 §3.3 argues that modern stacks have strong
artifact statements and weak local-name and threshold authorization languages.
That argument is considerably sharper when the stack in question is ratified
rather than moving. A reader who checks the citation and finds a draft will
assume the analysis predates publication and discount it.

Smaller items in the same pass: where C2PA appears in downstream work it is at
**2.4** (April 2026), and the originating pitch deck's 2.2 is a year stale. CDDL,
should it become relevant, is **RFC 8610 as updated by RFC 9165 and RFC 9682**.

**RFC 9804 is recorded as historical.** ARCH-0001 §3.1 already says canonical
S-expressions are "not selected here," and that stands. See §3.1.

---

## 3. DEC-002 — a criterion nobody scored

### 3.1 RFC 9804: historical, and what survives it

Revision 1 argued that RFC 9804 (Rivest and Eastlake, June 2025) elevated DEC-002
option 1, on the grounds that it defines four encodings — canonical for signing,
transport, advanced for human display, in-memory — and therefore already solved
the human-format problem.

**Sponsor correction: RFC 9804 is historical.** It is an Informational restatement
of a 1990s encoding, published so the format is citable, not because a live
ecosystem depends on it. Selecting it would mean adopting a serialization with
almost no modern library support in exchange for fidelity to a specification the
project has already declined to inherit. Option 1 should be treated as a
reference point for mapping — WP2 needs it — and not as a contender.

What survives RFC 9804 is not its syntax. It is **key-centricity**: the principle
that a principal is a key, that names are relative to a naming key, and that no
global authority is required to make an identifier meaningful. That principle is
already ARCH-0001 G1 and R-M-02, and it is the thing worth carrying forward. The
encoding that carried it is not.

This answers an open question revision 1 left for the reviewer, and the answer
saves two students real time: they will not build fixtures for an option that was
never going to win.

### 3.2 The registry objection

**Sponsor observation: the tags in CBOR and COSE are centrally defined, not key
centric.**

This is the structural correction, and revision 1 missed it entirely. Verified:

- **CBOR tags** are allocated from the IANA "CBOR Tags" registry — Standards
  Action for 0–23, Specification Required for 24–32767, First Come First Served
  above 32768. Every tag number is registry-allocated.
- **COSE header parameters** are allocated from the IANA "COSE Header Parameters"
  registry — Standards Action with Expert Review for 1–255, Specification
  Required for 256–65535, Expert Review above that, with integers below −65536
  reserved for Private Use and single-character string labels requiring Standards
  Action. COSE algorithm identifiers and CWT claim keys are likewise registry-
  governed.

Private-use ranges exist, and it is tempting to treat them as the escape. They
are not, and the distinction matters: **private use gives escape from the
registry, not a namespace.** Two parties independently using the same private-use
label collide, and nothing in the encoding can disambiguate them, because there
is no principal attached to the label. The identifier is global by construction;
only its allocation is informal.

This is the same argument SDSI made about principal names, applied one layer
down. SDSI observed that a name means something only relative to the key that
issued it, and that a global namespace requires a global authority nobody should
have to trust. Nobody applied that critique to **type** namespaces. Tag numbers,
header labels, claim keys, and predicate type URIs are all global identifiers
handed out by a central party — and a model whose whole premise is that
principals are keys inherits, at its extension points, exactly the global
namespace it rejected one layer up.

The properly key-centric form of an extension point is a pair: **(defining key,
local label)**. Key *K*'s `build-provenance` and key *K′*'s `build-provenance` are
different types, distinguishable without coordination, and neither needs
permission from a registry to exist. Compound reference through name chains
follows directly, exactly as SDSI compound names do.

ARCH-0001 already contains the precedent for handling this. R-M-01 says the
native encoding SHALL NOT be X.509, while the interchange matrix keeps X.509 as
an import target. The same move applies here: **CBOR tags and COSE headers are
interchange, not the native model.** R-I-03 already asks only for *export* to
in-toto/DSSE or COSE/CWT. Nothing requires the native information model to adopt
COSE's extension-point governance in order to export to it.

Proposed as **R-M-12** in §6.

### 3.3 A proposed fifth DEC-002 option

The registry objection does not eliminate CBOR. It separates two things DEC-002
option 2 currently bundles: CBOR as a **data model and encoding**, and
COSE/CBOR-tags as a **governed type space**. The first is neutral and well
supported in every plausible implementation language. The second is what conflicts
with key-centricity.

> **DEC-002, proposed additional option 5.** CBOR as the canonical encoding,
> using the CBOR data model and deterministic encoding rules, but with **no
> reliance on the IANA CBOR Tags registry and no native use of COSE header
> parameters**. Types, predicate types, and tags are identified key-relatively
> per R-M-12, carried as ordinary map entries. COSE_Sign1 and DSSE remain
> **export** envelopes under R-I-03, with the mapping from key-relative
> identifiers to registered COSE labels documented as a lossy interchange step in
> the §6 matrix.

This keeps modern library support, keeps SCITT and RFC 9943 interoperability at
the boundary, and keeps the native model free of central allocation. It is
offered as an option, not a recommendation; the reviewer may reasonably prefer
that DEC-002 stay a four-way choice and that R-M-12 constrain whichever wins.

Worth recording either way: **all four original options were scored on fidelity,
tooling, and ergonomics, and none was scored on namespace governance.** That is
the criterion this revision adds, and it may reorder the result.

### 3.4 A rule that holds whatever DEC-002 decides

Proposed as a requirement rather than a decision, because it constrains all
options equally.

The DSSE designers deliberately avoided canonicalization, for documented and
sound reasons: canonicalizing at verification time forces the verifier to parse
untrusted input *before* verifying it, which is error-prone and enlarges the
attack surface; canonicalization schemes have been broken before; and a canonical
form without an authenticated type indicator lets a signer produce a message in
one encoding that a verifier reads as another. Their answer was
Pre-Authentication Encoding: sign the exact bytes, with the payload type
authenticated alongside.

A project that canonicalizes at verification time walks into that critique, and
any reviewer who knows DSSE will raise it. The answer is to take DSSE's discipline
while keeping a canonical form:

> The signed payload is the canonical encoding, **verbatim**, carried with an
> authenticated type indicator. The verifier verifies the signature over the bytes
> it received and only then decodes. It never canonicalizes as part of
> verification. Canonicalization happens once, at authoring time, on trusted
> input. Any human-facing form is regenerated from already-verified bytes.

Note the interaction with §3.2: the authenticated type indicator is itself an
extension point, so under R-M-12 it must be key-relative in the native model even
though COSE supplies a registered one at the interchange boundary.

Proposed as **R-O-05** in §6.

---

## 4. DEC-006 withdrawn; display folds into DEC-007

**Sponsor correction: a readable authoring format is not required. Display forms
matter, and they tie to UI.**

Revision 1 proposed DEC-006, "authoring and display surface," with a restricted
YAML profile as its leading option. The authoring half of that is withdrawn.
Nothing in the analysis requires humans to author certificates or statements in a
text format; they are produced by tools, and an authoring format would be surface
area maintained for a use case that does not exist.

The display half is real but was filed in the wrong place. Display is not a
property of the encoding — it is what a **user interface** does with a statement
after verification, which is the same mechanism that answers "what does this
predicate value mean in words." That is DEC-007. Folding display into DEC-007
also resolves a concern revision 1 raised against itself: seven open decisions on
an unfrozen model was too many, and this removes one.

The YAML restriction list from revision 1 is retained only as an appendix note
against a future need for a diagnostic or debug rendering, and carries no
proposed status.

---

## 5. Proposed DEC-007 — predicate rendering and display

### 5.1 The gap

ARCH-0001 §4.1 defines `PredicateType` as a URI naming a statement vocabulary and
`Predicate` as a typed payload whose schema that URI identifies. §4.3 makes
statement acceptance conditional on the issuer being authorized for that
`PredicateType`. All of this concerns whether a predicate is *structurally valid*
and *permitted*. None concerns what it **means to a person**.

§3.1 credits PICS as the conceptual parent of modern attestation and §4.2 maps
`ArtifactStatement` onto it — issuer as rating service, subjects as labeled
objects, predicate as rating tuple. Right, but one step short of PICS's actual
contribution. PICS did not merely sign labels. It published **rating systems** as
separate machine-readable documents declaring the categories, permitted values,
scales, and the words a human reads. A label carried values; the rating system
carried meaning; a user agent resolved one against the other. That separation is
the idea, and it is what makes display a property of the data rather than of
whoever wrote the UI.

Modern stacks have not generalized it. Each re-invents a vocabulary inside its own
predicate type, in prose, in a specification document, where no verifier can
resolve it at runtime.

Note the interaction with §3.2: if `PredicateType` is a URI, it is a global
identifier, and R-M-12 applies to it as much as to a CBOR tag. A key-centric
predicate type is `(defining key, local label)`, and the vocabulary it
dereferences to is a statement *by that key* about what its own labels mean.
That composition — a key defining its own type space and publishing the rendering
for it — is the sharpest available statement of what this project is for.

### 5.2 Evidence the gap is live

The IETF draft *Agent Action Capsule Profile for SCITT*
(`draft-mih-scitt-agent-action-capsule-02`) defines an explicit disposition
vocabulary for agent actions: `executed`, `blocked`, `denied`, `timeout`,
`errored`, `deferred`, `expired`, `escalated`.

That is a PICS rating system, arrived at independently, in 2026, inside the SCITT
work, by authors who as far as the draft shows were not reasoning from PICS. It
is declared in prose in a draft rather than published as a resolvable artifact,
so nothing can dereference it, version it, or render from it programmatically.

This converts a claim into an observation. ARCH-0001 currently argues from history
that the PICS pattern is undersupplied. It can now argue from a current example
that the pattern is being **re-invented ad hoc because nobody specified it
generally** — and that the re-invention happens inside the very standard the
project interoperates with.

### 5.3 The proposal

> **DEC-007 — Predicate rendering, vocabulary resolution, and display**
>
> Question: how does a `PredicateType` convey the human-readable meaning of the
> values a `Predicate` carries, such that a user interface can render a statement
> without type-specific code?
>
> Options:
>
> 1. Out of scope. `PredicateType` identifies a schema; display is an application
>    concern.
> 2. A signed, versioned, dereferenceable **vocabulary statement** — itself an
>    ordinary statement by the key that defines the type — declaring claim
>    categories, permitted values, ordinal scales where they apply, and a
>    human-readable rendering for each value. Statements cite it by identifier and
>    digest.
> 3. As option 2, with rendering strings carried inline in each statement.
> 4. Reuse an existing vocabulary mechanism (SKOS, JSON-LD contexts, SHACL).
>
> Blocked on: nothing. The encoding of a vocabulary statement follows DEC-002;
> the identifier form follows R-M-12.
>
> Affects: the information model, if option 2 or 3 is selected — `PredicateType`
> acquires a defined resolution target. Affects verifier and UI output in all
> cases.
>
> Acceptance test: two unrelated predicate types, one build-provenance and one
> non-software, render legible statements through a single renderer with no
> type-specific code. Under option 2, changing a rendering must not invalidate
> existing signatures and must be detectable as a vocabulary version change.

Option 3 is noted mainly to be rejected: inlining makes every statement larger,
makes correcting a bad rendering impossible without re-signing, and lets two
statements of the same type disagree about what their own values mean. Option 4
deserves a serious look and would reduce invented surface, at the cost of a
dependency whose canonicalization and namespace governance must then be
reconciled with DEC-002, R-M-12, and R-O-05 — and all three of those are where
existing mechanisms tend to fail this model.

Option 2 has a property worth naming: a vocabulary statement is an
`ArtifactStatement` like any other, so the machinery that signs, reduces, and
verifies statements also governs the definitions of statement types. Nothing new
is required to make the semantic layer trustworthy.

### 5.4 DEC-007 and DEC-004 must not be collapsed

DEC-004 selects a **tag language** for authorization; R-M-08 requires tag
intersection semantics for every profile claimed. DEC-007 concerns a **rendering
vocabulary** for predicates.

They look similar and are not. A tag language needs a well-defined intersection
operation, because that is what reduction composes; it does not need to be
legible. A rendering vocabulary needs legibility and versioning; it has no
intersection semantics, and asking for one is a category error. They apply to
different object kinds — tags to `AuthzCert`, vocabularies to
`ArtifactStatement`.

They do share one thing, and it should be stated: under R-M-12 **both** are
key-relative. A tag is meaningful relative to the key that issued the
authorization; a predicate type is meaningful relative to the key that defined
it. That is the common principle. It is not a reason to merge them.

Collapsing them would be the most tempting available simplification and would
damage both. Proposed that ARCH-0001 say so explicitly, so it need not be
relitigated.

---

## 6. Proposed additive change to §4.1 — subject identity

`ArtifactId` is defined as `{ uri?: string, digest: { alg, hex } }`, and R-M-07
requires artifact statements to bind at least one content digest. This covers
artifacts that exist as bytes. It does not cover subjects that cannot be hashed:
a physical object, a dataset held elsewhere, an event, a role a person holds, a
book as a work rather than as a file. The stated intent is attestation over
arbitrary objects, and one identification mode is missing.

Proposed is a third mode costing no new machinery. Where a subject cannot be
hashed directly, it is **described** in the native model, the description is
canonicalized, and its digest becomes the subject's identity. The description is
data the system already encodes and signs; the canonicalization is whichever
DEC-002 selects; the digest is an ordinary content digest. R-M-07 is satisfied
rather than weakened — what is bound is the digest of the description, and the
description travels with the statement or is resolvable from it.

Three modes result: `digest` for bytes in hand, `locator` for subjects with an
external name, and `description` for subjects identified by the canonical digest
of a structured description. An `aliases` set binding several identifiers to one
subject is proposed alongside.

Two consequences for the document. This is precisely what in-toto's digest-set
model cannot express, which strengthens §3.3's gap analysis and should appear in
the interchange matrix as a known export loss. And it makes the project's own
working artifacts — library records, generated code, specification sections —
addressable as subjects well before any build pipeline exists.

Note that `locator` is a global identifier and therefore sits in tension with
R-M-12. The resolution is that a locator is *evidence about* a subject rather
than a definition of it: it is useful, it is not authoritative, and a verifier
should treat it as a hint. Worth stating in the document.

Proposed as **R-M-11** in §7.

---

## 7. Proposed new requirements

Four, all additive, in ARCH-0001's table style.

| ID | Pri | Requirement |
|----|-----|-------------|
| R-M-11 | M | An `ArtifactId` SHALL support identification by content digest, by external locator, or by the canonical digest of a structured description. At least one content digest SHALL be bound in all cases, per R-M-07. A locator SHALL be treated as non-authoritative evidence about a subject, not as its definition. |
| R-M-12 | M | Native extension points — type identifiers, predicate types, tags, and header parameters — SHALL be identified relative to a defining principal, as a (key, local label) pair. The native model SHALL NOT depend on a centrally allocated registry for their meaning. Registry-allocated identifiers MAY be used at interchange boundaries, and such mappings SHALL be documented as lossy per R-I-01. |
| R-O-05 | M | The signed payload SHALL be the canonical encoding verbatim, carried with an authenticated type indicator. A verifier SHALL verify the signature before decoding and SHALL NOT canonicalize input as part of verification. Any human-facing form SHALL be regenerated from verified canonical bytes. |
| R-O-06 | S | Verifier output SHALL report name resolution, authorization reduction, and statement acceptance as distinct results, per §4.3, rather than a single combined outcome. |

**R-M-12 is the load-bearing addition.** It is the natural completion of R-M-01:
that requirement rejects a central *identity* authority, and this one rejects a
central *vocabulary* authority. Together they say the model depends on no global
allocator at any layer. It also constrains DEC-002, DEC-004, and DEC-007
simultaneously, which is why it is proposed as a requirement rather than folded
into any one of them.

R-O-05 extends rather than replaces R-O-03, which requires that a canonicalization
algorithm be cited rather than silently invented. R-O-03 governs *which*
algorithm; R-O-05 governs *when it runs*.

R-O-06 is Should rather than Must because it constrains output shape rather than
correctness. It is proposed because §4.3 insists the three procedures not collapse
into one graph walk, and that discipline is worth little if the result is
flattened to a boolean at the last step. A statement can be authentic but
unauthorized — a valid signature from a key with no standing to make that claim —
and a combined verdict cannot express it.

---

## 8. Open questions for the reviewer

Ordered by downstream impact.

**[ANSWERED 2026-09-22 — R-M-12 stands; see ADR-0001 and ARCH-0002 P1.]**
It is no longer proposed here. What remains open is the consequence:
**does R-M-12 make DEC-002 option 2 untenable, or does proposed option 5 rescue
it?** This is now the central DEC-002 question and it should be settled before
fixtures are built. If option 5 is accepted, the practical choice narrows to "CBOR
data model with key-relative types" versus "JSON with JCS and key-relative types,"
and the decision becomes tractable for two students. If R-M-12 is judged too
strong, say so explicitly, because much of §3.2, §5.1, and §5.4 depends on it.

**[ANSWERED 2026-09-22 — it deserves its own document.]** R-M-12 is now
**ARCH-0002 P1**, accepted by ADR-0001. ARCH-0002 additionally drafts three
principles the sponsor raised at the same time: constrained objects are distinct
objects (P2), validity is checked at all three RFC 8949 levels and unknown fields
are rejected (P3), and generic parseability is a transport property rather than a
validation one (P4). **DEC-P4 — can all processing be key-local — is open there.**

**Does `locator` survive R-M-12?** §6 proposes treating it as non-authoritative
evidence. The stricter reading is that global locators have no place in the native
model at all and belong only in interchange. The looser reading is that ISBNs and
serial numbers are too useful to exclude. The proposal takes the middle position,
which may satisfy nobody.

**Does R-M-11 belong in v0.2.0 or wait for DEC-002?** The `description` mode
depends on a canonical encoding that does not yet exist. It can be specified
abstractly now, since the model is encoding-neutral by design, or deferred.
Specifying it now shapes WP1; deferring keeps v0.2.0 smaller.

**Should the interchange matrix record the in-toto export loss from §6, and the
COSE label mapping loss from §3.3?** R-I-01 requires publishing what is dropped.
Neither can be written precisely until R-M-11 and R-M-12 settle.

---

## 9. Changelog entry, if adopted

Ready to paste above the 0.1.0 entry in `ARCH-0001-CHANGELOG.md`. Trim to match
what is actually accepted.

```markdown
## 0.2.0 — 2026-09-1X

- Citations: draft-ietf-scitt-architecture replaced by RFC 9943 (Proposed
  Standard, June 2026); moved to related_rfcs. C2PA referenced at 2.4. CDDL, if
  reached, cited as RFC 8610 as updated by 9165 and 9682.
- RFC 9804 recorded as historical. DEC-002 option 1 retained as a mapping
  reference for WP2, not as a contender. Key-centricity, not S-expression syntax,
  identified as what the SPKI encoding lineage contributes.
- R-M-12 added: native extension points SHALL be key-relative (key, local label);
  no dependency on centrally allocated registries. CBOR tags, COSE header
  parameters, and CWT claim keys are interchange, not native. Completes R-M-01.
- DEC-002 amended: proposed option 5 — CBOR data model and deterministic encoding
  without IANA tag or COSE header dependence. Acceptance test extended with
  namespace governance, native authenticated type indicator, and canonicalization
  idempotence.
- DEC-006 withdrawn before filing. A human authoring format is not required.
  Display folded into DEC-007 as a UI concern.
- DEC-007 filed (open): predicate rendering, vocabulary resolution, and display.
  §5.4 records that tag languages and rendering vocabularies are distinct and must
  not be collapsed, while both are key-relative under R-M-12.
- §4.1 ArtifactId: additive third identification mode — canonical digest of a
  structured description. Aliases set added. Locator recorded as
  non-authoritative.
- Requirements added: R-M-11 (subject identification), R-M-12 (key-relative
  extension points), R-O-05 (sign-the-bytes; no canonicalization during
  verification), R-O-06 (separated verifier output).
- §3.3 gap analysis strengthened with draft-mih-scitt-agent-action-capsule-02 as
  a current instance of ad hoc vocabulary re-invention inside SCITT.
- No decision accepted. DEC-001 … DEC-005, DEC-007 remain open. DEC-006 withdrawn.
```

---

## 10. Revision history of this proposal

**0.2.0-proposed.3 — 2026-09-22.** Sponsor accepted R-M-12; it moves to
ARCH-0002 P1 via ADR-0001 and is no longer proposed here. Two §8 questions
answered. What remains in this proposal: the RFC 9943 citation, the DEC-002
amendment and option 5, DEC-007, R-M-11, R-O-05 and R-O-06.

**0.2.0-proposed.2 — 2026-09-16.** Sponsor review of rev.1. Three corrections:

1. *CBOR and COSE tags are centrally defined, not key centric.* Rev.1 missed this
   entirely and treated DEC-002 option 2 as namespace-neutral. Now §3.2, and the
   basis of R-M-12 and proposed option 5. This is the structural change.
2. *A readable authoring format is not required; display forms tie to UI.* Rev.1's
   DEC-006 is withdrawn; display folded into DEC-007 (§4, §5).
3. *RFC 9804 is historical.* Rev.1 argued it elevated DEC-002 option 1. Corrected
   in §3.1; what survives is key-centricity, not the syntax.

**0.2.0-proposed.1 — 2026-09-16.** Initial proposal: citation corrections, DEC-002
evidence, DEC-006 (authoring/display), DEC-007 (predicate rendering), ArtifactId
description mode, R-M-11 / R-O-05 / R-O-06.

---

## 11. What is deliberately not proposed

Recorded so omissions read as decisions rather than oversights.

No encoding is selected; DEC-002 stays open, and this revision argues only that it
be decided against a criterion that was missing. No tag language is selected;
DEC-004 is untouched beyond §5.4's boundary note and R-M-12's constraint. Nothing
is proposed for WP4 or WP5 — OpenPGP introducer import, X.509 import — which the
execution plan places out of scope for the semester. No transparency-service
requirement; R-O-04 stays Could and receipts stay out of the first demo. No
algorithm suite, no repository name, no implementation language: ARCH-0001
non-goal NG3, unchanged.

Nothing here alters §4.3's separation of name resolution, authorization reduction,
and statement acceptance, or §5's existing requirements. Where proposed text
appears to conflict with those, the existing text governs and the proposal is
wrong.

---

## Appendix A — withdrawn YAML profile notes

Retained from rev.1 without proposed status, against a future need for a
diagnostic or debug rendering. **Not proposed. Not required.**

Were a text rendering ever wanted, determinism would require narrowing YAML
rather than extending it: a single document with no streams; no anchors, aliases,
or merge keys; no custom tags; string-only mapping keys; duplicate keys an error
rather than last-wins; schema-driven typing, so a field declared textual makes
`no` the string `"no"`; no floating-point values; NFC-normalized strings; RFC 3339
UTC timestamps with integer seconds; and output ordering matching the binary
encoding's key order. Comments would be stripped and unsigned, which is why a
YAML surface was never a good home for meaning — under DEC-007 the rendering
belongs in the vocabulary, where it is signed.
