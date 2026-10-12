---
schema: "library-doc/v1"
id: R-0004-sources
title: "Sources consulted — uptake and applications"
type: evidence
status: draft
version: "0.1.0"
date: "2026-10-10"
updated: "2026-10-10"
---

# Sources

All retrievals **2026-10-10 (PT)** unless noted. Each row below was fetched
over HTTP in this research pass. Search-index snippets were used only to locate
URLs; **no claim in `report.md` rests on a snippet alone.**

Bibliography pinned at **`library@93891c9`**. Rows marked **record** already
resolve to a library record at that commit and are cited in `report.md` as
`[@id]`. Rows marked **fresh** were retrieved for this report and have no
record yet, or have only a stub — they are cited by URL and are listed in §4 as
ingestion candidates.

## 1. Retrieved for this report — primary

| Source | URL | Status | What it settled |
|---|---|---|---|
| C2PA Conformance Program and Trust List | https://c2pa.org/conformance/ | **stub record** `c2pa-conformance-program` | Program "provides assurance that products adhere to the Content Credentials specification"; covers generator products, validator products and CAs. C2PA Trust List launched mid-2025 with "a new public Certificate Policy which specifies C2PA requirements for CAs". Interim Trust List **frozen 1 January 2026**; "Existing certificates will remain valid for legacy support." Separate TSA trust list. Conforming products are "placed on a publicly-accessible list" which "guarantees interoperability". **No count published on the page.** |
| C2PA, *Content Credentials Deployment Guidance* (PDF, July 2026) | https://c2pa.org/wp-content/uploads/sites/33/2026/07/Content-Credentials-Deployment-Guidance.pdf | **fresh** | **"Since its launch, 54 products from 31 companies have passed conformance (as of May 14, 2026)."** Program launched 4 June 2025. "over 120 additional companies have submitted expressions of interest". "expects the number of assessed products to drastically increase over time". "there is a queue to go through the conformance program at the time this document was written". "not all C2PA implementations have gone through the Conformance program". Re-export/screenshot "can strip the embedded Content Credentials"; durable credentials combine watermarking and fingerprinting. DVIDS compared to how "LinkedIn and YouTube display Content Credentials". |
| C2PA official Trust List (PEM) | https://raw.githubusercontent.com/c2pa-org/conformance-public/refs/heads/main/trust-list/C2PA-TRUST-LIST.pem | **fresh** | The measurement in `report.md` §4.3. 37,911 bytes. sha256 `75cacc98b79ecac33713c7ecfb58d4a0ef383f3c1f886e7409f9e37e8664aea5`. 30 certificates, 17 organisations, 19 self-signed roots, 11 intermediates. Full subject listing in §3 below. |
| SLSA, *Mini Shai-Hulud: Where SLSA's Boundaries Fall* (May 2026) | https://slsa.dev/blog/2026/05/mini-shai-hulud-what-slsa-can-and-cannot-do | **stub record** `slsa-2026-mini-shai-hulud` | 84 compromised package builds across 42 `@tanstack` packages, 11 May 2026; worm spread to 170+ packages across `@mistralai`, `@uipath` and others. Chain: `pull_request_target` pwn request → Actions cache poisoning across trigger scopes → OIDC token scraped from runner memory with `id-token: write`. **"Both malicious runs ended with `status: failure`"** and packages were published anyway. **"Standard SLSA consumer tooling does not check workflow run status."** "An 'expected builder' check would have passed, because the pipeline was legitimate." "SLSA provenance records evidence. It answers 'what happened?'" / "Policy and verification answer 'was that good enough?'" "an attacker who fully controls code inside a trusted builder on the expected ref can still produce conforming provenance." "The boundary of observability is the boundary of the trust context." |
| Content Authenticity Initiative, *The State of Content Authenticity in 2026* | https://contentauthenticity.org/blog/the-state-of-content-authenticity-in-2026 | **fresh** | Published 18 January 2026, Andy Parsons. CAI is "a community of more than 6,000 members". Google Pixel 10 supports C2PA credentials; Sony PXW-Z300 brings Content Credentials to high-end video capture; Adobe Content Authenticity for Enterprise. CAWG 1.2 released. C2PA Conformance Explorer tracks "a growing cohort of Conforming Products" — **no number given**. Membership is advocacy-initiative membership, not deployment; reported as such in `report.md` §4.2. |
| npm registry search API | https://registry.npmjs.org/-/v1/search | **fresh** | Sampling frame for the §3.2 measurement. Exact query strings in `searches.md`. |
| npm registry package metadata | https://registry.npmjs.org/&lt;package&gt; | **fresh** | `dist-tags.latest` → `versions[latest].dist.attestations` is the provenance test used in §3.2. |
| Trusted Publishers for PyPI | https://docs.pypi.org/trusted-publishers/ | **stub record** `pypi-trusted-publishers` | Cited in `report.md` §3.4 for the pattern R-001 §8.5 establishes. Not re-analysed in this pass beyond confirming the URL resolves. |

