---
schema: "archdoc/v1"
id: R-0001
title: "What a Signature Proves: A Survey of Digital Signatures and Attestation"
short_title: "Signatures and attestation survey"
description: "Academic survey classifying attestation systems by what they let a key assert, who may assert it, and where trust begins."
type: research
category: security
status: draft
version: "0.2.0"
date: "2026-09-26"
updated: "2026-09-26"
needs_review: true
reviewed: false
canonical_path: research/0001-signatures-and-attestation/report.md
backlog: R-001
---

# What a Signature Proves
## A Survey of Digital Signatures and Attestation

**Status: first draft, complete in structure.** All eight research areas have
reported. Every citation key below resolves to a record in `m-of-n/library`;
`sources.md` records the mapping and `unverified.md` is the publication gate
for claims that could not be sourced primarily.

---
## Abstract

A digital signature proves that a particular private key was used over
particular bytes. It establishes neither the identity of the keyholder, nor
their authority to make the statement, nor the truth of what the statement
says — and the definition that secured the primitive, EUF-CMA, explicitly
models the signer as an oracle that signs whatever it is asked.

This survey classifies attestation systems by how they answer the three
questions the signature leaves open — who holds this key, what may it say, and
where does trust begin — rather than by application domain. Fourteen systems
are placed on a five-axis taxonomy (subject, predicate, authority, scoping,
root) spanning X.509/PKIX, the PGP web of trust, SDSI/SPKI, PICS and C2PA, TCG
device attestation and IETF RATS, the in-toto/SLSA/Sigstore/TUF supply-chain
stack, and the macaroon/Biscuit/UCAN capability family.

The classification supports a single claim: **the signature is the solved part,
and systems diverge almost entirely on authority and scoping.** Four findings
follow. Monotone attenuation survived everywhere, but the algebra that made it
composable — SPKI's closed meet over authorization tags — did not. Scoped
delegation was deliberately removed twice, from PKIX in 2008 and from the
supply-chain attestation layer in the 2020s, buying adoption in both cases.
Content labelling regressed: PICS published its vocabulary as a
separately-published, dereferenceable, machine-readable document, while C2PA
enumerates its vocabulary in the specification, so an unknown assertion
degrades from "fetch the description and render it" to "signed opaque blob."
And no system in the survey localises *type* names, though SDSI localised
principal names thirty years ago.

The survey contributes an original measurement to close a gap in the
literature: across all 1,769 CCADB-disclosed Mozilla-program intermediate CA
certificates (retrieved 2026-09-26), **31 (1.8%) carry a `nameConstraints`
extension and only 2 mark it critical as RFC 5280 requires**, with 29 of the 31
issued by a single CA family. Out-of-band root-store scoping is applied to 1
root in 172. This is the deployment reality of the mechanism PKIX offered in
place of RFC 1422's mandatory name subordination rule.

It also reports the May 2026 npm compromise as the field's sharpest empirical
result: 84 artifacts carrying cryptographically valid provenance attestations
that correctly named the builder, repository, workflow and ref. Every "who
signed this" question was answered correctly, and the answer was useless.

---

## 1. Introduction

A digital signature proves that a particular private key was used over
particular bytes. That is all it proves. It establishes neither the identity of
the keyholder, nor their authority to make the statement, nor the truth of what
the statement says.

This is not a limitation that was discovered later and patched around. It is
what the definition says. Goldwasser, Micali and Rivest secured the primitive
by handing the adversary an **oracle** that signs whatever it is asked, without
judgement, and demanding security anyway (§2.4). The standard definition of a
secure signature scheme therefore *presupposes* that signatures are produced
over messages the key holder did not choose and may never have seen. Every
inference from "this signature verifies" to "someone meant this" is an
inference the cryptography explicitly declines to support.

Fifty years of systems have been built on top of that narrow guarantee, and
almost none of the engineering effort has gone into the signature itself. It
has gone into the three questions the signature leaves open:

1. **Who holds this key?** — the naming problem (§§4–5)
2. **What is this key entitled to say?** — the authorization problem (§§8–9)
3. **Where does trust begin?** — the root problem (throughout)

### 1.1 Approach

This survey classifies attestation systems by how they answer those three
questions rather than by application domain. The classification is the
contribution: it makes visible that systems which appear unrelated — an X.509
certificate chain, a TPM quote, an in-toto attestation, a PICS label — are the
same construction with different answers, and that they are **incompatible in
ways their specifications do not state**.

Eight domains were surveyed: signature foundations (§2), X.509/PKIX (§4),
decentralised naming (§5), content labelling (§6), device and platform
attestation (§7), software supply chain (§8), capability tokens (§9), and the
post-quantum transition (§10). §3 gives the taxonomy, §11 populates it, §12
states what remains open.

### 1.2 Method and sourcing discipline

Each domain was researched against primary sources — specification text, RFCs,
peer-reviewed measurement papers, incident reports — with every citation
verified rather than recalled. Two commitments follow from that and are visible
throughout the text.

First, **every citation in this survey resolves to a record in an open
bibliographic library**, published alongside the paper. A claim whose source is
not in the library is absent by construction, not by oversight.

Second, each research pass recorded explicitly what it *could not* establish,
and those items are collated in a companion register rather than smoothed into
the prose. Where a widely-repeated claim could not be traced to a primary
source, this survey either omits it or marks it contested — including several
claims that would have strengthened the argument. Examples appear at §2.6
(priority claims in early signature history), §6.3 (C2PA platform adoption),
and §10.5 (TPM post-quantum key-type mapping).

Where the literature had no answer, this survey measured. §4.5 reports an
original measurement of name-constraint prevalence across the Web PKI, which no
prior published work appears to provide.

### 1.3 What this survey argues

The central claim is that **the signature is the solved part.** The
cryptographic core is settled, standardised, and now has published
post-quantum replacements. What is not settled — and what every incident in
§§4.8, 8.1 and 8.6 turns on — is authority and scoping.

A secondary claim, developed in §7.8 and §11.3, is that the field conflates two
categorically different things under the single word *attestation*:
**delegation**, which passes authority between principals over time and needs
revocation; and **integrity-of-state**, whose subject is a snapshot and whose
hard problem is freshness. Their temporal structures are inverted, and packing
the second into data structures designed for the first is where attestation
bugs actually live.

---

## 2. Foundations: what a signature proves

### 2.1 The object

A digital signature scheme is a triple of algorithms over bit strings:
`Gen(1ⁿ) → (pk, sk)`, `Sign(sk, m) → σ`, and `Verify(pk, m, σ) → {0,1}`, with
correctness `Verify(pk, m, Sign(sk, m)) = 1` for all `m`.

That is the entire object. What is *absent* from the type signature is the
subject of this survey: there is no person, no name, no timestamp, no purpose,
no document. `m` is a byte string; `pk` is a byte string. Everything the word
"signature" carries in ordinary language is imported from outside by
convention, protocol, or law.

### 2.2 The idea precedes the mechanism

The concept was stated as a named open problem, with no solution, by Diffie and
Hellman [@diffie-hellman-1976]. Section 4, "One-Way Authentication," is the
founding text:

> In order to develop a system capable of replacing the current written
> contract with some purely electronic form of communication, we must discover
> a digital phenomenon with the same properties as a written signature. It must
> be easy for anyone to recognize the signature as authentic, but impossible
> for anyone other than the legitimate signer to produce it. … Since any
> digital signal can be copied precisely, a true digital signature must be
> recognizable without being known.

Two things in that passage deserve emphasis. First, the motivation is
**dispute**, not secrecy: "a message may be sent but later repudiated by either
the transmitter or the receiver." The signature was invented to settle
arguments between parties who already communicated, which is precisely the
attestation use case. Second, Diffie and Hellman had no trapdoor function, so
they described signing as "deciphering" with the secret key — the mechanism was
proposed as a consequence of a public-key cryptosystem that did not yet exist.

Rivest, Shamir and Adleman supplied the missing trapdoor [@rsa-1978]. It is
worth recording that textbook RSA signing — the scheme in the paper that named
the field — is *existentially forgeable*: RSA is multiplicative, so `σ₁ · σ₂ mod
n` is a valid signature on `m₁ · m₂`, and an adversary holding two signatures
obtains a third for free. This is the cleanest available demonstration that
intuition about signatures is not a security argument, and it is why the next
decade went into definitions rather than schemes.

### 2.3 Toward proof

Rabin [@rabin-1979-tr212] was the first to *reduce* forgery to a hard problem:
inverting his squaring-based function is equivalent to factoring `n`, which
RSA's security is not known to be. Rabin also saw the chosen-message danger
before it had a name:

> Without the suffix, an adversary may attempt to feed to P messages M for his
> signature, hoping to learn the factorization of n from the solution of
> x(x+b) ≡ C(M) mod n, which will be produced by P as his signature.

His fix — a random 60-bit suffix hashed with the message — is the ancestor of
every randomized padding since, from PSS to EdDSA's nonce derivation.

Lamport removed number theory entirely [@lamport-1979-one-way], building
signatures from any one-way function by publishing `f(x₀), f(x₁)` per message
bit and revealing the preimage. One-time only: a second signature leaks the
key. Merkle solved that with *tree authentication*
[@merkle-1979-thesis; @merkle-1980-protocols], compressing `2^h` one-time keys
into a single short public key with an authentication path per signature — the
construction that is now the post-quantum mainstream (§10).

ElGamal [@elgamal-1985] gave the first discrete-log signature and introduced
the per-signature nonce `k`, the family's load-bearing fragility: reuse or bias
recovers `sk` outright. Schnorr [@schnorr-1989-smartcards;
@schnorr-1991-jcryptology] compressed that structure by applying Fiat–Shamir to
an identification protocol.

### 2.4 The definition: GMR

Goldwasser, Micali and Rivest [@gmr-1988-adaptive], building on
[@gmy-1983-strong-signatures] and [@gmr-1984-paradoxical], did the decisive
work — which was not the scheme but the **taxonomy**. They crossed attack
strength (key-only → known-message → generic chosen-message → directed →
*adaptive* chosen-message) against break severity (total break → universal →
selective → *existential* forgery), then defined security as the strongest
attack against the weakest break.

The resulting game, **EUF-CMA**: the challenger runs `Gen`, hands `pk` to the
adversary, and gives it oracle access to `Sign(sk, ·)`. The adversary adaptively
queries `m₁ … m_q`, each chosen after seeing prior answers, then outputs
`(m*, σ*)`. It wins if `Verify(pk, m*, σ*) = 1` and `m* ∉ {mᵢ}`.

### 2.5 What the definition refuses to assert

This subsection is the foundation of the entire survey. A valid signature
licenses exactly one inference — *the signing algorithm was run with `sk` over
these exact bytes* — and even that only contrapositively, contingent on a
hardness assumption and on `sk` not having leaked. Everything else lies outside
the quantifier:

- **Identity.** No person appears in the game. Binding `pk` to a human or
  organisation is entirely external. §§4–5 are about that externality.
- **Intent.** The most under-appreciated point, and the model states it
  explicitly: *the signer is an oracle.* GMR hand the adversary a machine that
  signs whatever it is asked, without judgement, and demand security anyway.
  The definition therefore **presupposes** that signatures are produced over
  messages the key holder did not choose and may never have seen. A signature
  is evidence that a signing routine executed — not that anyone read,
  understood, or assented to the content. Every "digital signature = consent"
  argument in law and product design is asserting something the cryptography
  explicitly declines to provide.
- **Authority.** Nothing in `Verify` speaks to whether the key holder was
  permitted to make the statement. §9 is about that gap.
- **Truth.** `m` is an uninterpreted string.
- **Non-repudiation.** A legal and evidentiary concept, not a cryptographic
  one. EUF-CMA gives unforgeability *against outsiders*; it says nothing about
  key custody, coercion, or a signer who leaks their own key deliberately.
- **Uniqueness of `σ`.** EUF-CMA permits an adversary to produce a *different*
  valid signature on an *already-signed* message; excluding that is strong
  unforgeability (SUF-CMA), a distinct and stronger notion. Systems that treat
  `σ` as an identifier assumed a property the standard definition never
  promised.
- **Bytes, not meaning.** Hash-then-sign binds `H(m)`, so a hash collision
  severs the binding without touching the key.
- **Context.** Nothing binds `σ` to a protocol, a recipient, or even to `pk`,
  unless designed in — the root of cross-protocol reuse attacks. EdDSA
  [@rfc-8032] hashes the public key into the challenge specifically to close
  part of this gap.

### 2.6 The standards lineage

FIPS 186 standardises *algorithms*, and — consistent with everything above —
says nothing about identity, intent or semantics; that is PKIX's problem (§4).
The line runs FIPS 186 (1994, DSA only) [@fips-186] → 186-1 (1998, adds RSA)
[@fips-186-1] → 186-2 (2000, adds ECDSA) [@fips-186-2] → 186-3 (2009)
[@fips-186-3] → 186-4 [@fips-186-4] → 186-5 (2023) [@fips-186-5], which adds
EdDSA and deterministic ECDSA, deprecates binary-field curves, and **removes
DSA for signature generation**, retaining it only to verify legacy signatures.

> **Contested attributions.** Priority claims in this area are unusually
> tangled and the survey states them with care. GCHQ's Ellis, Cocks and
> Williamson anticipated the *encryption and key-exchange* halves of
> public-key cryptography (declassified 1997), but the available accounts hold
> that the GCHQ work did not conceive digital signatures — the signature idea
> is the part of "New Directions" whose priority is not contested. Claims of a
> "first digital signature algorithm" need qualifying: Lamport's construction
> appears in Diffie–Hellman §4 (1976), credited to Lamport, three years before
> his own report. The widely-repeated claim that Rabin's 1979 scheme "was the
> first to meet EUF-CMA" is a *retrospective* reading — the definition
> post-dates the scheme by nine years — and this survey does not assert it.
> See `unverified.md`.

---

## 3. A taxonomy of assertion

Every system in §§4–10 is an instance of one form:

> **A says B has property C**

with a signature binding the statement to A's key. Systems differ along five
axes, and those axes are how the rest of this survey is organised.

| axis | question | why it separates systems |
|---|---|---|
| **Subject** | what is B? | a key, a name, a document, a device state, a build |
| **Predicate** | what is C, and who defines it? | fixed by the specification, or declared in a separate published vocabulary |
| **Authority** | who may say it? | inherited root store · local policy · hardware vendor · out-of-band |
| **Scoping** | can authority be narrowed on delegation? | and if so, along what dimension — name, tag, capability, or not at all |
| **Root** | where does trust begin? | a root store you inherited, a keyring you built, a policy you wrote, silicon |

**The claim this taxonomy is built to test:** the signature is the solved part.
Systems diverge almost entirely on **authority** and **scoping**, and a
surprising number simply do not answer the scoping question at all — they
assume an out-of-band trust root and delegate nothing.

§11 populates this table for every system surveyed.

---

## 4. Naming and identity: X.509 and PKIX

### 4.1 A certificate format designed to log into a directory

