# Unverified claims register

Every research lane was instructed to return, alongside its findings, an
explicit account of what it **could not** establish. Those accounts are
collated here verbatim, for all eight areas.

This file is a **publication gate**, not a to-do list. The rule:

> No claim appearing below may be stated as fact in `report.md` until it has
> been verified against a primary source and the source ingested into
> `library/`. A claim that cannot be verified is either cut, or stated in the
> paper as contested with the uncertainty named.

This exists because the cheapest way to lose an academic paper's credibility is
a confidently-worded sentence resting on a search-result summary. Several lanes
exhausted their web-search budget mid-task, so some entries are gaps in effort
rather than gaps in the record — they are recoverable, and the register says
which are which.

Some entries are **corrections to claims the drafting brief assumed**, not just
absences. Area B, for example, establishes that CVE-2021-3450 is *not* a
name-constraints bug and that RFC 9162 is effectively undeployed; area F
establishes that there is no CVE for SUNBURST. Those are recorded here because
getting them wrong would have been worse than omitting them.


## A — Foundations — Contested attributions (flag these in the paper)

*Source: `mini-reports/A-foundations.md`*

1. **Priority for public-key cryptography vs. priority for the signature idea.** GCHQ's James Ellis (1970, "non-secret encryption"), Clifford Cocks (1973, an RSA-equivalent) and Malcolm Williamson (1974, a DH-equivalent key exchange) anticipated the *encryption and key-exchange* halves of Diffie–Hellman; this was declassified in 1997. Multiple accounts — including Schneier's history and the standard teaching literature — state that the GCHQ work did **not** conceive digital signatures. Ralph Merkle's public-key distribution work was also submitted (Aug 1975) before Diffie–Hellman was published, appearing in CACM in April 1978. The upshot: the *signature* idea is the part of "New Directions" whose priority is not contested.
2. **"First digital signature algorithm."** Lamport's construction appears in Diffie–Hellman §4 (1976) credited to Lamport, three years before Lamport's CSL-98. Lamport's own account credits Diffie with posing the problem around 1975. Rabin's 1978 "Digitalized Signatures" chapter also contains a one-time scheme. Any flat claim of "first" needs qualifying.
3. **"Rabin 1979 was the first EUF-CMA-secure scheme."** Asserted on Wikipedia and repeated widely. It is a retrospective reading — the definition post-dates the scheme by nine years — and it depends on reading Rabin's randomized suffix as achieving the later notion. Do not state it as established.
4. **Schnorr's patent claim against DSA.** Schnorr asserted that U.S. Patent 4,995,082 read on DSA. NIST reviewed the asserted patents and concluded DSS infringed none. The dispute was never judicially resolved; DSA itself is covered by U.S. Patent 5,231,668 (filed 26 Jul 1991, David W. Kravitz, assigned to the U.S. and licensed royalty-free). Both patents have expired.

---


## A — Foundations — Could not establish

*Source: `mini-reports/A-foundations.md`*

- **A DOI for FIPS 186-1 and FIPS 186-3.** Neither is registered in Crossref, and neither NIST CSRC landing page lists one. The CSRC permalinks above are the best stable identifiers available. (FIPS 186, 186-2, 186-4 and 186-5 *do* resolve under 10.6028.)
- **A DOI or stable digital identifier for Rabin (1978), "Digitalized Signatures," in *Foundations of Secure Computation*.** The page range 155–168 is widely cited but I could not verify it against a primary source or publisher record; treat the pagination as unconfirmed.
- **Exact page range for FIPS 186-5's Federal Register notice** beyond the cited FR volume/number (88 FR, No. 23, 3 Feb 2023); the govinfo permalink is reliable but I did not confirm the page span.
- **Merkle, "Protocols for Public Key Cryptosystems" end page.** Crossref records "122–122"; secondary sources give 122–134 and 122–136. The start page 122 is certain; the end page is not.
- **Merkle's 1979 thesis page range for the tree-authentication material** (commonly cited as pp. 32–61) — seen in secondary sources only, not verified against the thesis itself.
- **Whether Rabin's TR-212 has a canonical DTIC vs. MIT DSpace citation preference.** Both exist (DTIC ADA078415; MIT DSpace 1721.1/149499); I used the MIT handle as primary.
- **Research budget note:** the session's web-search quota (200 calls) was exhausted at the end of this pass. Remaining gaps above were not for want of effort but would need a fresh search budget or direct library/publisher access to close.


## B — X.509 / PKIX — 4) COULD NOT ESTABLISH

*Source: `mini-reports/B-x509-pkix.md`*

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


