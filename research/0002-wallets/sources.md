---
schema: "library-doc/v1"
id: R-0002-sources
title: "Sources consulted — wallet market survey"
type: evidence
status: draft
version: "0.1.0"
date: "2026-10-02"
updated: "2026-10-02"
---

# Sources

All retrievals 2026-10-02 (PT) unless noted. Each row was fetched with
WebFetch or HTTP GET from this research pass. Search-index snippets were
used only to find URLs; a claim in `report.md` is not based on a snippet
alone.

`library/` was not modified. These URLs are not `[@record-id]` citations.

## Specifications and implementation sources

| Source | URL | What it settled |
|---|---|---|
| RFC 9580 HTML | https://www.rfc-editor.org/rfc/rfc9580.html | Obsoletes RFC 4880, RFC 5581, RFC 6637. Signature types 0x00 and 0x10–0x13. Trust Signature §5.2.3.21 (depth, amount, 60/120). Regular Expression §5.2.3.22. Exportable certification §5.2.3.19. Key flags 0x10 and 0x80 §5.2.3.29. Receiver decides validity, §5.2.1. |
| RFC 9580 text, §5.10–5.11 | https://www.rfc-editor.org/rfc/rfc9580.txt | Trust packet is local, implementation-defined, and SHOULD NOT be exported. User ID is unrestricted UTF-8, conventionally a name-addr. |
| RFC 4880 datatracker | https://datatracker.ietf.org/doc/rfc4880/ | Status line: obsoleted by RFC 9580. Body not re-read. |
| GnuPG manual, key management | https://www.gnupg.org/documentation/manuals/gnupg/OpenPGP-Key-Management.html | `trust` sets ownertrust. `tsign` is a trust signature. Listing shows trust and validity separately. `--quick-tsign-key` maps full→120 and marginal→60. |
| GnuPG manual, configuration | https://www.gnupg.org/documentation/manuals/gnupg/GPG-Configuration-Options.html | Trust models pgp, classic, tofu, tofu+pgp, direct, always, auto. completes-needed 1, marginals-needed 3, max-cert-depth 5. |
| GnuPG manual, trust values | https://www.gnupg.org/documentation/manuals/gnupg/Trust-Values.html | Letter codes for ownertrust and validity. |
| GnuPG `g10/pkclist.c` on master | https://raw.githubusercontent.com/gpg/gnupg/master/g10/pkclist.c | Warning strings for unknown, marginal, and never trust, beside a signature the caller has already checked. |
| GnuPG `g10/mainproc.c` on master | https://raw.githubusercontent.com/gpg/gnupg/master/g10/mainproc.c | `STATUS_GOODSIG` versus expired, revoked, and bad. `[uncertain]` tag handling. |
| GnuPG README and COPYING on master | https://raw.githubusercontent.com/gpg/gnupg/master/README , https://raw.githubusercontent.com/gpg/gnupg/master/COPYING | README still says RFC 4880. COPYING is GPL-3. |
| Sequoia README | https://gitlab.com/sequoia-pgp/sequoia/-/raw/main/README.md | Implements RFC 9580 and RFC 9980, and deprecated RFC 4880. LGPL-2.0-or-later. |
| Sequoia book, authenticating certificates | https://book.sequoia-pgp.org/auth_certs.html | `sq pki link add` depth 0. `sq pki link authorize --depth`. Retract and expiration. |
| Sequoia book, shadow CAs | https://book.sequoia-pgp.org/bckgrnd_shadow_cas.html | Local trust root. 120/120. Shadow CA example at trust amount 40 for public directories. |
| Thunderbird `msgReadStatus.ftl` on master | https://raw.githubusercontent.com/mozilla/releases-comm-central/master/mail/locales/en-US/messenger/openpgp/msgReadStatus.ftl | Uncertain, good-but-unverified, verified, and rejected strings. MPL-2.0 header. Not pinned to a product version. |

## Products

