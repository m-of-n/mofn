# Area H — Post-Quantum Signatures and Migration

## 1. Why: Shor, and why signatures are not "harvest now, decrypt later"

Shor's algorithm (FOCS 1994; SIAM J. Comput. 26(5):1484–1509, 1997) solves integer factorisation and discrete logarithm in polynomial time on a quantum computer. Every deployed public-key signature scheme — RSA, ECDSA, EdDSA — falls to it, as does every classical key-establishment scheme. Symmetric primitives and hash functions are only weakened (Grover), which is why hash-based signatures survive.

The migration *urgency* differs sharply between confidentiality and authenticity, and the difference is structural, not a matter of degree.

Encryption is retroactively breakable. A ciphertext recorded in 2026 can be decrypted in 2040 by whoever holds a cryptographically relevant quantum computer (CRQC). The secret was already committed to the wire; the adversary only needs patience. Hence "harvest now, decrypt later" and hence NIST's and industry's ordering: KEMs first.

Signatures are, in the ordinary case, *not* retroactively breakable. A forgery produced in 2040 cannot change the outcome of a verification that happened in 2026. Authentication is evaluated live, at verification time, so the deadline is "before a CRQC exists", not "before the data is captured". That is a real reprieve — but it has two carve-outs, and both are exactly where attestation lives:

1. **Trust anchors you cannot rotate.** A root CA key, or a secure-boot / TPM endorsement key fused at manufacture, is a public key published today that must still be trustworthy in 2045. It is harvested now and broken later, in precisely the HNDL sense. NSA's CNSA 2.0 puts software/firmware signing on the *earliest* deadline for exactly this reason.
2. **Artifacts still being verified after the break.** An attestation signed in 2026 and checked in 2050 is, at that verification event, indistinguishable from a signature forged in 2050. Long-lived attestation inherits the HNDL threat model even though transport signatures do not.

The mitigation for (2) is not simply a bigger signature. It is independent evidence that the signature existed before the break — RFC 3161 timestamps, transparency logs, evidence records. That evidence can be hash-based and therefore quantum-resistant.

## 2. NIST standardisation: what is final

The Secretary of Commerce approved and NIST published, all on **13 August 2024** (Federal Register notice 14 August 2024):

- **FIPS 203 — ML-KEM** (from CRYSTALS-Kyber), key encapsulation.
- **FIPS 204 — ML-DSA** (from CRYSTALS-Dilithium), module-lattice signatures.
- **FIPS 205 — SLH-DSA** (from SPHINCS+), stateless hash-based signatures.

**FN-DSA (FALCON), FIPS 206** is *not* final. NIST submitted the draft for approval on 28 August 2025; as of September 2026 it remains unpublished, with a final expected late 2026 / 2027. FN-DSA's attraction is compactness; its problem is floating-point Gaussian sampling, which is hard to implement in constant time. It should not be treated as available for a survey's migration recommendations.

FIPS 205 also forward-references **SP 800-230**, "Recommendation for Additional Stateless Hash-Based Digital Signature Parameter Sets", which will approve extra SLH-DSA parameter sets with *reduced* maximum signature counts — evidence that the parameter space is still moving, which matters for verifier longevity (§6).

## 3. The additional-signatures on-ramp

NIST ran a second competition for signatures with different structural assumptions (to avoid a lattice monoculture). On **14 May 2026** NIST published **NIST IR 8610**, the second-round status report, and advanced **nine** candidates to round 3: **FAEST, HAWK, MAYO, MQOM, QR-UOV, SDitH, SNOVA, SQIsign, UOV** — spanning isogeny, lattice, MPC-in-the-Head and multivariate families. Round 3 is expected to run roughly two years, with the 7th NIST PQC Standardization Conference in late spring/early summer 2027. Nothing from this track is deployable within the survey's horizon; its relevance is as a hedge against a lattice break.

## 4. Stateful hash-based signatures

**SP 800-208** (October 2020) approves **LMS/HSS** (RFC 8554) and **XMSS/XMSS^MT** (RFC 8391), as a supplement to FIPS 186. It approves only a subset of the RFCs' parameter sets (SHA-256, or SHAKE256 with 192-/256-bit output) and — critically — **requires key generation and signing to occur in a hardware cryptographic module that cannot export secret keying material**.

Statefulness is dangerous because each one-time key in the Merkle tree may be used exactly once. Reusing an index — from a restored VM snapshot, a database rollback, a replicated HSM, a crashed signer — leaks enough to forge. There is no cryptographic recovery; the failure is total and silent. This makes them unusable for general-purpose or distributed signing.

