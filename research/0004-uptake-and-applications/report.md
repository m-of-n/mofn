---
schema: "archdoc/v1"
id: R-0004
title: "Who Adopts Provenance, and Why the Ancestors Did Not"
short_title: "Uptake and applications"
description: "Adoption evidence for the supply-chain and content-provenance stacks, a failure-to-adopt analysis of SPKI/SDSI and PICS, and a four-condition model of uptake applied to this design. Closes no decision."
type: research
category: security
status: draft
version: "0.1.0"
date: "2026-10-10"
updated: "2026-10-10"
needs_review: true
reviewed: false
canonical_path: research/0004-uptake-and-applications/report.md
companion:
  - research/0001-signatures-and-attestation/report.md
informs: [PLAN-0001, PROC-0004]
open_decisions: [DEC-002, DEC-004]
backlog: T-027
library_pin: "library@93891c9"
---

# Who Adopts Provenance, and Why the Ancestors Did Not

**Status: first draft. Closes nothing.** This report does not settle DEC-002,
DEC-004, or any other open decision in ARCH-0001. Its recommendations are
proposals and its concluding section is an argument against this project's own
design, offered for review.

Bibliography pinned at **`library@93891c9`**. Citation keys of the form `[@record-id]` resolve to
records in that commit. Sources retrieved fresh for this report — those not yet
in the library — are in `sources.md` with digests and retrieval dates; the
queries that found them are in `searches.md`; claims that could not be
established from a primary source are in `unverified.md` and are **not stated
as fact below**.

This is the third D3 report (`PROC-0004` §3). It assumes, and does not repeat,
survey **R-001** (`research/0001-signatures-and-attestation/report.md`, this
repository — not a library record), whose §5–§8 supply most of the structural
analysis reused here. Where this report and R-001 differ, the difference is
marked.
---

## Abstract

Provenance infrastructure is being adopted at scale for the first time, by two
routes that look nothing alike. The software supply chain adopted it because
the marginal cost of producing a signed statement fell to zero inside CI. Content
provenance is being adopted because, since August 2026, two jurisdictions
require it by statute.

Two original measurements taken for this report quantify where that adoption
has reached. On npm, **100 of 300** of the most popular packages sampled carry
provenance attestations — but those 100 come from only **56 distinct publishing
scopes out of 242**, and the five largest account for 40 of them: provenance is
a per-pipeline switch, and counting packages flatters it. In content
provenance, the entire root of trust for the C2PA ecosystem is a published
list of **30 certificates belonging to 17 organisations**, three of which are
incumbent commercial certificate authorities from the WebPKI.

Both measurements point the same way. The field has industrialised the
production of signed statements and has not built an entitlement layer; where
it needed one, it reconstructed X.509's root-program structure rather than
inventing anything. That is the context in which the two direct ancestors of
this design — SPKI/SDSI and PICS — must be judged, because both failed, and
both failed for reasons that are *adoption economics*, not technical defects.

Section 7 proposes a four-condition model of uptake drawn from those failures.
Section 8 applies it to this project and reaches an uncomfortable result:
**three of the five reasons R-001 §5.7 gives for SPKI's non-adoption are
structural properties of this design as it stands today.** One of them is an
open decision the project can close; two are not, and the report says what
narrowing would be required to survive them.

---

## 1. What this report measures, and what it does not

The question is *uptake*: who deploys provenance and attestation systems, what
compels them, what stops them, and what the deployed systems gave up to get
deployed. It is not a market sizing and not a business plan; `PLAN-0001` §11
(D9) owns that, and this report is an input to it.

Three scopes are deliberately excluded. **Cryptographic adequacy** is R-001's
subject and is treated here as settled — the signature is the solved part.
**Encoding** belongs to the mechanism report and to DEC-002; nothing here
should be read as evidence for a serialisation. **Practitioner interviews**
(`PLAN-0001` §11, "3–5 short practitioner conversations if reachable") have not
been conducted and are not reflected below; this is desk research only.

What the report does claim to add over R-001 is two things R-001 explicitly
left open. R-001 §6.7 carries this sourcing note:

> Platform and newsroom adoption claims for C2PA circulate widely but could not
> be established from primary sources in this pass and are therefore not stated
> here.

