---
dimension: applications
researched: 2026-09-22
confidence: medium
---

# CBOR Applications: Use-Case Patterns and What They Demand of an Implementation

Scope note: this file covers the **applications** dimension — for each pattern,
what it is, why CBOR (RFC 8949 / STD 94) was chosen, and which specific CBOR
features an implementation is forced to get right. It closes with an
implementer's completeness checklist and a determinism-divergence comparison
(RFC 8949 §4.2 vs CTAP2 canonical CBOR vs CDE vs dCBOR), which is the
highest-value analytical content here.

---

## 1. Signed / attested data — COSE, CWT, EAT, mdoc, SD-CWT

**Pattern.** A payload (claims, a public key, a device identity, a fact about
provenance) is wrapped in a signing/MACing/encryption envelope and the
resulting bytes are transmitted, stored, or embedded in another format. The
receiver must reproduce byte-for-byte what the signer signed in order to
verify. This is the family with the tightest coupling to CBOR's encoding
determinism, because **the signature covers bytes, not a data model** — any
two encoders that emit different (but semantically equal) bytes for the same
logical structure will produce a signature mismatch or a verification bypass
if the verifier is lax about what it re-serializes.

- **COSE** (RFC 9052, "CBOR Object Signing and Encryption") defines
  `COSE_Sign1` as a 4-element array: `[protected, unprotected, payload,
  signature]`, where `protected` is itself **bstr-wrapped** CBOR (a map
  serialized to bytes and embedded as a byte string) — RFC 9052 §4.2, §4.4.
  Tag 18 identifies a tagged `COSE_Sign1`. The signature is computed over a
  `Sig_structure` that itself must be serialized "using the encoding
  described in Section 9" — i.e., the signer picks one canonical byte
  sequence, and the `protected` bstr is carried *verbatim* (not
  re-encoded) precisely so that verifiers don't need to reproduce the
  signer's serialization choices for that piece — only for the outer
  `Sig_structure` wrapper.
  (Source: https://www.rfc-editor.org/rfc/rfc9052.html, retrieved 2026-09-22)
- **CWT** (RFC 8392, "CBOR Web Token") is a COSE-wrapped CBOR map of claims,
  using small integer claim keys (iss=1, sub=2, aud=3, exp=4, nbf=5, iat=6,
  cti=7) specifically because "the use of JSON for encoding information ...
  is considered inefficient for some Internet of Things systems that use
  low-power radio technologies" (RFC 8392 §1). It forbids tag-prefixing
  standard claim values to minimize bytes (§5).
  (https://www.rfc-editor.org/rfc/rfc8392.html, retrieved 2026-09-22)
- **EAT** (RFC 9711, "Entity Attestation Token") layers device/remote
  attestation claims (UEID, debug state, boot measurements, nested
  "submodules") on top of CWT or JWT, explicitly reusing COSE/JOSE for
  "authenticity, integrity, and optionally confidentiality" (§1.2), and
  supports detached claims sets for modular attestation.
  (https://www.rfc-editor.org/rfc/rfc9711.html, retrieved 2026-09-22)
- **mdoc / ISO 18013-5** (mobile driver's license, and its EUDI-wallet
  descendants) wraps the `MobileSecurityObject` and `DeviceNameSpaces`
  structures using **CBOR tag 24** (`#6.24(bstr .cbor X)`) — "embedded CBOR
  data item" — inside a `COSE_Sign1`'s payload, so that the exact bytes that
  were hashed/signed by the issuer are preserved untouched through
  transport and selective disclosure, rather than being reconstructed by
  re-encoding a parsed data model (which could silently change bytes).
  (Multiple secondary implementer sources, e.g. go-mdoc/eudi-lib codebases;
  retrieved via search 2026-09-22 — primary spec ISO/IEC 18013-5:2021 is
  paywalled and not fetchable directly.)
- **SD-CWT** (draft-ietf-spice-sd-cwt, active WG item as of 2026-09-22) is
  the CBOR/COSE analogue of SD-JWT: claims are individually "salted"
  (128-bit salt + claim name + value), hashed, and the hash ("Blinded Claim
  Hash") replaces the claim in the signed CWT payload; a holder discloses
  only the salted claim needed, and a verifier recomputes the hash to
  match it against the signed set. A Key Binding Token adds an `sd_hash`
  claim over the disclosed set.
  (https://datatracker.ietf.org/doc/html/draft-ietf-spice-sd-cwt-07,
  retrieved 2026-09-22)

**What this forces on an implementation:**
- Correct bstr-wrapping/unwrapping (embed a full child CBOR item inside a
  byte string, both directly per COSE's `protected` field and via tag 24 for
  mdoc) — an encoder must serialize the *inner* item first, byte-for-byte,
  and treat the result as opaque bytes for the outer structure, never
  re-derive it from the parsed model on the verify side.
  - **Tag validity for tag 24**: content MUST be a byte string containing
    well-formed CBOR (RFC 8949 §3.4.5.1); wrapping the wrong type is a tag
    validity error (RFC 8949 §5.3.2).
- Deterministic/canonical encoding of at least the signed structure
  (`Sig_structure`, `protected` header map) — otherwise two logically
  identical objects sign to different bytes, and libraries that
  "canonicalize-then-verify" instead of "verify-the-actual-bytes" open a
  parser-differential attack surface (see §"Sharp edges" below).
- Tag handling and tag-number registry awareness (18/96/97/98 for COSE
  message types; 24 for embedded CBOR).
- Selective disclosure requires stable hashing of individually-serialized
  CBOR sub-items (SD-CWT) — implementation must serialize each disclosed
  claim deterministically before hashing, or a legitimate re-encoding would
  break hash matching.

---

## 2. Constrained-device messaging — CoAP, LwM2M, SenML, OSCORE

**Pattern.** Battery- or flash-constrained nodes (6LoWPAN/802.15.4 sensors,
NB-IoT modems) exchange small, frequent messages over lossy, low-bandwidth
links. CBOR is chosen because it is binary (denser than JSON), has a tiny
generic-decoder footprint, and supports **streaming/indefinite-length
encoding** so a sender doesn't need to buffer a whole message to know its
length up front.

- **CoAP** (RFC 7252) is the constrained HTTP-analogue transport; CBOR
  payloads (`application/cbor`) are one of its standard content-formats.
- **SenML** (RFC 8428, "Sensor Measurement Lists") defines both JSON and
  CBOR representations of sensor readings; the CBOR form uses **integer
  labels instead of text labels** for compactness (§6), and the format is
  explicitly designed to be implementable "in roughly 1 KB of flash on an
  8-bit microprocessor" (§2). Base Name/Time/Unit/Value fields let a
  sequence of records avoid repeating shared prefixes/offsets.
  (https://www.rfc-editor.org/rfc/rfc8428.html, retrieved 2026-09-22)
- **OSCORE** (RFC 8613) end-to-end-encrypts CoAP messages using an
  untagged `COSE_Encrypt0` structure, but further **compresses** the COSE
  envelope for the stateful CoAP request/response pattern (removing fields
  recoverable from context) because "COSE is constructed to support ...
  stateless use cases and is not fully optimized for use as a stateful
  security protocol, leading to a larger than necessary message expansion"
  (§6). Compression brought a typical request from 24 bytes (full COSE) to
  17 bytes (§6.3).
  (https://www.rfc-editor.org/rfc/rfc8613.html, retrieved 2026-09-22)
- **LwM2M** (OMA SpecWorks) uses SenML-CBOR and plain CBOR as one of its
  wire formats for the same reasons.

**What this forces on an implementation:**
- Small code size / no dynamic allocation: a "generic decoder" must run in
  ~1 KB flash class environments (SenML §2) — this pushes toward
  streaming/pull decoders over full-tree DOM decoders.
- **Indefinite-length item handling**: CBOR's streaming major-type-2–5
  "break"-terminated forms exist specifically so an encoder need not know
  a string/array/map's length in advance (RFC 8949 §3.2.1) — a constrained
  encoder emitting sensor data as it's produced relies on this; the decoder
  must correctly reassemble indefinite-length byte/text string chunks and
  refuse nesting an indefinite-length string inside another indefinite
  string chunk (disallowed by design, RFC 8949 §3.2.3, "to keep decoders
  from needing a stack for this specifically").
- Partial/streaming parsing: OSCORE and CoAP both push message contents
  through intermediaries and partial buffers — decoder must be resumable
  or work incrementally without the whole message in memory.
- Compact/omittable framing: OSCORE strips COSE structure that's
  recoverable from context, meaning the implementation must track protocol
  state (sequence numbers, partial IVs) outside the CBOR item itself.

---

## 3. Configuration and management — YANG-CBOR, CORECONF, SID

**Pattern.** Network/device configuration data modeled in YANG (used by
NETCONF/RESTCONF over XML/JSON) needs a compact wire form for constrained
management agents. YANG-CBOR + CORECONF is that binding.

- **RFC 9254** ("Encoding of Data Modeled with YANG in CBOR") maps YANG data
  nodes into CBOR, using **YANG Schema Item iDentifiers (SIDs)** — 63-bit
  unsigned integers — as CBOR map keys in place of YANG's string
  identifiers, explicitly "to minimize the size of the encoded data" (§3.4).
  SIDs used as map keys are further **delta-encoded** against a reference
  SID for the map (§3.2), trading a small integer-arithmetic cost for
  smaller payloads. CoAP Content-Format 140
  (`application/yang-data+cbor; id=sid`) is registered for this (§7).
  (https://www.rfc-editor.org/rfc/rfc9254.html, retrieved 2026-09-22)
- **draft-ietf-core-sid** defines the SID number space, registration, and a
  `.sid` file format (tooling: pyang) that maps YANG identifiers to their
  globally unique numeric SIDs.
  (https://datatracker.ietf.org/doc/draft-ietf-core-sid/, retrieved
  2026-09-22)
- **CORECONF** (draft-ietf-core-comi, still in active WG revision as of
  2026-09-22, rev -21 dated 2026-03-02) is the CoAP-based management
  protocol ("CoAP Management Interface") layered on YANG-CBOR, extending
  NETCONF/RESTCONF's data model to constrained nodes and networks, using
  CoAP POST for creation/RPC/action invocation.
  (https://datatracker.ietf.org/doc/draft-ietf-core-comi/, retrieved
  2026-09-22)

**What this forces on an implementation:**
- **Integer-keyed maps** are not just an optimization here but the wire
  contract: a decoder must resolve integer SIDs back to YANG schema nodes
  using an externally supplied `.sid` map — i.e., **schema-driven decode**,
  not self-describing decode. A generic "decode CBOR to JSON-like tree"
  library is necessary but not sufficient; the application needs a
  SID↔YANG-node table and delta-decoding logic for map keys.
  - CDDL-style schema validation is a natural fit for verifying that
    decoded CORECONF payloads match the YANG-derived structure.

---

## 4. Ledger / consensus serialization — Cardano

**Pattern.** Blockchain transactions and blocks must be serialized so that
independent nodes agree on identical bytes for hashing, signing, and
consensus; the ledger uses CBOR (with CDDL schemas) for transaction bodies,
Plutus data, and blocks.

- Cardano's ledger CDDL specifications (`cardano-ledger` repo, e.g.
  `conway.cddl`) define the on-chain structures. **The Cardano ledger itself
  does not currently enforce a canonical transaction encoding** — decoding a
  transaction and re-encoding it is not guaranteed to reproduce the same
  bytes, which matters because transaction hashes and signatures are
  computed over the *original* encoded bytes, not a re-derived canonical
  form.
- **CIP-21** ("Transaction requirements for interoperability with hardware
  wallets") was proposed specifically to get software wallets and hardware
  wallets to agree on a **deterministic serialization** so a hardware
  wallet's displayed/signed transaction body can be reproduced exactly by
  host software, addressing the practical problem that re-encoding a
  parsed transaction can reorder inputs or change Plutus datum encoding,
  altering the transaction hash and invalidating signatures.
  (https://cips.cardano.org/cip/CIP-21, retrieved via search 2026-09-22)
- Common implementer guidance (e.g. PyCardano, cardano-serialization-lib
  issue trackers) converges on: **always preserve original transaction
  bytes**; never round-trip decode→re-encode when the bytes must remain
  hash-stable.

**What this forces on an implementation:**
- **Byte-exact round-tripping**: the library must expose (or default to)
  "keep original bytes" semantics for anything that will be hashed or
  re-signed, rather than "decode to native structure, re-encode on
  output" — a correctness requirement stronger than mere determinism,
  because determinism only helps once *everyone* encodes canonically, and
  the base ledger does not require that.
- Where canonical encoding *is* wanted (CIP-21, cross-tool
  interoperability), the implementation needs an actual deterministic-CBOR
  mode (shortest-form integers/lengths, sorted map keys, no indefinite
  lengths) applied consistently by both the signer and the verifier.
- Correct handling of Plutus "Data" encoding (large integers via bignum
  tags 2/3, constructor-tagged sum types) without perturbing byte layout.

---

## 5. Authenticator protocols — CTAP2 / WebAuthn

**Pattern.** FIDO2 hardware authenticators (security keys, platform
authenticators) exchange CBOR-encoded requests/responses with the host over
USB/NFC/BLE; WebAuthn's `attestationObject` and COSE public keys are CBOR.
CBOR was chosen for its small decoder footprint on memory-constrained
security hardware and its self-describing yet compact structure.

- CTAP2 (FIDO Alliance, CTAP 2.1, §8 "Message Encoding") **mandates its own
  "CTAP2 canonical CBOR encoding form"**, stating explicitly that it
  "differs from the canonicalization suggested in Section 3.9 of
  [RFC8949]" (i.e., differs from what RFC 8949 §4.2 calls "core
  deterministic encoding"/what predecessor RFC 7049 called "Canonical
  CBOR"). Verbatim rule set (CTAP2.1 spec, §8, retrieved 2026-09-22 from
  https://fidoalliance.org/specs/fido-v2.1-ps-20210615/fido-client-to-authenticator-protocol-v2.1-ps-20210615.html):
  - Integers as small as possible (identical size-class rules to RFC 8949
    §4.2.1).
  - "The representations of any floating-point values are not changed" —
    i.e., **no float-shortening**; a 16-, 32-, and 64-bit encoding of the
    numeric value 1.5 are treated as *distinct, independently canonical*
    values, because CTAP2 considers the float's storage width part of its
    semantic meaning.
  - Lengths in major types 2–5 as short as possible.
  - Indefinite-length items MUST be made definite-length.
  - **Map key sort**: "sorted lowest value to highest" using a three-part
    rule: (1) lower major type sorts first; (2) shorter encoded key sorts
    first; (3) ties broken by bytewise lexical order. CTAP2 itself notes
    this is *only* equivalent to RFC 8949's pure bytewise-lexicographic
    sort for major types 0–3 and 7 (ints, strings, simple values) — the
    two diverge for types 4–6 (arrays/maps/tags used as keys), which CTAP2
    doesn't use as keys but flags as a compatibility landmine if it ever
    does.
  - **"Tags ... MUST NOT be present"** at all — a stricter rule than RFC
    8949, which permits tags in deterministic encoding provided a protocol
    fixes their presence/absence (§4.2.2).
  - Nesting depth capped at 4 levels of combined map/array nesting;
    authenticators MUST support at least 4 and other parties MUST NOT
    exceed 4 (memory-constrained hardware).
  - Default max message size 1024 bytes unless `maxMsgSize` says otherwise.
  - Unknown map keys MUST be ignored (forward compatibility, not a
    determinism rule but adjacent decoder behavior).
  (Verified by direct fetch/grep of CTAP2.1 spec HTML, 2026-09-22.)

**What this forces on an implementation:**
- A **distinct canonicalization mode** from RFC 8949/CDE — an
  implementation that only supports RFC 8949 §4.2 "core deterministic
  encoding" cannot correctly validate or produce CTAP2 messages; it needs
  the length-first-with-major-type-priority map sort AND a "never
  shorten floats" rule AND a "no tags ever" rule as a separately
  selectable policy.
- Depth-limited, bounded-size decoding by construction (hardware token
  memory limits) — reinforces the general DoS-resistance requirement but
  with concrete numbers (4 levels, 1024 bytes default) rather than "some
  reasonable limit."
- Because verifiers (browsers, servers) that check `attestationObject`
  bytes may apply RFC 8949-style tooling by habit, an implementation must
  be deliberate about which canonical form it is checking against — using
  the wrong one either rejects valid CTAP2 output or accepts CTAP2 output
  that isn't actually canonical per its own rules.

---

## 6. Content provenance and media manifests — C2PA, JPEG Trust

**Pattern.** Media files (images, video) carry an embedded, cryptographically
signed "manifest" describing edit history/provenance; the manifest format
must hold large embedded binary assets (thumbnails, ingredient hashes) plus
signed structured claims.

- **C2PA Technical Specification**: "the majority of assertions, as well as
  the claim and the claim signature are all serialized as CBOR (RFC 7049)",
  with extensibility for JSON-LD/XML/arbitrary binary via typed boxes.
  - The **claim signature** is a `COSE_Sign1_Tagged` structure (a
    CBOR tag byte followed by the 4-element COSE_Sign1 array) — same
    dependency on bstr-wrapped protected headers as in §1 above.
  - **Data boxes** hold arbitrary binary content referenced from an
    assertion, as a single CBOR "Content Type" box whose `data` field is a
    **bstr carrying the raw bytes directly** (not further CBOR-encoded),
    used to keep large embedded binary (e.g., thumbnails) out of the
    signed assertion structure itself while still being covered by the
    manifest's hash tree.
  (https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html,
  retrieved via search 2026-09-22; version-numbered spec family 1.0–2.4+.)
- JPEG Trust (JPEG committee's trust/provenance initiative) builds on
  similar C2PA-style manifest/COSE patterns for JPEG-native provenance
  metadata (lower confidence — not independently fetched from a JPEG Trust
  primary spec in this pass; flagged in Open Questions).

**What this forces on an implementation:**
- **Large bstr handling**: byte strings carrying multi-megabyte embedded
  assets (thumbnails, ingredient data) must not be forced through a
  decoder path that assumes small in-memory strings; on 32-bit targets
  this intersects the "64-bit length on 32-bit target" sharp edge (a
  crafted or legitimately large asset can specify a byte-string length
  that overflows `size_t`/`usize` on 32-bit platforms unless the decoder
  checks against actual remaining input length before allocating).
- Correct tag-plus-array parsing for `COSE_Sign1_Tagged` (major type 6 tag
  byte immediately preceding a 4-element array) as a specific, must-not-get
  it-wrong parse path, since a manifest with malformed/absent tag either
  breaks interop or silently accepts an unsigned/mistyped structure.
- Because manifests are meant to be forwarded/embedded across file-format
  boundaries (JPEG segments, MP4 boxes, etc.) without alteration, the
  same "preserve exact bytes, don't round-trip through a re-encoder"
  discipline as COSE/mdoc/Cardano applies to the signed portions.

---

## 7. Telemetry / logging at volume — CBOR Sequences (RFC 8742)

**Pattern.** A system emits a continuous or very large stream of independent
CBOR data items (log records, telemetry samples) that should not require
being wrapped in one giant top-level array (which would need its total
length known up front, or indefinite-length framing that some tooling
dislikes) nor re-parsed/re-serialized entirely each time a new record is
appended.

- **RFC 8742** defines a CBOR Sequence recursively: "a CBOR Sequence is a
  sequence of bytes that is either an empty sequence or an encoded CBOR
  data item followed by a CBOR Sequence" — i.e., simple concatenation of
  self-delimiting top-level items, no wrapping array, no separators needed
  because each CBOR item is self-delimiting. Registers media type
  `application/cbor-seq`, the `+cbor-seq` structured syntax suffix, and
  CoAP Content-Format ID 63.
  (https://www.rfc-editor.org/rfc/rfc8742.html, retrieved 2026-09-22)
- This directly enables append-only logs: a decoder can "consume and
  produce incrementally without requiring a streaming CBOR parser that
  delivers substructures incrementally" — you only need a decoder that can
  read "one item, then try to read another," which is a much lower bar
  than a fully incremental/streaming decoder.

**What this forces on an implementation:**
- A **sequence-aware decode loop**: `decode_one() -> (item, remaining_bytes)`
  repeated until input exhausted, distinct from "decode exactly one
  top-level item and error on trailing bytes" (RFC 8949 Appendix F's "too
  much data" well-formedness error class — an implementation must be able
  to *not* treat trailing bytes as an error when operating in sequence
  mode).
  - This is exactly the RFC 8949 Appendix F carve-out: "This is only an
    error if the application assumed that the input bytes would span
    exactly one data item. Where the application uses the self-delimiting
    nature of CBOR encoding to permit additional data after the data item,
    as is done in CBOR sequences [RFC8742] ... the CBOR decoder can simply
    indicate which part of the input has not been consumed."
    (RFC 8949, Appendix F; https://www.rfc-editor.org/rfc/rfc8949.html,
    retrieved 2026-09-22)
- Streaming decode without unbounded buffering: high-volume telemetry
  needs a decoder that can process and discard each item without holding
  the entire log/session in memory.

---

## 8. Schema validation and interop — CDDL, test vectors, diagnostic notation

**Pattern.** CBOR (and JSON) message formats need a way to be specified
unambiguously for interop testing, code generation, and human review without
hand-writing hex dumps.

- **CDDL** (RFC 8610, "Concise Data Definition Language") — "proposes a
  notational convention to express CBOR data structures ... to provide an
  easy and unambiguous way to express structures for protocol messages and
  data formats that use CBOR or JSON" (Abstract). Used pervasively by the
  specs above (COSE, CWT, mdoc, YANG-CBOR, Cardano ledger) to define wire
  structures formally, and by tooling to generate/validate test vectors
  (RFC 8610 Appendix F: reference tool; Appendix H: worked CDDL+instance
  examples).
  (https://www.rfc-editor.org/rfc/rfc8610.html, retrieved 2026-09-22)
- **Diagnostic notation**: RFC 8949's own §8 (informative) gives CBOR a
  human-readable text form for debugging/spec examples; RFC 8610 Appendix G
  extended this into "Extended Diagnostic Notation" (EDN) with byte-string
  text embedding, hex/octal/binary literals, CBOR-sequence embedding, and
  comments.
- **draft-ietf-cbor-edn-literals** (active WG draft, rev -24 line as of
  2026-09-22) formally consolidates and **obsoletes both** RFC 8949 §8 and
  RFC 8610 Appendix G as the single normative EDN reference, adding two
  IANA registries (encoding indicators; application-oriented literal
  forms) and new literal forms for epoch date/times, IP addresses/prefixes,
  and hash-value literals.
  (https://datatracker.ietf.org/doc/draft-ietf-cbor-edn-literals/,
  retrieved 2026-09-22)
- **CBOR Common Deterministic Encoding (CDE)**, itself expressed partly via
  CDDL, adds `.cde` and `.cdeseq` CDDL control operators that require the
  matched data item(s) to additionally satisfy CDE, not just be
  well-formed/valid CBOR — a schema-language hook for determinism testing.
  (draft-ietf-cbor-cde, §4; retrieved 2026-09-22)

**What this forces on an implementation:**
- A CDDL-capable validator (or at least a decoder exposing enough type
  information — major type, tag numbers, map/array shape) to check decoded
  data against a schema, separate from basic well-formedness.
- Support for diagnostic-notation round-tripping is valuable for test
  suites (encode → diagnostic string → compare against fixture) — pushes
  toward exposing an EDN encoder/decoder alongside the binary codec.
- Awareness that EDN's normative home is moving out of RFC 8949/8610 and
  into the dedicated edn-literals draft — a reference implementation
  written against "RFC 8949 §8" alone will miss newer literal forms.

---

## Implementer's completeness checklist

| Feature | Why it matters | Which application(s) force it | Spec locator |
|---|---|---|---|
| Shortest-form integer/length/tag encoding ("preferred serialization") | Baseline for any deterministic mode; smaller wire size | All signed-data and ledger patterns; CTAP2; CDE/dCBOR | RFC 8949 §4.2.1; CTAP2.1 §8 |
| Shortest-form float encoding (16→32→64 bit shortening) | Deterministic byte output for hashing/signing | RFC 8949 CDE/dCBOR determinism | RFC 8949 §4.2.1 — **but CTAP2 explicitly forbids this** (§8: "representations of any floating-point values are not changed") |
| Bytewise-lexicographic map key sort on *encoded* key | Canonical map ordering for hash/signature stability | COSE/CWT/EAT canonicalization; CDE; dCBOR | RFC 8949 §4.2.1 |
| Length-first (then lexical) map key sort — the *older* RFC 7049 order | Needed to interop with legacy "Canonical CBOR" implementations and CTAP2 | CTAP2 (adds a 3rd, major-type-first tier on top) | RFC 8949 §4.2.3; CTAP2.1 §8 |
| Indefinite-length item support (arrays/maps/byte-/text-strings + "break") | Streaming encode without knowing size up front | CoAP/SenML/OSCORE constrained streaming | RFC 8949 §3.2, §3.2.1 |
| Reject nested indefinite-length string chunks | Prevents unbounded decoder stack growth | Any decoder accepting untrusted CBOR (esp. constrained/embedded) | RFC 8949 §3.2.3 |
| Disallow/forbid indefinite lengths under a deterministic mode | Determinism requires one canonical byte form | COSE/CWT canonicalization; CDE; dCBOR; CTAP2 | RFC 8949 §4.2.1; CTAP2.1 §8 |
| Duplicate map key detection and defined behavior (reject, or first/last-wins, documented) | "Well-formed but not valid"; divergent handling across decoders is a parser-differential security bug (e.g., signature covers one interpretation, business logic uses another) | COSE/CWT verifiers; WebAuthn/CTAP2 (MUST reject); general security-sensitive decode | RFC 8949 §3 (map def.), §5.3.1; CTAP2.1 §8 ("MUST serialize ... without duplicate map keys"; decoders "SHOULD reject") |
| bstr-wrapping / tag 24 "embedded CBOR" correct nesting | Preserve exact signed bytes across a structural boundary | COSE `protected` header; mdoc `MobileSecurityObjectBytes`/`DeviceNameSpacesBytes`; C2PA claim signature | RFC 9052 §4.4; RFC 8949 §3.4.5.1 (tag 24); ISO 18013-5 (secondary sources) |
| Byte-exact round-trip / "keep original bytes" mode | Re-encoding a parsed model can silently change bytes and invalidate a hash/signature | Cardano ledger transactions; any COSE/CWT verifier that re-serializes instead of checking raw bytes | Cardano CIP-21; general COSE practice |
| Bignum tags 2/3 (positive/negative bignum) and preferred-serialization fallback to native ints when they fit | Large integers (crypto values, Plutus Data) must round-trip exactly | Cardano Plutus Data; COSE key material | RFC 8949 §3.4.3; §4.2.2 |
| 64-bit length/argument handling correctly on 32-bit targets (no truncation/overflow when computing buffer sizes) | Untrusted length fields up to 2^64-1 must not overflow a 32-bit `size_t` and cause under-allocation + heap overflow | Large bstr in C2PA manifests; any embedded/32-bit target decoder | RFC 8949 §3 general structure; security guidance in RFC 8949 §7 ("Resource exhaustion... integer overflow vulnerabilities") |
| Decoder recursion/nesting depth limit, no unbounded stack recursion | Untrusted deeply-nested arrays/maps/tags cause stack-overflow DoS | Any public-facing decoder; explicitly numerically bounded (4 levels) in CTAP2 | RFC 8949 §7 (resource exhaustion); CTAP2.1 §8 (max 4 levels); real-world CVE-2026-26209 (Python `cbor2`, uncontrolled recursion in `loads`, GHSA-3c37-wwvx-h642); RUSTSEC-2019-0025 / CVE-2019-25001 (`serde_cbor` stack overflow via excessively nested tags) |
| Non-well-formed input handling per RFC 8949 Appendix F taxonomy (too much data / too little data / syntax error, 5 subkinds) | Defines exactly what a conforming decoder must reject and how; underpins fuzzing/test-vector suites | All decoders; esp. security-sensitive ones (COSE/CTAP2/mdoc parsers) | RFC 8949 Appendix F, F.1 |
| Half-precision (binary16) float decode/encode, including how ±Infinity and NaN are represented in 16-bit form | Required for full preferred-serialization/shortest-float support | RFC 8949 core determinism; CDE | RFC 8949 §3.3; §4.2.1 example ("1.5 is encoded as 0xf93e00") |
| NaN canonicalization to a single bit pattern when a protocol doesn't need NaN payloads (typically `0xf97e00`) | Otherwise NaN's signaling bit / payload bits create non-unique deterministic encodings | RFC 8949 CDE; dCBOR (mandatory reduction) | RFC 8949 §4.2.2; dCBOR §2.4 |
| Numeric reduction: collapse float values numerically equal to an integer (incl. all zero forms `0`, `0.0`, `-0.0`) into the integer form | Application-level determinism beyond CDE's encoding-only scope | dCBOR | draft-mcnally-deterministic-cbor §2.4 |
| String vs. byte-string type discipline (major type 2 vs 3), no silent coercion | Text/byte confusion is a validity and security issue (e.g., a text-string-typed field silently accepting binary) | General; CDDL schema validation catches this at the type level | RFC 8949 §3.1 (major types); RFC 8610 (typed schemas) |
| Tag validity checks (admissible type & admissible value for tag content) | Prevents e.g. tag 0 wrapping non-text, or bignum tag wrapping a non-bytestring | COSE/CWT tag 18 etc.; mdoc tag 24; general tag-aware decoders | RFC 8949 §5.3.2 |
| CBOR Sequence (RFC 8742) decode mode: read one item, don't error on "too much data," repeat | High-volume/streamed logs need append-without-reparse and incremental consumption | Telemetry/logging at volume | RFC 8742; RFC 8949 Appendix F ("too much data" carve-out) |
| Integer-key / SID-driven, schema-external decode (map keys are meaningless without an external schema table) | Wire bytes alone are not self-describing; correctness requires the matching schema/SID table | YANG-CBOR / CORECONF | RFC 9254 §3.2–3.4; draft-ietf-core-sid |
| Diagnostic notation (and EDN) encode/decode for tooling, test vectors, debugging | Human-auditable text form used across all the specs above for examples/vectors | Cross-cutting (CDDL test suites, spec examples) | RFC 8949 §8 / RFC 8610 App. G, both **now superseded by** draft-ietf-cbor-edn-literals |

---

## Determinism divergences: RFC 8949 §4.2 vs CTAP2 canonical vs CDE vs dCBOR

| Rule | RFC 8949 §4.2.1 "core deterministic encoding" | RFC 8949 §4.2.3 "length-first" (RFC 7049-compatible) alternative | CTAP2 "canonical CBOR encoding form" (CTAP2.1 §8) | CBOR CDE (draft-ietf-cbor-cde) | dCBOR (draft-mcnally-deterministic-cbor) |
|---|---|---|---|---|---|
| Integer/length/tag size | Shortest form, exact same size-class table | Same as core | Identical size-class rules, stated independently | Inherits RFC 8949 §4.2.1 verbatim ("preferred-serialization") | Inherits CDE (no fork) |
| Float shortening | MUST use shortest form that preserves value (e.g. 1.5 → 0xf93e00) | Same as core | **Explicitly prohibited** — "representations of any floating-point values are not changed"; a 16-, 32-, 64-bit encoding of the same numeric value are each independently canonical | Same as RFC 8949 for shortest-head; leaves NaN/subnormal specifics to the protocol, clarifies quiet-NaN leading bit = 1 | Goes further: reduces floats numerically equal to an integer *into that integer* (a stronger, cross-type rule, not just "shortest float") |
| Map key sort order | Pure bytewise-lexicographic order of the keys' deterministic encodings | (1) shorter key sorts first, (2) ties by bytewise lexical order — **no major-type tier** | (1) **lower major type sorts first**, (2) shorter key sorts first, (3) ties by bytewise lexical order — a 3-tier rule; CTAP2 notes tiers 1–2 collapse to RFC 8949's rule only for major types 0–3 and 7 | Calls this `lexicographic-map-sorting`: strictly increasing bytewise order of CDE-encoded keys — same as RFC 8949 §4.2.1 | Inherits CDE/RFC 8949 §4.2.1 ordering |
| Indefinite lengths | MUST NOT appear | MUST NOT appear | MUST be converted to definite-length | `definite-length-only` constraint, same rule | Inherits CDE |
| Tags | Permitted, but a protocol MUST fix whether a given position is always-tagged or never-tagged (no either/or) | Same as core | **MUST NOT be present at all** — categorically stricter than RFC 8949 | Encourages tag definitions to state their own CDE behavior; no blanket ban | No blanket ban stated beyond CDE inheritance |
| Duplicate map keys | Well-formed but invalid; protocol must define reject-vs-first-wins behavior | Same | Encoders MUST NOT produce them; decoders SHOULD reject | Not separately restated (inherits RFC 8949 validity model) | Encoders/decoders MUST reject (explicit, stronger than "SHOULD") |
| NaN handling | Protocol should pick one bit pattern if NaN payloads aren't needed (typically 0xf97e00) — advisory, not mandatory | Same | Not shortened at all (see float row) — a specific-width NaN is canonical for that width | Clarifies quiet-NaN leading significand bit = 1; no payload-specific rule beyond preferred serialization | MUST reduce all NaNs to the half-width quiet NaN `0xf97e00` |
| Negative integer range | No special restriction beyond size-class rules (full major type 1 range to -2^64) | Same | Same size-class rules apply, no extra restriction stated | Inherits RFC 8949 | Restricts to values ≥ -2^63 (excludes the -2^63−1 … -2^64 "65-bit negative" range representable in CBOR but not in most native signed 64-bit integer types) |
| Simple values allowed | All CBOR simple values permitted subject to preferred serialization | Same | All CTAP2-relevant simple values (false/true/null/undefined etc. as used by the protocol); no blanket restriction stated in the canonical-form rules themselves | Inherits RFC 8949 | Restricts to exactly `false`, `true`, `null`, and floats — narrower than raw CBOR's simple-value space |
| Relationship / status | Base normative definition (RFC, Internet Standard STD 94) | Alternative sort mode defined *within* RFC 8949 for RFC 7049 compatibility | Independent, FIDO-Alliance-owned profile; explicitly states it diverges from "Section 3.9 of [RFC 8949]" (i.e., from core deterministic encoding) | IETF Internet-Draft (BCP-track), "updates RFC 8949" with clarifications only, no technical changes to RFC 8949 itself | IETF Internet-Draft (Experimental), explicitly "does not fork CDE" — a strict application-level narrowing on top of CDE |

**The single most load-bearing divergence to get right in an implementation:**
CTAP2's map-key sort has an extra, higher-priority tier (major type) that RFC
8949's core deterministic encoding does not have. For CTAP2's actual keyspace
(integers, text strings, simple values — never arrays/maps/tags as keys),
CTAP2 itself notes the two schemes coincide numerically, so bugs from this
divergence are latent rather than immediately visible — they will surface
only if/when a spec extension puts a complex-typed key into a CTAP2 map, or
if a generic library is reused across both a CTAP2 context and an RFC
8949/CDE context without a mode switch. The float-shortening prohibition and
the blanket tag ban are unconditional divergences that bite immediately if a
generic "canonical CBOR" encoder is pointed at CTAP2 traffic without a
CTAP2-specific mode.

---

## Sources

- RFC 8949 (STD 94), "Concise Binary Object Representation (CBOR)" — full text fetched and grepped directly. https://www.rfc-editor.org/rfc/rfc8949.html / https://www.rfc-editor.org/rfc/rfc8949.txt — retrieved 2026-09-22
- RFC 9052, "CBOR Object Signing and Encryption (COSE): Structures and Process" — https://www.rfc-editor.org/rfc/rfc9052.html — retrieved 2026-09-22
- RFC 8392, "CBOR Web Token (CWT)" — https://www.rfc-editor.org/rfc/rfc8392.html — retrieved 2026-09-22
- RFC 9711, "The Entity Attestation Token (EAT)" — https://www.rfc-editor.org/rfc/rfc9711.html — retrieved 2026-09-22
- draft-ietf-spice-sd-cwt (rev -07), "Selective Disclosure CBOR Web Tokens (SD-CWT)" — https://datatracker.ietf.org/doc/html/draft-ietf-spice-sd-cwt-07 — retrieved 2026-09-22
- RFC 8428, "Sensor Measurement Lists (SenML)" — https://www.rfc-editor.org/rfc/rfc8428.html — retrieved 2026-09-22
- RFC 8613, "Object Security for Constrained RESTful Environments (OSCORE)" — https://www.rfc-editor.org/rfc/rfc8613.html — retrieved 2026-09-22
- RFC 7252, "The Constrained Application Protocol (CoAP)" — referenced, not independently re-fetched this pass
- RFC 9254, "Encoding of Data Modeled with YANG in CBOR" — https://www.rfc-editor.org/rfc/rfc9254.html — retrieved 2026-09-22
- draft-ietf-core-comi (rev -21), "CoAP Management Interface (CORECONF)" — https://datatracker.ietf.org/doc/draft-ietf-core-comi/ — retrieved 2026-09-22
- draft-ietf-core-sid, "YANG Schema Item iDentifier (YANG SID)" — https://datatracker.ietf.org/doc/draft-ietf-core-sid/ — retrieved 2026-09-22
- CTAP 2.1 (FIDO Alliance, fido-v2.1-ps-20210615), §8 Message Encoding — direct fetch + grep of primary HTML — https://fidoalliance.org/specs/fido-v2.1-ps-20210615/fido-client-to-authenticator-protocol-v2.1-ps-20210615.html — retrieved 2026-09-22
- C2PA Technical Specification (v2.4) — https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html — retrieved via search 2026-09-22 (not independently re-fetched full text this pass)
- Cardano `cardano-ledger` CDDL files (e.g. Conway era) — repository referenced, direct file fetch 404'd this pass; described via CIP-21 and implementer trackers instead
- CIP-21, "Transaction requirements for interoperability with hardware wallets" — https://cips.cardano.org/cip/CIP-21 — retrieved via search 2026-09-22
- RFC 8610, "Concise Data Definition Language (CDDL)" — https://www.rfc-editor.org/rfc/rfc8610.html — retrieved 2026-09-22
- draft-ietf-cbor-edn-literals, "CBOR Extended Diagnostic Notation (EDN)" — https://datatracker.ietf.org/doc/draft-ietf-cbor-edn-literals/ — retrieved 2026-09-22
- draft-ietf-cbor-cde (CBOR Common Deterministic Encoding), disentangled build — https://cbor-wg.github.io/draft-ietf-cbor-cde/disentangle/draft-ietf-cbor-cde.html — retrieved 2026-09-22
- draft-mcnally-deterministic-cbor-08 (dCBOR) — https://www.ietf.org/archive/id/draft-mcnally-deterministic-cbor-08.html — retrieved 2026-09-22
- RFC 8742, "CBOR Sequences" — https://www.rfc-editor.org/rfc/rfc8742.html — retrieved 2026-09-22
- N. Mavrogiannopoulos et al. blog analysis, "The several canons of CBOR" (Adam Langley, ImperialViolet) — https://www.imperialviolet.org/2022/04/17/canonsofcbor.html — retrieved 2026-09-22 (secondary source, cross-checked against primary CTAP2 text above)
- GHSA-3c37-wwvx-h642 / CVE-2026-26209, Python `cbor2` uncontrolled-recursion DoS advisory — https://github.com/agronholm/cbor2/security/advisories/GHSA-3c37-wwvx-h642 — retrieved 2026-09-22
- RUSTSEC-2019-0025 / CVE-2019-25001, `serde_cbor` stack overflow via nested tags — https://rustsec.org/advisories/RUSTSEC-2019-0025.html — retrieved 2026-09-22
- ISO/IEC 18013-5:2021 (mdoc) — paywalled primary; described via secondary implementer sources (go-mdoc, eudi-lib-ios-iso18013-data-model) found via search — retrieved 2026-09-22 — **not independently verified against the primary ISO text**

## Open questions

- ISO/IEC 18013-5 (mdoc) is paywalled; the tag-24 bstr-wrapping description
  here rests on secondary/implementer sources, not the primary ISO text.
  Confidence on the exact mdoc CBOR structure is medium, not high.
- JPEG Trust's own primary specification was not directly fetched — the C2PA
  parallel is noted but not independently confirmed; treat as low confidence.
- Cardano's ledger CDDL file could not be fetched directly (404 on the path
  tried); the byte-exact-round-tripping claim rests on CIP-21 and
  implementer/issue-tracker discussion rather than a direct primary-spec
  quote about the ledger's own (lack of) canonical-encoding enforcement.
- draft-ietf-cbor-cde and draft-ietf-cbor-edn-literals are both live
  Internet-Drafts as of 2026-09-22; exact section numbers may shift before
  RFC publication — verify against the latest revision before citing section
  numbers in a downstream deliverable.
- CTAP2's "tags MUST NOT be present" rule was confirmed by direct primary-text
  fetch, but its precise interaction with future CTAP2.2+ revisions (if any
  reintroduce tag support for some extension) was not checked beyond the
  2.1 (2021-06-15) text used here.
- Did not independently verify the COSE `Sig_structure` encoding-restriction
  text of RFC 9052 §9 beyond the summary obtained; worth a direct-text pass
  if the COSE section of the final deliverable needs verbatim quotation.
