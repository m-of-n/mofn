# Area E — Device and Platform Attestation: Signatures Rooted in Hardware

## 1. The TPM lineage

The Trusted Computing Group's **TPM 1.2 Main Specification** (Level 2, Revision 116, 2011) and the **TPM 2.0 Library Specification** are two different design philosophies wearing the same name. TPM 1.2 hard-codes SHA-1 and RSA and fixes a single key hierarchy; TPM 2.0 is a *library* — algorithm-agile, with three separable hierarchies (platform, storage, endorsement) plus a null hierarchy, and a profile mechanism (e.g. the TCG PC Client Platform TPM Profile) selecting which of the library a given part must implement. TPM 2.0 is standardised as **ISO/IEC 11889-1..4:2015**; its current TCG revision is **Version 184, 20 March 2025**, published in Parts 0–4 (Introduction, Architecture, Structures, Commands, Supporting Routines). Note the versioning change: TCG moved from the `1.xx` scheme (1.16, 1.38, 1.59, 1.62) to a `TPM_SPEC_VERSION`-derived integer, so "184" is the successor to "1.83", not a leap.

The attestation machinery is small and specific. The **Endorsement Key (EK)** is a device-unique key associated with the TPM at manufacture, accompanied by an **EK certificate** issued by the TPM or platform vendor: this is the anchor that says "a genuine part of model M holds this key." The EK is a restricted decryption key and is deliberately *not* a signing key, precisely so it cannot itself be used as a tracking identity. Signing is done by **Attestation Identity Keys (AIK)** — in TPM 2.0 vocabulary, *attestation keys* (AK): restricted signing keys, `fixedTPM`/`fixedParent`, created under the endorsement hierarchy and constrained by the TPM to sign only TPM-generated structures. That restriction is load-bearing: an AK cannot be tricked into signing an arbitrary attacker-chosen blob that later reads as a valid quote.

**PCRs** (Platform Configuration Registers) are append-only accumulators: `PCR_new = H(PCR_old || measurement)`. They cannot be set, only extended (or reset at power-on, or by locality-restricted reset), so software that loads late cannot rewrite the record of what loaded early. The **measured boot chain** — specified for PCs by the *TCG PC Client Platform Firmware Profile* (Revision 1.05, 2020) — has each stage measure the next before transferring control, extending into PCR[0..7] and appending a human-parsable entry to a **TCG event log**. **`TPM2_Quote`** then signs a digest of a selected PCR set together with a caller-supplied nonce, producing the canonical hardware-rooted signature: *"the chip holding this AK observed this boot sequence, and it is answering your challenge now."*

## 2. Direct Anonymous Attestation

The original design had a privacy hole. To be credible, an AIK must be linked back to a certified EK — and the party doing that linking, the **Privacy CA**, sees the EK↔AIK mapping for every pseudonym a device ever uses. It can deanonymise any transaction, and it is a single point of collusion and of failure. Using the EK directly is worse: a globally unique, manufacturer-certified serial number signing every interaction.

**Direct Anonymous Attestation** (Brickell, Camenisch & Chen, ACM CCS 2004, pp. 132–145; IACR ePrint 2004/205) removed the online third party. A TPM *joins* once with an issuer, obtaining a Camenisch–Lysyanskaya-style credential; thereafter it produces zero-knowledge proofs of possession of that credential, so a verifier learns "a certified TPM signed this" and nothing more. The scheme's subtlety is the **basename**: with a null basename, signatures are unlinkable; with a verifier-supplied basename, signatures from the same TPM are linkable *to that verifier only*, which restores rate-limiting and rogue detection without enabling cross-verifier correlation. Extracted keys are handled by rogue-tagging rather than conventional revocation. DAA entered TPM 1.2 in RSA form; TPM 2.0 supports elliptic-curve DAA via `TPM2_Commit` and pairing-based schemes, and the idea propagated into Intel EPID and FIDO's ECDAA.

The historical verdict is worth recording in a survey: **DAA largely lost.** Intel's SGX began with EPID and moved to ECDSA/DCAP, where quotes are signed under an Intel-rooted certificate chain keyed to a specific platform — i.e. back to the Privacy-CA shape. TDX and SEV-SNP make no anonymity claim at all. Operational verifiability, revocation and TCB-recovery beat unlinkability.

## 3. DICE — identity for parts too small for a TPM

