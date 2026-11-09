---
schema: "design-log/v1"
id: DL-0030
part: produced
date: "2026-11-07"
---

# DL-0030 — produced

No primitive. Signing and hashing for N-11 come from `cryptography`, through
the existing `generate.py`.

| file | change |
|---|---|
| `spec/SPEC-0002-ksa-core.md` 0.5.0 → **0.6.0** | §7.2: type 5 **reserved, never assigned**. Two new paragraphs: every target binds a digest; a locator is an attribute on a digest or description target, never the target itself. §11.3 drops `{locator: text}`. §12.2: code 5 reserved, and a new target type MUST bind a digest. New §13.10, on locators as subjects and on descriptions that are only a URI. Appendix A gains N-11. Appendix B's CDDL drops `[5, tstr]`. Status entry for 0.6.0 |
| `spec/vectors/ksa-core/generate.py`, `vectors.json`, `vectors.md`, `README.md` | **N-11**: TV-4's attestation with `this = [5, uri]`, well-formed and signed; reject at V7 `structure`. Every existing vector is byte-identical (checked by diff) |
| `spec/ARCH-0001-authorization-attestation.md` 0.2.0 → **0.2.1** | PATCH. §4.1 `ArtifactId` row, §4.2 `ArtifactStatement` row, R-M-07 and R-M-11 notes point to SPEC-0002 0.6.0. §5.5: the locator-only row removed, intro says one of the two reverse gaps is closed. Changelog line |
| `prototype/wallet` 0.2.0 → **0.2.1** | `schema.py` drops target 5 (`aggregate` targets too); `test_vectors.py` expects N-11 at V7; `test_review_yaml.py`'s awkward-text cases move from a locator target to a description target. 270 tests pass |
| `project/BACKLOG-0001.md` 0.12.14 | T-048 done |
| `project/DECISIONS-0001.md` 0.6.1 | item 6's note: the rule is met |

**Version reasoning.** `SPEC-0002`'s MAJOR is "any change to signed or hashed
bytes", and none change. But a statement that verified under 0.5.0 can now be
invalid. That is a break in result, permitted here only because the document is
`0.x`; the status entry says so.

**Locator mode, R-M-11.** It still exists at the ARCH level, as evidence. In
KSA the mode is an attribute whose type some definition defines (`ARCH-0002`
P1). No locator type is registered, and none is needed: a registered type would
be a global allocation, which `ADR-0001` rejected.