Supplying that evidence is this report's first job. Its second is the
comparison R-001 does not make: setting the ancestors' failure beside the
descendants' success and asking what separates them.

## 2. Method and sourcing discipline

Three rules, inherited from `research/README.md` and R-001 §1.2.

**Primary sources only for factual claims.** Search-result snippets were used
to locate URLs and never as evidence. This mattered more than expected: the
first search pass for C2PA adoption returned nine results, of which seven were
secondary blogs that contradicted each other on camera-vendor support and on
whether Google Search verification had shipped. None is cited. Where a figure
appears below, it comes from a document published by the body responsible for
the fact.

**Original measurement where no primary source publishes the number.** Two
questions central to this report — how much of npm carries provenance, and how
large the C2PA root of trust is — are not answered by any primary publication.
Rather than cite a blog, both were measured directly. The method, the exact
queries, the retrieval dates and the digests are recorded so the measurements
can be repeated and contradicted. Both are reported with their limits stated.

**An explicit account of what could not be established.** `unverified.md` is a
publication gate, not a to-do list: nothing in it is asserted here. It includes
one correction to an assumption this report began with.

One limitation is structural and worth stating plainly. Three library records
central to this report's subject — `pypi-trusted-publishers`,
`slsa-2026-mini-shai-hulud` and `c2pa-conformance-program` — are **stubs**:
template text, `status: stub`, `confidence: low`, no digest, no retrieval date,
and `bears_on: []`. R-001 cites all three in its argument. The citations are
sound, because R-001's authors read the sources; the *records* were never
written. The library's evidence base is therefore thinnest in exactly the area
this report covers. All three sources were re-retrieved from primary URLs for
this report, and upgrading the records is filed as follow-on work (§10).

---

## 3. The software supply chain: adoption without entitlement

### 3.1 Why this stack was adopted

R-001 §8.7 gives the mechanism in one sentence, and it is the single most
important fact in this report:

> That agnosticism is precisely why adoption succeeded: a format making no
> trust commitments could be adopted by GitHub, npm, PyPI, Google and Debian
> simultaneously.

Two properties follow from it. First, **the marginal cost of producing a
statement is zero to the party producing it.** npm provenance is a flag on a CI
workflow; the signing identity is an ambient OIDC token the runner already
holds; the key is ephemeral and never handled by a human. Nobody had to decide
to become a keyholder. Compare SPKI's requirement, in Wang et al.'s words
[@wang-2006-reducing-spki], that "each user is required to manage his/her own
private/public key pair" — the premise that, R-001 §5.7(b) argues, was the
blocker.

Second, **no party had to agree with any other party about meaning.** An
in-toto predicate commits its producer to nothing beyond "this is what
happened." Adoption required no consensus on authority, because authority was
left out of the format.

### 3.2 Original measurement — how far provenance has actually spread on npm

No primary publication gives an ecosystem-wide rate. npm documents the
`npm audit signatures` command but publishes no denominator; the figures
circulating in third-party audits use incompatible samples and are recorded in
`unverified.md` rather than cited.

**Method.** On 2026-10-10 the npm registry search API was queried for the three
keyword terms `keywords:javascript`, `keywords:node` and `keywords:utility`,
each with `size=250`, `popularity=1.0`, `quality=0.0`, `maintenance=0.0` — a
pure popularity ranking. Results were deduplicated and the 300 highest-scoring
distinct packages retained. For each, the registry metadata document was
fetched and the `latest` dist-tag's `dist.attestations` field tested for
presence. Exact queries, the script, and the full result rows are in
`sources.md` and `searches.md`.

**Result.**

| measure | count | rate |
|---|---|---|
| packages sampled | 300 | — |
| packages whose latest version carries provenance | 100 | **33.3%** |
| distinct publishing scopes in the sample | 242 | — |
| scopes with any provenance | 56 | **23.1%** |
| provenance packages from the five largest scopes | 40 of 100 | — |
| fetch errors | 0 | — |

**Limits, stated.** The sample is popularity-ranked within three broad keyword
queries, not a download-ranked top-300 of the whole registry; a fourth query
(`text=*`) returned HTTP 400 and was dropped, which is recorded in
`searches.md`. The registry's popularity score is not a download count. The
measurement is of the latest published version only. It therefore supports
claims about *this sample on this date*, not about npm as a whole.

