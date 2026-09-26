---
schema: "archdoc/v1"
id: R-0001
title: "What a Signature Proves: A Survey of Digital Signatures and Attestation"
short_title: "Signatures and attestation survey"
description: "Academic survey classifying attestation systems by what they let a key assert, who may assert it, and where trust begins."
type: research
category: security
status: draft
version: "0.1.0"
date: "2026-09-26"
updated: "2026-09-26"
needs_review: true
reviewed: false
canonical_path: research/0001-signatures-and-attestation/report.md
backlog: R-001
---

# What a Signature Proves
## A Survey of Digital Signatures and Attestation

**Status: first draft.** Sections are filled from mini-reports as their research
completes; every citation resolves to a record in `m-of-n/library`.

---

## Abstract

*Pending — written last, once the sections it summarises exist.*

---

## 1. Introduction

A digital signature proves that a particular private key was used over
particular bytes. That is all it proves. It establishes neither the identity of
the keyholder, nor their authority to make the statement, nor the truth of what
the statement says.

Fifty years of systems have been built on top of that narrow guarantee, and
almost none of the engineering effort has gone into the signature itself. It has
gone into the three questions the signature leaves open:

1. **Who holds this key?** — the naming problem
2. **What is this key entitled to say?** — the authorization problem
3. **Where does trust begin?** — the root problem

This survey classifies attestation systems by how they answer those three
questions rather than by application domain. The classification is the
contribution: it makes visible that systems which appear unrelated — an X.509
certificate chain, a TPM quote, an in-toto attestation, a PICS label — are the
same construction with different answers, and that they are largely
**incompatible in ways their specifications do not state**.

*Full introduction pending mini-report A.*

## 2. Foundations: what a signature proves

*Pending mini-report A — Diffie–Hellman 1976 through EUF-CMA and the NIST DSS
lineage.*

## 3. A taxonomy of assertion

Every system in §§4–10 is an instance of one form:

> **A says B has property C**

with a signature binding the statement to A's key. Systems differ along five
axes, and those axes are how the rest of this survey is organised.

| axis | question | why it separates systems |
|---|---|---|
| **Subject** | what is B? | a key, a name, a document, a device state, a build |
| **Predicate** | what is C, and who defines it? | fixed by the specification, or declared in a separate published vocabulary |
| **Authority** | who may say it? | inherited root store · local policy · hardware vendor · out-of-band |
| **Scoping** | can authority be narrowed on delegation? | and if so, along what dimension — name, tag, capability, or not at all |
| **Root** | where does trust begin? | a root store you inherited, a keyring you built, a policy you wrote, silicon |

**The claim this taxonomy is built to test:** the signature is the solved part.
Systems diverge almost entirely on **authority** and **scoping**, and a
surprising number simply do not answer the scoping question at all — they assume
an out-of-band trust root and delegate nothing.

§11 populates this table for every system surveyed.

## 4. Naming and identity
*Pending mini-report B — X.509/PKIX, path validation, name constraints,
revocation, Certificate Transparency.*

## 5. Decentralised naming
*Pending mini-report C — PGP web of trust, SDSI, SPKI, DIDs.*

## 6. Content labelling
*Pending mini-report D — PICS, POWDER, C2PA.*

## 7. Device and platform attestation
*Pending mini-report E — TCG TPM, DAA, DICE, RATS, confidential computing.*

## 8. Software supply chain
*Pending mini-report F — in-toto, DSSE, SLSA, Sigstore, SCITT, TUF, SBOM.*

## 9. Capability and delegation
*Pending mini-report G — macaroons, biscuit, UCAN, ZCAP-LD.*

## 10. Post-quantum transition
*Pending mini-report H — FIPS 204/205, SP 800-208, migration and signature size.*

## 11. Comparative analysis
*Pending — the taxonomy table populated across all systems.*

## 12. Open problems
*Pending.*

## 13. Conclusion
*Pending.*

## References
*Generated from `library/exports/references.json`. Every entry is a library
record; nothing is typed by hand.*
