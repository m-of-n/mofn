---
schema: "archdoc-changelog/v1"
id: ARCH-0001-CHANGELOG
title: "ARCH-0001 changelog"
type: changelog
parent: ARCH-0001
status: active
version: "0.1.1"
date: "2026-09-15"
updated: "2026-09-21"
canonical_path: spec/ARCH-0001-CHANGELOG.md
---

# ARCH-0001 changelog

Format: newest first. Versions match the architecture document.

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