**DICE** (Device Identifier Composition Engine) achieves layered identity with no dedicated security chip. A tiny immutable ROM holds a **Unique Device Secret (UDS)**, measures the First Mutable Code, derives a **Compound Device Identifier** `CDI = KDF(UDS, measurement)`, and then makes the UDS unreadable before handing over control. Each layer repeats this, so every layer's key is a deterministic function of the device secret *and* every measurement below it. Change any firmware and the derived identity silently changes — attestation becomes an emergent property of key derivation rather than a signed log. The specification family comprises *Hardware Requirements for a DICE* (Rev. 78, 2018), *DICE Layering Architecture* (v1.0 Rev. 0.19, 23 July 2020), *DICE Attestation Architecture*, *DICE Certificate Profiles*, and *Symmetric Identity Based Device Attestation*; Google's *Open Profile for DICE* is the widely deployed open implementation.

## 4. IETF RATS

**RFC 9334, "Remote ATtestation procedureS (RATS) Architecture"** (Birkholz, Thaler, Richardson, Smith, Pan; Informational; January 2023; DOI 10.17487/RFC9334) supplies the vocabulary the rest of the field now borrows. Roles: the **Attester** produces **Evidence**; the **Verifier** appraises Evidence against **Reference Values** (from a *Reference Value Provider*) and **Endorsements** (from an **Endorser** — "a secure statement that an Endorser vouches for the integrity of an Attester's various capabilities", §4.2), under policy set by a **Verifier Owner**; the output is **Attestation Results**, consumed by a **Relying Party** under its own owner's policy.

Two topologies: in the **Passport Model** (§5.1) the Attester gets Attestation Results from the Verifier and presents them itself, like a passport at a border; in the **Background-Check Model** (§5.2) the Attester hands Evidence to the Relying Party, which forwards it to a Verifier — like an employer running a reference check.

