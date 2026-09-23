---
dimension: specifications
researched: 2026-09-22
confidence: high
---

# CBOR Specification Landscape

All entries below were confirmed against datatracker.ietf.org and/or rfc-editor.org
on 2026-09-22 unless flagged in "Unconfirmed". Dates are month/year of publication
as recorded by the RFC Editor.

## Master table

| Identifier | Exact title | Type | Date | Status/maturity | Obsoletes/Updates | Implementer relevance |
|---|---|---|---|---|---|---|
| RFC 7049 | Concise Binary Object Representation (CBOR) | RFC | Oct 2013 | Proposed Standard, **obsoleted by RFC 8949** | — | Historical only — do not implement against this; superseded | adjacent |
| RFC 8949 | Concise Binary Object Representation (CBOR) | RFC | Dec 2020 | **Internet Standard, STD 94** | Obsoletes RFC 7049 | The core CBOR data format spec, incl. §4.2 deterministic-encoding guidance | core to implement CBOR |
| RFC 8610 | Concise Data Definition Language (CDDL): A Notational Convention to Express CBOR and JSON Data Structures | RFC | Jun 2019 | Proposed Standard | Updated by RFC 9682 | Schema/validation language for CBOR (and JSON) messages | needed for a complete product |
| RFC 9165 | Additional Control Operators for CDDL | RFC | Dec 2021 | Proposed Standard | Extends RFC 8610 (does not formally "Update" it per datatracker metadata) | Adds `.bits`, `.cbor`, `.within`, `.and`, numeric-range/size operators to CDDL | needed for a complete product |
| RFC 9682 | Updates to the Concise Data Definition Language (CDDL) Grammar | RFC | Nov 2024 | Proposed Standard | **Updates RFC 8610** | Fixes/extends CDDL ABNF grammar; required reading alongside 8610 for any CDDL parser | needed for a complete product |
| RFC 9741 | CDDL: Additional Control Operators for the Conversion and Processing of Text | RFC | Mar 2025 | Proposed Standard | Extends CDDL (RFC 8610); does not formally update it | Adds `.abnf`, `.abnfb`, `.feature`, base64/text-conversion control operators to CDDL | needed for a complete product |
| draft-ietf-cbor-cddl-modules-07 | CDDL Module Structure | Internet-Draft | 02 Sep 2026 | Active WG draft, "I-D Exists", intended Standards Track | Extends RFC 8610 | Adds include/import/namespace mechanism for large CDDL models — watch for adoption progress | adjacent |
| draft-ietf-cbor-edn-literals-27 | Concise Diagnostic Notation (CDN) | Internet-Draft | 20 Jul 2026 | **In WG Last Call**, intended Standards Track | Formalizes/updates the informal diagnostic notation described in RFC 8949 & RFC 8610 | Standardizes human-readable CBOR diagnostic notation (EDN) — needed by any tool that prints/parses CBOR-as-text | needed for a complete product |
| RFC 8742 | Concise Binary Object Representation (CBOR) Sequences | RFC | Feb 2020 | Proposed Standard | — | Defines `application/cbor-seq`, concatenation of CBOR items without an enclosing array | needed for a complete product |
| RFC 8746 | Concise Binary Object Representation (CBOR) Tags for Typed Arrays | RFC | Feb 2020 | Proposed Standard | — | Tags 64–87 for homogeneous numeric arrays (typed arrays) | needed for a complete product |
| RFC 8943 | Concise Binary Object Representation (CBOR) Tags for Date | RFC | Nov 2020 | Proposed Standard | — | Tag 100 (days since epoch) and tag 1004 (full-date string) | needed for a complete product |
| RFC 9090 | Concise Binary Object Representation (CBOR) Tags for Object Identifiers | RFC | Jul 2021 | Proposed Standard | — | Tag 111 for OIDs | adjacent |
| RFC 9164 | Concise Binary Object Representation (CBOR) Tags for IPv4 and IPv6 Addresses and Prefixes | RFC | Dec 2021 | Proposed Standard | — | Tags 52/54/260/261 etc. for network addresses/prefixes | adjacent |
| RFC 9277 | On Stable Storage for Items in Concise Binary Object Representation (CBOR) | RFC | Aug 2022 | Proposed Standard | — | Guidance on tag 259-style stable storage / self-describing structures; relevant to long-term archival encoding | adjacent |
| RFC 9581 | Concise Binary Object Representation (CBOR) Tags for Time, Duration, and Period | RFC | Aug 2024 | Proposed Standard | Establishes companion IANA registries for timescales/time-tag map keys | Tags for epoch/duration/period beyond the base RFC 8949 tag 1 (epoch time) | needed for a complete product |
| RFC 8392 | CBOR Web Token (CWT) | RFC | May 2018 | Proposed Standard | Not updated/obsoleted by any RFC as of today (confirmed via datatracker history) | CBOR analogue of JWT; used with COSE for signed/MAC'd/encrypted claims | needed for a complete product |
| RFC 9052 | CBOR Object Signing and Encryption (COSE): Structures and Process | RFC | Aug 2022 | **Internet Standard, STD 96** | Obsoletes RFC 8152 (jointly with RFC 9053); **updated by RFC 9338** | Core COSE structures (Sign1, Mac0, Encrypt0, etc.) used to secure CBOR/CWT payloads | needed for a complete product |
| RFC 9053 | CBOR Object Signing and Encryption (COSE): Initial Algorithms | RFC | Aug 2022 | **Informational** (not part of STD 96) | Obsoletes RFC 8152 (jointly with RFC 9052) | Initial signing/MAC/encryption/key-wrap algorithm set for COSE | needed for a complete product |
| RFC 9054 | CBOR Object Signing and Encryption (COSE): Hash Algorithms | RFC | Aug 2022 | Informational | Does not obsolete RFC 8152; companion to 9052/9053 | Registers SHA-1/SHA-2/SHA-3/SHAKE hash algorithm identifiers for COSE | adjacent |
| RFC 9338 | CBOR Object Signing and Encryption (COSE): Countersignatures | RFC | Dec 2022 | **Internet Standard, STD 96** (with RFC 9052) | **Updates RFC 9052** | Adds countersignature header parameters/algorithms fixing security issues in RFC 8152's countersign design | needed for a complete product |
| RFC 9360 | CBOR Object Signing and Encryption (COSE): Header Parameters for Carrying and Referencing X.509 Certificates | RFC | Feb 2023 | Proposed Standard | Does not update prior RFCs; builds on RFC 9052 | x5bag/x5chain/x5t/x5u header params for X.509 in COSE | needed for a complete product |
| RFC 9597 | CBOR Web Token (CWT) Claims in COSE Headers | RFC | Jun 2024 | Proposed Standard | Does not formally update RFC 8392; extends it | Lets CWT claims appear in COSE header (not just payload) — relevant to newer CWT-based protocols (e.g. mdoc-style credentials) | adjacent |
| draft-ietf-cbor-serialization-08 | CBOR Serialization and Determinism | Internet-Draft | 29 Jul 2026 | **In WG Last Call**, intended Standards Track | Effectively the current successor/consolidation of the deterministic-encoding effort (general/preferred-plus/deterministic serialization classes) | THE document to watch for "how do I get deterministic CBOR" — supersedes the parked CDE draft in practice | needed for a complete product |
| draft-ietf-cbor-cde-13 | CBOR Common Deterministic Encoding (CDE) | Internet-Draft | 13 Oct 2025 | **Expired / Parked WG document** (intended as BCP) | Predecessor effort now effectively folded into draft-ietf-cbor-serialization | Historical — do not treat as the current determinism spec | adjacent |
| draft-mcnally-deterministic-cbor-18 | dCBOR: Deterministic CBOR | Internet-Draft (individual, non-WG) | 10 Aug 2026 | **Active**, but explicitly "no formal standing in the IETF standards process"; expires 11 Feb 2027 | Independent narrowing-rules profile for deterministic CBOR | Used by some ecosystems (e.g. Blockchain Commons / Gordian) as a de facto determinism profile; not an IETF WG product | adjacent |
| draft-ietf-cbor-packed-19 | Packed CBOR | Internet-Draft | 02 Feb 2026 | **Expired**; datatracker shows it "Waiting for WG Chair Action" | Tags/simple values for compacting repetitive CBOR structures | Compression scheme for CBOR — track for future revival/adoption, not yet stable | adjacent |
| draft-ietf-cbor-edn-e-ref-03 | External References to Values in CBOR Diagnostic Notation (EDN) | Internet-Draft | expired | Expired | Extension to CDN/EDN | Niche — only relevant to diagnostic-notation tooling | adjacent |
| IETF CBOR Working Group | (charter) | WG | active | Chartered WG; current milestone: "Updated version of CDDL, replacing RFC 8610 and its updates, to be submitted to IESG" by **30 Jun 2027** | — | Chairs: Barry Leiba, Christian Amsüss, Paul E. Hoffman. List: cbor@ietf.org | needed for a complete product |
| IANA CBOR Tags registry | Concise Binary Object Representation (CBOR) Tags | Registry | ongoing | Governed by RFC 8949 (references RFC 9581 for companion timescale/time-map-key registries) | Tag ranges: 0–23 Standards Action; 24–32767 Specification Required; 32768–2^64-1 First Come First Served | Authoritative source for all registered tag semantics (400+ entries) | core to implement CBOR |
| IANA CBOR Simple Values registry | Concise Binary Object Representation (CBOR) Simple Values | Registry | ongoing | Governed by RFC 8949 | 0–19 Standards Action; 32–255 Specification Required | Authoritative source for simple-value semantics (false/true/null/undefined + extensions) | core to implement CBOR |
| IANA COSE registries | COSE Header Parameters / Header Algorithm Parameters / Algorithms / Key Common Parameters / Key Type Parameters / Key Types / Elliptic Curves / Verifiable Data Structure Algorithms / Verifiable Data Structure Proofs | Registry group | ongoing | Governed by RFC 9052/9053/etc.; tiered Standards-Action-With-Expert-Review / Specification-Required / Expert-Review by numeric range | Authoritative source for all COSE algorithm and parameter identifiers | needed for a complete product |

