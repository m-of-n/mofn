---
schema: "archdoc/v1"
id: R-0002
title: "Wallet market survey — commercial products, open source, and PGP trust indicators"
short_title: "Wallet market survey"
description: "What key-holding and trust-indicator products already show a person, which of those habits the local m-of-n wallet should copy, change, or refuse, and how a file-based wallet can protect a private key. Does not close a decision."
type: research
category: security
status: draft
version: "0.2.0"
date: "2026-10-02"
updated: "2026-10-02"
needs_review: true
reviewed: false
canonical_path: research/0002-wallets/report.md
informs: [APP-0001, PLAN-0004]
open_decisions: [DEC-002]
backlog: R-002
---

# Wallet market survey

**Status: draft. Recommendations are proposals.** This memo does not close
DEC-002 or any other open decision, and it does not specify the wallet.

It answers [issue 58](https://github.com/m-of-n/mofn/issues/58). Every factual
claim below was checked against a page fetched on 2026-10-02. Anything that
could not be checked is written "not verified". URLs and the queries that
found them are in `sources.md` and `searches.md`.

`library/` was not touched. This report therefore cites fetched URLs rather
than `[@record-id]` keys. Ingesting those URLs as library records is separate
work.

PLAN-0004 is not on `main`. It was read from the worktree for
[PR 57](https://github.com/m-of-n/mofn/pull/57)
(`project/PLAN-0004-application-plan.md` on `doc/app-0001-no-kg`). APP-0001
was read from `main`.

---

## 1. What this is measuring

The product those documents describe is a **local wallet**. It holds keys,
unsigned trust roots, and statements. It makes attestations and delegations.
It evaluates a presented set by reduction and explains the verdict. Principals
are keys. Names are local to a naming key (SDSI). Authorization is an
SPKI-shaped reduction of a delegation chain. A vocabulary renders the
sentence. PLAN-0004 adds: no network, no keychain product, no revocation
product, no knowledge-graph engine, five views, files on disk. APP-0001's
product moment is the authorization line: a signature can be valid and the
key can still have no standing to say the thing.

Cryptocurrency payment wallets are out of scope. A product is in scope only
when it holds keys or credentials and shows trust or provenance to a person,
or when it is the open-source tool the issue names.

The question is not "which product should we wrap". It is which habits a
relying party already has, and which of those habits would erase the
distinction the wallet exists to show.

## 2. Commercial products

### 2.1 Microsoft Artifact Signing (formerly Trusted Signing)

Vendor: Microsoft, on Azure. The overview calls it a fully managed signing
service. The user creates an Artifact Signing account, completes identity
validation, and uses a certificate profile. Certificates are managed inside
FIPS 140-3 Level 3 HSMs. The file does not leave the endpoint: the client
sends a digest. Profiles cover Public Trust, Private Trust, VBS enclave, CI
policy, and test signing. The service integrates with "leading developer
toolsets"; a named CLI on the overview page was not verified.

Public price, from the Learn SKU article (the Azure pricing page fetched the
same day rendered the dollar cells as "$-", so the numbers below are the
Learn article's, not the marketing calculator's):

| SKU | Monthly price | Included signatures | After quota | Profiles |
|---|---|---|---|---|
| Basic | $9.99 per account | 5,000 | $0.005 each | 1 of each type |
| Premium | $99.99 per account | 100,000 | $0.005 each | 10 of each type |

Both SKUs include Public Trust and Private Trust signing. What Windows shows
a person who later runs the signed file was not verified.

### 2.2 SSL.com eSigner for Code

Vendor: SSL.com. The product page describes a cloud-HSM code-signing service
for Windows executables, drivers, installers, and scripts, aimed at CI (it
names GitHub Actions, Jenkins, and Azure DevOps). The private key stays in
the cloud HSM. "eSigner.com" is the place the page says you sign without
hardware.

Prices printed on that page:

- Certificate: IV $129.00/yr, OV $129.00/yr, EV $349.00/yr, EV sole proprietor
  $359.00/yr.
- Cloud-signing subscription, monthly tiers: Tier 1 $15.00/mo (240 signings,
  1 credential), Tier 2 $63.75/mo (1,200 signings, 5 credentials), Tier 3
  $131.25/mo (3,600 signings, 9 credentials), Tier 4 $187.50/mo (12,000
  signings, 13 credentials). Unused signatures roll into the next period
  while the certificate is active. An annual subscription option is offered;
  its dollar amounts were not in the fetched text.

The page does not describe a relying-party view. The trust indicator, if any,
is the platform that later consumes the public code-signing certificate.
That UI was not verified.

### 2.3 DigiCert Software Trust Manager

Vendor: DigiCert, part of DigiCert ONE. The signer guide says a person with
the `sign` permission signs with keys stored in Software Trust Manager, using
SMCTL (CLI) or Click-to-sign (a desktop UI), or a supported third-party
tool. The private key remains in Software Trust Manager. Licensing is a
subscription counted in units (production signature units per hash, test
signature units, cryptographic operations, HSM keypair slots). The licensing
page says to contact DigiCert Sales for the agreement. **No public price was
on the pages fetched.** The public marketing site returned a bot wall, so
claims that appear only in search snippets of that page (approval workflows,
FIPS level) are not used here.

### 2.4 SignPath

Vendor: SignPath. The homepage fetched describes a software-integrity
platform (pipeline integrity, semantic code signing, software attestation,
code governance) whose pitch is cryptographic proof that a release is
authentic, unmodified, and approved by the right people. **Price and the relying-party screen were not on that page.** Key
custody was not on that page either. A later fetch of SignPath's own
docs (section 10.8) does say where the private key is kept. The feature
row stays "not verified" except for the keys cell, which that later fetch
supports.

### 2.5 Adobe Content Credentials and Inspect

Adobe's Creative Cloud help page describes Content Credentials as durable
metadata, "a digital nutrition label", including who created the content and
how it was made (camera, generative AI, or an edit in a tool such as
Photoshop). They are available in Photoshop, Lightroom, Adobe Stock, and
Premiere. A person hovers a "Cr" icon, or uses a Chrome extension. A
separate price for the feature was not stated.

Inspect, on Adobe Content Authenticity (Beta) at `inspect.cr`, is documented
as a C2PA validator. The user uploads or drops a file, or passes a public
asset URL. The tool shows author and tools used. If the claim signature's
certificate is **not** on the C2PA trust list, the source section shows
"Unrecognized". If it is on the list, Inspect shows the issuer organization
name from the certificate (the `O` attribute) and the signature time. That
is a trust indicator aimed at a person. It is "is this signer on the list",
not "was this signer allowed to make this claim".

### 2.6 Microsoft Entra Verified ID and Authenticator

Microsoft's Verified ID overview says a verifiable credential is claims an
issuer attests about a subject, signed with the issuer's DID. Microsoft
supports the `did:web` method, which it describes as trusting a web domain's
existing reputation. The wallet is the Microsoft Authenticator app: it
creates DIDs, handles issuance and presentation, and backs up the DID seed
in an encrypted wallet file.

The Authenticator tutorial shows the relying-party moment. After a QR scan,
Authenticator displays who the issuing party is and that the request comes
from a verified domain. The text says it is the user's choice whether to
trust that party. The user can later present the credential and see activity
of where it was presented. Whether that works offline, and how revocation
appears, were not in the fetched pages.

### 2.7 Apple Wallet, driver's license or state ID

Apple's support pages say a person adds an eligible driver's license or ID
from a participating US state or territory to Wallet on iPhone or Apple
Watch. The ID data is encrypted. Neither the issuing authority nor Apple can
see when and where it is used. Face ID or Touch ID (or a passcode, for
certain accessibility features) gates use. Presentation is in person at
select TSA checkpoints, businesses, and venues, or in participating apps and
websites. This is a credential wallet with a platform trust indicator, not a
general key wallet and not a statement about an artifact. A separate price
was not stated. The list of participating states was not copied from a
secondary article; the fetched page says "a participating US state or
territory" and does not enumerate them in the text extracted here.

### 2.8 GitHub artifact attestations

Vendor: GitHub, built on Sigstore. Generating an attestation produces a
signed claim linking an artifact to the workflow, repository, organization,
environment, commit SHA, triggering event, and other OIDC-token data.
GitHub's own docs say artifact attestations by themselves provide SLSA v1.0
Build Level 2, and that a reusable workflow can be used toward Level 3.
Public repositories use the Sigstore Public Good Instance, and a copy of the
bundle is also stored and written to a public transparency log. Private
repositories use GitHub's Sigstore instance, which the docs say has **no**
transparency log and only federates with GitHub Actions. Attestations on
private or internal repositories require GitHub Enterprise Cloud. A dollar
price for that plan was not fetched.

The consumer command documented is `gh attestation verify` against an
expected `owner/repo`. The same page warns that an attestation is not a
guarantee the artifact is secure: it links the bytes to source and build
instructions, and the consumer still has to decide. A web UI for that
verdict was not verified. Offline verification is documented on a separate
page that was not fetched, so offline is "not verified" in the table.

### 2.9 GPG Suite (GPGTools)

The GPGTools site describes GPG Mail, a macOS Mail extension, and GPG
Keychain. GPG Mail 8 is in beta and requires an active GPG Mail 7 Support
Plan. The site says the Support Plan will be a yearly subscription starting
with GPG Mail 8. **No numeric price was on the pages fetched.** How that UI
shows an untrusted OpenPGP signature was not verified; the trust behaviour
that was verified is GnuPG's, which GPG Mail sits on top of. Treat the
GPG Suite row as a commercial front end whose trust screen was not opened.

### 2.10 Looked at and not given a row

Proton's fetched help page explains that Proton Mail generates a PGP key
pair and that a signature is "proof that you have written the message". It
does not describe ownertrust, marginal trust, or a distinct "valid but
untrusted" state. That display is **not verified**, so Proton is not in the
table.

## 3. Open source

### 3.1 GnuPG

GnuPG's README (repository `master`, fetched 2026-10-02) calls it a free
command-line implementation of OpenPGP "as defined by RFC 4880", with key
management and access to public key directories. `COPYING` in that tree is
the GNU GPL version 3. The manual's trust-signature command still points the
reader at RFC 4880. RFC 4880 is obsoleted by RFC 9580 (section 5 below).
Whether a given GnuPG release implements the RFC 9580 packet changes was
**not verified**. The ownertrust and display behaviour below is from the
current manual and from `g10/pkclist.c` on `master`.

### 3.2 Sequoia `sq`

Sequoia's README describes an implementation of OpenPGP as defined by RFC
9580 and RFC 9980, and of the deprecated RFC 4880. The license stated there
is the GNU LGPL version 2 or later. `sq` is a CLI. On first use it creates a
**local trust root** in the certificate store. A certificate's User ID is
authenticated when a path from that root reaches it with trust amount 120
out of 120. `sq pki link add` writes a certification from that root at trust
depth 0, which authenticates only that binding. `sq pki link authorize
--depth N` makes the certified certificate a trusted introducer for N hops.
Links can expire and can be retracted. `sq` also creates **shadow CAs** that
record where a certificate came from and attach a trust amount to that
provenance. The book gives an example: a certificate fetched from
`keys.openpgp.org` is linked through "Public Directories" and "Downloaded
from keys.openpgp.org", and the public-directories shadow CA is shown at
trust amount 40. That is a provenance indicator for *how the certificate
arrived*, not a statement about an artifact.

### 3.3 Thunderbird

The English strings in
`mail/locales/en-US/messenger/openpgp/msgReadStatus.ftl` on
`mozilla/releases-comm-central` `master` are MPL 2.0. They are a UI, not a
library. A numbered Thunderbird release was not pinned, and whether that UI
implements RFC 9580 trust signatures was **not verified**. What the strings
do say is in section 5.4. Acceptance is a local decision about a key
("accepted", "verified", "rejected"), which is closer to GnuPG's `direct`
trust model than to a computed web of trust.

### 3.4 Sigstore: Cosign and Rekor

Sigstore's overview (OpenSSF / Linux Foundation) says signing uses ephemeral
keys, Fulcio binds an OIDC identity into a short-lived certificate, and
Rekor records the event in an append-only log. The private key is discarded
after one signature. Verification checks the artifact signature, that the
certificate identity matches an expected identity, that the certificate
chains to the Sigstore root, and that the entry is in Rekor. Cosign, Rekor,
the policy-controller, and Witness are Apache 2.0 (LICENSE files fetched).
The Cosign signing overview fetched here is the keyless flow. A PKCS#11
section is linked from the docs navigation; that page was not fetched, so
long-lived and hardware keys are **not verified**.

Rekor is not a wallet. It is a log plus a CLI that can make and verify
entries, fetch an inclusion proof, and look entries up by public key or
artifact.

The policy-controller is a Kubernetes admission controller that enforces a
`ClusterImagePolicy` using Cosign metadata. Witness records in-toto
attestations, evaluates OPA Rego policy, can sign keylessly with Sigstore,
and says attestations can be carried across an air gap. Neither is a
person-facing wallet. They matter because they are where "who may sign" is
currently expressed: a policy object or a CLI expectation, not a reduced
delegation.

### 3.5 in-toto and slsa-verifier

in-toto (Apache 2.0, copyright 2018 New York University) has a project owner
write a **layout**: the steps, and the functionaries authorized to perform
them. A functionary produces a **link** file (command and related files). A
later check validates the links against the layout. That is an artifact
statement with an authorization list. It is not a chain the functionary can
narrow further, and it is not rendered as a sentence.

`slsa-verifier`'s README tells readers who are checking GitHub Actions
attestations to generate them with GitHub artifact attestations and verify
with `gh attestation verify`, and describes its own guidance as something
simpler tooling should replace. Its LICENSE is Apache 2.0. Thresholds,
offline use, and revocation were not stated in the portion used here.

### 3.6 C2PA Tool

`c2patool` (Content Authenticity Initiative; MIT and Apache 2.0, copyright
notice 2020 Adobe) reads a C2PA manifest out of an audio, image, or video
file as JSON, and can add one. The `trust` subcommand checks certificates
against a trust-anchor file. The usage doc shows pointing
`--trust_anchors` at the official C2PA trust list PEM, and says that list is
not an allow-list of end-entity certificates. Default output is JSON, not a
sentence. Inspect (section 2.5) is the human view of a similar check.

### 3.7 SignServer Community

Keyfactor's SignServer Community README describes an LGPL-licensed subset of
SignServer Enterprise for learning, testing, and prototyping signing
workflows for code, documents, and artifacts. The same README says it is not
intended for production. Enterprise price, the UI, and revocation were not
fetched.

## 4. Feature table

Cell values are only `yes`, `no`, `partial`, or `not verified`. "UI" and
"CLI" are split so the cell is one of those four words. A legend of what
`partial` means for that product is in the notes under the table, not in the
cell.

| Product | Keys | Roots | Delegation | Threshold | Local names | Statement | Readable claim | Offline | Revocation | Network or log | UI | CLI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Artifact Signing | yes | partial | not verified | not verified | no | partial | not verified | partial | not verified | yes | yes | not verified |
| eSigner for Code | yes | partial | not verified | not verified | no | partial | not verified | no | not verified | yes | yes | not verified |
| Software Trust Manager | yes | partial | not verified | not verified | no | partial | not verified | no | not verified | yes | yes | yes |
| SignPath | yes | not verified | not verified | not verified | not verified | partial | not verified | not verified | not verified | not verified | not verified | not verified |
| Adobe apps + Inspect | not verified | yes | not verified | no | no | yes | partial | no | not verified | yes | yes | no |
| Entra + Authenticator | yes | partial | not verified | no | no | partial | yes | not verified | not verified | yes | yes | no |
| Apple Wallet ID | partial | partial | no | no | no | no | partial | not verified | not verified | not verified | yes | no |
| GitHub artifact attestations | no | partial | no | no | no | yes | partial | not verified | not verified | partial | not verified | yes |
| GPG Suite | not verified | not verified | not verified | not verified | not verified | not verified | not verified | not verified | not verified | not verified | yes | not verified |
| GnuPG | yes | yes | partial | partial | partial | partial | partial | yes | yes | partial | no | yes |
| Sequoia `sq` | yes | yes | partial | partial | partial | partial | partial | yes | partial | partial | no | yes |
| Thunderbird OpenPGP | yes | partial | not verified | not verified | no | no | yes | partial | not verified | partial | yes | no |
| Cosign (keyless, as documented) | partial | partial | no | no | no | yes | partial | not verified | partial | yes | no | yes |
| Rekor | no | no | no | no | no | partial | no | no | no | yes | no | yes |
| in-toto | partial | partial | no | not verified | no | yes | no | yes | not verified | no | no | yes |
| slsa-verifier | no | not verified | no | no | no | yes | not verified | not verified | not verified | not verified | no | yes |
| policy-controller | no | partial | no | not verified | no | yes | no | not verified | not verified | yes | no | yes |
| Witness | partial | partial | not verified | not verified | no | yes | no | partial | not verified | partial | no | yes |
| c2patool | partial | yes | not verified | no | no | yes | partial | partial | not verified | partial | no | yes |
| SignServer CE | partial | not verified | not verified | not verified | no | yes | not verified | not verified | not verified | yes | not verified | not verified |

Notes on `partial`, only where the word would otherwise hide the mechanism:

- **SignPath, keys.** The crypto-providers page says the private key
  remains on the HSM during signing. Everything else in that row is still
  not verified. See section 10.8.
- **Artifact Signing / eSigner / Software Trust Manager, roots and statement.**
  The thing signed is a digest. The trust root is a CA the platform already
  has, or a private CA the tenant operates. That is not a local unsigned
  root for one topic.
- **Artifact Signing, offline.** The file stays on the endpoint; signing
  still needs the service.
- **Inspect, readable claim.** Author, tools, and issuer organization are
  shown. A certificate off the C2PA trust list is "Unrecognized". There is
  no vocabulary sentence and no standing check.
- **Authenticator, statement.** The statement is about a person (claims),
  not about an artifact.
- **GitHub, network.** Public repositories use a public log. The docs say
  the private-repository instance has no transparency log.
- **GnuPG / `sq`, delegation and threshold.** See section 5. The threshold
  is a count of introducers, or a trust amount, not a k-of-n subject.
- **GnuPG, local names.** A non-exportable certification stays on one
  machine, but it certifies a global User ID.
- **Cosign, keys and revocation.** The documented flow creates an ephemeral
  key and a short-lived certificate, then discards the key. Longer-lived
  keys were not verified. Expiry of that certificate is the revocation story
  that was actually written down.

## 5. PGP and OpenPGP trust indicators

### 5.1 Which specification

RFC 9580 (July 2024, Proposed Standard) obsoletes RFC 4880, RFC 5581, and
RFC 6637. The datatracker page for RFC 4880 says it is obsoleted by RFC
9580. The trust-signature and trust-packet text below is quoted from RFC
9580, which was fetched. The RFC 4880 body was not re-read; the GnuPG manual
still cites it for trust signatures.

RFC 9580 is explicit that it specifies packet formats, not a trust model and
not key storage. Section 5.2.1 says the vagueness of signature meanings is
intentional, because "OpenPGP places final authority for validity upon the
receiver of a signature".

### 5.2 Two different things, often shown as one

**Validity** is whether a User ID is bound to a key, calculated from
certifications. **Ownertrust** is whether the user has decided that this key
may certify other keys. GnuPG's `--edit-key` listing prints both on the
primary key: "trust" is the assigned ownertrust, "validity" is calculated.
The same letter codes are used for both (manual, "Trust Values"):

| Code | Shown as | Meaning in that table |
|---|---|---|
| `-` | unknown | No ownertrust assigned / not yet calculated |
| `e` | expired | Calculation failed; probably an expired key |
| `q` | undefined | Not enough information |
| `n` | never | Never trust this key |
| `m` | marginal | Marginally trusted |
| `f` | full | Fully trusted |
| `u` | ultimate | Ultimately trusted |
| `r` | revoked | Validity only: key or User ID revoked |
| `?` | err | Unknown value |

Ownertrust is local. RFC 9580 §5.10 defines the Trust packet (type 12) as
keyring-local data recording which keyholders are trustworthy introducers.
The format is implementation-defined. Trust packets SHOULD NOT be exported,
and SHOULD be ignored except on a local keyring. Setting ownertrust
(`--edit-key` → `trust`, or `--quick-set-ownertrust`) updates GnuPG's
trustdb immediately. It does not certify the key.

A certification is a different object. Signature types 0x10–0x13 certify a
User ID and differ only in how much checking the certifier claims to have
done (generic, persona, casual, positive). RFC 9580 says most
implementations emit generic (0x10) and few distinguish the others. A
non-exportable certification (§5.2.3.19) is how a user marks a key valid on
their own implementation; it is stripped on export. GnuPG's `lsign` /
`--quick-lsign-key` produces that. **Signing the key is what makes it
valid. Assigning ownertrust is what lets it make other keys valid.** The
manual's trust-model text says using the web of trust properly means both:
actively signing keys, and marking users as trusted introducers.

### 5.3 Trust signatures are not SPKI delegation

RFC 9580 §5.2.3.21, Trust Signature subpacket (type 5): one octet of level
(depth), one octet of trust amount. Level 0 means an ordinary validity
signature. Level 1 asserts the signed key is a trusted introducer, and the
second octet is the degree. Level n asserts the key may issue level n−1
trust signatures. Trust amount is 0–255. Values below 120 are partial; 120
or greater is complete. Implementations SHOULD emit 60 for partial and 120
for complete.

§5.2.3.22, Regular Expression, is only meaningful with a trust signature of
level greater than 0. It limits which User IDs the introduced key's
signatures will be trusted for. The pattern is Henry Spencer's "almost
public domain" syntax, matched against the User ID as UTF-8, and the
subpacket includes a trailing NUL.

That is the whole scoping mechanism: depth, an amount, and a regex over a
display string. It delegates **the right to certify names**, not the right
to assert a predicate about an artifact. There is no tag, no intersection,
and no closed reduction.

GnuPG's `--quick-tsign-key` writes this subpacket. Its `trustspec` maps `f`
/ `full` to 120 and `m` / `marginal` to 60, and takes a depth plus an
optional domain. The manual still tells the reader to see RFC 4880 for the
definition. `--trust-model pgp` (web of trust plus trust signatures, "PGP
5.x and later") is the default when a new trust database is created.
`--trust-model classic` is the PGP 2 web of trust without that. Defaults
elsewhere in the same manual: `--completes-needed` 1, `--marginals-needed`
3, `--max-cert-depth` 5. One fully trusted introducer, or three marginal
ones, is enough to make a new key valid. That is a count of people, not a
threshold subject.

Key flags (§5.2.3.29) include "the private component of this key may have
been split by a secret-sharing mechanism" (0x10) and "may be in the
possession of more than one person" (0x80). They are hints on a
self-signature. The RFC does not define an m-of-n verification procedure for
them. They are not a threshold subject.

Sequoia uses the same 120-point scale (section 3.2) but puts the root in a
local key the program creates, and records fetch provenance as shadow CAs.
Depth is still "how many introducer hops", not "which predicate".

### 5.4 What a client shows when the signature verifies and the key is not trusted

GnuPG separates the cryptographic result from the trust result, and then
prints both.

In `g10/mainproc.c` on `master`, a signature that checks, is not expired,
and is not from an expired or revoked key is `STATUS_GOODSIG`. The primary
User ID is printed with that line. If the user asked to show User ID
validity, the calculated trust value is appended. Independently,
`g10/pkclist.c` switches on the trust mask and, for `TRUST_UNKNOWN` and
`TRUST_UNDEFINED`, prints:

> WARNING: The key's User ID is not certified with a trusted signature!
> There is no indication that the signature belongs to the owner.

(The non-User-ID form is "This key is not certified with a trusted
signature!") For `TRUST_MARGINAL`:

> WARNING: The key's User ID is not certified with sufficiently trusted signatures!
> It is not certain that the signature belongs to the owner.

For `TRUST_NEVER` the same function prints "WARNING: We do NOT trust this
key!" and "The signature is probably a FORGERY." and returns a bad-signature
error. The comment above that case says this level can come from TOFU, which
supports negative assertions. `TRUST_FULLY` and `TRUST_ULTIMATE` print no
such warning.

So a relying party can see a **good** signature and, in the same check, a
warning that the name is not bound strongly enough. The warning is easy to
miss, and the word "FORGERY" is used for a negative trust assertion, which
is a stronger claim than "not certified". `--trust-model always` skips key
validation, treats used keys as fully valid, and suppresses the `[uncertain]`
tag. The manual says not to use it unless some other validation scheme
exists. Expired, revoked, and disabled keys are still refused under that
model.

TOFU (`--trust-model tofu`) is documented as experimental and as weaker than
the web of trust: it remembers the first key seen for an email address and
warns on a conflict. The default `auto` policy marks a binding marginally
trusted. `tofu+pgp` takes the maximum of the two models.

Thunderbird's strings, for a signature that is present:

| State | Heading | Explanation in the string |
|---|---|---|
| Key not accepted yet | Uncertain Digital Signature | "you haven't yet decided if the signer's key is acceptable to you." |
| Accepted, not verified | (see note) | "a valid digital signature from a key that you have already accepted. However, you have not yet verified that the key is really owned by the sender." |
| Verified | (see note) | "a valid digital signature from a verified key." |
| Rejected | Invalid Digital Signature | "you have previously decided to reject the signer key." |
| Technical failure | Invalid Digital Signature | corrupted or modified. |

The same file also defines the titles "Uncertain Digital Signature",
"Good Digital Signature", and "Invalid Digital Signature", and separate
accessible names for the icons: "Good signature", "Verified signature",
"Unverified signature", "Unknown signature status", "Bad signature". Which
title is paired with which explanation is a property of the caller, which
was not read, so the table does not assert that pairing except where the
explanation string itself says "valid". The useful split inside the
explanations is **accepted** versus **verified**. There is no string in
that file for marginal ownertrust, trust depth, or a regex scope.

## 6. What a relying party already expects

From the products above, a person checking something already expects:

1. **A cryptographic result that is not the whole answer.** GnuPG prints
   "good" and then a trust warning. Thunderbird prints "good" and then
   "not yet verified". GitHub's docs say a valid attestation is not a
   statement that the artifact is secure. Inspect shows a manifest and, in
   another section, whether the signer is recognized.
2. **A name for the signer.** A User ID, an OIDC identity, an organization
   in a certificate, an issuer DID and domain, or a state issuing authority.
   The name is almost always global and issuer-supplied.
3. **A root they did not have to build.** A platform CA, the C2PA trust
   list, Fulcio, `did:web`, or the state that enrolled the license. Local
   roots exist (GnuPG ownertrust, Sequoia's local trust root, Thunderbird's
   accept button) and are widely treated as the expert path.
4. **A durable local decision.** Accept the key, set ownertrust, link a
   certificate, trust this issuer. Not a fresh out-of-band check on every
   file.
5. **Expiry or revocation as a visible third state**, at least in OpenPGP
   (revocation signatures, expired keys) and in Sigstore (short-lived
   certificates). Many commercial UIs were not verified on this point.
6. **For an artifact, a digest bound to a builder or a tool chain**, and a
   short human description (Content Credentials' "nutrition label", GitHub's
   workflow and repository). Not a raw signature blob.
7. **For a supply-chain consumer, an expected source.** `gh attestation
   verify -R owner/repo` fails closed on the wrong repository. in-toto fails
   closed on a functionary who is not in the layout. The expected source is
   a parameter or a file the verifier already has. It is not derived by
   reducing a chain the signer presented.

What the market does **not** show, on any page fetched here, is a reduced
delegation chain rendered as a sentence, with authorization separated from
authenticity, for an arbitrary vocabulary. That absence is the gap APP-0001
already names. It is not a reason to copy the indicator the market uses
instead.

## 7. What m-of-n should copy, change, or refuse

Proposals only. They do not amend APP-0001 or PLAN-0004, and they do not
accept a stack, an encoding, or a revocation design.

### 7.1 Copy

- **Keep the split Thunderbird and GnuPG already had to invent:** one line
  for "the signature checks", another for "I have not accepted this key".
  APP-0001's six-dimension verdict is that split made explicit. Do not
  collapse it into a single padlock.
- **Copy GitHub's sentence, not its identity.** A valid provenance that
  names the real builder can still be the wrong thing to trust. The verdict
  should be able to say that in the authorization line.
- **Copy Inspect's habit of showing the claim in words** (author, tool,
  issuer) and Sequoia's habit of recording why a certificate is present
  (shadow CA, trust amount). The wallet's domain file is the place those
  words come from. The "why this root" for a collected statement can be as
  small as which file it was loaded from. That is not a network.
- **Copy the accept-the-issuer moment** from Authenticator ("it is your
  choice if you trust this issuing party") and from Thunderbird's accepted /
  rejected keys. In this design that moment is an unsigned trust root, and
  it is scoped. Section 7.3 says what not to copy about how far the
  acceptance reaches.
- **Copy short-lived authority as a fact the verifier computes**, which
  Sigstore does with certificate expiry and which APP-0001 already prefers
  to a revocation protocol. Show expiry as its own outcome when a validity
  window exists. Do not invent a revocation protocol in this memo.

- **Copy passphrase protection of a key that stays a file**, and the
  split where the signer asks for the passphrase and the caller gets a
  signature rather than the key. Section 10 is the survey. Section 10.7
  is the proposal. It does not pick an algorithm.

### 7.2 Change

- **Names.** Every product above binds a global string (User ID, email,
  domain, organization, workflow) to a key and then trusts the string.
  Change the display so the sentence's names are expansions under a naming
  key the relying party already holds. A global string inside a credential
  is evidence, not the principal.
- **The good-signature line is too loud.** GnuPG's trusted and untrusted
  cases share the words "Good signature". Thunderbird's accepted-unverified
  case is also "Good Digital Signature". The wallet's primary sentence
  should be the authorization result. "Signature valid" is one dimension,
  not the headline.
- **Delegation should be shown as the chain that reduced**, not as a trust
  amount. The Sequoia book that was fetched explains depth with an
  Alice/Bob/Carol/Dave example and does not render a predicate. A wallet
  view that lists "root → delegation → statement" in the words of the
  vocabulary is the change. PLAN-0004's verdict view is the place. It is
  still reduction, not a graph query.
- **Thresholds.** Where the market has a number, it is "3 marginal
  introducers or 1 full one", or a 0–255 trust amount, or an enterprise
  approval step that was not verified as cryptography. Change that to a
  k-of-n subject on the statement, or leave thresholds as the cut APP-0001
  already allows. Do not present a count of introducers as if it were m-of-n.

### 7.3 Refuse

- **Refuse ownertrust as the authorization model.** Ownertrust answers "may
  this key certify other people's names?" The wallet's question is "may
  this key assert this predicate about this subject?" Using one scalar for
  both is how a valid signature becomes a trusted statement. Do not add
  ownertrust, marginal-versus-full, or `--marginals-needed`.
- **Refuse the web of trust.** Trust signatures plus a regex over a User ID
  are the standard's scoped delegation. They do not reduce, they do not
  narrow a predicate, and they treat a display string as a capability. The
  regex is also the wrong layer: it re-parses a name the key holder was
  free to write. Local names are defined by a naming key, not matched out
  of a User ID.
- **Refuse "probably a FORGERY" for an uncertified key.** GnuPG uses that
  sentence for `TRUST_NEVER`. Lack of a certification is not evidence of
  forgery. The wallet should say "no standing" or "not accepted", and stop.
- **Refuse a global trust list as the root.** C2PA's list, Fulcio, a public
  CA, and `did:web` all make "recognized organization" look like
  authorization. Inspect's "Unrecognized" is the failure mode those systems
  have. A recognized signer with no delegation is the failure mode this
  project cares about, and those UIs do not show it. A local unsigned root
  stays the floor, as APP-0001 already says.
- **Refuse keyless OIDC identity as the principal.** Cosign's overview is
  right that long-lived keys are easy to lose and that a log makes signing
  events public. The principal in this design is still a key. An OIDC email
  or a workflow name can be a claim a key makes. It is not a substitute for
  the key.
- **Refuse a network dependency in the verdict.** Rekor, keyservers, the
  C2PA trust-list URL, and Authenticator's issuance flow all assume a
  service is reachable. PLAN-0004 says no network. The market's logs are
  evidence a relying party may *already hold*, the way a shadow CA records
  a download after the fact. Fetching them during `check` would make the
  verdict depend on a third party. Do not add that.
- **Refuse cloud HSM custody as the wallet.** Artifact Signing, eSigner,
  and Software Trust Manager keep the private key in a service the user
  does not hold. That matches a company signing pipeline. It contradicts
  "keys are files" and "no keychain product". The demo wallet should not
  grow a hosted signing service in order to look like those products.
- **Refuse to treat OpenPGP's group-key and split-key flags as m-of-n.**
  They are advisory bits. They do not evaluate a share.

- **Refuse a long-lived unlocked agent, a passphrase on the command
  line, and moving the private key out of a file** into a platform store
  or a token for the CLI milestone. Section 10 says what each of those
  protects and what it does not. Hardware-backed keys are a later option,
  not a change accepted here.

### 7.4 Delegation chains and key-centric trust, against ownertrust and the web of trust

This is the comparison the rest of the memo is for.

| | PGP ownertrust and the web of trust | This design |
|---|---|---|
| Principal | A key, but almost always reached through a User ID string | A key or its digest |
| What "trust" means | This key may certify other keys' names, fully or marginally | An unsigned local root: this key may speak on this topic |
| How trust moves | A trust signature carries depth and an amount. One full introducer, or three marginal ones, validates a name. Depth counts hops of introducers | A delegation statement is itself a signed claim, narrowed by intersection, then reduced. There is no marginal amount |
| Scope | A regular expression over the User ID | The delegation's topic and the subject's identity, reduced |
| What a signature on an object means | Type 0x00: the signer owns it, created it, or says it was not modified | A typed value from a domain, rendered by that domain |
| Local names | A non-exportable certification, or a Trust packet that must not be exported. The name certified is still a global User ID | A name defined by a naming key. Meaningless under any other key |
| What the person reads | "Good signature from Alice <alice@example.com>" plus a warning if the binding is weak | The rendered sentence, and a separate line if the key has no standing |
| m-of-n | Not specified. A hint flag, or a count of introducers | A threshold subject, if the floor includes it. Not a property of trust |

Ownertrust cannot be patched into this. It is a second, local, non-exported
opinion about whether someone's *certifications of names* count. The wallet
already has a place for that kind of unsigned opinion: the trust root. The
change is that the root is not "I trust Alice's key in general". It is "I
trust this key for this topic", and everything past the root is a chain the
reducer either accepts or names the break in.

The web of trust's one idea worth keeping is the one RFC 9580 states
outright: the receiver, not the signer, decides validity. That is already
the trust root. The machinery built on top of it — introducers, marginal
counts, regex scopes, and a single "good signature" line — answers a naming
problem this design handles with local names, and it never asks the
authorization question at all.

## 8. What this does not decide

- DEC-002 stays open. Nothing here selects an encoding.
- APP-0001's open questions (command name, domain lookup, `--json`, whether
  the prototype encoding may ship, whether thresholds are in the floor) stay
  open.
- PLAN-0004's proposed stack stays a proposal on PR 57. This memo does not
  merge it and does not depend on it being merged. Section 10.7 is a
  proposal for that plan. This branch does not edit the plan.
- No KDF, AEAD mode, or secret-key packet format is selected. DEC-002
  stays open, so secret-key encryption is not an encoding decision either.
- No product in section 2 or 3 is nominated as the implementation.

## 9. Products and facts not verified

- DigiCert public price, and any approval-workflow claim that lives only on
  the marketing site (that site blocked the fetch).
- SignPath price, key custody, UI, and whether "approved by the right
  people" is a cryptographic delegation.
- GPG Suite price, and its signature-status UI.
- Proton Mail's display of an untrusted signature.
- A Windows or macOS dialog after Artifact Signing, eSigner, or Software
  Trust Manager has signed a file.
- GitHub's website UI for attestations, and offline `gh` verification (a
  separate doc exists; it was not fetched).
- Cosign with a long-lived key or PKCS#11.
- Whether current GnuPG implements RFC 9580 packet changes, or only the
  trust behaviour in the manual and `master` sources cited here.
- Whether Thunderbird implements trust signatures, marginal trust, or
  revocation in the UI. Only `msgReadStatus.ftl` on `master` was read.
- Apple's on-screen wording when a license is presented, and whether
  presentation works offline.
- Entra revocation and offline presentment.
- in-toto thresholds; slsa-verifier behaviour past its README; SignServer
  Enterprise price and UI.
- Section 5.10's implementation-defined trust-packet bytes (intentionally
  unspecified). GnuPG's trustdb format was not read.
- The KDF inside signify and minisign. Both man pages say the secret key
  is passphrase-protected and do not name the function.
- Whether a YubiKey OpenPGP key is non-exportable. The page that was
  fetched documents touch-to-verify, not export.
- Whether CNG's on-disk key containers are encrypted. The Learn page
  documents the directories and process isolation, not the file format.
- A Python standard-library equivalent of `sodium_memzero`. The
  `secrets` module page documents generating secrets, not wiping
  memory. No wipe function is named there. See section 10.7.
- Whether macOS `ps` shows a passphrase passed in argv. Linux
  `/proc/pid/cmdline` was fetched. The non-goal does not depend on the
  macOS case.
- Where a Developer ID private key sits during Apple notarization. The
  notarization page does not say. It is not evidence of cloud custody,
  and it is not evidence against it.

## 10. Private-key protection

Proposals only, same as section 7. This section is how a **local personal
wallet** keeps a private key that is a file. It does not close DEC-002,
and it does not pick a cipher.

A technique is in here only if a page fetched on 2026-10-02 says so.
"Protects" means the thing that page actually claims. A copied wallet
without its passphrase is the at-rest case. Memory, another local user,
the calling process, and export are separate, and most of these tools
cover only the first.

### 10.1 OpenPGP secret-key encryption (RFC 9580)

RFC 9580 §3.7 defines a string-to-key (S2K) specifier: it turns a
passphrase into a symmetric key. The two uses named there are encrypting
the secret part of a private key, and symmetrically encrypted messages.
This section is the first of those.

§3.7.1 lists four specifier types. Simple S2K (id 0) and Salted S2K
(id 1) are not for new data, except Salted S2K when the implementation
knows the string is high entropy. Iterated and Salted S2K (id 3) and
Argon2 (id 4, citing RFC 9106) may be generated. Argon2 takes a 16-octet
salt, passes, parallelism, and a memory size in kibibytes, and the RFC
says to invoke Argon2id.

§3.7.2: an implementation MUST NOT generate Simple S2K. It SHOULD NOT
generate Salted S2K for a low-entropy passphrase. Argon2 is RECOMMENDED.
Iterated and Salted S2K MAY be used if Argon2 is not available, with a
high octet count and a strong passphrase, and the RFC says that method
does not provide memory hardness.

§3.7.2.1 is the secret-key encryption octet, the first octet after the
public key material in a Secret Key packet (§5.5.3). Zero means the
secret material is not encrypted. 253 is AEAD and may be generated. 254
is CFB and may be generated. 255 (MalleableCFB) and the legacy
cipher-id-in-the-usage-octet form must not be generated. Argon2 is only
legal with usage octet 253; any other combination MUST be rejected.

§5.5.3: for usage 253 the key-encryption key is HKDF (RFC 5869) with
SHA-256, no salt, and an info string taken from the packet. The secret
material is one AEAD plaintext with one authentication tag. The
additional data includes the public-key fields. Usage 254 appends a
SHA-1 of the plaintext and encrypts it with CFB. Usage 0 stores the
secret in the clear (v6 has no trailing checksum).

§13.7: a version 6 secret key SHOULD be protected with AEAD (usage 253)
unless it must be read by an implementation that has no AEAD. The same
section says CFB-encrypted secret keys (254 or 255) can leak secret data
if an attacker who can write the encrypted key corrupts it and the key
is later used.

What this protects: at rest, against someone who has the file and not
the passphrase, and only when the usage octet is not zero. AEAD (253)
also rejects a modified ciphertext instead of releasing a mangled key
(§13.7). What it does not protect: the key after it has been decrypted,
another user who can read the process that decrypted it, a caller that
has been handed the plaintext, or export — the file is the key. A weak
passphrase is outside the mechanism. It fits a file-based offline
wallet as a **candidate**, not as a chosen format. Choosing the OpenPGP
packet would be an encoding decision, and DEC-002 is open.

### 10.2 GnuPG `gpg-agent`

The manual's "Invoking GPG-AGENT" says `gpg-agent` is a daemon that
manages secret keys independently of any one protocol, and that a
pinentry program must be installed (or named with `pinentry-program`).
The agent is what `gpg` starts on demand. The passphrase prompt is that
separate program, not an argument of `gpg`.

Agent protocol §2.6.2, `PKSIGN`: the client sets a keygrip and a hash.
The agent checks the key, asks for the passphrase, and returns a
signature S-expression. The example session in that section says the
agent asked the user for the passphrase and then returned the signature.
The client does not receive the secret key on that command.
`OPTION use-cache-for-signing=0` makes that operation ignore the
passphrase cache. The command-line form of the same idea is
`--ignore-cache-for-signing`.

The cache is not "until logout". Agent options: `--default-cache-ttl`
defaults to 600 seconds and resets on use; `--max-cache-ttl` defaults
to 7200 seconds and does not reset. The SSH-key variants default to
1800 and 7200 seconds.

This is not non-exportable storage. §2.6.5, export of a secret key
through the agent protocol, is documented as "Not implemented."
§2.6.7, `GET_PASSPHRASE`, can return the passphrase to the client, in
hex, for a caller that asks. A secret key that lives in a file can
still be copied as that file. The trust-indicator behaviour in section
5 is a different question and is not repeated here.

What this protects: the calling process, on the `PKSIGN` path, does not
hold the secret key, and a cache entry dies. What it does not protect:
the same user, root, a client that calls `GET_PASSPHRASE`, or anyone
who copies the secret-key file. A cache of two hours is a long time.
It fits the **shape** of v1 (the engine holds the unlocked key; the CLI
does not). It does not fit as a dependency, and a cache with no maximum
lifetime would not fit at all.

### 10.3 SSH

OpenSSH `PROTOCOL.key` (in the portable tree, `$OpenBSD: PROTOCOL.key,v
1.4`) describes `openssh-key-v1`. The file holds a cipher name, a KDF
name, KDF options, the public keys, and an encrypted list of private
keys. For `kdfname` `bcrypt` the options are a salt and a round count.
Unencrypted keys use cipher `none` and KDF `none`. A checkint is
duplicated so decryption can be tested.

`ssh-keygen(1)` asks for a passphrase when it writes a private key. The
passphrase may be empty. The man page says the default format is
OpenSSH-specific and is preferred because it protects keys at rest.
`-a` sets the KDF rounds, "currently `bcrypt_pbkdf(3)`", default 32.
There is no recovery of a lost passphrase. `ssh(1)` says the same
passphrase encrypts the sensitive part of the private key file using
AES-128. `PROTOCOL.key` says the cipher is a field in the file rather
than one fixed algorithm. Both pages were fetched. They are not the
same sentence. This memo does not pick which one a given file uses.

`ssh(1)` also says a private key file should be readable by the user
and not accessible by others, and that `ssh` ignores a private key file
that is accessible by others. It recommends the same for `~/.ssh`:
read, write, and execute for the user, not accessible by others. It
does not print the numbers 0600 or 0700. Those numbers in section 10.7
are this project's proposal for that rule.

`ssh-agent(1)` holds private keys. The man page says authentication
passphrases and private keys never go over the network when the agent
is forwarded: the socket is forwarded, and the agent returns the
result. The socket "is accessible only to the current user, but is
easily abused by root or another instance of the same user." Without
`-t`, the default maximum lifetime of an identity is forever.
`ssh-add(1)` `-c` marks an identity so use requires confirmation
through `ssh-askpass(1)`. `-t` sets a lifetime. The private key on disk
is still a file. The agent holds a copy.

What the passphrase protects: the file at rest. What the mode protects:
other users reading the file, if the mode is actually that. What
confirm-before-use protects: an agent-held key being used with no one
at the keyboard. What none of this protects: root, another process of
the same user that has the agent socket, a key whose passphrase is
empty, or export of the file. An agent whose default lifetime is
forever is the case section 10.9 refuses.

### 10.4 signify, minisign, age

`signify(1)` `-G` writes `keyname.pub` and `keyname.sec`. Unless `-n`
is given, it prompts for a passphrase to protect the secret key. A
wrong passphrase is one of the documented failure reasons. The secret
key is a file. The man page does not name a KDF, an agent, or a KMS.
That absence is what was fetched, not a claim that the implementation
has no KDF.

`minisign(1)` `-G` writes a public key and encrypts the secret key to
a file (`~/.minisign/minisign.key` in the example). `-W` means do not
encrypt or decrypt the secret key with a password. `-C` changes or
removes the password. The man page does not name a KDF, an agent, or a
KMS.

`age(1)` identities are files. A native identity is a line beginning
`AGE-SECRET-KEY-1` (or `AGE-SECRET-KEY-PQ-1` for the hybrid). The same
manual says a passphrase-encrypted age file can itself be an identity
file, and that the passphrase is requested interactively. It also says
passphrase-protected identity files are not necessary for most use
cases, "where access to the encrypted identity file implies access to
the whole system." For SSH keys used as identities, the manual says
keys held on hardware tokens such as YubiKeys, or accessed via
`ssh-agent(1)`, are not supported.

The age v1 specification's scrypt recipient encrypts the file key, not
a long-term signing key by a different name. The stanza carries a
16-byte salt and a work factor. The wrap key is scrypt (RFC 7914) with
`r = 8`, `p = 1`, and a domain-separated salt. The body is
ChaCha20-Poly1305 of the file key, nonce fixed at twelve zero bytes. A
scrypt stanza MUST be the only stanza in the header. That is a concrete
KDF-plus-AEAD. It is a candidate next to RFC 9580's Argon2-plus-AEAD.
It is not a selection.

All three fit a file-based offline wallet: a secret key file, a
passphrase, no agent required for the common path. age's refusal of
`ssh-agent` for SSH identities is the same refusal as section 10.9.
The README notes a YubiKey plugin as an extension. That plugin is the
hardware case in section 10.6, not the default.

### 10.5 Wrapping by the operating system

Two different operations get called "use the keychain".

**Wrap the passphrase only.** The private key stays a file. A copy of
the wallet still needs the passphrase, and the passphrase now also
needs that machine's store. The file remains portable if the user still
knows the passphrase.

**Move the private key into the OS store.** The wallet no longer has a
file it can copy onto another machine and unlock. That breaks "keys
are files". It is not v1.

macOS, two different layers. Apple's "Storing Keys in the Keychain"
says the keychain is the place to store small secrets, including
cryptographic keys, and that an application adds and retrieves items.
"Protecting keys with the Secure Enclave" says a key that is only in
the keychain is still copied into memory in the clear when it is used.
A key created in the Secure Enclave is not: the application never
handles the plaintext, the enclave cannot take a preexisting key, and
the keys are NIST P-256 only. `kSecAttrTokenIDSecureEnclave` is that
second path. Apple Platform Security's keychain chapter says items live
in a SQLite database, `securityd` decides which process may read them,
and access groups share items across apps from the same developer
rather than limiting them to one process. Secret values are encrypted
with AES-256-GCM. A "this device only" class does not survive restore
onto another device. An ACL can require a biometric or the passcode,
evaluated in the Secure Enclave.

So the keychain can store a passphrase (the first operation). The
Secure Enclave is the second operation, and it cannot even import the
file key this wallet already has.

Windows DPAPI. `CryptProtectData` encrypts a blob the caller still
holds. Typically only a user with the same logon credential can decrypt
it, and encryption and decryption usually must happen on the same
computer. `CRYPTPROTECT_LOCAL_MACHINE` binds the blob to the computer
instead, and any user on that computer can decrypt it. Optional extra
entropy, if used, has to be presented again on decrypt. Wrapping the
passphrase is the first operation. Wrapping the private key makes a
blob that is not a portable wallet file.

Windows CNG. The key-storage page says long-lived keys must be isolated
so they are never present in the application process, and that the
Microsoft software key storage provider runs in the LSA process. The
same page says CNG also stores private keys as files, for a user key
under `%APPDATA%\Microsoft\Crypto\Keys`, and in other directories for
machine and service keys. Those files are OS containers reached through
the key storage router. They are not a `wallet/keys` file the user
copies. Whether those files are encrypted at rest was not on the page
(section 9).

Linux kernel keyrings. `keyrings(7)` is an in-kernel store for keys and
other security data, with system calls for user space to use it for its
own purposes. A key has permissions for possessor, user, group, and
other, and one of the bits is read. It is not a file in the wallet, and
it is not a non-exportable token: a caller with read permission can
read the payload.

Secret Service. The freedesktop specification says a client stores a
secret in a service running in the user's login session, and retrieves
it with `GetSecret`. Locked collections are not readable until the
service unlocks them, which may prompt for a master password. The
secret is returned to the client. That fits a passphrase. It does not
fit the private key, because the key would no longer be the file.

None of these are v1 requirements. The optional later step in section
10.7 is the passphrase-only wrap. Putting the private key in any of
them is out of scope for the same reason a token is.

### 10.6 Hardware tokens

Not v1. The private key would no longer be a file the wallet holds.
This is a later option. It is not an accepted change.

GnuPG's OpenPGP card howto: `generate` generates the key on the card.
The prompt asks whether to make an off-card backup of the **encryption**
key, and says that without that backup encrypted data is unrecoverable
if the card is lost. The signature key is not given that prompt in the
text that was fetched. The card has a PIN and an Admin PIN. `forcesig`
toggles "the signature force PIN flag". `gpg --card-status` in that
howto prints "Signature PIN ....: forced". A signature, in that setup,
needs the card and the PIN. It does not need a key file, except for the
optional encryption-key backup the howto recommends.

YubiKey's OpenPGP notes (the 5.2.3 enhancements page) say the touch
policy can require a touch on the hardware before an OpenPGP
cryptographic operation. Firmware 5.2.3 adds a touch cache: one touch
unlocks OpenPGP operations for up to 15 seconds, or until the session
ends. The page does not say the private key cannot be exported. That
part is not verified. A 15-second cache is also not the same thing as
a touch on every signature.

PKCS #11 v3.0 (the OASIS base specification): if `CKA_EXTRACTABLE` is
`CK_FALSE`, certain attributes of the private key cannot be revealed
in plaintext outside the token. `CKA_ALWAYS_AUTHENTICATE` can force the
user to provide a PIN for each sign or decrypt. The token may still
allow wrapping when extractable is true. "Non-exportable" is that
attribute, not a property of every PKCS #11 object.

age's SSH path refusing YubiKeys (section 10.4) is the same boundary
from the other side: the file tool does not pretend to drive the token.

### 10.7 What fits v1

Proposed. The lines that only restate "keys are files" and "no cloud
custody" are requirements that follow from constraints already in
PLAN-0004 and section 7.3. The modes, the prompt, and the wipe are the
proposal.

- Private keys are files under `wallet/keys`. The directory is mode
  0700. Each private key file is mode 0600. That is the numeric form of
  the rule `ssh(1)` states as "not accessible by others".
- Each private key file is encrypted at rest, so a copied wallet is
  useless without the passphrase. The mechanism is passphrase-based
  secret-key encryption. The candidates that were actually read are
  RFC 9580 S2K with AEAD (usage octet 253, Argon2 recommended) and a
  single modern KDF plus AEAD (the age specification's scrypt and
  ChaCha20-Poly1305 is one that was read end to end). No winner.
  DEC-002 is still open, so this is not an encoding choice either.
- The engine prompts for the passphrase. It is not a command-line
  argument. On Linux, `/proc/pid/cmdline` holds the complete command
  line of a running process (`proc_pid_cmdline(5)`), so an argument is
  visible to anything that can read that file. The passphrase is not
  logged.
- The plaintext key exists only inside the engine, for one signature,
  and is then wiped. libsodium's `sodium_memzero` exists because a
  compiler or linker may delete a `memset` of memory that looks
  unused. `sodium_mlock` asks the kernel not to swap that memory;
  `sodium_munlock` zeroes it before unlocking. The Python `secrets`
  module, fetched the same day, generates secrets and does not
  document a wipe. No standard-library equivalent was on that page
  (section 9).
- The CLI asks the engine to sign. The engine holds the unlocked key.
  Callers do not. That is the `PKSIGN` shape in section 10.2, without
  a cache that outlives the one operation.
- Optional, and not this milestone: an OS store from section 10.5 holds
  the **passphrase**, not the key. The key file stays the file.
- A hardware-backed non-exportable key is out of scope for the CLI
  engine milestone, because the private key would no longer be a file
  (section 10.6).

### 10.8 Commercial signers, custody only

These are the contrast. m-of-n does not take custody of the key in a
service.

Sections 2.1 through 2.3 already say Artifact Signing, eSigner, and
Software Trust Manager keep the private key in the vendor's HSM or
service. The client sends a digest, or signs through the vendor's
tool. That is cloud custody.

DigiCert KeyLocker's benefits page says KeyLocker generates and stores
the private key in HSM storage, generates the certificate request, and
requires multi-factor authentication to sign. The page's argument for
cloud storage is that a hardware token can be lost and that an
on-premises HSM is costly. The private key is not a file the user
holds.

SignPath, which section 2.4 could not settle from the homepage: the
managing-certificates page says creating the CSR in SignPath creates
the private key on SignPath's HSM, and that importing a PFX is worse
because the key may already have been exposed. The crypto-providers
page says the provider implements KSP, PKCS #11, or CryptoTokenKit so
that local tools can sign, and that during the operation the private
key remains on the HSM. Price and the relying-party screen remain not
verified.

Apple notarization is not this. The notarization page says the notary
service scans Developer ID-signed software for malicious content and
code-signing issues and, if it finds none, returns a ticket to staple
to the software. The page does not say Apple holds the developer's
private key. Where that key is stored was not on the page.

AWS KMS, as the plain cloud-KMS case: the concepts page says the
initial HSM backing key is generated on an HSM in the domain and is
designed never to be exported from the HSM in plaintext. What leaves
the HSM is that key encrypted under HSM-managed domain keys.

None of these is a local file. Section 7.3 already refuses that shape.
This section adds KeyLocker and SignPath, which the first pass could
not verify, and separates notarization from custody so the two are not
treated as the same product.

### 10.9 Non-goals

- Cloud HSM or KMS custody, including KeyLocker and SignPath's HSM.
  The key would not be a file the user holds.
- Keyless OIDC (Fulcio) as the principal. Already refused in section
  7.3. A short-lived certificate is not a substitute for the key.
- Putting the private key in a git repository, or in a transparency
  log. GitHub's public attestations are written to a public log
  (section 2.8). A private key is not an attestation.
- A long-lived unlocked agent with no timeout. `ssh-agent(1)`'s
  default lifetime is forever. That default is not the proposal.
- The passphrase on the command line, or in shell history because it
  was on the command line. Section 10.7.
- The Secure Enclave, a CNG key container, or a PKCS #11 token as the
  v1 key. Section 10.5 and section 10.6.
