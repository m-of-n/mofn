---
schema: "archdoc/v1"
id: R-0006
title: "Comparative Anatomy of the Mechanisms: the Evidence Base for DEC-002 and DEC-004"
short_title: "Mechanism"
description: "The D3 mechanism report: four layers the field fuses, the six conditions a signed encoding must meet, the DEC-002 candidates scored against them, and the authorization algebra that distinguishes DEC-004's options. Evidence only — it decides nothing. v0.2.0 reads the scoring against ADR-0003 D2, which fixed one canonical encoding without accepting DEC-002."
type: research
category: security
status: draft
version: "0.2.0"
date: "2026-10-14"
updated: "2026-10-16"
needs_review: true
reviewed: false
canonical_path: research/0006-mechanism/report.md
companion:
  - research/0001-signatures-and-attestation/report.md
  - research/0005-context/report.md
informs: [PLAN-0001, PROC-0004]
open_decisions: [DEC-002, DEC-003, DEC-004, DEC-005]
backlog: T-026
library_pin: "library@60b3284"
---

# Comparative Anatomy of the Mechanisms
## The evidence base for DEC-002 and DEC-004

**Status: second draft. It decides nothing, and that is not a disclaimer.**
DEC-002 and DEC-004 are open. `CONTRIBUTING` §5 and `ARCH-0001` §9.2 are
explicit that only an `ADR-NNNN` accepts a decision; MD-3 **narrowed** DEC-002
without accepting it, and `ADR-0003` **D2** has since fixed one canonical
encoding for the KSA core while saying in terms that it **does not accept
DEC-002**. Nothing below may be cited as a decision. §3.9 states where the
evidence sits relative to both, and §3.13 reads conditions (5) and (6) against
the specifications D2 brought with it, because a reviewer must be able to see
all of this without reading an issue thread.

**What changed in v0.2.0.** `ADR-0003`, `SPEC-0001`…`SPEC-0005`, `UC-0001` and
`ARCH-0003` landed on 2026-10-14, after this report was drafted. §3.2, §3.9,
§3.10, §3.12, §5.2, §6 and §8 are reconciled against them and §3.13 is new. No
score in §3.4–§3.8 changed: the scoring was against specification text that has
not moved, and D2 did not select by scoring. `design-log/0012-…/review.md` §4
records what that reconciliation refused to do.

Bibliography pinned at **`library@60b3284`**. Citation keys `[@record-id]`
resolve at that commit; all 62 were re-checked against it for this revision.

**This is a synthesis pass, not a retrieval pass.** No new web retrieval was
performed. The evidence is survey R-001, the library's FX-1 extractions of
RFC 8949 [@rfc-8949], RFC 8785 [@rfc-8785] and RFC 9804 [@rfc-9804], the
`canonical-encoding` topic answer, the DSSE read [@secure-systems-lab-dsse],
and the decoder spike recorded in `design-log/0007-rejecting-decoder-spike/`.
`searches.md` records that absence and says where the original searches live.
What this report adds is **arrangement**: the material exists across three
extractions, a topic answer, a spike and a survey, and no single document puts
it in front of a reviewer in the order a decision needs.

This is the second of the three D3 reports (`PROC-0004` §3): *comparative
anatomy; the evidence base for DEC-002/DEC-004.* Context is **R-0005**; uptake
is **R-0004**.

---

## Abstract

An encoding decision looks like a matter of taste and is in fact a security
decision, because **determinism is not uniqueness**. RFC 8949 §4.2's
deterministic encoding is an *encoder-side* rule, and a conforming decoder
accepts non-deterministic input happily; its FX-1 extraction enumerates
**fourteen** decisions §4.2 leaves to the application.

This report sets out six conditions a signed encoding must meet, in two groups.
Four make it **safe to sign**. Two more make it **safe to derive an identifier
from**, and no *encoding* supplies them. The asymmetry is the finding: a sort or
normalisation divergence fails **loudly** when signing, as a signature
mismatch, and **silently** when naming, where it yields a confidently wrong
name.

**The accepted core now demonstrates that asymmetry rather than only predicting
it** (§3.13, new in v0.2.0). `SPEC-0003` §6 supplies condition (5) for ranges —
eleven base kinds, eight with set-valued array ranges, every one given a
canonical order — and `SPEC-0004` §6.3 is careful to compare ranges by containment and
never by bytes. But the three fields that are semantically *sets* one layer up
— the threshold member list `trusts`, the scope `about`, and the delegation
key lists — carry no order rule and no distinctness rule, while `SPEC-0002`
§4.1 makes array order *"significant and signed"* and §4.5 makes the statement
digest a hash of those bytes. One semantic trust statement therefore has as many
digests as its member list has permutations, and `revoke`, `review` and
`approve` all name statements by digest. The loud path is correct and the silent
path is exposed, in one specification.

Scored against the six, the four DEC-002 candidates do not rank the way the
three published acceptance-test axes rank them, and that disagreement is the
useful result. **Option 3 should be withdrawn rather than out-scored**, on four
grounds of which the strongest is that RFC 8785 §3.2.3 *prohibits* what
condition (5) requires while RFC 8949 §4.2.1 is merely *silent* — so what we
would need is a modification of JCS rather than a subset, and under R-O-03 a
modification is a partly invented algorithm. **Option 1 reaches uniqueness by
grammar rather than by algorithm** — two ABNF productions, no sort step, no
number algorithm — which is the smallest attack surface of any candidate; it
loses on data model and library availability, both named DEC-002 drivers.
**Option 5 must construct registry-freedom by subtraction.** Option 4 is
dominated on every axis.

One question was open in the source material and is now closed by experiment.
The falsifier — *if canonicality cannot be checked on decode without
re-encoding, the R-O-05 separation is cosmetic and DSSE is simply right* —
**did not fire**: single pass, no re-encoding, both surviving candidates, 60
fixtures of which 36 negative.

For DEC-004, §4 isolates the distinction the modern literature lost. SPKI's
`AIntersect` is a **closed binary operation on authorization tags**, so
authority forms a meet-semilattice and a chain of N certificates reduces to one
tuple. **No system in R-001's survey does this.** The 2026 agentic drafts have
independently reinvented most of SPKI's tag vocabulary while exposing only a
`subsumes` decision procedure — they are, in R-001's phrase, one `⊓` away.

---

## 1. Scope, and what this report must not do

**In scope.** The comparative anatomy of the mechanisms this project would
build on, and the assembled evidence for two open decisions: DEC-002 (the
concrete native encoding) and DEC-004 (the tag language).

**Out of scope, deliberately.** Adoption and uptake (R-0004). Historical
framing and the gap argument (R-0005). Cryptographic adequacy, which R-001
treats as settled — the signature is the solved part. And **any recommendation
that would amount to taking a decision**: §7 states what this report refuses to
recommend and why that refusal is substantive rather than procedural.

**A note on where the live evidence lives.** Most of what follows was produced
in the library, under topic `canonical-encoding`, and is recorded in three FX-1
extractions and a topic answer rather than in a report. That is by design —
`library/CLAUDE.md` holds the extraction bar and `ARCH-0001` §9.4 forbids
parallel architecture documents. The job here is to put it in front of a
reviewer in decision order, with the disagreements intact.