## 2. Carried from survey R-001, not re-retrieved

`report.md` reuses R-001's structural analysis of SPKI (§5.5, §5.7), PICS
(§6.1–6.2), C2PA's vocabulary binding (§6.5), human factors (§6.6), and the
supply-chain entitlement gap (§8.4–8.7). Those sections cite library records
directly and were **not** re-retrieved here; R-001 is merged and its citations
resolve at `library@93891c9`. The records relied on, by key:

`aclu-fahrenheit-451-2`, `pics-censorship-faq`, `pics-1-1-labels`,
`pics-1-1-services`, `pics-dsig-1-0`, `gvu-1998-webmaster-survey`,
`powder-description-resources`, `w3c-tag-obsolete-powder`,
`draft-ietf-spki-cert-structure`, `ietf-spki-wg`, `rfc-2693`,
`wang-2006-reducing-spki`, `ellison-schneier-2000-ten-risks`, `rfc-3820`,
`rfc-8555`, `rfc-9162`, `c2pa-2-4`, `c2pa-ux-2-2`, `cawg-identity-1-2`,
`cscw-2023-provenance-trust`, `moruzzi-2025-content-authenticities`,
`ide-2025-signals-of-provenance`, `eu-ai-act-art-50`, `ca-sb-942`,
`eu-code-of-practice-marking`, `nsa-2025-content-credentials`,
`eu-cra-2024-2847`, `eo-14028`, `eo-14144`, `eo-14306`,
`ntia-2021-sbom-minimum`, `cisa-2026-sbom-minimum`, `iso-iec-5962-2021`,
`spdx-3-0-1`, `cyclonedx-1-7`, `in-toto-2019`, `in-toto-attestation-v1`,
`secure-systems-lab-dsse`, `slsa-1-2`, `sigstore-2022`, `sigstore-threat-model`,
`tuf-spec`, `tuf-2010`, `gittuf-2025`, `rfc-9942`, `rfc-9943`,
`draft-mih-scitt-agent-action-capsule`,
`draft-asor-wimse-agent-delegation-chain`, `draft-hamr-oauth-agent-delegation`,
`draft-niyikiza-oauth-attenuating-agent-tokens`, `ucan-1-0`,
`biscuit-spec-3-3`, `zooko-2001-names`, `w3c-did-core`, `did-key-method`.

## 3. Measurement outputs

### 3.1 C2PA Trust List — full subject listing

Retrieved 2026-10-10. File sha256
`75cacc98b79ecac33713c7ecfb58d4a0ef383f3c1f886e7409f9e37e8664aea5`.
Split with `awk` on `BEGIN CERTIFICATE`; subjects read with
`openssl x509 -noout -subject -enddate`. Sorted.

