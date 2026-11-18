---
schema: "design-log/v1"
id: DL-0051
part: produced
date: "2026-11-17"
---

# DL-0051 — produced

## What the audit found (origin/main at 732d777)

- **Landing page wrong.** `docs/index.md` said *pre-implementation* and
  *DEC-001 … DEC-005 and DEC-007 are open*. DEC-001, 002, 003 and 007 are
  accepted (ADR-0006, 0004, 0005, 0007); the wallet has shipped pre-releases.
  It also linked the v0.2.0 proposal as "under review"; it was folded into
  ARCH-0001 v0.2.0 on 2026-11-07.
- **Download page wrong.** It said there was nothing to download;
  `wallet-v0.8.1` and `wallet-v0.10.0` exist, and APP-0005 documents them.
- **Both were tracked inside `docs/`**, the directory CLAUDE.md says never to
  edit, so nothing regenerated or reviewed them.
- **Nav.** One flat list per section sorted by filename: eight ADRs ahead of
  ARCH-0001, full titles up to ~120 characters, research's README titled
  "README".
- **No page showed its status** on the site, though every document declares
  one; PROC-0004 §9 asks that nothing draft read as settled.
- **No styling hook**: no `extra_css`, no `custom_dir`.
- Links: `--strict` already caught missing pages; anchors were not checked.

## Changes

| file | change |
|---|---|
| `bin/manifest` | nav grouped by `type` (Architecture / Decisions / Specifications / Proposals and changelogs; Plans / Application / Process / Reference / Retrospectives), `short_title` as label, id prefixed for ARCH/SPEC/UC, ARCH-0001 and research README pinned first, unknown type → "Other" so no page drops |
| `site-src/index.md`, `site-src/download.md` | moved from `docs/`; status section rewritten to point at the ADRs and the register instead of enumerating decisions; download points at the releases and APP-0005 |
| `site-src/overrides/main.html` | status banner from front matter: status, id, version, updated, *not yet reviewed*, source link |
| `site-src/assets/extra.css` | banner colours (light/dark), tables scroll inside the page, long codes wrap |
| `bin/build-site` | stages `site-src/*.md` and `site-src/assets/` into `docs/` |
| `.gitignore` | `docs/` ignored as a whole |
| `mkdocs.yml` | `custom_dir`, `extra_css`, indigo/teal palette, `repo_url`, `validation.links.anchors: warn` (fails under `--strict`) |

Verified: `bin/build-site` passes `--strict` with anchor checking on (a
planted bad anchor aborts it); `bin/validate-archdoc` 0 errors;
`bin/lib-sync --check` clean.
