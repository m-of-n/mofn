---
schema: "design-log/v1"
id: DL-0004
part: produced
date: "2026-10-01"
---

# DL-0004 — produced

Three PRs. The first is the decision; the other two are defects the first one
turned up.

| PR | repo | what |
|---|---|---|
| [library#34](https://github.com/m-of-n/library/pull/34) | `library` | the decision — 9 files, +242 −64 |
| [library#37](https://github.com/m-of-n/library/pull/37) | `library` | library#36, stacked on #34 — 2 files |
| [mofn#55](https://github.com/m-of-n/mofn/pull/55) | `mofn` | the nav generator bug — 4 files |

## library#34 — the decision

## The rule, as a document

`docs/scope.md` §4 rewritten (v0.2.0 → v0.3.0), heading changed from
*"storage is hierarchical"* to **"`body` is a shelf, not a byline"**. A
three-row table pairing each question with the one field that answers it; the
CycloneDX case worked through to show nothing is lost; the corollary that a
re-publication of the same text under another body is an `identifiers` entry
and not a record; and the cheap-reversal argument (`body` is a directory, so
reshelving is `git mv` plus `bin/reindex`, and ids never move) as the reason
this was safe to decide rather than defer a third time.

**Both rejected options are written up with the condition that would reopen
one.** "Split the field" — a multi-valued `publishers`/`standardized_by` — is
recorded as the honest model of dual affiliation and the only option with real
query power, rejected *for now* because nothing queries it yet, and named as the
right answer the moment a report needs *"every record ratified by a body other
than its author."*

§4 also closes what revision 2 carried as **open question 2** ("when does a body
directory get created?"): a value earns a directory by making records easier to
find, so `regulator` collapsing EU and US sources is a shelving choice, not a
claim about legal entities. Open-question list renumbered; §1, §5 and §6 were
left alone because records and `bin/reindex` cite them by number.

## The premise the issue got wrong

#27 says `publisher` is "already rendered in the bibliography" and that only
`identifiers.ecma` is lost. Reading `bin/reindex` instead of taking that at face
value:

- **`publisher` was rendered nowhere.** The bibliography emitted authors, date
  and one identifier. It reached CSL-JSON via `bin/export` and no human-visible
  view.
- **`identifiers` rendered only `rfc` and `doi`** — so `ecma`, `iso`, `nist`,
  `eo` and `draft` were all invisible, not just `ecma`.

So option 1 as stated was lossy, and accepting it required `bin/reindex` changes
it did not mention: `publisher` now renders; every identifier scheme now renders
(an RFC's DOI dropped when both are present, since it only restates the number);
and both `index/records.md` and `index/bibliography.md` carry a one-line note
under the title saying the sections are **storage shelves, not publisher
attribution** — which is job 3, the section heading, fixed at the point a reader
would otherwise misread it.

## Five copies of one enum, down to one

The `body` values existed in `schema/record.schema.yaml`, `schema/tags.yaml`,
`bin/validate`, and **twice** in `bin/ingest`. The `tags.yaml` copy had drifted.

Resolved by **deletion rather than resync**: `body` is not a tag, so it leaves
`tags.yaml` (v0.1.0 → v0.2.0) and is replaced there by a comment saying why.
`schema/record.schema.yaml:fields.body` (v0.5.0 → v0.6.0) becomes the single
declaration; `bin/validate` and `bin/ingest` parse it at run time.

The enum's `values` was converted from a flow list to a **block sequence**,
because `bin/_yaml.py` is deliberately dependency-free and has no flow
collections — a flow list parses as a truncated string, which would have given
each tool a *silently different* list than the schema. Both tools now exit
non-zero with a message naming the cause if the list is reflowed. Verified by
reflowing it.

`schema/record.schema.yaml` also gained real notes on `publisher` (the
publisher-identity field; MAY name two, author first) and `identifiers` (open
map, every key rendered), and a `storage.values` note forbidding further copies.

## A rule that binds without a 280-record migration

`bin/validate` warns when a record at `read`/`summarized`/`distilled` names no
publisher. Measured first: **158 of 280 records have no publisher, and 0 of
those 158 is past `fetched`.** So the warning fires zero times today and binds
every record from the next read onward. A backfill would have touched records
owned by three open lanes (library#19, #28, #29) for no present gain.

## Records and skills

- `records/community/cyclonedx-1-7/record.yaml`: `publisher` changed from
  `"Ecma International"` to `"OWASP Foundation / Ecma International"`, and the
  comment block that said `body: community` was *provisional, filed as an issue
  rather than decided* rewritten to say it is settled and why.
- `.claude/skills/ingest-reference/SKILL.md` and `summarize/SKILL.md`: both told
  agents to prefer a controlled tag from `schema/tags.yaml` "— subject, body,
  role". `body` is no longer there, so both now say so and point at `publisher`.

## Gates

`bin/validate` 280 records / 17 topics / 0 errors / 0 warnings;
`bin/export && bin/reindex` 280 records, 0 dangling;
`bin/check-pr-extraction origin/main` 1 record touched, FX-1 met.
`index/` and `exports/` untracked since library#31, so nothing generated is in
the diff.

## Deliberately not done

- **No `DEC-*` touched and no ADR written.** This is library curation, not
  m-of-n architecture; DEC-001…005 and DEC-007 stay open.
- **No backfill of `publisher`** — see above.
- **`records/other/ecma-424/` left in place.** Found during the work: a bare
  stub (`body: other`, no digest, no publisher) duplicating `cyclonedx-1-7` —
  the same text under the other body, which §4 now states is an `identifiers`
  entry and not a record. It is the predicted failure mode of treating `body` as
  an authority claim, which makes it evidence for the decision. Not fixed here:
  ids are stable forever and retiring a record is not a reshelving, so it is a
  decision for the owning lane, raised as its own issue.

## library#37 and mofn#55 — what the first PR turned up

`library#36` was filed by the model during the first half, for instructions
left stale by library#31. Acting on it found **two false claims of its own and
one live bug** (see `review.md` for the false claims).

**library#37**, stacked on #34 because it edits step 7 of the same skill file
four lines from step 9:

- `.claude/skills/ingest-reference/SKILL.md` step 9 told agents to commit
  `index/` and `exports/` and said CI fails if you skip it. Both halves are
  inverted after library#31 — the paths are gitignored, and CI fails if they
  *are* tracked. Rewritten to run the generators and not commit them.
- `docs/gaps.md` §6 cited `docs/scope.md` §4 as describing a signed statement
  over `MANIFEST.yaml` as the federation integrity mechanism. §4 has never
  mentioned federation, in **either** revision — a wrong citation, not a stale
  one, checked against git history rather than current main. Corrected to
  `docs/construction.md` decision 4, which describes the mechanism as *content
  hash is identity*: digest-based, so two libraries agree which document they
  mean and nothing about who said so. Signing is therefore federation's
  **undesigned** half, which is a sharper gap than the bullet claimed.

**mofn#55** — the one item that was a live bug with a published consequence
rather than a wording fix:

`bin/manifest` decided whether to list the library bibliography in the nav by
testing whether `library/index/bibliography.md` exists — generated and
gitignored since library#31. So it asked *"has somebody run `bin/reindex`
here"*, not *"does the pinned library provide a bibliography"*. `bin/build-site`
then ran `bin/manifest` **before** generating the views, so on every clean
checkout the page was staged into the site and omitted from the nav. The tracked
`mkdocs.nav.yml` still listed it, so `git status` looked clean, and mkdocs
reports a not-in-nav page at INFO level, so `--strict` missed it.

**The deployed site has a bibliography nobody can navigate to** — in a repo
whose `CLAUDE.md` generates the nav on purpose because a hand-kept one rots.
Fixed by generating the views before the nav, and by testing the *generator*
rather than its output, with a fallback for a pre-library#31 pin. Verified three
ways: listed on a clean checkout, byte-identical nav with and without
`library/index/` present, omitted with a stderr warning when `bin/reindex` is
removed.

It also carried a second instance of the same class: `PLAN-0003` is a published
document that appeared in neither the nav nor `project/PUBLISHING.md`, and
nothing in CI gates either file.