---

## 2. Four layers the field fuses

Before any candidate can be compared, the thing being compared has to be
separated from three neighbours it is routinely confused with. R-001 §11.3
identifies the conflations; this section names the layers.

| layer | question it answers | our decision | failure if fused |
|---|---|---|---|
| **Identifier** | how is a principal named on the wire? | **DEC-003** | a name that is not canonical is two names |
| **Encoding** | how does a logical value become bytes? | **DEC-002** | two values, one byte string, or the reverse |
| **Envelope** | what binds a signature to those bytes? | **DEC-005** | signed bytes ≠ verified bytes |
| **Vocabulary** | what do the fields *mean*, to a machine and a person? | **DEC-004**, **DEC-007** | an unknown term degrades to an opaque blob |

The field fuses these constantly, and two instances matter here.

**DSSE fuses envelope and encoding, then un-fuses them better than expected.**
Its stated objection to canonical forms is that canonicalisation forces a
verifier to parse untrusted input before authenticating it. PAE answers the
injectivity problem by **length-prefixed framing** rather than by
canonicalisation — no escaping, no ordering rule, no normalisation. That is a
second route to condition (1) below, and it is the route RFC 9804's verbatim
octet-string form takes too. Two specifications, thirty years apart, reaching
injectivity by framing instead of by algorithm, is a finding worth carrying
into D5.

**COSE fuses identifier and envelope.** `iss`/`sub` in CWT claims
[@rfc-8392; @rfc-9052] are envelope-level identifiers, which is exactly where
DEC-003 must not silently land.

The separation is not pedantry. `ARCH-0001` §4.3 keeps name resolution,
authorization reduction and statement acceptance as three procedures and
forbids collapsing them into one graph walk; the layer table is the same
discipline applied to the wire.

---

## 3. DEC-002 — the encoding

### 3.1 Why this is a security decision

The intuition that an encoding choice is a matter of ecosystem taste is wrong
for one reason: **determinism is not uniqueness.**

RFC 8949 §4.2's deterministic encoding is an **encoder-side** rule. A
conforming CBOR decoder accepts non-deterministic input happily, and nothing in
§4.2 obliges it to object. The library's FX-1 extraction of RFC 8949 enumerates
**fourteen decisions §4.2 leaves to the application**, each with a negative
fixture.

Two distinct things can go wrong, and the project needs both named because they
fail differently:

- **Signing.** Two byte strings that should be one. The producer's canonical
  form and the verifier's differ, and the signature fails to verify. **Loud.**
- **Naming.** One value with two canonical forms, under R-M-02 where a `KeyId`
  *is* the principal's name and under P4 where a domain of discourse is
  identified by the hash of a set. Two parties conclude they hold different
  vocabularies, or two distinct principals share one name. **Silent, and
  confidently wrong.**

That asymmetry organises everything below. It is also why the six conditions
split into two groups rather than forming one list.

### 3.2 The six conditions

From the `canonical-encoding` topic answer, in its numbering.

**Group A — safe to sign.**

1. The encoding is **injective** over the values it encodes, not merely
   deterministic.
2. The decoder **rejects** non-canonical input rather than normalising it.
3. Canonicalisation runs **once, at authoring**, on trusted input, and never as
   part of verification.
4. The encoding profile is named by an **authenticated type indicator** carried
   inside the signed bytes.

**Group B — safe to derive an identifier from.**

5. Set-valued fields carried in arrays have a **defined canonical order**.
6. Text that is load-bearing for identity has a declared **Unicode
   normalisation** rule, or an explicit refusal to normalise together with
   rejection of unnormalised input.

R-O-05, proposed in `ARCH-0001-PROPOSAL-v0.2.0` §3.4, delivers (3) and (4) and
**assumes** (1) and (2). Group B is reachable by no *candidate encoding*, and it
is not reachable by R-O-05 either, because at an identifier there are no
received bytes to verify verbatim. **The digest is produced by
canonicalising.** Group B therefore has to be supplied **above** the encoding,
by the data model — which is exactly what `SPEC-0003` §6 has since done for part
of (5), and §3.13 reads that result against this list.

> **Where conditions (2) and (5) stand after ADR-0003.** Condition (2) was
> routed to `ARCH-0002` **P5** rather than to a new `R-O-07`, on the grounds
> that P5 already binds encoder and verifier both. That clause has **not
> landed**: mofn#97 carries it as P5.1 in `ARCH-0002` v0.7.0 and is open, P5
> remains `[draft]`, and `ADR-0002` — the instrument that would make it
> normative — is `proposed`. Meanwhile `SPEC-0002` §4.3 and §13.1 **already
> require condition (2) normatively**, as a validating decoder that rejects and
> never repairs, under an ADR that is accepted. The principle is behind its own
> specification. That is §3.13's subject and it is the standing argument on
> mofn#97.

### 3.3 Condition (1), sharpened by an attack

The attack notebook attached to DSSE sharpens condition (1) in a way the topic
answer did not initially state. Lodato's September 2020 proof-of-concept is a
**polyglot payload**: injective within CBOR, injective within protobuf, and
ambiguous **across the pair** — with `payloadType` flipped after signing
because it sat outside the signature.

So condition (1) must hold over the **(profile, bytes) pair**, not over bytes
under one profile. Two consequences:

- the authenticated type indicator of condition (4) is **load-bearing**, not
  belt-and-braces; and
- **option 4 is the candidate most exposed to it**, because it has two live
  profiles by construction.

This notebook is the citation behind R-O-05's type-indicator clause and is its
ancestor in a literal sense.

### 3.4 Option 3 — withdraw rather than out-score

JSON with RFC 8785 JCS [@rfc-8785], DSSE for the signed form. Four grounds, in
descending force.

**(i) Condition (5): prohibited versus absent.** RFC 8949 §4.2.1 is **silent**
on array order, so a profile may add a bytewise rule without contradicting it.
RFC 8785 §3.2.3 **prohibits** reordering. The canonicalisation we need is
therefore a *modification* of JCS rather than a subset of it, and under R-O-03 —
*the canonicalization algorithm for each concrete encoding SHALL be cited, not
invented silently* — a modification is a partly invented algorithm. Scoping the
citation does not repair it.

**(ii) §5 mandates the ordering R-O-05 forbids.** Applications MUST parse and
check I-JSON, verify correctness and locate the signature property, and only
then verify the signature. Appendix F spells out the same scheme: parse, save
the signature value, **remove** the signature property, re-serialise,
re-canonicalise, then compare. Precision matters here and the extraction is
careful about it — Appendix F carries no BCP 14 keyword, so the contradiction
rests on §5 alone with Appendix F as the only worked description of what §5
means. JCS can be used producer-side only, and Appendix C licenses exactly
that; but Appendix C concedes it is the minority path, and once R-O-05 forces
the signature out of the payload, JCS does no work at verification time at all.
Its remaining job is identity derivation — the job it is worst at.

