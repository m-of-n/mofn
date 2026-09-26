# Area B — X.509 / PKIX

Everything below is web-verified this session. RFC text was downloaded from rfc-editor.org and quoted from the local copies (not paraphrased from memory). I also ran an **original measurement** against CCADB's live data to close the biggest gap in the literature — see §4.

---

## 1) MINI-REPORT

### 1. Lineage: a certificate format designed to log into a directory

ITU-T X.509 was first published in **November 1988** as *"The Directory – Authentication framework,"* a member Recommendation of the X.500 Directory series (ISO/IEC 9594-8). Its current title is *"Information technology – Open Systems Interconnection – The Directory: Public-key and attribute certificate frameworks"*; the in-force edition is the 9th (10/2019), carried forward by Corrigenda 1–3 (2021, 2023, 2026) and Amendment 1 (2024). No 10th edition exists as of September 2026.

The design assumption is load-bearing and it failed. X.509's naming type is the X.500 Distinguished Name, which presupposes a single global Directory with one global DN namespace in which every entity has exactly one canonical name and certificates are published for retrieval. Gutmann's assessment is blunt: *"the original problem that X.509 certificates were designed to solve was access control to an X.500 directory, [which] is nothing like the problem or problems that need to be solved today,"* and *"since the concept of a global distributed directory... was never realised, there's no clear idea where to fetch a certificate from"* — the "Which directory?" problem, alongside the "Which John Smith?" problem. RFC 2693 (SPKI Certificate Theory) states the same conclusion from the other side: *"The original X.500 plan is unlikely ever to come to fruition. Collections of directory entries... are considered valuable or even confidential by those owning the lists and are not likely to be released to the world."*

The Internet's answer was a profile, not a redesign. RFC 5280 (May 2008) keeps X.509's ASN.1 and path-validation semantics and repurposes the container: identities that actually matter — DNS names, email addresses, IP addresses, URIs — move into `subjectAltName`, and §4.2.1.6 concedes that a certificate may carry an **empty** subject DN entirely, in which case `subjectAltName` MUST be present and critical. The global namespace was abandoned in practice while its syntax was retained.

Critically for this survey, **PKIX also deliberately dropped the one thing its predecessor had that scoped delegation**. RFC 1422 (Kent, 1993, PEM) imposed a mandatory *name subordination rule*: a CA could only certify entities whose names sat below its own in the X.500 tree, and RFC 5280 §3.2 describes exactly why it was dropped — X.509v3 extensions "obviate the need for the name subordination rule," yielding a "more flexible architecture" in which **"Name constraints may be imposed through explicit inclusion of a name constraints extension in a certificate, but are not required."** Scoped delegation went from a structural invariant to a CA-discretionary option in one design decision. That sentence is the single most important primary-source finding in this area.

### 2. RFC 5280 as the operative profile

RFC 5280 remains **Proposed Standard** — never advanced — and obsoletes RFC 3280, which obsoleted RFC 2459. It has been updated nine times: RFC 6818, 8398, 8399, 9549, 9598, 9608, 9618, 9925, 10007. It contains roughly 304 `MUST`, 34 `MUST NOT`, 82 `SHOULD`, 13 `SHOULD NOT` and 10 `SHALL` occurrences. It is a profile, not an architecture: it constrains encoding and validation and says almost nothing about who may vouch for what.

### 3. Path validation (§6) — what it actually does

The algorithm takes nine inputs, including *trust anchor information*: issuer name, key algorithm, key, optional parameters. RFC 5280 §6.1.1 says plainly that *"the trust anchor information is trusted because it was delivered to the path processing procedure by some trustworthy out-of-band procedure."* The trust decision is imported, not derived.

Initialization (§6.1.2) establishes eleven state variables, including `permitted_subtrees`, `excluded_subtrees`, `valid_policy_tree`, `explicit_policy`, `policy_mapping`, `inhibit_anyPolicy` and `max_path_length`. Then, for each certificate *i* in 1..n:

- **§6.1.3(a)** — verify signature under `working_public_key`; validity period covers now; certificate is not revoked; issuer name equals `working_issuer_name`.
- **§6.1.3(b)(c)** — check the subject DN and every `subjectAltName` against `permitted_subtrees` and `excluded_subtrees`, skipping self-issued non-final certificates.
- **§6.1.3(d)(e)(f)** — advance the policy tree; fail if `explicit_policy` is 0 and the tree is NULL.
- **§6.1.4(g)** — if this certificate carries `nameConstraints`, **intersect** `permittedSubtrees` into state and **union** `excludedSubtrees` into state. Constraints therefore only ever tighten going down the path — the one genuinely sound piece of the design.
- **§6.1.4(h)–(j)** — decrement counters; apply `policyConstraints` and `inhibitAnyPolicy`.
- **§6.1.4(k)(l)(m)(n)** — require `basicConstraints` present with `cA=TRUE`; decrement and check `max_path_length`; apply `pathLenConstraint`; require `keyCertSign` if `keyUsage` is present.
- **§6.1.4(o)** — recognize and process any other critical extension.
- **§6.1.5/6.1.6** — wrap up policy state and emit the validated public key, subject DN and policy set.

Two structural facts matter. First, `nameConstraints` processing sits in step (g), *inside* the loop, and is fed only by certificates in the path — the algorithm has no channel for the relying party's own scoping of a trust anchor. RFC 5280 §6.2 explicitly leaves root-embedded constraints advisory: *"Implementations that use self-signed certificates to specify trust anchor information are free to process or ignore such information."* Making trust-anchor constraints binding required RFC 5937 (Ashmore & Wallace, 2010) — which is **Informational**. Second, §6.1.3(a)(3) requires only that "the certificate is not revoked," with the method left open, and offers no rule for what to do when status cannot be obtained.

### 4. Name constraints (§4.2.1.10) — and whether anyone uses them

