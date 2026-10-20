---
schema: "archdoc/v1"
id: R-0005
title: "Why Provenance, Why Now, and the Gap the Ancestors Left"
short_title: "Context"
description: "The D3 context report: the narrow guarantee a signature gives, the four forcing functions that made provenance urgent after thirty years of indifference, and the specific gap four prior attempts left open. Closes no decision."
type: research
category: security
status: draft
version: "0.1.1"
date: "2026-10-14"
updated: "2026-10-16"
needs_review: true
reviewed: false
canonical_path: research/0005-context/report.md
companion:
  - research/0001-signatures-and-attestation/report.md
  - research/0006-mechanism/report.md
informs: [PLAN-0001, PLAN-0002, PROC-0004]
open_decisions: [DEC-002, DEC-004, DEC-007]
backlog: T-025
library_pin: "library@60b3284"
---

# Why Provenance, Why Now, and the Gap the Ancestors Left

**Status: first draft. Closes nothing.** No `DEC-*` is decided, narrowed, or
recommended here. Where this report touches an open decision it says which, and
says that the decision is open.

Bibliography pinned at **`library@60b3284`**. Citation keys of the form
`[@record-id]` resolve to records at that commit.

**This is a synthesis pass, not a retrieval pass** — and that is a limitation,
stated here rather than buried. No new web retrieval was performed for this
report. Its evidence is survey **R-001**
(`research/0001-signatures-and-attestation/report.md`), the library at the pin
above, and the extractions and topic answers those records carry. `searches.md`
records the absence and says where the original searches live. Everything this
report adds is **arrangement and argument**, not new fact.

This is the first of the three D3 reports (`PROC-0004` §3). It is scoped to
*why provenance, why now; the historic gap*. The comparative anatomy and the
evidence for DEC-002/DEC-004 are **R-0006**; adoption measurement and the
failure-to-adopt analysis are **R-0004**. Where this report would repeat them,
it cites instead.

---

## Abstract

A digital signature proves that a particular private key was used over
particular bytes. It proves nothing about who holds the key, whether they were
entitled to say what they said, or whether it is true. This is not a gap that
was discovered and patched; it is what the definition says. Goldwasser, Micali
and Rivest secured the primitive by handing the adversary an **oracle** that
signs whatever it is asked, and demanding security anyway [@gmr-1988-adaptive].
The standard definition therefore presupposes signatures over messages the key
holder never saw.

Fifty years of engineering has gone into the three questions that leaves open —
*who holds this key, what may it say, where does trust begin* — and this report
argues that the field answered the first, half-answered the third, and has
barely begun the second.

Four forcing functions made that unfinished business urgent between 2020 and
2026, after thirty years of indifference: supply-chain compromises that
verified correctly, statutory mandates in two jurisdictions, the collapse of the
marginal cost of signing inside CI, and the arrival of autonomous agents acting
with delegated authority. None of the four is a cryptographic problem.

Four prior attempts left four different pieces of the answer. X.509 removed
scoped delegation deliberately in 2008 and now carries it at **1.8% deployment**
[@survey-2026-nameconstraints-measurement]. OpenPGP localised trust but never
had an authorization language. SDSI/SPKI built the authorization calculus and
**never shipped a wire format** [@draft-ietf-spki-cert-structure]. PICS
published a dereferenceable, machine-readable vocabulary and was destroyed by
politics rather than by engineering [@pics-censorship-faq].

The gap the four leave jointly is narrow and specific, and §7 states it:
**nothing in the surveyed field localises *type* names.** SDSI localised
principal names thirty years ago and the idea was never applied one layer down,
to the vocabulary in which statements are made. That is the opening this project
targets, and §8 records honestly that targeting it is not the same as being able
to cross it.

---

## 1. What this report is for

`PROC-0004` §3 scopes it in six words: *why provenance, why now; the historic
gap.* That maps to three questions, and the report answers them in order:

1. **What does the primitive actually give us?** (§2) Because every claim about
   provenance is a claim about what sits on top of a signature, and the
   literature routinely over-reads the bottom layer.
2. **Why is this urgent in 2026 and not in 1998?** (§3–§4) Because the technical
   problem has not changed and the answer is therefore not technical.
3. **What did the prior attempts leave?** (§5–§7) Because this project is a
   recombination of four of them, and a recombination that cannot say what each
   parent got wrong is a pastiche.

