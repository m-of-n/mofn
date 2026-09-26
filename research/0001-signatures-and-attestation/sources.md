# Sources

Every reference cited in `report.md` resolves to a record in `m-of-n/library`.
This file is the bridge: it records what each lane returned, and the library
record id once ingested.

**Rule:** a citation with no library record does not appear in the paper. The
bibliography is generated from `library/exports/references.json`, so an
unrecorded source is simply absent — which is the enforcement mechanism, not an
honour system.

## Ingestion status

| lane | references returned | ingested | records |
|---|---|---|---|
| A foundations | pending | — | — |
| B X.509 / PKIX | pending | — | — |
| C decentralised naming | pending | — | — |
| D content labelling | pending | — | — |
| E device attestation | pending | — | — |
| F supply chain | pending | — | — |
| G capability tokens | pending | — | — |
| H post-quantum | pending | — | — |

## Already held before this survey

The library carried 78 records at the start of R-001, including the CBOR/COSE
ecosystem, RFC 9943 (SCITT), RFC 2693 (SPKI), RFC 9804, W3C PICS, DSSE,
in-toto, FIPS 186-5 and the NIST signature set. Those are reused rather than
re-ingested; `bin/ingest` refuses a duplicate id across all bodies.
