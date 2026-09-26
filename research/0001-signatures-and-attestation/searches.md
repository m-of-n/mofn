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