**What it is not.** It is not a market analysis — `PLAN-0001` §11 (D9) owns
that. It is not an adoption measurement — R-0004 owns that, and this report
cites its numbers rather than re-deriving them. It is not a comparative anatomy
of mechanisms — R-0006 owns that. And it takes no position on encoding, tag
language, or envelope: DEC-002, DEC-004 and DEC-005 are open, and §8 is written
so that nothing in it can be read as narrowing them. **`ADR-0003` D2 has since
fixed the KSA core's encoding without accepting DEC-002** (2026-10-14); that
changes nothing in this report, which argues from the thirty years before it,
and R-0006 §3.9 is where it is read.

---

## 2. The narrow guarantee

### 2.1 What the object is

A signature scheme is a triple over bit strings: `Gen(1ⁿ) → (pk, sk)`,
`Sign(sk, m) → σ`, `Verify(pk, m, σ) → {0,1}`. What is absent from that type
signature is the entire subject of provenance. There is no person, no name, no
time, no purpose and no document. `m` is a byte string and `pk` is a byte
string; everything the word *signature* carries in ordinary language is imported
from outside by convention, protocol or law.

The idea preceded the mechanism by two years. Diffie and Hellman posed it as a
named open problem with no solution [@diffie-hellman-1976], and the motivation
in their §4 is worth recovering because it is exactly the attestation case:

> a message may be sent but later repudiated by either the transmitter or the
> receiver.

The signature was invented to **settle arguments between parties who already
communicated** — not to establish identity, and not to keep secrets. Rivest,
Shamir and Adleman supplied the trapdoor [@rsa-1978]; Rabin gave the first
reduction to a hard problem and anticipated the chosen-message danger before it
had a name [@rabin-1979-tr212]; Lamport removed number theory entirely
[@lamport-1979-one-way] and Merkle made it reusable [@merkle-1979-thesis;
@merkle-1980-protocols], which is the construction the post-quantum mainstream
now runs on.

### 2.2 The definition, and the oracle

The decisive work was taxonomic rather than constructive. GMR
[@gmr-1988-adaptive], building on [@gmy-1983-strong-signatures] and
[@gmr-1984-paradoxical], crossed attack strength against break severity and
defined security as *the strongest attack against the weakest break* — EUF-CMA.

The detail that matters for this project is in the game's shape. The challenger
gives the adversary **oracle access to `Sign(sk, ·)`**: a machine that signs
whatever it is asked, without judgement. Security is demanded anyway. So the
standard definition does not merely fail to model intent — it **presupposes**
that signatures are produced over messages the key holder did not choose and may
never have seen.

R-001 §2.5 enumerates what therefore lies outside the quantifier: identity,
intent, authority, truth, non-repudiation, uniqueness of `σ`, meaning as opposed
to bytes, and context. That enumeration is this project's `LIMITATIONS.md` in
its academic form, and the sentence the repository leads with —
*this proves origin and integrity, it does not prove truth* — is a restatement
of it.

### 2.3 Why this is the right place to start a context report

Because the three questions the definition leaves open are the only axes on
which the systems in §5 actually differ:

1. **Who holds this key?** — the naming problem.
2. **What is this key entitled to say?** — the authorization problem.
3. **Where does trust begin?** — the root problem.

R-001's central claim is that **the signature is the solved part**. The
cryptographic core is settled, standardised [@fips-186-5], and now has published
post-quantum replacements [@fips-204; @fips-205]. Everything contested is in
questions 2 and 3.

That claim does real work in a context report, because it rules out an entire
class of answer to *why now*. Nothing in §3 happened because the cryptography
improved.

---

## 3. Why now — four forcing functions

Thirty years separate SPKI's working group from this one, and the technical
problem has not materially changed. What changed is the cost of ignoring it.
Four things moved, independently, between 2020 and 2026.

### 3.1 Attacks where provenance was present and correct

The field's motivating incidents are not cases where provenance was missing.
They are cases where it was recorded accurately and did not help.

**SolarWinds (2020)** [@solarwinds-8k; @fireeye-sunburst] inserted SUNSPOT
[@crowdstrike-sunspot] into the build, so the malicious artifact was produced by
the legitimate pipeline and signed with the legitimate key. Every "who built
this" question had a correct and reassuring answer.

**event-stream (2018)** [@npm-event-stream; @event-stream-issue-116;
@ghsa-event-stream] was a maintainer handing over publish rights to a
volunteer. No key was stolen and no build was subverted; the authority was
**given away**, which no integrity mechanism models.

