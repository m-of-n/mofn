# m-of-n

**Key-centric semantic assertions.** Authorization, local names, and artifact
attestation with a model whose principals are keys, whose names are relative to
a naming key, whose subjects may be *k*-of-*n*, and whose statements carry
meaning a person can read.

USF CS690 Master's Project, Fall 2026. Sponsor: Paul Lambert.
Everything is open source. No proprietary data, no NDA.

!!! warning "What this does not do"
    It proves **origin and integrity**, not truth. A perfectly valid attestation
    can assert something false. See [Limitations](LIMITATIONS.md).

## Status

**Pre-implementation.** The architecture is at v0.1.0 draft. **DEC-001 … DEC-005
and DEC-007 are open** — no encoding, tag language, or envelope has been
selected. Documents published here are drafts and are marked as such. Do not
cite an open decision as settled.

## The problem

Modern attestation stacks — in-toto, SLSA, SCITT (RFC 9943), C2PA — bind
statements to artifacts well and say almost nothing about what a statement
*means* to a person. Two older bodies of work solved the missing pieces and were
never combined:

- **SDSI/SPKI** gave us principals that are keys, names local to a naming key,
  delegation, and *k*-of-*n* subjects — but never standardised a first-class
  statement about an artifact.
- **PICS** gave us signed labels about content, with rating systems published
  separately from the labels that cite them — but had no principal or delegation
  model at all.

This project builds the native model that has both.

## Read next

- [ARCH-0001](architecture/ARCH-0001-authorization-attestation.md) — architecture, the source of truth
- [Open proposal v0.2.0](architecture/ARCH-0001-PROPOSAL-v0.2.0.md) — under review
- [Plan](architecture/PLAN-0001-project-plan.md) · [Backlog](architecture/BACKLOG-0001.md)
