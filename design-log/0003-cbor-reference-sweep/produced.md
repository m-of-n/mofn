---
schema: "design-log/v1"
id: DL-0003
part: produced
date: "2026-09-22"
---

# DL-0003 — produced

## In `library/` (submodule)

- **51 records.** 39 new RFC records + 6 IETF drafts + 2 consortium records
  (CBOR WG, COSE WG) + 2 IANA registry `dataset` records; plus `rfc-8949` and
  `rfc-9052`, which existed only as unfilled templates and were authored.
- Every record carries a **sha-256 of the retrieved bytes** (RFC/draft `.txt`,
  registry page) and a `retrieved` date. No third-party document committed.
- Every record carries a **`usefulness` verdict with a reason**, including 14
  `marginal` and 4 `not-useful` — the scope §6 requirement that a negative
  judgement be recorded rather than the document silently dropped.
- **2 new topics**: `cbor-implementation` (37 records), `cbor-ecosystem` (11).
  Determinism records were filed under the existing `canonical-encoding`.
- `rfc-8949` taken to `status: read` with a full six-section `summary.md` and a
  12-entry `implementations` block (scope §3: an implementation of a spec we
  hold is an `implementations` entry, not a record).

## In `mofn/research/0001-cbor/`

`report.md` (RPT-0001), `sources.md`, `searches.md`, and `dimensions/` — the
six raw agent surveys, archived as evidence with a README marking them
unverified.

## Tooling change

`library/bin/reindex` — two bug fixes, both latent until a record used `cites`:

1. `listify()` raised `AttributeError` on a `{title, locator}` entry — the
   exact "cites gap" form `docs/references.md` §1 defines as the frontier
   queue. The documented snowballing mechanism crashed the first time it was
   used.
2. The `cites` loop appended both a bare string and an `(rid, target)` tuple
   for the same gap, which would have raised in the frontier table renderer.

`bin/validate && bin/export && bin/reindex` all clean: 77 records, 9 topics,
0 errors, 0 warnings, 0 dangling relations, 1 frontier entry.
