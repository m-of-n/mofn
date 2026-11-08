---
schema: "design-log/v1"
id: DL-0031
part: produced
date: "2026-11-07"
---

# DL-0031 — produced

Vectors, test code and spec text. No primitive: signing and hashing are
`cryptography`, as before.

| file | change |
|---|---|
| `spec/vectors/ksa-core/generate.py` | TV-14…20: trust and attestation statements over DV-1 `build-provenance`; an `evaluations` block E-1…E-4 with the expected SPEC-0004 answer, reason and failing statement. **Declared, not computed** |
| `spec/vectors/ksa-core/vectors.json`, `vectors.md` | regenerated. TV-1…13 and N-1…10 are **byte-identical** (`git diff` shows additions only) |
| `spec/SPEC-0002-ksa-core.md` 0.6.0 → **0.7.0** | Appendix A carries the new vectors (MINOR: additive) |
| `spec/SPEC-0004-ksa-trust-evaluation.md` 0.3.0 → **0.4.0** | Appendix A: hypothetical Ask 3 replaced by asks 3–6 over E-1…E-4. No rule or existing answer changes (MINOR: additive) |
| `prototype/wallet/tests/test_delegation.py` | E-1…E-4 checked by a test-only reading of §6.3 items 1, 3, 4, 6; TV-13 renders under DV-2 as "Alice says that for Bob, name is fred." and as unresolved without it |
| `project/BACKLOG-0001.md` | T-012c done; T-049 done; T-065 added (engine delegation) |

| eval | statements | answer | reason | §6.3 item |
|---|---|---|---|---|
| E-1 | TV-14, TV-15 | no | `widening` at TV-14 | 4: `about` outside `may-delegate.ranges` |
| E-2 | TV-16, TV-17 | yes | — | the control: the same hop within ranges |
| E-3 | TV-16, TV-18, TV-19 | no | `depth` at TV-18 | 3: no delegation left |
| E-4 | TV-20, TV-17 | no | `widening` at TV-20 | 6: onward depth 1 where at most 0 remains |

The test walker discriminates: dropping item 6 turns E-4 into **yes**;
dropping item 3 turns E-3 into **yes**.