**xz-utils (2024)** [@cve-2024-3094; @freund-2024-xz; @cox-2024-xz-timeline;
@tukaani-xz-backdoor] ran the same pattern over three years of social
engineering, with the payload in test fixtures that the release tarball included
and the repository did not.

**Mini Shai-Hulud (2026)** [@slsa-2026-mini-shai-hulud] is the sharpest result
the field has, and R-0004 analyses it in full. The short form: 84 artifacts
carried cryptographically valid provenance attestations naming the correct
builder, repository, workflow and ref — and **both malicious runs ended with
`status: failure`** while standard consumer tooling does not check run status.
SLSA's own write-up states the boundary plainly: provenance answers *what
happened*, policy and verification answer *was that good enough*, and only the
first has been industrialised.

The pattern across all four — and Ohm et al. [@ohm-2020-backstabbers] document
it across 174 packages — is that the failure is **entitlement, not integrity**.

### 3.2 Statute

Between 2021 and 2026 provenance stopped being a best practice.

In the United States, EO 14028 [@eo-14028] and the OMB memoranda that implement
it [@omb-m-22-18; @omb-m-23-16; @omb-m-26-05] made attestation a condition of
federal software procurement, with NIST's secure-development framework
[@sp-800-218; @sp-800-218r1] as the substance and a self-attestation form
[@cisa-ssdf-attestation-form-2024] as the instrument. SBOM minimum elements
moved from NTIA [@ntia-2021-sbom-minimum; @ntia-sbom-minimum-elements] to CISA
[@cisa-2026-sbom-minimum].

In the European Union, the Cyber Resilience Act [@eu-cra-2024-2847] attaches
obligations to products with digital elements, and Article 50 of the AI Act
[@eu-ai-act-art-50] requires machine-readable marking of synthetic content, with
a code of practice attached [@eu-code-of-practice-marking]. California SB 942
[@ca-sb-942] does the same at state level. Germany's BSI technical guidelines
[@bsi-tr-03183-1] and the UK's code of practice
[@uk-software-security-code-of-practice] carry the pattern further.

Two observations, both of which bear on this project.

**Regulation mandates existence, not entitlement.** R-001 §8.4 establishes it
and R-0004 §3 measures the consequence: the statutes require that a statement be
*produced and available*, and are silent on who was entitled to make it. That is
the same gap §3.1's incidents expose, now with a compliance deadline attached.

**The content-provenance mandates arrived with a stack already built.** C2PA
[@c2pa-2-4] existed before Article 50 did, and the NSA's 2025 guidance
[@nsa-2025-content-credentials] endorsed it. So one half of the field acquired a
forcing function PICS never had — R-001 §6.4 makes this argument and §5.4 below
returns to it.

### 3.3 The marginal cost of a signed statement reached zero

This is the least discussed and arguably the most important of the four.

Signing used to require a key, a ceremony and a person. Three changes removed
all three: ACME [@rfc-8555] made certificate issuance free and automatic;
Sigstore [@sigstore-2022] replaced long-lived keys with ten-minute certificates
bound to an OIDC identity; and CI platforms began minting workload identity
tokens, so a build can prove what produced it without any human holding
anything. PyPI's trusted publishers [@pypi-trusted-publishers] is the same
pattern on another ecosystem.

The consequence is structural rather than quantitative. **Provenance became a
per-pipeline switch** — and R-0004's npm measurement shows exactly that
signature: 100 of 300 sampled packages carry attestations, but from only 56
distinct publishing scopes out of 242, with five scopes accounting for 40.
Counting packages flatters adoption because one configuration change attests
many artifacts.

Cheap production of statements with no corresponding language for entitlement is
precisely the imbalance §3.1's incidents turn on. The field industrialised the
easy half because the easy half got cheap.

### 3.4 Delegated authority stopped being a human-paced problem

The fourth function is recent enough that the literature is still drafts.

Three active individual Internet-Drafts
[@draft-niyikiza-oauth-attenuating-agent-tokens;
@draft-asor-wimse-agent-delegation-chain; @draft-hamr-oauth-agent-delegation]
apply offline, holder-side attenuation to chains of AI agents. None is
WG-adopted. R-001 §9.2 records a detail worth repeating here: the first cites
Dennis and Van Horn [@dennis-vanhorn-1966] and macaroons [@macaroons-2014] but
**not SPKI**; the second cites SPKI only as a *"historical standards-track
ancestor."*