| Source | URL | What it settled |
|---|---|---|
| Artifact Signing overview | https://learn.microsoft.com/en-us/azure/artifact-signing/overview | Managed signing, FIPS 140-3 L3 HSMs, digest signing, Public and Private Trust, Basic and Premium SKUs named. |
| Artifact Signing SKU change | https://learn.microsoft.com/en-us/azure/artifact-signing/how-to-change-sku | $9.99 and $99.99 monthly, quotas 5,000 and 100,000, $0.005 overage. |
| Artifact Signing pricing page | https://azure.microsoft.com/en-us/pricing/details/trusted-signing/ | Fetched; dollar amounts rendered as "$-". Numbers in the report are from the Learn SKU article, not this page. |
| SSL.com eSigner | https://www.ssl.com/esigner/ | Cloud HSM, CI integrations named, certificate and tier prices as quoted. |
| DigiCert signer guide | https://docs.digicert.com/en/software-trust-manager/get-started/quick-start-guides/signer-guide.html | SMCTL and Click-to-sign. Key remains in Software Trust Manager. `sign` permission. |
| DigiCert licensing | https://docs.digicert.com/en/software-trust-manager/get-started/requirements/licensing.html | Subscription units. Price via DigiCert Sales. No public price on the page. |
| DigiCert marketing page | https://www.digicert.com/software-trust-manager | Fetch returned a bot wall (about 1 KB). Not used. |
| SignPath homepage | https://signpath.io/ | Marketing description only. No price. |
| Adobe Content Credentials overview | https://helpx.adobe.com/creative-cloud/help/content-credentials.html | Nutrition-label description, Cr icon, apps named. |
| Inspect tool | https://opensource.contentauthenticity.org/docs/getting-started/inspect.md | Upload or URL. "Unrecognized" versus issuer organization on the C2PA trust list. |
| c2patool README | https://raw.githubusercontent.com/contentauth/c2patool/main/README.md | CLI reads and adds manifests. |
| c2patool usage | https://raw.githubusercontent.com/contentauth/c2patool/main/docs/usage.md | `trust` subcommand and official trust-list URL. |
| c2patool licenses | https://raw.githubusercontent.com/contentauth/c2patool/main/LICENSE-MIT and LICENSE-APACHE | MIT and Apache-2.0. |
| c2pa crate README | https://raw.githubusercontent.com/contentauth/c2pa-rs/main/README.md | Same dual license for the crate. States c2patool moved to its own repository. |
| Entra Verified ID overview | https://learn.microsoft.com/en-us/entra/verified-id/decentralized-identifier-overview | did:web, Authenticator as wallet, encrypted seed backup. |
| Authenticator Verified ID tutorial | https://learn.microsoft.com/en-us/entra/verified-id/using-authenticator | Issuer name and verified domain shown. User chooses whether to trust the issuer. |
| Add license to Apple Wallet | https://support.apple.com/en-us/111803 | Eligible state or territory ID, encrypted, Face ID or Touch ID. |
| Present license from Apple Wallet | https://support.apple.com/en-us/118237 | In-person and in participating apps and websites. |
| GitHub artifact attestations (concept) | https://docs.github.com/en/actions/concepts/security/artifact-attestations | Sigstore, SLSA v1.0 Build Level 2, public log versus private instance with no log. Not a guarantee of security. |
| GitHub how-to | https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations | `gh attestation verify`. Enterprise Cloud required for private or internal repositories. |
| GPGTools homepage and store URL | https://gpgtools.org/ and https://gpgtools.org/store | Support plan, GPG Mail 8 beta, yearly subscription announced. No numeric price in the fetched HTML. |
| Proton PGP help | https://proton.me/support/how-to-use-pgp | Key pair and "proof that you have written the message". No untrusted-signature UI. Not used as a table row. |
| Sigstore overview | https://docs.sigstore.dev/about/overview/ | Ephemeral keys, Fulcio, Rekor, what verification checks. |
| Cosign signing overview | https://docs.sigstore.dev/cosign/signing/overview/ | Keyless flow. Custom roots are a heading; that section's body was not relied on. |
| Rekor overview | https://docs.sigstore.dev/logging/overview/ | Immutable log and CLI. |
| Cosign, Rekor, policy-controller, slsa-verifier, Witness LICENSE | raw `LICENSE` on each GitHub default branch | Apache-2.0. |
| in-toto README and LICENSE | https://raw.githubusercontent.com/in-toto/in-toto/master/README.md and LICENSE | Layout, steps, functionaries, link files. Apache-2.0, NYU 2018. |
| slsa-verifier README | https://raw.githubusercontent.com/slsa-framework/slsa-verifier/main/README.md | Points GitHub users at `gh attestation verify`. |
| policy-controller README | https://raw.githubusercontent.com/sigstore/policy-controller/main/README.md | Admission controller, `ClusterImagePolicy`. |
| Witness README | https://raw.githubusercontent.com/in-toto/witness/main/README.md | in-toto, Rego, keyless Sigstore, air gap. |
| SignServer CE README | https://raw.githubusercontent.com/Keyfactor/signserver-ce/main/README.md | LGPL subset, not for production. |

## Project documents read, not external evidence

| Document | Where |
|---|---|
| APP-0001 | `project/APP-0001-application-design.md` on `origin/main` |
| PLAN-0002 §§1–2 | `project/PLAN-0002-product-spec.md` on `origin/main` |
| PLAN-0004 | worktree for PR 57, `doc/app-0001-no-kg`, not on `main` |
| research/README.md and R-0001 front matter | tone and folder shape |