They are nonetheless recommended where signing is rare, centralised and hardware-controlled, and where conservatism matters more than convenience: firmware and software signing, and long-lived roots. CNSA 2.0 designates **LMS and XMSS (single-tree variants only)**, with LMS/SHA-256-192 preferred, as the choice for software and firmware signing, allowing ML-DSA-87 where distributed signing or high signature volume makes state management impractical.

## 5. Sizes — the actual migration blocker

Classical baseline (RFC 8032 / SEC1 conventions): Ed25519 = 32-byte public key, **64-byte signature**. ECDSA P-256 = 33-byte compressed key, 64-byte raw (≈70–72 DER) signature. RSA-2048 = 256-byte signature.

**ML-DSA (FIPS 204, Table 2), bytes:**

| Parameter set | Private key | Public key | Signature |
|---|---|---|---|
| ML-DSA-44 | 2 560 | 1 312 | **2 420** |
| ML-DSA-65 | 4 032 | 1 952 | **3 309** |
| ML-DSA-87 | 4 896 | 2 592 | **4 627** |

**SLH-DSA (FIPS 205, Table 2), bytes** — all 12 sets; SHA2 and SHAKE variants have identical sizes:

| Parameter set | Category | Public key | Signature |
|---|---|---|---|
| SLH-DSA-{SHA2,SHAKE}-128s | 1 | 32 | **7 856** |
| SLH-DSA-{SHA2,SHAKE}-128f | 1 | 32 | **17 088** |
| SLH-DSA-{SHA2,SHAKE}-192s | 3 | 48 | **16 224** |
| SLH-DSA-{SHA2,SHAKE}-192f | 3 | 48 | **35 664** |
| SLH-DSA-{SHA2,SHAKE}-256s | 5 | 64 | **29 792** |
| SLH-DSA-{SHA2,SHAKE}-256f | 5 | 64 | **49 856** |

Ratios against Ed25519's 64-byte signature: ML-DSA-44 ≈ **38×**, ML-DSA-87 ≈ **72×**, SLH-DSA-128s ≈ **123×**, SLH-DSA-256f ≈ **779×**. Counting key *and* signature, ML-DSA-87 is 7 219 bytes against Ed25519's 96 — about **75×**. SLH-DSA's tiny public keys (32–64 bytes) are a genuine advantage for trust anchors burned into ROM; its signatures are the problem.

## 6. Migration guidance

- **NIST IR 8547 ipd** (12 Nov 2024) sets the planning baseline: 112-bit ECDSA and RSA **deprecated after 2030**; ECDSA, EdDSA and RSA at *any* strength **disallowed after 2035**.
- **NIST SP 1800-38** (NCCoE, *Migration to Post-Quantum Cryptography*): Volume A preliminary draft April 2023; Volumes B and C preliminary drafts December 2023 (comment closed 20 Feb 2024). Volume C covers interoperability and performance testing of the draft standards. It is practice guidance, not a mandate.
- **CNSA 2.0** (NSA; announced September 2022, FAQ v2.0 April 2024, v2.1 December 2024). Support/prefer → exclusive-use: software & firmware signing **2025 → 2030**; web browsers/servers/cloud 2025 → 2033; traditional networking 2026 → 2030; operating systems 2027 → 2033; niche equipment 2030 → 2033; custom applications and legacy equipment → 2033. Signing uses LMS/XMSS or ML-DSA-87.
- **Hybrid / composite signatures.** IETF LAMPS `draft-ietf-lamps-pq-composite-sigs` defines composite ML-DSA with RSASSA-PKCS1-v1.5, RSASSA-PSS, ECDSA, Ed25519 and Ed448 for X.509, as a single algorithm identifier whose verification requires *both* components. It completed IETF Last Call on -14 (comments to 2026-02-03) and is at -19 (21 April 2026), Standards Track. Composite is the pragmatic transition vehicle for PKI, at the cost of stacking both signatures' sizes.

## 7. What this means for long-lived attestation — and the gap

A TLS handshake signature has a security lifetime of milliseconds; size costs a round trip. An attestation has the inverse profile: size is paid once at creation and stored forever, while the verification event may be decades away. That inverts the algorithm choice. For transport, ML-DSA's 2.4 KB is the pain point and lattice risk is acceptable. For a 2050 verification, **SLH-DSA is the better fit on assumptions** (security rests only on the hash function — no structured-lattice assumption that might not survive 25 years of cryptanalysis) and the worse fit on size. Its 32–64 byte public keys are ideal for trust anchors; its 7.8–49.9 KB signatures are hostile to per-step in-toto attestations, embedded C2PA manifests, and TPM command buffers.

