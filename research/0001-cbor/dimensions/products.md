---
dimension: products
researched: 2026-09-22
confidence: medium
---

# CBOR in shipping products and platforms

Scope: commercial/consortium products and platforms where CBOR (RFC 8949 / STD 94), or
CBOR-based COSE (RFC 9052/9053), is actually part of the wire format or data model.
Every row below is checked against a primary or near-primary source. Where a claim is
plausible but I could not verify it against a primary source, it is marked
"claimed-unverified" rather than asserted as fact.

## Summary table

| Product / platform | Vendor / consortium | CBOR role | Citation |
|---|---|---|---|
| ISO/IEC 18013-5 mdoc / mDL | ISO/IEC JTC1 | Direct — mdoc data structures (DeviceRequest, DeviceResponse, MobileSecurityObject) are CBOR, defined via CDDL; signed via COSE (MSO) | [ISO 18013-5](https://www.iso.org/standard/69084.html), [MATTR explainer](https://learn.mattr.global/docs/concepts/iso-mdoc-standards) |
| EUDI Wallet (EU Digital Identity Wallet) / ARF | European Commission + eu-digital-identity-wallet consortium | Direct, via ISO 18013-5 — proximity ("PID"/mDL) presentation flow required to use CBOR-encoded mdoc; online flow can instead use SD-JWT VC (not CBOR) | [ARF docs](https://eu-digital-identity-wallet.github.io/eudi-doc-architecture-and-reference-framework/1.3.0/arf/) |
| Apple Wallet IDs (driver's licenses / state IDs) | Apple | Direct — built on the mdoc/ISO 18013-5 format (CBOR + COSE) | [Apple: Verify with Wallet](https://developer.apple.com/wallet/get-started-with-verify-with-wallet/), [MATTR explainer](https://learn.mattr.global/docs/concepts/iso-mdoc-standards) |
| Google Wallet digital IDs / Android Identity Credential | Google | Direct — CBOR-encoded DeviceRequest/DeviceResponse/MSO per ISO 18013-5; Google ships Multipaz (OpenWallet Foundation) as the reference CBOR/mdoc implementation | [Google Wallet dev docs](https://developers.google.com/wallet/identity/verify/accepting-ids-from-wallet-offline) |
| US state mDL rollouts (CA, and 13+ states in Apple Wallet as of Aug 2025; more via Google Wallet/Samsung) | State DMVs + Apple/Google | Direct, via ISO 18013-5 mdoc | [California mDL launch](https://www.gov.ca.gov/2024/09/19/californians-can-now-store-drivers-licenses-state-ids-in-apple-wallet/), [MacRumors state tracker](https://www.macrumors.com/2025/08/20/iphone-drivers-licenses-10-states/) |
| FIDO2 / CTAP2 (WebAuthn authenticator protocol) | FIDO Alliance | Direct — CTAP2 command parameters and responses are CBOR maps (major type 5); CTAP 2.3 is a Proposed Standard as of Feb 2026 | [FIDO CTAP2 spec](https://fidoalliance.org/specs/fido-v2.0-id-20180227/fido-client-to-authenticator-protocol-v2.0-id-20180227.html), [Yubico CTAP2 developer docs](https://developers.yubico.com/CTAP/) |
| YubiKey (5-series, Bio, Security Key) | Yubico | Direct — implements CTAP2's CBOR commands (MakeCredential, GetAssertion, GetInfo, ClientPin) | [Yubico FIDO2 CBOR docs](https://developers.yubico.com/yubikit-android/JavaDoc/fido/2.8.2/com/yubico/yubikit/fido/Cbor.html) |
| WebAuthn attestationObject (any platform authenticator: Windows Hello, Touch ID/Face ID via platform authenticator, Chrome/Android) | W3C / browser & OS vendors | Direct — `attestationObject` returned to the browser is CBOR-encoded (fmt, authData, attStmt) | [MDN: attestationObject](https://developer.mozilla.org/en-US/docs/Web/API/AuthenticatorAttestationResponse/attestationObject) |
| Passkeys (Apple/Google/Microsoft platforms) | Apple, Google, Microsoft | Direct, indirectly — passkeys are FIDO2/WebAuthn credentials; the CTAP2/attestationObject CBOR encoding applies when a security key or platform authenticator is used as the CTAP layer; cloud sync itself (iCloud Keychain, Google Password Manager) is a proprietary sync protocol, not documented as CBOR | [Corbado: WebAuthn vs CTAP vs FIDO2](https://www.corbado.com/blog/webauthn-vs-ctap-vs-fido2) |
| Matter (smart home) | Connectivity Standards Alliance (CSA) | **Not CBOR** — Matter's data/interaction model uses its own Tag-Length-Value (TLV) binary encoding, defined in the Matter Core Specification. It is conceptually similar to CBOR (compact, self-describing, binary) but is a distinct, CSA-defined format | [Matter 1.4 Core Spec (CSA)](https://csa-iot.org/wp-content/uploads/2024/11/24-27349-006_Matter-1.4-Core-Specification.pdf) — TLV sections; see Corrections below |
| OCF (Open Connectivity Foundation) / IoTivity, IoTivity-Lite | OCF / Samsung, Intel (TinyCBOR) | Direct — OCF resource payloads are CBOR by default (`application/cbor`), with JSON/XML as alternate content types; IoTivity-Lite uses Intel's TinyCBOR library | [cbor.io implementations](https://cbor.io/impls.html), [IoTivity-lite (DeepWiki)](https://deepwiki.com/iotivity/iotivity-lite) |
| OMA LwM2M (device management) | Open Mobile Alliance / OMA SpecWorks | Direct, optional — SenML-CBOR and a dedicated LwM2M CBOR content format (`application/vnd.oma.lwm2m+cbor`) are registered content formats alongside SenML-JSON and TLV | [IANA media type registration](https://www.iana.org/assignments/media-types/application/vnd.oma.lwm2m+cbor), [OMA LwM2M 1.2 spec](https://www.openmobilealliance.org/release/lightweightm2m/V1_2_2-20240613-A/HTML-Version/OMA-TS-LightweightM2M_Core-V1_2_2-20240613-A.html) |
| CoAP deployments (general) | IETF (RFC 7252) + implementers (Californium, libcoap, Eclipse, ARM Mbed) | Direct, as a payload option — CoAP itself is transport/messaging; CBOR is one of several registered content-formats carried over it, and OSCORE (RFC 8613, CoAP object security) uses COSE/CBOR directly | [RFC 7252](https://www.rfc-editor.org/rfc/rfc7252.html), [RFC 8613 OSCORE](https://datatracker.ietf.org/doc/html/rfc8613) |
| CORECONF (CoAP Management Interface) | IETF core WG | Direct — CORECONF = CoAP transport + YANG-CBOR (RFC 9254) as the payload encoding, positioned as the constrained-device analogue of NETCONF/RESTCONF | [RFC 9254](https://www.rfc-editor.org/rfc/rfc9254.html), [draft-ietf-core-comi](https://datatracker.ietf.org/doc/draft-ietf-core-comi/) |
| Thread (mesh network layer) | Thread Group / CSA | **Not CBOR** — Thread's Mesh Link Establishment and Operational Dataset use their own TLV encoding (Thread 1.1.1 spec), unrelated to CBOR | [OpenThread Operational Dataset](https://openthread.io/reference/group/api-operational-dataset) |
| UPTANE | Uptane Alliance / IETF-adjacent, used by automakers | **Not CBOR by default** — the Uptane Standard is built on TUF and its reference metadata format is canonical JSON; the Standard is described as wire-format-agnostic, and academic work has proposed a CBOR profile for interoperability, but this is not the default shipped format | [Uptane Standard 2.1.0](https://uptane.org/docs/2.1.0/standard/uptane-standard), [dual-layer CBOR proposal (NYU)](https://ssl.engineering.nyu.edu/papers/moore_pouf_2020.pdf) |
| AUTOSAR | AUTOSAR partnership (OEMs/suppliers) | **No confirmed CBOR use found** — AUTOSAR's own serialization work (e.g., SOME/IP, ARXML) does not reference CBOR in primary docs found; treat any "AUTOSAR uses CBOR" claim as unverified | [AUTOSAR SOME/IP example](https://some-ip.com/papers/cache/AUTOSAR_TR_SomeIpExample_4.1.1.pdf) |
| EAT (Entity Attestation Token), RFC 9711 | IETF RATS WG | Direct — an EAT is either a CWT (CBOR) or JWT (JSON); CBOR path uses COSE for the security envelope | [RFC 9711](https://www.rfc-editor.org/info/rfc9711/) |
| Arm PSA Attestation Token | Arm | Direct — CBOR/COSE encoded (COSE_Sign1 or COSE_Mac0), a profile of EAT; standardized as RFC 9783 | [RFC 9783](https://datatracker.ietf.org/doc/rfc9783/) |
| Arm CCA (Confidential Compute Architecture) attestation token | Arm | Direct — CCA token = platform token + realm token, CBOR/COSE encoded, an Arm profile of EAT | [Arm learning path: CCA + Veraison](https://learn.arm.com/learning-paths/servers-and-cloud-computing/cca-veraison/attestation-token/) |
| Veraison (attestation verification framework) | Linux Foundation / Arm-led open source project | Direct — verifies CBOR/COSE-encoded evidence (PSA, CCA) against CoRIM/CoMID (also CBOR/CDDL, per draft-ietf-rats-corim) | [Veraison GitHub](https://github.com/veraison), [draft-ietf-rats-corim](https://datatracker.ietf.org/doc/draft-ietf-rats-corim/) |
| AWS Nitro Enclaves attestation documents | Amazon Web Services | Direct — attestation document is CBOR-encoded, COSE_Sign1-signed (CBOR tag 18, ES384) | [AWS nsm-api attestation_process.md](https://github.com/aws/aws-nitro-enclaves-nsm-api/blob/main/docs/attestation_process.md) |
| Intel TDX quotes / AMD SEV-SNP attestation reports | Intel, AMD | **Not CBOR** — both are fixed proprietary binary structures (TD Quote / SEV-SNP attestation report), not CBOR-encoded | [Intel TDX DCAP docs](https://download.01.org/intel-sgx/latest/dcap-latest/linux/docs/Intel_TDX_DCAP_Quoting_Library_API.pdf) |
| Android hardware key attestation | Google | **Not CBOR** for the core attestation extension — it is an X.509 certificate with an ASN.1/DER attestation extension (OID 1.3.6.1.4.1.11129.2.1.17). CBOR appears only in the separate "provisioning info" certificate extension (OID …2.1.30) | [Android key attestation docs](https://developer.android.com/privacy-and-security/security-key-attestation) |
| TCG Open DICE / DICE certificates | Trusted Computing Group, Google (Open Profile for DICE) | Direct, as an alternative to X.509 — Open DICE allows UDS/CDI certificates encoded as CBOR Web Tokens (CWT, COSE_Sign1), and hybrid chains mixing X.509 and CWT certs | [Open Profile for DICE spec](https://pigweed.googlesource.com/open-dice/+/HEAD/docs/specification.md), [Veraison DICE library](https://github.com/veraison/dice) |
| C2PA (Content Credentials) | Coalition for Content Provenance and Authenticity (Adobe, Microsoft, BBC, Google, etc.) | Direct — claims and most assertions in a C2PA manifest are CBOR (deterministic CBOR per RFC 8949 §4.2.1); the manifest is embedded via JUMBF, which also allows JSON/XML/UUID box types | [C2PA Technical Spec 2.2](https://spec.c2pa.org/specifications/specifications/2.2/specs/_attachments/C2PA_Specification.pdf) |
| JPEG Trust (ISO/IEC 21617) | JPEG Committee (ISO/IEC) | Aligned with / compatible with C2PA's JUMBF+CBOR manifest approach, but I could not confirm JPEG Trust's own normative encoding choice from a primary ISO source in this pass — treat as claimed-unverified pending direct spec review | [JUMBF / C2PA background](https://en.wikipedia.org/wiki/JUMBF) |
| SCITT (Supply Chain Integrity, Transparency and Trust) | IETF SCITT WG | Direct — Signed Statements and Receipts are COSE_Sign1 CBOR data items; countersigned Merkle-inclusion proofs use COSE header label 394 | [draft-ietf-scitt-architecture](https://datatracker.ietf.org/doc/draft-ietf-scitt-architecture/), [draft-ietf-scitt-scrapi](https://datatracker.ietf.org/doc/draft-ietf-scitt-scrapi/) |
| Microsoft Signing Transparency (Azure) | Microsoft | Direct, shipping — production Azure service builds (Azure Attestation, Managed HSM, Confidential Ledger, MST itself) are logged to a SCITT-standard-compliant ledger using COSE/CBOR signed statements and receipts; built on `scitt-ccf-ledger` (CCF) | [Microsoft Signing Transparency announcement](https://techcommunity.microsoft.com/blog/microsoft-security-blog/microsoft-leads-a-new-era-of-software-supply-chain-transparency/4528369), [scitt-ccf-ledger](https://github.com/microsoft/scitt-ccf-ledger) |
| in-toto attestations / DSSE (used by Sigstore, cosign, SLSA tooling) | in-toto community, OpenSSF | **Not CBOR** — in-toto Statements are JSON; DSSE envelope's mandated `payloadType` for in-toto is `application/vnd.in-toto+json`. Other payload types (including a CBOR one) are technically permitted by DSSE but are not what in-toto/cosign ship by default | [in-toto attestation bundle spec](https://github.com/in-toto/attestation/blob/main/spec/v1/bundle.md), [sigstore docs](https://docs.sigstore.dev/cosign/verifying/attestation/) |
| CoSWID (Concise SWID tags) / SBOM tooling | IETF SACM WG, NIST swid-tools | Direct — CoSWID is explicitly the CBOR-encoded counterpart to XML SWID tags (ISO/IEC 19770-2), aimed at constrained IoT/SBOM use; NIST's swid-tools/swid-builder generate both | [draft-ietf-sacm-coswid](https://datatracker.ietf.org/doc/html/draft-ietf-sacm-coswid-22), [NIST swid-tools](https://github.com/usnistgov/swid-tools) |
| Cardano | Cardano / IOG (Input Output Global), Emurgo | Direct — the ledger's on-chain transaction and block serialization is CBOR, formally specified per-era via CDDL | [Cardano developer docs: Transactions](https://developers.cardano.org/docs/learn/core-concepts/transactions/), [PyCardano serialization guide](https://pycardano.readthedocs.io/en/latest/guides/serialization.html) |
| IOTA | IOTA Foundation | **Unconfirmed / likely not CBOR for the core ledger** — IOTA's UTXO/Stardust output serialization uses a custom "packable" byte-packing scheme (its own binary layout), not CBOR, per its SDK docs. A CBOR claim appears in academic proposals for IOTA-based verifiable credentials (IoT identity), not in the core protocol. Treat "IOTA uses CBOR" as claimed-unverified/mixed | [IOTA Stardust docs](https://docs.iota.org/developer/stardust/addresses), [SSI4IoT paper (proposal, not shipped protocol)](https://arxiv.org/pdf/2405.02476) |

## Sector notes

### Identity and credentials
The mdoc/mDL ecosystem (ISO/IEC 18013-5, EUDI ARF, Apple Wallet, Google Wallet, US state
rollouts) is the single strongest, most concretely verified use of CBOR in this whole
survey: CBOR is normatively required for the CDDL-defined mdoc data structures
(`DeviceRequest`, `DeviceResponse`, `MobileSecurityObject`), and COSE is used for signing.
Note the EUDI Wallet's *online* (remote) presentation flow can instead use SD-JWT VC —
CBOR/mdoc there applies specifically to the ISO 18013-5-aligned proximity/PID flows and
mdoc-format credentials, not to every EUDI Wallet credential type.

### Authentication
FIDO2/CTAP2 is a clean, unambiguous, verified CBOR user: the FIDO Alliance's CTAP2 spec
mandates CBOR maps for all commands and responses, and this is what YubiKey and other
CTAP2 authenticators implement. WebAuthn's `attestationObject`, returned to the browser
during registration, is also CBOR. "Passkeys" as a marketing term span multiple transport
paths; the CBOR claim holds specifically at the CTAP2/attestationObject layer, not
necessarily for proprietary cloud-sync transport of the credential itself.

### IoT / smart home
This is the sector with the sharpest CBOR-vs-not split, and the most common place to get
it wrong:
- **OCF/IoTivity: yes, CBOR** (direct, well documented, TinyCBOR reference implementation).
- **LwM2M: yes, optional CBOR** (SenML-CBOR and a dedicated LwM2M CBOR content-format,
  alongside JSON/TLV alternatives).
- **CoAP: CBOR is a payload option, not inherent** — CoAP is a REQUEST/RESPONSE
  transport; CBOR is one of many registered Content-Formats carried over it. OSCORE
  (CoAP's object-security layer) does use COSE/CBOR directly.
- **CORECONF: yes, CBOR** (it is explicitly CoAP + YANG-CBOR/RFC 9254).
- **Matter: no.** Matter uses its own TLV binary encoding, defined in the CSA's Matter
  Core Specification. This is the single most likely place someone conflates "IoT +
  compact binary + self-describing" with CBOR. See Corrections.
- **Thread: no.** Thread's TLV (Mesh Link Establishment, Operational Dataset) is also a
  distinct, non-CBOR TLV scheme.

### Automotive
No primary-source evidence found that AUTOSAR uses CBOR anywhere in its standard stack
(SOME/IP, ARXML/XML are its serialization mechanisms). UPTANE, the automotive OTA-update
security framework built on TUF, defaults to JSON/canonical-JSON metadata; the Standard is
wire-format-agnostic and a CBOR profile has been proposed academically for
interoperability/compactness, but this is not confirmed as a shipped default in production
OEM Uptane deployments as of this research pass. Both should be treated as
**not confirmed CBOR** rather than as CBOR users.

### Attestation and confidential computing
Strong, verified CBOR cluster: IETF RATS's EAT (RFC 9711), Arm's PSA Attestation Token
(RFC 9783) and CCA token, the Veraison verifier project, CoRIM/CoMID, and AWS Nitro
Enclaves' attestation documents are all CBOR/COSE. TCG Open DICE optionally uses CBOR Web
Tokens for its certificate chain (alongside X.509). By contrast, **Intel TDX and AMD
SEV-SNP use their own fixed binary attestation-report structures, not CBOR** — a
plausible-sounding but incorrect claim would be "Intel/AMD confidential computing
attestation is CBOR-based like Arm's." **Android's core hardware key-attestation
extension is ASN.1/DER inside an X.509 certificate, not CBOR** — CBOR shows up only in a
separate, secondary "provisioning info" certificate extension. This is a second common
error worth flagging explicitly.

### Content provenance
C2PA is a genuine, verified, and fairly deep CBOR user: claims and the majority of
assertions inside a C2PA manifest are CBOR, deterministically encoded per RFC 8949 §4.2.1,
all packaged inside JUMBF boxes (which can alternatively hold JSON/XML/UUID content —
so not every byte in a C2PA manifest is CBOR, but the claim and most assertions are).
JPEG Trust (ISO/IEC 21617) is described as C2PA-compatible/aligned, but this pass did not
verify JPEG Trust's own normative serialization choice against a primary ISO text — flagged
as claimed-unverified.

### Cloud/infra, supply chain, SBOM
SCITT (an IETF-standardizing effort, not yet an RFC as of this research date) is CBOR/COSE
by design, and it has a real shipping product behind it: **Microsoft Signing Transparency**,
now used to log production builds of several Azure confidential-computing services. This is
one of the better "commercial product actually uses CBOR/COSE today" anchors in the
cloud/infra sector. By contrast, **in-toto attestations and the DSSE envelope — the
format underlying Sigstore/cosign and most SLSA tooling — are JSON, not CBOR**; DSSE's
envelope is format-agnostic in principle, but the shipped, standard in-toto payload type is
explicitly `application/vnd.in-toto+json`. This is arguably the single most important
correction in the "cloud/infra" part of this survey, since in-toto/DSSE is sometimes lumped
in with COSE/CBOR supply-chain-security tooling. CoSWID is a real, if niche, CBOR product:
NIST ships CBOR-capable tooling (`swid-tools`) alongside XML SWID tooling for SBOM/software
identification.

### Crypto/blockchain
Cardano is a clean, well-documented, verified CBOR user — its ledger rules define every
on-chain object (transactions, blocks) via CDDL-specified CBOR, era by era. IOTA is murkier:
its actual UTXO/Stardust serialization is a custom "packable" byte format per its own SDK
documentation, not CBOR; the CBOR claim for IOTA seems to originate from research proposals
about representing W3C Verifiable Credentials/DID documents for IOTA-based IoT identity
use cases, not from IOTA's core ledger protocol. Treat "IOTA is CBOR-based like Cardano" as
false/unverified pending a primary IOTA protocol spec citation.

### Networking/telemetry
CORECONF (RFC 9254 YANG-CBOR + CoAP) is the clearest "SNMP successor for constrained
devices" candidate that is genuinely CBOR-based, positioned by the IETF core WG as filling
the gap NETCONF/RESTCONF leave for constrained networks.

## Sources

- ISO/IEC 18013-5:2021 (ISO catalog listing), retrieved 2026-09-22: https://www.iso.org/standard/69084.html
- MATTR Learn, "ISO/IEC 18013-5, 18013-7 and 23220 explained," retrieved 2026-09-22: https://learn.mattr.global/docs/concepts/iso-mdoc-standards
- EUDI Wallet Architecture and Reference Framework docs, retrieved 2026-09-22: https://eu-digital-identity-wallet.github.io/eudi-doc-architecture-and-reference-framework/1.3.0/arf/
- Apple Developer, "Get started with the Verify with Wallet API," retrieved 2026-09-22: https://developer.apple.com/wallet/get-started-with-verify-with-wallet/
- Google for Developers, "In-person Acceptance of Digital Credentials (Offline)," retrieved 2026-09-22: https://developers.google.com/wallet/identity/verify/accepting-ids-from-wallet-offline
- California Governor's Office, mDL/Apple Wallet announcement, retrieved 2026-09-22: https://www.gov.ca.gov/2024/09/19/californians-can-now-store-drivers-licenses-state-ids-in-apple-wallet/
- MacRumors, "iPhone Driver's Licenses in Apple Wallet Now Available in 10 U.S. States," retrieved 2026-09-22: https://www.macrumors.com/2025/08/20/iphone-drivers-licenses-10-states/
- FIDO Alliance, CTAP2 specification (2018 ID), retrieved 2026-09-22: https://fidoalliance.org/specs/fido-v2.0-id-20180227/fido-client-to-authenticator-protocol-v2.0-id-20180227.html
- Yubico Developers, CTAP2 developer docs, retrieved 2026-09-22: https://developers.yubico.com/CTAP/
- Yubico YubiKit Android, Cbor class docs, retrieved 2026-09-22: https://developers.yubico.com/yubikit-android/JavaDoc/fido/2.8.2/com/yubico/yubikit/fido/Cbor.html
- MDN, AuthenticatorAttestationResponse.attestationObject, retrieved 2026-09-22: https://developer.mozilla.org/en-US/docs/Web/API/AuthenticatorAttestationResponse/attestationObject
- Corbado, "WebAuthn vs. CTAP vs. FIDO2," retrieved 2026-09-22: https://www.corbado.com/blog/webauthn-vs-ctap-vs-fido2
- CSA, Matter 1.4 Core Specification PDF, retrieved 2026-09-22: https://csa-iot.org/wp-content/uploads/2024/11/24-27349-006_Matter-1.4-Core-Specification.pdf
- cbor.io, list of implementations (incl. TinyCBOR/IoTivity), retrieved 2026-09-22: https://cbor.io/impls.html
- DeepWiki, iotivity/iotivity-lite overview, retrieved 2026-09-22: https://deepwiki.com/iotivity/iotivity-lite
- IANA media types registry, application/vnd.oma.lwm2m+cbor, retrieved 2026-09-22: https://www.iana.org/assignments/media-types/application/vnd.oma.lwm2m+cbor
- OMA SpecWorks, LwM2M 1.2.2 Core Technical Specification, retrieved 2026-09-22: https://www.openmobilealliance.org/release/lightweightm2m/V1_2_2-20240613-A/HTML-Version/OMA-TS-LightweightM2M_Core-V1_2_2-20240613-A.html
- IETF, RFC 7252 (CoAP), retrieved 2026-09-22: https://www.rfc-editor.org/rfc/rfc7252.html
- IETF, RFC 8613 (OSCORE), retrieved 2026-09-22: https://datatracker.ietf.org/doc/html/rfc8613
- IETF, RFC 9254 (YANG-CBOR), retrieved 2026-09-22: https://www.rfc-editor.org/rfc/rfc9254.html
- IETF, draft-ietf-core-comi (CORECONF), retrieved 2026-09-22: https://datatracker.ietf.org/doc/draft-ietf-core-comi/
- OpenThread, Operational Dataset API reference, retrieved 2026-09-22: https://openthread.io/reference/group/api-operational-dataset
- Uptane Alliance, Uptane Standard for Design and Implementation 2.1.0, retrieved 2026-09-22: https://uptane.org/docs/2.1.0/standard/uptane-standard
- NYU (Moore et al.), "Using a Dual-Layer Specification to Offer Selective Interoperability for Uptane," retrieved 2026-09-22: https://ssl.engineering.nyu.edu/papers/moore_pouf_2020.pdf
- AUTOSAR, SOME/IP serialization example TR, retrieved 2026-09-22: https://some-ip.com/papers/cache/AUTOSAR_TR_SomeIpExample_4.1.1.pdf
- IETF, RFC 9711 (EAT), retrieved 2026-09-22: https://www.rfc-editor.org/info/rfc9711/
- IETF, RFC 9783 (Arm PSA Attestation Token), retrieved 2026-09-22: https://datatracker.ietf.org/doc/rfc9783/
- Arm Learning Paths, "Get Started with CCA Attestation and Veraison," retrieved 2026-09-22: https://learn.arm.com/learning-paths/servers-and-cloud-computing/cca-veraison/attestation-token/
- Veraison project, GitHub org, retrieved 2026-09-22: https://github.com/veraison
- IETF, draft-ietf-rats-corim (CoRIM), retrieved 2026-09-22: https://datatracker.ietf.org/doc/draft-ietf-rats-corim/
- AWS, aws-nitro-enclaves-nsm-api attestation_process.md, retrieved 2026-09-22: https://github.com/aws/aws-nitro-enclaves-nsm-api/blob/main/docs/attestation_process.md
- Intel, TDX DCAP Quoting Library API PDF, retrieved 2026-09-22: https://download.01.org/intel-sgx/latest/dcap-latest/linux/docs/Intel_TDX_DCAP_Quoting_Library_API.pdf
- Android Developers, "Verify hardware-backed key pairs with key attestation," retrieved 2026-09-22: https://developer.android.com/privacy-and-security/security-key-attestation
- Google, Open Profile for DICE specification, retrieved 2026-09-22: https://pigweed.googlesource.com/open-dice/+/HEAD/docs/specification.md
- Veraison, DICE evidence manipulation library, retrieved 2026-09-22: https://github.com/veraison/dice
- C2PA, Content Credentials Technical Specification 2.2 PDF, retrieved 2026-09-22: https://spec.c2pa.org/specifications/specifications/2.2/specs/_attachments/C2PA_Specification.pdf
- Wikipedia, JUMBF, retrieved 2026-09-22: https://en.wikipedia.org/wiki/JUMBF
- IETF, draft-ietf-scitt-architecture, retrieved 2026-09-22: https://datatracker.ietf.org/doc/draft-ietf-scitt-architecture/
- IETF, draft-ietf-scitt-scrapi, retrieved 2026-09-22: https://datatracker.ietf.org/doc/draft-ietf-scitt-scrapi/
- Microsoft Tech Community, "Microsoft Leads a New Era of Software Supply Chain Transparency," retrieved 2026-09-22: https://techcommunity.microsoft.com/blog/microsoft-security-blog/microsoft-leads-a-new-era-of-software-supply-chain-transparency/4528369
- Microsoft, scitt-ccf-ledger GitHub repo, retrieved 2026-09-22: https://github.com/microsoft/scitt-ccf-ledger
- in-toto, attestation bundle spec (v1), retrieved 2026-09-22: https://github.com/in-toto/attestation/blob/main/spec/v1/bundle.md
- Sigstore docs, "In-Toto Attestations," retrieved 2026-09-22: https://docs.sigstore.dev/cosign/verifying/attestation/
- IETF, draft-ietf-sacm-coswid-22, retrieved 2026-09-22: https://datatracker.ietf.org/doc/html/draft-ietf-sacm-coswid-22
- NIST, swid-tools GitHub repo, retrieved 2026-09-22: https://github.com/usnistgov/swid-tools
- Cardano Developer Portal, "Transactions," retrieved 2026-09-22: https://developers.cardano.org/docs/learn/core-concepts/transactions/
- PyCardano docs, serialization guide, retrieved 2026-09-22: https://pycardano.readthedocs.io/en/latest/guides/serialization.html
- IOTA Documentation, Stardust "Addresses and Keys," retrieved 2026-09-22: https://docs.iota.org/developer/stardust/addresses
- arXiv, "SSI4IoT: Unlocking the Potential of IoT Tailored Self-Sovereign Identity" (proposal paper, not a shipped IOTA protocol feature), retrieved 2026-09-22: https://arxiv.org/pdf/2405.02476

## Corrections

Places where CBOR is commonly but wrongly said to be used (or where the CBOR claim needs
a precise qualifier):

1. **Matter (smart home, CSA) is often assumed to use CBOR** because it is a compact,
   binary, self-describing IoT data format from roughly the same design era and problem
   space as CBOR/CoAP-based IoT stacks (OCF, LwM2M). It does not: Matter defines and uses
   its own TLV encoding in the CSA Matter Core Specification. Do not conflate "IoT +
   compact binary encoding" with "therefore CBOR."

2. **Intel TDX and AMD SEV-SNP attestation are sometimes assumed to follow the same
   CBOR/COSE pattern as Arm CCA/PSA attestation** (since all three are discussed together
   under "confidential computing attestation"). They don't — TD Quotes and SEV-SNP
   attestation reports are vendor-defined fixed binary structures, not CBOR. AWS Nitro
   Enclaves is the outlier among cloud CC platforms in actually using CBOR/COSE.

3. **Android key attestation is sometimes described as "CBOR-based" by analogy with
   ISO 18013-5 mdoc (which Android also implements for digital IDs).** The core hardware
   key-attestation certificate extension is ASN.1/DER in an X.509 certificate, not CBOR.
   CBOR only appears in the separate remote-provisioning-info extension. These are two
   different Android subsystems (Keystore attestation vs. Identity Credential/mdoc) and
   should not be merged.

4. **in-toto attestations / DSSE (Sigstore, cosign, SLSA provenance) are sometimes lumped
   in with COSE/CBOR-based supply-chain security tooling** because they sit in the same
   "software supply chain trust" conversation as SCITT and CoSWID. In-toto's actual
   payload type is JSON (`application/vnd.in-toto+json`); DSSE is format-agnostic but the
   shipped ecosystem is JSON, not CBOR. SCITT (and Microsoft's shipping SCITT-based
   Signing Transparency service) is the CBOR/COSE-based analogue in the same space —
   these are two different, independently-evolving standards, not the same thing.

5. **IOTA is sometimes stated as "CBOR-based like Cardano"** by loose analogy (both are
   ledgers with compact binary on-chain formats, both have CBOR mentioned somewhere in
   their surrounding literature). Cardano's CBOR usage is normatively specified and easy
   to verify (CDDL specs per era). IOTA's actual UTXO/output byte-packing is a bespoke
   "packable" scheme per its own SDK docs; the CBOR association there traces to academic
   proposals for IOTA-based verifiable-credential/DID formats, not the core ledger
   protocol. Flag any blanket "IOTA = CBOR" claim as unverified.

6. **AUTOSAR and UPTANE are sometimes assumed to use CBOR "because automotive is
   constrained/embedded, like IoT."** No primary AUTOSAR documentation found confirms
   CBOR use (its serialization mechanisms are SOME/IP and ARXML/XML). UPTANE's Standard is
   wire-format-agnostic and its reference/example implementations are JSON-based (via TUF);
   a CBOR profile exists only as an academic interoperability proposal, not a confirmed
   shipped default.

7. **JPEG Trust (ISO/IEC 21617) is sometimes assumed to inherit C2PA's CBOR-in-JUMBF
   approach wholesale.** JPEG Trust is described as aligned/compatible with C2PA, but this
   research pass could not confirm JPEG Trust's own normative serialization choice against
   a primary ISO text — treat as unverified rather than assuming CBOR by inheritance.
