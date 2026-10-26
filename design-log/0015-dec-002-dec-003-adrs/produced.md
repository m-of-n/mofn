---
schema: "design-log/v1"
id: DL-0015
part: produced
date: "2026-10-25"
---

# DL-0015 — produced

| file | change |
|---|---|
| `spec/ADR-0004-dec-002-encoding.md` | new; DEC-002 → option 5; scoring table; acceptance test met / owed |
| `spec/ADR-0005-dec-003-key-identifier.md` | new; DEC-003 → `kid` = SHA-256(suite public-key encoding); alternatives table; acceptance test supplied |
| `spec/ARCH-0001-authorization-attestation.md` | v0.1.5. DEC-002/003 status lines; option 5 added to §7's list; §4.1 `KeyId` narrowed; `open_decisions` trimmed |
| `spec/SPEC-0002-ksa-core.md` | v0.2.0. §6.1 digest row; §12.3 collision rule. No bytes change |
| `spec/ARCH-0002-key-relative-naming.md` | v0.9.0. P1.1 import rule report → reject; stays draft |
| `project/DECISIONS-0001.md` | v0.4.0. Items 2 and 4b closed |
| `spec/ARCH-0001-PROPOSAL-v0.2.0.md` | proposed.6. Option 5 noted as accepted; the rest still proposed |
| `CLAUDE.md` | the "DEC-001 … DEC-005 are open" rule and the `src/` row updated |

## Text the model added beyond the four answers

Each is a reading of an answer, flagged so a reviewer can reject it:

- **"Suites that share a key algorithm share `kid`s"** (ADR-0005 §4, SPEC-0002
  §12.3) — follows from *registry rule* plus *fixed SHA-256* and R-M-02, but
  the human was not asked it directly.
- **"Agility comes from a new identifier version"** (ADR-0005 §3) — the model's
  account of what *fixed SHA-256* leaves for later.
- **The DEC-002 scoring table.** Cells marked *(ours)* are the model's reasoning,
  not cited findings.
