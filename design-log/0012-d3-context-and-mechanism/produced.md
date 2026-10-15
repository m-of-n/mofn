---
schema: "design-log/v1"
id: DL-0012
part: produced
date: "2026-10-14"
---

# DL-0012 — produced

| file | lines | what it is |
|---|---|---|
| `research/0005-context/report.md` | 632 | **R-0005** — why provenance, why now; the historic gap |
| `research/0005-context/sources.md` | — | 72 keys, zero unresolved; where each claim's evidence was retrieved |
| `research/0005-context/searches.md` | — | **no searches were run** — the method limitation, stated |
| `research/0006-mechanism/report.md` | 809 | **R-0006** — comparative anatomy; the DEC-002/DEC-004 evidence |
| `research/0006-mechanism/sources.md` | — | the four load-bearing records and what each supplies |
| `research/0006-mechanism/searches.md` | — | as above, plus why staleness bites less here |
| `project/BACKLOG-0001.md` | 0.10.0 → **0.11.0** | T-025, T-026 → `review` |
| `library` submodule pin | `31aabab` → **`f57dcbc`** | §1 |

Nothing in `spec/`. Nothing in `src/`. **No `DEC-*` decided, narrowed, or
recommended.**

---

## 1. The pin move, and why it was not optional

`bin/lib-sync --check` was **failing on `main`**: the pin had been advanced to
`f57dcbc` in the working tree and never staged. The model flagged this two turns
earlier as a pre-existing condition and did not touch it.

T-026 forced the issue. Its evidence base is RFC 9804's FX-1 extraction and RFC
8785's pass 3 — library#46 — and **neither exists at `31aabab`**. At that pin
`records/ietf/rfc-8785/` is absent entirely and `rfc-9804/distilled/` does not
exist. Writing the mechanism report against the committed pin was not possible;
writing it against an unstaged working-tree state and citing `library@f57dcbc`
would have produced a report whose bibliography did not reproduce.

So the pin moved, staged, in this change. `f57dcbc` was verified present on
`origin/main` first.

**This answers `DECISIONS-0001` Tier 3 item 11 by doing it** — *"who moves the
submodule pin, the lane that merged or whoever next needs it?"* — in favour of
*whoever next needs it*. Recorded as a data point, not filed as a closure;
closing a register item is not an agent's call.

## 2. R-0005 — the shape chosen, and the one that was rejected

**Chosen:** narrow guarantee → four forcing functions → the five-axis frame →
four ancestors → two conflations → the gap stated as a conjunction → the
counter-argument.

**Rejected:** the obvious chronological shape — 1976, 1988, 1996, 1999, 2020 —
which R-001 already does better and at greater length. A context report that
retells the survey's history adds a worse copy of §§4–6. The four-ancestor
section is therefore organised by **what each contributed to this design**, not
by date, and each subsection ends with what the project takes from it.

Three things in the report are arrangement rather than restatement, and they
are the contribution such as it is:

- **§3's four forcing functions.** R-001 has all four pieces — incidents in §8,
  statute in §8.4, Sigstore/ACME in §8.2, agentic drafts in §9.2 — and never
  groups them as an answer to *why now*. The grouping yields the claim that
  §3.5 states: none of the four is a cryptographic problem.
- **§7's conjunction table.** Four properties, who has each, who lacks it. The
  gap is the conjunction, not any row.
- **§5.1's distinction.** *X.509 cannot express scoped delegation* is false and
  the project should stop reaching for it; *X.509 has not, measurably, in
  seventeen years* is true and is the stronger argument. RFC 3820 exists and
  gives X.509 SPKI's delegation bit and depth control on the standards track.

## 3. R-0006 — the hard part was §3.9

The scoring material is dense and already written; arranging it was
straightforward. **One section took most of the judgement.**

R-0006 is commissioned as *the evidence base for DEC-002*. The evidence, honestly
assembled, runs against MD-3's narrowing — and against the older sponsor
correction of 2026-09-16 that recorded RFC 9804 as historical and option 1 as
*not a contender*. Three shapes were available:

| | | |
|---|---|---|
| i | score only option 5, as MD-3 directed | **rejected** — a mechanism report that omits the candidate the late evidence favours is not evidence, it is advocacy |
| ii | score all four and recommend option 1 | **rejected** — that is taking DEC-002, which `CLAUDE.md` forbids absolutely and which the material does not support anyway (§3.8: the rankings disagree) |
| iii | score all four, state where the evidence sits relative to both decisions, and name the question nobody has been asked | **taken** |