**(iii) The number algorithm is not in the cited document.** §3.2.2.3 says, in
the specification's own words, that *the algorithm itself is not included in
this document*, pointing instead at V8 and Ryu — two implementations. Citing
RFC 8785 means citing three artifacts, one an edition of an annually revised
standard. Citing RFC 8949 §4.2.1 means citing STD 94, complete in itself.

**(iv) The envelope reintroduces a global type identifier.** Weakened, and the
weakest of the four — see §5.1.

**The number problem is a constraint, not the disqualifier**, and an earlier
draft of the topic answer had that wrong. Threshold `k` and `n`, digests,
counters and `Validity` at second, millisecond or microsecond resolution all
fit inside IEEE 754 double precision; the ceiling falls between microsecond and
nanosecond time and nowhere else in our model. The real hazards are sharper and
sit elsewhere, and all three are in the specification's own appendices:

- Appendix B serialises the double at hex `4430000000000000` — exactly 2⁶⁸ — as
  `295147905179352830000`, **a different integer, silently, with a signature
  that verifies perfectly**, because the ±9007199254740991 range is only a
  SHOULD in Note (1).
- Appendix D's remedy of carrying such values as JSON strings is **itself not
  canonicalised**, and Appendix E's own worked example shows `"055"` becoming
  `"55"` and a timestamp gaining `.000` under a different parser style. That is
  condition (1) failing *inside the remedy*. The field the RFC uses to
  demonstrate it is named `time` — which is our `Validity`.
- Appendix B serialises both `0000000000000000` and `8000000000000000` as `0`,
  so positive and negative zero collapse.

**What is recorded in option 3's favour**, because an honest scoring says so:
it wins **namespace governance** outright — the criterion the v0.2.0 proposal
§3.3 records as never scored. JSON has no tag space and no header space, and
RFC 8785 §4 has no IANA actions. Where option 5 must *construct*
registry-freedom by subtraction, option 3 is registry-free by construction, and
P1's displacement of type identity is a no-op in JSON because there is no
encoding layer to move it out of. It also removes five of RFC 8949's fourteen
determinism rows. **That belongs in the D5 package whichever way the decision
goes.**

One earlier claim is **withdrawn**: JCS does not leave a duplicate-key hole.
§3.1 requires I-JSON, under which duplicate property names MUST NOT appear, so
JCS closes it by constraining input. The residual problem is narrower — §5
mandates a duplicate check that Appendix A's reference canonicaliser is
structurally incapable of performing, because by the time it runs the parser
has already collapsed duplicates and destroyed the evidence.

### 3.5 Option 1 — scored late, and it changed two claims

Canonical S-expressions (RFC 9804) as canonical; JSON as diagnostic. RFC 9804
reached full FX-1 extraction on **2026-10-04**, which removed the blocker the
topic answer had named. Condition by condition:

| # | condition | RFC 9804 |
|---|---|---|
| 1 | injective | **Yes at its own layer, with one crack** |
| 2 | decoder rejects | **Mechanism yes — better than any candidate's — obligation no** |
| 3 | no canonicalisation at verification | **Compatible; the document is silent, and on ordering, silence is permission** |
| 4 | authenticated type indicator | **Not supplied, and the obvious substitute is explicitly disqualified** |
| 5 | canonical order for sets | **Not supplied, but silent rather than prohibiting** |
| 6 | Unicode normalisation | **No rule, but no place for a normaliser to hide** |

Three of those deserve the detail.

**Uniqueness by grammar, not by algorithm (condition 1).** §6.2 asserts
uniqueness directly, and the mechanism is **subtraction**: every octet-string
in verbatim mode, every list with no separating blanks. That collapses the five
octet-string representations of §4 to one and deletes every optional length
prefix, whitespace allowance and padding choice at a stroke. There is no
sorting step, no normalisation step and no number algorithm. Compare: RFC
8785's uniqueness depends on the ECMAScript `Number::toString` algorithm the
document does not include, plus a UTF-16 code-unit sort; RFC 8949 §4.2's
determinism depends on encoder-side rules about integer head length, map key
order and float shortening. **RFC 9804's canonical form depends on a grammar of
two productions.** It is the smallest attack surface of the three by a wide
margin.

**The crack is on the identity path.** §4.6 says an octet-string with no
display-hint *may be considered to have* a default media type, and that the
default is neither written out nor stripped; §4.7 then makes the hint part of
equality. So an octet-string written with an explicit
`[24:application/octet-stream]` hint and the same octet-string written with no
hint are the *same value* to an application applying the default, and have
**different canonical forms**, hence different digests. Injectivity holds in
the signing direction and fails in the naming direction — §3.1's asymmetry
reappearing in option 1 from a different cause. It is cheap to close with one
profile rule (never write a hint equal to the profile default) and RFC 9804 §8
already sanctions application-level restrictions; but **it must be closed
explicitly, and the source does not close it.**

**Condition (2): the mechanism is published as a grammar.** §7.2 gives the
canonical form its *own* ABNF, separate from the advanced one — two productions.
A decoder implementing `c-sexp` and not `sexp` rejects non-canonical input **by
construction**: not normalising and comparing, simply failing to parse. The
obligation, though, is absent — §6 requires an implementation to support basic
transport too, which is an alternation including a brace-wrapped base-64 form,
and the document never says which to use when. So a conforming implementation
**must** accept `{KDE6YTE6YjE6Yyk=}` wherever it accepts `(1:a1:b1:c)`.
Condition (2) is available to a profile that states it and is not supplied by
the document — the same shape as P5 above, and it routes there the same way.

**Condition (4) has a trap that will be proposed.** §11 reads in full *"This
document has no IANA actions"* — no version field, no media type, no magic
number, no envelope. The tempting substitute is the display-hint, since it is
the only modifier an octet-string carries and is inside the canonical bytes.
**§4.6 forecloses it:** the hint *"has no other function"* than display. Using
it for type would be the silent reinterpretation R-O-03 exists to prevent.
What is left is a convention — a distinguished first element of the outer list
— which is registry-free and accommodates R-M-12's key-relative requirement
directly.

**Two findings from option 1 change claims made earlier in the topic answer,
and both are recorded against our own prior position.**

1. **Condition (5) is not a discriminator between DEC-002 options.** Every
   candidate is silent on canonical order for set-valued fields *except option
   3, which prohibits it.* The gap is real and is ours to close under any
   option; what distinguishes option 3 is not that it lacks the rule but that
   it forbids one.
2. **The single criterion recorded as option 3's outright win — namespace
   governance — option 1 also wins**, by the same argument and without paying
   option 3's §5 cost.

**Two things stop that being a conclusion**, and both are named DEC-002
drivers. The data model is far poorer — octet-strings and lists only, no
integers, maps, booleans or null — so **every** `ARCH-0001` §4 logical type
needs an application-level mapping in which injectivity must be re-established
by hand, field by field, with no help from the format. Option 1 *moves* the
hard part rather than removing it. And **library availability is its weakest
axis**, thin above the parser layer.

### 3.6 Option 5 — registry-freedom by subtraction

CBOR data model, no IANA tags, COSE as export only; type identity is
`(defining key, label)` per P1; YAML as the human form with a canonical one-way
mapping.