```
C=CN, O=Huanyu Trust Ltd, CN=Huanyu Trust C2PA EC-384 Root CA            notAfter=Apr 13 2051
C=CN, O=Huawei Technologies Co., Ltd., CN=HUAWEI C2PA ECC384 Root CA E346 notAfter=Apr  8 2046
C=CN, O=Snowball Technology Co., Ltd., CN=Snowball ECC P384 Claim Signing ICA for C2PA G1  notAfter=Jun 19 2031
C=CN, O=Snowball Technology Co., Ltd., CN=Snowball ECC P384 Root CA for C2PA G1            notAfter=Jun 13 2046
C=CN, O=TrustAsia Technologies, Inc., CN=TrustAsia C2PA ECC Root CA      notAfter=Jun  5 2051
C=CN, O=TrustAsia Technologies, Inc., CN=TrustAsia C2PA RSA Root CA      notAfter=Jun  5 2051
C=CN, ST=Beijing, L=Beijing, O=Xiaomi Inc., CN=Xiaomi Root CA(EC-P384)   notAfter=Sep 19 2050
C=NL, O=Irdeto BV, CN=Irdeto C2PA Root CA G1                             notAfter=Dec  5 2050
C=US, O=DigiCert, Inc., CN=DigiCert ECC P384 L1 Claim Signing ICA for C2PA G1  notAfter=Aug 26 2030
C=US, O=DigiCert, Inc., CN=DigiCert ECC P384 Root for C2PA G1            notAfter=Aug 26 2050
C=US, O=DigiCert, Inc., CN=DigiCert RSA4096 L1 Claim Signing ICA for C2PA G1   notAfter=Aug 26 2030
C=US, O=DigiCert, Inc., CN=DigiCert RSA4096 Root for C2PA G1             notAfter=Aug 26 2050
C=US, O=Google LLC, CN=Google C2PA Media Services 1P ICA G3              notAfter=May  8 2030
C=US, O=Google LLC, CN=Google C2PA Mobile A 1P ICA G3                    notAfter=May  8 2030
C=US, O=Google LLC, CN=Google C2PA Mobile A 1P ICA G3 L1                 notAfter=May  8 2030
C=US, O=Google LLC, CN=Google C2PA Mobile B 1P ICA G3                    notAfter=May  8 2030
C=US, O=Google LLC, CN=Google C2PA Mobile B 1P ICA G3 L1                 notAfter=May  8 2030
C=US, O=Google LLC, CN=Google C2PA Root CA G3                            notAfter=May  8 2050
C=US, O=Whole Earth Labs LLC, CN=RealReel C2PA Root CA                   notAfter=Jul 24 2051
C=US, ST=California, L=San Francisco, O=Encypher Corp., CN=Encypher C2PA Issuing CA 2026   notAfter=May 23 2031
C=US, ST=California, L=San Francisco, O=Encypher Corp., CN=Encypher C2PA Root CA 2026      notAfter=May 17 2046
C=US, ST=New York, L=New York, O=Tauth Labs Inc., CN=Tauth Root CA       notAfter=Dec 31 2045
C=US, ST=New York, L=New York, O=Trufo Inc., CN=Trufo C2PA Root CA (2025, ECC P384)        notAfter=Dec 25 2045
C=US, ST=Washington, O=Verimago LLC, CN=Verimago Claim Signing Issuing CA notAfter=May 15 2031
C=US, ST=Washington, O=Verimago LLC, CN=Verimago Root CA                 notAfter=May 15 2046
CN=Adobe Product Issuing CA vault-a-or2.adobe.net cai, O=Adobe Inc, C=US notAfter=Nov 20 2030
CN=Castlabs C2PA ECC P-384 Root CA, C=DE, O=Castlabs                     notAfter=Jul  5 2036
CN=SSL.com C2PA ECC Root CA 2025, O=SSL Corporation, C=US                notAfter=Jul 12 2050
CN=SSL.com C2PA RSA Root CA 2025, O=SSL Corporation, C=US                notAfter=Nov  1 2050
CN=vivo Content Provenance and Authenticity Root CA, O=vivo Mobile Communication Co., Ltd., C=CN  notAfter=Sep 11 2055
```

Derived: **30** certificates · **17** organisations · **19** self-signed roots ·
**11** intermediates · `C=US` 20, `C=CN` 8, `C=NL` 1, `C=DE` 1. Google holds 6
certificates, DigiCert 4. Three organisations — DigiCert, SSL Corporation
(SSL.com) and TrustAsia — are incumbent WebPKI certificate authorities.

### 3.2 npm provenance — measurement parameters and result

Run 2026-10-10. Sampling frame: npm registry search API, three queries (the
fourth, `text=*`, returned HTTP 400 and was dropped — see `searches.md`), each
`size=250&popularity=1.0&quality=0.0&maintenance=0.0`, deduplicated by package
name keeping the highest popularity score, truncated to the top 300.

Provenance test: fetch `https://registry.npmjs.org/<name>`, read
`dist-tags.latest`, test `versions[latest].dist.attestations` for presence.
Concurrency 8, three retries with backoff, custom User-Agent.

| measure | value |
|---|---|
| packages sampled | 300 |
| latest version carries provenance | 100 (**33.3%**) |
| no provenance | 200 |
| fetch errors | 0 |
| distinct publishing scopes in sample | 242 |
| scopes with any provenance | 56 (**23.1%**) |
| provenance packages from the 5 largest scopes | 40 |

Concentration in the provenance set: `@inquirer` 16, `@oxc-parser` 9,
`@appium` 6, `@jsonjoy.com` 5, `@oxlint` 4, `@supabase` 3, `@oxfmt` 3,
`@astrojs` 3, `@typescript-eslint` 2, `@hey-api` 2.

**Reproduction.** The measurement script and the 300-row result set are not
committed (they are a one-off and the registry is live). The method above is
sufficient to repeat it; the numbers will drift as the registry does, and any
repetition should record its own date.

## 4. Ingestion candidates

Filed as follow-on work in `report.md` §10. None blocks this report, because
each is cited by URL with a retrieval date here.

| Source | Why it should be a record | `bears_on` |
|---|---|---|
| C2PA *Content Credentials Deployment Guidance* (PDF) | The only primary publication of conformance counts | D9, R-0004 |
| C2PA official Trust List PEM | The measured root of trust; digest-pinned, drifts | D9, R-0004 |
| CAI *State of Content Authenticity in 2026* | Primary for CAI membership and 2025–26 product launches | D9 |
| npm registry provenance endpoint behaviour | The `dist.attestations` field is the measurement surface | D9 |

**Upgrade, not create** — `c2pa-conformance-program`,
`slsa-2026-mini-shai-hulud` and `pypi-trusted-publishers` are existing stub
records. Per `library/CLAUDE.md`, filling a stub to summary level is ingestion
held to the summary bar, not FX-1. Record the digest and locator; **do not
commit the PDF bytes.**