**What it shows.** Two readings differ by ten points, and the gap is the
finding. Counting packages gives 33.3%. Counting publishers gives 23.1%,
because **provenance is a property of a publishing pipeline, not of a package**:
`@inquirer` contributes 16 packages to the provenance set and one decision;
the `oxc` toolchain contributes roughly twenty platform-specific binding
packages and one decision. Per-package counts of provenance adoption are
inflated by monorepos, and any adoption claim phrased per-package should be
read with that in mind — including this report's own headline figure.

Read either way, the direction is clear and the level is modest: three years
after npm provenance became generally available, roughly a quarter of the
popular publishers sampled have switched it on. Adoption is real, voluntary,
rising, and nowhere near universal — which is what "zero marginal cost, no
forcing function" produces.

### 3.3 What that adoption bought — the May 2026 result

R-001 §8.6 treats the May 2026 npm compromise as the survey's strongest
empirical support. Re-retrieved for this report, the SLSA write-up
[@slsa-2026-mini-shai-hulud] yields three details R-001 does not record, all of
which sharpen the point.

On 11 May 2026, attackers chained a `pull_request_target` misconfiguration,
GitHub Actions cache poisoning across trigger scopes, and extraction of the
ambient OIDC token from runner memory, to publish **84 compromised package
builds across 42 `@tanstack` packages**; the worm then spread to **more than
170 packages** across other namespaces. Every published build carried a
cryptographically valid provenance attestation naming the correct builder,
repository, workflow and ref.

The three additional details:

1. **Both malicious workflow runs ended with `status: failure`, and packages
   were published during them anyway.** The signal existed.
2. **"Standard SLSA consumer tooling does not check workflow run status."** The
   signal was not consumed.
3. The post's own conclusion: *"an attacker who fully controls code inside a
   trusted builder on the expected ref can still produce conforming
   provenance."*

And the sentence R-001 already quotes, which remains the best available
statement of this project's thesis by an adopting project about its own
deployment: *"An 'expected builder' check would have passed, because the
pipeline was legitimate; it was the code running inside it that was not."*

The uptake reading is specific. **The adoption succeeded and the protection
did not**, and the reason is not cryptographic. A system optimised for
adoption by making no trust commitments cannot then answer a trust question.
The 33.3% measured in §3.2 is 33.3% of a layer that, by its own maintainers'
account, answers *what happened* and not *was that good enough*.

### 3.4 Where authorization actually lives

R-001 §8.5 establishes the pattern and this report adds nothing to it beyond
emphasis: the entitlement decision moved to the **registry**, out of band from
every format. PyPI Trusted Publishing [@pypi-trusted-publishers] binds a
specific OIDC identity — repository, workflow, environment — to permission to
publish a specific project. That is real scoped delegation, specified nowhere
in in-toto, SLSA, DSSE or Sigstore, and implemented separately by each index.

For an uptake analysis this is the decisive structural fact. **The market
demonstrated demand for scoped delegation and satisfied it with
per-platform configuration rather than with an interoperable format.** Every
index that solved it solved it again. That is either the gap this project
addresses or the evidence that the gap is comfortably survivable; §8 argues it
is not obviously the former.

---

## 4. Content provenance: adoption by statute

### 4.1 The forcing function PICS never had

R-001 §6.4 establishes the mandates and they are not restated in full. The
operative dates: **EU AI Act Article 50** [@eu-ai-act-art-50] applies from
2 August 2026, requiring machine-readable marking of synthetic audio, image,
video and text; the Commission's Code of Practice on marking
[@eu-code-of-practice-marking] of 10 June 2026 points at C2PA and references
CAWG assertions; **California SB 942** as amended by AB 853 [@ca-sb-942] became
operative 2 August 2026 and reaches large platforms and capture-device
manufacturers.

The **Cyber Resilience Act** [@eu-cra-2024-2847] is the softer case and the
contrast is instructive. Annex I, Part II (1) requires an SBOM "in a commonly
used and machine-readable format covering at the very least the top-level
dependencies" — existence, one level deep, format unnamed, disclosed to
regulators with disclosure to users optional under Annex II (9). R-001 §8.4
summarises it as mandating existence, not entitlement. For uptake purposes the
sharper point is that **the CRA mandates an inventory and names no format**,
which produces compliance activity without producing interoperability.