ITU-T X.509 was first published in November 1988 as *"The Directory –
Authentication framework,"* a member Recommendation of the X.500 Directory
series [@itu-x509-1988; @itu-x509]. Its design assumption is load-bearing, and
it failed. X.509's naming type is the X.500 Distinguished Name, which
presupposes a single global Directory with one global DN namespace in which
every entity has exactly one canonical name. Gutmann's assessment
[@gutmann-2002-pki-not-dead] is blunt: "the original problem that X.509
certificates were designed to solve was access control to an X.500 directory,
[which] is nothing like the problem or problems that need to be solved today,"
and "since the concept of a global distributed directory… was never realised,
there's no clear idea where to fetch a certificate from." SPKI reaches the same
conclusion from the other side [@rfc-2693]: "The original X.500 plan is
unlikely ever to come to fruition."

The Internet's answer was a profile, not a redesign. RFC 5280 [@rfc-5280]
keeps X.509's ASN.1 and path-validation semantics and repurposes the container:
the identities that actually matter — DNS names, email addresses, IP addresses,
URIs — move into `subjectAltName`, and §4.2.1.6 concedes that a certificate may
carry an **empty** subject DN entirely. *The global namespace was abandoned in
practice while its syntax was retained.*

### 4.2 The design decision that removed scoped delegation

PKIX deliberately dropped the one thing its predecessor had that scoped
delegation. RFC 1422 [@rfc-1422] imposed a mandatory **name subordination
rule**: a CA could only certify entities whose names sat below its own in the
X.500 tree. RFC 5280 §3.2 describes why it was dropped — X.509v3 extensions
"obviate the need for the name subordination rule," yielding a "more flexible
architecture" in which:

> Name constraints may be imposed through explicit inclusion of a name
> constraints extension in a certificate, **but are not required.**

Scoped delegation went from a structural invariant to a CA-discretionary option
in a single design decision. This survey treats that sentence as the pivotal
primary-source fact in the area.

### 4.3 Path validation imports its trust decision

RFC 5280 §6.1.1 states plainly that "the trust anchor information is trusted
because it was delivered to the path processing procedure by some trustworthy
out-of-band procedure." The algorithm is a careful, well-specified procedure
whose first premise is supplied from outside itself — the §2.5 gap, relocated
into an API parameter.

The one genuinely sound piece of the design is step §6.1.4(g): a certificate's
`nameConstraints` **intersect** into `permitted_subtrees` and **union** into
`excluded_subtrees`, so constraints only ever tighten going down a path. This
is monotone attenuation, and it is the same shape as SPKI's tag intersection
(§9.3) and macaroon caveats (§9.2).

But `nameConstraints` processing sits *inside* the loop, fed only by
certificates in the path. The algorithm has no channel for the relying party's
own scoping of a trust anchor, and §6.2 leaves root-embedded constraints
advisory: "Implementations that use self-signed certificates to specify trust
anchor information are free to process or ignore such information." Making
trust-anchor constraints binding required RFC 5937 [@rfc-5937] — which is
Informational.

### 4.4 Name constraints are fail-open by construction

The mechanism is real, but its semantics default to permitting. RFC 5280
§4.2.1.10: "Restrictions apply only when the specified name form is present. If
no name of the type is in the certificate, the certificate is acceptable." The
Security Considerations concede the consequence directly:

> In general, using the nameConstraints extension to constrain one name form
> (e.g., DNS names) offers no protection against use of other name forms (e.g.,
> electronic mail addresses).

Worse, §4.2.1.10 declares the syntax and semantics for `otherName`,
`ediPartyName` and `registeredID` constraints "are not defined by this
specification" — so any newly defined `otherName` identity type escapes
existing constraints by default. That is not hypothetical: RFC 9598
[@rfc-9598] had to amend §4.2.1.10 to extend `rfc822Name` constraints to the
new `SmtpUTF8Mailbox` `otherName`, precisely because "legacy Certification
Authorities constrained to issue certificates for a specific set of domains
would lack corresponding UTF-8 constraints."

The CA/Browser Forum had to engineer around all of this, re-expressing "scoped"
as "explicitly exclude the universe," name form by name form: for a Technically
Constrained TLS Subordinate CA, if no `dNSName` is permitted the CA **must
include a zero-length `dNSName`** in exclusions, and if no IP is permitted, 8
and 32 zero octets [@cabforum-tls-br]. The Forum also had to relax RFC 5280
itself, permitting non-critical constraints for legacy compatibility — and the
S/MIME Baseline Requirements [@cabforum-smime-br] are franker still, allowing
this "until the `nameConstraints` extension is supported by Application
Software Suppliers whose software is used by a substantial portion of Relying
Parties worldwide." That is a 2023 standards document conceding the extension
is still not reliably supported.

### 4.5 An original measurement: how much scoping is actually deployed

The literature reports no prevalence statistic for name constraints in the Web
PKI. This survey therefore measured it [@survey-2026-nameconstraints-measurement].

**Method.** All 1,769 disclosed, unexpired, unrevoked intermediate certificates
in Mozilla's program were downloaded from CCADB's
`MozillaIntermediateCertsCSVReport` on 2026-09-26, parsed with
`openssl x509 -noout -text`, and counted for the `X509v3 Name Constraints`
extension. Root counts come from `IncludedCACertificateReportPEMCSV`.

| Measure | Result |
|---|---|
| Disclosed intermediate CA certificates | 1,769 |
| Carrying a `nameConstraints` extension | **31 (1.8%)** |
| `serverAuth`-capable intermediates | 1,613 — of which 31 constrained (**1.9%**) |
| Of the 31, marked critical as RFC 5280 requires | **2** |
| Issuer concentration | 29 of 31 from one CA family (HARICA) |
| Included roots / distinct CA owners | 172 / 50 (121 Websites bit, 91 Email bit) |
| Roots with a "Mozilla Applied Constraints" value | **3 of 172** — only **one** a positive scope |

Two readings follow. First, the scoping mechanism PKIX offers instead of RFC
1422's structural rule is deployed on **under 2%** of intermediates, and
correctly marked critical on **2 certificates in the entire disclosed set**.
Second, out-of-band root-store scoping — the escape hatch for §6.2's advisory
treatment — is applied to one root in 172, and is not portable: Go's bundle
does not carry it [@golang-61963].

Implementation quality remains poor. Five distinct Go `crypto/x509`
name-constraint CVEs were published within eleven months
[@go-nameconstraint-cves], including an excluded subdomain constraint failing
to prevent a leaf claiming `*.example.com`, multiple email constraints where
"only the last constraint will be considered," and a case-sensitivity bypass of
`excludedSubtrees`. OpenSSL's CVE-2022-3602/3786 buffer overflows were, per the
project's own post-mortem [@openssl-2022-email-overflow], "introduced as part
of punycode decoding functionality (currently only used for processing email
address name constraints in X.509 certificates)." NSS shipped a period in which
libPKIX silently did not enforce constraints at all [@mozilla-bug-856060].

### 4.6 Revocation: documented collapse, now formally conceded

RFC 5280 §3.3 states that "this profile does not require the issuance of CRLs."
§6.3.3 terminates with "if the revocation status has still not been determined,
then return the cert_status UNDETERMINED" — and nothing in RFC 5280 says what a
relying party must do with UNDETERMINED. **That undefined branch is where
soft-fail lives.**

Measurement confirms the collapse. Liu et al. [@liu-2015-revocation] found that
"no browser in its default configuration correctly checks all revocations and
rejects certificates if revocation information is unavailable," with mobile
browsers never checking at all and Chrome's CRLSet covering 0.35% of
revocations. Zhang et al. [@zhang-2014-heartbleed] found that three weeks after
Heartbleed, over 87% of vulnerable certificates had not been revoked. OCSP
Must-Staple [@rfc-7633] reached 0.02% of certificates
[@chung-2018-must-staple]. Langley's "Revocation doesn't work"
[@langley-2011-revocation; @langley-2014-revchecking] made the soft-fail
argument that justified replacing live checking with CRLSets and OneCRL.

The ecosystem has since capitulated and rebuilt. CA/B Forum ballot SC-063
[@cabforum-sc063] made OCSP optional and CRLs mandatory. Let's Encrypt shut its
OCSP responders down on 2025-08-06 [@letsencrypt-ocsp-eol], citing the privacy
leak. The IETF standardised the surrender in RFC 9608 [@rfc-9608], which adds a
`noRevAvail` extension and updates §6.1.3 so that "Step (a)(3) is skipped."
CRLite [@larisch-2017-crlite] finally shipped in Firefox 142.

**The honest summary: online revocation as specified never worked, and the
replacement is push-based local data structures plus certificates too
short-lived to need revoking.**

### 4.7 Certificate Transparency

RFC 6962 [@rfc-6962] and RFC 9162 [@rfc-9162] are **both Experimental**. RFC
9162 is exact about what CT buys: "The logs do not themselves prevent
misissuance, but they ensure that interested parties (particularly those named
in certificates) can detect such misissuance." CT is a detection and audit
control layered over a trust model it cannot fix.

One deployment fact matters for accuracy: **RFC 9162 has essentially no
deployment.** Apple's CT policy still names RFC 6962, and the live evolution
path is the non-IETF Static CT API / Sunlight specification, which keeps RFC
6962 semantics and changes only the serving architecture. A survey citing RFC
9162 as "the current CT standard" would be describing a document, not a system.

### 4.8 What the CA compromises demonstrated

DigiNotar is the flagship. Fox-IT's *Black Tulip* report
[@foxit-2012-black-tulip] documents perimeter breach on 17 June 2011, all eight
CA-management servers compromised, and **531** fraudulent certificates — not
the commonly cited "300+". The `*.google.com` certificate was used against
roughly 300,000 unique IPs, ~95% in Iran. **It was caught not by X.509 but by
Chrome's hardcoded key pinning.**

The pattern repeats with different mechanisms: Comodo (2011, via a compromised
RA), TURKTRUST (2013, again caught by Chrome pinning)
[@mozilla-2013-turktrust], ANSSI (2013, a government sub-CA in a
traffic-inspection appliance) [@mozilla-2013-anssi], Symantec (caught by CT,
escalating to full distrust) [@google-2017-symantec], WoSign/StartCom (2016)
[@google-2016-wosign], and continuing through Entrust (2024), distrusted for
"an observed pattern of compliance failures, unmet improvement commitments, and
the absence of tangible, measurable progress."

The common property is structural, not operational. Because name constraints
are optional and — per §4.5 — almost never present, **any** of the 121
TLS-trusted roots, or any of the 1,769 intermediates beneath them, can issue a
technically valid certificate for **any** name. Security is the minimum over
~50 organisations across many jurisdictions. EFF's SSL Observatory
[@eff-2010-ssliverse] named this in 2010: the trust model is "1 of N CAs (N is
large)," and "the security of HTTPS is only as strong as the practices of the
least trustworthy/competent CA."

**Every mitigation that actually caught these incidents — pinning, CRLSets, CT,
root-program distrust — sits outside RFC 5280.**

### 4.9 Assessment: does X.509 already solve scoped delegation?

**No — but the honest reason is narrower and more interesting than "the
mechanism doesn't exist," and this survey is careful to state the defensible
claim.**

Name constraints *are* a genuine scoped-delegation primitive. They are enforced
offline by the relying party, they tighten monotonically down a path, and they
need no third party at validation time. A claim that X.509 *cannot express*
scoped delegation is false and would be correctly rebutted by any PKIX
reviewer. This survey does not make it.

The defensible claim is about **defaults, enforceability and expressibility**:

1. **Optional by explicit design decision** (§4.2). The invariant was removed,
   not absent.
2. **Fail-open by default** (§4.4). Safety requires enumerating and explicitly
   excluding every name form, and new name forms escape old constraints.
3. **Not binding at the trust root** (§4.3). Root-store constraints are applied
   to 1 of 172 Mozilla roots and are not portable.
4. **Still not reliably enforced** (§4.5). Five Go CVEs in eleven months; a
   2023 CA/B Forum document still permitting non-critical constraints.
5. **Barely deployed** (§4.5). 31 of 1,769; 2 marked critical.

The deepest point is not a deployment statistic. In X.509, scoping is something
a **parent grants to a child**, expressed over a name form the parent chose,
and **the top of every chain is unconstrained by construction** — a relying
party has no in-format way to say "I trust this CA only for `example.com`."
That must live in root-store policy, out of band.

A design in which a principal *is* a key, and every name is interpreted
relative to its issuing principal, makes unscoped authority **inexpressible**
rather than merely discouraged. That is the real difference, and it is a
difference in what the format permits by default — not in whether scoping can
be written down at all.

## 5. Decentralised naming

### 5.1 The shared premise

PGP, SDSI and SPKI converge on two moves. First, the **principal is a key**,
not a name: SDSI 1.1 states flatly that "SDSI principals *are* public digital
signature verification keys," and that "two principals are taken as being the
same if and only if they have the same public key" [@sdsi-1-1]. Second, **names
are local**. SPKI argues that the names people actually use "are local names…
They do not need to be globally unique. Rather, they need to be unique for the
one entity that maintains that address book" [@rfc-2693].

Where X.509 asks *is this the certificate for `CN=Alice`?*, these systems ask
*is this key authorised, by a chain I can follow from a key I already hold?*

### 5.2 OpenPGP: less scoped delegation than its reputation suggests

RFC 4880 [@rfc-4880] was obsoleted by RFC 9580 [@rfc-9580] in July 2024, a
cryptographic modernisation (v6 keys, AEAD) that carries the trust machinery
forward **substantively unchanged**. That machinery is thinner than commonly
assumed. Two signature subpackets do the work: **Trust Signature** (type 5),
carrying a level (depth) and a trust amount, where level *n* delegates the
right to issue level *n−1*; and **Regular Expression** (type 6), a regex used
"in conjunction with Trust Signature packets (of level > 0) to limit the scope
of trust that is extended."

So PGP does have scoped, depth-limited delegation — but **the scope predicate
is a regex over a display string, not over a permission**. The delegation is
always of the same power (certify identities), narrowed only by which identity
strings it covers. There is no way to say "trusted to certify, but only for
signing releases." And RFC 9580 specifies **no trust-computation algorithm at
all**: the Trust packet "is used only within keyrings," is not exported, and
"the format of Trust packets is defined by a given implementation." The web of
trust is an implementation convention, never a standardised evaluator. Tooling
narrows it further — GnuPG exposes the wire format's arbitrary regex to users
as a domain filter only [@gnupg-key-management].

The empirical collapse is the decisive fact. Ulrich et al.
[@ulrich-2011-openpgp-wot] analysed a December 2009 keyserver snapshot: of ~2.7M
keys, the actual web of trust was **325,410 keys** across **240,283 strongly
connected components**, with the largest component only ~45,000 nodes — 14% of
WoT keys. Then in June 2019 the certificate-flooding attack
[@cve-2019-13050] exploited the append-only keyserver design; upstream
mitigation was to **stop importing third-party signatures by default**, and
distributions moved to keys.openpgp.org, which does not publish third-party
certifications [@keys-openpgp-org-faq]. The distribution channel for the web of
trust was deliberately shut off. PGP's answer to Zooko's triangle was, in the
end, an email-verifying directory.

