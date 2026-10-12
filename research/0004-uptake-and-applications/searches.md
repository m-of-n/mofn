---
schema: "library-doc/v1"
id: R-0004-searches
title: "Searches — uptake and applications"
type: evidence
status: draft
version: "0.1.0"
date: "2026-10-10"
updated: "2026-10-10"
---

# Searches

Queries run **2026-10-10**, verbatim, in order. Yield is the URL that was then
fetched, or an **explicit miss**. Snippets were not treated as evidence.

Wohlin snowballing requires each iteration's yield to be recorded as it
happens; this file exists because that is impossible retroactively
(`research/README.md`). The misses are the half that is usually lost, and three
of them below changed what `report.md` claims.

## 1. Web search

| # | Query | Mode | Yield |
|---|---|---|---|
| 1 | `Sigstore Rekor transparency log total entries npm provenance adoption statistics 2026` | extended | **Miss for the intended fact.** No primary total for Rekor entries and no 2026 npm provenance rate. Nine results, all secondary. A blog claim of "over a billion artifacts signed through Rekor as of 2025" was not verifiable against a Sigstore publication → `unverified.md`. Rekor v2 GA (Oct 2025, tile-backed, year-sharded) appeared in a single blog → not used. |
| 2 | `C2PA Content Credentials adoption 2026 members camera manufacturers platforms deployed` | extended | **Partial.** Nine results, seven secondary blogs, mutually contradictory on Nikon's status, on whether Google Search verification had shipped, and on TikTok's labelling figures. None cited. Located two primary hosts worth fetching: `contentauthenticity.org` and `c2pa.org`. All vendor-adoption specifics → `unverified.md`. |
| 3 | `c2pa conforming products list JSON "conformance" trust list URL github` | standard | **Hit, and the most productive query of the pass.** Surfaced the `c2pa-org/conformance-public` GitHub repository holding `trust-list/C2PA-TRUST-LIST.pem`, and the C2PA-hosted *Content Credentials Deployment Guidance* PDF that carries the only primary conformance count found. Both fetched. |
| 4 | `npm provenance attestations percentage of packages published statistics GitHub blog primary` | extended | **Miss, and decisive for method.** No GitHub or npm publication of an ecosystem-wide provenance rate exists. Three third-party audits surfaced with incompatible samples (top-50 by downloads ≈12%; jsDelivr top-2000 GitHub-published 26/205 ≈12.6%; a dependency-closure drift study 22/95) → all quarantined in `unverified.md`. **This miss is why `report.md` §3.2 is an original measurement rather than a citation.** |

## 2. Page retrieval

| # | URL | Yield |
|---|---|---|
| 5 | `https://contentauthenticity.org/blog/the-state-of-content-authenticity-in-2026` | Hit. Published 18 Jan 2026. "more than 6,000 members"; Google Pixel 10; Sony PXW-Z300; Adobe Content Authenticity for Enterprise; CAWG 1.2. Conformance Explorer described as tracking "a growing cohort" with **no number**. |
| 6 | `https://c2pa.org/conformance/` | Hit. Trust List launched mid-2025 with a public Certificate Policy; Interim Trust List frozen 1 Jan 2026; separate TSA list; links a JSON conforming-products list. **No count on the page.** |
| 7 | `https://conformance.c2pa.org/` | **Miss — hard.** `getaddrinfo ENOTFOUND`. The hostname does not resolve. A secondary source had described a live JSON registry at a conformance-explorer URL; see the correction in `unverified.md`. |
| 8 | `https://slsa.dev/blog/2026/05/mini-shai-hulud-what-slsa-can-and-cannot-do` | Hit. 84 package builds / 42 `@tanstack` packages / 170+ in the worm; the full attack chain; and three details R-001 does not record, including **"Both malicious runs ended with `status: failure`"** and **"Standard SLSA consumer tooling does not check workflow run status."** |
| 9 | `https://c2pa.org/wp-content/uploads/sites/33/2026/07/Content-Credentials-Deployment-Guidance.pdf` | Hit. **"Since its launch, 54 products from 31 companies have passed conformance (as of May 14, 2026)."** Plus 120+ expressions of interest, the conformance queue, and the re-export/screenshot stripping note. PDF **not committed** — digest and locator recorded in `sources.md` per `library/CLAUDE.md`. |

## 3. Direct measurement

| # | Command / endpoint | Yield |
|---|---|---|
| 10 | `curl https://raw.githubusercontent.com/c2pa-org/conformance-public/refs/heads/main/trust-list/C2PA-TRUST-LIST.pem` | Hit. 37,911 bytes, sha256 `75cacc98…64aea5`. Split on `BEGIN CERTIFICATE` → **30** certificates. `openssl x509 -noout -subject -issuer -enddate` on each → 17 organisations, 19 self-signed roots, 11 intermediates, `C=US` 20 / `C=CN` 8 / `C=NL` 1 / `C=DE` 1. Full listing in `sources.md` §3.1. |
| 11 | `https://registry.npmjs.org/-/v1/search?text=keywords:javascript&size=5&popularity=1.0&quality=0.0&maintenance=0.0` | Hit. Probe confirming the search API accepts a pure-popularity weighting. `total: 59917`. |
| 12 | `https://registry.npmjs.org/-/v1/search?text=*&size=250&popularity=1.0&…` | **Miss.** `HTTP Error 400: Bad Request`. The wildcard is not a valid `text` value. **Dropped from the sampling frame**, which is why `report.md` §3.2 states three keyword queries and not four, and why the sample is described as popularity-ranked *within keyword queries* rather than registry-wide. |
| 13 | `https://registry.npmjs.org/-/v1/search?text={keywords:javascript, keywords:node, keywords:utility}&size=250&popularity=1.0&quality=0.0&maintenance=0.0` | Hit. Deduplicated to 300 distinct packages by highest popularity score. |
| 14 | `https://registry.npmjs.org/<name>` × 300, reading `versions[dist-tags.latest].dist.attestations` | Hit. 100 with provenance, 200 without, **0 fetch errors**. By publishing scope: 56 of 242. Concentration: top 5 scopes = 40 of the 100. |

## 4. Not searched, deliberately

- **Practitioner interviews.** `PLAN-0001` §11 allows 3–5 short conversations.
  None were attempted in this pass; `report.md` §1 states this and §10 carries
  it forward.
- **Encoding and serialisation.** Owned by the mechanism report and DEC-002.
  No query in this pass touched it, so nothing here should be read as evidence
  for an encoding.
- **Re-retrieval of R-001's sources.** R-001 is merged and its 155 citations
  resolve at `library@93891c9`. Re-fetching them would have produced drift, not
  evidence. `sources.md` §2 lists exactly which records are relied on without
  re-retrieval.
