---
schema: "library-doc/v1"
id: RPT-0001-sources
title: "Sources consulted — CBOR research"
type: evidence
status: draft
version: "0.1.0"
date: "2026-09-22"
updated: "2026-09-22"
---

# Sources

All retrievals 2026-09-22 unless stated.

## 1. Primary sources verified by the author

These were fetched and checked directly, not via an agent. Every specification
identifier in `report.md` rests on this tier.

| Source | URL | Retrieved | What it settled |
|---|---|---|---|
| RFC Editor index (index created 2026-09-21) | https://www.rfc-editor.org/rfc-index.txt | 2026-09-22 | The authoritative list of all 41 CBOR/COSE/CDDL RFCs, with exact titles, authors, dates, status, and Obsoletes/Updates relations. Every RFC in the bibliography was taken from here verbatim. |
| IETF datatracker document API | `https://datatracker.ietf.org/api/v1/doc/document/?name=<draft>` | 2026-09-22 | Current revision, state and **expiry** of all six drafts. Established that CDE `-13` expired 2026-04-17 and Packed `-19` expired 2026-08-06, against secondary accounts treating both as live. |
| `draft-ietf-cbor-serialization-08` full text | https://www.ietf.org/archive/id/draft-ietf-cbor-serialization-08.txt | 2026-09-22 | Abstract and a `grep -ci cde` returning 0 — the draft makes no claim to supersede CDE. Basis for using `see_also` rather than `supersedes`. |
| `draft-mcnally-deterministic-cbor-18` full text | https://www.ietf.org/archive/id/draft-mcnally-deterministic-cbor-18.txt | 2026-09-22 | Abstract and normative reference list. Establishes that at `-18` dCBOR narrows RFC 8949 §4.2 directly and does not mention CDE. |
| IETF CBOR WG | https://datatracker.ietf.org/wg/cbor/about/ | 2026-09-22 | `ietf-cbor-wg` record |
| IETF COSE WG | https://datatracker.ietf.org/wg/cose/about/ | 2026-09-22 | `ietf-cose-wg` record |
| IANA CBOR Tags registry | https://www.iana.org/assignments/cbor-tags/cbor-tags.xhtml | 2026-09-22 | `iana-cbor-tags` record — the R-M-12 evidence |
| IANA CBOR Simple Values registry | https://www.iana.org/assignments/cbor-simple-values/cbor-simple-values.xhtml | 2026-09-22 | `iana-cbor-simple-values` record |
| 45 RFC and draft full texts | `rfc-editor.org/rfc/rfc<n>.txt`, `ietf.org/archive/id/<draft>-<rev>.txt` | 2026-09-22 | Each hashed; the sha-256 is in the corresponding `record.yaml`. Bytes are not committed. |

## 2. Agent dimension surveys

Six parallel agents, 2026-09-22. Raw outputs archived under `dimensions/`,
each with its own full source list and retrieval dates. **Unverified except
where `report.md` says otherwise.**

| File | Dimension | Sources in file |
|---|---|---|
| `dimensions/specifications.md` | specs, published and in flight | datatracker, rfc-editor, IANA |
| `dimensions/open-source.md` | implementations | repo pages, crates.io / PyPI / npm / NuGet / Maven, RUSTSEC, GHSA, NVD |
| `dimensions/products.md` | shipping products | vendor developer docs, consortium pages, spec texts |
| `dimensions/markets.md` | market drivers | EUR-Lex, analyst press releases (flagged), vendor stats |
| `dimensions/applications.md` | use-case patterns and determinism | primary spec texts incl. CTAP2.1 §8, RFC 8949 §4.2, IPLD DAG-CBOR spec |
| `dimensions/consortiums.md` | governance | datatracker charters, iana.org, iso.org, fidoalliance.org, c2pa.org, ec.europa.eu |

## 3. Regulatory sources

| Source | Retrieved | Note |
|---|---|---|
| Regulation (EU) 2024/1183 (eIDAS 2.0), via EUR-Lex | 2026-09-22 | In force 20 May 2024; wallet availability ~24 Dec 2026; relying-party acceptance Nov 2027. Primary text. |
| Directive (EU) 2025/2205 | 2026-09-22 | European digital driving licence aligned to ISO 18013-5. Via agent; **not** author-verified against EUR-Lex. |

## 4. Security advisories cited in the report

CVE-2026-26209 / GHSA-3c37-wwvx-h642 (`cbor2` recursion DoS) · CVE-2025-68131 /
GHSA-wcj4-jw5j-44wh (`cbor2` decoder state leak) · CVE-2025-24302 and
CVE-2025-20025 (TinyCBOR recursion) · RUSTSEC-2021-0127 (`serde_cbor`
unmaintained) · RUSTSEC-2019-0025 / CVE-2019-25001 (`serde_cbor` stack
overflow) · GHSA-g3qj-j598-cxmq (`cbor-extract` heap over-read via
`fido2-lib`). All via `dimensions/open-source.md`; advisory IDs were **not**
independently re-fetched by the author.

## 5. Figures deliberately not relied on

Recorded so they are not silently reused as fact:

- Confidential-computing market size: **$5.7B–$54B** across analyst firms, ~10×
  disagreement; one implies a 90–95% CAGR. Not cited in the report.
- Passwordless/FIDO market size: **$16.85B–$27.66B** across five firms, no
  shared methodology. Not cited.
- LwM2M "23% CAGR": traceable to a 2019/2020 press release. Stale.
- C2PA "6,000+ members": a coalition headcount, not a usage measure.
- Paywalled and therefore assessed second-hand only: **ISO/IEC 18013-5**
  (CHF 227/part), 18013-6/-7, 23220, JPEG Trust / ISO/IEC 19566-5.