### 5.3 SDSI and SPKI

SDSI's contribution is **linked local namespaces** [@sdsi-1-1]. Every principal
defines its own bindings — "the principal you call `alice-smith` may be
different from the principal I call `alice-smith`" — and names *chain* across
namespaces: `bob's alice`, extensible to `bob's alice's mother`. The stated
motivation is that X.509-style schemes "are both excessively complex and
incomplete," their complexity arising from "dependence on global name spaces."

SPKI [@rfc-2692; @rfc-2693] supplies the authorisation calculus and records the
merge explicitly: "Ron Rivest and Butler Lampson showed with SDSI 1.0 that one
can not only use local names locally, one can use local names globally. The
clear security advantage and operational simplicity of SDSI names caused us in
the SPKI group to adopt SDSI names as part of the SPKI standard."

The core objects are the **5-tuple** ⟨Issuer, Subject, Delegation, Authorization,
Validity⟩ and, separately, the **4-tuple** name certificate ⟨Issuer, Name,
Subject, Validity⟩. **Two layers: names resolve to keys, keys hold authority,
and neither is required to do the other's job.** §9.4 argues this separation is
the piece the modern field dropped and is now rediscovering.

Reduction and tag intersection are treated in §9.3, where they are compared
against the systems that replaced them.

### 5.4 RFC 9804: what survived

RFC 9804 [@rfc-9804] standardised SPKI's S-expressions in June 2025. Its own
§1.3 explains the 28-year gap: the S-expressions came from SDSI in 1996 and
were refined "during the merger of SDSI and SPKI during the first half of
1997," but the specification "was never actually submitted to the IETF."

The motive is **live interoperability, not revival**: these S-expressions "are
in active use today between GnuPG and Ribose's RNP." Two OpenPGP
implementations needed a citable spec for a private-key serialisation format.
RFC 9804 standardises **the encoding layer of SPKI and nothing else** — no
5-tuples, no delegation, no reduction. That is a precise measure of what
survived: the syntax did; the authorisation theory did not.

### 5.5 Why the SPKI working group shipped no standards-track output

The WG published two **Experimental** RFCs in September 1999 — the requirements
and the theory. The actual bits-on-the-wire document,
`draft-ietf-spki-cert-structure-05`, **expired and was never published**
[@draft-ietf-spki-cert-structure]; the WG is recorded as concluded
[@ietf-spki-wg]. Read structurally: the group standardised the *rationale* and
abandoned the *format*. A theory RFC with no wire format and no conformance
target cannot be implemented interoperably, which is close to a sufficient
explanation for zero deployment on its own.

### 5.6 Modern descendants

W3C DID Core [@w3c-did-core] is deliberately empty where SPKI was full: it
"does not presuppose any particular technology or cryptography," defines
`capabilityInvocation` and `capabilityDelegation` as *verification
relationships* whose semantics are left to methods and applications, and pushes
everything real into DID methods — of which there were 100+ experimental specs
at 1.0 publication [@w3c-did-extensions-methods]. That is a registry of
namespaces, not a resolution of the naming problem.

`did:key` [@did-key-method] is the purest SDSI position in modern dress:
"purely generative, requiring no look ups in a registry." It is also honest
about the cost — "Since `did:key` values are not stored in any registry, they
cannot be updated or deactivated." The key *is* the name, so there is no
rotation and no revocation.

Keybase took the opposite tack, *borrowing* namespaces by letting a key claim
Twitter/GitHub/DNS identities via signed, publicly-auditable proofs — "many
weak global namespaces, cross-checked" in place of "one strong global
namespace." It was acquired in May 2020 [@zoom-keybase-2020] and ceased to be
an independent identity layer.

**Was Zooko's triangle [@zooko-2001-names] resolved?** Honestly, no — it was
relocated. Consensus-ledger naming delivers all three properties for
first-come-first-served registration, but buys decentralised agreement with a
global consensus artefact, which is a global namespace without a corporate
registrar, and inherits squatting and Sybil exposure. SDSI's move was cleaner:
deny that a name must be global at all, accepting that "human-meaningful" is
only ever meaningful *to someone*.

### 5.7 Why none displaced X.509

Five concrete reasons, none of which is "ahead of their time":

**(a) No wire format, no conformance target** (§5.5). You cannot ship interop
against a rationale.

**(b) Bootstrapping is quadratic and the payoff deferred.** X.509 requires one
party to act; the relying party inherits a root store they never touch.
SPKI/PGP require *both* endpoints to hold keys and to have constructed a path.
Wang et al. [@wang-2006-reducing-spki] state it bluntly: such systems "have
seen limited deployment in the real world… because each user is required to
manage his/her own private/public key pair." Their proposed fix was to back
SPKI onto Kerberos — an admission that the key-per-user premise was the blocker.

**(c) Path discovery was externalised to the prover.** RFC 2693 §6.3.4 hands
the client the job of finding and ordering the chain. "Bring your own proof" is
fine for a grid job and hostile for a browser.

**(d) No trust-anchor installation path.** X.509's anchors live in a handful of
root programs, and those programs are the actual product. A key-centric scheme
has nowhere to install an anchor and no entity to audit. The 240,283-component
graph of §5.2 is what a trust fabric looks like without one.

**(e) X.509 removed the incentive to switch, from the inside.** Ellison and
Schneier [@ellison-schneier-2000-ten-risks] named the CA business model —
"They cost almost nothing to make, and if you can convince someone to buy a
certificate each year for $5, that times the population of the Internet is a
big yearly income." That rent was then destroyed *from inside X.509*: ACME
[@rfc-8555] made issuance free and automatic, and Certificate Transparency
[@rfc-9162] supplied the accountability that "who do we trust, and for what?"
demanded. X.509 also absorbed the delegation story — RFC 3820 [@rfc-3820] gave
grid computing restricted proxy certificates with `pCPathLenConstraint`, i.e.
SPKI's delegation bit and depth control, inside the incumbent format, on the
standards track. Once the incumbent is free, automated, audited and delegating,
the migration case evaporates.

## 6. Content labelling

Sections 4 and 5 concern assertions about *keys*. This section concerns
assertions about *content* — and it contains the survey's sharpest finding,
because the field solved a problem in 1996, abandoned it, and has not
recovered it.

### 6.1 PICS: the architecture worth recovering

PICS 1.1 was published as two W3C Recommendations on 31 October 1996
[@pics-1-1-services; @pics-1-1-labels], with signatures added by DSig 1.0 in
May 1998 [@pics-dsig-1-0]. The architecturally interesting move is a
separation. A **rating service** is "an individual, group, organization, or
company that provides content labels"; a **rating system** "specifies the
dimensions used for labeling, the scale of allowable values on each dimension,
and a description of the criteria used in assigning values."

The rating system is published *separately, as its own machine-readable
document*, under the MIME type `application/pics-service`, declaring for each
category a short wire name (`transmit-as`), a human-readable `name` and
`description`, and a value domain. A label then **cites its rating system by
URL** rather than carrying the vocabulary inline:

```
(PICS-1.1 "http://www.gcf.org/v2.5" labels on "1994.11.05T08:15-0500"
 until "1995.12.31T23:59-0000" for "http://w3.org/PICS/Overview.html"
 ratings (suds 0.5 density 0 color/hue 1))
```

The consequence is **late binding of meaning**. A user agent meeting `suds 0.5`
from a vocabulary it has never heard of can dereference the service URL,
retrieve the machine-readable description, and render a correct human-readable
interface — category name, scale, criteria — *without a software update and
without W3C having blessed that vocabulary*. The vocabulary is a resource on
the web, not a clause in a specification.

The second separation is **label bureaus**: "a computer system which supplies,
via a computer network, ratings of documents. It may or may not provide the
documents themselves." The distribution specification defines an HTTP query
protocol (`u=` for target URLs, `s=` for desired rating services) returning
`application/pics-labels`. Third parties could assert things about content they
neither authored nor hosted, and clients could **shop among assessors**.

### 6.2 POWDER, and how both failed

POWDER [@powder-description-resources] reached Recommendation on 1 September
2009, keeping PICS's premise that descriptions "are always attributed to a
named individual, organization or entity that may or may not be the creator of
the described resources," and adding an IRI-set algebra and an RDF/OWL mapping.
Eleven weeks later W3C retired PICS as superseded by POWDER.

**The two failed differently, and the difference matters.**

PICS did not fail technically; it was consumed by a political fight. After
*Reno v. ACLU* (1997) struck down the Communications Decency Act, PICS was
repositioned as the self-regulatory alternative to statute. The civil-liberties
response — the ACLU's *Fahrenheit 451.2*
[@aclu-fahrenheit-451-2] — argued that ratings-and-blocking infrastructure
would banish controversial speech more effectively than a statute could. W3C
counter-argued [@pics-censorship-faq]. The debate consumed the standard's
reputation.

Meanwhile the supply side never materialised. The GVU 10th WWW User Survey
(April 1998) found roughly **82% of webmasters had rated none of their pages**,
and 70.5% planned to rate none [@gvu-1998-webmaster-survey]. Both dominant
vocabularies depended on *self*-labelling: voluntary work with no payoff to the
labeller and real liability exposure if the label was wrong.

POWDER failed quietly — no controversy, no users. W3C's TAG proposed obsoleting
PICS, CC/PP and POWDER together [@w3c-tag-obsolete-powder], recording that
POWDER's labelling function "did not take off as expected." That issue remains
open awaiting a vote eight years on, which is its own adoption evidence.

The shared root cause: both were description infrastructures **with no forcing
function on either side**. Nobody had to label, and almost no user agent
consumed labels.

### 6.3 C2PA / Content Credentials

The current specification is Content Credentials 2.4 [@c2pa-2-4]. A
**manifest** is "one or more assertions (including content bindings), a single
claim, and a claim signature"; an **assertion** is "a data structure which
represents a statement either made by the signer or gathered at claim
generation-time, concerning the asset"; a **claim** is the "digitally signed
and tamper-evident data structure that references a set of assertions."
Embedding is via JUMBF superboxes. External manifests and **soft bindings**
allow a manifest to live apart from its asset and be recovered by perceptual
match "even if the underlying bits differ."

The UX Recommendations [@c2pa-ux-2-2] are a separate document — and are
**frozen at 2.2 while the technical specification has advanced to 2.4**. They
define three validation states (*well-formed*, *valid*, *trusted*, the last
requiring the signer to be on a supported Trust List), L1–L4 progressive
disclosure, and display recipes for degraded states. They explicitly warn about
the implied-truth effect of partial labelling and about ambiguous phrasing such
as "Made with AI."

### 6.4 The forcing function PICS never had

**EU AI Act Article 50** [@eu-ai-act-art-50] applies from 2 August 2026:
providers of AI systems generating synthetic audio, image, video or text must
mark outputs "in a machine-readable format and detectable as artificially
generated or manipulated." The European Commission's Code of Practice on
marking and labelling AI-generated content [@eu-code-of-practice-marking],
published 10 June 2026, points at C2PA as the digitally-signed-metadata
solution and references CAWG metadata assertions. **California SB 942** as
amended by AB 853 [@ca-sb-942] became operative 2 August 2026, deliberately
realigned to match the EU timeline, and extends obligations to large platforms
and capture-device manufacturers. Four national cyber agencies issued joint
guidance in January 2025 [@nsa-2025-content-credentials].

This is the decisive structural difference from PICS. **PICS asked webmasters
to label voluntarily and 82% declined. C2PA's labellers are model vendors and
device makers who now face statutory marking duties.**

### 6.5 Does C2PA reproduce the PICS separation?

**No. C2PA bakes its vocabulary into the specification.** This is the central
finding of this section.

The evidence is direct. §6.2.2 of the 2.4 specification states that "the list
of publicly known labels can be found in Chapter 18, *C2PA Standard
Assertions*" — and Chapter 18 enumerates the vocabulary **in the specification
document itself**: `c2pa.actions`, `c2pa.ingredient`, `c2pa.metadata`,
`c2pa.hash.data`, `c2pa.soft-binding`, `c2pa.thumbnail`, and, new in 2.4,
`c2pa.ai-disclosure` and `c2pa.environmental-sustainability`. Adding a category
means shipping a new version of the specification — and the record shows
exactly that: **2.4 was needed to add an AI-disclosure assertion, at the moment
regulation demanded one.**

C2PA does have an extensibility mechanism, but it is **namespacing without
self-description**. §6.2.1 provides entity-specific namespaces beginning with
the entity's Internet domain name, with a versioning convention. That gives
collision-free names. It does *not* give a dereferenceable, machine-readable
declaration of what the categories are, what values they permit, or how to
phrase them for a human — the four things an `application/pics-service`
document supplied. The specification defines no human-readable descriptions for
assertion labels at all; presentation is delegated to implementers via the
separate, version-lagging UX document. A validator meeting
`com.litware.something` can verify the signature over it and then **has nothing
to show the user**.

Compare the failure modes directly:

> In PICS, an unknown vocabulary degrades to *"fetch the description and render
> it."* In C2PA, an unknown assertion degrades to *"signed opaque blob."*

That is a real regression in extensibility, hidden behind the fact that C2PA's
cryptography is vastly better than DSig 1.0's.

**Partial recovery exists, outside the specification.** The Creator Assertions
Working Group, a DIF working group since March 2025, publishes assertion
definitions independently of C2PA [@cawg-identity-1-2], and the EU Code of
Practice cites CAWG alongside C2PA. This is institutionally the PICS pattern —
a separate body publishing a vocabulary that labels cite. But CAWG
specifications are **prose documents requiring hard-coded implementer support**,
not machine-readable descriptions a client can dereference at validation time.
Notably, the 2.4 technical specification makes no mention of CAWG or of any
external assertion registry.

**The label-bureau half is also unrecovered.** External manifests and manifest
repositories superficially resemble label bureaus, but the assertions in a
recovered manifest still come from the production chain that signed the asset.
There is no C2PA equivalent of the PICS `u=`/`s=` query — *"give me every
assertion any party has made about this asset, and let me choose whose
assessment I trust."* Third-party assessment — a fact-checker, a rights body, a
newsroom disputing an image — has no first-class place in the manifest model.
C2PA's trust model is a **Trust List of signers**, which answers "is this
signer accredited?" — a question about *keys* — rather than PICS's "which
assessor's vocabulary do I want applied?" — a question about *content*. A
system defined by assertions about content has quietly drifted back to the key
question.

### 6.6 Human factors: the demand side still looks like PICS

Three findings bear on whether any of this reaches a user.

**Provenance can reduce trust in truthful content.** A CSCW study (N=595)
[@cscw-2023-provenance-trust] found provenance lowered trust in deceptive
media, especially composites, but also *overcorrected*, shifting perceptions
away from truth for some non-deceptive media; incomplete or invalid validation
states significantly moved judgements. The authors conclude that users "confuse
media credibility with the orthogonal (albeit related) concept of provenance
credibility" — which is precisely the §2.5 confusion, arriving at the user
interface.