### 4.2 Conformance: the measurable part

The C2PA Conformance Program [@c2pa-conformance-program] is the body that
decides which implementations count. Its own deployment guidance, published
July 2026, states:

> Since its launch, 54 products from 31 companies have passed conformance (as
> of May 14, 2026).

and adds that "over 120 additional companies have submitted expressions of
interest," that the program "expects the number of assessed products to
drastically increase over time," and — candidly — that "there is a queue to go
through the conformance program at the time this document was written" and
"not all C2PA implementations have gone through the Conformance program."

The Content Authenticity Initiative separately reports "more than 6,000
members" as of 18 January 2026. That figure is membership of an advocacy
initiative, not deployment, and is reported here as such; the 54/31 figure is
the one that measures implementations.

The Trust List timeline matters for a reason §4.4 returns to: the official
C2PA Trust List launched mid-2025 with "a new public Certificate Policy which
specifies C2PA requirements for CAs," and the Interim Trust List was **frozen
on 1 January 2026**, with existing certificates remaining valid for legacy
support.

### 4.3 Original measurement — the whole root of trust is 30 certificates

The C2PA conformance page links a machine-readable trust list but publishes no
count. The list was therefore fetched and counted directly.

**Method.** `C2PA-TRUST-LIST.pem` was retrieved from the `c2pa-org/
conformance-public` repository on 2026-10-10 (37,911 bytes, sha256
`75cacc98b79ecac33713c7ecfb58d4a0ef383f3c1f886e7409f9e37e8664aea5`), split into
individual certificates, and each certificate's subject, issuer and expiry read
with `openssl x509`. A certificate was classified a root when subject equals
issuer. Full output is in `sources.md`.

**Result.**

| measure | value |
|---|---|
| certificates in the list | **30** |
| distinct organisations | **17** |
| self-signed roots | 19 |
| intermediates | 11 |
| jurisdiction `C=US` | 20 certificates |
| jurisdiction `C=CN` | 8 certificates |
| jurisdiction `C=NL`, `C=DE` | 1 each |

The 17 organisations are Adobe, Castlabs, DigiCert, Encypher, Google, Huanyu
Trust, Huawei, Irdeto, Snowball Technology, SSL Corporation (SSL.com), Tauth
Labs, TrustAsia, Trufo, Verimago, vivo, Whole Earth Labs (RealReel) and Xiaomi.
Google holds 6 of the 30 certificates and DigiCert 4.

**Three readings, in increasing order of interest.**

First, the trust list is small, and that is not a criticism — it is the
mechanism. A short, curated, publicly audited anchor set is what makes
validation tractable for a client that must render a verdict to a user.

Second, **it is a root program**. The structure is X.509's: a handful of
anchors, a Certificate Policy that binds the CAs, a conformance regime, a
frozen legacy list, and commercial certificate authorities selling into it.
DigiCert, SSL.com and TrustAsia are incumbent WebPKI CAs. R-001 §5.7(e) quotes
Ellison and Schneier [@ellison-schneier-2000-ten-risks] on the CA business
model — "if you can convince someone to buy a certificate each year for $5,
that times the population of the Internet is a big yearly income." Content
provenance, built to solve a problem X.509 never addressed, has reconstituted
X.509's commercial structure within about eighteen months of having a statutory
mandate.

Third, and most relevant to this project: **this is precisely the trust-anchor
installation path that R-001 §5.7(d) identifies as the thing SPKI did not
have.** A key-centric design "has nowhere to install an anchor and no entity to
audit." C2PA built the entity. Seventeen organisations now constitute the root
of trust for a labelling regime that two jurisdictions require by law. One may
think that concentration unhealthy — and §8 argues the project should say so
publicly — but it is *working*, in the narrow sense that products conform,
regulators have something to point at, and a validator has a decidable
question to ask.

### 4.4 What C2PA traded away to get adopted

