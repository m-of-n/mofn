---
schema: "design-log/v1"
id: DL-0055
part: produced
date: "2026-11-23"
---

# DL-0055 — produced

- **ARCH-0001 0.3.4**, edited in place (§9.1). PATCH: no requirement moves.
  - **§6 cells.** in-toto (import names its accepted digest algorithms); DSSE
    (*n* signatures and never *k*; `keyid` is unauthenticated; exterior
    fields per P5.2); COSE_Sign1 + CWT (SCITT `iss`/`sub` protected,
    `x5chain` unprotected; P1.1's `kid` and `cnf`); PICS; W3C VC; SCITT
    receipt.
  - **The KSA envelope paragraph.** No row, because the table maps foreign
    objects. It is not a DEC-005 candidate, every export signs again, and
    DEC-005 is open.
  - **§6.1, Notes to the rows**, six numbered notes with locators.
- **ARCH-0001-CHANGELOG 0.3.4.**

What the notes record as **owed, not decided**:

- whether an import of Data Integrity-secured VCs is refused or carved out,
  since it canonicalises at verification (R-O-05);
- how a KSA `kid` is written as CWT `iss` and `sub` (WP3, under DEC-005);
- P5.2's negative fixture, and COSE `crit` if COSE is chosen.
