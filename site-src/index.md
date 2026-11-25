# m-of-n

**Key-centric Semantic Attestations (KSA).** Authorization, local names, and artifact
attestation with a model whose principals are keys, whose names are relative to
a naming key, whose subjects may be *k*-of-*n*, and whose statements carry
meaning a person can read.

USF CS690 Master's Project, Fall 2026. Sponsor: Paul Lambert.
Code is licensed Apache-2.0 and documentation CC-BY-4.0 (see the
[repository](https://github.com/m-of-n/mofn)); the reference library is a
separate repository with its own terms.

!!! warning "What this does not do"
    It proves **origin and integrity**, not truth. A perfectly valid attestation
    can assert something false. See [Limitations](LIMITATIONS.md).

## Status

**Research prototype.** The architecture is a **draft** and every page on this
site says what state it is in, in the banner under its title.

- **Decided:** a decision is accepted only by an ADR, listed under
  *Architecture → Decisions* in the navigation. Anything without one is open.
- **Open:** listed, with what each one blocks, in the
  [decision register](project/DECISIONS-0001.md). Do not cite an open decision
  as settled.
- **Software:** the wallet ships as prototype pre-releases — see
  [Download](download.md). Do not use real keys.

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
- [Decision register](project/DECISIONS-0001.md) — what is open, and what it blocks
- [Bibliography](library/bibliography.md) — the literature the design rests on
- [Plan](project/PLAN-0001-project-plan.md) · [Backlog](project/BACKLOG-0001.md)