What the agentic case adds is **rate and depth**. A human delegating to a
colleague does so occasionally and can be asked afterwards what they intended.
An agent spawning sub-agents does so continuously, and the question an auditor
needs answered — *which human sits at the root of this chain, and what did they
actually authorise?* — is a delegation-provenance question that a chain of
ephemeral keys cannot answer (R-001 §9.4). Work on capability models for agentic
systems [@veski-2026-capmas; @systems-security-agentic-computing] is converging
on the same requirement from the other direction.

This is where the thirty-year-old authorization calculus becomes load-bearing
again, and it is the clearest statement available of why this project is timely
rather than antiquarian.

### 3.5 What the four have in common

None of them is a cryptographic problem, and none is solved by a better
signature. Each is a question about **authority**: who was entitled to say this,
how was that entitlement narrowed on the way here, and who decided. That is the
question §5's four ancestors answered in four incompatible ways.

---

## 4. The one form, and five axes

Before the history, the frame. R-001 §3 observes that every system in the field
is an instance of one shape:

> **A says B has property C**

with a signature binding the statement to A's key. Systems differ along five
axes, and the axes — not the application domains — are what separate them:

| axis | question | why it separates systems |
|---|---|---|
| **Subject** | what is B? | a key, a name, a document, a device state, a build |
| **Predicate** | what is C, and **who defines it**? | fixed by specification, allocated from a registry, or separately published |
| **Authority** | who may say it? | inherited root store · local policy · hardware vendor · out of band |
| **Scoping** | can authority be narrowed on delegation? | and along what dimension — name, tag, capability, or not at all |
| **Root** | where does trust begin? | a root store you inherited, a keyring you built, a policy you wrote, silicon |

R-001 §11.1 populates this for fourteen systems and §11.2 draws the finding that
matters for a *context* report: the Subject and Predicate columns are diverse
and largely unproblematic, while **the Authority and Root columns are where
every system either punts or hard-codes.** Read the Authority column downward in
R-001's table and it says: *inherited root store, a parameter, a command-line
flag, assumed, out of scope of this document.*

That is the historic gap in one column. §5 is how four different projects
arrived at it.

---

## 5. Four attempts, four pieces

### 5.1 X.509 — scoped delegation, removed deliberately

X.509 was published in 1988 as part of the X.500 directory
[@itu-x509-1988; @itu-x509], and its purpose was authentication *to a
directory*. The naming model is inherited from that: a Distinguished Name is a
path in a global tree that was assumed to exist.

The decisive moment for this project is not 1988 but the transition from RFC
1422 to the PKIX profile. **RFC 1422 made name subordination a structural
invariant** [@rfc-1422]: a CA could only certify names below its own point in
the tree. RFC 3280 and then RFC 5280 [@rfc-3280; @rfc-5280] replaced that with
an **optional** `nameConstraints` extension.

R-001 §4.5 measured the result, and it is the survey's original contribution:
across all **1,769** CCADB-disclosed Mozilla-program intermediate CA
certificates [@ccadb], **31 (1.8%) carry a `nameConstraints` extension and only
2 mark it critical** as RFC 5280 requires, with 29 of the 31 issued by a single
CA family [@survey-2026-nameconstraints-measurement]. Out-of-band root-store
scoping reaches 1 root in 172.

Two further properties compound it. The extension is **fail-open by
construction** — a non-critical constraint may be ignored by a verifier that
does not implement it — and implementation history shows the checking itself is
error-prone [@go-nameconstraint-cves; @golang-61963]. Meanwhile the incidents
that scoping would have contained happened anyway
[@foxit-2012-black-tulip; @mozilla-2013-turktrust; @mozilla-2013-anssi;
@google-2016-wosign; @google-2017-symantec].

**What X.509 contributes to this project is therefore a negative result with a
number attached.** Optional scoping is not scoping. A design in which unscoped
authority is *inexpressible* rather than merely discouraged is the thing the
deployment record argues for, and R-001 §12 lists it as the first open problem.

It is important not to overstate this. R-001 §4.9 asks directly whether X.509
already solves scoped delegation, and the honest answer is that it has the
machinery — `nameConstraints`, and RFC 3820's proxy certificates with
`pCPathLenConstraint` [@rfc-3820], which is SPKI's delegation bit and depth
control inside the incumbent format. The failure is deployment and defaults, not
expressive power. That distinction matters because it means *"X.509 cannot do
this"* is the wrong argument and *"X.509 does not do this, measurably, after
seventeen years"* is the right one.