R-001 §6.5 is the finding and it is not improved by restatement: C2PA bakes its
vocabulary into the specification [@c2pa-2-4], so an unknown assertion degrades
to a signed opaque blob where PICS's unknown vocabulary degraded to "fetch the
description and render it." The label-bureau half — third-party assertions
about content one neither authored nor hosts — has no first-class place in the
manifest model.

What this report adds is the *uptake* interpretation, and it cuts against the
project's instinct. R-001 §6.5 presents the baked-in vocabulary as "a real
regression in extensibility." Read as adoption economics it is also a
**precondition of conformance**. A conformance program can test an enumerated
vocabulary. It cannot test "the product correctly renders any self-describing
vocabulary it has never seen," because that is not a finite test. C2PA's
closed vocabulary and C2PA's testable conformance regime are the same design
decision seen from two sides, and the conformance regime is why 54 products
from 31 companies can be said to interoperate at all.

The trade is real and it is not free — the human-factors findings R-001 §6.6
collects (provenance shifting trust away from truthful content
[@cscw-2023-provenance-trust]; "human washing" and the "downward shift of
trust" as participant coinages [@moruzzi-2025-content-authenticities]; AI
labels inaccessible to screen readers [@ide-2025-signals-of-provenance]) are
failures of interpretation, which is what a published vocabulary is for. But an
uptake report that presents late binding as a free win has not understood why
the system that abandoned it is the one that shipped.

---

## 5. Failure to adopt: SPKI/SDSI

R-001 §5.7 gives five reasons. This section does not relitigate them; it
reclassifies them, because the classification determines which ones this
project inherits.

| # | R-001 §5.7 | kind | fixable by a specification? |
|---|---|---|---|
| (a) | No wire format, no conformance target | **artefact gap** | **Yes** — write the format |
| (b) | Bootstrapping quadratic, payoff deferred | adoption economics | No — a property of key-centricity |
| (c) | Path discovery externalised to the prover | **architectural** | Partly — a resolver can be specified |
| (d) | No trust-anchor installation path | **architectural + institutional** | No — requires an institution |
| (e) | X.509 removed the incentive, from inside | historical | Moot — already happened |

Two observations follow.

**(a) is the one that is purely an absence.** The working group published the
requirements and the theory as Experimental RFCs in September 1999 and let
`draft-ietf-spki-cert-structure-05` expire
[@draft-ietf-spki-cert-structure; @ietf-spki-wg]. R-001 §5.5 reads this
structurally: the group "standardised the rationale and abandoned the format."
Nothing prevented the format being written. It was not written, and zero
deployment followed almost mechanically.

**(d) is the one no specification can supply.** An anchor set is an
institution: somebody must curate it, somebody must audit the curator, and
relying parties must obtain it without effort. X.509 has root programs. C2PA
built one in eighteen months under statutory pressure (§4.3). Sigstore has
Fulcio's root plus a small set of accepted OIDC issuers. SPKI's answer was that
each relying party is its own anchor — intellectually clean, and it leaves the
relying party with work to do before the first verification succeeds.

The cumulative effect is that SPKI asked **both** endpoints to do new work for
a benefit that arrived only once enough others had done the same. X.509 asked
one party to buy a certificate and gave the relying party a root store they
never touched. R-001 §5.7(b) is right that this is the blocker, and it is worth
being precise about why: it is not that key management is hard, it is that the
*payoff is deferred past the point where a rational adopter would stop*.

---

## 6. Failure to adopt: PICS

PICS is the more painful case, because R-001 §6.1 establishes that it was
**architecturally better** at the thing this project cares about — a
separately published, dereferenceable, self-describing vocabulary cited by URL
— and it still died.

R-001 §6.2 identifies two causes. This report takes them in order of how much
they should worry us.

**The supply side never materialised.** The GVU 10th WWW User Survey of April
1998 found roughly **82% of webmasters had rated none of their pages**, and
70.5% planned to rate none [@gvu-1998-webmaster-survey]. Both dominant
vocabularies depended on self-labelling: unpaid work, no payoff to the
labeller, and real liability exposure if the label was wrong. This is the
single most transferable finding in the failure analysis, and it generalises
past content labelling: **a provenance system whose statements must be
authored by a human, for no reward, does not get statements.** The supply-chain
stack escaped it by making CI the author.