§3.9 is (iii). It says the scoring postdates both decisions, states the question
— *does "historical" describe the document's status or the encoding's fitness?*
— and routes it to mofn#8 as an agenda item for a human. It says twice that it
does not reopen either decision.

**§7 is the other half of that discipline.** It records what the report refuses
to recommend and why the refusal is substantive: the six conditions and the
three acceptance axes rank the candidates differently, the two criteria against
option 1 are ones no fixture will change, and the two unsatisfied conditions
depend on P4, which is held. *A recommendation drawn from that material would be
a preference wearing a table.*

## 4. Citation keys were checked mechanically, and it mattered

Both reports were checked with a script that extracts every `[@key]` and
resolves it against `library/records/*/` at the pin. **R-0005: 72 distinct keys,
zero unresolved. R-0006: 15, zero unresolved.**

This was not ceremony. Four keys used by R-001 — `zooko-2001-names`,
`w3c-did-core`, `zcap-ld`, `wang-2006-reducing-spki` — **do not resolve at
`f57dcbc`**, and the first draft of R-0005 would have cited at least two of
them from memory of the survey text. They were replaced with attributions to
R-001 §5.6, §5.7 and §9.2 instead. A citation key that does not resolve is
exactly the *"report that cites a URL inline and nowhere else"* failure
`research/README.md` warns about, one layer in.

**Worth raising:** R-001 cites keys that no longer resolve at the current pin.
Whether the records were renamed, removed in the Threat-Radar fold-back
(`c95f204`), or never existed is not established here. Proposed in `review.md`
§3 as something to check, not filed.

## 5. The two companion files are the honest half

Four files nobody will read first, and they carry the method limitation:

- **No retrieval pass.** Both `searches.md` files lead with it.
- **R-0005 cannot have found anything R-001 and R-0004 missed** — its own
  `searches.md` says so, and names the consequence: statutory material in §3.2
  is the most time-sensitive and the most likely to have moved since 2026-09-26.
- **R-0006's staleness exposure is narrower** and is named precisely: the CBOR
  profile drafts, which moved to `deterministic-cbor-profiles` and are not
  scored, and the 2026 agentic drafts, whose constraint vocabularies are exactly
  what changes between revisions.

## 6. A defect found while publishing: no research report has ever reached the site

`PROC-0004` §3 requires the D3 reports be *"markdown, **published**"*. They were
not, and had not been since the tree was created.

`bin/manifest`'s `TREES` globbed `*.md` at each tree root. `research/` keeps a
report at `NNNN-slug/report.md`, so **the glob matched only
`research/README.md`** — and `bin/build-site` line 36 had the identical blind
spot, staging `research/*.md` and nothing below it. R-0001, R-0002, R-0003 and
**R-0004, merged two days ago as a D3 deliverable**, were authored, reviewed and
never navigable.

The generated nav hid it rather than catching it: it faithfully generated a
Research section containing one entry, and nothing compares that against what is
on disk.

Fixed in both generators, which must agree or `mkdocs build --strict` fails on a
nav entry with no page:

- `bin/manifest` — `TREES` carries a per-tree glob list; `research` gets
  `["*.md", "*/report.md"]`. Document records now key off the path **relative to
  the tree** rather than the bare filename, so `source`, `url` and the nav entry
  stay consistent for a nested page. A second `TREES` loop at the PUBLISHING
  table needed the same arity fix.
- `bin/build-site` — stages each `research/*/report.md` to
  `docs/research/<slug>/report.md`. **Only `report.md`** is published;
  `sources.md` and `searches.md` are evidence for a reviewer, not site pages.

**Verified**, with the limit stated: `mkdocs` is not installed in this
environment, so `mkdocs build --strict` was **not** run locally. What was run is
the check that reproduces its failure mode — stage the tree exactly as
`build-site` does, then resolve all 33 nav entries against the staged files.
**All seven research reports resolve**, as do every `spec/` and `project/`
entry. The three that do not — `LIMITATIONS.md`, `library/construction.md`,
`library/bibliography.md` — come from `build-site` lines this change does not
touch and were not staged by the simulation. CI's `docs` job is the real gate.

Document count went **21 → 28**.