The cheapest route to condition (1) here is **exclusion rather than harder
canonicalisation**, and the `rcbor` spike demonstrates it: no floats, no tags,
definite lengths only, smallest-form integer heads, map keys sorted bytewise on
their **encoded** form per §4.2.1, duplicate encoded keys rejected rather than
resolved. The cost is expressiveness — a decimal must travel as an integer or a
string.

**Exclusion does not reach conditions (5) or (6)**, which are additions rather
than removals, and that asymmetry is worth naming: a reduced profile buys
signing safety by deleting cases and **cannot buy naming safety the same way.**

Three defects in the spike are evidence for the identity-path gap rather than
incidental bugs, and they are recorded because each maps to an open decision:

- `keyid()` hashes the key bytes it is handed **with no canonical encoding
  step**, so DEC-003's requirement to specify canonical key bytes before
  hashing is unsatisfied in the only code that exists — and the demo hides it
  because its keys are literal byte strings;
- every identifier is truncated to 128 bits, roughly a 2⁶⁴ birthday bound for
  something that functions as a **name** under R-M-02;
- the envelope type indicator is a global string naming the rcbor statement
  profile, which is **R-M-12-non-conformant**.

### 3.7 Option 4 — dominated

Dual canonical with a documented bijection. Library availability is nominally
the union and therefore the best, but it requires both toolchains **plus the
bijection**, which no ecosystem supplies and which would be written and
maintained here. The type indicator is the worst position of the four, because
with two live profiles the indicator must be injective over the (profile,
bytes) **pair** — which is §3.3's attack exactly. And a bijection between a
specification that *prohibits* array reordering and one that is *silent* on it
has to pick a side on condition (5) and therefore cannot be faithful to both.

### 3.8 The two rankings disagree, and that is the useful result

DEC-002's own acceptance test names three axes among its criteria: library
availability, a native authenticated type indicator, and canonicalisation
idempotence.

| | library availability | type indicator | idempotence |
|---|---|---|---|
| **Option 1** | **worst** | cheap — a list element, registry-free | **wins** |
| **Option 2 / 5** | **best** | must be constructed by subtraction | good |
| **Option 3** | rich | comes from the envelope, PAE-authenticated | **idempotent but lossy — see below** |
| **Option 4** | nominally union, really neither | **worst** — injective over the pair | per-side, plus cross-form stability |

**Idempotence misleads on option 3 and the answer has to be precise. JCS *is*
idempotent**: run it on its own output and nothing changes. What fails is
**injectivity, on the first pass** — §3.4's 2⁶⁸ example, the ±0 collapse, the
`"055"` → `"55"` drift inside the remedy. Stable on re-application, lossy on
application. For condition (1) that is **worse than non-idempotence would be,
because non-idempotence is loud and lossiness is silent.**

**The ranking the three axes produce is not the ranking the six conditions
produce.** Option 1 wins idempotence and the type indicator cheaply and loses
library availability badly; options 2 and 5 win library availability outright
and must construct the indicator; option 3 is ecosystem-rich and registry-free
and is the only candidate that prohibits what condition (5) needs. DEC-002's
driver list **includes** library availability, so the axis option 1 loses is a
named driver and not a detail.

### 3.9 Where this leaves the narrowing — overtaken, not resolved

Three human decisions bear on the scoring above, and as of 2026-10-14 the third
has changed what the other two mean.

| | what it did | when |
|---|---|---|
| sponsor correction | RFC 9804 recorded as *historical*, option 1 as *not a contender*; folded into `PLAN-0001` §13 | **2026-09-16** |
| **MD-3** | narrowed DEC-002 to option 5, retaining option 2 as the comparison fixture — **a narrowing, not an acceptance** | **2026-09-28** |
| **`ADR-0003` D2** | **accepted**: one canonical encoding for every hashed or signed object, and it is the deterministic CBOR profile of FKSA suite 1, *"which is MD-3's option 5"* | **2026-10-14** |

The evidence in §3.4–§3.8 postdates the first two — RFC 9804 reached FX-1 on
**2026-10-04** and the topic closed on **2026-10-08** — and it predates the
third.

**D2 is an acceptance and the earlier two were not.** `ADR-0003` is
`status: accepted` with a sponsor in `decision_makers`, which is the instrument
`ARCH-0001` §9.2 requires and the thing MD-3 never was. Its `version_policy` is
that *"an accepted ADR changes only by superseding it."*

**And D2 still does not accept DEC-002.** It says so in the decision row: *"This
ADR does not accept DEC-002; the DEC-002 ADR and its fixtures still decide
it."* The two statements are consistent and a reader must not collapse them:

- **fixed** — what the KSA core encodes with, for statements and definitions
  alike, now written out as bytes in `SPEC-0002` §4 with vectors behind it;
- **open** — DEC-002 itself, whose acceptance test is three round-trip fixtures
  and whose ADR is still owed (`DECISIONS-0001` Tier 1 item 4b, **Oct 28**).

#### What that does to the question this section used to ask

The honest question in v0.1.0 was *does "historical" describe the document's
status or the encoding's fitness?*, and the honest answer now is that **it has
been overtaken rather than answered.** D2 selected CBOR, but it did not select
it by scoring: it selected it by **adopting a core protocol that already
existed, was implemented, and had a reference verifier** (`ADR-0003` Context).
That is an integration argument, and integration arguments are not weaker than
fitness arguments — they are *about a different thing*. Nothing in §3.4–§3.8
was weighed in reaching it, and nothing in §3.4–§3.8 contradicts it, because the
six conditions rank *encodings* and D2 ranked *a core to build on*.

Two consequences follow, and the report states them rather than acting on them.

**The widening request on mofn#8 has changed in kind.** Before 10-14 it asked a
sponsor to widen a scoring set from two to three. After 10-14 the same request
asks to supersede an accepted ADR, which is a materially larger thing and a
different conversation. **This report does not recommend it**, does not reopen
D2, and notes only that whoever answers mofn#8 should be told that the bar
moved, because the issue text predates the ADR and still reads as the smaller
ask.

**The residue of the scoring is no longer comparative.** What survives is not
*which option* but **what option 5 must construct that option 1 would have got
from its grammar** — §3.6 and §3.10 — and those are now **work items against a
fixed encoding**, not arguments against a candidate. §3.13 is the first instalment
of that list.

### 3.10 The falsifier, and the experiment that settled it

The topic answer recorded a falsifier against its own position:

> If checking canonicality on decode cannot be done without re-encoding, then
> condition (2) drags the canonicaliser of the producer back into the verifier,
> the R-O-05 separation is cosmetic, and DSSE is simply right — meaning abandon
> canonical form, sign received bytes, and identify subjects by content digest
> only.