**The politics consumed the standard's reputation.** After *Reno v. ACLU*
(1997) struck down the Communications Decency Act, PICS was repositioned as the
self-regulatory alternative to statute, and the civil-liberties response — the
ACLU's *Fahrenheit 451.2* [@aclu-fahrenheit-451-2] — argued that
ratings-and-blocking infrastructure would suppress controversial speech more
effectively than a statute could. W3C counter-argued [@pics-censorship-faq].

It is tempting for this project to file the second cause under "not our
problem," and that would be a mistake. The ACLU's argument was not that PICS
was badly engineered. It was that a general-purpose, cryptographically
enforceable mechanism for third parties to make machine-readable assertions
about content, consumed automatically by user agents, is a censorship
infrastructure regardless of its designers' intent. **That argument applies
without modification to a general-purpose mechanism for third parties to make
signed, scoped, delegable assertions about arbitrary subjects.** The design
this project is pursuing is closer to the thing the ACLU objected to than C2PA
is, because the label-bureau pattern — anyone may assert about anything, and
relying parties shop among assessors — is exactly what `R-M-07` and the
third-party statement model contemplate.

POWDER's end is the quieter warning. It reached Recommendation on 1 September
2009; eleven weeks later W3C retired PICS as superseded by it; and W3C's TAG
later proposed obsoleting PICS, CC/PP and POWDER together, recording that
POWDER's labelling function "did not take off as expected"
[@w3c-tag-obsolete-powder; @powder-description-resources]. R-001 notes that the
issue remained open awaiting a vote eight years on, which is its own adoption
evidence. **A technically improved successor to an unadopted standard inherits
the non-adoption**, because the thing that was missing was never in the
specification.

---

## 7. A four-condition model of uptake

The cases above support a compact model. A provenance or attestation system is
adopted at scale when four conditions hold simultaneously; the historical
record contains no counterexample found in this pass, and §10 says what would
falsify it.

**C1 — Near-zero marginal cost on the supply side.** Someone must produce
statements, and the cost of producing each one must approach zero, *or* a
forcing function must make the cost irrelevant.

**C2 — A wire format with a conformance target.** Implementers need something
to be correct against, and a body that says whether they are.

**C3 — A trust-anchor installation path.** The relying party must obtain a
starting point for evaluation without doing work.

**C4 — Near-zero marginal cost on the relying-party side.** Verification must
not require the relying party to construct, discover or order anything.

| system | C1 supply | C2 format+conformance | C3 anchor path | C4 relying party | adopted? |
|---|---|---|---|---|---|
| X.509 / WebPKI | ✅ CA sells it | ✅ PKIX + root programs | ✅ root stores | ✅ inherited | **yes** |
| SLSA / Sigstore / in-toto | ✅ CI, zero cost | ✅ predicates, cosign | ✅ Fulcio + OIDC issuers | ⚠️ identity is a CLI flag | **yes** (§3.2: partial) |
| C2PA | ✅ statutory + vendor | ✅ conformance program | ✅ 30-cert Trust List | ✅ validator ships the list | **yes, rising** |
| PICS | ❌ unpaid human labour | ⚠️ spec, no conformance regime | ❌ bureaus never appeared | ❌ user picks a service | **no** |
| SPKI/SDSI | ❌ every user a keyholder | ❌ format expired | ❌ none by design | ❌ prover supplies the chain | **no** |

The model's claim is that the ✅/❌ pattern, not technical merit, predicts the
outcome — and PICS is the test case, because on expressiveness it beats the
system that replaced it.

Two refinements the table hides. C1 and C4 are the same economic fact seen from
two ends, and a system failing both fails twice over, which is SPKI and PICS.
And C2 is the only condition a specification project can discharge by writing a
document; C1, C3 and C4 are discharged by institutions, defaults and
deployment.

---

## 8. Which failure modes this design still carries

This is the section `PLAN-0001` §6 requires: *"Any uptake story that does not
confront why the last attempt died is not worth writing."* The answer is worse
than comfortable.

### 8.1 Three of SPKI's five reasons are present today