**Two coinages are worth attributing precisely.** In Moruzzi et al.
[@moruzzi-2025-content-authenticities], both "downward shift of trust" and
"human washing" are **participant coinages, not authors' constructs** — both
attributed to participant (30). Participants worried that overemphasising
AI-mediated content "could result in audiences dismissing legitimate media as
fake"; conversely "the absence of a label might lead to the assumption that no
AI was involved," which participant 30 called *human washing*.

**Indicators are unevenly perceivable.** Ide et al.
[@ide-2025-signals-of-provenance] (N=28: 15 sighted, 13 blind or low-vision)
document AI labels inaccessible to screen readers, low engagement with platform
labels in favour of unreliable content-based cues, and visual-only designs —
watermarks, overlay text — offering nothing to blind participants.

### 6.7 What this section recommends

The recoverable idea is not PICS's syntax, its politics, or DSig's
cryptography. It is the **self-describing, separately published,
dereferenceable vocabulary**: a machine-readable document declaring categories,
permitted values, and human-readable names and descriptions, cited by URL from
the label that uses it.

C2PA has the cryptography PICS lacked and, through Article 50 and SB 942, the
deployment mandate PICS never had. What it gave up is the one thing PICS got
right. The human-factors literature suggests the cost is concrete: "downward
shift of trust" and "human washing" are both failures of *interpretation*, and
interpretation is exactly what a published vocabulary with human-readable
descriptions is for.

> **Sourcing note.** Platform and newsroom adoption claims for C2PA circulate
> widely but could not be established from primary sources in this pass and are
> therefore not stated here. See `unverified.md`.

## 7. Device and platform attestation

Sections 4–6 concern assertions whose subject is a name or a document. This
section concerns assertions whose subject is a **machine state**, and it is the
only place in this survey where a verification succeeds *because of a property
of matter*.

### 7.1 The TPM lineage

TPM 1.2 [@tcg-tpm-1-2-main] and TPM 2.0 [@tcg-tpm-2-0-library-184] are two
design philosophies sharing a name. 1.2 hard-codes SHA-1 and RSA and fixes a
single key hierarchy; 2.0 is a *library* — algorithm-agile, with separable
platform, storage and endorsement hierarchies and a profile mechanism
[@tcg-pc-client-ptp] selecting what a given part must implement. It is
standardised as ISO/IEC 11889 [@iso-iec-11889-2015].

The attestation machinery is small and specific. The **Endorsement Key** is
device-unique and accompanied by a vendor-issued certificate: the anchor
asserting "a genuine part of model M holds this key." It is a restricted
*decryption* key and deliberately **not** a signing key, so that it cannot
itself serve as a tracking identity. Signing is done by **attestation keys**
(AK): restricted signing keys, `fixedTPM`/`fixedParent`, constrained by the TPM
to sign only TPM-generated structures. That restriction is load-bearing — an AK
cannot be tricked into signing an attacker-chosen blob that later reads as a
valid quote.

**PCRs** are append-only accumulators, `PCR_new = H(PCR_old ‖ measurement)`.
They cannot be set, only extended, so software that loads late cannot rewrite
the record of what loaded early. The measured boot chain
[@tcg-pc-client-pfp] has each stage measure the next before transferring
control, appending a parsable entry to an event log
[@tcg-integrity-event-log]. `TPM2_Quote` then signs a digest of selected PCRs
together with a caller-supplied nonce, producing the canonical hardware-rooted
statement: *the chip holding this AK observed this boot sequence, and it is
answering your challenge now.*

### 7.2 Direct Anonymous Attestation, and why it lost

The original design had a privacy hole. To be credible an AK must be linked
back to a certified EK — and the **Privacy CA** doing that linking sees the
EK↔AK mapping for every pseudonym a device ever uses.

DAA [@brickell-2004-daa] removed the online third party: a TPM joins once with
an issuer, obtaining a Camenisch–Lysyanskaya-style credential, then produces
zero-knowledge proofs of possession, so a verifier learns "a certified TPM
signed this" and nothing more. The subtlety is the **basename**: null basename
gives unlinkable signatures, while a verifier-supplied basename makes
signatures from the same TPM linkable *to that verifier only* — restoring
rate-limiting and rogue detection without enabling cross-verifier correlation.

**The historical verdict is that DAA largely lost**, and the survey records it
because the reason is instructive. Intel SGX began with EPID and moved to
ECDSA/DCAP [@intel-sgx-dcap-quotelib], where quotes chain to an Intel-rooted
certificate keyed to a specific platform — i.e. back to the Privacy-CA shape.
TDX and SEV-SNP make no anonymity claim at all. **Operational verifiability,
revocation and TCB recovery beat unlinkability.**

### 7.3 DICE: identity without a chip

DICE achieves layered identity with no dedicated security hardware
[@tcg-dice-hw-requirements; @tcg-dice-layering]. Immutable ROM holds a Unique
Device Secret, measures the First Mutable Code, derives
`CDI = KDF(UDS, measurement)`, then makes the UDS unreadable before handing
over control. Each layer repeats this.

The consequence deserves emphasis: **every layer's key is a deterministic
function of the device secret and every measurement below it.** Change any
firmware and the derived identity silently changes. Attestation becomes an
emergent property of key derivation rather than a signed log. Google's Open
Profile for DICE [@google-open-dice] is the widely deployed open
implementation.

### 7.4 IETF RATS: the vocabulary the field now borrows

RFC 9334 [@rfc-9334] supplies the role model. An **Attester** produces
**Evidence**; a **Verifier** appraises it against **Reference Values** (from a
Reference Value Provider) and **Endorsements** (from an Endorser), under policy
set by a **Verifier Owner**; the output is **Attestation Results**, consumed by
a **Relying Party**. Two topologies: the **Passport Model**, where the Attester
presents results itself, and the **Background-Check Model**, where the Relying
Party forwards Evidence to a Verifier.

RFC 9711 [@rfc-9711] gives Evidence and Results a concrete token format (EAT),
and CoRIM [@draft-ietf-rats-corim] — still an Internet-Draft — is the
unfinished other half: a signed CBOR container supplying the Verifier its
inputs, with CoMID *triples* for reference values, endorsed values, identity
and attestation keys.

### 7.5 Confidential computing and mass deployment

SGX identifies an enclave by `MRENCLAVE` (measured contents) and `MRSIGNER`
(signer), converting a locally-MAC'd report into a remotely verifiable quote
via a Quoting Enclave. TDX [@intel-tdx-whitepaper; @intel-tdx-dcap-quoting] is
**parasitic on SGX's infrastructure** — its TD Quoting Enclave is itself an SGX
enclave. AMD SEV-SNP [@sev-snp-primer-2026; @aws-snp-attestation] signs a
launch measurement with a VCEK derived from chip-fused secrets *and the current
TCB version*, certified ARK → ASK → VCEK; **firmware downgrade is expressed as
a different key, not a flag a verifier might ignore** — an elegant encoding of
the attestation worldview. Arm CCA [@draft-ffm-rats-cca-token;
@arm-cca-den0125] is the first of the four designed natively to RATS/EAT
shapes, binding a platform token and a realm token by carrying a hash of the
realm key as the platform token's nonce.

At mass scale, Android Key Attestation [@android-key-attestation] reuses X.509:
an attested key arrives with a chain to a Google root whose leaf carries a
`KeyDescription` extension with security level, authorisation lists, patch
level and `verifiedBootState`. Apple App Attest [@apple-app-attest] generates a
Secure Enclave key per app install, returning a CBOR attestation in WebAuthn's
shape. **Both collapse the RATS role separation: the silicon vendor is
simultaneously manufacturer, Endorser, root CA, and — via unpublished risk
signals — part of the Verifier.**

### 7.6 What a hardware root adds, and what it still does not prove

Four things are added, worth separating because they are usually conflated:

1. **Non-exfiltrability.** The private key was generated inside a die and
   provably cannot be copied out. A signature is evidence of *live interaction
   with one particular physical artefact*, not merely knowledge of a secret.
2. **A factory-injected anchor.** The manufacturer asserts this key was placed
   in a part built to a specification.
3. **Unforgeable-from-above measurement.** PCR extend is append-only; DICE
   destroys the UDS before mutable code runs; SNP's launch measurement is taken
   outside the guest. Later code cannot rewrite the record of earlier code.
4. **Freshness binding.** A nonce makes the statement present-tense rather than
   a replayable historical artefact.

What it does **not** prove:

- **Not that the code is good.** A quote signs a *hash*; its meaning comes
  entirely from reference values supplied out of band. Without them, a quote is
  an unforgeable statement about a number.
- **Not runtime integrity.** Measured boot is *load-time*. Code that is
  exploited but not modified produces identical PCRs.
- **Not physical security.** The sharpest irony in the section: the thing that
  makes hardware attestation special — its claim about physical reality — is
  exactly where its residual risk sits. It proves "a key inside a part of model
  M," not that the part is not decapped, glitched, or on a bus interposer.
- **Not *which* machine you are talking to.** Absent binding between the
  attestation key and the transport channel, an unhealthy attester can relay a
  challenge to a healthy machine. Attestation and channel establishment must be
  fused; they often are not.
- **Not survivable against its own root.** Root compromise is total and, in
  band, undetectable.

### 7.7 Is the RATS Endorser a vocabulary authority?

**Substantially yes, with two refinements that matter to this survey's thesis.**

The shared structure is exact: a signed token is syntactically verifiable but
semantically empty, and a third party external to both signer and consumer
supplies the interpretive frame. A PCR digest means "firmware 3.2.1 with secure
boot enabled" *only because a CoRIM said so*, exactly as a PICS label means
something only because a rating system said so (§6.1). In both cases the
interpretive authority, not the signer, is where the trust sits, and
compromising or mis-scoping it silently changes what every existing signature
means, **retroactively**.

**First refinement: RATS splits the role in two.** The Reference Value Provider
supplies "hash X *is* firmware Y" — a publisher-of-record function. The
Endorser supplies "this Attester's key belongs to a part with these
capabilities" — a *capability* claim about the device. RATS thus cleanly
separates **lexical** authority from **evaluative** authority, and most rating
system designs do not.

**Second refinement, and the more interesting one: RATS places the vocabulary
upstream of the consumer.** A conventional vocabulary authority publishes
definitions to everybody and every relying party interprets tokens itself. RATS
concentrates interpretation in the Verifier and hands the Relying Party a
pre-digested Attestation Result — an *opinion*, not claims-plus-dictionary. The
Relying Party can then be arbitrarily thin: it need not know what a PCR is.
This is a genuine architectural contribution and the correct answer to "who has
to understand the vocabulary."

It also **relocates the governance problem rather than solving it**. The
Verifier Owner's appraisal policy is now where "whose endorsements count" is
decided, and that policy is out of scope of every RATS document.

### 7.8 Integrity of state is not delegation

Hardware attestation does something categorically different from X.509 and
SPKI, and the difference is visible in the data structures.

X.509 [@rfc-5280] binds a *name* to a key, and the chain is a **delegation of
naming authority** — `pathLenConstraint` and `nameConstraints` exist to bound
how far and over what it may be passed on. SPKI [@rfc-2693] makes delegation a
first-class field. Both concern **authority flowing between principals over
time**.

An attestation has no principal-with-permissions as its subject and **no
delegation bit anywhere**. Its subject is a *snapshot*: this compute context
was in this state, at this instant, in answer to this nonce. Nothing is being
granted. Where chains appear — EK → AK, ARK → ASK → VCEK, DICE layer
certificates — they are **provenance or derivation chains**, not delegations.
DICE is the cleanest illustration: identity is *recomputed* per layer, so any
change in measured code produces a **different identity** rather than an
invalid signature. That is the opposite of delegation semantics, where the key
stays the same and only the permission narrows.

Two consequences follow.

**Temporal structure inverts.** Delegation credentials are long-lived and
therefore need revocation infrastructure — the hard, unsolved part of PKI
(§4.6). Attestations are intrinsically ephemeral and nonce-bound; their hard
problem is *freshness*. AMD's encoding of TCB version into VCEK derivation is
the attestation worldview in miniature: a stale TCB does not yield a revoked
credential, it yields a different key.

**And a hazard worth naming.** The industry keeps packing integrity-of-state
payloads into delegation containers: Android carries device state in an X.509
extension; DICE Certificate Profiles [@tcg-dice-cert-profiles] express
derivation chains as X.509. The syntax invites path-validation reflexes — check
the chain, check validity dates, trust the leaf — that are simply **wrong** for
state claims, where the only question that matters is whether measurements
match reference values *the certificate does not contain*. The container says
"delegation"; the payload says "snapshot." Verifier implementations that miss
this are where attestation bugs actually live.

## 8. Software supply chain

This section contains the survey's clearest demonstration that the signature is
not the hard part: a domain with excellent cryptographic hygiene, broad
industry adoption, and a documented 2026 attack in which **every signature
verified correctly and the answer was useless**.

### 8.1 The attacks that motivated the field

**SolarWinds / SUNBURST (disclosed December 2020)** is the decisive case
because every artifact-level control worked. The SUNSPOT implant
[@crowdstrike-sunspot] ran *on the build server*: it polled for `MsBuild.exe`,
confirmed the Orion solution was compiling, swapped a source file for a
backdoored copy, let MSBuild compile it, then restored the original. The
resulting DLL was signed with SolarWinds' genuine code-signing certificate. The
git repository was never touched; the divergence existed only inside one build
machine's working directory, for the duration of one compile.

> Source review would not have caught it, and signature verification
> *succeeded*. Signing attests provenance, not integrity of build inputs.

**event-stream (npm, 2018)** was a pure authorization failure. The maintainer
handed publish rights to a volunteer who asked by email — "he emailed me and
said he wanted to maintain the module, so I gave it to him"
[@event-stream-issue-116]. The injected payload decrypted only when the package
description matched one specific target application [@npm-event-stream;
@ghsa-event-stream]. **Nothing cryptographic was broken: the legitimate
publisher published.**

**xz-utils (2024)** [@cve-2024-3094; @freund-2024-xz; @tukaani-xz-backdoor]
attacked the *distribution of authority*. The activation glue existed **only in
the release tarballs, not in git**, while the payload sat in git disguised as
corrupt-input test fixtures. The account that cut the backdoored releases had
taken roughly **17 months** to travel from first patch to release authority,
aided by sockpuppets pressuring the maintainer about bus factor
[@cox-2024-xz-timeline]. Source-versus-artifact divergence is a first-class
threat, and so is patient social engineering of the delegation graph.

**Typosquatting** [@ohm-2020-backstabbers; @vu-2020-typosquatting] is a
*naming* attack: no signature is forged, no build is subverted, no provenance
claim is falsified. It sits entirely outside what attestation formats express.

### 8.2 in-toto, DSSE, SLSA, Sigstore, SCITT, TUF

**in-toto** [@in-toto-2019] introduced the **layout**, signed by the project
owner — whom the paper calls "the foundation of trust" — enumerating steps, the
KEYIDs authorised to sign each step's link metadata, a threshold, and artifact
rules chaining steps by material/product flow. The **Attestation Framework**
[@in-toto-attestation-v1] generalised this into Statement, Predicate, Envelope
and Bundle layers. Note one property: the Bundle "is not authenticated as a
whole," so attestations can be deleted, replayed or injected undetected.