Three consequences the survey should draw:

1. **Attestation systems need timestamping and transparency anchoring as a first-class requirement, not an option.** Only an independent, pre-break record of existence distinguishes a genuine 2026 signature from a 2050 forgery. Transparency logs and RFC 3161 timestamps provide this and can themselves be hash-based.
2. **Verifier longevity is an unmodelled risk.** Verification code for ML-DSA/SLH-DSA must exist and be correct in 2050, against parameter sets that are still being extended (SP 800-230).
3. **Envelopes must authenticate the algorithm and express quantum-resistant thresholds.** DSSE explicitly places "no restriction on the signature algorithm or format" and treats KEYID as an *unauthenticated hint*; the in-toto attestation envelope spec says implementations "SHOULD NOT require the inclusion of signing key algorithms in the signature". Agility by omission is not agility: it permits algorithm confusion, and it cannot express "at least N of the threshold signatures must be quantum-resistant" — a 3-of-5 root holding two ML-DSA and three Ed25519 keys is *not* quantum-resistant, a point raised explicitly in gittuf issue #1516.

### Stated PQ migration paths — assessment

| System | Stated path? | Evidence |
|---|---|---|
| **TPM / TCG** | **Yes, strongest** | TPM 2.0 spec **v1.85, released 27 March 2026**, integrates ML-KEM and ML-DSA (reported as ML-KEM for endorsement keys, ML-DSA for attestation keys). Caveat: silicon already deployed with RSA/ECDSA EKs fused at manufacture cannot be upgraded, and those EK certificates are the device's attestation trust anchor for its whole life. |
| **SCITT** | **Weakened/regressed** | Draft-09 §6.2.4 said agility "enables the gradual transition to stronger algorithms, including e.g. post-quantum signature algorithms." In the published **RFC 9943 (June 2026)**, §9.6 *Cryptographic Agility* is reduced to a single sentence — that SCITT "benefits from the format's cryptographic agility" via COSE — and the words "quantum" and "post-quantum" **do not appear anywhere in the RFC**. No PQ profile, no long-term-validation/evidence-record profile, despite receipts being explicitly long-lived. |
| **in-toto** | **No spec-level path; implementation-led** | No post-quantum issues exist in the `in-toto` GitHub org at all. Movement is entirely in the surrounding ecosystem: TUF **TAP 21** ("ML-DSA signing scheme for TUF metadata", merged May 2026); `securesystemslib` #1123 "Support ML-DSA" (closed 10 Aug 2026); `go-securesystemslib` #168 (opened 1 Sep 2026, still open); gittuf #1516 exploring ML-DSA roots; Sigstore threads across cosign, fulcio (#2002 "Bootstrap ML-DSA certificate chain"), rekor (#932 "Quantum-computing-proofing Rekor", open) and rekor-tiles (#425 dual-signed PQC checkpoints). |
| **C2PA** | **Genuine gap — the clearest finding** | The string "quantum" appears **zero times** in C2PA Specification **2.1, 2.2 and 2.3**. §13.2.1's allowed signature algorithms are ES256/384/512, PS256/384/512 and EdDSA (Ed25519 only) — all quantum-vulnerable — and "the deprecated list is empty." Meanwhile §10.3.2.5.1 states that manifests without timestamps cease to be valid when the credential expires, and the spec's own model is that timestamped manifests remain valid **indefinitely**. C2PA therefore explicitly commits to decades-long verification of content provenance using exclusively Shor-breakable algorithms, with no stated migration path and no deprecation signal. For a provenance system whose entire value proposition is long-horizon trust in media, this is the sharpest mismatch in the survey. |

The pattern: hardware (TPM) has moved, software supply chain (in-toto/TUF/Sigstore) is moving bottom-up through implementations while the specs stay silent, transparency (SCITT) has agility but dropped its explicit PQ language on the way to RFC, and content provenance (C2PA) has not engaged at all.

---

## REFERENCES

`title | authors | year | venue | stable id`

