---
schema: "library-doc/v1"
id: R-0006-sources
title: "Sources consulted — mechanism"
type: evidence
status: draft
version: "0.1.0"
date: "2026-10-14"
updated: "2026-10-14"
---

# Sources

Bibliography pinned at **`library@f57dcbc`**. Every `[@key]` in `report.md`
resolves at that commit; checked mechanically, **15 distinct keys, zero
unresolved.**

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

**One, and it is already owned.** RDF Canon 1.0 — `w3c-rdf-canon-1-0` carries
`topic: canonical-encoding` at the pin and is **deliberately unread**
(§3.12). It is not a DEC-002 candidate and cannot become one, but it is
plausibly the one ratified algorithm for canonically ordering a set. **library#56
owns reading it.** No other un-recorded source was touched by this pass.