**DSSE** [@secure-systems-lab-dsse] deserves close attention because its design
rationale is a substantive position, and this survey endorses it. Canonical
JSON has one practical and two theoretical problems: it requires the payload to
be JSON; "two semantically different payloads could have the same canonical
encoding"; and "it requires the verifier to parse the payload before verifying,
which is both error-prone—too easy to forget to verify—and an unnecessarily
increased attack surface." The conclusion is the **sign-the-bytes rule**:

> The preferred solution is to transmit the encoded byte stream exactly as it
> was signed, which the verifier verifies before parsing.

This inverts the usual order of operations — the parser is downstream of the
signature check, so a hostile payload never reaches it unauthenticated — and
signing `payloadType` inside PAE closes a cross-format confusion attack.
Against that, DSSE's `keyid` is "an optional, unauthenticated hint… MUST NOT be
used for security decisions," which §10.4 revisits as an agility problem.

**SLSA** [@slsa-1-2] defines build levels L0–L3 and, from v1.2, a Source track,
carrying a Provenance predicate and a Verification Summary Attestation that
lets consumers delegate verification to a trusted party. **Sigstore**
[@sigstore-2022] issues 10-minute Fulcio certificates binding an ephemeral key
to an OIDC identity, logging to the Rekor transparency log. **SCITT**
[@rfc-9943; @rfc-9942] defines Issuer → Signed Statement → Transparency Service
→ Receipt → Transparent Statement. **TUF** [@tuf-2010; @tuf-spec] is the
field's strongest authorization model: four top-level roles each with a
threshold, plus delegated targets roles scoped by path patterns, with
terminating and non-terminating delegation semantics.

### 8.3 What an SBOM proves

An SBOM is **a claim about composition, asserted by whoever generated it**.
Unsigned, it proves nothing. Wrapped in a DSSE envelope as an in-toto
predicate, it proves only that a particular key asserted that component list
for that artifact digest — not that the list is complete, not that it was
derived from the actual build, and not that the asserter was entitled to speak
for the artifact. An SBOM from post-hoc binary analysis and one from a hermetic
builder are **indistinguishable at the envelope layer**.

Decisively: **xz's backdoor would appear in no SBOM.** The component list was
correct; the *bytes of that component* differed from its source.

SPDX 2.2.1 is ISO/IEC 5962:2021 [@iso-iec-5962]; SPDX 3.0.1 [@spdx-3-0-1] is
current at the project. CycloneDX is standardised as ECMA-424 [@ecma-424].
NTIA's Minimum Elements [@ntia-2021-sbom-minimum] have been superseded by CISA
2026 guidance [@cisa-2026-sbom-minimum].

### 8.4 Regulation mandates existence, not entitlement

The **EU Cyber Resilience Act** [@eu-cra-2024-2847] puts the SBOM obligation in
Annex I, Part II, point (1): manufacturers must draw one up "in a commonly used
and machine-readable format covering at the very least the **top-level
dependencies**." No format is named; Annex VII places it in technical
documentation disclosable to regulators, and Annex II point 9 makes disclosure
to *users* optional. The CRA therefore mandates an SBOM's **existence**, one
level deep, in an unnamed format, primarily for regulators.

In the US, EO 14028 [@eo-14028] remains unrevoked, but the machinery moved: EO
14144 §2(a)–(b) [@eo-14144] would have required *machine-readable* secure
development attestations with validating artifacts — and EO 14306 [@eo-14306]
**struck those provisions** in June 2025, replacing the validation programme
with an industry consortium. The word "attestation" does not appear in EO
14306.

### 8.5 The analytical core: strong evidence layer, absent entitlement layer

**This domain has built an excellent evidence layer and almost no entitlement
layer — and, uncomfortably, the projects say so themselves.**

Almost every scheme takes the authorization decision as an *input*:

- in-toto's validation model takes `recognizedAttesters` as a **parameter** and
  emits attester names "to be fed into policy engine." The framework has no
  notion of which attester may speak about which subject or predicate type.
- SLSA states that consumers "MUST accept only specific signer-builder pairs"
  and that `builder.id` "MUST reflect the trust base that consumers care
  about" — but **the signer→builder mapping lives nowhere in the format.**
