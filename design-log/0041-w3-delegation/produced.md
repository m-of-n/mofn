---
schema: "design-log/v1"
id: DL-0041
part: produced
date: "2026-11-14"
---

# DL-0041 — produced

No primitive. Test statements are signed with the existing `signer.py`
(PyNaCl) and the vector seeds.

| file | change |
|---|---|
| `prototype/wallet/engine/reduce.py` | `_walk` (§6.2 start, breadth-first, sorted by digest), `_follow` (§6.3 items 1–6 and the state table), `_range_ok`, `_same`, `_onward_ok`. New `Hop`, `Reach`, `Broken`; `Covered.path`, `Stopped.link`/`path`; `Anchor.may_delegate`, `Anchor.not_on_or_after`; `anchor_from(v, …)`. `_cover` uses the reached states instead of anchors, then a broken link to the speaker, then `no-path`. §6.5: 16 edges per path, 4096 edges per evaluation → `work-bound`, never a partial yes |
| `prototype/wallet/engine/definition.py` | `range_within` — the enum subset rule, for `delegation: 2` |
| `prototype/wallet/engine/statement.py` | `trust(...)` builder |
| `prototype/wallet/engine/check.py` | trust statements reach the engine; the authorization line shows the chain on a pass and names the broken link on a fail; JSON `path` lists each hop |
| `prototype/wallet/engine/store.py`, `cli.py` | `root add --depth N` (stored as `may delegate: {depth}`); `mofn delegate KEY --as YOU …` signs a trust statement with `--valid-days` |
| `prototype/wallet/tests/test_delegation.py` | the walker is removed; E-1…E-7 run on `reduce.evaluate`, with the same expectations |
| `prototype/wallet/tests/test_paths.py` | **new**, 20 cases: two hops, scope narrowing, out-of-topic, `delegation: 0`, expired / not-yet-valid hop, `may-delegate.not-on-or-after`, expired anchor statement, depth, allow/exclude keys and their accumulation, cycle, order independence, and `delegation: 1` vs `2` |
| `demo/slice.sh`, `fixtures/golden/chain-*.txt` | ④ chain green, ⑤ the same 31 days on, ⑥ a widened link; 8 cases × 2 codecs |
| `spec/vectors/ksa-core/README.md` | says the engine, not a walker, checks E-1…E-4 |
| `project/BACKLOG-0001.md` 0.13.3 → **0.14.0** | W-3, T-065, T-041, T-047 → review; T-042 subsumed; W-2b unblocked |
| `prototype/wallet` 0.6.0 → **0.7.0** | changelog |

## T-042: the evidence

`_same(a, b)` is `encode(a) == encode(b)`, and it is the only comparison a
`delegation: 1` hop gets. `test_delegation_same_is_bytes_equal`: the same
range is followed; a narrower range, the same set in another order, and the
unbounded range are each refused with `widening`, naming the hop. That is
`R-0006` §4.7's reading exactly: the floor (*equal bytes, else empty*) exists
inside the accepted core per type, and fails closed. `delegation: 2` narrows
(`test_delegation_scoped_narrows_where_same_cannot`), which `bytes-equal`
cannot.

**What this does not do.** It selects none of DEC-004's three options and
says nothing about a tag language. It shows that I3's reducer can be built
and tested without one, over `SPEC-0003` attribute ranges. DEC-004 remains
open in `ARCH-0001`; nothing here edits it.

## Design notes the human did not see as options

- **Where a `no` points.** If the speaker was reached but not for this value,
  the reason is `no-path` at the attestation (E-6). Otherwise, if some hop
  toward the speaker failed, it is that hop's code at that hop (E-1, E-3,
  E-4). Otherwise `no-path`, no anchor. Only the first broken link is
  reported; §10.3 asks for *every* reason, and the others are in `Broken`
  but not yet surfaced.
- **`delegation: 1` against `may-delegate.ranges`.** §6.3 item 4 says the
  range "MUST equal that range". The engine requires equality with a range in
  `scope` **and**, if present, in `deleg.ranges`. The other reading (equal to
  scope, merely within `deleg.ranges`) is not tested by any vector.
- **Codes.** `delegation: 0` → `type-error` (SPEC-0003 §5.4 calls it one);
  a `delegation: 1` mismatch and an out-of-topic hop → `widening` (§6.3
  item 4). An expired hop, or an expired `may-delegate.not-on-or-after`,
  → `not-valid-at-time`, at follow time: `cap` only falls, so pruning there
  gives the same answer as checking `cap` at coverage.
- **The broken-link sentence has no date** ("the delegation has expired"),
  so the demo's golden is stable when checked with `--at` 31 days on.
- **A hop to a name** is resolved with `names.py` (§6.3 item 1). An
  unresolved name on a hop is not reported as a broken link. Untested.
- **Not done:** revocation of a hop (§7.1; the answer still says 0
  revocations considered), rotation on a path (§7.2), threshold hops (§6.4,
  T-043), and `mofn delegate` to a name.