## B — X.509 / PKIX — Two corrections to assumptions in the brief

*Source: `mini-reports/B-x509-pkix.md`*

- **CVE-2021-3450 is not a name-constraints bug.** It is an OpenSSL `X509_V_FLAG_X509_STRICT` flaw that overwrote the result of the prior CA-validity check. Do not cite it in the name-constraints section.
- **RFC 9162 is Experimental and effectively undeployed.** Framing it as "the current CT standard" would be inaccurate; RFC 6962 v1 plus the non-IETF Static CT API / Sunlight spec is what actually runs.


## C — Decentralised naming — COULD NOT ESTABLISH

*Source: `mini-reports/C-decentralised-naming.md`*

- **Exact conclusion date of the IETF SPKI working group.** Datatracker records WG state "Concluded" and charter state "Approved," last updated **2001-02-10**, but publishes no explicit conclusion date; secondary sources say only "around 2001." The 2001-02-10 timestamp should be cited as *charter last-updated*, not as the conclusion date.
- **DOIs for RFC 9580 and RFC 9804.** The rfc-editor info pages I fetched did not display them. RFC DOIs follow the `10.17487/RFCxxxx` pattern, but I did not verify these two specifically — cite by RFC number/URL.
- **HP eSpeak's use of SPKI certificates for delegated access control.** This appeared in a search summary but Carl Ellison's primary page (`theworld.com/~cme/html/spki.html`) is no longer resolvable, and I found no citable primary source. **Do not use this claim without an independent source** — it is the single most-repeated "SPKI shipped somewhere" assertion and I could not substantiate it.
- **Whether UCAN is genuinely in production at Storacha/web3.storage.** The documentation URL 301-redirects to `fil.one`, whose page makes no mention of UCAN, DIDs, delegation or attenuation. Fly.io's macaroon use is the one production attenuation deployment I verified directly.
- **Adoption rate of OpenPGP trust signatures.** Ulrich et al. (2011) measure the signature graph but report no figure for how many keys carry type-5 Trust Signature subpackets or regex scoping. I found no study that measures this. The argument in §2 rests on spec/tooling analysis plus the graph data, not on a direct measurement of tsign usage.
- **Verbatim text of Zooko's 2001 post.** `web.archive.org` is blocked in this environment; the title, date and formulation are taken from the Wikipedia article's citation of the archived page. Verify against the archive before quoting.
- **Current Let's Encrypt headline figures** (active certificates / FQDNs). The stats page (last updated 24 Sept 2026) renders its numbers client-side and returned no figures. §8(e)'s argument does not depend on a specific number, but if the survey wants one, it needs a separate source.
- **Whether any browser or operating system ever shipped SPKI/SDSI certificate validation.** I found no evidence either way; I assert only the absence of a trust-anchor installation path, which follows from the format never being standardised. Phrased as "no path to integration" rather than "was rejected by vendors."
- **DID v1.1's status as of today (2026-09-26).** Verified only as a Candidate Recommendation Snapshot dated 5 March 2026, with the note that it was not expected to advance before 5 April 2026; `https://www.w3.org/TR/did/` still resolves to the 1.0 Recommendation of 19 July 2022. Whether 1.1 has since become a Recommendation is unconfirmed.

*(Report body: ~1,470 words.)*

Note on method: the WebSearch budget for this session was exhausted (200/200) partway through; the remaining verification was done by direct WebFetch and by downloading and parsing RFC/paper text locally. All RFC facts above come from the fetched RFC text itself, not from search summaries.


## D — Content labelling — COULD NOT ESTABLISH

*Source: `mini-reports/D-content-labelling.md`*