### 5.2 OpenPGP — local trust, no authorization language

OpenPGP [@rfc-4880; @rfc-9580] took the opposite root decision: no inherited
root store, a keyring the relying party assembles, and trust signatures that let
a user designate introducers.

R-001 §5.2 finds that the web of trust delivers less scoped delegation than its
reputation suggests. Its scoping dimensions are a trust *level* (depth) and a
**regular expression over the UserID display string** — which is scoping over a
rendered name, not over what the key may assert. And the deployed graph is not a
fabric: Ulrich et al. [@ulrich-2011-openpgp-wot] analyse a strongly-connected
component inside a graph of hundreds of thousands of components, which is what a
trust structure looks like with no anchor-installation path. The SKS keyserver
network's collapse under certificate-flooding [@cve-2019-13050] removed even the
distribution layer; current practice has retreated to verified-email directories
[@keys-openpgp-org-faq].

**OpenPGP's contribution is the demonstration that localised trust is not enough
on its own.** It localised *who you trust* and never built a language for *what
you trust them to say*. R-001 §5.2's assessment — more an identity system than
an authorization system — is why `ARCH-0001` places PGP as an **introducer
import**, not as the validation algorithm, and why WP4 is explicitly deferred.

### 5.3 SDSI and SPKI — the calculus, with no wire format

SDSI's contribution is **linked local namespaces** [@sdsi-1-1]: every principal
defines its own bindings, so *the principal you call `alice-smith` may be
different from the principal I call `alice-smith`*, and names chain —
`bob's alice`, extensible to `bob's alice's mother`. The stated motivation is
that X.509-style schemes are *"both excessively complex and incomplete,"* their
complexity arising from *"dependence on global name spaces."*

SPKI [@rfc-2692; @rfc-2693] supplied the authorization calculus and recorded the
merge in its own text — Rivest and Lampson having shown *"that one can not only
use local names locally, one can use local names globally."* The result is two
object kinds: the **5-tuple** ⟨Issuer, Subject, Delegation, Authorization,
Validity⟩ and the **4-tuple** name certificate ⟨Issuer, Name, Subject,
Validity⟩. **Two layers, and neither required to do the other's job.**

R-0006 §4 treats the authorization algebra as DEC-004 evidence and this report
does not duplicate it. What belongs here is the failure analysis, because it is
the most directly instructive history this project has.

The SPKI working group published two **Experimental** RFCs in September 1999 —
the requirements and the theory. The bits-on-the-wire document,
`draft-ietf-spki-cert-structure-05`, **expired and was never published**
[@draft-ietf-spki-cert-structure], and the working group is recorded as
concluded [@ietf-spki-wg]. Read structurally: *the group standardised the
rationale and abandoned the format.* A theory RFC with no wire format and no
conformance target cannot be implemented interoperably, which R-001 §5.5 calls
close to a sufficient explanation for zero deployment on its own.

R-001 §5.7 gives five reasons none of the decentralised schemes displaced X.509,
and R-0004 §8 applies them to this project adversarially. The one that belongs
in a context report is (e): **X.509 removed the incentive to switch from the
inside.** Ellison and Schneier [@ellison-schneier-2000-ten-risks] named the CA
rent; ACME [@rfc-8555] then destroyed it, Certificate Transparency
[@rfc-6962; @rfc-9162] supplied the accountability, and RFC 3820 [@rfc-3820]
absorbed the delegation story. *Once the incumbent is free, automated, audited
and delegating, the migration case evaporates.*

**What survived is measurable.** RFC 9804 [@rfc-9804] standardised SPKI's
S-expressions in June 2025 — and its own §1.3 explains the 28-year gap. The
motive is live interoperability between GnuPG and Ribose's RNP, not revival. It
standardises **the encoding layer of SPKI and nothing else**: no 5-tuples, no
delegation, no reduction. That is a precise measure of what survived. The syntax
did; the authorization theory did not.

> **This is not a DEC-002 statement.** RFC 9804 is also DEC-002 option 1, and
> R-0006 §3.5 scores it as such. Nothing in this paragraph bears on that
> scoring; *historical as a revival* and *viable as an encoding* are different
> claims about different things, and conflating them is an error this project
> has already made once (`PLAN-0001` §13). `ADR-0003` D2 has since selected a
> CBOR profile for the KSA core — on the ground that it adopted an implemented
> core protocol, not on any reading of this paragraph (R-0006 §3.9).

