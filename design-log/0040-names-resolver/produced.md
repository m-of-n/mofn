---
schema: "design-log/v1"
id: DL-0040
part: produced
date: "2026-11-13"
---

# DL-0040 — produced

No primitive. TV-35 is signed with `cryptography` through the existing
`generate.py`.

| file | change |
|---|---|
| `prototype/wallet/engine/names.py` | **new**. `Resolver(statements, definitions, at)` collects the usable bindings and rotation links, and `resolve(name)` runs `SPEC-0004` §5.3.2. It returns a `Resolution`: the keys, the bindings used, and each failure (`name-unresolved`, `name-foreign`, `name-cycle`, `work-bound`). `valid_at` moved here from `reduce.py` |
| `prototype/wallet/engine/reduce.py` | `Anchor.trusts` may be a name. Name anchors are resolved before coverage and replaced by one anchor per key, each with the same `about`. An unresolved name is reported before the coverage reasons, and `Coverage.names` holds each resolution (§10.3) |
| `prototype/wallet/engine/definition.py` | a base-kind-`name` value is valid when it is one label; `Definition.is_naming` |
| `prototype/wallet/tests/test_names.py` | **new**. R-1…R-10 and E-8…E-10 from `vectors.json`, plus: TV-13 is not a binding, a binding outside its window or without DV-4 is not used, and the result does not depend on statement order |
| `spec/vectors/ksa-core/generate.py`, `vectors.json`, `vectors.md`, `README.md` | TV-35, bob2's `key-publish`; R-8…R-10 at 2026-10-25, each resolution now with its own `at`. Every existing vector is byte-identical, checked by diffing `vectors.json` |
| `spec/SPEC-0002-ksa-core.md` 0.9.0 → **0.9.1** | Appendix A gains TV-35. PATCH: no rule changes |
| `spec/SPEC-0004-ksa-trust-evaluation.md` 0.6.0 → **0.6.1** | Appendix A gains R-8…R-10 and states each row's time. PATCH |
| `spec/ADR-0008-sdsi-names.md` 0.1.0 → **1.0.0** | **accepted** on the human's instruction (`review.md`). The acceptance test is marked met |
| `project/BACKLOG-0001.md` 0.13.3 | T-040s → done; T-040 → review, with what is not yet done |
| `prototype/wallet` 0.5.0 → **0.6.0** | changelog |

## What the resolver is

A function from a name to a set of keys. Take *Carol's builder*,
`[7, carol, ["builder"]]`. The resolver looks for Carol's attestations that
assign a naming-type attribute `builder`. TV-30 says Carol's builder is
*Alice's fred's sam*, so it resolves that name in turn: Alice's `fred` is Bob
(TV-28), and Bob's `sam` is Dave (TV-29). The answer is {Dave}. No anchor is
consulted on the way. Trust is applied afterwards: Carol's anchor (TV-31)
trusts *Carol's builder*, so it now trusts Dave, and Dave's attestation TV-19
is covered (E-8). Bob, whom the name passed through, gains nothing (E-10).

## Design notes the human did not see as options

- **Name anchors are expanded before coverage, not inside it.** One anchor per
  resolved key, with the original `about`. That keeps §5.3 and §6 as two
  procedures (`ARCH-0001` §4.3) and leaves `_cover` unchanged.
- **The reason for an unresolved name is its first failure,** except that
  `work-bound` wins, because §5.3.5 fails the whole resolution. The vectors
  pin one reason each, and each has only one failing branch.
- **A namespace is the key's successor plus every key that rotates into it.**
  That reads §5.3.2 step 2 and §7.2 ("`K`'s namespace continues as `K′`'s")
  together. The old key's bindings count only if issued before the rotate
  (§7.2, past only). R-9 tests that.
- **A link needs the successor's `key-publish` in the statement set,** not just
  in the key store. In the prototype every vector key is in the store, so
  testing the store would have made R-10 impossible to express. §7.2 says
  "in the key store by its own `key-publish`", and the statement is that
  evidence.
- **Of two rotations from one key, the earlier is followed.** §7.2 does not
  say. Nothing tests it.
- **Compromise marks are not read** (`SPEC-0001` §9.6). The engine has no such
  store yet.
- **A binding must pass every §5.2 check, not only its naming attribute's.** An
  attestation with a type the wallet does not hold binds nothing.

## Not done

- `mofn check` and the anchor store take kids only. A name anchor works
  through `reduce.evaluate`, not yet from the command line.
- A trust **hop** to a name (`SPEC-0002` §8.6 as a delegation step) waits for
  multi-hop delegation in the engine, T-065.
- The `names` verdict line (§10.4) does not yet show a resolved name.
- `PLAN-0004` §7.2 is a dated status at Nov 12, and it is left as it is. Its
  name-resolution row was true on that date.