- Sigstore's threat model states that verifying a keyless signature "does not
  guarantee that the signer should be able to authenticate… or that the signer
  should have signed the given message." This is enforced concretely: `cosign
  verify` refuses keyless verification without `--certificate-identity` and
  `--certificate-oidc-issuer`. **The expected identity is a command-line
  argument.**
- SCITT is bluntest: "Authentication and authorization are implementation
  specific and out of scope of the SCITT architecture."

**Two genuine exceptions, and they are the oldest ideas in the field.** TUF
expresses scoped delegation properly — "who may sign for `django/*`" is a
first-class, verifiable, revocable statement. in-toto's *layout* binds specific
KEYIDs to specific steps with thresholds. But both bottom out in an assumed
root: the in-toto paper says "we assume that the public keys of project owners
are known to the verifiers" and "in-toto will not mandate how trust is
bootstrapped." **Delegation exists below the root, and nothing standardises the
root** — and the newer, far more widely deployed layer (attestations, SLSA,
DSSE, Sigstore) dropped the delegation machinery and kept only the envelope.

**SCITT is the interesting middle case and deserves credit.** It mandates that
Registration Policies and trust anchors "MUST be made Transparent and available
to all Relying Parties… by Registering them as Signed Statements." That makes
the authorization decision *auditable and versioned* — more than anyone else
offers. But it standardises only the obligation, not the language: policy is
transparent and **not interoperable**.

**Where authorization actually lives today is the registry, not the
attestation.** PyPI Trusted Publishing [@pypi-trusted-publishers] binds a
specific OIDC identity — repository, workflow, environment — to permission to
publish a specific project, minting a short-lived project-scoped token. That is
real scoped delegation, implemented by the package index, **out of band from
every format described above**. The ecosystems solved the problem the formats
declined to.

### 8.6 The 2026 empirical proof

In May 2026, attackers compromised 84 npm artifacts across 42 packages by
chaining a `pull_request_target` misconfiguration, Actions cache poisoning, and
OIDC token extraction from runner memory [@slsa-2026-mini-shai-hulud]. The
resulting packages carried **cryptographically valid provenance attestations
that accurately named the correct builder, repository, workflow and ref**,
signed through Sigstore with the legitimate OIDC token.

SLSA's own write-up concedes the point: "SLSA provenance records evidence. It
answers *what happened?* Policy and verification answer *was that good
enough?*" and "an 'expected builder' check would have passed, because the
pipeline was legitimate; it was the code running inside it that was not."

**Every "who signed this" question was answered correctly, and the answer was
useless.** That sentence is the strongest available empirical support for this
survey's thesis: the signature is the solved part.

### 8.7 Assessment

in-toto and SLSA are excellent *provenance* formats and poor *authorization*
formats, by design and by admission — evidence grammars deliberately agnostic
about policy. **That agnosticism is precisely why adoption succeeded**: a
format making no trust commitments could be adopted by GitHub, npm, PyPI,
Google and Debian simultaneously. But the field has industrialised the
production of signed statements while leaving "who was entitled to say that" to
a command-line flag, a registry configuration page, or a policy engine nobody
has standardised.

Three plausible recovery paths exist — TUF-style delegation reapplied to
attestation subjects (gittuf [@gittuf-2025] does exactly this for Git), SCITT
registration policies given an interoperable language, or VSAs as recursive
delegated authority. **None has consolidated.** Regulation compounds the gap
rather than closing it (§8.4).

## 9. Capability and delegation

### 9.1 Designation fused with authority

The capability model dates to Dennis and Van Horn [@dennis-vanhorn-1966], which
introduced the C-list: a per-computation "sphere of protection" in which naming
an object and being permitted to use it are the same act. Hardy
[@hardy-1988-confused-deputy] supplies the negative argument. A compiler,
invoked with a user-supplied output path, wrote to a billing file it alone had
rights to; **the caller designated the target, the deputy supplied the
authority, and the two came from different places.** Capabilities close that
gap by refusing to separate them.

This is the through-line for the section: a bearer token saying "the holder may
do X" but not "on this object, for this request" is a confused-deputy
generator.

### 9.2 The modern family

**Macaroons** [@macaroons-2014] are minted from a root key at the target
service; the signature is a nested chain of HMACs, each keyed by the previous.
Anyone holding the macaroon can append a **caveat** and re-chain, producing a
strictly narrower credential **without contacting the issuer**. First-party
caveats are predicates the target evaluates against request context;
third-party caveats embed a predicate encrypted for another service, requiring
a discharge macaroon.

The weakness is structural, and the authors state it plainly: verification
"requires knowledge of its root key—and since this key confers the ability to
arbitrarily modify the macaroon and its caveats, it cannot be widely shared."
**Every verifier is a forger.** Macaroons are also not third-party-auditable.
Fly.io's production deployment [@ptacek-2024-macaroons] is the one verified
attenuation deployment at scale.

**Biscuit** [@biscuit-spec-3-3] fixes the symmetry: an append-only sequence of
signed blocks, each carrying Datalog and a next public key, signed by the
previous private key. Verification needs only the root **public** key. Scoping
rules do the security work — a later block cannot make an earlier check pass.

**UCAN** [@ucan-1-0] names principals by DID and chains delegations by
reference, each restating or attenuating the parent, with hierarchical command
paths giving containment. **ZCAP** [@zcap-ld] expresses the same idea in
JSON-LD with `parentCapability` chains — and remains a W3C CCG draft, never a
Recommendation.

**OAuth, for contrast** [@rfc-6749; @rfc-6750; @rfc-9068], gives the client no
power to narrow: §3.3 says the authorization server "MAY fully or partially
ignore the scope requested by the client." OAuth's delegation primitive is
**re-issuance by an authority**, not holder-side attenuation — the opposite
design point. RFC 9396 [@rfc-9396] adds structured authorization details.

Proof-of-possession is an **orthogonal axis**: RFC 7800 [@rfc-7800] and DPoP
[@rfc-9449] narrow *who may present*, not *what is authorized*. Biscuit and
macaroons attenuate without PoP; DPoP does PoP without attenuation.

**Agentic delegation, 2026.** Three active individual Internet-Drafts
[@draft-niyikiza-oauth-attenuating-agent-tokens;
@draft-asor-wimse-agent-delegation-chain; @draft-hamr-oauth-agent-delegation]
apply offline holder-side attenuation to AI agent chains. None is
WG-adopted. Notably, the first cites Dennis 1966 and macaroons but **not**
SPKI; the second cites SPKI as a "historical standards-track ancestor."

### 9.3 Intersection versus accumulation

SPKI [@rfc-2693] does something none of these do. Its §6.3 reduction rule
composes two 5-tuples into one, and `AIntersect` is a **closed binary operation
on authorization tags** — the intersection of two authorizations is itself an
authorization of the same kind, computed element-wise over `(*)`, `(* set …)`,
`(* prefix …)`, `(* range …)` forms. Two consequences follow: **authority forms
a meet-semilattice with a computable meet**, and a chain of N certificates
**reduces to a single 5-tuple**. The chain is evidence, not payload.

**Nothing in the modern family does this.** Every one accumulates, then checks
containment:

| System | Attenuation operation | Verification |
|---|---|---|
| Macaroons | append caveat, re-chain HMAC | evaluate conjunction of predicates against request |
| Biscuit | append signed block of Datalog checks | run all checks plus authorizer policies |
| UCAN | new delegation referencing parent proof | command-path containment at execution |
| ZCAP | new zcap with `parentCapability` | child's `allowedAction` ⊆ parent's |
| Attenuating-token draft | derive token with narrower constraint map | normative `subsumes` per constraint type |
| WIMSE draft | new hop | scope covered, bounds tighter, expiry ≤, depth ≤ |
| **SPKI** | **intersect tags** | **reduce chain to one tuple** |

The attenuating-token draft is worth singling out because it **independently
reinvents most of SPKI's tag algebra** — its constraint vocabulary (`exact`,
`range`, `one_of`, `not_one_of`, `contains`, `subset`, `wildcard`, `all`,
`any`) is close to isomorphic to SPKI's `*`-forms, and it imposes a
decidability requirement on extensions. But its normative primitive is
`subsumes(C, P)`, a **decision procedure**, not a **meet** computing `C ⊓ P`.
The partial order is there; the lattice operation is not exposed. That is a
real, implementable gap: on that constraint fragment the meet *is* computable,
and computing it would let a chain collapse to one normalised token.

**Why did the field abandon intersection?** Not oversight — a semantic shift.
SPKI tags describe a *static permission space*, closed under meet.
Macaroon-style caveats describe a *dynamic admissibility predicate over request
context*: `time < T`, `ip = …`, or a third-party discharge obligation. You
cannot intersect "holder proves membership in group G at service A" into a tag,
because it is not a tag — it is deferred evidence. Once caveats are arbitrary
predicates, the meet degenerates to conjunction, and conjunction has no normal
form. Biscuit makes this maximally explicit: a Datalog program's authority is
defined only extensionally, relative to an authorizer's facts. You can ask *is
this request permitted?* but not *what does this token authorize?* — a question
SPKI could answer in closed form.

The price is paid in **size** (monotone growth, versus SPKI's compression to a
single tuple) and in **static analysis** (no offline "is token A weaker than
token B?" without a solver).

### 9.4 Naming: feature or gap?

These systems delegate to keys and mostly decline to say who the keys are.
Macaroons and Biscuit name no subject at all. UCAN and ZCAP do name principals,
and that is where they take the most criticism. The 2026 drafts bind hops by
key while explicitly disclaiming identity.

**The case for it being a feature** is the original argument: the confused
deputy is fixed by designating authority *with* the request, not by asking the
deputy "who are you." Unnamed keys also give privacy, offline verification, and
clean composition.

**The case for it being a gap** is that four things the deployed world wants
all turn out to be naming problems in disguise. **Revocation**: you cannot
revoke an authority you cannot name — hence status lists and short expiries.
**Rotation**: a key is not a stable identity. **Accountability and audit**: the
entire 2026 agentic literature is about *delegation provenance* — showing an
auditor which human sits at the root of a chain — and a chain of ephemeral
keys cannot answer that. **Organizational policy**: "anyone in group G" is
inexpressible over raw keys; macaroons smuggle it back via third-party caveats,
Biscuit via authorizer-supplied facts.

**SPKI, again, had the better architecture, and it is the piece the field
dropped.** RFC 2693 is *two* systems: 5-tuples carrying authorizations over
keys, and SDSI 4-tuple name certificates resolving locally-meaningful names to
keys, with names usable as subjects in authorization tuples. Two layers, and
neither required to do the other's job. Macaroons, Biscuit and the agent drafts
collapsed to one layer and are now rediscovering, under the banner of
provenance, that they need the second.

This survey's assessment: **the omission is an *unbundling*, not a flaw in the
capability model — but it is an unbundling the ecosystem has not re-bundled,
and the 2026 agentic drafts are where the bill is coming due.**

> **Scope note.** The claim that no surveyed system computes a true meet was
> checked against macaroons, Biscuit, UCAN, ZCAP and the three 2026 drafts. It
> is stated as "none of the systems surveyed here," not as a universal claim.

## 10. Post-quantum transition

### 10.1 Why signatures are not "harvest now, decrypt later" — except where they are

Shor's algorithm [@shor-1994; @shor-1997] breaks RSA, ECDSA and EdDSA. But the
migration *urgency* differs structurally between confidentiality and
authenticity, and conflating them produces bad roadmaps.

Encryption is **retroactively** breakable: a ciphertext recorded today can be
decrypted in 2040. Signatures, in the ordinary case, are not — a forgery
produced in 2040 cannot change the outcome of a verification that happened in
2026. Authentication is evaluated live, so the deadline is "before a
cryptographically relevant quantum computer exists," not "before the data is
captured."

**That reprieve has two carve-outs, and both are exactly where attestation
lives:**

1. **Trust anchors that cannot be rotated.** A root CA key, or a TPM
   endorsement key fused at manufacture, is a public key published today that
   must still be trustworthy in 2045. It is harvested now and broken later, in
   precisely the HNDL sense.
2. **Artifacts still being verified after the break.** An attestation signed in
   2026 and checked in 2050 is, at that verification event, indistinguishable
   from a signature forged in 2050.

The mitigation for (2) is not a bigger signature. It is **independent evidence
that the signature existed before the break** — timestamps and transparency
logs, which can themselves be hash-based and therefore quantum-resistant.

### 10.2 What is standardised

NIST published FIPS 203 [@fips-203], **FIPS 204 (ML-DSA)** [@fips-204] and
**FIPS 205 (SLH-DSA)** [@fips-205] on 13 August 2024. **FN-DSA (FIPS 206) is
not final** as of September 2026 and should not be treated as available.

SP 800-208 [@sp-800-208] approves the *stateful* hash-based schemes LMS
[@rfc-8554] and XMSS [@rfc-8391], and requires key generation and signing to
occur in a hardware module that cannot export secret keying material.
Statefulness is dangerous because each one-time key may be used exactly once:
reusing an index — from a restored VM snapshot, a database rollback, a
replicated HSM — leaks enough to forge, with **no cryptographic recovery; the
failure is total and silent**. CNSA 2.0 [@cnsa-2-0] nonetheless designates
LMS/XMSS for software and firmware signing, where signing is rare, centralised
and hardware-controlled.

NIST IR 8610 [@nistir-8610] advanced nine candidates to a third round in May
2026, hedging against a lattice monoculture; nothing from that track is
deployable within this survey's horizon.

### 10.3 Sizes, and why they bite attestation specifically

Against Ed25519's 32-byte public key and **64-byte signature**:

| Scheme | Public key | Signature | Sig ratio |
|---|---|---|---|
| Ed25519 | 32 | 64 | 1× |
| ML-DSA-44 | 1,312 | **2,420** | ~38× |
| ML-DSA-65 | 1,952 | 3,309 | ~52× |
| ML-DSA-87 | 2,592 | **4,627** | ~72× |
| SLH-DSA-128s | 32 | **7,856** | ~123× |
| SLH-DSA-192s | 48 | 16,224 | ~254× |
| SLH-DSA-256f | 64 | **49,856** | ~779× |

A TLS handshake signature has a security lifetime of milliseconds and pays for
size in a round trip. **An attestation has the inverse profile**: size is paid
once at creation and stored forever, while the verification event may be
decades away. That inverts the algorithm choice. For a 2050 verification,
SLH-DSA is the better fit **on assumptions** — its security rests only on a
hash function, with no structured-lattice assumption that might not survive 25
years of cryptanalysis — and the worse fit on size. Its 32–64 byte public keys
are ideal for trust anchors burned into ROM; its 7.8–49.9 KB signatures are
hostile to per-step in-toto attestations and embedded C2PA manifests.

Migration deadlines: NIST IR 8547 ipd [@nistir-8547] deprecates 112-bit ECDSA
and RSA after 2030 and disallows ECDSA, EdDSA and RSA at any strength after
**2035**. Composite signatures [@draft-ietf-lamps-pq-composite-sigs] are the
pragmatic PKI transition vehicle, at the cost of stacking both sizes.

### 10.4 Agility by omission is not agility

DSSE explicitly places "no restriction on the signature algorithm or format"
and treats `keyid` as an *unauthenticated hint*; the in-toto envelope
specification [@in-toto-envelope-v1] says implementations "SHOULD NOT require
the inclusion of signing key algorithms in the signature."

This survey argues that is a defect rather than flexibility. It permits
algorithm confusion, and — more importantly — **it cannot express "at least N
of the threshold signatures must be quantum-resistant."** A 3-of-5 root holding
two ML-DSA and three Ed25519 keys is *not* quantum-resistant, and no envelope
in the supply-chain stack can say so.

Two further consequences the field has not modelled. **Verifier longevity**:
verification code for ML-DSA and SLH-DSA must exist and be correct in 2050,
against parameter sets still being extended. And **timestamping becomes a
first-class requirement, not an option** (§10.1).

### 10.5 Who has a stated path

| System | Stated path? | Evidence |
|---|---|---|
| **TPM / TCG** | **Yes — strongest** | Library spec v1.85 (March 2026) integrates ML-KEM and ML-DSA [@tcg-tpm-2-0-library-185]. Caveat: silicon already deployed with RSA/ECDSA EKs fused at manufacture cannot be upgraded, and those EK certificates anchor the device for its whole life. |
| **SCITT** | **Weakened** | Draft-09 said agility "enables the gradual transition to stronger algorithms, including e.g. post-quantum signature algorithms." In the published RFC 9943 [@rfc-9943], §9.6 is reduced to one sentence, and the words "quantum" and "post-quantum" **do not appear anywhere in the RFC** — despite receipts being explicitly long-lived. |
| **in-toto / TUF / Sigstore** | **No spec path; implementation-led** | Movement is entirely in the surrounding ecosystem — TUF TAP 21 [@tuf-tap-21] adds an ML-DSA signing scheme; `securesystemslib`, gittuf and Sigstore threads are open. |
| **C2PA** | **Genuine gap — the clearest finding** | "Quantum" appears **zero times** in specifications 2.1–2.3; §13.2.1's allowed algorithms are ES256/384/512, PS256/384/512 and Ed25519 — all Shor-breakable — and "the deprecated list is empty." Meanwhile the spec's own model is that timestamped manifests remain valid **indefinitely**. |

The C2PA finding deserves the emphasis. **A provenance system whose entire
value proposition is long-horizon trust in media has committed to
decades-long verification using exclusively quantum-vulnerable algorithms, with
no stated migration path and no deprecation signal.** Per §10.1's carve-out
(2), this is the worst combination of properties in the survey.

The overall pattern: hardware has moved; software supply chain is moving
bottom-up through implementations while its specifications stay silent;
transparency has agility but dropped its explicit PQ language on the way to
RFC; and content provenance has not engaged at all.

> **Sourcing note.** The C2PA claim is stated as "no stated migration path in
> the published specification," which is what the evidence supports; whether
> non-public roadmap discussion exists could not be established. Likewise the
> TPM v1.85 key-type mapping rests on secondary reporting. See `unverified.md`.

## 11. Comparative analysis

### 11.1 The taxonomy populated

| System | Subject (B) | Predicate (C), and who defines it | Authority | Scoping on delegation | Root |
|---|---|---|---|---|---|
| **X.509 / PKIX** | a name (DN, then SAN) | "this key belongs to this name" — fixed by profile | inherited root store | `nameConstraints`, **optional, fail-open**, 1.8% deployed | root program, out of band |
| **PGP web of trust** | a key + UserID string | "this UserID belongs to this key" — fixed | local keyring | trust level (depth) + **regex over display string** | keys you chose |
| **SDSI / SPKI** | a key, or a local name | authorization tag — **defined by the issuing key** | the issuing key itself | **tag intersection** (closed meet) + delegation bit | your own key |
| **PICS** | a document (URL) | **separately published, dereferenceable vocabulary** | any rating service; client chooses | n/a (no delegation) | client's chosen bureau |
| **C2PA** | a media asset | assertion label — **enumerated in the spec** | Trust List of accredited signers | n/a | conformance program |
| **TPM / RATS** | a machine state snapshot | measurement vs. **reference values (CoRIM)** | manufacturer + Verifier Owner policy | **none — no delegation bit** | silicon, at manufacture |
| **DICE** | a layer's identity | implicit: identity *is* the measurement | derivation from UDS | n/a — identity regenerated per layer | immutable ROM |
| **in-toto / SLSA** | an artifact digest | predicate type — extensible by URI | `recognizedAttesters`, **a parameter** | layout binds KEYIDs to steps (below root) | assumed; explicitly unspecified |
| **TUF** | a target path | "this role may sign these paths" | root role, with thresholds | **path-pattern delegation, terminating or not** | root role, out of band |
| **Sigstore** | an artifact digest | OIDC identity in a 10-minute cert | **a command-line flag** | none | Fulcio root via TUF |
| **SCITT** | a statement about an artifact | issuer-defined | Registration Policy, **transparent but not interoperable** | none standardised | TS operator |
| **Macaroons** | bearer (no subject) | caveat predicates over request context | root key holder | **append caveat**; every verifier is a forger | the target service |
| **Biscuit** | bearer (no subject) | Datalog checks | root public key | append signed block; scoped fact visibility | root keypair |
| **UCAN / ZCAP** | a DID | command path / `allowedAction` | parent delegation | restate-or-attenuate, containment-checked | a DID, method-dependent |

### 11.2 The claim the taxonomy was built to test

§3 stated it: *the signature is the solved part; systems diverge almost
entirely on authority and scoping.* The table supports it, and sharpens it into
four findings.

**Finding 1 — the Subject and Predicate columns are diverse and largely
unproblematic; the Authority and Root columns are where every system either
punts or hard-codes.** Read the Authority column downward: "inherited root
store," "a parameter," "a command-line flag," "assumed," "out of scope of this
document." Four of the most widely deployed systems in the table locate the
authorization decision *outside the format entirely*. §8.5 documents that the
supply-chain projects say so in their own specifications.

**Finding 2 — monotone attenuation is the one idea that survived everywhere;
the algebra that made it composable did not.** X.509's `nameConstraints`
intersect-and-union (§4.3), SPKI's `AIntersect` (§9.3), macaroon caveats,
Biscuit blocks, UCAN's restate-or-attenuate: every serious system narrows
monotonically. But only SPKI made authority a **meet-semilattice with a
computable meet**, letting a chain reduce to a single tuple. Everyone else
accumulates and checks containment. §9.3 argues the abandonment was a semantic
shift rather than an oversight — once caveats became arbitrary predicates over
request context, the meet degenerated to conjunction — and that the 2026
agentic drafts have independently reinvented most of the tag algebra without
exposing the lattice operation.

**Finding 3 — scoped delegation was deliberately removed twice, in two
different decades, from two different fields.** RFC 1422's name subordination
rule was a structural invariant; RFC 5280 §3.2 made it optional and the result
is 1.8% deployment (§4.5). in-toto's layout and TUF's delegated targets express
real scoped delegation; the far more widely adopted attestation/DSSE/SLSA layer
kept the envelope and dropped the delegation machinery (§8.5). In both cases
the removal bought adoption — a format that makes no trust commitments is
adoptable by everyone simultaneously — and in both cases the bill arrived later
as an attack that verified correctly.

**Finding 4 — the predicate column contains a regression the field has not
noticed.** PICS in 1996 published its vocabulary as a *separately published,
dereferenceable, machine-readable document with human-readable descriptions*,
so an unknown vocabulary degraded to "fetch the description and render it"
(§6.1). C2PA enumerates its vocabulary **in the specification**, so an unknown
assertion degrades to "signed opaque blob" (§6.5). RATS is the one modern
system that gets this right, and it does so by a different route — it puts the
vocabulary *upstream of the consumer* in the Verifier, handing the Relying
Party an opinion rather than claims-plus-dictionary (§7.7).

### 11.3 Two categorical distinctions the field conflates

**Delegation versus integrity-of-state.** X.509 and SPKI chains pass *authority
between principals over time*, and therefore need revocation — the hard,
unsolved part of PKI (§4.6). Attestation chains are *provenance or derivation*
chains whose subject is a snapshot; nothing is granted, and the hard problem is
freshness, not revocation (§7.8). The two have inverted temporal structures,
and the industry routinely packs the second into containers designed for the
first — Android's device state in an X.509 extension, DICE derivation chains as
X.509 — inviting path-validation reflexes that are simply wrong for state
claims.

**Provenance versus entitlement.** SolarWinds, event-stream and Mini
Shai-Hulud (§8.1, §8.6) are all cases where provenance was recorded correctly
and entitlement was the actual failure. The field has industrialised the first
and standardised almost none of the second.

### 11.4 What has never been localised

SDSI's contribution was to localise **principal names**: a name is interpreted
relative to the key that defined it, so a global namespace is unnecessary
(§5.3). Nothing in this survey localises **type names**. Every system in the
table either fixes its predicate vocabulary in a specification (C2PA, X.509,
PGP), allocates it from a registry (in-toto predicate types, COSE algorithms),
or declines to define one at all (DSSE, macaroons).

PICS came closest by making the vocabulary a dereferenceable web resource, but
its vocabulary was still owned by a *service*, not by a key, and it had no
signature binding a vocabulary to its definer until DSig arrived two years
later. RATS splits lexical from evaluative authority but still assumes reference
values arrive from a recognised provider.

This gap is the specific opening the m-of-n project targets, and the survey
records it here as an observation about the literature rather than as a
proposal.

## 12. Open problems

The survey leaves seven problems genuinely open. Each is stated as a question a
future system must answer, with the evidence from §§4–10 that makes it hard.

**1. Where does a relying party put its own scoping?** Every format lets a
parent scope a child; none lets a *verifier* scope a root it has installed.
X.509 makes root-embedded constraints advisory (§4.3) and the binding
alternative is Informational; RATS pushes it into a Verifier Owner policy that
no document specifies (§7.7); supply-chain formats make it a command-line flag
(§8.5). A design in which unscoped authority is **inexpressible** rather than
merely discouraged would close this, but no deployed system does that.

**2. Can the lattice be recovered without giving up context predicates?** SPKI
could answer *what does this token authorize?* in closed form; nothing modern
can (§9.3). The obstacle is real — third-party caveats and Datalog checks are
deferred evidence, not tags. An open question is whether a **hybrid** is
possible: a tag fragment closed under meet, normalised at each hop, plus an
uninterpreted predicate residue that accumulates. The 2026 attenuating-token
draft is one `⊓` away from testing this.

**3. How does a vocabulary become self-describing again without a registry?**
§11.4 records that no system localises type names. PICS made the vocabulary
dereferenceable but service-owned; C2PA made it spec-owned; DSSE declined to
define one. Whether a `(defining key, local label)` pair can carry a
machine-readable schema and human-readable description, the way an
`application/pics-service` document did, is untested.

**4. What is the interoperable language for a registration policy?** SCITT
uniquely requires policies to be *transparent* — registered as signed
statements, versioned, auditable — and then leaves their encoding to the
operator (§8.5). Transparency without interoperability means a relying party
can read the policy and still cannot evaluate it.

**5. How is freshness expressed for a statement that outlives its verifier's
assumptions?** Attestation's hard problem is freshness, not revocation (§7.8).
But §10.1's carve-out shows long-lived attestation inherits a
harvest-now-forge-later threat, whose only mitigation is independent evidence
of pre-break existence. No format in the survey requires a timestamp or
transparency anchor; C2PA's model explicitly lets timestamped manifests remain
valid indefinitely while using only quantum-vulnerable algorithms (§10.5).

**6. Can an envelope express a quantum-resistance threshold?** A 3-of-5 root
with two ML-DSA and three Ed25519 keys is not quantum-resistant, and no
envelope in the supply-chain stack can say so (§10.4). "Agility by omission" is
not agility.

**7. How is a naming layer re-bundled onto a capability system?** Revocation,
rotation, audit and organizational policy are all naming problems in disguise
(§9.4). SPKI had two layers; the modern family collapsed to one and is
rediscovering the need under the banner of provenance. Whether the second layer
can be added without reintroducing a global namespace is the question SDSI
answered for principals and nobody has answered for anything else.

## 13. Conclusion

Fifty years after Diffie and Hellman posed the problem, the cryptographic core
is settled. EUF-CMA is a stable definition, the standards lineage is mature,
and the post-quantum replacements are published (§2, §10). What this survey
finds is that essentially none of the field's difficulty lives there.

The difficulty lives in the three questions a signature leaves open, and the
evidence assembled here shows the field answering them by **deferral**. X.509
removed a structural scoping invariant and replaced it with an optional,
fail-open extension that this survey measured at **1.8% deployment, correctly
marked critical on 2 certificates out of 1,769** (§4.5). The supply-chain
stack made the authorization decision an input — a parameter, a flag, an
assumed root — and said so in its own specifications (§8.5). C2PA enumerated
its vocabulary in the specification document and thereby lost the late-binding
property PICS had in 1996 (§6.5). Capability systems dropped SPKI's
authorization lattice and its naming layer, and the 2026 agentic drafts are
reinventing both (§9.3, §9.4).

In each case the deferral bought adoption, and in each case it was later paid
for. The clearest single piece of evidence is the May 2026 npm compromise
(§8.6): 84 artifacts carrying **cryptographically valid provenance attestations
that accurately named the correct builder, repository, workflow and ref**.
Every "who signed this" question was answered correctly, and the answer was
useless. That is this survey's thesis in one incident.

Two distinctions, if adopted, would clarify a good deal of subsequent work.
**Delegation is not integrity-of-state**: one passes authority between
principals and needs revocation, the other describes a snapshot and needs
freshness, and packing the second into containers built for the first is where
attestation bugs live (§7.8, §11.3). And **provenance is not entitlement**:
recording what happened is a solved engineering problem, and deciding who was
entitled to make it happen is not.

Finally, the survey records one thing the literature has not done. SDSI
localised *principal names*, showing that a global namespace was unnecessary
for identity. **Nobody has localised type names** (§11.4). Every system
surveyed fixes its predicate vocabulary in a specification, allocates it from a
registry, or declines to define one — and the one system that came closest,
PICS in 1996, made the vocabulary a dereferenceable web resource owned by a
service rather than by a key. Whether that generalises is an open question, and
it is the one this project intends to pursue.

---

## References

*Generated from `library/exports/references.json`. Every entry is a library
record; nothing is typed by hand. Run `bin/build-references` after any
ingestion to regenerate this section.*

<!-- REFERENCES:BEGIN -->
<!-- generated by bin/build-references — do not edit by hand -->

- **[aclu-fahrenheit-451-2]** Fahrenheit 451.2: Is Cyberspace Burning?  
  <https://www.aclu.org/documents/fahrenheit-4512-cyberspace-burning>
- **[android-key-attestation]** Android Key and ID Attestation  
  <https://source.android.com/docs/security/features/keystore/attestation>
- **[apple-app-attest]** DCAppAttestService / App Attest  
  <https://developer.apple.com/documentation/devicecheck>
- **[biscuit-spec-3-3]** Biscuit Specification v3.3  
  <https://doc.biscuitsec.org/reference/specifications.html>
- **[brickell-2004-daa]** Direct Anonymous Attestation  
  <https://eprint.iacr.org/2004/205>
- **[c2pa-2-4]** Content Credentials: C2PA Technical Specification 2.4  
  <https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html>
- **[c2pa-ux-2-2]** C2PA User Experience Guidance for Implementers 2.2  
  <https://spec.c2pa.org/specifications/specifications/2.2/ux/UX_Recommendations.html>
- **[ca-sb-942]** California AI Transparency Act SB 942, as amended by AB 853  
  <https://leginfo.legislature.ca.gov/>
- **[cabforum-sc063]** Ballot SC-063v4: Make OCSP Optional, Require CRLs  
  <https://cabforum.org/2023/07/14/ballot-sc-063-v4make-ocsp-optional-require-crls-and-incentivize-automation/>
- **[cabforum-smime-br]** CA/Browser Forum Baseline Requirements for S/MIME Certificates  
  <https://github.com/cabforum/smime/blob/main/SBR.md>
- **[cabforum-tls-br]** CA/Browser Forum Baseline Requirements for TLS Server Certificates  
  <https://github.com/cabforum/servercert/blob/main/docs/BR.md>
- **[cawg-identity-1-2]** CAWG Identity Assertion 1.2  
  <https://cawg.io/identity/1.2/>
- **[chung-2018-must-staple]** Is the Web Ready for OCSP Must-Staple?  
  <https://doi.org/10.1145/3278532.3278543>
- **[cisa-2026-sbom-minimum]** 2026 Minimum Elements for a Software Bill of Materials (SBOM)  
  <https://www.cisa.gov/resources-tools/resources/2026-minimum-elements-software-bill-materials-sbom>
- **[cnsa-2-0]** Commercial National Security Algorithm Suite 2.0 (CNSA 2.0) Algorithms and FAQ  
  <https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF>
- **[cox-2024-xz-timeline]** Timeline of the xz open source attack  
  <https://research.swtch.com/xz-timeline>
- **[crowdstrike-sunspot]** SUNSPOT: An Implant in the Build Process  
  <https://www.crowdstrike.com/en-us/blog/sunspot-malware-technical-analysis/>
- **[cscw-2023-provenance-trust]** Examining the Impact of Provenance-Enabled Media on Trust and Accuracy Perceptions  
  <https://doi.org/10.1145/3610061>
- **[cve-2019-13050]** CVE-2019-13050: SKS keyserver certificate spamming attack  
  <https://access.redhat.com/articles/4264021>
- **[cve-2024-3094]** CVE-2024-3094 (xz-utils backdoor, CVSS 10.0)  
  <https://nvd.nist.gov/vuln/detail/CVE-2024-3094>
- **[dennis-vanhorn-1966]** Programming Semantics for Multiprogrammed Computations  
  <https://doi.org/10.1145/365230.365252>
- **[did-key-method]** The did:key Method v0.9  
  <https://w3c-ccg.github.io/did-key-spec/>
- **[diffie-hellman-1976]** New Directions in Cryptography  
  <https://doi.org/10.1109/TIT.1976.1055638>
- **[draft-ffm-rats-cca-token]** Arm CCA Reference Attestation Token  
  <https://datatracker.ietf.org/doc//>
- **[draft-ietf-lamps-pq-composite-sigs]** Composite ML-DSA for use in X.509 Public Key Infrastructure  
  <https://datatracker.ietf.org/doc//>
- **[draft-ietf-rats-corim]** Concise Reference Integrity Manifest (CoRIM)  
  <https://datatracker.ietf.org/doc//>
- **[draft-ietf-spki-cert-structure]** Simple Public Key Certificate (expired, never published)  
  <https://datatracker.ietf.org/doc//>
- **[draft-niyikiza-oauth-attenuating-agent-tokens]** Attenuating Authorization Tokens for Agentic Delegation Chains  
  <https://datatracker.ietf.org/doc//>
- **[ecma-424]** ECMA-424 CycloneDX Bill of Materials Specification, 2nd Edition  
  <https://ecma-international.org/publications-and-standards/standards/ecma-424/>
- **[eff-2010-ssliverse]** An Observatory for the SSLiverse  
  <https://www.eff.org/files/defconssliverse.pdf>
- **[elgamal-1985]** A Public Key Cryptosystem and a Signature Scheme Based on Discrete Logarithms  
  <https://doi.org/10.1109/TIT.1985.1057074>
- **[ellison-schneier-2000-ten-risks]** Ten Risks of PKI: What You're not Being Told about Public Key Infrastructure  
  <https://www.schneier.com/academic/paperfiles/paper-pki.pdf>
- **[eo-14028]** Executive Order 14028: Improving the Nation's Cybersecurity  
  <https://www.govinfo.gov/content/pkg/FR-2021-05-17/pdf/2021-10460.pdf>
- **[eo-14144]** Executive Order 14144: Strengthening and Promoting Innovation in the Nation's Cybersecurity  
  <https://www.govinfo.gov/content/pkg/FR-2025-01-17/pdf/2025-01470.pdf>
- **[eo-14306]** Executive Order 14306: Sustaining Select Efforts To Strengthen the Nation's Cybersecurity  
  <https://www.govinfo.gov/content/pkg/FR-2025-06-11/pdf/2025-10804.pdf>
- **[eu-ai-act-art-50]** EU AI Act Article 50: Transparency Obligations  
  <https://artificialintelligenceact.eu/article/50/>
- **[eu-code-of-practice-marking]** EU Code of Practice on marking and labelling AI-generated content  
  <https://digital-strategy.ec.europa.eu/en/news/commission-publishes-code-practice-marking-and-labelling-ai-generated-content>
- **[eu-cra-2024-2847]** Regulation (EU) 2024/2847 (Cyber Resilience Act)  
  <http://data.europa.eu/eli/reg/2024/2847/oj>
- **[event-stream-issue-116]** event-stream issue #116: I don't know what to say.  
  <https://github.com/dominictarr/event-stream/issues/116>
- **[fips-186]** FIPS 186: Digital Signature Standard (DSS), 1994  
  <https://csrc.nist.gov/pubs/fips/186/upd1/final>
- **[fips-186-1]** FIPS 186-1: Digital Signature Standard (DSS), 1998  
  <https://csrc.nist.gov/pubs/fips/186-1/final>
- **[fips-186-2]** FIPS 186-2: Digital Signature Standard (DSS), 2000  
  <https://doi.org/10.6028/NIST.FIPS.186-2>
- **[fips-186-3]** FIPS 186-3: Digital Signature Standard (DSS), 2009  
  <https://csrc.nist.gov/pubs/fips/186-3/final>
- **[fips-186-4]** Digital Signature Standard (DSS), FIPS 186-4  
  <https://csrc.nist.gov/pubs/fips/186-4/final>
- **[fips-186-5]** Digital Signature Standard (DSS)  
  <https://csrc.nist.gov/pubs/fips/186-5/final>
- **[fips-203]** FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard  
  <https://doi.org/10.6028/NIST.FIPS.203>
- **[fips-204]** FIPS 204: Module-Lattice-Based Digital Signature Standard (ML-DSA)  
  <https://doi.org/10.6028/NIST.FIPS.204>
- **[fips-205]** FIPS 205: Stateless Hash-Based Digital Signature Standard (SLH-DSA)  
  <https://doi.org/10.6028/NIST.FIPS.205>
- **[foxit-2012-black-tulip]** Black Tulip: Report of the investigation into the DigiNotar CA breach  
  <https://www.enisa.europa.eu/sites/default/files/all_files/Operation_Black_Tulip_v2.pdf>
- **[gittuf-2025]** Rethinking Trust in Forge-Based Git Security (gittuf)  
  <https://doi.org/10.14722/ndss.2025.241008>
- **[gmr-1984-paradoxical]** A Paradoxical Solution to The Signature Problem  
  <https://doi.org/10.1109/SFCS.1984.715946>
- **[gmr-1988-adaptive]** A Digital Signature Scheme Secure Against Adaptive Chosen-Message Attacks  
  <https://doi.org/10.1137/0217017>
- **[gmy-1983-strong-signatures]** Strong Signature Schemes  
  <https://doi.org/10.1145/800061.808774>
- **[gnupg-key-management]** GnuPG manual: OpenPGP Key Management (tsign, trustspec)  
  <https://www.gnupg.org/documentation/manuals/gnupg/OpenPGP-Key-Management.html>
- **[go-nameconstraint-cves]** Go crypto/x509 name-constraint defects (five CVEs, 2025-2026)  
  <https://cveawg.mitre.org/api/cve/CVE-2025-58187>
- **[golang-61963]** TUBITAK Kamu SM root should be constrained (golang/go#61963)  
  <https://github.com/golang/go/issues/61963>
- **[google-2016-wosign]** Distrusting WoSign and StartCom Certificates  
  <https://security.googleblog.com/2016/10/distrusting-wosign-and-startcom.html>
- **[google-2017-symantec]** Chrome's Plan to Distrust Symantec Certificates  
  <https://security.googleblog.com/2017/09/chromes-plan-to-distrust-symantec.html>
- **[google-open-dice]** Open Profile for DICE  
  <https://pigweed.googlesource.com/open-dice/+/HEAD/docs/specification.md>
- **[gutmann-2002-pki-not-dead]** PKI: It's Not Dead, Just Resting  
  <https://doi.org/10.1109/MC.2002.1023787>
- **[gvu-1998-webmaster-survey]** GVU 10th WWW User Survey: webmaster PICS labelling rates  
  <https://sites.cc.gatech.edu/gvu/user_surveys/survey-1998-04/graphs/webmaster/q69.htm>
- **[hardy-1988-confused-deputy]** The Confused Deputy (or why capabilities might have been invented)  
  <https://doi.org/10.1145/54289.871709>
- **[ide-2025-signals-of-provenance]** Signals of Provenance: Navigating Indicators in AI-Generated Media for Sighted and Blind Individuals  
  <https://arxiv.org/abs/2505.16057>
- **[ietf-spki-wg]** IETF SPKI Working Group charter and documents  
  <https://datatracker.ietf.org/wg/spki/about/>
- **[in-toto-2019]** in-toto: Providing farm-to-table guarantees for bits and bytes  
  <https://www.usenix.org/conference/usenixsecurity19/presentation/torres-arias>
- **[in-toto-attestation-v1]** in-toto Attestation Framework v1  
  <https://in-toto.io/>
- **[in-toto-envelope-v1]** in-toto Attestation Framework: Envelope  
  <https://github.com/in-toto/attestation/blob/main/spec/v1/envelope.md>
- **[intel-sgx-dcap-quotelib]** Intel SGX ECDSA QuoteLibReference (DCAP API)  
  <https://download.01.org/intel-sgx/latest/dcap-latest/linux/docs/Intel_SGX_ECDSA_QuoteLibReference_DCAP_API.pdf>
- **[intel-tdx-whitepaper]** Intel Trust Domain Extensions (white paper)  
  <https://www.intel.com/content/dam/develop/external/us/en/documents/tdx-whitepaper-final9-17.pdf>
- **[iso-iec-11889-2015]** ISO/IEC 11889:2015 Trusted Platform Module Library  
  <https://www.iso.org/standard/66510.html>
- **[iso-iec-5962]** ISO/IEC 5962:2021 SPDX Specification V2.2.1  
  <https://www.iso.org/standard/81870.html>
- **[itu-x509-1988]** ITU-T X.509 (1988): The Directory - Authentication framework  
  <https://www.itu.int/rec/T-REC-X.509-198811-S>
- **[keys-openpgp-org-faq]** keys.openpgp.org FAQ: third-party certification policy  
  <https://keys.openpgp.org/about/faq>
- **[lamport-1979-one-way]** Constructing Digital Signatures from a One Way Function  
  <https://lamport.azurewebsites.net/pubs/dig-sig.pdf>
- **[langley-2011-revocation]** Revocation doesn't work  
  <https://www.imperialviolet.org/2011/03/18/revocation.html>
- **[larisch-2017-crlite]** CRLite: A Scalable System for Pushing All TLS Revocations to All Browsers  
  <https://doi.org/10.1109/SP.2017.17>
- **[letsencrypt-ocsp-eol]** OCSP Service Has Reached End of Life  
  <https://letsencrypt.org/2025/08/06/ocsp-service-has-reached-end-of-life>
- **[liu-2015-revocation]** An End-to-End Measurement of Certificate Revocation in the Web's PKI  
  <https://doi.org/10.1145/2815675.2815685>
- **[macaroons-2014]** Macaroons: Cookies with Contextual Caveats for Decentralized Authorization in the Cloud  
  <https://theory.stanford.edu/~ataly/Papers/macaroons.pdf>
- **[merkle-1979-thesis]** Secrecy, Authentication, and Public Key Systems  
  <https://www.ralphmerkle.com/papers/Thesis1979.pdf>
- **[moruzzi-2025-content-authenticities]** Content Authenticities: A Discussion on the Values of Provenance Data for Creatives and Their Audiences  
  <https://doi.org/10.1145/3698061.3726918>
- **[mozilla-2013-anssi]** Revoking Trust in one ANSSI Certificate  
  <https://blog.mozilla.org/security/2013/12/09/revoking-trust-in-one-anssi-certificate/>
- **[mozilla-2013-turktrust]** Revoking Trust in Two TurkTrust Certificates  
  <https://blog.mozilla.org/security/2013/01/03/revoking-trust-in-two-turktrust-certficates/>
- **[mozilla-bug-856060]** Name Constraints ignored by libPKIX verification engine  
  <https://bugzilla.mozilla.org/show_bug.cgi?id=856060>
- **[nistir-8547]** NIST IR 8547 ipd: Transition to Post-Quantum Cryptography Standards  
  <https://csrc.nist.gov/pubs/ir/8547/ipd>
- **[nistir-8610]** NIST IR 8610: Status Report on the Second Round of the Additional Digital Signature Schemes  
  <https://csrc.nist.gov/pubs/ir/8610/final>
- **[npm-event-stream]** Details about the event-stream incident  
  <https://blog.npmjs.org/post/180565383195/details-about-the-event-stream-incident>
- **[nsa-2025-content-credentials]** Content Credentials: Strengthening Multimedia Integrity in the Generative AI Era  
  <https://media.defense.gov/2025/Jan/29/2003634788/-1/-1/0/CSI-CONTENT-CREDENTIALS.PDF>
- **[ntia-2021-sbom-minimum]** The Minimum Elements For a Software Bill of Materials (SBOM)  
  <https://www.ntia.gov/report/2021/minimum-elements-software-bill-materials-sbom>
- **[ohm-2020-backstabbers]** Backstabber's Knife Collection: A Review of Open Source Software Supply Chain Attacks  
  <https://doi.org/10.1007/978-3-030-52683-2_2>
- **[openssl-2022-email-overflow]** CVE-2022-3786 and CVE-2022-3602: X.509 Email Address Buffer Overflows  
  <https://openssl-library.org/post/2022-11-01-email-address-overflows/>
- **[pics-1-1-services]** PICS 1.1 Rating Services and Rating Systems and Their Machine Readable Descriptions  
  <https://www.w3.org/TR/REC-PICS-services-961031>
- **[pics-censorship-faq]** PICS, Censorship, and Intellectual Freedom FAQ  
  <https://www.w3.org/PICS/PICS-FAQ-980126.html>
- **[pics-dsig-1-0]** PICS Signed Labels (DSig) 1.0 Specification  
  <https://www.w3.org/TR/1998/REC-DSig-label-19980527/>
- **[powder-description-resources]** POWDER: Description Resources  
  <https://www.w3.org/TR/powder-dr/>
- **[ptacek-2024-macaroons]** Macaroons Escalated Quickly  
  <https://fly.io/blog/macaroons-escalated-quickly/>
- **[pypi-trusted-publishers]** Trusted Publishers for PyPI  
  <https://docs.pypi.org/trusted-publishers/>
- **[rabin-1979-tr212]** Digitalized Signatures and Public-Key Functions as Intractable as Factorization  
  <https://dspace.mit.edu/handle/1721.1/149499>
- **[rfc-1422]** PEM Part II: Certificate-Based Key Management  
  <https://www.rfc-editor.org/rfc/rfc1422.html>
- **[rfc-2692]** SPKI Requirements  
  <https://www.rfc-editor.org/rfc/rfc2692.html>
- **[rfc-2693]** SPKI Certificate Theory  
  <https://www.rfc-editor.org/rfc/rfc2693.html>
- **[rfc-3820]** Internet X.509 PKI Proxy Certificate Profile  
  <https://www.rfc-editor.org/rfc/rfc3820.html>
- **[rfc-4880]** OpenPGP Message Format  
  <https://www.rfc-editor.org/rfc/rfc4880.html>
- **[rfc-5280]** Internet X.509 Public Key Infrastructure Certificate and CRL Profile  
  <https://www.rfc-editor.org/rfc/rfc5280.html>
- **[rfc-5937]** Using Trust Anchor Constraints during Certification Path Processing  
  <https://www.rfc-editor.org/rfc/rfc5937.html>
- **[rfc-6749]** The OAuth 2.0 Authorization Framework  
  <https://www.rfc-editor.org/rfc/rfc6749.html>
- **[rfc-6962]** Certificate Transparency  
  <https://www.rfc-editor.org/rfc/rfc6962.html>
- **[rfc-7633]** X.509v3 TLS Feature Extension (OCSP Must-Staple)  
  <https://www.rfc-editor.org/rfc/rfc7633.html>
- **[rfc-7800]** Proof-of-Possession Key Semantics for JSON Web Tokens (JWTs)  
  <https://www.rfc-editor.org/rfc/rfc7800.html>
- **[rfc-8032]** Edwards-Curve Digital Signature Algorithm (EdDSA)  
  <https://www.rfc-editor.org/rfc/rfc8032.html>
- **[rfc-8391]** XMSS: eXtended Merkle Signature Scheme  
  <https://www.rfc-editor.org/rfc/rfc8391.html>
- **[rfc-8554]** Leighton-Micali Hash-Based Signatures  
  <https://www.rfc-editor.org/rfc/rfc8554.html>
- **[rfc-8555]** Automatic Certificate Management Environment (ACME)  
  <https://www.rfc-editor.org/rfc/rfc8555.html>
- **[rfc-9162]** Certificate Transparency Version 2.0  
  <https://www.rfc-editor.org/rfc/rfc9162.html>
- **[rfc-9334]** Remote ATtestation procedureS (RATS) Architecture  
  <https://www.rfc-editor.org/rfc/rfc9334.html>
- **[rfc-9396]** OAuth 2.0 Rich Authorization Requests  
  <https://www.rfc-editor.org/rfc/rfc9396.html>
- **[rfc-9449]** OAuth 2.0 Demonstrating Proof of Possession (DPoP)  
  <https://www.rfc-editor.org/rfc/rfc9449.html>
- **[rfc-9580]** OpenPGP  
  <https://www.rfc-editor.org/rfc/rfc9580.html>
- **[rfc-9598]** Internationalized Email Addresses in X.509 Certificates  
  <https://www.rfc-editor.org/rfc/rfc9598.html>
- **[rfc-9608]** No Revocation Available for X.509 Public Key Certificates  
  <https://www.rfc-editor.org/rfc/rfc9608.html>
- **[rfc-9711]** The Entity Attestation Token (EAT)  
  <https://www.rfc-editor.org/rfc/rfc9711.html>
- **[rfc-9804]** Simple Public Key Infrastructure (SPKI) S-Expressions  
  <https://www.rfc-editor.org/rfc/rfc9804.html>
- **[rfc-9943]** An Architecture for Trustworthy and Transparent Digital Supply Chains  
  <https://www.rfc-editor.org/rfc/rfc9943.html>
- **[rsa-1978]** A Method for Obtaining Digital Signatures and Public-Key Cryptosystems  
  <https://doi.org/10.1145/359340.359342>
- **[schnorr-1989-smartcards]** Efficient Identification and Signatures for Smart Cards  
  <https://doi.org/10.1007/0-387-34805-0_22>
- **[sdsi-1-1]** SDSI — A Simple Distributed Security Infrastructure, version 1.1  
  <https://people.csail.mit.edu/rivest/pubs/RL96.ver-1.1.html>
- **[secure-systems-lab-dsse]** Dead Simple Signing Envelope (DSSE)  
  <https://github.com/secure-systems-lab/dsse>
- **[sev-snp-primer-2026]** AMD SEV-SNP: A Confidential Computing Primer  
  <https://arxiv.org/abs/2608.04039>
- **[shor-1994]** Algorithms for Quantum Computation: Discrete Logarithms and Factoring  
  <https://doi.org/10.1109/SFCS.1994.365700>
- **[sigstore-2022]** Sigstore: Software Signing for Everybody  
  <https://doi.org/10.1145/3548606.3560596>
- **[slsa-1-2]** SLSA Specification v1.2  
  <https://slsa.dev/spec/v1.2/>
- **[slsa-2026-mini-shai-hulud]** Mini Shai-Hulud: Where SLSA's Boundaries Fall  
  <https://slsa.dev/blog/2026/05/mini-shai-hulud-what-slsa-can-and-cannot-do>
- **[sp-800-208]** SP 800-208: Recommendation for Stateful Hash-Based Signature Schemes  
  <https://doi.org/10.6028/NIST.SP.800-208>
- **[spdx-3-0-1]** SPDX Specification v3.0.1  
  <https://spdx.github.io/spdx-spec/v3.0.1/>
- **[survey-2026-nameconstraints-measurement]** Name-constraint prevalence among CCADB-disclosed intermediate CA certificates (original measurement, 2026-09-26)  
  <https://ccadb.my.salesforce-sites.com/mozilla/MozillaIntermediateCertsCSVReport>
- **[tcg-dice-cert-profiles]** DICE Certificate Profiles r01  
  <https://trustedcomputinggroup.org/wp-content/uploads/DICE-Certificate-Profiles-r01_pub.pdf>
- **[tcg-dice-hw-requirements]** Hardware Requirements for a Device Identifier Composition Engine r78  
  <https://trustedcomputinggroup.org/wp-content/uploads/Hardware-Requirements-for-Device-Identifier-Composition-Engine-r78_For-Publication.pdf>
- **[tcg-integrity-event-log]** TCG Guidance on Integrity Measurements and Event Log Processing v1 r0p118  
  <https://trustedcomputinggroup.org/wp-content/uploads/TCG-Guidance-Integrity-Measurements-Event-Log-Processing_v1_r0p118_24feb2022-1.pdf>
- **[tcg-pc-client-pfp]** TCG PC Client Platform Firmware Profile Specification r1.05  
  <https://trustedcomputinggroup.org/wp-content/uploads/TCG_PCClient_PFP_r1p05_05_3feb20.pdf>
- **[tcg-pc-client-ptp]** TCG PC Client Platform TPM Profile (PTP) for TPM 2.0 v1.06 r32  
  <https://trustedcomputinggroup.org/wp-content/uploads/TCG-PC-Client-Platform-TPM-Profile-for-TPM-2.0-Version-1.06-Revision-32_5April24.pdf>
- **[tcg-tpm-1-2-main]** TPM Main Specification Version 1.2, Level 2, Revision 116  
  <https://trustedcomputinggroup.org/resource/tpm-main-specification/>
- **[tcg-tpm-2-0-library-184]** TPM 2.0 Library Specification, Parts 0-4, Version 184  
  <https://trustedcomputinggroup.org/resource/tpm-library-specification/>
- **[tcg-tpm-2-0-library-185]** TPM 2.0 Library Specification v1.85 (PQC: ML-KEM, ML-DSA)  
  <https://trustedcomputinggroup.org/new-computing-specification-implements-pqc-measures-to-protect-users-from-quantum-attacks/>
- **[tuf-2010]** Survivable key compromise in software update systems  
  <https://doi.org/10.1145/1866307.1866315>
- **[tuf-tap-21]** TAP 21: ML-DSA signing scheme for TUF metadata  
  <https://github.com/theupdateframework/taps/blob/master/tap21.md>
- **[ucan-1-0]** User Controlled Authorization Network (UCAN) Specification v1.0.0  
  <https://github.com/ucan-wg/spec>
- **[ulrich-2011-openpgp-wot]** Investigating the OpenPGP Web of Trust  
  <https://doi.org/10.1007/978-3-642-23822-2_27>
- **[w3c-did-core]** Decentralized Identifiers (DIDs) v1.0  
  <https://www.w3.org/TR/did-core/>
- **[w3c-did-extensions-methods]** DID Extensions: Methods registry  
  <https://www.w3.org/TR/did-extensions-methods/>
- **[w3c-tag-obsolete-powder]** W3C TAG proposal to obsolete CC/PP and POWDER (issue 86)  
  <https://github.com/w3c/transitions/issues/86>
- **[wang-2006-reducing-spki]** Reducing the Dependence of SPKI/SDSI on PKI  
  <https://doi.org/10.1007/11863908_11>
- **[zcap-ld]** Authorization Capabilities (ZCAP-LD) v0.4.0-rc.6  
  <https://w3c-ccg.github.io/zcap-spec/>
- **[zhang-2014-heartbleed]** Analysis of SSL Certificate Reissues and Revocations in the Wake of Heartbleed  
  <https://doi.org/10.1145/2663716.2663758>
- **[zooko-2001-names]** Names: Decentralized, Secure, Human-Meaningful: Choose Two  
  <https://web.archive.org/web/20011020191610/http://zooko.com/distnames.html>
- **[zoom-keybase-2020]** Zoom Acquires Keybase  
  <https://blog.zoom.us/zoom-acquires-keybase-and-announces-goal-of-developing-the-most-broadly-used-enterprise-end-to-end-encryption-offering/>

<!-- REFERENCES:END -->