**It did not fire** (mofn#73, `design-log/0007-rejecting-decoder-spike/`).
Canonicality is decidable by parsing alone, for both candidates, with no
re-encoding and no second pass: 60 fixtures, 36 of them negative, every
accepted input read exactly once front to back.

The finding worth carrying is that RFC 8949 §4.2.1's *"order map keys by their
encoded bytes"* reads like a property only an encoder can know, and is not —
the decoder is already looking at exactly those bytes, so the check is a
bytewise comparison of two buffer slices. **The producer sorted on exactly the
bytes the consumer is looking at.** Two things fall out: strictly-ascending
comparison enforces ordering and duplicate rejection in one test, so duplicate
keys are free; and smallest-form head checking is purely local, living in one
function where no call site can forget it.

**But the options differ in kind, not only in cost**, and this is the sharpest
discriminator the spike produced. Option 1's equivalent of smallest-form is
**in the grammar** — `03:abc` is *ungrammatical*, not non-canonical, so there
is no code path in which the rule is separable from parsing and a conforming
reader cannot omit it. Option 5's equivalent is a rule the implementation must
state and check; an implementation that omits it still parses every valid
document. This is why `ARCH-0002` P5.1 is load-bearing under option 5 and
redundant under option 1.

**`ADR-0003` D2 spent that conditional.** With the CBOR profile fixed, P5.1 is
load-bearing — not conditionally so — and `SPEC-0002` §4.3 has already written
the rule out: seven enumerated rejections and *"Rejection MUST NOT be replaced
by repair: a decoder MUST NOT re-sort, re-encode or otherwise normalise and then
accept."* The specification cites this spike for the single-pass claim. So the
clause mofn#97 is trying to add to the principle is **already normative in the
specification that derives from it**, which inverts the usual order and is the
sharpest form of that PR's case.

**What parsing cannot decide**, recorded as a limit rather than a gap: option
1's default display-hint crack (§3.5), and condition (6), where NFC and NFD
spellings are both valid UTF-8 and both canonical. Both sit on the **identity**
path — the asymmetry predicted in §3.1, confirmed by experiment.

### 3.11 Condition (6), and the incident that is not theoretical

Under P1 a type is a `(defining key, label)` pair, and under R-M-02 a `KeyId`
is a name — so text is load-bearing for identity in this design in a way it is
not in most. RFC 8949 §5.6.1 compares text byte by byte and §3.1 requires UTF-8
while saying nothing about normalisation form.

RFC 8785 §3.1 is better here in one respect — it closes the ambiguity by
requiring that components preserve Unicode string data as is — and worse in
two: that MUST binds parties we do not control and is unenforceable, and it
forecloses normalising at canonicalisation time, leaving only
normalise-at-authoring plus reject-at-decode as a citation-compatible route.

**The hazard is documented, not hypothetical.** Transcribing the
`canonical-encoding` record's own test vectors corrupted **U+FB33 HEBREW LETTER
DALET WITH DAGESH**, which has a canonical decomposition that an ordinary
normalising layer applies silently. Any JCS pipeline containing such a layer
breaks signatures on exactly that input.

Option 1 has a structural property here that neither JSON nor CBOR has:
**RFC 9804 has no text type.** An octet-string is octets; whether it *consists
of text* is an application claim the format never inspects, and the extraction's
R-0010 — *"No escape sequences are interpreted in the octet-string"* — gives a
conforming parser no licence to touch a byte. So there is no string-processing stage
for such a layer to inhabit. The hazard is not ruled out — an application can
still hand the encoder differently-normalised bytes — but it is **pushed up to
the application boundary, where it is visible, instead of hiding in the
serialiser.**

### 3.12 What remains genuinely open on DEC-002

- **Condition (6) is half-supplied and the other half is unenforceable.**
  `SPEC-0002` §4.1 takes the *explicit refusal to normalise* branch in terms —
  text is *"Preserved byte-exact; MUST NOT be normalised (no Unicode
  normalisation, no case folding, no whitespace trimming) by any producer or
  verifier"* — which is more than RFC 8949 says. What it cannot supply is the
  companion clause, rejection of unnormalised input, because NFC and NFD are
  both valid UTF-8 and §4.3 has no test that separates them (§3.13).
- **Condition (5) is no longer unsupplied — but it was supplied above the
  encoding, and only in part.** `SPEC-0003` §6 gives every base kind a canonical
  range order and §13.4 states the property (5) asks for. The three arrays that
  are semantically *sets* at the statement layer did not get the same treatment.
  **§3.13** is that finding and it is the main new material in v0.2.0.
- **Condition (5) depends on P4** and on `Threshold` members being a set rather
  than a sequence. P4 is **held** (MD-2), and `SPEC-0002` §8.6 has since
  encoded the threshold member list as `[2* kid]` — an array, which is to say a
  **sequence** (§3.13). Dropping P4 would shrink the answer to four conditions
  and restore option 3 to contention — so whoever takes DEC-002 takes a
  position on P4 whether or not they say so (`ADR-0002` §4).
- **Prior art for condition (5) exists and is deliberately unread.** RDF Canon
  1.0 canonicalises RDF *datasets* — unordered sets of triples — so it is not a
  DEC-002 candidate for our tree-shaped statements and cannot become one. But
  it is plausibly the one ratified algorithm for canonically ordering a set,
  including the hard blank-node case. **The claim that no candidate supplies
  condition (5) is scoped to the DEC-002 candidates and is not a claim about
  the state of the art.** library#56 owns reading it.
- **The round-trip fixtures now partly exist, and the gap in them is the
  case §5.1 warned about.** `spec/vectors/ksa-core/` carries one definition vector,
  eight statement vectors and six negative vectors, generated and
  double-encoded against an independent encoder, under D2's encoding. Against DEC-002's acceptance test — `NameCert`,
  `AuthzCert` *with a threshold subject*, `ArtifactStatement` — TV-1/TV-2 cover
  the name-binding shape, TV-4 attests about an artifact digest, and TV-5 is a
  delegating `trust` with range constraints. **There is no vector anywhere in
  the set with a threshold subject**, though `SPEC-0002` §8.6 specifies the
  form. These are also not *round-trip* fixtures: they are produce-and-verify
  vectors, and T-034's idempotence and round-trip tests remain `todo`. D5 is
  due **Oct 28**.


### 3.13 Conditions (5) and (6) in the accepted core

New in v0.2.0. `ADR-0003` did not arrive alone: it brought `SPEC-0002` and
`SPEC-0003`, which are the first documents of ours to write Group B's subject
matter down as bytes. Read against §3.2's list, they do three things — one
better than this report predicted, one exactly as predicted, and one that is a
gap worth a reviewer's attention.

#### (5) was supplied, and not by the encoding

§3.2 as first written said Group B *"is reachable by no candidate"*, and §3.12
in v0.1.0 said *"no decoder can supply (5)"*. Both remain true of encodings and
both were the wrong place to look. `SPEC-0003` §6 gives **every base kind its
own canonical range order**, each stated in that kind's own terms: enum ranges
in the order the type's `values` declares them; text ranges *"distinct … sorted
in bytewise order"*; key and digest ranges distinct and sorted; dns-name,
ip-prefix and email ranges sorted with no pattern within another; boolean ranges
with `false` first. §13.4 then states the property condition (5) asks for, in
almost its words: *"Ranges have exactly one encoding (§6), so two statements
scoping the same set have the same bytes."*