**(a) No wire format, no conformance target — present, and it is DEC-002.**
ARCH-0001's encoding decision is open by design, `src/` is empty on purpose,
and `spec/vectors/` is a Fall 2026 deliverable not yet shipped. This is
*exactly* the state the SPKI working group was in when it concluded: a
well-specified rationale and no bits on the wire. The difference is that this
project knows it, has the gap on the critical path, and has D4/D5/D7 aimed at
it. The similarity is that intent is not a format. **Until `spec/vectors/`
exists and something third-party validates against it, this project has
reproduced SPKI's one purely-fixable failure.**

**(c) Path discovery externalised to the prover — present, and structural.**
ARCH-0001's reduction evaluates a presented set. RFC 2693 §6.3.4 handed the
client the job of finding and ordering the chain, which R-001 §5.7(c) calls
"fine for a grid job and hostile for a browser." The demo floor (D6) reduces a
*presented* chain, which is the same posture. Nothing in the architecture says
where a relying party obtains the statements it reduces.

**(d) No trust-anchor installation path — present, and the hardest.** A
key-centric design with local names has no root program and nothing to audit.
§4.3 measured what the alternative looks like: C2PA has 17 organisations and a
Certificate Policy. This project has unsigned local trust roots in a file
(`PLAN-0004`), which is correct for a research prototype and is not an
installation path.

Reason (b) — quadratic bootstrapping — is inherited in full, because it is a
property of key-centricity itself, which is the design's premise and not a
defect to be fixed. Reason (e) is historical and does not recur.

### 8.2 PICS's supply-side failure is the live risk

PICS died because 82% of the parties who had to author labels authored none.
The supply-chain stack escaped that by making CI the author at zero marginal
cost. **This project's statements are, today, authored by humans with a wallet.**
`PLAN-0004`'s product is a local wallet: a person holds keys, makes
attestations, delegates. For a research prototype and a demo that is right. As
an uptake story it is the PICS position — voluntary authorship, deferred
payoff, and liability if the statement is wrong — and the four-condition model
scores it ❌ on C1.

The mitigation that the evidence actually supports is **not** persuading humans
to author statements. It is the supply-chain pattern: find the place where a
statement is already being produced mechanically, and attach entitlement to it.
PyPI Trusted Publishing (§3.4) is the shape of the opportunity — scoped
delegation that every registry reimplements privately because no format offers
it.

### 8.3 The censorship objection applies, and silence is not a strategy

§6 argues that the ACLU's *Fahrenheit 451.2* objection transfers to any
general-purpose third-party assertion mechanism, and that this design is
*closer* to the objectionable pattern than C2PA, because third-party
assessment is a first-class goal rather than an omission.

PICS's reputational collapse took about a year and was not recovered. The
project's existing posture — `LIMITATIONS.md`, "proves origin and integrity,
not truth" — is necessary and does not address this, because the objection is
not that the mechanism lies. It is that a mechanism which reliably tells the
truth about who said what is a more effective instrument of suppression than
one that does not. The honest response is to state the dual-use property in
the published limitations, name the design features that bound it, and say
which are deliberate. §10 files this.

### 8.4 What would have to be true for this design to be adopted

Applying the model to the project rather than to history:

- **C2 is reachable this semester.** Close DEC-002, publish `spec/vectors/`,
  and get one implementation that is not ours to validate against it. This is
  the highest-leverage uptake action available and it is already the plan.
- **C1 is reachable only by changing who authors statements.** The target
  should be an existing mechanical producer, not a human.
- **C3 is not reachable by this project and should not be attempted.** The
  defensible position is to *ride* existing anchor sets rather than found one
  — which makes the WP2/WP3 mapping work (SPKI/SDSI ↔ native, in-toto ↔
  `ArtifactStatement`) strategically more important than it looks on the plan,
  because a mapping is how a design without an anchor path borrows one.
- **C4 requires naming where statements come from.** A resolver story — even
  "out of scope, and here is the interface" — closes the gap between "we reduce
  a presented set" and "a relying party can verify something."

None of this is a decision. ARCH-0001 §9.4 reserves architectural change to the
document, and `propose-arch` is the route; this report is input, not a diff.

---

## 9. What this feeds into D9

`PLAN-0001` §11 lists five segments. This report bears on their ranking rather
than their content, and two conclusions are worth carrying forward.