The mechanism is real: `permittedSubtrees`/`excludedSubtrees` over `GeneralName` forms, exclusions dominating permissions, intersect-and-union propagation. RFC 5280 requires it to appear only in CA certificates, requires conforming CAs to mark it **critical**, forbids an empty sequence, and requires conforming applications to process `directoryName` constraints (with `rfc822Name`, URI, `dNSName`, `iPAddress` only `SHOULD`).

But the semantics are **fail-open by construction**. §4.2.1.10: *"Restrictions apply only when the specified name form is present. If no name of the type is in the certificate, the certificate is acceptable."* RFC 5280's own Security Considerations (§8) concede the consequence: ***"In general, using the nameConstraints extension to constrain one name form (e.g., DNS names) offers no protection against use of other name forms (e.g., electronic mail addresses)."*** Worse, §4.2.1.10 declares that *"the syntax and semantics for name constraints for otherName, ediPartyName, and registeredID are not defined by this specification"* — so any newly defined `otherName` identity type escapes existing constraints by default. That is not hypothetical: RFC 9598 (2024) had to **amend §4.2.1.10** to extend `rfc822Name` constraints to the new `SmtpUTF8Mailbox` `otherName`, and additionally forbid its use for ASCII local-parts, precisely because *"legacy Certification Authorities constrained to issue certificates for a specific set of domains would lack corresponding UTF-8 constraints."*

The CA/Browser Forum had to engineer around all of this. TLS BR §7.1.2.5.2 makes `nameConstraints` `MUST` for the *Technically Constrained TLS Subordinate CA* profile and then spells out the closure by hand: `permittedSubtrees` must contain `dNSName`, `iPAddress` **and** `directoryName` entries; if no `dNSName` is permitted the CA **MUST include a zero-length `dNSName`** in exclusions; if no IPv4/IPv6 is permitted it **MUST include 8 / 32 zero octets**. In other words, "scoped" had to be re-expressed as "explicitly exclude the universe," name form by name form. And the Forum had to relax RFC 5280 itself: *"As an explicit exception from RFC 5280, this extension SHOULD be marked critical, but MAY be marked non-critical if compatibility with certain legacy applications that do not support Name Constraints is necessary."* The S/MIME BR is even franker, permitting non-critical constraints *"until the nameConstraints extension is supported by Application Software Suppliers whose software is used by a substantial portion of Relying Parties worldwide"* — a 2023 standards document conceding the extension still is not reliably supported.

**Is it used? I measured it.** I downloaded CCADB's `MozillaIntermediateCertsCSVReport` (all disclosed, unexpired, unrevoked intermediates in Mozilla's program) on 2026-09-26, parsed all 1,769 PEMs with `openssl x509 -text`, and counted:

| Measure | Result |
|---|---|
| Disclosed intermediate CA certificates | 1,769 |
| Carrying a `nameConstraints` extension | **31 (1.8%)** |
| `serverAuth`-capable intermediates | 1,613 — of which 31 constrained (**1.9%**) |
| Of the 31, marked **critical** as RFC 5280 requires | **2** |
| Issuer concentration | 29 of 31 from HARICA roots; 1 Actalis; 1 TunTrust |

