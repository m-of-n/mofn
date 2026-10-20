---
schema: "library-doc/v1"
id: R-0006-unverified
title: "Unverified claims register — mechanism"
type: evidence
status: draft
version: "0.1.0"
date: "2026-10-17"
updated: "2026-10-17"
---

# Unverified claims register

This file is a **publication gate, not a to-do list**. The rule, inherited from
R-001:

> No claim appearing below may be stated as fact in `report.md` until it has
> been verified against a primary source and the source ingested into
> `library/`. A claim that cannot be verified is either cut, or stated in the
> report as contested with the uncertainty named.

Every entry is a cell of `report.md` §2.2 printed as **∅**, or a guarantee §2.4
names as inherited rather than checked. **None is stated as fact in
`report.md`.** Checked 2026-10-17 by reading each ∅ cell, plus every sentence in
§2.3–§2.5 that touches the same system, against this list.

They are not unknowable. Most are well-known facts about well-known
specifications, which is why they matter here: they are exactly the cells a
model would fill from memory, and a reader could not tell those apart from
the sourced ones.

## 1. PICS and DSig 1.0

Records `pics-1-1-labels`, `pics-1-1-services`, `pics-dsig-1-0` and
`powder-description-resources` are **unfilled templates** at `library@60b3284`.
`pics-dsig-1-0` records its digest as `not fetched`.

| ∅ cell | what would fill it |
|---|---|
| whether and how a PICS 1.1 label binds the content it labels (a hash option on the label?) | `pics-1-1-labels`, written up |
| what DSig 1.0 signs, whether it canonicalises, and when | `pics-dsig-1-0`, fetched and written up |
| how a DSig verifier proceeds | the same |

What `report.md` *does* say about PICS comes from R-001 §6.1 and §11.1, which
cite these records by key but quote the specifications directly: rating service
versus rating system, the label citing its system by URL, label bureaus, the
client choosing among them.

## 2. W3C Verifiable Credentials

**No record exists** for the VC Data Model (1.1 or 2.0), VC Data Integrity, or
VC-JOSE-COSE. A `grep -ril` for `verifiable credential`, `vc-data-model`,
`data integrity` and `vc-jose` across `records/` and `topics/` finds only the
generic phrase *data integrity* in unrelated guidance (`searches.md` §2).

| ∅ cell | what would fill it |
|---|---|
| what a VC hashes, what it signs, and what its proof carries | new records: VC Data Model 2.0, VC Data Integrity 1.0, VC-JOSE-COSE |
| **whether VC Data Integrity canonicalises at verification** — the one VC fact that bears on condition (3) | VC Data Integrity, plus whichever cryptosuite would be cited |
| how a VC verifier proceeds | the same |

`ARCH-0001` R-I-06 (*Could*) and the §6 *W3C VC* row both depend on these.
`report.md` §2.5 says the row cannot be evidenced until they exist.

## 3. DID

Records `w3c-did-core`, `w3c-did-1-1`, `w3c-did-extensions-methods` and
`did-key-method` are stubs. The trust and undefined cells in §2.2 come from
R-001 §5.6's quotations. The **verifier-procedure cell** is ∅: DID resolution
and verification-method selection are not in the library.

## 4. in-toto

`in-toto-attestation-v1`, `in-toto-envelope-v1` and `in-toto-2019` are stubs.
The Statement's field list and digest-map shape in §2.2 are taken **second-hand**
from the SLSA 1.2 extraction (`slsa-1-2`), which quotes them. in-toto's own
`DigestSet` specification, and the layout's verification procedure, are ∅.
R-001 §8.2 and §8.5 supply the layout's trust placement by quotation.

## 5. SPKI's signed structure

`draft-ietf-spki-cert-structure` and `sdsi-1-1` are stubs.

| ∅ cell | what would fill it |
|---|---|
| the exact to-be-signed construction of an SPKI certificate | `draft-ietf-spki-cert-structure`, written up. It is the wire format the WG never published (R-001 §5.5) |
| which fields of a signed SPKI object are authenticated | the same |

## 6. Merkle proofs

`rfc-6962`, `rfc-9162` and the three Merkle papers are stubs. Every guarantee
§2.4 states about inclusion and consistency proofs is **RFC 9942's description
of RFC 9162**, not RFC 9162 checked. `report.md` §2.4 says this in its first
paragraph. The RFC 9942 extraction's `reviewed_by` is also empty, and §2.4 says
so too.

## 7. What is deliberately not here

- **Anything in §3–§5.** Those sections rest on FX-1 extractions at the pin,
  and `sources.md` §2 records them.
- **Claims carried from R-001.** R-001 keeps its own register
  (`research/0001-signatures-and-attestation/unverified.md`). Every R-001
  passage `report.md` relies on was checked against it, 2026-10-17: no claim
  taken from §5.6, §6.1, §8.2, §8.5 or §11.1–§11.3 is listed there. The nearest
  item is register D-10, on whether third-party label bureaus were ever deployed
  at scale. §2.2 says the client *chooses* among bureaus, which is a claim about
  the protocol. It makes no claim about deployment. Register C's DID 1.1 status
  item is not touched, because `report.md` states no DID status.
