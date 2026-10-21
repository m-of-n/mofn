# Produced

Model: Claude Opus 5.5 · 2026-10-17 · tooling, no specification text.

## What was built

The issue's suggested shape, plus the validator half it described but did not
prescribe.

| file | change |
|---|---|
| `bin/manifest` | `sources()` adds `research/*/report.md`, staged as `<slug>.md`; `source` in the manifest is the real repo path |
| `bin/build-site` | stages `research/*/report.md` → `docs/research/<slug>.md` |
| `bin/validate-archdoc` | validates `research/*/report.md`; id kinds gain `R` and `RPT` |
| `research/README.md` | new §*What publishes* — the rule, written down |
| `mkdocs.nav.yml`, `project/PUBLISHING.md` | regenerated: 29 → 34 documents |

**The first two rows did not ship — see *Superseded by mofn#103* below.**

Answers to #88's four questions, as built:

1. **`report.md` only.** Evidence (`sources.md`, `searches.md`,
   `unverified.md`) stays in the repo; `dimensions/` and `mini-reports/` never
   publish.
2. **`title`**, as for `spec/` and `project/`.
3. **Drafts publish.** Status is in front matter and flagged ⚠️ in
   `PUBLISHING.md`; PROC-0004 §9.4 asks that drafts not *read as settled*, not
   that they stay private.
4. **Sorted by directory name.** The id collision is documented, not fixed.

## Verification

- `bin/validate-archdoc`: 34 documents, 0 errors — all five reports already
  conformed. A probe report with a bad id and missing keys produced 6 errors
  and exit 1, then was removed.
- `mkdocs build --strict` (pinned `requirements-docs.txt`): passes; all five
  reports render at `research/<slug>/`. No report contains a relative link, so
  staging `report.md` without its siblings breaks nothing.
- `bin/lib-sync --check`: clean.
- **Not run locally:** `bin/build-site` end to end. The session's worktree
  isolation refused to run the library's `bin/export`/`bin/reindex`, so the
  build was staged by hand with a placeholder bibliography page. CI's `docs`
  job runs the real thing.

## Alternatives the model considered and rejected

- **Publish the evidence files too.** It would strengthen the "archive the
  basis" claim, but they are not written as pages, two reports' evidence files
  have no front matter, and `unverified.md` is a publication *gate* — putting
  it on the site defeats its purpose. They are one click away on GitHub.
- **Nav title from `short_title`.** Shorter, but spec/ and project/ use
  `title`, and switching globally would rename existing nav entries — scope
  creep in a bug fix.
- **Renumber `0001-cbor` / `RPT-0001` to resolve the collision.** The id is
  cited from PRs, the design log and `library` records; a design-log id
  "must not silently retarget" and the same logic holds here. Documented in
  `research/README.md` instead; renumbering is the team's call.
- **Have `build-site` read the staged set from `docs/manifest.json`** so the
  two generators cannot drift. Cleaner, but changes how every tree stages for
  a research-only bug. Both scripts carry a "keep in step" comment instead.
- **Validate the evidence files.** They are not `archdoc/v1` documents; adding
  front matter to them would be churn across reports this change does not own.

## Superseded by mofn#103 (2026-10-20)

mofn#103 (the D3 reports, `design-log/0012-d3-context-and-mechanism`) merged
its **own** fix for the publishing half of #88 first, to get `R-0005` and
`R-0006` onto Pages. The two fixes were written in parallel and disagree on
one thing: where a report lands.

| | this entry, as first built | mofn#103, on `main` |
|---|---|---|
| staged to | `docs/research/<slug>.md` | `docs/research/<slug>/report.md` |
| URL | `research/<slug>/` | `research/<slug>/report/` |
| `bin/manifest` | a `sources(d)` helper | a per-tree glob list in `TREES` |

Merging `main` into this branch took **mofn#103's `bin/manifest` and
`bin/build-site` whole** and dropped this branch's. Reason: #103's URLs are
already live and linked from #100, and changing them in a fix would break
links for no gain. Neither shape is wrong. `research/README.md` now names the
`report/` URL.

What this change still carries, and #103 did not: **validation**
(`bin/validate-archdoc` on `research/*/report.md`, kinds `R`/`RPT`, so
ARCH-0001 §9.5 is enforced on reports) and the **written rule**
(`research/README.md` §*What publishes*). Both answer #88 as filed.

Also renumbered `0012` → `0013`: `main` already held two `0012` entries
(mofn#103, mofn#109). See `design-log/README.md`.
