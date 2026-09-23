---
dimension: open-source
researched: 2026-09-22
confidence: medium
---

# CBOR open-source implementation landscape (survey)

All facts below were retrieved via web search/fetch on **2026-09-22** unless
marked otherwise. Star counts, download counts, and "latest release" figures
are snapshots from that date and will drift. Where a search tool's summary
could not be corroborated against a primary source, it is flagged
"unverified."

## C / C++

| Project | Repo | License | Latest verified release | Stars (2026-09-22) | Notes |
|---|---|---|---|---|---|
| libcbor | [PJK/libcbor](https://github.com/PJK/libcbor) | MIT | Not confirmed exact version/date (releases page exists but version not captured); actively developed, ~1,468 commits | 404 | C99, RFC 8949 compliant, supports CBOR Sequences, no global state. Runs the CBOR WG's own test vectors in CI (see PR #446). No CVEs found in a targeted search of NVD/OpenCVE-style sources. |
| QCBOR | [laurencelundblade/QCBOR](https://github.com/laurencelundblade/QCBOR) | Permissive "Linux-license"-style (opened by Qualcomm/CAF in 2018) | v1.6.1 stable; v2.x alpha in a dev branch | 240 | Designed for small devices (<4KB object code in minimal config); companion project **t_cose** adds COSE (RFC 8152/9052) on top. v2 dev branch is adding dCBOR and full deterministic/canonical encoding; v1.x does not fully canonicalize (map sorting not done on encode per the fetched README). Extensive tag support (base64, regex, UUID, MIME). |
| TinyCBOR | [intel/tinycbor](https://github.com/intel/tinycbor) | MIT | v7.0 ("dropped the leading 0.") — released as v0.6 series before that; used inside Qt releases | not captured | **Security history:** CVE-2025-24302 and CVE-2025-20025 — uncontrolled recursion in CBOR parsing, fixed in 0.6.1+ (CVSS v4 5.4, medium; confirmed via [Snyk advisory](https://security.snyk.io/vuln/SNYK-UNMANAGED-INTELTINYCBOR-12427405) and multiple mirrors — [Intel advisory INTEL-SA-01326](https://www.intel.com/content/www/us/en/security-center/advisory/intel-sa-01326.html)). The repo's own `SECURITY.md` is a generic Intel PSIRT boilerplate and does not itself list the CVE — verify current advisory status before shipping. Repo has moved its default branch to `main` and switched fully to CMake; still receiving maintenance commits. |
| cn-cbor | [jimsch/cn-cbor](https://github.com/jimsch/cn-cbor) (recommended upstream; originally [cabo/cn-cbor](https://github.com/cabo/cn-cbor), 2013 proof-of-concept, and a parallel [obgm/cn-cbor](https://github.com/obgm/cn-cbor) fork also exists) | MIT | Not captured (191 commits) | 81 (jimsch fork) | Aimed at constrained nodes (<1 KiB code on ARM in early research use). Multiple diverging forks exist — pick jimsch's for active maintenance per community guidance found in search results. |
| NanoCBOR | [bergzand/NanoCBOR](https://github.com/bergzand/NanoCBOR) | CC0-1.0 | Not captured | 58 | Decoder compiles to ~600–800 bytes on Cortex-M0+. Packaged into [RIOT-OS](https://doc.riot-os.org/group__pkg__nanocbor.html) as `pkg/nanocbor`; RIOT's `pkg/libcose` (COSE for constrained nodes) depends on it, and the SUIT firmware-manifest stack in RIOT consumes libcose. 2 open issues / 7 open PRs at time of check — moderate maintenance bandwidth. |
| zcbor | [NordicSemiconductor/zcbor](https://github.com/NordicSemiconductor/zcbor) | Apache-2.0 | v0.9.1 (PyPI + GitHub release) | 155 | Distinctive feature: a Python code generator that turns a **CDDL** schema into C encode/decode code, plus a low-footprint runtime C library. Ships as a Zephyr module (`CONFIG_ZCBOR`). This is one of the few OSS tools that treats CDDL as a first-class build input rather than documentation. |
| COSE-C | [cose-wg/COSE-C](https://github.com/cose-wg/COSE-C) | not captured | last updated ~2024-04-02 per search snippet | not captured | C++ COSE implementation with a C interface; crypto backend is OpenSSL or mbedTLS. Maintained under the IETF COSE working group's GitHub org, not a single company. |
| libcose | [bergzand/libcose](https://github.com/bergzand/libcose) | not captured | not captured | not captured | COSE for constrained nodes, no dynamic allocation; built on NanoCBOR; used by SUIT manifest processing in RIOT-OS. |
| wolfCOSE | [aidangarske/wolfCOSE](https://github.com/aidangarske/wolfCOSE) | not captured | not captured | not captured | Newer (wolfSSL-adjacent) embedded COSE+CBOR stack advertising PQC and FIPS 140-3/MISRA-C targeting — found in search only, not independently verified beyond the repo description. Treat as early-stage/unverified maturity. |

## Rust

| Project | Repo / crates.io | License | Notes |
|---|---|---|---|
| serde_cbor | [crates.io/serde_cbor](https://crates.io/crates/serde_cbor) | MIT/Apache-2.0 | **Deprecated.** [RUSTSEC-2021-0127](https://rustsec.org/advisories/RUSTSEC-2021-0127.html): unmaintained, repo archived by its author; issued 2021-11-30 (reported 2021-08-15). No patched version exists — the advisory itself tells users to migrate. There is also an earlier vulnerability advisory, [RUSTSEC-2019-0025](https://rustsec.org/advisories/RUSTSEC-2019-0025.html) (stack overflow flaw in the deserializer), from before the deprecation. Do not start new projects on this crate. |
| ciborium | [crates.io/ciborium](https://crates.io/crates/ciborium) / [docs.rs](https://docs.rs/ciborium) | Apache-2.0 (via the Enarx project) | The RUSTSEC advisory's own recommended replacement (alongside minicbor). serde-integrated (`from_reader`/`into_writer` + a `Value` type). Per its docs: "deterministic, smallest-size encodings" on output, liberal accepting on input (interoperates with serde_cbor-produced data). Map type is `Vec<(Value,Value)>`, preserving wire order rather than forcing BTreeMap ordering. Split into `ciborium` and `ciborium-ll` (low-level, no_std/no_alloc-capable). Basis for Google's `coset` COSE crate. |
| minicbor | [twittner/minicbor](https://github.com/twittner/minicbor) / [crates.io](https://crates.io/crates/minicbor) | Blue Oak Model License 1.0.0 | The other RUSTSEC-recommended serde_cbor replacement; explicitly `no_std`-first, with a derive-macro crate (`minicbor_derive`) for typed Encode/Decode. No serde dependency (smaller footprint) — trades off ecosystem interop for size, unlike ciborium. |
| coset | [google/coset](https://github.com/google/coset) / [crates.io](https://crates.io/crates/coset) | not captured (Google OSS, "not an officially supported Google product" per its own README) | COSE (RFC 8152/9052) types built on top of ciborium's CBOR parsing. `no_std`-capable with `alloc`. Mirrored into AOSP (Android). Actively used per search signals; API still described as "under construction." |
| cddl | [anweiss/cddl](https://github.com/anweiss/cddl) / [crates.io](https://crates.io/crates/cddl) | not captured | CDDL (RFC 8610) parser plus JSON/CBOR/CSV validator. Community signal ("actively developed" badge, an issue opened by the maintainer as recently as August 2026) but the crate's own docs describe its origin as "a personal learning exercise," and there is a **RUSTSEC advisory, RUSTSEC-2025-0061** (a dependency of `cddl` — content/nature not verified in this pass; flagged for follow-up). Treat production-readiness as unproven; this is the weakest link in the whole CDDL tooling story across languages. |
| cddl-cat | [ericseppanen/cddl-cat](https://github.com/ericseppanen/cddl-cat) / [crates.io](https://crates.io/crates/cddl-cat) | not captured | Smaller, more narrowly scoped CDDL validator; supports CBOR (via ciborium) or JSON (via serde_json) as the data side. Less actively promoted than `anweiss/cddl`. |
| dCBOR (Rust) | [BlockchainCommons/bc-dcbor-rust](https://github.com/BlockchainCommons/bc-dcbor-rust) | not captured | Reference implementation of Blockchain Commons' dCBOR application profile (still an IETF Internet-Draft — `draft-mcnally-deterministic-cbor`, at -12 as of the search results, not an RFC). |
| ldclabs/cbor2 (Rust) | [github.com/ldclabs/cbor2](https://github.com/ldclabs/cbor2) / [crates.io](https://crates.io/crates/cbor2) | not captured | A newer, separate Rust crate (unrelated to Python's `cbor2`) advertising async I/O, canonical/deterministic encoding, COSE-style integer map keys, semantic tags, diagnostic notation and no_std support, explicitly wire-compatible with ciborium's deterministic output. Too new to assess adoption; flagged as one-to-watch rather than an established default. |
| cbor4ii | crates.io | not captured | Appears in dependency graphs (e.g. referenced from `cbor2`'s crates.io page) as another CBOR crate; not independently investigated beyond that mention — unverified maturity. |

## Go

| Project | Repo | License | Notes |
|---|---|---|---|
| fxamacker/cbor | [fxamacker/cbor](https://github.com/fxamacker/cbor) | MIT | Latest release **v2.9.2** (2026-05-03, per GitHub fetch). ~1.1k stars. Full RFC 8949 + RFC 8742 (CBOR Sequences) conformance; supports Core Deterministic Encoding and a "CTAP2 Canonical CBOR" preset specifically for WebAuthn/FIDO2 use; configurable tag registry; indefinite-length/streaming support; configurable decode limits against malicious input. **Security:** passed multiple confidential 2022 assessments plus a public NCC-Group-for-Microsoft assessment (no vulns found in the audited subset); 98% coverage, fuzzed with a private continuation of the archived [fxamacker/cbor-fuzz](https://github.com/fxamacker/cbor-fuzz) harness (billions of execs required per release per project docs — this is a maintainer claim, not independently reproduced here). Originally built because, in 2019, no existing Go CBOR library met the author's WebAuthn/FIDO2 needs. **Downstream users** the project's own README lists: Arm, EdgeX Foundry, Flow Foundation, IBM, Kubernetes, Let's Encrypt, the Linux Foundation, Microsoft, Red Hat, Tailscale — this is a self-reported list from the maintainer, not independently confirmed per-project here. Also the CBOR engine behind [fxamacker/webauthn](https://github.com/fxamacker/webauthn) and pulled in as a dependency by the community [go-webauthn/webauthn](https://github.com/go-webauthn/webauthn) fork. |
| veraison/go-cose | [veraison/go-cose](https://github.com/veraison/go-cose) | not captured | Go COSE (RFC 9052/9338) implementation; forked from `mozilla-services/go-cose`, with Mozilla and Veraison maintainers agreeing to retire the Mozilla original in favor of this one. Uses fxamacker/cbor underneath for deterministic encoding. Supports PS/ES/EdDSA signature algorithms. Used in remote-attestation tooling (Veraison is a CNCF-adjacent attestation-verification project). |

## Python

| Project | Repo / PyPI | License | Notes |
|---|---|---|---|
| cbor2 | [agronholm/cbor2](https://github.com/agronholm/cbor2) / [PyPI](https://pypi.org/project/cbor2/) | MIT | The de facto standard Python CBOR library. Latest version **6.1.4**, published 2026-08-01 (per PyPI fetch). 306 stars. Notably, the extension backend **is now implemented in Rust** (confirmed directly from the project's current GitHub README on 2026-09-22) rather than the historical C extension + pure-Python fallback — worth flagging to a team since it changes the build/toolchain story (a Rust toolchain, v1.93.0+, is needed to build from source). Extensive tag support (stdlib objects, shared/cyclic references, string references). Ships a CLI (`cbor2` command) that converts CBOR to a JSON-ish printable form. **Security history (both fixed):** <br>• **CVE-2026-26209** / [GHSA-3c37-wwvx-h642](https://github.com/agronholm/cbor2/security/advisories/GHSA-3c37-wwvx-h642): DoS via uncontrolled recursion decoding deeply nested CBOR (CVSS 7.5, High); payloads under 100KB could crash a worker; affected ≤5.8.0, fixed in 5.9.0. <br>• **CVE-2025-68131** / [GHSA-wcj4-jw5j-44wh](https://github.com/agronholm/cbor2/security/advisories/GHSA-wcj4-jw5j-44wh): information-disclosure — decoder's "shareable"/"sharedref" (tags 28/29) table wasn't cleared between decode calls on a reused `CBORDecoder`, letting one message leak values from an earlier message across a trust boundary; affected 3.0.0–5.7.x, fixed in 5.8.0; Low severity. |
| cbor-diag | Ruby gem, not Python — see below | | (Corrected from the task's suggested Python framing: `cbor-diag` is [cabo/cbor-diag](https://github.com/cabo/cbor-diag), a **Ruby** gem/CLI by Carsten Bormann, Apache-2.0, for converting CBOR ↔ Extended Diagnostic Notation. Its logic has been reimplemented independently in other languages — e.g., a Rust-based WASM port, [jfromaniello/cbor-diag-wasm](https://github.com/jfromaniello/cbor-diag-wasm) — but there is no canonical Python "cbor-diag" package verified in this pass.) |
| dag_cbor (Python) | [dag-cbor.readthedocs.io](https://dag-cbor.readthedocs.io/en/latest/getting-started.html) | not captured | IPLD's DAG-CBOR profile (CBOR subset used by IPFS/IPLD content-addressed data) — see IPLD section below. |
| python-fido2 (Yubico) | not directly researched | not captured | Referenced here because its `strict_cbor` option (default `True`) validates that authenticator responses use canonical CBOR — a concrete example of CBOR canonicality being load-bearing for security in a widely deployed library. |

## JavaScript / TypeScript

| Project | Repo / npm | License | Notes |
|---|---|---|---|
| cbor2 (npm) | [hildjj/cbor2](https://github.com/hildjj/cbor2) / [npm](https://www.npmjs.com/package/cbor2) | not captured | Supersedes `node-cbor`/npm `cbor` (also by hildjj). Web-first (Node 20+ and Deno), synchronous decode API, intentionally breaks API compatibility with the old `cbor` package to modernize. The [hildjj/node-cbor](https://github.com/hildjj/node-cbor) repo's own docs say new users and most existing users should move to `cbor2`; `node-cbor`/`cbor` npm package now gets only "catastrophic bug" fixes. |
| cbor-x | [kriszyp/cbor-x](https://github.com/kriszyp/cbor-x) / [npm](https://www.npmjs.com/package/cbor-x) | MIT | Performance-focused implementation; project claims 3–10x faster than other JS CBOR implementations. Implements RFC 8949, RFC 8746 (typed arrays), RFC 8742 (sequences), **Packed CBOR**, and a proposed "record extension" for compact repeated-structure encoding — one of the only JS libraries engaging with Packed CBOR at all. **Security history:** an optional native addon dependency, `cbor-extract` (≤2.2.0), had a heap buffer over-read in `extractStrings()` triggerable by a 5-byte payload, causing a SIGSEGV crash — reachable in practice through `fido2-lib`'s WebAuthn attestation parsing path ([GHSA-g3qj-j598-cxmq](https://github.com/advisories/GHSA-g3qj-j598-cxmq)). Fixed in `cbor-extract@2.2.1`/`cbor-x@1.6.3` (2026-03-08). The pure-JS fallback path (no native addon) was not affected. |
| borc | [dignifiedquire/borc](https://github.com/dignifiedquire/borc) (also forked as `@exodus/borc`) / [npm](https://www.npmjs.com/package/borc) | not captured | A fork of the older `node-cbor` that drops streaming/async in favor of a minimal, fast sync API. Per npm-trends-style data surfaced in search, v3.0.0 had ~114k weekly downloads and ~30 GitHub stars at last check — high usage relative to its low star count, typical of a dependency pulled in transitively rather than chosen directly. |
| @ipld/dag-cbor | [ipld/js-ipld-dag-cbor](https://github.com/ipld/js-ipld-dag-cbor) / [npm](https://www.npmjs.com/package/@ipld/dag-cbor) | not captured | JS implementation of the DAG-CBOR IPLD codec (see below); used across the IPFS/Helia stack (`@helia/dag-cbor`). |
| cborg | referenced only via a third-party comparison page (pkgpulse) | not captured | Appears in comparisons against cbor-x/dag-cbor; not independently verified here — flagged for follow-up if the JS section needs deeper coverage. |
| cbor-diag-wasm | [jfromaniello/cbor-diag-wasm](https://github.com/jfromaniello/cbor-diag-wasm) | not captured | WASM port (from a Rust implementation) of Carsten Bormann's CBOR diagnostic-notation tool, for Node/browser use. |

## IPLD / content-addressed data (cross-language, notable niche)

DAG-CBOR (the CBOR profile used throughout IPFS/IPLD/Filecoin-adjacent tooling) deserves its own line because it is a real-world, widely deployed **canonical CBOR profile**, distinct from RFC 8949's own (optional) deterministic-encoding section and from dCBOR:

- Spec: [ipld.io DAG-CBOR spec](https://ipld.io/specs/codecs/dag-cbor/spec/) — CBOR tag 42 repurposed for CIDs, no other tags permitted, string-only map keys, shortest-form integer/length encoding enforced on decode, "additional strictness requirements... to ensure canonical data encoding forms."
- Implementations found: JS (`@ipld/dag-cbor`, `@helia/dag-cbor`), Python (`dag_cbor`, self-described as "fully compliant... enforcing a unique (strict) encoded representation").

## Java / Kotlin

| Project | Coordinates | License | Notes |
|---|---|---|---|
| jackson-dataformat-cbor | `com.fasterxml.jackson.dataformat:jackson-dataformat-cbor` (Maven Central); newer artifacts under `tools.jackson.dataformat` | Apache-2.0 | The standard JVM route: CBOR support for the ubiquitous Jackson streaming/tree/data-binding APIs. Latest version seen in search: 2.22.0. Repo: `FasterXML/jackson-dataformats-binary`. Not itself CDDL- or COSE-aware; it is a low-level codec that other libraries build on. |
| kotlinx-serialization-cbor | `org.jetbrains.kotlinx:kotlinx-serialization-cbor` (part of [Kotlin/kotlinx.serialization](https://github.com/Kotlin/kotlinx.serialization)) | Apache-2.0 (kotlinx.serialization project license) | Multiplatform (JVM/Kotlin Native/JS) CBOR support integrated with Kotlin's `@Serializable` model. Defaults to indefinite-length array/map encoding (a deliberate divergence from "shortest form" canonical style); supports CBOR tags on properties. |
| webauthn4j / Yubico java-webauthn-server | mentioned only as downstream consumers | | Both are cited (per search results, not independently fetched) as maintained JVM WebAuthn libraries that rely on CBOR/COSE underneath; not investigated for which CBOR codec each embeds. |

## Swift

| Project | Repo | License | Notes |
|---|---|---|---|
| SwiftCBOR (original) | [valpackett/SwiftCBOR](https://github.com/valpackett/SwiftCBOR) | not captured | The original, most-forked Swift CBOR implementation (RFC 7049-era). Encodes directly from Swift types or via a wrapper `CBOR` enum. |
| SwiftCBOR (EU DCC fork) | [eu-digital-green-certificates/SwiftCBOR](https://github.com/eu-digital-green-certificates/SwiftCBOR) | not captured | Notable real-world downstream use: forked and hardened for the EU Digital COVID Certificate ("green pass") ecosystem, which relies on COSE-signed CBOR (CWT) payloads. |
| swift-cbor | [nnabeyang/swift-cbor](https://github.com/nnabeyang/swift-cbor) | MIT | Newer, `Codable`-based encoder/decoder (rather than the older manual `CBOR` enum style), SPM-distributed. |
| edgeengineer/cbor | [edgeengineer/cbor](https://github.com/edgeengineer/cbor) | not captured | Newer, cross-platform-Swift-focused, Codable-integrated library. Too new to assess adoption; flagged as unverified maturity. |

The Swift ecosystem is fragmented across at least 4 actively-forked implementations with no single de facto standard (unlike Go's fxamacker/cbor or Python's cbor2) — this is itself a finding, not just a listing artifact.

## C# / .NET

| Project | Package | License | Notes |
|---|---|---|---|
| System.Formats.Cbor | [NuGet](https://www.nuget.org/packages/System.Formats.Cbor/) / [source in dotnet/runtime](https://github.com/dotnet/runtime/blob/main/src/libraries/System.Formats.Cbor/src/System.Formats.Cbor.csproj) | MIT (.NET runtime license) | Part of the official .NET BCL since .NET 5; ships as its own NuGet package for netstandard2.0/.NET Framework 4.6.2 consumers too. Low-level, stateful `CborReader`/`CborWriter` API (comparable to a SAX-style pull parser) rather than an object-mapping layer — teams need their own serialization layer on top. Supports configurable "conformance modes" (a built-in notion of strict/canonical vs. lax parsing). Documented breaking change in .NET 8 around `DateTimeOffset` formatting — worth flagging for any team pinning to older behavior. |

## Erlang / Elixir

| Project | Package | License | Notes |
|---|---|---|---|
| cbor (Elixir) | [hex.pm/packages/cbor](https://hex.pm/packages/cbor) | not captured | Elixir implementation of RFC 8949 (renamed module `Cbor` → `CBOR`). `CBOR.decode` returns `{:ok, decoded, rest}`. Handles the impedance mismatch of infinity/NaN (no native Elixir concept) via a `CBOR.Tag` struct. |
| erl_cbor | [hex.pm/packages/erl_cbor](https://hex.pm/packages/erl_cbor) | not captured | Erlang-native implementation of RFC 7049-era CBOR. |
| ecbor | [hex.pm/packages/ecbor](https://hex.pm/packages/ecbor) | not captured | A second, apparently independent Erlang CBOR package; not compared against erl_cbor for maturity in this pass. |

Coverage here is the thinnest of any language surveyed — three small, apparently independently-maintained packages, no dominant implementation, and none of them showed up in downstream-adoption searches the way fxamacker/cbor or cbor2 did.

## COSE implementations (cross-cutting)

COSE (RFC 8152 / RFC 9052 "CBOR Object Signing and Encryption") is the security layer most teams actually need alongside raw CBOR, so it's worth listing separately from the encoders:

| Project | Language | Notes |
|---|---|---|
| t_cose | C | Laurence Lundblade's companion to QCBOR for COSE_Sign1/COSE_Mac0. |
| COSE-C | C/C++ | IETF COSE-WG maintained; OpenSSL or mbedTLS backend. |
| libcose | C | Constrained-device COSE, built on NanoCBOR, used by RIOT-OS's SUIT stack. |
| wolfCOSE | C | wolfSSL-adjacent, embedded/PQC/FIPS-140-3 oriented — unverified maturity, found only via search. |
| coset | Rust | Google, built on ciborium; mirrored into AOSP. |
| veraison/go-cose | Go | RFC 9052/9338; supersedes the retired mozilla-services/go-cose; built on fxamacker/cbor. |
| python-fido2 (Yubico) | Python | Embeds COSE key handling for CTAP2/WebAuthn; enforces canonical CBOR by default. |

## Test vectors and conformance suites

- **RFC 8949 Appendix A** is the baseline: a hex/value worked-example table baked directly into the standard (see [datatracker.ietf.org/doc/html/rfc8949](https://datatracker.ietf.org/doc/html/rfc8949)). Multiple implementations (e.g., libcbor per its PR #446, and third-party projects like `jkammerland/cbor_tags`) explicitly wire these ~81 literal examples into their own test suites, effectively making Appendix A the de facto shared conformance baseline across the ecosystem — but it's small, hand-authored, and does not exercise adversarial/malformed input.
- **[Darkyenus/cbor-test-vectors](https://github.com/Darkyenus/cbor-test-vectors)** — a small, independent repo that re-publishes the RFC 8949 Appendix A examples as a machine-processable JSON array, explicitly to make them easier to consume from arbitrary test harnesses. Useful, but it is essentially a repackaging of Appendix A, not an independent adversarial corpus.
- **cbor.io** ([cbor.io/spec.html](https://cbor.io/spec.html), [cbor.io/tools.html](https://cbor.io/tools.html), [cbor.io/impls.html](https://cbor.io/impls.html)) — Carsten Bormann's community hub page listing implementations and tools across languages; a reasonable starting index but not itself a test-vector generator.
- **Fuzzing** is where real adversarial coverage actually lives, and it is per-project rather than shared: fxamacker/cbor has a dedicated (partly private) coverage-guided fuzz harness with a stated 95%+ coverage gate per release; cbor2 (Python) ships fuzz-derived regression tests for its two recent CVEs; TinyCBOR's uncontrolled-recursion CVEs suggest its historical fuzzing coverage had gaps around deep nesting specifically. There is **no shared, cross-language CBOR fuzz corpus or OSS-Fuzz integration** that this research surfaced — each implementation fuzzes (or doesn't) on its own.

## Gaps: what open source does not serve well

1. **CDDL tooling is thin and fragmented.** Only two general-purpose CDDL validators surfaced with any real activity — `anweiss/cddl` (Rust) and the narrower `ericseppanen/cddl-cat` — and the more prominent one (`anweiss/cddl`) explicitly documents its own origin as a personal learning project and carries a RUSTSEC advisory on a dependency (RUSTSEC-2025-0061, contents not verified here). zcbor's CDDL→C code generator is the most production-oriented use of CDDL found, but it's scoped to embedded C, not general validation. There is no CDDL tool with the maturity signal (adoption, security assessment, multi-year stability) that fxamacker/cbor or cbor2 have for plain CBOR.
2. **Packed CBOR has essentially one real implementation.** `cbor-x` (JS) is the only library in this survey that implements the IETF `draft-ietf-cbor-packed` mechanism (at draft -19 as of the search results — still not an RFC). No C, Rust, Go, or Python implementation of Packed CBOR was found.
3. **dCBOR is single-vendor.** Blockchain Commons maintains the spec (still an Internet-Draft, `draft-mcnally-deterministic-cbor`) and reference implementations in Rust and TypeScript (`bc-dcbor-rust`, `bc-dcbor-ts`) and Swift; QCBOR's v2 dev branch is adding dCBOR support but that's still unreleased/alpha. No independent third-party dCBOR implementation (i.e., not from Blockchain Commons or a library explicitly integrating their spec) was found.
4. **No shared adversarial test-vector / fuzz corpus.** As noted above, conformance testing largely stops at RFC 8949 Appendix A (a small, well-formed-input-only set); security-relevant edge cases (deep nesting, indefinite-length abuse, huge length prefixes, duplicate map keys, non-canonical encodings) are covered inconsistently and per-project, which is exactly the class of bug that produced the TinyCBOR and cbor2 CVEs found in this survey.
5. **Swift and Erlang/Elixir have no dominant, clearly-most-maintained implementation** the way Go and Python do — Swift has 4+ active forks, Erlang/Elixir has 3 small independent packages. A team building on either platform has real evaluation work to do that other languages have already settled.
6. **Canonical/deterministic encoding is inconsistently implemented and inconsistently named.** RFC 8949 §4.2's "Core Deterministic Encoding," CTAP2's own canonical form, DAG-CBOR's canonical strictness rules, and dCBOR's profile are four related-but-distinct specs, and libraries pick different subsets to support (QCBOR v1 does not sort map keys on encode; ciborium and fxamacker/cbor both claim RFC 8949 §4.2 conformance; DAG-CBOR and dCBOR each add their own extra constraints). A team that needs cross-implementation determinism guarantees (e.g., for content addressing or signing) needs to pick one profile explicitly rather than assuming "canonical CBOR" is a single interoperable thing.

## What I could not verify

- Exact GitHub star counts, last-commit dates, and license identifiers for: TinyCBOR, cn-cbor (jimsch fork's exact commit/release date), NanoCBOR's latest tagged release, zcbor's exact star/fork count as of today (only a slightly stale search-summarized figure was obtained), COSE-C, libcose, wolfCOSE, borc's current (vs. a cached npm-trends) download figures, cddl (anweiss)'s license and exact star count, coset's license, veraison/go-cose's star count, kotlinx-serialization-cbor's release cadence, SwiftCBOR variants' license terms, System.Formats.Cbor's current NuGet download count, and all three Erlang/Elixir packages' license and star counts. In each case I attempted at least one targeted search or fetch; where the search tool's own summary was the only source and I could not cross-check it against the primary page directly, I marked the cell "not captured" rather than reporting the search summary as fact.
- **RUSTSEC-2025-0061** (surfaced as affecting a dependency of `cddl`): I did not fetch the advisory text directly and could not confirm its severity, CVE mapping, or whether it's actually exploitable in typical `cddl` usage. Flagged, not asserted.
- The precise version of Python `cbor2` at which the backend moved from a C extension to a Rust extension. I confirmed the *current* (6.1.4, 2026-09-22) state is Rust-based via the live GitHub README, but did not trace the changelog to find the exact transition release.
- Whether `cborg` (JS) is a real, separately-maintained project or primarily a comparison artifact from a single third-party blog post (pkgpulse) — only one weak source surfaced.
- The `github.com/cyberphone/CBOR.js` project surfaced once in search results but was not investigated at all — unverified even at the level of "what is it."
- Whether Kubernetes, Let's Encrypt, Tailscale, IBM, Red Hat, Arm, and Flow Foundation *actually* use fxamacker/cbor in shipped, current code — this list is copied from the fxamacker/cbor README's own self-reported "used by" claims and was not independently confirmed against each downstream project's own dependency manifests.
- Any CVE history for libcbor (C), QCBOR, cn-cbor, NanoCBOR, zcbor, ciborium, minicbor, coset, veraison/go-cose, jackson-dataformat-cbor, kotlinx-serialization-cbor, any Swift CBOR library, System.Formats.Cbor, or any Erlang/Elixir CBOR package — targeted searches for "CVE libcbor" and similar came back empty (a reasonable news-you-can-use fact — "no CVE found in this search" — but I cannot rule out CVEs my search terms simply missed).

## Sources

- https://github.com/PJK/libcbor (2026-09-22)
- https://github.com/PJK/libcbor/pull/446 (2026-09-22)
- https://github.com/laurencelundblade/QCBOR (2026-09-22)
- https://github.com/intel/tinycbor (2026-09-22)
- https://github.com/intel/tinycbor/releases (2026-09-22)
- https://github.com/intel/tinycbor/blob/main/SECURITY.md (2026-09-22)
- https://security.snyk.io/vuln/SNYK-UNMANAGED-INTELTINYCBOR-12427405 (2026-09-22)
- https://www.intel.com/content/www/us/en/security-center/advisory/intel-sa-01326.html (2026-09-22, not directly fetched — via search snippet)
- https://github.com/jimsch/cn-cbor (2026-09-22)
- https://github.com/cabo/cn-cbor (2026-09-22, via search)
- https://github.com/obgm/cn-cbor (2026-09-22, via search)
- https://github.com/bergzand/NanoCBOR (2026-09-22)
- https://doc.riot-os.org/group__pkg__nanocbor.html (2026-09-22, via search)
- https://github.com/RIOT-OS/RIOT/tree/master/pkg/libcose (2026-09-22, via search)
- https://github.com/bergzand/libcose (2026-09-22, via search)
- https://github.com/NordicSemiconductor/zcbor (2026-09-22)
- https://github.com/NordicSemiconductor/zcbor/releases (2026-09-22)
- https://crates.io/crates/serde_cbor (2026-09-22, via search)
- https://rustsec.org/advisories/RUSTSEC-2021-0127.html (2026-09-22)
- https://rustsec.org/advisories/RUSTSEC-2019-0025.html (2026-09-22, via search)
- https://crates.io/crates/ciborium (2026-09-22, via search — direct fetch failed)
- https://docs.rs/ciborium (2026-09-22, via search)
- https://github.com/twittner/minicbor (2026-09-22, via search)
- https://crates.io/crates/minicbor (2026-09-22, via search — direct fetch failed)
- https://github.com/google/coset (2026-09-22, via search)
- https://crates.io/crates/coset (2026-09-22, via search)
- https://github.com/anweiss/cddl (2026-09-22, via search)
- https://crates.io/crates/cddl (2026-09-22, via search)
- https://osv.dev/vulnerability/RUSTSEC-2025-0061 (2026-09-22, surfaced only, not fetched)
- https://github.com/ericseppanen/cddl-cat (2026-09-22, via search)
- https://github.com/BlockchainCommons/bc-dcbor-rust (2026-09-22, via search)
- https://github.com/BlockchainCommons/bc-dcbor-ts (2026-09-22, via search)
- https://developer.blockchaincommons.com/dcbor/ (2026-09-22, via search)
- https://www.ietf.org/archive/id/draft-mcnally-deterministic-cbor-08.html (2026-09-22, via search)
- https://github.com/ldclabs/cbor2 (2026-09-22, via search)
- https://github.com/fxamacker/cbor (2026-09-22)
- https://github.com/fxamacker/webauthn (2026-09-22, via search)
- https://github.com/go-webauthn/webauthn/pull/790 (2026-09-22, via search)
- https://github.com/fxamacker/cbor-fuzz (2026-09-22, via search)
- https://github.com/veraison/go-cose (2026-09-22, via search)
- https://github.com/agronholm/cbor2 (2026-09-22)
- https://pypi.org/project/cbor2/ (2026-09-22)
- https://github.com/agronholm/cbor2/security/advisories/GHSA-3c37-wwvx-h642 (2026-09-22)
- https://github.com/agronholm/cbor2/security/advisories/GHSA-wcj4-jw5j-44wh (2026-09-22)
- https://github.com/cabo/cbor-diag (2026-09-22, via search)
- https://github.com/jfromaniello/cbor-diag-wasm (2026-09-22, via search)
- https://dag-cbor.readthedocs.io/en/latest/getting-started.html (2026-09-22, via search)
- https://developers.yubico.com/python-fido2/ (2026-09-22, via search)
- https://github.com/hildjj/cbor2 (2026-09-22, via search)
- https://github.com/hildjj/node-cbor (2026-09-22, via search)
- https://www.npmjs.com/package/cbor2 (2026-09-22, via search)
- https://github.com/kriszyp/cbor-x (2026-09-22, via search)
- https://www.npmjs.com/package/cbor-x (2026-09-22, fetch blocked with HTTP 403; data via search only)
- https://github.com/advisories/GHSA-g3qj-j598-cxmq (2026-09-22, via search)
- https://github.com/dignifiedquire/borc (2026-09-22, via search)
- https://www.npmjs.com/package/borc (2026-09-22, via search)
- https://github.com/ipld/js-ipld-dag-cbor (2026-09-22, via search)
- https://ipld.io/specs/codecs/dag-cbor/spec/ (2026-09-22, via search)
- https://www.npmjs.com/package/@ipld/dag-cbor (2026-09-22, via search)
- https://mvnrepository.com/artifact/com.fasterxml.jackson.dataformat/jackson-dataformat-cbor (2026-09-22, via search)
- https://kotlinlang.org/api/kotlinx.serialization/kotlinx-serialization-cbor/ (2026-09-22, via search)
- https://github.com/Kotlin/kotlinx.serialization (2026-09-22, via search)
- https://github.com/valpackett/SwiftCBOR (2026-09-22, via search)
- https://github.com/eu-digital-green-certificates/SwiftCBOR (2026-09-22, via search)
- https://github.com/nnabeyang/swift-cbor (2026-09-22, via search)
- https://github.com/edgeengineer/cbor (2026-09-22, via search)
- https://www.nuget.org/packages/System.Formats.Cbor/ (2026-09-22, via search)
- https://github.com/dotnet/runtime/blob/main/src/libraries/System.Formats.Cbor/src/System.Formats.Cbor.csproj (2026-09-22, via search)
- https://learn.microsoft.com/en-us/dotnet/core/compatibility/extensions/8.0/cbor-datetime (2026-09-22, via search)
- https://hex.pm/packages/cbor (2026-09-22, via search)
- https://hex.pm/packages/erl_cbor (2026-09-22, via search)
- https://hex.pm/packages/ecbor (2026-09-22, via search)
- https://github.com/cose-wg/COSE-C (2026-09-22, via search)
- https://github.com/aidangarske/wolfCOSE (2026-09-22, via search)
- https://datatracker.ietf.org/doc/html/rfc8949 (2026-09-22, via search)
- https://cbor.io/spec.html (2026-09-22, via search)
- https://cbor.io/tools.html (2026-09-22, via search)
- https://cbor.io/impls.html (2026-09-22, via search)
- https://github.com/Darkyenus/cbor-test-vectors (2026-09-22, via search)
- https://datatracker.ietf.org/doc/draft-ietf-cbor-packed/ (2026-09-22, via search)
- https://github.com/w3c/webauthn/issues/1624 (2026-09-22, via search)
