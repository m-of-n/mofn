---
schema: "design-log/v1"
id: DL-0005
title: "Cipher suite — definition and critique, before any statement schema"
date: "2026-10-02"
model: "grok"
human: "pending"
outcome: "R-0003. No code."
status: open
---

# DL-0005 — produced

- `research/0003-cipher-suite/report.md` (R-0003)
- `research/0003-cipher-suite/example.yaml` — the existing
  `HPKE_P256_AES_GCM_128` class written as data, with nulls where the class
  has no signature, no signature encoding, and no signed-bytes rule
- `research/0003-cipher-suite/sources.md`
- `research/0003-cipher-suite/searches.md`

No file under `src/`, `spec/`, or `prototype/` was added or edited.
`bin/manifest` was not run: it only scans `research/*.md`, not
`research/<id>/report.md`, which is the same layout R-0002 already uses.

## Rejected while writing, before any human review

- Patching `derive_csi` (`self` → `cls`) in the hpke checkout. Real defect.
  Wrong repository, and the function body would still hash a docstring or
  need a derivation this task said not to invent.
- Copying the HPKE module into `src/` and "fixing" the table. That would
  put a session cipher suite in the product and would keep the stripped
  SEC1 public key and the private `csi` as if they were chosen.
- Filling the key-exchange slot with DHKEM(P-256) because the example uses
  that class. The example is a transcription. The v1 slot stays empty.
- Picking Ed25519, ECDSA, or COSE as the statement signature because the
  HPKE suite has none. That is an algorithm choice, and COSE would lean on
  DEC-002.
- Implementing `readable_pk_id`. `Persona.addPeer` calls it and it is
  missing. Implementing it picks how a public key becomes an id.
- Designing wallet, attestation, or delegation fields beyond the six names
  in R-0003 §8.