1. Algorithms for Quantum Computation: Discrete Logarithms and Factoring | P. W. Shor | 1994 | Proc. 35th Annual Symposium on Foundations of Computer Science (FOCS), pp. 124–134 | doi:10.1109/SFCS.1994.365700
2. Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer | P. W. Shor | 1997 | SIAM Journal on Computing 26(5):1484–1509 | doi:10.1137/S0097539795293172; arXiv:quant-ph/9508027
3. FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard | NIST | 2024 | NIST FIPS (published 13 Aug 2024) | doi:10.6028/NIST.FIPS.203
4. FIPS 204: Module-Lattice-Based Digital Signature Standard | NIST | 2024 | NIST FIPS (published 13 Aug 2024) | doi:10.6028/NIST.FIPS.204
5. FIPS 205: Stateless Hash-Based Digital Signature Standard | NIST | 2024 | NIST FIPS (published 13 Aug 2024) | doi:10.6028/NIST.FIPS.205
6. Announcing Issuance of FIPS 203, FIPS 204 and FIPS 205 | U.S. Dept. of Commerce / NIST | 2024 | Federal Register, 14 Aug 2024 | FR 2024-17956
7. FIPS 206 (FN-DSA) Status Update | R. Perlner (NIST) | 2025 | NIST PQC presentation / pqc-forum announcement | csrc.nist.gov/csrc/media/presentations/2025/fips-206-fn-dsa-(falcon)/images-media/fips_206-perlner_2.1.pdf
8. NIST IR 8610: Status Report on the Second Round of the Additional Digital Signature Schemes for the NIST PQC Standardization Process | NIST | 2026 | NIST Internal Report (14 May 2026) | csrc.nist.gov/pubs/ir/8610/final
9. Nine Candidates Advance to the Third Round of the Additional Digital Signatures for the PQC Standardization Process | NIST | 2026 | NIST news release, 14 May 2026 | nist.gov/news-events/news/2026/05/nine-candidates-advance-third-round-additional-digital-signatures-pqc
10. NIST SP 800-208: Recommendation for Stateful Hash-Based Signature Schemes | D. Cooper, D. Apon, Q. Dang, M. Davidson, M. Dworkin, C. Miller | 2020 | NIST Special Publication (Oct 2020) | doi:10.6028/NIST.SP.800-208
11. Leighton-Micali Hash-Based Signatures | D. McGrew, M. Curcio, S. Fluhrer | 2019 | IETF RFC 8554 (Informational) | doi:10.17487/RFC8554
12. XMSS: eXtended Merkle Signature Scheme | A. Huelsing, D. Butin, S. Gazdag, J. Rijneveld, A. Mohaisen | 2018 | IETF RFC 8391 (Informational) | doi:10.17487/RFC8391
13. NIST SP 800-230 (forthcoming): Recommendation for Additional Stateless Hash-Based Digital Signature Parameter Sets | NIST | forthcoming | NIST Special Publication | cited as ref. [24] in FIPS 205
14. NIST IR 8547 ipd: Transition to Post-Quantum Cryptography Standards | NIST | 2024 | NIST Internal Report, Initial Public Draft (12 Nov 2024) | csrc.nist.gov/pubs/ir/8547/ipd
15. NIST SP 1800-38 (A/B/C): Migration to Post-Quantum Cryptography | NIST NCCoE | 2023 | NIST Special Publication, preliminary drafts (Vol. A Apr 2023; Vols. B & C Dec 2023) | csrc.nist.gov/pubs/sp/1800/38/iprd-(1)
16. Commercial National Security Algorithm Suite 2.0 — Algorithms and FAQ | U.S. National Security Agency | 2022 (FAQ v2.0 Apr 2024; v2.1 Dec 2024) | NSA Cybersecurity Advisory / CSI | media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF
17. Composite Module-Lattice-Based Digital Signature Algorithm (ML-DSA) for use in X.509 Public Key Infrastructure | M. Ounsworth, J. Gray, M. Pala, J. Klaussner, S. Fluhrer | 2026 | IETF Internet-Draft draft-ietf-lamps-pq-composite-sigs-19 (21 Apr 2026), Standards Track | datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/
18. An Architecture for Trustworthy and Transparent Digital Supply Chains | H. Birkholz, A. Delignat-Lavaud, C. Fournet, Y. Deshpande, S. Lasker | 2026 | IETF RFC 9943 (Standards Track, June 2026) | doi:10.17487/RFC9943
19. An Architecture for Trustworthy and Transparent Digital Supply Chains (draft-ietf-scitt-architecture-09, §6.2.4) | same authors | 2024 | IETF Internet-Draft, 15 Oct 2024 | ietf.org/archive/id/draft-ietf-scitt-architecture-09.html
20. Trusted Platform Module 2.0 Library Specification, v1.85 | Trusted Computing Group | 2026 | TCG specification, released 27 Mar 2026 | trustedcomputinggroup.org/new-computing-specification-implements-pqc-measures-to-protect-users-from-quantum-attacks/
21. C2PA Specification, versions 2.1 / 2.2 / 2.3 (§13.2.1 Signature Algorithms; §10.3.2.5.1 time-stamps) | Coalition for Content Provenance and Authenticity | 2024–2026 | C2PA technical specification | spec.c2pa.org/specifications/specifications/2.3/specs/C2PA_Specification.html
22. DSSE: Dead Simple Signing Envelope — Protocol | Secure Systems Lab | 2021– | Project specification | github.com/secure-systems-lab/dsse/blob/master/protocol.md
23. in-toto Attestation Framework — Envelope (spec/v1/envelope.md) | in-toto project | 2023– | Project specification | github.com/in-toto/attestation/blob/main/spec/v1/envelope.md
24. TAP 21: ML-DSA signing scheme for TUF metadata | The Update Framework | 2026 | TUF Augmentation Proposal (PR #195, opened 4 May 2026, merged) | github.com/theupdateframework/taps/blob/master/tap21.md
25. Edwards-Curve Digital Signature Algorithm (EdDSA) | S. Josefsson, I. Liusvaara | 2017 | IETF RFC 8032 (Informational) | doi:10.17487/RFC8032
26. Ecosystem PQ-migration issue threads (evidence of activity, not normative) | various | 2026 | GitHub | securesystemslib#1123 (closed 2026-08-10); go-securesystemslib#168 (open, 2026-09-01); gittuf#1516; sigstore/rekor#932; sigstore/fulcio#2002; sigstore/rekor-tiles#425; sigstore/cosign#4960

---

## COULD NOT ESTABLISH

- **SP 800-230 publication status.** FIPS 205 reference [24] lists it as "[Forthcoming]". `csrc.nist.gov/pubs/sp/800/230/final` returns HTTP 404. I could not determine whether a draft or final has since appeared, nor what the additional parameter sets are.
- **Whether NIST IR 8547 has been finalised.** Only the initial public draft (12 Nov 2024) is confirmed on CSRC. Secondary sources say it was still a draft in mid-2026; unverified.
- **OMB M-26-15.** Appeared only in a secondary search summary as directing agencies to align with IR 8547 and setting 2035 as the full-migration date. Not verified against a primary source; treat as unconfirmed.
- **FIPS 206 / FN-DSA draft submission date (28 Aug 2025).** From secondary reporting (DigiCert, Encryption Consulting) and a NIST pqc-forum thread title; I did not retrieve a NIST-hosted document stating it. The *absence* of a final FIPS 206 as of Sept 2026 is well supported.
- **TPM 2.0 v1.85 key-type mapping.** TCG's own announcement page returned HTTP 403. The version (v1.85), date (27 Mar 2026) and the ML-KEM + ML-DSA addition are confirmed via SDxCentral; the specific mapping "ML-KEM for endorsement keys, ML-DSA for attestation keys" comes from a secondary summary only. I did not read the TCG spec itself, and could not confirm whether LMS/XMSS or SLH-DSA are on TCG's roadmap.
- **SP 1800-38 current status.** Only preliminary drafts of Volumes A, B and C are confirmed (2023). Whether final volumes or additional volumes have been published since is unestablished.
- **CNSA 2.0 timeline table** is taken from a secondary aggregator (postquantum.com), consistent with the Wikipedia algorithm list; the NSA FAQ PDF at media.defense.gov was not retrievable from this environment (returned HTML, not PDF). The category-by-category years should be re-checked against NSA's FAQ v2.1 before publication.
- **Ed25519 / ECDSA / RSA sizes** are standard values from RFC 8032 and SEC1/X9.62 encoding conventions, stated from specification convention rather than re-fetched; the PQ sizes were extracted directly from the FIPS 204 and FIPS 205 PDFs.
- **C2PA non-public work.** I established that the *published* specs 2.1–2.3 contain no quantum-related text and that the allowed algorithm list is entirely classical. I could not establish whether C2PA has internal, mailing-list or roadmap discussion of PQ migration — GitHub issue search over `c2pa-org` for "post-quantum" returned one unrelated issue. The gap claim should be stated as "no stated migration path in the published specification", which is precisely what the evidence supports.
- **Web search budget for this session was exhausted (200/200)** partway through; remaining verification was done by direct fetch of primary PDFs/RFCs and the GitHub API, which is why some secondary claims above remain unconfirmed.

Working files (FIPS 204/205 and IR 8547 text extracts, RFC 9943, C2PA spec HTML) are in `/private/tmp/claude-502/-Users-paul-cb-projects-USF-2026-Provenance/a2928010-b766-425d-ad2d-56d56dd96b80/scratchpad/`.
