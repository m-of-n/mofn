---
schema: "library-doc/v1"
id: R-0006-sources
title: "Sources consulted — mechanism"
type: evidence
status: draft
version: "0.2.0"
date: "2026-10-14"
updated: "2026-10-17"
---

# Sources

Bibliography pinned at **`library@60b3284`**. Every `[@key]` in `report.md`
resolves at that commit; checked mechanically for v0.3.0, **20 distinct keys,
51 citations, zero unresolved** (15 keys at v0.2.x).

The low key count relative to R-0005 is not thinness. This report's evidence is
concentrated in **four fully-extracted records and one topic answer**, and it
quotes their extraction artifacts rather than ranging widely.

## 1. The sourcing situation

**No source was retrieved over HTTP for this report.** It is a synthesis pass;
`searches.md` records that. Unlike R-0005, however, the material it synthesises
is itself the product of **FX-1 full extraction** — the library's highest bar —
so most claims below trace to a requirement id or a verbatim quotation inside a
`distilled/` artifact rather than to prose.

## 2. The load-bearing records

| record | profile at the pin | what `report.md` takes from it |
|---|---|---|
| `[@rfc-8949]` CBOR | FX-1 `full` | §4.2 is an **encoder-side** rule; the **fourteen** application-left decisions, each with a negative fixture; §4.2.1 map-key order by encoded bytes; §5.6.1 byte-by-byte text comparison; §3.1 UTF-8 with no normalisation rule |
| `[@rfc-8785]` JCS | FX-1 `full` | §3.2.3 **prohibits** array reordering; §5's mandated verification ordering; Appendix F's remove-and-re-canonicalise; §3.2.2.3's excluded number algorithm; Appendix B's 2⁶⁸ and ±0 cases; Appendix D/E's lossy remedy; §3.1 I-JSON, closing the duplicate-key claim; §4 no IANA actions |
| `[@rfc-9804]` canonical S-expressions | FX-1 `full` (2026-10-04) | §6.2 uniqueness; §7.2's two-production canonical grammar; §4.6/§4.7 the display-hint crack; §6/§6.3 the brace-wrapped base-64 obligation; §10 as the whole security-considerations section; §11 no IANA actions; §8's sanctioned restrictions; R-0010 on escape sequences |
| `[@secure-systems-lab-dsse]` DSSE | read in full at pinned commit (FX-1 N/A — type `repo`) | `(t, n)` is **not** threshold; `payloadType` SHOULD; *"MUST ignore unrecognized fields"*; `KEYID` MUST NOT be used for security decisions; PAE's length-prefixed framing; Lodato's polyglot attack notebook |
| `library/topics/canonical-encoding.yaml` | `status: answered` (2026-10-08) | The six conditions; the four grounds against option 3; the three-axis costing; the U+FB33 incident; the falsifier |

Secondary, cited once each: `[@rfc-2693]` for `AIntersect` and the 5-tuple;
`[@rfc-8392]`, `[@rfc-9052]` for CWT/COSE as envelope-level identifiers;
`[@macaroons-2014]`, `[@biscuit-spec-3-3]`, `[@ucan-1-0]`,
`[@draft-niyikiza-oauth-attenuating-agent-tokens]`,
`[@draft-asor-wimse-agent-delegation-chain]`, `[@dennis-vanhorn-1966]`,
`[@hardy-1988-confused-deputy]`, `[@did-key-method]` for §4.

## 2a. Added for the comparative anatomy (v0.3.0, §2.2–§2.5)

Retrieval dates are the records' `content.retrieved` at the pin. This pass
fetched nothing itself: it read the records.

| record | retrieved | profile at the pin | what `report.md` takes from it |
|---|---|---|---|
| `[@secure-systems-lab-dsse]` | 2026-10-03 | distilled | PAE; authenticated vs unauthenticated fields; P8's verify-then-parse; P10's same-bytes rule; `t` application-specific; signature format out of band |
| `[@slsa-1-2]` | 2026-10-02 | distilled, FX-1; `reviewed_by` empty | the in-toto Statement's fields and digest map, **second-hand**; *"non-cryptographic digest types"*; subject/predicate/builder checks |
| `[@rfc-9943]` SCITT architecture | 2026-09-26 | distilled, FX-1; protocol and design-notes `reviewed_by` empty | opaque payload; hash-of-payload statements; protected/unprotected headers; TS trust anchors; transparent registration policy; the out-of-scope list; what registration proves |
| `[@rfc-9942]` COSE Receipts | 2026-09-22 | distilled, FX-1; **`reviewed_by` empty on all artifacts** | inclusion and consistency proof shapes and verification order; single-boolean recommendation; what is out of scope; leaks of log size |
| `[@rfc-9052]` COSE | 2026-09-22 | distilled | `Sig_structure`; protected header as bstr; §9 encoding of the to-be-signed bytes only |
| `[@rfc-2693]` SPKI theory | 2026-10-08 | distilled, FX-1 | 5-tuple and 4-tuple; the reduction rule; the ACL as root; key hash as identifier; what is sketched, not specified |
| `[@rfc-2692]` SPKI requirements | 2026-10-08 | summarized | *"signed exactly as it is transmitted"*; vocabulary left to code |
| `[@rfc-9804]` | 2026-10-04 | distilled, FX-1 | canonical form used for signing (§6.2); no authenticated type indicator |
| `[@w3c-rdf-canon-1-0]` | 2026-10-05 | summarized (no `distilled/`) | hashing internal to labelling; no signature defined; no rejection obligation |
| `library/topics/scitt.yaml` | — | answered | *"inherited, not checked"*; detection of a dishonest issuer, not a dishonest log |