Eleven base kinds. **Eight** of them — codes 1, 3, 4, 5, 6, 7, 8 and 11 — have
ranges that are *sets written as arrays*, and **all eight were given an order**.
Two more, integer and time, are ordered pairs where the question does not arise;
the eleventh, `record`, has no range at all. **That is condition (5),
discharged at the data-model layer, by hand.** It confirms §3.2's framing — Group B is *"additions, not
subtractions"* — by showing what the addition costs: not one algorithm but a
rule per kind, each of which can be got wrong independently, and none of which a
decoder enforces.

#### The same discipline was not carried up to the sets above the ranges

Three fields are semantically sets, are encoded as arrays, and have **no
distinctness rule and no order rule** anywhere:

| field | where | what the document calls it |
|---|---|---|
| `trusts: [2* kid]` | `SPEC-0002` §8.6, the threshold form of `trust` | a **set** — `SPEC-0004` §6.4: *"trusts a set `M` of keys"*, *"Distinctness is by kid."* |
| `about: [+ attribute-range]` | `SPEC-0002` §8.6, every `trust` statement | the scope; §6.3 quantifies over it as *"every attribute range in `s.about`"* |
| `may-delegate.ranges`, `.allow-keys`, `.exclude-keys` | `SPEC-0002` §8.6 | allow-lists and deny-lists — sets by construction |

`SPEC-0002` §4.1 is explicit that for an **array**, *"order is significant and
signed"*, and §4.5 makes the statement digest SHA-256 of the TBS. Put together:

> **One semantic trust statement has as many statement digests as its member
> list has permutations.** Two wallets that trust the same three keys with
> threshold 2, about the same scope, and that list them in different orders,
> produce statements that are byte-distinct, digest-distinct, and — to anything
> that names statements by digest — two different statements.

`SPEC-0003` kind 7 already has the rule this needs, one document away: *"an
array of distinct kids, sorted."* It is simply not invoked by §8.6.

The consequences are on the identity path, which is the asymmetry §3.1 predicted
and the reason this report separates the two groups at all:

- **`revoke` names its target by digest** (`SPEC-0002` §8.7) and only the
  speaker may revoke. A speaker who re-serialises a statement in a different
  member order and revokes *that* digest has revoked nothing.
- **`review` and `approve` target `[3, statement-digest]`** (§8.1). A panel
  under `SPEC-0005` counts approvals over cited inputs; two members citing two
  permutations of one statement cite two objects.
- **Deduplication of a statement set** is by digest, so the same statement
  arrives twice and counts twice.

**Trust evaluation itself is safe, and that is the instructive part.**
`SPEC-0004` §6.3 compares ranges with **within**, never with bytes, exactly as
`SPEC-0003` §13.4 instructs — *"narrowing is decided by the base kind's rules,
never by comparing bytes."* So the evaluator is order-independent while the
identifier is not. **Loud path correct, silent path exposed**, in one
specification, which is §3.1 confirmed rather than argued.

**One place in evaluation does compare for equality, and it is undefined.**
`SPEC-0004` §6.4 requires, for onward delegation from a threshold set, *"`n`
distinct members each to have issued a trust statement to the same key with
identical `about` and `may-delegate`"*. **`identical` is not defined.** If it means byte
equality, the permutation problem blocks delegations that semantically agree; if
it means semantic equality, no document says what semantic equality of an
unordered collection of attribute-ranges is — and §6.3's `within` gives mutual
containment, not identity. This is the only equality comparison in `SPEC-0004`
and it is the one the rest of the document is careful to avoid.

#### (6): the refusal was taken, the enforcement cannot be

`SPEC-0002` §4.1 closes §3.11's ambiguity in the strongest available form —
*"MUST NOT be normalised … by any producer or verifier"*. That is condition
(6)'s second branch, taken explicitly, and it is more than RFC 8949 offered.

It is also, precisely, **the clause §3.11 criticised RFC 8785 §3.1 for.** The
criticism was that such a MUST *"binds parties we do not control and is
unenforceable"*, and that is now equally true of our own specification: NFC and
NFD spellings are both valid UTF-8, both canonical KSA-CBOR, and §4.3 has no
test that distinguishes them. The report should say so about its own project's
document, having said it about someone else's. The U+FB33 corruption in §3.11
would survive every check in `SPEC-0002`.

What this does *not* mean is that the two are equally placed. §3.11's third
route — **normalise at authoring, reject at decode** — is still open to us and
is closed to JCS, because `SPEC-0003` could declare a normalisation form for the
labels and language tags that are load-bearing for identity under P1, and §4.3
could then test it. Nobody has proposed that. It is listed in §8.

#### What a reviewer should take from this section

Not that the specifications are wrong. `SPEC-0003` §6 is the best treatment
condition (5) has had anywhere in this project, and §13.4 shows it was
deliberate. The finding is that **the discipline stopped one layer below where
the identifiers are**, and that the one field the specification itself calls a
*set* is the one field with no ordering rule. It is a short fix — invoke kind
7's rule on `trusts`, state an order for `about` — and it is a
`SPEC-0002`-layer fix, not a DEC-002 one. **This report does not propose the
diff**; `ARCH-0001` §9.4 and `CLAUDE.md` route that through a proposal against
the document, and it is filed as an open item in §8 instead.

---

## 4. DEC-004 — the tag language

### 4.1 The distinction the modern field lost

SPKI [@rfc-2693] does something no system in R-001's survey does. Its §6.3
reduction composes two 5-tuples into one, and `AIntersect` is a **closed binary
operation on authorization tags** — the intersection of two authorizations is
itself an authorization of the same kind, computed element-wise over `(*)`,
`(* set …)`, `(* prefix …)`, `(* range …)` forms.

Two consequences, and both are architectural rather than cosmetic:

1. **Authority forms a meet-semilattice with a computable meet.**
2. **A chain of N certificates reduces to a single 5-tuple.** The chain is
   evidence, not payload.

Every modern system instead **accumulates, then checks containment**:

| system | attenuation operation | verification |
|---|---|---|
| Macaroons [@macaroons-2014] | append caveat, re-chain HMAC | evaluate conjunction of predicates against request |
| Biscuit [@biscuit-spec-3-3] | append signed block of Datalog checks | run all checks plus authorizer policies |
| UCAN [@ucan-1-0] | new delegation referencing parent proof | command-path containment at execution |
| Attenuating-token draft [@draft-niyikiza-oauth-attenuating-agent-tokens] | derive token with narrower constraint map | normative `subsumes` per constraint type |
| WIMSE draft [@draft-asor-wimse-agent-delegation-chain] | new hop | scope covered, bounds tighter, expiry ≤, depth ≤ |
| **SPKI** | **intersect tags** | **reduce chain to one tuple** |

### 4.2 Why the field abandoned the meet — and it was not oversight

A **semantic shift**, and getting this right matters because it determines
whether the meet is recoverable.

SPKI tags describe a **static permission space**, closed under meet.
Macaroon-style caveats describe a **dynamic admissibility predicate over
request context**: `time < T`, `ip = …`, or a third-party discharge obligation.
You cannot intersect *"holder proves membership in group G at service A"* into
a tag, because it is not a tag — it is **deferred evidence**. Once caveats are
arbitrary predicates, the meet degenerates to conjunction, and conjunction has
no normal form.

