---
schema: "library-doc/v1"
id: R-0004-unverified
title: "Unverified claims register — uptake and applications"
type: evidence
status: draft
version: "0.1.0"
date: "2026-10-10"
updated: "2026-10-10"
---

# Unverified claims register

This file is a **publication gate, not a to-do list**. The rule, inherited from
R-001:

> No claim appearing below may be stated as fact in `report.md` until it has
> been verified against a primary source and the source ingested into
> `library/`. A claim that cannot be verified is either cut, or stated in the
> report as contested with the uncertainty named.

Every entry below is **absent from `report.md`**. Several were in the drafting
brief and were cut on failing to verify; §4 records one correction to an
assumption the report started with.

Adoption research is unusually exposed to this failure. The attractive numbers
— platform counts, labelled-video totals, "X% of packages" — circulate almost
entirely in secondary commentary, and the 2026 blog posts surfaced in this pass
frequently contradicted each other and read as promotional. That is the reason
`report.md` carries two original measurements instead.

## 1. Supply-chain deployment scale — could not establish

- **Total Rekor transparency-log entries.** A blog asserts "over a billion
  artifacts signed through Rekor as of 2025." No Sigstore publication found
  giving a total. Not stated.
- **Rekor v2 general availability (October 2025), tile-backed, year-sharded,
  `hashedrekord` and `dsse` entry types only.** Single secondary source. Not
  stated. Plausible and worth a primary check if the mechanism report needs it.
- **Count of unique npm packages ever published with provenance** — a figure of
  "over 16,000" was attributed to a Sigstore blog post in a search summary, but
  the post was not retrieved and the figure has no denominator. Not stated.
- **npm provenance rate from third-party audits.** Three mutually incompatible
  samples: ≈12% of the 50 most-downloaded (April 2026); 26 of 205
  GitHub-published packages in the jsDelivr top 2,000 (≈12.6%, 2025); and
  22 of 95 provenance-bearing packages in a dependency closure whose attested
  commit did not contain the published version (23.2%). **None cited.**
  `report.md` §3.2 substitutes its own measurement with its sample stated.
  Note that the third study measures a *different* property — attestation
  accuracy, not presence — and is the more interesting of the three; it is an
  ingestion candidate for whoever takes the mechanism report.

## 2. C2PA vendor and platform adoption — could not establish

R-001 §6.7 already carries a sourcing note that platform and newsroom adoption
claims "could not be established from primary sources." **This pass did not
clear it**, and the list below records what specifically failed, so the next
attempt starts from here rather than from zero.

- **Camera vendors.** Secondary sources list Leica, Sony, Canon and Samsung as
  shipping capture-time signing, with Apple and a Google Pixel 11 announced but
  not shipping. **Nikon is actively contested**: one source says C2PA was added
  to the Z6 III by firmware in August 2025 and then suspended weeks later after
  a signing vulnerability, not restored as of early 2026; another lists Z8, Z9
  and Zf as supported. One source says Canon's rollout is slower than
  committed. No vendor announcement was retrieved for any of this. **Nothing
  about camera vendors is stated in `report.md`.** The CAI blog's Sony
  PXW-Z300 and Google Pixel 10 mentions *are* primary for those two and are the
  only capture-device facts used.
- **OpenAI applying Content Credentials to every ChatGPT image including the
  free tier, and via the DALL·E API since May 2026.** Secondary only.
- **Midjourney not embedding C2PA credentials as of early 2026.** Secondary
  only. A negative claim about a named company on secondary sourcing is the
  worst case; firmly not stated.
- **TikTok having labelled "over 1.3 billion" AI-generated or AI-edited
  videos.** Secondary only, and the single most-repeated figure in the pass.
  Not stated.
- **Google bringing C2PA verification and SynthID detection natively to Google
  Search and Chrome.** Sources disagree on announced versus live. Not stated.
- **"The majority of content shared on social platforms loses its Content
  Credentials during upload."** Secondary. The *primary* deployment guidance
  says only that re-exporting or screenshotting "can strip the embedded Content
  Credentials" and that durable credentials combine watermarking and
  fingerprinting. `report.md` uses the weaker primary statement and not the
  quantified secondary one.
- **C2PA steering-committee composition** (OpenAI, Amazon, Meta, Sony named in
  a secondary source). Not retrieved from C2PA. Not stated.

## 3. Conformance count freshness — a known staleness, stated

The only primary conformance count found is **"54 products from 31 companies
… (as of May 14, 2026)"** in a PDF published July 2026. It is quoted in
`report.md` §4.2 *with its as-of date*, which is approximately five months
before this report. The document itself says there is a queue and that the
number is expected to increase "drastically," so **54/31 should be read as a
floor, not a current figure.** A live count could not be obtained (§4).

## 4. Correction to an assumption the report began with

The drafting brief assumed the C2PA **Conformance Explorer** publishes a live,
machine-readable conforming-products list at a stable URL, and that the report
could cite a current count from it. Both halves failed:

- `https://conformance.c2pa.org/` **does not resolve** (`ENOTFOUND`,
  2026-10-10). The hostname in the secondary source is wrong or dead.
- `https://c2pa.org/conformance/` links an Explorer and a JSON list but the
  page itself publishes no count, and no stable JSON endpoint was confirmed.

What *is* machine-readable and stable is the **trust list** in the
`c2pa-org/conformance-public` repository — which is why `report.md` §4.3
measures the root of trust rather than the product count. The measurement that
appears in the report is the one the failure forced, not the one that was
planned. Recording this is the point of the file.

## 5. Out of scope for this pass, not unverifiable

Listed so that their absence reads as a decision rather than an oversight.

- **Practitioner interviews** (`PLAN-0001` §11, 3–5 conversations). Not
  attempted. Would bear directly on §8.2's claim about who authors statements
  in the wallet model, which is currently an inference.
- **SBOM compliance rates under the CRA.** Full obligations do not apply until
  11 December 2027, so a compliance rate does not yet exist to measure. The
  CRA's *text* is verified via `[@eu-cra-2024-2847]`.
- **OpenPGP web-of-trust adoption in Debian.** Named in `report.md` §10 as the
  strongest candidate counterexample to the four-condition model. Not
  investigated in this pass. Whoever tests the model should start there.
