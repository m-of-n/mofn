---
schema: "archdoc-changelog/v1"
id: ARCH-0001-CHANGELOG
title: "ARCH-0001 changelog"
type: changelog
parent: ARCH-0001
status: active
version: "0.1.3"
date: "2026-09-15"
updated: "2026-10-23"
canonical_path: spec/ARCH-0001-CHANGELOG.md
---

# ARCH-0001 changelog

Format: newest first. Versions match the architecture document.

## 0.1.3 — 2026-10-23

- Additive only (§9.1), from the CBOR/COSE extraction handed over in mofn#112
  (library records at `bafd536`). §7 DEC-002 and DEC-003 each gain a block of
  **inputs their ADR must answer**: the omitted driver *detectability of an
  order-only divergence*; "no IANA tags" restated as a rule of our profile; the
  acceptance test's threshold invariant, which no schema language checks, owned
  by a named verifier step; RFC 9679 thumbprints not native-eligible as written;
  the IANA allocation inside a post-quantum COSE thumbprint; and the inverse
  question for a suite-free `kid`.
- No decision accepted, ranked or withdrawn. DEC-001 … DEC-005 remain open. The
  §6 matrix is untouched — that is mofn#110's lane.

## 0.1.2 — 2026-10-14

- Additive only (§9.1). New §4.4: a pointer to **ARCH-0003**, the wallet, persona,
  key and definition object model drafted from sponsor direction of 2026-10-14.
- No model, requirement or decision change in this document.

## 0.1.1 — 2026-09-21

- Editorial only. No model, requirement, or decision change.
- `canonical_path` moved from `artifacts/docs/` to `spec/`. "Artifact" is a
  normative term in this document (`ArtifactId`, `ArtifactStatement`, R-M-07,
  and RFC 9943's definition); using it for a directory of authored documents
  overloaded the most load-bearing noun in the model. Execution documents
  (PLAN, BACKLOG, PROC) moved to `project/`.

## 0.1.0 — 2026-09-15

- Initial checkpoint from research pass on X.509, PGP/WoT, SDSI, SPKI, PICS, in-toto, DSSE, COSE/CWT, SCITT, SLSA.
- Constraint recorded: native model is not X.509; interchange is required.
- Information model drafted: NameCert, AuthzCert, AclEntry, ArtifactStatement, Endorse.
- Requirements R-M-*, R-I-*, R-O-*, R-D-* written.
- Interchange matrix first cut.
- Open decisions DEC-001 … DEC-005 filed; none accepted.
- No encoding, tag language, or envelope selected.