I also parsed CCADB's `IncludedCACertificateReportPEMCSV`: **172 included roots from 50 distinct CA owners; 121 carry the Websites trust bit, 91 the Email bit.** Exactly **3 of 172** carry a "Mozilla Applied Constraints" value, and only **one** is a positive scope — TÜBİTAK Kamu SM, constrained out-of-band to `*.tr`; the other two are Telekom Security S/MIME roots annotated *"No name constraints are to be applied."* Out-of-band root-store scoping is applied to one root in 172, and it is Firefox-specific: Go's bundle does not carry it (golang/go#61963).

Implementation quality is still poor in 2026. I verified five distinct `crypto/x509` name-constraint CVEs against the authoritative MITRE CVE records, all within eleven months: **CVE-2025-58187** (quadratic-complexity name-constraint checking, pub. 2025-10-29), **CVE-2025-61727** ("an excluded subdomain constraint... does not prevent a leaf certificate from claiming the SAN `*.example.com`", pub. 2025-12-03), **CVE-2026-27137** (multiple email constraints sharing a local-part — "only the last constraint will be considered"), **CVE-2026-27138** (panic on empty DNS name plus excluded constraints), **CVE-2026-33810** (case-sensitivity bypass of `excludedSubtrees`, pub. 2026-04-08). OpenSSL's CVE-2022-3602/3786 buffer overflows were, per the project's own post-mortem, *"introduced as part of punycode decoding functionality (currently only used for processing email address name constraints in X.509 certificates)."* NSS shipped a period in which libPKIX silently did not enforce constraints at all (Bugzilla #856060). (Note: CVE-2021-3450 is **not** a name-constraints bug — it is an `X509_V_FLAG_X509_STRICT` flaw that clobbered the CA-validity check.)

### 5. Revocation: documented collapse, now formally conceded

RFC 5280 §3.3 states that *"this profile does not require the issuance of CRLs."* §5.1.2.5 requires `nextUpdate` but then admits *"the behavior of clients processing CRLs that omit nextUpdate is not specified by this profile."* §6.3.3 terminates with *"if the revocation status has still not been determined, then return the cert_status UNDETERMINED"* — and nothing in RFC 5280 says what a relying party must do with UNDETERMINED. That undefined branch is where soft-fail lives.

Measurement confirms the collapse. Liu et al. (IMC 2015) found 8% of served certificates revoked, ~1% of still-advertised certificates actually revoked, only ~3% (corrected to 6–7%) of hosts supporting OCSP stapling, and that **"no browser in its default configuration correctly checks all revocations and rejects certificates if revocation information is unavailable"** — mobile browsers never check at all. Chrome's CRLSet covered **0.35%** of revocations. Zhang et al. (IMC 2014) found that three weeks after Heartbleed, >87% of vulnerable certificates had not been revoked. Langley's "Revocation doesn't work" (2011) and "No, don't enable revocation checking" (2014) made the soft-fail argument that justified replacing live checking with CRLSets and OneCRL — both admittedly partial. OCSP Must-Staple (RFC 7633, 2015) reached **0.02%** of all certificates (Chung et al., IMC 2018).

The ecosystem has since capitulated and rebuilt. CA/B Forum ballot SC-063 (passed July 2023, effective 2024-03-15) made OCSP **optional** and CRLs **mandatory**. Let's Encrypt shut its OCSP responders down entirely on **2025-08-06**, citing the privacy leak: *"the Certificate Authority immediately becomes aware of which website is being visited from that visitor's particular IP address."* The IETF standardized the surrender in **RFC 9608** (June 2024), which adds a `noRevAvail` extension and updates §6.1.3 so that *"Step (a)(3) is skipped"* — revocation checking is formally omitted for short-lived certificates. Meanwhile CRLite finally shipped in Firefox 142 (2025), reportedly reaching ~87.8% coverage. The honest summary: online revocation as specified in RFC 5280 and RFC 6960 never worked, and the replacement is a combination of push-based local data structures and certificates too short-lived to need revoking.

### 6. Certificate Transparency

RFC 6962 (Laurie, Langley, Kasper, June 2013) and RFC 9162 (Laurie, Messeri, Stradling, December 2021) are **both Experimental**. RFC 9162's own framing is exact about what CT buys: *"The logs do not themselves prevent misissuance, but they ensure that interested parties (particularly those named in certificates) can detect such misissuance."* CT is a detection and audit control layered over a trust model it cannot fix.

Two deployment facts matter for a survey. Chrome has required SCTs for all publicly-trusted certificates issued on or after **2018-04-30**. And **RFC 9162 has essentially no deployment**: Apple's CT policy still names RFC 6962, and Let's Encrypt engineering states on the record *"I don't believe there are any implementations of ct v2, and nobody runs any logs... It does seem like ctv2 is DOA."* The live evolution path is instead the non-IETF **Static CT API / Sunlight** specification, which keeps RFC 6962 semantics and changes only the serving architecture; Let's Encrypt retires its RFC 6962-API logs in February 2026. A survey that cites RFC 9162 as "the current CT standard" would be describing a document, not a system.

### 7. What the CA compromises demonstrated

DigiNotar (2011) is the flagship. Fox-IT's *"Black Tulip"* final report (13 August 2012) documents perimeter breach on 17 June 2011, all eight CA-management servers compromised, and **531** fraudulent certificates across six issuing sub-CAs — not the commonly cited "300+". The `*.google.com` certificate was used against roughly 300,000 unique IPs, ~95% in Iran. It was caught not by X.509 but by **Chrome's hardcoded key pinning**. DigiNotar was bankrupt within a month.

The pattern repeats with different mechanisms: Comodo (March 2011, 9 certificates via a compromised RA); TURKTRUST (Aug 2011 mis-issued intermediates, `*.google.com` MITM detected Dec 2012 again via Chrome pinning); ANSSI (Dec 2013, a government sub-CA in a traffic-inspection appliance); Trustwave (Feb 2012, a sub-CA knowingly sold for SSL inspection); Symantec (2015 test certificates caught by CT, escalating to full Chrome/Firefox distrust in 2017–18); WoSign/StartCom (2016, 64 knowingly backdated SHA-1 certificates and a concealed acquisition); and continuing — Camerfirma (2021), TrustCor (2022), e-Tugra (2022 disclosure, 2023 removal), **Entrust (June 2024**, distrusted for "an observed pattern of compliance failures, unmet improvement commitments, and the absence of tangible, measurable progress"; business sold to Sectigo in January 2025), Chunghwa Telecom and Netlock (2025).

The common property is structural, not operational. Because name constraints are optional and almost never present, **any** of the 121 TLS-trusted roots in Mozilla's store — or any of the 1,769 intermediates beneath them — can issue a technically valid certificate for **any** name. Security is the minimum over ~50 organizations across many jurisdictions. EFF's SSL Observatory named this in 2010: the trust model is *"1 of N CAs (N is large)"*, and *"the security of HTTPS is only as strong as the practices of the least trustworthy/competent CA."* Every mitigation that actually caught these incidents — pinning, CRLSets, CT, root-program distrust — sits **outside** RFC 5280.

### 8. S/MIME as the email-identity application

RFC 8551 (Schaad, Ramsdell, Turner, April 2019) defines S/MIME 4.0 messaging; RFC 8550 covers certificate handling. Identity binding is looser than TLS's: the email address *"SHOULD be in the subjectAltName extension and SHOULD NOT be in the subject distinguished name,"* but receiving agents **MUST** also recognize the legacy PKCS#9 `emailAddress` attribute in the DN — two places a verifier must look, with the domain part compared case-insensitively and the local part only `SHOULD` be. Most tellingly, *"Receiving agents MUST recognize and accept certificates that contain no email address,"* falling back to an address book. The name-to-key binding that S/MIME rests on is optional in the certificate.

The CA/Browser Forum S/MIME Baseline Requirements (v1.0.0 effective 2023-09-01) impose the structure RFC 8551 lacks: four certificate types (mailbox-, organization-, sponsor-, individual-validated) across Legacy/Multipurpose/Strict generations, with Legacy profiles prohibited after 2025-07-15. Their §7.1.5 makes `nameConstraints` on `rfc822Name` and `directoryName` mandatory for a sub-CA to count as technically constrained — but only 91 of 172 Mozilla roots carry the Email trust bit at all, and my measurement found essentially no constrained S/MIME intermediates in the TLS-oriented disclosure set.

### 9. Assessment: does X.509 already solve scoped delegation?

**No — but the honest reason is narrower and more interesting than "the mechanism doesn't exist."**

Name constraints *are* a genuine scoped-delegation primitive. They are enforced offline by the relying party, they tighten monotonically down a path (intersect permitted, union excluded), and they need no third party at validation time. A competing design that claims X.509 *cannot express* scoped delegation is making a false claim and would be correctly rebutted by any PKIX reviewer.

The defensible claim is about **defaults, enforceability and expressibility**, and it is well supported:

1. **Optional by explicit design decision.** RFC 1422 mandated name subordination; RFC 5280 §3.2 states constraints "are not required." The invariant was removed, not absent.
2. **Fail-open by default.** A name form not mentioned is unconstrained (§4.2.1.10), which RFC 5280 §8 itself admits "offers no protection against use of other name forms." Safety requires enumerating and explicitly excluding every name form — which the CA/B Forum had to specify literally, down to zero-length `dNSName` and 32 zero octets. And new name forms escape old constraints by default, as RFC 9598 had to patch.
3. **Not binding at the trust root.** §6.2 makes constraints in a self-signed root advisory. Binding trust-anchor constraints require RFC 5937, which is Informational; root-store-imposed constraints exist but are applied to **1 of 172** Mozilla roots and are not portable to other TLS stacks.
4. **Still not reliably enforced.** Five Go name-constraint CVEs in eleven months, OpenSSL memory-safety bugs in the same code path, a historical NSS period with no enforcement, and a 2023 CA/B Forum document still permitting non-critical constraints because client support is inadequate.
5. **Barely deployed.** 31 of 1,769 intermediates (1.8%); 29 of those from a single CA family; 2 marked critical.

The deepest point is not a deployment statistic. In X.509, scoping is something a **parent grants to a child**, expressed over a name form the parent chose, and the top of every chain is unconstrained by construction — a relying party has no in-format way to say "I trust this CA only for `example.com`." That has to live in root-store policy, out of band. A design in which a principal *is* a key and every name is interpreted relative to its issuing principal makes unscoped authority **inexpressible** rather than merely discouraged. That is a real and defensible difference — a difference in what the format permits by default, not in whether scoping can be written down at all. I would recommend the project state the claim in exactly those terms; the stronger phrasing is both false and easy to refute.

*(~1,750 words excluding tables and headings.)*

---

## 2) REFERENCES

Format: `title | authors | year | venue | stable id`

**Standards — core**
1. The Directory: Public-key and attribute certificate frameworks | ITU-T | 2019 (Ed.9; 1st ed. 1988) | ITU-T Recommendation X.509 / ISO-IEC 9594-8 | https://www.itu.int/rec/T-REC-X.509/en
2. The Directory – Authentication framework | ITU-T | 1988 | ITU-T Rec. X.509 (1st ed.) | T-REC-X.509-198811-S
3. Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile | D. Cooper, S. Santesson, S. Farrell, S. Boeyen, R. Housley, W. Polk | 2008 | IETF Proposed Standard | RFC 5280
4. Privacy Enhancement for Internet Electronic Mail: Part II: Certificate-Based Key Management | S. Kent | 1993 | IETF (Historic) | RFC 1422
5. Internet X.509 PKI Certificate and CRL Profile | R. Housley, W. Polk, W. Ford, D. Solo | 2002 | IETF | RFC 3280 (obs. by 5280)
6. Updates to the Internet X.509 PKI Certificate and CRL Profile | P. Yee | 2013 | IETF | RFC 6818
7. Internationalized Email Addresses in X.509 Certificates | A. Melnikov, W. Chuang, C. Bonnell | 2024 | IETF Standards Track (updates 5280) | RFC 9598
8. Internationalization Updates to RFC 5280 | — | 2024 | IETF (updates 5280) | RFC 9549
9. No Revocation Available for X.509 Public Key Certificates | R. Housley, T. Okubo, J. Mandel | 2024 | IETF Standards Track (updates 5280) | RFC 9608
10. Updates to X.509 Policy Validation | D. Benjamin | 2024 | IETF (updates 5280) | RFC 9618
11. Unsigned X.509 Certificates | D. Benjamin | 2026 | IETF (updates 5280) | RFC 9925
12. Clarification to Processing Key Usage Values During CRL Validation | — | 2026 | IETF (updates 5280) | RFC 10007
13. Trust Anchor Format | R. Housley, S. Ashmore, C. Wallace | 2010 | IETF Standards Track | RFC 5914
14. Using Trust Anchor Constraints during Certification Path Processing | S. Ashmore, C. Wallace | 2010 | IETF **Informational** | RFC 5937

**Revocation and transparency**
15. X.509 Internet PKI Online Certificate Status Protocol – OCSP | S. Santesson, M. Myers, R. Ankney, A. Malpani, S. Galperin, C. Adams | 2013 | IETF Proposed Standard | RFC 6960
16. The TLS Multiple Certificate Status Request Extension | Y. Pettersen | 2013 | IETF Proposed Standard | RFC 6961
17. X.509v3 TLS Feature Extension (OCSP Must-Staple) | P. Hallam-Baker | 2015 | IETF Proposed Standard | RFC 7633
18. Certificate Transparency | B. Laurie, A. Langley, E. Kasper | 2013 | IETF **Experimental** | RFC 6962
19. Certificate Transparency Version 2.0 | B. Laurie, E. Messeri, R. Stradling | 2021 | IETF **Experimental** | RFC 9162

**S/MIME**
20. S/MIME Version 4.0 Message Specification | J. Schaad, B. Ramsdell, S. Turner | 2019 | IETF Standards Track | RFC 8551
21. S/MIME Version 4.0 Certificate Handling | J. Schaad, B. Ramsdell, S. Turner | 2019 | IETF Standards Track | RFC 8550

**Critiques of global naming**
22. SPKI Certificate Theory | C. Ellison, B. Frantz, B. Lampson, R. Rivest, B. Thomas, T. Ylonen | 1999 | IETF Experimental | RFC 2693
23. SPKI Requirements | C. Ellison | 1999 | IETF Experimental | RFC 2692
24. SDSI — A Simple Distributed Security Infrastructure (v1.1) | R. Rivest, B. Lampson | 1996 | MIT tech report | https://people.csail.mit.edu/rivest/pubs/RL96.ver-1.1.html
25. PKI: It's Not Dead, Just Resting | P. Gutmann | 2002 | IEEE Computer 35(8):41–49 | DOI 10.1109/MC.2002.1023787
26. Ten Risks of PKI: What You're Not Being Told about Public Key Infrastructure | C. Ellison, B. Schneier | 2000 | Computer Security Journal 16(1):1–7 | https://www.schneier.com/academic/archives/2000/01/ten_risks_of_pki_wha.html

**Measurement literature**
27. An End-to-End Measurement of Certificate Revocation in the Web's PKI | Y. Liu, W. Tome, L. Zhang, D. Choffnes, D. Levin, B. Maggs, A. Mislove, A. Schulman, C. Wilson | 2015 | ACM IMC '15, pp. 183–196 | DOI 10.1145/2815675.2815685
28. Analysis of SSL Certificate Reissues and Revocations in the Wake of Heartbleed | L. Zhang, D. Choffnes, D. Levin, T. Dumitraş, A. Mislove, A. Schulman, C. Wilson | 2014 | ACM IMC '14 | DOI 10.1145/2663716.2663758
29. CRLite: A Scalable System for Pushing All TLS Revocations to All Browsers | J. Larisch, D. Choffnes, D. Levin, B. Maggs, A. Mislove, C. Wilson | 2017 | IEEE S&P 2017, pp. 539–556 | dblp conf/sp/LarischCLMMW17
30. Is the Web Ready for OCSP Must-Staple? | T. Chung, J. Lok, B. Chandrasekaran, D. Choffnes, D. Levin, B. Maggs, A. Mislove, J. Rula, N. Sullivan, C. Wilson | 2018 | ACM IMC '18 | DOI 10.1145/3278532.3278543
31. Comprehensive Revocation Checking at Scale: the Deployment of CRLite in Mozilla Firefox | (authors unconfirmed) | 2026 | ACM SIGCOMM 2026 | DOI 10.1145/3789240.3829108 — *see could-not-establish*
32. An Observatory for the SSLiverse | P. Eckersley, J. Burns | 2010 | DEFCON 18 | https://www.eff.org/files/defconssliverse.pdf

**Policy documents**
33. CA/Browser Forum Baseline Requirements for the Issuance and Management of Publicly-Trusted TLS Server Certificates | CA/Browser Forum | current (retrieved 2026-09-26) | CA/B Forum | https://github.com/cabforum/servercert/blob/main/docs/BR.md
34. CA/Browser Forum Baseline Requirements for the Issuance and Management of Publicly-Trusted S/MIME Certificates | CA/Browser Forum | v1.0.0 eff. 2023-09-01 | CA/B Forum | https://github.com/cabforum/smime/blob/main/SBR.md
35. Ballot SC-063v4: Make OCSP Optional, Require CRLs, and Incentivize Automation | CA/Browser Forum SCWG | 2023 (eff. 2024-03-15) | CA/B Forum | https://cabforum.org/2023/07/14/ballot-sc-063-v4make-ocsp-optional-require-crls-and-incentivize-automation/
36. Ballot 105: Technical Constraints for Subordinate Certificate Authorities | CA/Browser Forum | 2013 | CA/B Forum | cabforum.org
37. Mozilla Root Store Policy | Mozilla | current | Mozilla governance | https://www.mozilla.org/en-US/about/governance/policies/security-group/certs/policy/
38. Chrome Root Program Policy v1.8 | Google | current | googlechrome.github.io | https://googlechrome.github.io/chromerootprogram/crp/policy/
39. Common CA Database (CCADB) public reports | Mozilla / CA industry | retrieved 2026-09-26 | CCADB | https://www.ccadb.org/resources

**Incident reports and practitioner sources**
40. Black Tulip — Report of the investigation into the DigiNotar Certificate Authority breach | J. R. Prins et al., Fox-IT B.V. (for Dutch Min. of Interior) | 2012-08-13 | Fox-IT report PR-110202 v1.0 | https://www.enisa.europa.eu/sites/default/files/all_files/Operation_Black_Tulip_v2.pdf
41. Fraudulent *.google.com Certificate | Mozilla Security Team | 2011 | Mozilla Security Blog | https://blog.mozilla.org/security/2011/08/29/fraudulent-google-com-certificate/
42. Revoking Trust in Two TurkTrust Certificates | Mozilla Security Team | 2013 | Mozilla Security Blog | https://blog.mozilla.org/security/2013/01/03/revoking-trust-in-two-turktrust-certficates/
43. Revoking Trust in one ANSSI Certificate | Mozilla Security Team | 2013 | Mozilla Security Blog | https://blog.mozilla.org/security/2013/12/09/revoking-trust-in-one-anssi-certificate/
44. Improved Digital Certificate Security | S. Somogyi, A. Eijdenberg | 2015 | Google Security Blog | https://security.googleblog.com/2015/09/improved-digital-certificate-security.html
45. Chrome's Plan to Distrust Symantec Certificates | D. O'Brien, R. Sleevi, A. Whalley | 2017 | Google Security Blog | https://security.googleblog.com/2017/09/chromes-plan-to-distrust-symantec.html
46. Distrusting WoSign and StartCom Certificates | A. Whalley | 2016 | Google Security Blog | https://security.googleblog.com/2016/10/distrusting-wosign-and-startcom.html
47. Security concerns with the e-Tugra certificate authority | I. Carroll | 2022 | ian.sh | https://ian.sh/etugra
48. Revocation doesn't work | A. Langley | 2011-03-18 | ImperialViolet | https://www.imperialviolet.org/2011/03/18/revocation.html
49. No, don't enable revocation checking | A. Langley | 2014-04-19 | ImperialViolet | https://www.imperialviolet.org/2014/04/19/revchecking.html
50. Revocation checking and Chrome's CRL (CRLSets) | A. Langley | 2012-02-05 | ImperialViolet | https://www.imperialviolet.org/2012/02/05/crlsets.html
51. Revoking Intermediate Certificates: Introducing OneCRL | Mozilla Security Team | 2015-03-03 | Mozilla Security Blog | https://blog.mozilla.org/security/2015/03/03/revoking-intermediate-certificates-introducing-onecrl/
52. Ending OCSP Support in 2025 / OCSP Service Has Reached End of Life | Let's Encrypt (ISRG) | 2024-12-05 / 2025-08-06 | Let's Encrypt blog | https://letsencrypt.org/2024/12/05/ending-ocsp ; https://letsencrypt.org/2025/08/06/ocsp-service-has-reached-end-of-life
53. End of Life Plan for RFC 6962 Certificate Transparency Logs | Let's Encrypt (ISRG) | 2025-08-14 | Let's Encrypt blog | https://letsencrypt.org/2025/08/14/rfc-6962-logs-eol
54. Certificate transparency versions and status of CTv2 (thread; Let's Encrypt engineer statement) | mcpherrinm et al. | 2024–25 | Let's Encrypt Community Forum | https://community.letsencrypt.org/t/certificate-transparency-versions-and-status-of-ctv2/218492
55. Apple's Certificate Transparency policy | Apple Inc. | retrieved 2026 | Apple Support | https://support.apple.com/en-us/103214
56. CVE-2022-3786 and CVE-2022-3602: X.509 Email Address Buffer Overflows | OpenSSL Project | 2022-11-01 | openssl-library.org | https://openssl-library.org/post/2022-11-01-email-address-overflows/
57. CVE-2025-58187, CVE-2025-61727, CVE-2026-27137, CVE-2026-27138, CVE-2026-33810 (Go `crypto/x509` name-constraint defects) | Go Security Team | 2025–2026 | MITRE CVE records | https://cveawg.mitre.org/api/cve/CVE-2025-58187 (etc.)
58. Name Constraints ignored by libPKIX verification engine | K. Engert (rep.), R. Sleevi (analysis) | 2013 | Mozilla Bugzilla #856060 | https://bugzilla.mozilla.org/show_bug.cgi?id=856060
59. Add generic mechanism to add name constraints to built-in certificates | Mozilla/NSS | 2014 (NSS 3.19) | Mozilla Bugzilla #991783 | https://bugzilla.mozilla.org/show_bug.cgi?id=991783
60. x/crypto/x509roots: "TUBITAK Kamu SM SSL Kok Sertifikasi" should be constrained | Go project | 2023 | GitHub golang/go#61963 | https://github.com/golang/go/issues/61963

**Original measurement (this work)**
61. Name-constraint prevalence among CCADB-disclosed intermediate CA certificates | this survey, area B | 2026-09-26 | original measurement | Method: parse all 1,769 PEMs from `https://ccadb.my.salesforce-sites.com/mozilla/MozillaIntermediateCertsCSVReport` with `openssl x509 -noout -text`, count `X509v3 Name Constraints`; root counts from `.../mozilla/IncludedCACertificateReportPEMCSV`. Reproducible; figures drift as CCADB updates.

---

## 3) REQUIREMENTS (extracted from RFC 5280 unless noted)

Format: **verbatim text** | section | verb | actor

### (a) Path validation

| # | Verbatim | Locator | Verb | Actor |
|---|---|---|---|---|
| R-PV-01 | "Conforming implementations of this specification are not required to implement this algorithm, but MUST provide functionality equivalent to the external behavior resulting from this procedure." | RFC 5280 §6 | MUST | conforming implementation |
| R-PV-02 | "A conforming implementation MUST include an X.509 path processing procedure that is functionally equivalent to the external behavior of this algorithm." | §6.1 | MUST | conforming implementation |
| R-PV-03 | "A certificate-using system MUST reject the certificate if it encounters a critical extension it does not recognize or a critical extension that contains information that it cannot process." | §4.2 | MUST | certificate-using system |
| R-PV-04 | "The certificate MUST satisfy each of the following: (1) The signature on the certificate can be verified using working_public_key_algorithm, the working_public_key, and the working_public_key_parameters. (2) The certificate validity period includes the current time. (3) At the current time, the certificate is not revoked. … (4) The certificate issuer name is the working_issuer_name." | §6.1.3(a) | MUST | path-validating implementation |
| R-PV-05 | "If the basic constraints extension is not present in a version 3 certificate, or the extension is present but the cA boolean is not asserted, then the certified public key MUST NOT be used to verify certificate signatures." | §4.2.1.9 | MUST NOT | relying party |
| R-PV-06 | "If certificate i is a version 1 or version 2 certificate, then the application MUST either verify that certificate i is a CA certificate through out-of-band means or reject the certificate." | §6.1.4(k) | MUST | application |
| R-PV-07 | "Conforming CAs MUST include this extension in all CA certificates that contain public keys used to validate digital signatures on certificates and MUST mark the extension as critical in such certificates." (basicConstraints) | §4.2.1.9 | MUST (×2) | conforming CA |
| R-PV-08 | "An implementation MAY augment the algorithm presented in Section 6.1 to further limit the set of valid certification paths that begin with a particular trust anchor." | §6.2 | MAY | implementation |
| R-PV-09 | "Implementations that use self-signed certificates to specify trust anchor information are free to process or ignore such information." *(no RFC 2119 verb — permissive by omission; root-embedded constraints are therefore advisory)* | §6.2 | — (permissive) | implementation |
| R-PV-10 | "The trust anchor information is trusted because it was delivered to the path processing procedure by some trustworthy out-of-band procedure." *(declarative; the trust decision is out of scope)* | §6.1.1(d) | — (declarative) | relying party |

### (b) Name constraints

| # | Verbatim | Locator | Verb | Actor |
|---|---|---|---|---|
| R-NC-01 | "Name constraints may be imposed through explicit inclusion of a name constraints extension in a certificate, but are not required." | §3.2(b) | — (**explicit non-requirement**) | CA |
| R-NC-02 | "The name constraints extension, which MUST be used only in a CA certificate, indicates a name space within which all subject names in subsequent certificates in a certification path MUST be located." | §4.2.1.10 | MUST (×2) | CA / path validator |
| R-NC-03 | "Conforming CAs MUST mark this extension as critical and SHOULD NOT impose name constraints on the x400Address, ediPartyName, or registeredID name forms." | §4.2.1.10 | MUST; SHOULD NOT | conforming CA |
| R-NC-04 | "Conforming CAs MUST NOT issue certificates where name constraints is an empty sequence. That is, either the permittedSubtrees field or the excludedSubtrees MUST be present." | §4.2.1.10 | MUST NOT; MUST | conforming CA |
| R-NC-05 | "Applications conforming to this profile MUST be able to process name constraints that are imposed on the directoryName name form and SHOULD be able to process name constraints that are imposed on the rfc822Name, uniformResourceIdentifier, dNSName, and iPAddress name forms." | §4.2.1.10 | MUST; **SHOULD** | conforming application |
| R-NC-06 | "If a name constraints extension that is marked as critical imposes constraints on a particular name form, and an instance of that name form appears in the subject field or subjectAltName extension of a subsequent certificate, then the application MUST either process the constraint or reject the certificate." | §4.2.1.10 | MUST | application |
| R-NC-07 | "Restrictions apply only when the specified name form is present. If no name of the type is in the certificate, the certificate is acceptable." | §4.2.1.10 | — (**fail-open semantics**) | path validator |
| R-NC-08 | "The syntax and semantics for name constraints for otherName, ediPartyName, and registeredID are not defined by this specification…" | §4.2.1.10 | — (**undefined**) | — |
| R-NC-09 | "In general, using the nameConstraints extension to constrain one name form (e.g., DNS names) offers no protection against use of other name forms (e.g., electronic mail addresses)." | §8 (Security Considerations) | — (**acknowledged gap**) | — |
| R-NC-10 | "In addition, name constraints for distinguished names MUST be stated identically to the encoding used in the subject field or subjectAltName extension. If not, then name constraints stated as excludedSubtrees will not match and invalid paths will be accepted…" | §8 | MUST | CA |
| R-NC-11 | "To avoid acceptance of invalid paths, CAs SHOULD state name constraints for distinguished names as permittedSubtrees wherever possible." | §8 | SHOULD | CA |
| R-NC-12 | "When evaluating name constraints, conforming implementations MUST perform a case-insensitive exact match on a label-by-label basis." | §7.2 | MUST | conforming implementation |
| R-NC-13 | "If permittedSubtrees is present in the certificate, set the permitted_subtrees state variable to the intersection of its previous value and the value indicated in the extension field. If permittedSubtrees does not include a particular name type, the permitted_subtrees state variable is unchanged for that name type." | §6.1.4(g)(1) | (imperative algorithm step) | path validator |
| R-NC-14 *(external)* | "For a TLS Subordinate CA to be Technically Constrained, Name Constraints extension MUST be encoded as follows. As an explicit exception from RFC 5280, this extension SHOULD be marked critical, but MAY be marked non-critical if compatibility with certain legacy applications that do not support Name Constraints is necessary." | CA/B Forum TLS BR §7.1.2.5.2 | MUST; SHOULD; MAY | CA |
| R-NC-15 *(external)* | "Non-critical Name Constraints are an exception to RFC 5280 (4.2.1.10), however, they MAY be used until the `nameConstraints` extension is supported by Application Software Suppliers whose software is used by a substantial portion of Relying Parties worldwide." | CA/B Forum S/MIME BR §7.1.2 fn | MAY | CA |

### (c) Revocation checking

| # | Verbatim | Locator | Verb | Actor |
|---|---|---|---|---|
| R-RV-01 | "However, this profile does not require the issuance of CRLs." | §3.3 | — (**explicit non-requirement**) | CA |
| R-RV-02 | "An entry MUST NOT be removed from the CRL until it appears on one regularly scheduled CRL issued beyond the revoked certificate's validity period." | §3.3 | MUST NOT | CRL issuer |
| R-RV-03 | "At the current time, the certificate is not revoked. This may be determined by obtaining the appropriate CRL (Section 6.3), by status information, or by out-of-band mechanisms." | §6.1.3(a)(3) | (required condition; **method unspecified**) | path validator |
| R-RV-04 | "Conforming CRL issuers MUST include the nextUpdate field in all CRLs." | §5.1.2.5 | MUST | conforming CRL issuer |
| R-RV-05 | "The behavior of clients processing CRLs that omit nextUpdate is not specified by this profile." | §5.1.2.5 | — (**gap**) | client |
| R-RV-06 | "The extension SHOULD be non-critical, but this profile RECOMMENDS support for this extension by CAs and applications." (cRLDistributionPoints) | §4.2.1.13 | SHOULD; RECOMMENDS | CA; application |
| R-RV-07 | "Conforming implementations that support CRLs are not required to implement this algorithm, but they MUST be functionally equivalent to the external behavior resulting from this procedure…" | §6.3 | MUST (conditional on CRL support) | conforming implementation |
| R-RV-08 | "After processing such CRLs, if the revocation status has still not been determined, then return the cert_status UNDETERMINED." | §6.3.3 | — (**terminates without a rule for UNDETERMINED → soft-fail**) | CRL processor |
| R-RV-09 | "CAs SHOULD NOT include URIs that specify https, ldaps, or similar schemes in extensions. CAs that include an https URI in one of these extensions MUST ensure that the server's certificate can be validated without using the information that is pointed to by the URI." | §8 | SHOULD NOT; MUST | CA |
| R-RV-10 *(RFC 6960)* | "Prior to accepting a signed response for a particular certificate as valid, OCSP clients SHALL confirm that: 1. The certificate identified in a received response corresponds to the certificate that was identified in the corresponding request; 2. The signature on the response is valid; 3. The identity of the signer matches the intended recipient of the request; 4. The signer is currently authorized to provide a response for the certificate in question; 5. The time at which the status being indicated is known to be correct (thisUpdate) is sufficiently recent; 6. … nextUpdate … is greater than the current time." | RFC 6960 §3.2 | SHALL | OCSP client |
| R-RV-11 *(RFC 6960)* | "This state does not necessarily mean that the certificate was ever issued or that the time at which the response was produced is within the certificate's validity interval." (the "good" state) | RFC 6960 §2.2 | — (**semantic limitation**) | OCSP client |
| R-RV-12 *(RFC 9608, updates §6.1.3)* | "If the noRevAvail certificate extension specified in this document is present or the ocsp-nocheck certificate extension [RFC6960] is present, then Step (a)(3) is skipped." | RFC 9608 §4 | (updates RFC 5280 §6.1.3) | relying party |
| R-RV-13 *(RFC 9608)* | "Certificates for CAs MUST NOT include the noRevAvail extension. Certificates that include the noRevAvail extension MUST NOT include certificate extensions that point to CRL repositories or provide locations of OCSP responders." | RFC 9608 §3 | MUST NOT | CA |

---

## 4) COULD NOT ESTABLISH

1. **Prior published prevalence statistic for name constraints.** No peer-reviewed measurement paper reporting the fraction of Web PKI intermediates carrying `nameConstraints` was found. I substituted my own measurement (ref. 61); it is reproducible but is a point-in-time CCADB snapshot (2026-09-26) covering **Mozilla-disclosed intermediates only** — not Chrome/Apple/Microsoft stores, not undisclosed or expired CAs, and not enterprise/private PKI (where anecdote suggests name constraints are more common, but I have no data).
2. **Full bibliographic details of the 2026 SIGCOMM CRLite deployment paper** (DOI 10.1145/3789240.3829108). ACM DL returned HTTP 403. The 87.8%-coverage figure and "only broadly deployed comprehensive revocation mechanism" claim come from a search-engine summary; treat as provisional.
3. **Verbatim text of CA/B Forum ballots SC-063 and SC-081.** cabforum.org ballot pages would not render. Passage/effective dates for SC-063 are corroborated by multiple independent secondary sources plus the BR revision table; SC-081's short-lived-certificate revocation exemption is secondary-sourced only.
4. **Current (2022–2026) OCSP stapling deployment rate.** The most recent hard figures remain 2015 (Liu et al., ~6–7%) and 2018 (Chung et al., 0.02% Must-Staple). No remeasurement located. Note this is partly moot now that Let's Encrypt has shut OCSP down.
5. **Whether TÜBİTAK's `*.tr` "Mozilla Applied Constraints" value is actually enforced in production NSS** via `CERT_GetImposedNameConstraints`, versus being CCADB disclosure metadata. I verified the CCADB value directly (1 of 172 roots); I could not verify the enforcement path. Go's bundle demonstrably does not carry it.
6. **No Dutch (PKIoverheid) or Taiwanese case of out-of-band imposed name constraints exists**, contrary to the brief's hypothesis. The verified out-of-band cases are ANSSI (Mozilla/NSS mechanism, bug 991783) and India CCA (Chrome/CRLSet domain restriction, 2014 — a Chrome-specific mechanism, not RFC 5280 name constraints). TURKTRUST (2013) is a real incident but is the *origin* of the CA/B Forum's technically-constrained-sub-CA rule, not an example of imposed constraints.
7. **No Hanno Böck or Ivan Ristić piece specifically on name-constraint obstacles** was located. Do not attribute that commentary to them. The best-sourced practitioner evidence is Ryan Sleevi's diagnosis in Mozilla Bugzilla #856060 and the CA/B Forum's own BR exception text (R-NC-14, R-NC-15), which I verified verbatim.
8. **No Java/JSSE name-constraint CVE** was located, in contrast to Go and OpenSSL. Absence of evidence only.
9. **The "~30,000 misissued Symantec certificates" figure** is a press/community aggregate, not a single official audit total. Symantec's own audits reported 23 certs, then a further 164 across 76 domains plus 2,458 for unregistered domains.
10. **Firm state attribution for DigiNotar/Comodo.** Fox-IT stops at "a perpetrator located in the Islamic Republic of Iran." Treat stronger claims as contested.
11. **RFC 6962 does not contain an explicit "any CA can issue for any domain" sentence.** Do not cite it for that. Use EFF's SSL Observatory ("1 of N CAs (N is large)") or certificate.transparency.dev. For detection-vs-prevention, RFC 9162 §1 gives a clean primary quote (used above).
12. **Exact Apple/Opera DigiNotar removal dates** — only Microsoft, Mozilla and Google dates are primary-sourced.

---

### Two corrections to assumptions in the brief
- **CVE-2021-3450 is not a name-constraints bug.** It is an OpenSSL `X509_V_FLAG_X509_STRICT` flaw that overwrote the result of the prior CA-validity check. Do not cite it in the name-constraints section.
- **RFC 9162 is Experimental and effectively undeployed.** Framing it as "the current CT standard" would be inaccurate; RFC 6962 v1 plus the non-IETF Static CT API / Sunlight spec is what actually runs.

### Note for the survey editor
My CCADB root-store count (121 TLS-trusted roots) independently matches the figure another area's research produced, which is a useful cross-check. Both are point-in-time (2026-09-26) and should be cited with a retrieval date.

### Note on side effects
No files were written into the project repository. All downloads and analysis scripts live in the session scratchpad (`/private/tmp/claude-502/.../scratchpad`): the RFC texts, `BR.md`, `SBR.md`, `interm.csv` and `roots.csv` are there if you want to re-run the measurement.