1. **Authors of the CSCW provenance-trust study (ref. 20).** I verified the findings, N=595, venue (PACM HCI / CSCW) and DOI 10.1145/3610061, but did not retrieve the author list — ACM DL returned HTTP 403 and my web-search budget ran out. The arXiv abstract page would settle it in one fetch.
2. **Exact release date of C2PA 2.4.** The spec page itself says only "Version 2.4, April 2026"; the 2.4 index page carries no publication date; Wikipedia gives 21 April 2026. Not confirmed from a C2PA primary source (no 2.4 press release found).
3. **Whether a UX Recommendations 2.3 or 2.4 exists.** The 2.4 index links "User Experience Guidance" at **2.2**. I treat the UX document as frozen at 2.2, but cannot rule out an unlinked newer draft.
4. **Content of the new 2.4 "Attestations" and "Soft Binding API" documents.** Listed in the 2.4 suite; not read. The Attestations spec may bear on the third-party-assessment gap I identify in §7 and should be checked before that claim is published.
5. **ISO standardisation of C2PA.** Frequently asserted informally; no primary evidence found. JUMBF's ISO status (19566-5:2023) *is* established, via C2PA's own normative reference.
6. **Platform and newsroom adoption specifics.** Claims about BBC, AFP, Reuters, AP, France Télévisions, LinkedIn, TikTok ("3 billion videos labelled"), YouTube, Meta and X came only from SEO-farm aggregators (softwareseni.com, c2paviewer.com, editorsweblog.org, eyesift.com) with no primary citation. **Do not publish these without primary sourcing.** The camera-manufacturer facts (Leica M11-P, Sony, Canon, Nikon revocation, Pixel 10) and the "6,000 members and affiliates" figure are better sourced (Wikipedia + C2PA's own announcement) but the latter is self-reported.
7. **Outcome of the W3C TAG obsoletion proposal.** Issue #86 was still open and "Awaiting AC Vote" at the time of my fetch; I could not determine whether PICS/POWDER were ever formally obsoleted (as distinct from PICS being "Retired" on 24 Nov 2009).
8. **A quantitative count of PICS-labelled pages.** The GVU 1998 webmaster survey gives self-reported labelling rates; I found no crawl-based measurement of how much of the web actually carried PICS labels.
9. **Direct quotation of C2PA 2.4 §18 in full.** My assertion-label list is from a summarising fetch of the spec, not a verbatim extract of Chapter 18. The claim "the vocabulary is enumerated in the spec" is solid (§6.2.2 is quoted), but the exact label list should be re-checked against Chapter 18 before publication.
10. **Whether PICS labels for third-party bureaus were ever deployed at meaningful scale.** The protocol is specified; I found no evidence of a production label bureau serving third-party labels.


## E — Device attestation — COULD NOT ESTABLISH

*Source: `mini-reports/E-device-attestation.md`*

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


## F — Software supply chain — COULD NOT ESTABLISH

*Source: `mini-reports/F-supply-chain.md`*

1. **ISO stage of SPDX 3.0.** An ISO catalogue entry "ISO/IEC DIS 5962 — SPDX® Specification V3.0" appears to exist (iso.org/standard/93810.html), but iso.org blocks automated fetch (403). The live stage code, ballot dates, and whether it has advanced to FDIS or publication are unverified. **Do not assert a publication date for an ISO SPDX 3.0 standard.** ISO/IEC 5962:2021 (V2.2.1) is the only confirmed published ISO SPDX standard.
2. **CycloneDX ISO/IEC status — negative finding, not exhaustively verified.** No ISO/JTC 1 reference found on the Ecma ECMA-424 page or tc54.org, and no JTC 1 fast-track/PAS record was located, but the JTC 1 registers were not swept. Safe phrasing: "standardized as ECMA-424 (Ecma International, TC54); as of this writing it carries no ISO/IEC designation."
3. **CISA 2026 Minimum Elements — field list not extracted.** Title, date (2026-07-29), authoring bodies, final status and explicit supersession of NTIA 2021 are confirmed; CISA's document host returned 403, so the actual new data fields and practices are unverified. Do not cite specific 2026 fields.
4. **Venue for Okafor, Davis & Torres-Arias (DOI 10.1145/3832783.3834333).** The arXiv record lists this ACM DOI, but it resolves in neither Crossref nor OpenAlex, so the conference could not be identified. Cite as arXiv:2406.15596 with the DOI noted.
5. **Notary Project / Notation trust model.** The CNCF page confirms Incubating status (accepted 2017-10-24) but carries no technical detail, and notaryproject.dev's docs index did not state definitively whether Notation uses X.509 trust stores rather than TUF, nor spell out the Notary v1 → v2 relationship. The trust-store/trust-policy characterization above is from the docs' structure, not from a normative specification statement. Verify against the Notary Project signature specification before printing.
6. **SpellBound: Defending Against Package Typosquatting** (arXiv:2003.03471) — title, authors and abstract verified; **no peer-reviewed venue or DOI confirmed.** Treat as a preprint.
7. **CrowdStrike SUNSPOT blog publication date.** Technical content fully verified; the date could not be extracted (Wayback 504, no date on the live page). Commonly given as 11 Jan 2021 — verify before printing.
8. **FireEye disclosure date conflict.** The original post reads 13 Dec 2020; Google Cloud's republished copy reads 12 Dec 2020 (a Mandiant→Google migration artifact). Cite 13 Dec 2020 and consider a footnote.
9. **event-stream attacker aliases.** Only `right9ctrl` (npm/GitHub account) and `hugeglass` (the GitHub org hosting flatmap-stream) are evidenced from primary sources. **No primary source was found connecting "right-ventricle" or "Hydro-Ja" to this incident** — recommend dropping both from the survey.
10. **No CVE exists for SUNBURST or SUNSPOT.** Do not cite CVE-2020-10148 as "the SolarWinds CVE"; it is the separate Orion API auth bypass tied to SUPERNOVA (CVSS 3.1 9.8).
11. **The "18,000" figure** is a vendor self-estimate of *potential exposure* ("fewer than 18,000... may have had an installation... that contained this vulnerability"), not confirmed compromises. No figure for second-stage victims was verified.
12. **`build-to-host.m4`** is named in Freund's oss-security disclosure, **not** in Tukaani's own upstream statement — attribute the filename to Freund.
13. **Ohm et al.'s 61% typosquatting** is a proportion of their curated 174-package attack dataset, not of npm or PyPI at large. Phrase carefully.
14. **JiaT75 first-commit date** — GitHub API author-date gives 2022-01-28; Russ Cox's timeline gives 2022-02-07 for the first merged commit. Both defensible; footnote the basis.
15. **NIST SP 800-161r1 exact day of original publication** (May 2022 confirmed; day-of-month not verified).
16. **Method caveat:** this session exhausted its web-search budget (200/200 calls) partway through. Later items were verified by direct fetch of authoritative URLs, government APIs (Federal Register, NVD, Crossref, OpenAlex), the EU Publications Office CELLAR endpoint, and project source repositories via `gh`/`curl`. No claim in the report rests on a search-result snippet alone. Two domains (iso.org, cisa.gov asset host) refused automated fetch entirely — see items 1 and 3.


## G — Capability and delegation — COULD NOT ESTABLISH

*Source: `mini-reports/G-capability-delegation.md`*

1. **Mark S. Miller, *Robust Composition* (2006).** Cited secondhand — draft-niyikiza §1.3 lists "capability-based security (Dennis 1966, Miller 2006)". I could not fetch the thesis itself: erights.org and combex.com both refused connections during this session. Full citation (Johns Hopkins University PhD thesis, 2006) is from memory and should be re-verified before use.
2. **Miller, Yee, Shapiro, "Capability Myths Demolished."** Standard reference for object-capability vs. ACL comparison and the confused-deputy analysis. Host `srl.cs.jhu.edu` no longer resolves (DNS failure), and the session's web-search budget (200 calls) was exhausted before I could find a mirror. Year (2003) and report series (SRL2003-02) are unverified.
3. **Macaroons DOI.** NDSS Symposium papers carry no DOI. The stable identifiers are the NDSS programme page and the authors' PDF, both listed above.
4. **ZCAP editors and date for v0.4.0-rc.6.** The rendered spec page I fetched did not list editors or a publication date. A search snippet attributed v0.3 to Lemmer-Webber, Sporny and M. S. Miller with date 2023-01-22, but I could not confirm this from the document itself. Also note ZCAP has *never* been a W3C Recommendation — it is a CCG work item, and the survey should say so.
5. **Biscuit authorship/provenance.** The specification site names no individual authors and does not state the originating organization. The project is now under Eclipse; secondary sources attribute its origin to Clever Cloud, which I could not confirm from a primary source.
6. **draft-asor's treatment of subject identity.** My claim that it does not mention DIDs, SPIFFE or workload identity rests on a single summarization pass over the draft HTML, not a full read. Given it is a WIMSE-adjacent draft using proof-of-possession, treat "binds hops to keys but defines no naming layer" as the defensible statement and re-read §§1–4 before asserting the stronger version.
7. **UCAN quadratic token growth.** Sourced to Prakash 2026 (arXiv:2603.24775), a non-peer-reviewed preprint, as a secondary claim. I found no independent measurement, and the growth characteristic differs between UCAN 0.x (nested JWT, the version the criticism targets) and UCAN 1.0 (DAG-CBOR envelopes with CID-referenced proofs, which should be linear). The survey should scope the criticism to 0.x explicitly.
8. **Whether any deployed system computes a true meet.** I checked macaroons, Biscuit, UCAN, ZCAP, and all three 2026 drafts, and found only containment/subsumption checking. I did not exhaustively survey every capability token system (e.g. Tahoe-LAFS, Waterken, CapBAC/ACE-OAuth, Google's internal successors), so "nothing does intersection" should be stated as "none of the systems surveyed here," not as a universal claim.


## H — Post-quantum — COULD NOT ESTABLISH

*Source: `mini-reports/H-post-quantum.md`*

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