Biscuit makes this maximally explicit: a Datalog program's authority is defined
only extensionally, relative to an authorizer's facts. You can ask *is this
request permitted?* but not *what does this token authorize?* — a question SPKI
could answer in closed form.

**The price is paid in two places.** In **size**: monotone growth versus SPKI's
compression to a single tuple. And in **static analysis**: no offline *"is
token A weaker than token B?"* without a solver.

### 4.3 The 2026 drafts are one `⊓` away

The attenuating-token draft [@draft-niyikiza-oauth-attenuating-agent-tokens] is
worth singling out because it **independently reinvents most of SPKI's tag
algebra**. Its constraint vocabulary — `exact`, `range`, `one_of`,
`not_one_of`, `contains`, `subset`, `wildcard`, `all`, `any` — is close to
isomorphic to SPKI's `*`-forms, and it imposes a decidability requirement on
extensions.

But its normative primitive is `subsumes(C, P)`: a **decision procedure**, not
a **meet** computing `C ⊓ P`. The partial order is there; the lattice operation
is not exposed. R-001 §9.3 judges that a real, implementable gap — on that
constraint fragment the meet *is* computable, and computing it would let a
chain collapse to one normalised token.

Note the citation pattern, because it is evidence about how much of SPKI
survived as *knowledge* rather than as *deployment*: the attenuating-token
draft cites Dennis and Van Horn [@dennis-vanhorn-1966] and macaroons but **not
SPKI**; the WIMSE draft [@draft-asor-wimse-agent-delegation-chain] cites SPKI
only as a *"historical standards-track ancestor."*

### 4.4 What this means for DEC-004

`ARCH-0001` frames DEC-004 as a choice among three options — SPKI tag
S-expressions as-is, constrained JSON tags with an explicit ∩ operator, or a
small embedded policy subset. `ARCH-0002` **P7** reframes the question and is
**held** (MD-2): the question is not *which tag language* but *what must a
profile specify, and what is the minimum profile?*

The evidence above supports that reframing without settling it, and yields four
things a profile must name:

| | what a profile must specify | requirement it serves |
|---|---|---|
| tag/label types in use | drawn from a domain of discourse | P4 (**held**) |
| intersection semantics **per type** | — | **R-M-08**, which already requires this per profile |
| required verifier behaviour | what must be understood | **P5**, plus P5.1 once mofn#97 lands (§3.2) |
| rendering | the human-readable form | P3, **DEC-007** (open) |

Two findings bear directly on the minimum profile.

**The hybrid question is open and is the interesting one.** R-001 §12 problem 2
asks whether a tag fragment closed under meet, normalised at each hop, plus an
uninterpreted predicate residue that accumulates, is constructible. The
obstacle is real — third-party caveats and Datalog checks are deferred
evidence, not tags. **The 2026 attenuating-token draft is one `⊓` away from
testing it.** If the answer is yes, DEC-004 is not a choice between SPKI's
algebra and the modern family but a composition of both; if no, it is a choice,
and the project should say which it took and what it gave up.

**`ARCH-0001` already provides the escape hatch, and it is the right one.**
DEC-004 records that v0.1 may ship **tag as opaque byte string** plus one
profile (`urn:…:tag:bytes-equal`), so reduction can be implemented before the
language is rich. That is the D6 demo floor's actual dependency, and it means
**DEC-004 does not block Nov 11** — which §6 returns to.

### 4.5 Naming is not optional, and that is a DEC-004 finding

R-001 §9.4 asks whether the capability family's refusal to name subjects is a
feature or a gap, and reaches an answer this project should adopt consciously
because it is the argument for its own two-layer shape.

**The case for a feature** is the original one: the confused deputy
[@hardy-1988-confused-deputy] is fixed by designating authority *with* the
request, not by asking the deputy who it is. Unnamed keys also give privacy,
offline verification and clean composition.

**The case for a gap** is that four things the deployed world wants turn out to
be naming problems in disguise. **Revocation** — you cannot revoke an authority
you cannot name. **Rotation** — a key is not a stable identity; `did:key`
[@did-key-method] is honest that purely generative identifiers cannot be
updated or deactivated. **Accountability and audit** — the entire 2026 agentic
literature is about showing an auditor which human sits at the root of a chain,
and a chain of ephemeral keys cannot answer that. **Organisational policy** —
*"anyone in group G"* is inexpressible over raw keys; macaroons smuggle it back
via third-party caveats, Biscuit via authorizer-supplied facts.

R-001's assessment is that the omission is an **unbundling, not a flaw in the
capability model** — but an unbundling the ecosystem has not re-bundled, and
the 2026 drafts are where the bill is coming due. SPKI had two layers,
authorization over keys and SDSI name certificates resolving local names, with
names usable as subjects in authorization tuples; the modern family collapsed
to one and is rediscovering the need under the banner of provenance.

**That is the direct argument for `ARCH-0001` R-M-04** — name bindings and
authorization bindings SHALL be distinct object kinds — and it is why DEC-004
cannot be settled as a pure capability-token question.

---

## 5. Where the two decisions touch

### 5.1 DSSE, read in full, moved two claims

Two results from reading the envelope [@secure-systems-lab-dsse] at the pinned
commit, both recorded against earlier positions of our own.

**Withdrawn: the `(t, n)` envelope does not carry threshold semantics.** The
sentence previously relied on continues *"where t is application-specific"* — so
`t` is a **verifier-side parameter supplied out of band, not a field**. The
schema carries only `payload`, `payloadType` and `signatures`, and the
specification adds that multiple signatures are *"equivalent to separate
envelopes with individual signatures."*

**A DSSE envelope carries `n` and cannot carry `k`.** Two consequences, and the
second is worse than the first. R-M-06's interchange story is exactly as
expensive as it looked: under **every** DEC-002 option, `k` and the member set
must travel **inside the signed payload**. And because the envelope is declared
equivalent to separate envelopes, an intermediary may legitimately split or
merge them — so threshold meaning inferred from signature count is not merely
absent but **unsafe to infer**.

**Weakened: option 3's fourth ground.** `payloadType` is only RECOMMENDED to be
a media type or URI — a SHOULD — and the specification explicitly licenses
coding it *"as a shorter string or enum"*, which PAE authenticates just as
well. DSSE does not **force** a centrally allocated identifier; its default
recommends one, and the cost of declining is ecosystem divergence rather than
non-conformance. The ground survives as the weakest of the four rather than
falling.

### 5.2 Two collisions that are quiet, not loud

**P5 versus DSSE's ignore-unknown default.** DSSE requires consumers to *"MUST
ignore unrecognized fields"* — the opposite default to `ARCH-0002` P5's
reject-unknown. The collision is at the **envelope layer only**: unsupported
payload *types* are rejected, and the payload interior is ours to govern.
**Proposed** as **P5.2** in mofn#97 (`ARCH-0002` v0.7.0, still open) — import
rejects, export emits none — and that resolution is reasoned entirely from DSSE
while **DEC-005 is open**, so it is owed a redo against COSE `crit` if COSE is
chosen. It has not landed; v0.1.0 of this report said it had, which was wrong on
two counts, since `ARCH-0002` v0.6.0 on `main` is an unrelated revision carrying
`ARCH-0003`'s cross-references.

