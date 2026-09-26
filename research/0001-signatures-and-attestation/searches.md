# Searches

Per `mofn/research/README.md`: archive the searches, not just the findings.
Wohlin snowballing requires recording each iteration's yield, and that cannot be
done retrospectively.

## Round 1 — 2026-09-26, eight parallel research lanes

| lane | area | prompt focus |
|---|---|---|
| A | foundations | DH 1976 → RSA → Rabin → Lamport → ElGamal → GMR → Schnorr → FIPS 186-x |
| B | X.509 / PKIX | RFC 5280, path validation, **name constraints in practice**, revocation failure, CT, CA compromises |
| C | decentralised naming | PGP RFC 9580, SDSI, SPKI RFC 2692/2693/9804, DIDs, **why none displaced X.509** |
| D | content labelling | PICS 1.1 + DSig, POWDER, C2PA, human-factors research, EU AI Act Art. 50 |
| E | device attestation | TPM 1.2/2.0, DAA, DICE, RATS RFC 9334, EAT, CoRIM, SGX/TDX/SEV-SNP/CCA |
| F | supply chain | in-toto USENIX 2019, DSSE rationale, SLSA, Sigstore, SCITT RFC 9943, TUF, SBOM, CRA |
| G | capability tokens | Dennis & Van Horn, confused deputy, macaroons NDSS 2014, biscuit, UCAN, ZCAP, PoP |
| H | post-quantum | Shor, FIPS 203/204/205, NISTIR 8610, SP 800-208, LMS/XMSS, sizes, migration |

Each lane was instructed to **verify every citation by search** rather than
recall, and to return an explicit *could not establish* section.

*Per-lane query logs appended as lanes return.*

## Research lane query logs (2026-09-26)

All eight lanes ran to completion. Each was instructed to verify every citation
by search or direct fetch rather than from memory, and to return an explicit
"could not establish" section.

| Lane | Tool calls | Notes |
|---|---|---|
| A — foundations | 46 | confirmed 17 of 25 refs field-by-field against the Crossref REST API; read Rabin, Lamport and Merkle scans directly |
| B — X.509 / PKIX | 71 | downloaded RFC text and quoted from local copies; ran an original CCADB measurement |
| C — decentralised naming | 61 | RFC facts taken from fetched RFC text, not search summaries |
| D — content labelling | 48 | C2PA 2.4 spec read directly for §6.2.1/§6.2.2 and Chapter 18 |
| E — device attestation | 28 | TCG site returns HTTP 403 to automated fetch; version claims come from filenames and summaries |
| F — supply chain | 129 | verified against NVD, Crossref, OpenAlex, the Federal Register API and EU CELLAR |
| G — capability / delegation | 46 | all three 2026 agentic drafts verified on datatracker |
| H — post-quantum | 52 | sizes extracted directly from the FIPS 204 and FIPS 205 PDFs |

**Seven of eight lanes exhausted the 200-call web-search budget.** That is
recorded because it explains the shape of `unverified.md`: a number of the
open items are gaps in remaining effort rather than gaps in the record, and
are recoverable with a fresh budget. Each lane says which of its items are
which.

Two hosts refused automated fetch throughout and account for several open
items: `trustedcomputinggroup.org` (403) and `iso.org` (403).
