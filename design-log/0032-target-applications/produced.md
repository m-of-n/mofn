---
schema: "design-log/v1"
id: DL-0032
part: produced
date: "2026-11-09"
---

# DL-0032 — produced

No primitive: signing and hashing are `cryptography`, as before.

| file | change |
|---|---|
| `spec/ARCH-0001-authorization-attestation.md` 0.2.1 → **0.3.0** | §1 motivation paragraph (AI agents, no normative content); **new §2.3**: §2.3.1 supply chain (SC-1…3), §2.3.2 archives (AR-1…3), §2.3.3 not targets; §10 C2PA pointer |
| `spec/ARCH-0001-CHANGELOG.md` | 0.3.0 entry |
| `spec/vectors/ksa-core/generate.py`, `vectors.json`, `vectors.md` | DV-3 `library-review` (Dave); TV-21…26; evaluations E-5…E-7; `record_sha256`. Every existing vector is byte-identical (the only `-` line in the diff is a JSON comma) |
| `spec/SPEC-0002-ksa-core.md` 0.7.0 → **0.8.0** | Appendix A carries them (MINOR: additive) |
| `spec/UC-0001-ksa-use-cases.md` 0.1.0 → **0.2.0** | traceability: UC → §2.3 row → vectors |
| `prototype/wallet/engine/definition.py`, wallet **0.3.0** | a text attribute (base kind 3) is a valid assignment. v0 refused every non-enum value, so TV-26's `locator` failed |
| `prototype/wallet/tests/test_delegation.py` | the walker handles unbounded ranges and any subject; E-5…E-7; DV-3 template conformance; DV-3 rendering through the same renderer; E-7 through the **engine** (one hop) |
| `project/BACKLOG-0001.md` | T-012b in review; T-066 (render a description target) |

| ARCH row | vectors | answer | evidence |
|---|---|---|---|
| SC-1 | TV-4, TV-7 | yes; then `revoked` | SPEC-0004 App. A Asks 1–2 |
| SC-2 | TV-5, TV-16, TV-17 | yes; E-1/E-3/E-4 fail | E-2, test walker |
| SC-3 | TV-9, TV-6 | **illustrative** | SPEC-0005 has no vectors |
| AR-1 | TV-22, TV-23, TV-25 | yes | E-5 |
| AR-2 | TV-24 | no, `no-path` | E-6 |
| AR-3 | TV-26 | yes | E-7, engine |
