# research/

Authored research **reports** on the project's subject matter, and the evidence
behind them. Published to Pages.

```
research/
  NNNN-slug/
    report.md     archdoc-style front matter; the finding and its basis
    sources.md    every source consulted, with retrieval dates
    searches.md   the queries run, verbatim, and their yield
```

D3 lives here: **context**, **mechanism**, **uptake & applications**.

## What publishes

**`report.md` only**, staged to the site as `research/<NNNN-slug>/` and listed
in the nav under its front-matter `title`. `bin/manifest` and `bin/build-site`
select it; nobody adds it to a list.

- **Drafts publish.** Every report states its `status`, and
  `project/PUBLISHING.md` flags drafts — PROC-0004 §9.4 asks that nothing
  draft reads as settled, not that drafts stay private.
- **Evidence does not publish.** `sources.md`, `searches.md`, `unverified.md`
  and the like stay in the repository, linked from GitHub. They are the
  archived basis, not reader-facing pages.
- **Raw agent outputs never publish.** `dimensions/` and `mini-reports/` are
  unverified and marked *do not cite*.
- **`report.md` is validated.** `bin/validate-archdoc` enforces the
  `archdoc/v1` front matter and the ARCH-0001 §9.5 `version`/`updated` rule on
  it, as for `spec/` and `project/`. Set `publish: false` to withhold one.
- **A report links only to absolute URLs.** It is staged without its sibling
  files, so a relative link to `sources.md` fails `mkdocs --strict`.

The directory number is **not** an id: `0001-cbor` (`RPT-0001`) and
`0001-signatures-and-attestation` (`R-0001`) share it. Cite a report by its
front-matter `id`. New reports take the next free `R-NNNN` and the matching
directory number.

Two rules, both learned the hard way:

1. **Every source that mattered also gets a `library/records/` entry.** A report
   that cites a URL inline and nowhere else is a report whose evidence
   evaporates.
2. **Archive the searches, not just the findings.** `docs/construction.md` in
   the library was written from research that was then discarded — the
   conclusions survived, the basis did not. Wohlin snowballing requires
   recording each iteration's yield, and that is impossible retroactively.

Research about *how to run the library* — bibliography method, ingestion
workflow — goes in `library/research/`, not here.