## Notes on determinism (RFC 8949 §4.2 vs CDE vs dCBOR)

- RFC 8949 §4.2 itself only describes *a* deterministic encoding recipe (sorted map
  keys, shortest-form integers/floats, no indefinite-length items) as an optional
  mode — it is not a separate document.
- The WG's follow-on attempt to codify "Common Deterministic Encoding" as its own
  BCP (draft-ietf-cbor-cde) is **expired and parked** as of the last revision
  (13 Oct 2025).
- That effort has been effectively superseded in WG activity by
  **draft-ietf-cbor-serialization** (currently rev -08, in WG Last Call, dated
  29 Jul 2026), which defines three serialization tiers (general / preferred-plus /
  deterministic) and is the document to cite for "how do I do deterministic CBOR"
  going forward. It is not yet an RFC.
- **dCBOR** (draft-mcnally-deterministic-cbor, currently rev -18, dated 10 Aug 2026)
  is a separate, non-WG individual submission with no IETF standing. It is used in
  some application ecosystems but should not be presented as an IETF standard.

## Notes on Packed CBOR

- draft-ietf-cbor-packed is at revision -19 (02 Feb 2026) and is currently
  **expired**, with datatracker showing it "Waiting for WG Chair Action" rather
  than active WG Last Call. Its status should be re-checked before citing it as
  a near-term standard — this is the least stable item in this table.

