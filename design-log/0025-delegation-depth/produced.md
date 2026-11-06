---
schema: "design-log/v1"
id: DL-0025
part: produced
date: "2026-11-06"
---

# DL-0025 — produced

No spec text yet. The agent produced:

- the two questions, with recommendations (1a, 2a). The arguments for 1a:
  - Boolean is a special case of integer depth: absent `may-delegate` means one
    hop, and depth ≥ 1 means delegate onward.
  - `ranges` and the key lists are the width control that RFC 2693 §4.1.4 says
    depth lacks.
  - OpenPGP trust signatures (RFC 9580) are a deployed integer depth.
  - (b) supersedes an accepted ADR and changes the wire format late.
- what R-M-10 must say once rewritten (in mofn#136):
  - it matches SPEC-0004 §6.3;
  - it cites RFC 2693 §4.1.3–§4.1.4;
  - it records as a **stated limit** that depth is not a security bound;
  - a vector covers `depth` and `widening`.

The R-M-10 diff and the §4.2 `AuthzCert.delegate` replacement are owed to
T-012a (mofn#134). Only one ARCH-0001 change may be in flight at a time.