**Segment 3 (AI agent attestation) is strengthened, for a reason the plan does
not give.** The plan calls it "fastest-moving, least served." The uptake
evidence adds the better argument: agent action chains are **mechanically
produced** — an agent's delegation is emitted by software, not authored by a
person — which satisfies C1, the condition PICS failed and the wallet model
currently fails. The relevant drafts are in the library already
[@draft-mih-scitt-agent-action-capsule; @draft-asor-wimse-agent-delegation-chain;
@draft-hamr-oauth-agent-delegation; @draft-niyikiza-oauth-attenuating-agent-tokens].
The segment is attractive because it is the one where nobody has to be
persuaded to write anything down.

**Segment 1 (regulated supply chain) should be positioned against the
entitlement gap, not the SBOM mandate.** The CRA mandates existence in an
unnamed format (§4.1); competing on inventory is competing on a commodity. The
gap the evidence actually shows is §3.4's: every registry reimplements scoped
publishing authority privately. That is a concrete, named, repeatedly-solved
problem with no interoperable answer.

Segments 2, 4 and 5 are not assessed here. Segment 5 (archives and cultural
heritage) is the one this project's own library work exercises, and the
four-condition model predicts it scores poorly on C1 for the same reason PICS
did — worth confronting before it is chosen as a demo domain.

---

## 10. Open questions and follow-on work

**For review.** The four-condition model (§7) is this report's one original
analytical claim and the place to attack it. It would be falsified by a system
adopted at scale while failing C1 or C3 — the strongest candidate the author
could not resolve is OpenPGP's web of trust in specific communities (Debian
keyring), which may be an instance of C3 being satisfied *locally* rather than
absent. §8.2's recommendation would be weakened if the wallet model's authors
turn out to be organisations with compliance duties rather than individuals.

**Library follow-on, filed separately.** `pypi-trusted-publishers`,
`slsa-2026-mini-shai-hulud` and `c2pa-conformance-program` are stubs (§2) and
all three now have primary retrievals recorded in `sources.md`; they should be
ingested properly with digests and `bears_on`. Four sources retrieved fresh for
this report have no record at all and are listed in `sources.md` as ingestion
candidates, including the C2PA deployment guidance and the C2PA trust list.

**For ARCH-0001, via `propose-arch`, not here.** Whether the dual-use
property in §8.3 belongs in `LIMITATIONS.md`; whether a resolver interface is
in scope (§8.4, C4); and whether the WP2/WP3 mappings should be reframed as
anchor-borrowing rather than interoperability.

**Not attempted.** Practitioner interviews (`PLAN-0001` §11). Deployment scale
for Sigstore/Rekor and for C2PA at platform level — both are in
`unverified.md` with an account of why.

---

## References

Citation keys resolve to `library@93891c9`. Sources retrieved for this report
and not yet in the library are listed in full, with digests and retrieval
dates, in `sources.md`.

- `[@aclu-fahrenheit-451-2]`, `[@pics-censorship-faq]`,
  `[@gvu-1998-webmaster-survey]`, `[@powder-description-resources]`,
  `[@w3c-tag-obsolete-powder]` — PICS and POWDER
- `[@draft-ietf-spki-cert-structure]`, `[@ietf-spki-wg]`,
  `[@wang-2006-reducing-spki]`, `[@ellison-schneier-2000-ten-risks]` — SPKI
- `[@c2pa-2-4]`, `[@c2pa-conformance-program]`, `[@cscw-2023-provenance-trust]`,
  `[@moruzzi-2025-content-authenticities]`, `[@ide-2025-signals-of-provenance]`
  — content provenance
- `[@eu-ai-act-art-50]`, `[@ca-sb-942]`, `[@eu-code-of-practice-marking]`,
  `[@eu-cra-2024-2847]` — forcing functions
- `[@slsa-2026-mini-shai-hulud]`, `[@pypi-trusted-publishers]` — supply chain
- `[@draft-mih-scitt-agent-action-capsule]`,
  `[@draft-asor-wimse-agent-delegation-chain]`,
  `[@draft-hamr-oauth-agent-delegation]`,
  `[@draft-niyikiza-oauth-attenuating-agent-tokens]` — agent attestation