**What the frame could not use.** Twenty-three records consulted for the
anatomy are unfilled stubs at the pin: the three in-toto records, CWT, SCRAPI,
RFC 6962, RFC 9162, the SPKI structure draft, SDSI 1.1, Wang 2006, six PICS and
POWDER records, four DID records and the three Merkle papers. And the three VC
specifications have no record at all. They are listed with what would fill
each in `unverified.md`, and are the ingestion candidates of §5.

**Secondary, via R-001** (quoted there, not re-read): §5.6 for DID Core and
`did:key`; §6.1 for PICS; §8.2 and §8.5 for in-toto's layout and trust
assumptions; §11.1–§11.3.

**In-repo, for §4.6–§4.7:** `SPEC-0003` §5.4 and §6; `SPEC-0004` §6.1–§6.4;
`ADR-0003` Decision and D2; `ARCH-0001` §4, §5, §6 and DEC-004;
`BACKLOG-0001` T-041–T-043 and the W-1/W-3 overlap note. All read at `c0c93c3`.

## 3. In-repo evidence, not library records

| source | what it supplies |
|---|---|
| `design-log/0007-rejecting-decoder-spike/` + `prototype/statements/` | §3.10 — the falsifier did not fire; 60 fixtures, 36 negative; the map-order finding; the grammar-versus-rule asymmetry |
| `spec/ARCH-0002-key-relative-naming.md` v0.6.0 | §3.2's P5.1 note and §5.2's P5.2 resolution |
| `spec/ADR-0002-provisional-principles.md` §4 | §3.12 — P4 is held, and the cost of holding it moved to the critical path |
| `research/0001-signatures-and-attestation/report.md` §9, §11, §12 | §4 in full — the accumulation table, the semantic-shift argument, problem 2 |
| `PLAN-0001` §13; `project/meetings/2026-09-28.md` | §3.9 — the two human decisions the evidence postdates |

## 4. Claims carried as withdrawals

Two positions of our own are marked in `report.md` as **withdrawn** rather than
silently corrected, and both withdrawals came from reading a primary source
properly:

1. DSSE's `(t, n)` envelope does **not** carry threshold semantics (§5.1).
2. JCS does **not** leave a duplicate-key hole (§3.4).

A third is **weakened**: option 3's fourth ground, `payloadType` as a forced
global identifier (§5.1).

## 5. Ingestion candidates

**v0.3.0 adds seven, in the order that unblocks most** (detail in
`unverified.md`). They need human approval of the inventory before `bin/ingest`
runs, in the `library` repo opened directly and not in this submodule
(`PROC-0003` §1):

1. `pics-dsig-1-0` and `pics-1-1-labels` — write up the stubs (DSig's digest is
   `not fetched`).
2. **VC Data Model 2.0, VC Data Integrity 1.0, VC-JOSE-COSE** — no records exist.
3. `in-toto-attestation-v1` — write up the stub; §2.2 now reads it second-hand
   through SLSA.
4. `rfc-9162` — every proof guarantee in §2.4 is inherited from it.
5. `draft-ietf-spki-cert-structure` — SPKI's signed structure.

Also: `records/ietf/rfc-8785` does not cite **library#46**, the PR that produced
its design notes; `report.md` §3.4 carries the link instead.

**From v0.2.x: one, and it is already owned.** RDF Canon 1.0 — `w3c-rdf-canon-1-0` carries
`topic: canonical-encoding` at the pin and is **deliberately unread**
(§3.12). It is not a DEC-002 candidate and cannot become one, but it is
plausibly the one ratified algorithm for canonically ordering a set. **library#56
owns reading it.** No other un-recorded source was touched by this pass.
