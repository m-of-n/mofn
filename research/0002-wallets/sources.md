---
schema: "library-doc/v1"
id: R-0002-sources
title: "Sources consulted — wallet market survey"
type: evidence
status: draft
version: "0.2.0"
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

## Private-key protection

All of these were fetched on 2026-10-02.

| Source | URL | What it settled |
|---|---|---|
| RFC 9580, S2K and secret keys | https://www.rfc-editor.org/rfc/rfc9580.txt | §3.7 S2K types including Argon2. §3.7.2 generation rules. §3.7.2.1 usage octets 0, 253, 254, 255. §5.5.3 secret-key packet, HKDF, AEAD tag. §13.7 AEAD recommended for v6 secret keys; CFB corruption note. |
| GnuPG invoking gpg-agent | https://www.gnupg.org/documentation/manuals/gnupg/Invoking-GPG_002dAGENT.html | Daemon manages secret keys. Pinentry is a separate program. |
| GnuPG agent options | https://www.gnupg.org/documentation/manuals/gnupg/Agent-Options.html | default-cache-ttl 600s, max-cache-ttl 7200s. SSH variants 1800 and 7200. ignore-cache-for-signing. |
| GnuPG agent protocol | https://www.gnupg.org/documentation/manuals/gnupg/Agent-Protocol.html | Command index: PKSIGN, GET_PASSPHRASE, EXPORT. |
| GnuPG PKSIGN | https://www.gnupg.org/documentation/manuals/gnupg/Agent-PKSIGN.html | Client sends a hash; agent asks for the passphrase; returns a signature, not the key. use-cache-for-signing. |
| GnuPG GET_PASSPHRASE | https://www.gnupg.org/documentation/manuals/gnupg/Agent-GET_005fPASSPHRASE.html | Can return the passphrase to the client. |
| GnuPG agent EXPORT | https://www.gnupg.org/documentation/manuals/gnupg/Agent-EXPORT.html | "Not implemented." |
| OpenSSH PROTOCOL.key | https://raw.githubusercontent.com/openssh/openssh-portable/master/PROTOCOL.key | openssh-key-v1. ciphername, kdfname bcrypt (salt, rounds), or none/none. |
| ssh-keygen(1) | https://man.openbsd.org/ssh-keygen | Passphrase prompt. OpenSSH format preferred for keys at rest. bcrypt_pbkdf rounds, default 32. No recovery of a lost passphrase. |
| ssh(1) | https://man.openbsd.org/ssh | Private key not accessible by others, or ssh ignores it. Passphrase encrypts the sensitive part with AES-128. ~/.ssh recommended owner-only. |
| ssh-agent(1) | https://man.openbsd.org/ssh-agent | Holds private keys. Forwarding does not send the key. Socket abused by root or the same user. Default lifetime forever. |
| ssh-add(1) | https://man.openbsd.org/ssh-add | -c confirm via ssh-askpass. -t lifetime. Passphrase from the tty. |
| signify(1) | https://man.openbsd.org/signify | -G prompts for a passphrase unless -n. Secret key is a file. KDF not named. |
| minisign(1) | https://raw.githubusercontent.com/jedisct1/minisign/master/share/man/man1/minisign.1 | Secret key encrypted to a file. -W skips the password. -C changes it. KDF not named. |
| age(1) | https://raw.githubusercontent.com/FiloSottile/age/main/doc/age.1 | Identity files. Passphrase-encrypted file as an identity. SSH keys via ssh-agent or hardware tokens are not supported. |
| age v1 spec, scrypt | https://raw.githubusercontent.com/C2SP/C2SP/main/age.md | scrypt recipient: salt, work factor, ChaCha20-Poly1305, fixed nonce. Must be the only stanza. |
| age README | https://raw.githubusercontent.com/FiloSottile/age/main/README.md | Names age-plugin-yubikey as an extension. Behavior of the file tool is from age(1), not from this README. |
| libsodium secure memory | https://doc.libsodium.org/memory_management | sodium_memzero, sodium_mlock, sodium_munlock. |
| Python secrets | https://docs.python.org/3/library/secrets.html | Generates secrets. Does not document wiping memory. |
| Apple Secure Enclave attribute | https://developer.apple.com/documentation/security/ksecattrtokenidsecureenclave.md | kSecAttrTokenIDSecureEnclave. Points at the protecting-keys article. |
| Protecting keys with the Secure Enclave | https://developer.apple.com/documentation/security/protecting-keys-with-the-secure-enclave.md | Enclave creates the key. Cannot import a preexisting key. P-256 only. Keychain-only keys are copied into memory to be used. |
| Storing keys in the keychain | https://developer.apple.com/documentation/security/storing-keys-in-the-keychain.md | Keychain stores small secrets, including keys, via the keychain API. |
| Apple keychain data protection | https://support.apple.com/guide/security/keychain-data-protection-secb0694df1a/web | SQLite, securityd, AES-256-GCM, access groups, this-device-only, ACL in the Secure Enclave. Published date on the page: 2024-12-19. Fetched 2026-10-02. |
| CryptProtectData | https://learn.microsoft.com/en-us/windows/win32/api/dpapi/nf-dpapi-cryptprotectdata | Same logon, usually same computer. CRYPTPROTECT_LOCAL_MACHINE binds to the computer. |
| CNG key storage | https://learn.microsoft.com/en-us/windows/win32/seccng/key-storage-and-retrieval | Isolation in the LSA process. Private keys also stored as files under %APPDATA%\Microsoft\Crypto\Keys and other profile directories. |
| Linux keyrings(7) | https://man7.org/linux/man-pages/man7/keyrings.7.html | In-kernel key store. Permissions include a read bit for possessor, user, group, and other. |
| Secret Service | https://specifications.freedesktop.org/secret-service-spec/latest/description.html | Secrets in a per-login service. GetSecret returns the secret. Locked collections can prompt. |
| OpenPGP card howto, generating keys | https://www.gnupg.org/howtos/card-howto/en/ch03s03.html | generate on the card. Optional off-card backup of the encryption key. forcesig. PIN and Admin PIN. |
| OpenPGP card howto, card status | https://www.gnupg.org/howtos/card-howto/en/ch03.html | Sample card-status line "Signature PIN ....: forced". |
| YubiKey OpenPGP 5.2.3 notes | https://developers.yubico.com/PGP/YubiKey_5.2.3_Enhancements_to_OpenPGP_3.4.html | Touch-to-verify. Touch cache up to 15 seconds. Export not discussed. |
| PKCS #11 base v3.0 | https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/os/pkcs11-base-v3.0-os.html | CKA_EXTRACTABLE CK_FALSE. CKA_ALWAYS_AUTHENTICATE forces a PIN per use. |
| proc_pid_cmdline(5) | https://man7.org/linux/man-pages/man5/proc_pid_cmdline.5.html | /proc/pid/cmdline holds the process command line. |
| DigiCert KeyLocker benefits | https://docs.digicert.com/en/digicert-keylocker/overview/benefits.html | Generates and stores the private key in an HSM. MFA to sign. |
| SignPath managing certificates | https://docs.signpath.io/managing-certificates | CSR path creates the private key on SignPath's HSM. |
| SignPath crypto providers | https://docs.signpath.io/crypto-providers | Local tools sign through KSP, PKCS #11, or CryptoTokenKit. Private key remains on the HSM. |
| Apple notarization | https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution.md | Notary service scans Developer ID-signed software and returns a ticket. Does not say where the private key is. |
| AWS KMS concepts | https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html | HSM backing key is designed never to leave the HSM in plaintext. |

## Project documents read, not external evidence

| Document | Where |
|---|---|
| APP-0001 | `project/APP-0001-application-design.md` on `origin/main` |
| PLAN-0002 §§1–2 | `project/PLAN-0002-product-spec.md` on `origin/main` |
| PLAN-0004 | worktree for PR 57, `doc/app-0001-no-kg`, not on `main` |
| research/README.md and R-0001 front matter | tone and folder shape |