### 5.4 PICS — the vocabulary layer, and a political death

PICS [@pics-1-1-labels; @pics-1-1-services] is the ancestor this project has the
most to learn from and the one least often read.

Its architecture separated three things the modern field fuses. A **rating
service** published, at a URL, a machine-readable description of its own
vocabulary — each category's name, its permitted values, and **a human-readable
description of what each value means**. A **label** was then a short signed
statement binding a document URL, and optionally a content checksum, to values
in that vocabulary. And the **client chose which services to consult**. DSig
[@pics-dsig-1-0] added signatures two years later.

The consequence is the property R-001 §11.2 identifies as a regression the field
has not noticed. Under PICS, an unknown vocabulary degraded to *"fetch the
description and render it."* Under C2PA [@c2pa-2-4], whose assertion labels are
enumerated in the specification, an unknown assertion degrades to *"signed
opaque blob."* **PICS in 1996 had a property the 2026 stack does not.**

PICS did not fail on engineering. R-001 §6.2 and the FAQ [@pics-censorship-faq]
record what happened: it became the technical substrate of a censorship debate,
the ACLU's *Fahrenheit 451.2* [@aclu-fahrenheit-451-2] named it as a mechanism
for mandatory rating, and self-rating collapsed on the demand side —
a 1998 survey found most webmasters had not rated [@gvu-1998-webmaster-survey].
POWDER [@powder-description-resources] replaced it and failed quietly.

**Two lessons, and the second is uncomfortable.** First, the dereferenceable
vocabulary is a recoverable idea and this project should recover it — R-001 §12
problem 3 asks whether a `(defining key, local label)` pair can carry a
machine-readable schema and human-readable description the way an
`application/pics-service` document did, and that question is this project's
`DEC-007`, which is **open**. Second, PICS had no forcing function and C2PA has
one in statute (§3.2), which R-001 §6.4 identifies as the difference that
matters. A project proposing a vocabulary layer in 2026 should be clear-eyed
that *the architecture was never the problem*.

---

## 6. Two distinctions the field conflates

R-001 §11.3 isolates two category errors. Both belong in a context report
because both are load-bearing for how this project is scoped.

**Delegation versus integrity-of-state.** An X.509 or SPKI chain passes
*authority between principals over time*, and therefore needs revocation — the
hard, conceded-unsolved part of PKI [@langley-2011-revocation;
@langley-2014-revchecking; @larisch-2017-crlite; @letsencrypt-ocsp-eol]. An
attestation chain is a *provenance or derivation* chain whose subject is a
snapshot; nothing is granted, and the hard problem is **freshness**, not
revocation. Their temporal structures are inverted, and the industry routinely
packs the second into containers designed for the first — device state in an
X.509 extension [@android-key-attestation], DICE derivation chains as X.509
[@tcg-dice-cert-profiles] — which invites path-validation reflexes that are
simply wrong for state claims.

**Provenance versus entitlement.** Every incident in §3.1 is a case where
provenance was recorded correctly and entitlement was the actual failure. The
field has industrialised the first and standardised almost none of the second.

`ARCH-0001` is built on the first distinction: §4.3 keeps name resolution,
authorization reduction and statement acceptance as **three separate
procedures**, and the architecture note that they must not be collapsed into one
graph walk is this finding in normative form. The second distinction is the
project's thesis.

---

## 7. The gap, stated precisely

R-001 §11.4 states it, and it is narrower than "provenance needs authorization":

> SDSI's contribution was to localise **principal names**: a name is interpreted
> relative to the key that defined it, so a global namespace is unnecessary.
> **Nothing in this survey localises *type* names.**

Every system in R-001's table does one of three things with its predicate
vocabulary. It **fixes it in a specification** (C2PA, X.509, PGP). It
**allocates it from a registry** (in-toto predicate types
[@in-toto-attestation-v1], COSE algorithms [@iana-cose-algorithms], CBOR tags
[@iana-cbor-tags]). Or it **declines to define one** (DSSE
[@secure-systems-lab-dsse], macaroons).

PICS came closest, and §5.4 says how — but its vocabulary was owned by a
*service*, not by a key, and it had no signature binding a vocabulary to its
definer until DSig arrived. RATS [@rfc-9334] splits lexical from evaluative
authority and is the one modern system that gets the degradation behaviour
right, but it does so by putting the vocabulary *upstream of the consumer* in
the Verifier, and still assumes reference values [@draft-ietf-rats-corim] arrive
from a recognised provider.