## Recent status changes worth flagging

- RFC 9682 (Nov 2024) updates RFC 8610 — anyone implementing CDDL against only
  RFC 8610 needs to layer this grammar fix in.
- RFC 9741 (Mar 2025) is the newest published CDDL control-operator RFC (text
  conversion operators) — postdates RFC 9165.
- draft-ietf-cbor-serialization and draft-ietf-cbor-edn-literals both entered
  **WG Last Call** with July 2026 revisions — both are close to becoming RFCs;
  worth re-checking status at next review.
- draft-ietf-cbor-cde moved from "active WG document" to **expired/parked**
  (BCP track abandoned in favor of the serialization draft).

## Sources

- https://www.rfc-editor.org/rfc/rfc8949.html (retrieved 2026-09-22)
- https://datatracker.ietf.org/doc/rfc8949/ (retrieved 2026-09-22)
- https://datatracker.ietf.org/doc/rfc7049/ (retrieved 2026-09-22)
- https://datatracker.ietf.org/doc/rfc8610/ (retrieved 2026-09-22)
- https://datatracker.ietf.org/doc/rfc9165/ (retrieved 2026-09-22)
- https://datatracker.ietf.org/doc/rfc9682/ (retrieved 2026-09-22)
- https://datatracker.ietf.org/doc/rfc9741/ (retrieved 2026-09-22)
- https://datatracker.ietf.org/doc/rfc8742/ (retrieved 2026-09-22)
- https://datatracker.ietf.org/doc/rfc8746/ (retrieved 2026-09-22)
- https://datatracker.ietf.org/doc/rfc8943/ (retrieved 2026-09-22)
- https://datatracker.ietf.org/doc/rfc9090/ (retrieved 2026-09-22)
- https://datatracker.ietf.org/doc/rfc9164/ (retrieved 2026-09-22)
- https://datatracker.ietf.org/doc/rfc9277/ (retrieved 2026-09-22)
- https://datatracker.ietf.org/doc/rfc9581/ (retrieved 2026-09-22)
- https://datatracker.ietf.org/doc/rfc8392/ (retrieved 2026-09-22)
- https://datatracker.ietf.org/doc/rfc8392/history/ (retrieved 2026-09-22)
- https://datatracker.ietf.org/doc/rfc9052/ ; https://www.rfc-editor.org/info/rfc9052 (retrieved 2026-09-22)
- https://datatracker.ietf.org/doc/rfc9053/ (retrieved 2026-09-22)
- https://datatracker.ietf.org/doc/rfc9054/ ; https://www.rfc-editor.org/info/rfc9054 (retrieved 2026-09-22)
- https://datatracker.ietf.org/doc/rfc9338/ ; https://www.rfc-editor.org/info/rfc9338 (retrieved 2026-09-22)
- https://datatracker.ietf.org/doc/rfc9360/ (retrieved 2026-09-22)
- https://datatracker.ietf.org/doc/rfc9597/ (retrieved 2026-09-22)
- https://www.rfc-editor.org/info/std94 (retrieved 2026-09-22)
- https://datatracker.ietf.org/wg/cbor/documents/ (retrieved 2026-09-22)
- https://datatracker.ietf.org/wg/cbor/about/ (retrieved 2026-09-22)
- https://datatracker.ietf.org/doc/draft-ietf-cbor-packed/ (retrieved 2026-09-22)
- https://datatracker.ietf.org/doc/draft-ietf-cbor-cde/ (retrieved 2026-09-22)
- https://datatracker.ietf.org/doc/draft-mcnally-deterministic-cbor/ (retrieved 2026-09-22)
- https://datatracker.ietf.org/doc/draft-ietf-cbor-serialization/ (retrieved 2026-09-22)
- https://datatracker.ietf.org/doc/draft-ietf-cbor-edn-literals/ (retrieved 2026-09-22)
- https://datatracker.ietf.org/doc/draft-ietf-cbor-cddl-modules/ (retrieved 2026-09-22)
- https://www.iana.org/assignments/cbor-tags/cbor-tags.xhtml (retrieved 2026-09-22)
- https://www.iana.org/assignments/cbor-simple-values/cbor-simple-values.xhtml (retrieved 2026-09-22)
- https://www.iana.org/assignments/cose/cose.xhtml (retrieved 2026-09-22)

## Unconfirmed

- draft-ietf-cbor-edn-e-ref-03 exact expiration/revision date — datatracker listing
  showed it in the WG's expired-drafts list but I did not fetch its individual
  document page to confirm the exact date/status text; treat the "expired" status
  as provisional until directly re-checked.
- Whether RFC 9165 and RFC 9741 carry a formal datatracker "Updates: RFC 8610"
  relationship or are merely additive extensions — the fetched summaries were
  inconsistent on this point (RFC 9165's own text frames itself as additive
  rather than a formal Update, unlike RFC 9682 which datatracker explicitly
  lists as "Updates RFC 8610"). Recommend a direct check of each RFC's masthead
  metadata (the "Updates:" line on page 1) before asserting a formal relationship
  either way.
- Exact current substantive content/milestone detail for draft-ietf-cbor-packed's
  "Waiting for WG Chair Action" state (e.g., whether this means re-adoption,
  advancement to WGLC, or something else) — only the state label was retrieved,
  not the shepherd writeup or chair notes.