> **And DEC-005's ground has shifted under both.** `ADR-0003` took FKSA's
> envelope: `SPEC-0002` §5 is a four-or-five element KSA-CBOR array
> `[suite, says, tbs, sig, ? pub]`, which is **neither DSSE nor COSE_Sign1**.
> DEC-005 as written in `ARCH-0001` offers exactly those two. So the KSA core
> now has a settled envelope while the decision that was supposed to choose one
> is still listed open — and `ADR-0003` says nothing about DEC-005, where for
> DEC-002 it was careful to say it was not accepting it. **Two readings are
> available** — that `SPEC-0002` §5 answers DEC-005 and the register has not
> caught up, or that DEC-005 was only ever about the *export* profile for
> `ArtifactStatement` and is untouched — and this report cannot pick between
> them, because the difference is what a human meant. It is in §8 for whoever
> owns the register. Until it is settled, the analysis in this section is about
> an **export target**, not about our own envelope.

**`KEYID` versus `KeyId`.** DSSE's `KEYID` is unauthenticated and *"MUST NOT be
used for security decisions"* — the exact opposite of our `KeyId`, which under
R-M-02 **is** the principal's name. The terms collide and the failure is quiet:
a mapping table written under R-I-01 that lines the two up because they share a
name would put the principal's name in the one envelope field DSSE forbids
relying on. **The rule for any export profile is that the principal travels in
the payload, never in `signatures[].keyid`.** This is a DEC-003 finding that
arrived from a DEC-005 document, which is itself an argument for §2's layer
table.

---

## 6. What is on the critical path, and what is not

Stated because the scoring above can make everything look blocking. Revised for
`ADR-0003`, which moved three of the four rows.

| | blocked by | due |
|---|---|---|
| **D5** DEC-002 package | **no longer the fixtures.** `spec/vectors/ksa-core/` supplies the encoding's vectors; what is missing is the **threshold-subject** case (§3.12), the round-trip and idempotence tests (T-034), and the ADR itself (T-033) | **Oct 28** |
| **D4** WP1 schema | **nothing, and it has largely been delivered** — `SPEC-0003` §5 is the typed data model WP1 asked for, no longer encoding-neutral but against a fixed encoding | Oct 21 |
| **D6** reduction + vectors | **not DEC-004** — the opaque-tag profile is sufficient. `SPEC-0004` §6 now specifies path-following, so the reduction has a normative target | **Nov 11, the floor** |
| **D7** mappings | DEC-005's status is now itself unclear (§5.2); R-I-01 table owes two rows | Nov 25 |

**DEC-004 still does not block the demo floor** and DEC-002 still does not block
WP1. What has changed is the character of D5's dependency. In v0.1.0 it was *"a
dependency on work nobody has started rather than on a decision nobody has
taken"*; the work has now started, from a different direction, and the residual
dependency is narrower and more specific:

- the **threshold subject** — specified in `SPEC-0002` §8.6, unvectored, and
  the one shape §5.1 names as where a specification reading was already wrong
  once;
- the **set-ordering question** of §3.13, which the acceptance test's
  `AuthzCert`-with-threshold fixture would have surfaced immediately, because
  building it forces someone to decide what order the members go in;
- the **ADR** (T-033), which `ADR-0003` D2 explicitly leaves owed.

Those three are the same item seen from three sides, and the fixture is the
cheapest way to reach all of them.

---

## 7. What this report refuses to recommend, and why

The refusal is substantive, not procedural.

**It does not pick a DEC-002 option**, and after `ADR-0003` D2 it does not
treat the encoding as picked either (§3.9). Not because an agent may not —
though `CLAUDE.md` is explicit that it may not — but because the scoring above
genuinely does not produce one. The six conditions and the three acceptance
axes rank the candidates differently (§3.8), the two criteria that go against
option 1 are ones no fixture will change, and the two conditions nobody
satisfies depend on a principle that is held (§3.12). A recommendation drawn
from that material would be a preference wearing a table.

**It does not pick a DEC-004 option**, because §4.4's reframing is the live
question and P7 is held. The useful output is the list of what a profile must
specify, not a choice among three languages.

**It does not treat the D5 fixtures as a formality.** Every claim in §3 is
drawn from specification text and one spike. The acceptance test asks for
round-trip fixtures for `NameCert`, `AuthzCert` with a **threshold subject**,
and `ArtifactStatement` — and §5.1 is the warning: the threshold case is where
a reading of a specification was already wrong once.

**It does not propose the `SPEC-0002` §8.6 diff that §3.13 implies.** The fix
looks obvious and short, which is exactly when an agent should not write it into
a normative specification: `ARCH-0001` §9.4 and `CLAUDE.md` route a change to a
document through a proposal against that document, and `SPEC-0002` is now
governed by an accepted ADR. §3.13 states the defect and §8 files the item.

**It does not read `ADR-0003` D2 as settling DEC-002**, and it does not read
`SPEC-0002` §5 as settling DEC-005. D2 refused the first in terms; nobody has
said anything about the second, and the difference between *decided* and
*not yet written down* is not an agent's to infer.

What it does claim: the material for both decisions is now assembled, the
disagreements are visible rather than smoothed, the two places where our own
earlier positions were withdrawn are marked as withdrawals rather than quietly
corrected, and the three claims this revision had to retract — on P5.1, on P5.2,
and on condition (5) being unsupplied — are retracted in place, with the reason,
rather than edited out.

---

## 8. Open items this report hands on

| item | owner |
|---|---|
| **`trusts` and `about` have no canonical order, and `SPEC-0004` §6.4's `identical` is undefined** (§3.13) — a `SPEC-0002` §8.6 fix, proposed against the document, not written here | **new** — spec lane |
| **Does `SPEC-0002` §5 answer DEC-005, or is DEC-005 only the export profile?** (§5.2) — `ADR-0003` is silent where it was explicit for DEC-002 | **new** — register / sponsor |
| **Declare a Unicode normalisation form for the labels and language tags that are load-bearing under P1, and test it at §4.3** — the one route to condition (6) still open to us (§3.13) | **new** — `SPEC-0003` lane |
| Read RDF Canon 1.0 as prior art for condition (5) | library#56 |
| Build the **threshold-subject** fixture — the gap in `spec/vectors/ksa-core/` (§3.12) | T-031, **Oct 28** |
| Round-trip and idempotence tests in CI — still `todo`, and the vectors are produce-and-verify only | T-034 |
| Score the surviving options against §3.2's six conditions in the ADR | T-032, T-033 |
| Whether to widen the scoring set to three — **and that the bar moved on 2026-10-14**, since the request now means superseding an accepted ADR | **mofn#8** — sponsor, not a lane (§3.9) |
| P5.1 and P5.2 land in the principle they already govern in the specification | **mofn#97**, blocked on a non-author review (§3.2) |
| P5.2 redone against COSE `crit` if DEC-005 goes that way | DEC-005 |
| Canonical key bytes before hashing — unsatisfied in the only code that exists | **DEC-003** (§3.6) |
| Whether a meet-plus-residue hybrid is constructible | **DEC-004**, R-001 §12 problem 2 |
