---
schema: "library-doc/v1"
id: R-0002-searches
title: "Searches — wallet market survey"
type: evidence
status: draft
version: "0.1.0"
date: "2026-10-02"
updated: "2026-10-02"
---

# Searches

Queries run on 2026-10-02. Yield is the URL that was then fetched, or an
explicit miss. Snippets were not treated as evidence.

| Query | Yield |
|---|---|
| RFC 9580 OpenPGP trust signature ownertrust validity obsoletes RFC 4880 | rfc-editor and datatracker HTML for RFC 9580. Fetched. |
| GnuPG manual "This key is not certified with a trusted signature" ownertrust validity | Manual URLs. The warning text itself was then taken from `g10/pkclist.c`, not from the forum posts in the results. |
| Microsoft Azure Trusted Signing pricing 2026 overview | Learn SKU article and Azure pricing URL. Both fetched. Pricing page did not expose numbers. |
| DigiCert Software Trust Manager code signing what users do pricing | Signer guide and licensing guide fetched. Marketing page later blocked. |
| Thunderbird OpenPGP untrusted key signature display support.mozilla.org | support.mozilla.org returned a client challenge. Bugzilla hits were not used. Strings taken from `msgReadStatus.ftl` on GitHub. |
| Sigstore cosign Rekor overview docs.sigstore.dev license | Overview, signing overview, Rekor overview, LICENSE files. Fetched. |
| Sequoia sq trust root web of trust | `book.sequoia-pgp.org` chapters. Fetched. docs.rs pages in the results were not fetched. |
| GitHub artifact attestations gh attestation verify documentation | Concept page and how-to. Fetched. Offline-verification URL in the results was not fetched. |
| C2PA c2patool verify content credentials | c2patool README and usage, Inspect doc. Fetched. |
| Apple Wallet driver's license or state ID support.apple.com | support.apple.com/111803 and /118237. Fetched. A third-party "which states" article was not used. |
| thunderbird openpgp accepted unverified signature status | searchfox returned 406. Raw GitHub file succeeded. |
| github gpg gnupg "not certified with a trusted signature" | `gh search code` on `gpg/gnupg` pointed at the current msgid in `po/*.po` and then at `pkclist.c`. |

Pages fetched directly, without a search, after the first hits named them:
GnuPG configuration and trust-values manual pages, RFC 9580 `.txt` for §5.10,
Sequoia README, in-toto README, slsa-verifier README, policy-controller README,
Witness README, SignServer CE README, GPGTools site, Proton help, Entra and
Authenticator Learn articles, SSL.com eSigner, SignPath homepage.

Misses:

- https://www.digicert.com/software-trust-manager — bot wall.
- https://support.mozilla.org/en-US/kb/openpgp-thunderbird-howto-and-faq — client challenge.
- https://helpx.adobe.com/photoshop/using/content-credentials.html — HTTP 403.
- https://gpgtools.org/store — same marketing shell as the homepage; no price.
- Sequoia `sq` README raw URL returned a stub of 99 bytes and was not used.
- Cosign PKCS#11 page linked from the docs nav was not opened.