**RFC 9711, "The Entity Attestation Token (EAT)"** (Lundblade, Mandyam, O'Donoghue, Wallace; Proposed Standard; April 2025) gives Evidence and Results a concrete token format: attestation claims carried in a CWT or JWT, with nonce, UEID, boot/debug state, measurements and submodules, profiled per ecosystem.

**CoRIM** — *Concise Reference Integrity Manifest* (draft-ietf-rats-corim-11, 6 July 2026; Birkholz, Fossati, Deshpande, Smith, Pan) — is the still-unfinished other half: a signed CBOR container of tags supplying the Verifier its inputs. **CoMID** (Concise Module Identifier) tags carry *triples*: reference-value triples (intended state), endorsed-value triples (claims not present in Evidence), conditional-endorsement triples, identity and attestation-key triples, and links to **CoSWID** software tags; **CoTL** lists authoritative tag sources.

## 5. Confidential computing attestation

- **Intel SGX**: an enclave is identified by `MRENCLAVE` (its measured contents) and `MRSIGNER` (its signer). `EREPORT` produces a locally MAC-verifiable report; a privileged **Quoting Enclave** converts it into a remotely verifiable **quote**, originally EPID-signed, now ECDSA under the **DCAP** model with platform certification keys chained to Intel's Provisioning Certification Service.
- **Intel TDX**: a TD's `TDREPORT` is MAC'd with a hardware key; the **TD Quoting Enclave** — *itself an SGX enclave* — verifies it with `EVERIFYREPORT2` and re-signs with an Intel-certified attestation key. TDX attestation is therefore parasitic on SGX's infrastructure.
- **AMD SEV-SNP**: the guest requests a report over the **launch measurement** (initial guest memory and vCPU state) plus 64 bytes of guest-supplied report data. It is signed by the **VCEK**, derived from chip-fused secrets *and the current TCB version*, and certified **ARK → ASK → VCEK** from AMD's Key Distribution Service. Firmware downgrade is expressed as a *different key*, not as a flag a verifier might ignore.
- **Arm CCA**: two EAT-profiled tokens (draft-ffm-rats-cca-token) — a **platform token** signed by the CPAK covering monitor and RMM measurements, and a **realm token** signed by the RAK covering the Realm Initial Measurement and Realm Extensible Measurements — cryptographically bound by carrying a hash of the realm key as the platform token's nonce. CCA is the first of the four designed natively to RATS/EAT shapes.

## 6. Mass deployment

**Android Key Attestation** reuses X.509: an attested Keystore key arrives with a certificate chain to a Google attestation root, where the leaf carries a `KeyDescription` extension with `attestationSecurityLevel` (TrustedEnvironment or StrongBox), the hardware- and software-enforced authorisation lists, OS version and patch level, and a root-of-trust structure containing `verifiedBootState`. The assertion is: *this key lives in secure hardware on a device whose boot chain verified.*

**Apple App Attest** (`DCAppAttestService`) generates a Secure Enclave key per app install and returns a CBOR attestation object in WebAuthn's shape (format `apple-appattest`), chained to Apple's App Attest Root CA and binding a hash of the App ID; subsequent requests carry *assertions* signed by that key with a monotonic counter. The assertion is: *a genuine build of this app, on a genuine Apple device, holds this key.*

Both collapse the RATS role separation: the silicon vendor is simultaneously manufacturer, Endorser, root CA, and — via risk signals it does not publish — part of the Verifier.

## 7. Analytical core

### What the hardware root of trust actually adds

Four distinct things, worth separating because they are usually conflated:

1. **Non-exfiltrability.** The private key was generated inside a die and provably cannot be copied out (`fixedTPM`, Secure Enclave, VCEK from fuses). A signature is therefore evidence of *live interaction with one particular physical artefact*, not merely knowledge of a secret. This is the only place in the whole signature literature where a verification succeeds *because of* a property of matter.
2. **A factory-injected anchor.** EK certificates, DICE UDS, AMD's ARK, Google's and Apple's roots. The manufacturer asserts that this key was placed in a part built to a specification.
3. **Unforgeable-from-above measurement.** PCR extend is append-only; DICE destroys the UDS before mutable code runs; SNP's launch measurement is taken by firmware outside the guest; TDX's report is MAC'd by hardware. Later code cannot rewrite the record of earlier code. This is the structural asymmetry that makes measured boot meaningful at all.
4. **Freshness binding.** The nonce in `TPM2_Quote`, EAT, or SNP report data makes the statement present-tense rather than a replayable historical artefact.

### What it still does not prove

- **Not that the code is good.** A quote signs a *hash*. Its meaning comes entirely from reference values supplied out of band (CoRIM/CoMID, a vendor RIM). Without them, a quote is an unforgeable statement about a number.
- **Not runtime integrity.** Measured boot is *load-time*. Code that is exploited but not modified produces identical PCRs. The measurement-to-execution gap is a TOCTOU window the architecture does not close.
- **Not physical security.** This is the sharpest irony: the thing that makes hardware attestation special — its claim about physical reality — is exactly where its residual risk sits. Attestation proves "a key inside a part of model M," not that the part is not decapped, glitched, on a bus interposer, or in an adversary's lab. Discrete-TPM bus sniffing and fault injection against SEV are the canonical demonstrations.
- **Not *which* machine you are talking to.** Absent binding between the attestation key and the transport channel, an unhealthy attester can relay a challenge to a healthy machine and pass it off as its own (the relay or "cuckoo" problem). Attestation and channel establishment must be fused; they often are not.
- **Not the operator, the owner, the jurisdiction, the intent, or anything outside the TEE boundary** — a point cloud confidential-computing deployments routinely oversell.
- **Not survivable against its own root.** Intel signs its quoting enclaves; AMD holds the ARK; Google and Apple hold their attestation roots. Root compromise or a leaked batch key is total and, in-band, undetectable.

### Is the RATS Endorser the same structural idea as a vocabulary/rating authority?

**Substantially yes, with two refinements that matter.**

The shared structure is exact: a signed token is syntactically verifiable but semantically empty, and a third party external to both signer and consumer supplies the interpretive frame that converts it into a claim. A PCR digest means "firmware 3.2.1 with secure boot enabled" *only because* a CoRIM said so, exactly as a rating token means "suitable for professional reliance" only because a vocabulary authority said so. In both cases the interpretive authority, not the signer, is where the real trust sits, and in both cases compromising or mis-scoping that authority silently changes what every existing signature means, retroactively.

The first refinement: RATS **splits the role in two**, which a generic vocabulary authority does not. The **Reference Value Provider** supplies "hash X *is* firmware Y" — a factual, publisher-of-record function. The **Endorser** supplies "this Attester's key belongs to a part with these capabilities, protected this well" — a *capability* claim about the device, not about the evidence. Endorsements in RATS are thus closer to a conformance/certification regime (a Common Criteria EAL, a lab accreditation) than to a semantic dictionary. A survey should say that RATS cleanly separates *lexical* authority from *evaluative* authority, and that most rating-system designs do not.

The second refinement, and the more interesting one: **RATS places the vocabulary upstream of the consumer.** A conventional vocabulary authority publishes definitions to everybody, and every relying party interprets tokens itself. RATS instead concentrates interpretation in the **Verifier** and hands the Relying Party a pre-digested **Attestation Result** — an *opinion*, not claims-plus-dictionary. The Relying Party can then be arbitrarily thin: it need not know what a PCR is, what firmware exists, or who Intel are. This is a genuine architectural contribution and the correct answer to "who has to understand the vocabulary." It also relocates the governance problem rather than solving it: the Verifier Owner's appraisal policy is now the place where "whose endorsements count" is decided, and that policy is out of scope of every RATS document. Any vocabulary-authority design should copy the Verifier/Relying Party split and should expect the policy layer to be where all the contested questions end up.

### Integrity of state, not delegation

Hardware attestation is doing something categorically different from X.509 and SPKI, and the difference is visible in the data structures.

**X.509 (RFC 5280, May 2008)** binds a *name* to a key, and the chain is a **delegation of naming authority**: `basicConstraints` with `pathLenConstraint`, `nameConstraints`, and EKU exist to bound how far, and over what, issuing authority may be passed on. **SPKI (RFC 2693, September 1999)** makes delegation a first-class field — the 5-tuple's explicit delegation bit and authorisation `tag` say *what permission is being passed and whether the recipient may pass it further*. Both are about **authority flowing between principals over time**.

An attestation has no principal-with-permissions as its subject and no delegation bit anywhere. Its subject is a **snapshot**: *this compute context was in this state, at this instant, in answer to this nonce*. Nothing is being granted. Where chains do appear — EK cert → AK cert, ARK → ASK → VCEK, DICE layer certificates — they are **provenance chains** (manufacturing lineage) or **derivation chains**, not delegations. DICE is the cleanest illustration: each layer's identity is *recomputed* as `KDF(parent secret, measurement)`. Authority is not handed down; identity is regenerated, and any change in the measured code produces a different identity instead of an invalid signature. That is the opposite of delegation semantics, where the delegated key stays the same and only the permission narrows.

Two consequences for a survey.

First, **temporal structure inverts**. Delegation credentials are long-lived and therefore need revocation infrastructure (CRL, OCSP) — the hard, unsolved part of PKI. Attestations are intrinsically ephemeral and nonce-bound; their hard problem is *freshness* (nonce vs. epoch-ID vs. timestamp, which RFC 9334 treats explicitly), and the Passport Model reintroduces a revocation-shaped problem only because it caches an Attestation Result for later reuse. AMD's encoding of the TCB version *into the VCEK derivation* is a neat expression of the attestation worldview: a stale TCB does not yield a revoked credential, it yields a *different* key.

Second, and worth flagging as a hazard: **the industry keeps packing integrity-of-state payloads into delegation containers.** Android key attestation carries device state in an X.509 extension; DICE Certificate Profiles express derivation chains as X.509. The syntax invites path-validation reflexes — check the chain, check validity dates, trust the leaf — that are simply wrong for state claims, where the only question that matters is whether the measurements match reference values *that the certificate does not contain*. The container says "delegation"; the payload says "snapshot." Verifier implementations that miss this are where attestation bugs actually live.

---

## REFERENCES

`title | authors | year | venue | stable id`

1. Remote ATtestation procedureS (RATS) Architecture | H. Birkholz, D. Thaler, M. Richardson, N. Smith, W. Pan | 2023 (January) | IETF, Informational, RATS WG | RFC 9334, DOI 10.17487/RFC9334, https://www.rfc-editor.org/info/rfc9334/
2. The Entity Attestation Token (EAT) | L. Lundblade, G. Mandyam, J. O'Donoghue, C. Wallace | 2025 (April) | IETF, Proposed Standard, RATS WG | RFC 9711, https://www.rfc-editor.org/info/rfc9711 · https://datatracker.ietf.org/doc/rfc9711/
3. Concise Reference Integrity Manifest | H. Birkholz, T. Fossati, Y. Deshpande, N. Smith, W. Pan | 2026 (6 July) | IETF Internet-Draft (RATS WG), Standards Track intended | draft-ietf-rats-corim-11, https://datatracker.ietf.org/doc/draft-ietf-rats-corim/
4. Direct Anonymous Attestation | E. Brickell, J. Camenisch, L. Chen | 2004 | ACM CCS 2004 (11th ACM Conf. on Computer and Communications Security), pp. 132–145 | https://eprint.iacr.org/2004/205 (IACR ePrint 2004/205)
5. Trusted Platform Module 2.0 Library, Parts 0–4, Version 184 | Trusted Computing Group | 2025 (20 March) | TCG specification | https://trustedcomputinggroup.org/resource/tpm-library-specification/ (e.g. Part 1: Architecture, .../Trusted-Platform-Module-2.0-Library-Part-1-Version-184_pub.pdf)
6. Information technology — Trusted Platform Module Library — Parts 1–4 | ISO/IEC JTC 1 | 2015 | International Standard | ISO/IEC 11889-1:2015 … 11889-4:2015, https://www.iso.org/standard/66510.html
7. TPM Main Specification, Version 1.2, Level 2, Revision 116 (Parts 1–3) | Trusted Computing Group | 2011 | TCG specification | https://trustedcomputinggroup.org/resource/tpm-main-specification/
8. TCG PC Client Platform Firmware Profile Specification, Family "2.0", Revision 1.05 | Trusted Computing Group | 2020 (3 Feb) | TCG specification | https://trustedcomputinggroup.org/wp-content/uploads/TCG_PCClient_PFP_r1p05_05_3feb20.pdf
9. TCG PC Client Platform TPM Profile (PTP) Specification for TPM 2.0, Version 1.06 Revision 32 | Trusted Computing Group | 2024 (5 April) | TCG specification | https://trustedcomputinggroup.org/wp-content/uploads/TCG-PC-Client-Platform-TPM-Profile-for-TPM-2.0-Version-1.06-Revision-32_5April24.pdf
10. Hardware Requirements for a Device Identifier Composition Engine, Revision 78 | Trusted Computing Group | 2018 | TCG specification | https://trustedcomputinggroup.org/wp-content/uploads/Hardware-Requirements-for-Device-Identifier-Composition-Engine-r78_For-Publication.pdf
11. DICE Layering Architecture, Version 1.0 Revision 0.19 | Trusted Computing Group | 2020 (23 July) | TCG specification | https://trustedcomputinggroup.org/wp-content/uploads/DICE-Layering-Architecture-r19_pub.pdf
12. Implicit Identity Based Device Attestation, Version 1.0 Revision 0.93 | Trusted Computing Group | — | TCG specification | https://trustedcomputinggroup.org/wp-content/uploads/TCG-DICE-Arch-Implicit-Identity-Based-Device-Attestation-v1-rev93.pdf
13. Symmetric Identity Based Device Attestation, v1 r0p94 | Trusted Computing Group | — | TCG specification (public review) | https://trustedcomputinggroup.org/wp-content/uploads/TCG_DICE_SymIDAttest_v1_r0p94_pubrev.pdf
14. DICE Certificate Profiles, r01 | Trusted Computing Group | — | TCG specification | https://trustedcomputinggroup.org/wp-content/uploads/DICE-Certificate-Profiles-r01_pub.pdf
15. Open Profile for DICE | Google | — | Open specification | https://pigweed.googlesource.com/open-dice/+/HEAD/docs/specification.md
16. TPM 2.0 Keys for Device Identity and Attestation, v1 r12 | Trusted Computing Group | 2021 (8 Oct) | TCG guidance | https://trustedcomputinggroup.org/wp-content/uploads/TPM-2p0-Keys-for-Device-Identity-and-Attestation_v1_r12_pub10082021.pdf
17. Intel Trust Domain Extensions (white paper) | Intel Corporation | — | Vendor specification/white paper | https://www.intel.com/content/dam/develop/external/us/en/documents/tdx-whitepaper-final9-17.pdf
18. Intel TDX Data Center Attestation Primitives — Quoting Library API | Intel Corporation | — | Vendor API specification | https://download.01.org/intel-sgx/latest/dcap-latest/linux/docs/Intel_TDX_DCAP_Quoting_Library_API.pdf
19. Intel SGX ECDSA QuoteLibReference (DCAP API) | Intel Corporation | — | Vendor API specification | https://download.01.org/intel-sgx/latest/dcap-latest/linux/docs/Intel_SGX_ECDSA_QuoteLibReference_DCAP_API.pdf
20. AMD SEV-SNP: A Confidential Computing Primer | (see arXiv record) | 2026 | arXiv preprint | arXiv:2608.04039, https://arxiv.org/abs/2608.04039
21. Attest an Amazon EC2 instance with AMD SEV-SNP | Amazon Web Services | — | Vendor documentation | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/snp-attestation.html
22. Arm's Confidential Compute Architecture Reference Attestation Token | T. Fossati, et al. | — | IETF Internet-Draft (individual submission) | draft-ffm-rats-cca-token-04, https://datatracker.ietf.org/doc/draft-ffm-rats-cca-token/
23. Learn the architecture — Introducing Arm Confidential Compute Architecture | Arm Ltd. | — | Vendor documentation | DEN0125, https://developer.arm.com/documentation/den0125/400/
24. Key and ID attestation | Android Open Source Project | — | Platform documentation | https://source.android.com/docs/security/features/keystore/attestation
25. Verify hardware-backed key pairs with key attestation | Android Developers | — | Platform documentation | https://developer.android.com/privacy-and-security/security-key-attestation
26. DCAppAttestService / App Attest | Apple Inc. | — | Platform documentation | https://developer.apple.com/documentation/devicecheck (WWDC21 session 10244, https://developer.apple.com/videos/play/wwdc2021/10244/)
27. SPKI Certificate Theory | C. Ellison, B. Frantz, B. Lampson, R. Rivest, B. Thomas, T. Ylonen | 1999 (September) | IETF, Experimental | RFC 2693, https://www.rfc-editor.org/info/rfc2693/
28. Internet X.509 Public Key Infrastructure Certificate and CRL Profile | D. Cooper, S. Santesson, S. Farrell, S. Boeyen, R. Housley, W. Polk | 2008 (May) | IETF, Proposed Standard | RFC 5280, DOI 10.17487/RFC5280, https://www.rfc-editor.org/info/rfc5280/
29. TCG Guidance on Integrity Measurements and Event Log Processing, v1 r0p118 | Trusted Computing Group | 2022 (24 Feb) | TCG guidance | https://trustedcomputinggroup.org/wp-content/uploads/TCG-Guidance-Integrity-Measurements-Event-Log-Processing_v1_r0p118_24feb2022-1.pdf

---

## COULD NOT ESTABLISH

- **Exact day of TPM 1.2 Revision 116.** Secondary sources say "1 March 2011"; the TCG filename encodes `01032011`, which is ambiguous between 1 March and 3 January 2011. The TCG landing page returned HTTP 403 to automated fetch. Year (2011) is safe; cite without a day.
- **Which TPM 1.2 revision ISO/IEC 11889:2009 corresponds to.** Sources confirm a 2009 ISO adoption of TPM 1.2, but not whether it tracks Revision 103 or 116. I did not cite a 2009 ISO number in the report for this reason.
- **Whether DICE Layering Architecture r19 (2020) is still current**, and the current revision of the DICE *Attestation Architecture* and *Certificate Profiles* documents. TCG's site blocked direct fetch; versions above come from PDF filenames and secondary summaries.
- **Whether CoRIM has been approved as an RFC.** As of draft-11 (July 2026) it remains an Internet-Draft; I could not confirm IESG approval or an assigned RFC number.
- **Current PC Client Platform Firmware Profile revision.** Verified r1.05 (Feb 2020); a later revision very likely exists but I could not confirm its number. (Note the separate, more recent *PC Client Platform TPM Profile* v1.06 rev 32, April 2024 — a different document.)
- **WG adoption status of the Arm CCA attestation token draft.** It is an individual submission (`draft-ffm-rats-cca-token`, -04), not `draft-ietf-rats-*`; I could not confirm RATS WG adoption or an Arm-published normative equivalent.
- **Current Android KeyMint `attestationVersion` / schema numbers** and the precise present-day StrongBox requirements — the docs are versioned continuously and I did not pin a value.
- **Attribution for the "cuckoo attack."** I described the relay problem but could not verify the canonical citation (believed to be Parno, *Bootstrapping Trust in a Trusted Platform*, USENIX HotSec 2008) before the session's web-search budget was exhausted. **Verify before citing.**
- **Whether Apple publishes a normative App Attest specification** (as opposed to developer documentation and WWDC material). Details above are drawn from Apple developer docs plus third-party analyses; the CBOR `apple-appattest` format details should be re-checked against Apple's own docs.
- **Session note:** the WebSearch budget (200/200) was exhausted during this task, so a handful of secondary details rest on search-result summaries rather than a direct fetch of the primary PDF; trustedcomputinggroup.org returns 403 to the fetch tool, so all TCG version/date claims come from filenames and search summaries rather than document front matter.