So the gap is the conjunction of four things, each of which exists separately
and none of which exists together:

| piece | who has it | who lacks it |
|---|---|---|
| principal names relative to a key | SDSI/SPKI | everyone else |
| an authorization algebra closed under intersection | SPKI | the entire modern family (R-0006 §4) |
| *k*-of-*n* subjects as first-class principals | SPKI; TUF thresholds [@tuf-spec] | the envelope layer, which carries `n` and cannot carry `k` |
| a dereferenceable, human-legible vocabulary | PICS | C2PA, in-toto, DSSE |

**That conjunction is what `ARCH-0001` proposes to build**, and the four rows
map onto G1, G3, G4 and G5 respectively.

---

## 8. What this means for the project — and the honest counter-argument

Two things follow for scope, and one against.

**It explains the composition.** This project is not proposing a new signature,
a new envelope, or a new transparency log. It proposes to take SPKI-shaped
rights and names, PICS-shaped artifact predicates, and an existing envelope for
bytes on the wire — which is exactly `ARCH-0001` §3.3's "composition target."
§5 is the argument that each parent contributed a different, separable piece.

**It explains the two in-scope targets.** MD-1 put software supply chain and
archives/library in scope. §3.1 and §3.3 are the case for the first. The second
is the case R-001 §11.4 implies: a vocabulary mechanism demonstrated against one
domain cannot show it generalises, and generalisation is the whole claim.

**And the counter-argument, which belongs in a context report rather than in a
footnote.** R-0004 §8 applies R-001 §5.7's five reasons for SPKI's non-adoption
to this design and finds that **three of the five are structural properties of
it as it stands today**. §5.1 above adds a fourth consideration pointing the
same way: the incumbent's failure is deployment and defaults, not expressive
power, so the honest claim is not *X.509 cannot express scoped delegation* but
*X.509 has not, measurably, in seventeen years*. Whether a design in which
unscoped authority is inexpressible fares better is **an open empirical
question**, and this report does not assert that it will.

The one reason in R-001 §5.7 this project can close by its own effort is (a) —
*no wire format, no conformance target.* SPKI standardised the rationale and
abandoned the format. `PROC-0004` §4's requirement that `spec/vectors/` be
consumable by an implementation that has only that directory is the direct
answer to that failure, and **D5, D6 and D7 are the deliverables that would make
it true.** That is a schedule claim, not an argument, and it is the right place
for a context report to stop.

---

## 9. What this report leaves open

Stated so the omissions read as decisions rather than oversights.

| open | owner |
|---|---|
| Whether the key-relative vocabulary of §7 is expressible at all | **DEC-007**, open; `ARCH-0002` P3/P4, both draft and P4 held |
| What the statements are encoded in | **DEC-002**, open — R-0006 §3 is the evidence, not the answer. `ADR-0003` D2 fixed the KSA core's encoding and declined to accept DEC-002; R-0006 §3.9 separates the two |
| What the authorization language is | **DEC-004**, open — R-0006 §4 |
| Whether adoption is plausible | R-0004 §7–§8; this report does not re-argue it |
| Market and applications | D9, `PLAN-0001` §11 |
| Practitioner interviews | Not conducted. Desk research only, as in R-0004 |

---

## 10. Conclusion

A signature proves that a key was used over bytes, and the definition that
secured it models the signer as an oracle. Everything provenance needs sits
above that line, and the field has spent fifty years building on the narrow
guarantee without finishing the two questions it leaves open.

What is new is not the problem but the pressure. Attacks now verify correctly;
statute now compels production without compelling entitlement; signing is free,
so statements are abundant and authority is not; and autonomous agents have made
delegation continuous. Four ancestors each solved one piece — scoped delegation
with a measured 1.8% deployment, localised trust without an authorization
language, an authorization calculus with no wire format, and a dereferenceable
vocabulary killed by politics.

The gap they leave jointly is that **no system localises the vocabulary in which
statements are made.** SDSI localised principal names in 1996 and nobody applied
the move one layer down. Whether it can be applied there is the project's
question, and it is open — along with the encoding it would be written in, the
tag language it would constrain, and the honest possibility, recorded in R-0004
§8, that the reasons the ancestors failed still apply.
