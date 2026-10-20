# Question

**Asked (2026-10-17):** "complete #88"

No further context. mofn#88 is the issue body; it is the brief.

## What #88 established

- `bin/build-site` copied `research/*.md` and `bin/manifest` globbed
  `research/*.md`. `research/README.md` lays reports out as
  `research/NNNN-slug/report.md`. So **no research report has ever reached the
  site, the nav, `project/PUBLISHING.md` or `docs/manifest.json`** — only
  `research/README.md` did.
- `bin/validate-archdoc` checks `spec/` and `project/` only. The `archdoc/v1`
  front matter on every report was **decorative**, and the ARCH-0001 §9.5
  `version`/`updated` rule — which `CLAUDE.md` says CI enforces — was not
  enforced for any report.
- D3 (PROC-0004 §3: three reports, *markdown, published*) cannot be called done
  until a report is reachable on the site.

## What #88 left to decide

1. Which files publish — `report.md` only, or the evidence files too?
2. What the nav title is.
3. Whether drafts publish at all.
4. Ordering, given two `0001-` directories (`RPT-0001`, `R-0001`).

The issue suggested a shape: recurse one level, publish `report.md` only, title
from front matter, stage to `docs/research/<slug>.md`, and write the rule into
`research/README.md`.
