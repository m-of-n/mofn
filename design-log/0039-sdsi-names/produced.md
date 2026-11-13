---
schema: "design-log/v1"
id: DL-0039
part: produced
date: "2026-11-12"
---

# DL-0039 — produced

No primitive. The signing and hashing for TV-27…34, N-12 and N-13 come from
`cryptography`, through the existing `generate.py`.

| file | change |
|---|---|
| `spec/SPEC-0002-ksa-core.md` 0.8.0 → **0.9.0** | §7.2 registers type 7, the **name** `[7, kid, [+ label]]`: 1–16 labels, each `[a-z][a-z0-9-]{0,62}`, and the issuer kid is the digest it binds. §8.1: `trust` may be about a name, `aggregate` may not. §8.6: a trust to a name trusts each key it resolves to. §11.3 gives the human form. §12.2 notes code 7. New §13.11, on names as subjects. The Appendix B CDDL. Appendix A gains DV-4, TV-27…34, N-12 and N-13. The banner read 0.6.0 and is corrected |
| `spec/SPEC-0003-ksa-definitions.md` 0.1.3 → **0.2.0** | §6 registers base kind 12, `name`. New §6.4: a naming type is recognised by its base kind, not its definer, and DV-2's text `name` is not one |
| `spec/SPEC-0004-ksa-trust-evaluation.md` 0.5.0 → **0.6.0** | New **§5.3 Name resolution**: bindings (§5.3.1), the procedure (§5.3.2), groups (§5.3.3), failures `name-unresolved` / `name-foreign` / `name-cycle` (§5.3.4), bounds (§5.3.5), where names are used (§5.3.6). Changes in §2 terms, §3, §4.2 (`trusts` may be a name), §6.2, §6.3 item 1, §6.4, §7.2, §10.1 (an ask's subject is never a name), §10.3, §10.4 (`names` line), §11.7–§11.8 and §14.2. Appendix A gains R-1…R-7 and asks 7–9. The banner read 0.3.0 and is corrected |
| `spec/ADR-0008-sdsi-names.md` | **new, `status: proposed`**. It records the six choices and the rejected options. An ADR is needed because SPEC-0002 §12 and SPEC-0003 §12 require one for a registry entry. The agent did not mark it accepted |
| `spec/vectors/ksa-core/generate.py`, `vectors.json`, `vectors.md`, `README.md` | DV-4 `naming`; TV-27…34; N-12 (empty labels) and N-13 (`Fred`); `resolutions` R-1…R-7 and `name_evaluations` E-8…E-10, both **declared**. Every existing positive vector, negative vector, definition and evaluation is byte-identical, checked by diffing `vectors.json` before and after |
| `spec/ARCH-0001-authorization-attestation.md` 0.3.0 → **0.3.1** | PATCH. The §4.1 `Principal` and `Name` rows, the §4.2 `NameCert` row and §4.3 item 1 now point to the SPECs. The §5.5 SDSI row is removed, and the intro says both reverse gaps are closed. Changelog line |
| `prototype/wallet` 0.4.1 → **0.5.0** | `schema.py`: target 7 is checked and gets a human form, and `trust` accepts it. `definition.py`: base kind 12. `test_vectors.py`: N-12 and N-13 fail at V7. 366 tests pass. **No resolver**; that is T-040 |
| `project/BACKLOG-0001.md` 0.13.2 | T-040s → review; T-040 unblocked, with its acceptance vectors named |
| `design-log/README.md` | row for 0039; the next free id is now 0040 (it said 0038, which was already taken) |

## Design notes the human did not see as options

- **Resolution is a set-valued rewrite, not a graph search.** `resolve(I,
  labels)` recurses on the first label and unions over the bindings. It
  terminates because a call that is already in progress is a cycle, and
  because nesting is capped at 16. The cap matches §6.5's edge bound.
  Exceeding it fails the whole resolution (`work-bound`), never giving a
  partial set, for the reason §6.5 gives.
- **A failed branch does not fail a non-empty result.** If `fred` has two
  bindings and one dead-ends, the name resolves to the other, and the dead end
  is reported. The alternative, failing on any dead branch, would let an issuer
  break a name by adding a binding. That is the same reason the human gave for
  rejecting `name-ambiguous`.
- **The name does not use depth, and `allow` / `exclude` apply to the resolved
  key.** Without the second rule, an `exclude-keys` could be bypassed by
  trusting a name that resolves to the excluded key.
- **Ask subjects are never names.** An ask about *Alice's fred* (for example,
  "is Alice's fred a person?") is a reasonable question. It needs a coverage
  rule about attestations whose target is a name, and nothing asked for one.
  It is left undefined, and an attestation about a name with no naming-type
  attribute has no effect. Nothing else in this change relies on that.
- **Name evaluations are kept out of `evaluations`.** `test_delegation.py`
  iterates `evaluations`, and the engine has no resolver, so putting E-8…E-10
  there would turn CI red for work that T-040 owes.

## Not done

- No resolver in `prototype/wallet/engine/` (T-040).
- No rotation vector for names. TV-8 rotates Bob → bob2, but bob2 has no
  `key-publish` in the vectors, so §7.2 never links them.
- `PLAN-0004` §7 still says name resolution is "not met". That remains true
  for the engine, and the row is not edited here.
