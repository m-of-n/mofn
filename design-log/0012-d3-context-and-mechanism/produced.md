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
| `research/0005-context/sources.md` | — | **101** keys, zero unresolved; where each claim's evidence was retrieved. The "72" first recorded here was a miscount — §7 |
| `research/0005-context/searches.md` | — | **no searches were run** — the method limitation, stated |
| `research/0006-mechanism/report.md` | 809 | **R-0006** — comparative anatomy; the DEC-002/DEC-004 evidence |
| `research/0006-mechanism/sources.md` | — | the four load-bearing records and what each supplies |
| `research/0006-mechanism/searches.md` | — | as above, plus why staleness bites less here |
| `project/BACKLOG-0001.md` | 0.10.0 → **0.11.1** | T-025, T-026 → `review`; T-027 corrected; T-031 narrowed — §7 |
| `library` submodule pin | `31aabab` → **`f57dcbc`** → **`60b3284`** | §1, §7 |

Nothing in `spec/`. Nothing in `src/`. **No `DEC-*` decided, narrowed, or
recommended.**

**§7 is a second pass, dated 2026-10-16**, reconciling both reports with
`ADR-0003` and the KSA specifications, which landed after the first pass and
are the reason this change needed more than a rebase.

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

---

## 7. Second pass, 2026-10-16 — reconciling with ADR-0003

The first pass was written on 2026-10-14. That same day, `ARCH-0003` (mofn#102)
and then `ADR-0003` with `SPEC-0001`…`SPEC-0005`, `UC-0001` and
`spec/vectors/ksa-core/` (mofn#104) merged to `main`. The branch went stale in
three files and **wrong in four claims**, which is the part a rebase does not
fix.

### 7.1 What the conflicts actually were

`library` (the submodule pin, `f57dcbc` versus `main`'s `60b3284`) and
`project/PUBLISHING.md` (generated). `mkdocs.nav.yml` auto-merged. All three
are generated or pin files: `main`'s side was taken and the generators re-run.
**No authored content conflicted**, which is the one thing the publishing fix
in §6 is responsible for — the nav is generated, so a nav conflict is never a
content decision.

The pin move to `60b3284` had an unlooked-for effect. §3 of `review.md` raised
that **four keys R-001 cites did not resolve at `f57dcbc`**. All four —
`zooko-2001-names`, `w3c-did-core`, `zcap-ld`, `wang-2006-reducing-spki` —
**resolve at `60b3284`**, and a full re-check finds all 175 of R-001's distinct
keys resolving. So the cause was the third of the three the model could not
choose between: the records existed and the pin was behind them. The finding is
**resolved, not merely stale**, and `review.md` §3 now says so. R-001 still
carries no `library_pin`, which was the other half of that finding and is still
true.

### 7.2 The four claims that were wrong, and are retracted in place

| claim in v0.1.0 | status | where |
|---|---|---|
| P5.1 "landed in `ARCH-0002` v0.6.0 (mofn#72)" | **wrong twice.** mofn#97 is open and carries it as v0.7.0; `ARCH-0002` v0.6.0 on `main` is an unrelated revision | R-0006 §3.2 |
| P5.2 "Resolved … in `ARCH-0002` v0.6.0" | **wrong, same cause** | R-0006 §5.2 |
| condition (5) supplied by no candidate, and "no decoder can supply (5)" | **true of encodings, and the wrong place to look.** `SPEC-0003` §6 supplies it for ranges, per base kind | R-0006 §3.2, §3.12, §3.13 |
| "The round-trip fixtures do not exist … none has been built, under any option" | **overtaken.** `spec/vectors/ksa-core/` exists; the threshold subject is the gap | R-0006 §3.12, §6 |

All four are **retracted in the text with the reason**, not edited out. The
first two were forward references to a sibling branch written as though it had
merged — the specific failure mode of running several lanes at once, and the
third instance in this design log after `DL-0009` §4 and `DL-0011`'s rename
collision.

### 7.3 §3.13 is the new material, and it is a finding about our own documents

The reconciliation was expected to be bookkeeping. It was not: reading
`SPEC-0002` §8.6 against the report's own condition (5) turned up that the
threshold member list `trusts` is specified as `[2* kid]` — an array — while
`SPEC-0004` §6.4 calls it a set — *"trusts a set `M` of keys"* — and that
`SPEC-0002` §4.1 makes array order *"significant and signed"*. `SPEC-0003` kind 7 has exactly the rule
required, *"an array of distinct kids, sorted"*, one document away and not
invoked.

That makes one semantic trust statement have as many statement digests as its
member list has permutations, on the **identity** path, which is the precise
asymmetry R-0006 §3.1 predicted in the abstract. Two further instances —
`about` and the `may-delegate` key lists — and one undefined comparison,
`SPEC-0004` §6.4's *"identical `about` and `may-delegate`"*, came out of the
same read.

**This is the most consequential thing in the change and it is the thing the
model is least entitled to act on.** It is written as a finding with every
section cited inline so a reviewer can check it without trusting the report,
and the fix is not proposed. See `review.md` §4 and §6.

### 7.4 The miscount, found by re-counting

`sources.md` claimed **72 distinct keys** for R-0005. The real figure is
**101**. The first pass's counting pass missed multi-key citations of the form
`[@a; @b]`, of which `report.md` has several, so the count was wrong while the
*resolution* claim — zero unresolved — was right then and is right now. Fixed in
`sources.md` with the cause stated, and in `searches.md`.

§4 of this file says citation keys *"were checked mechanically, and it
mattered."* It did matter, and it was also checked with a pattern that could not
see half the syntax it was checking. Both halves of that belong on the record.

### 7.5 Two stale backlog rows, fixed while in the file

**T-027 said "not started."** R-0004 merged in mofn#87 on 2026-10-12. The row
was stale, not the work — the same shape as T-029e in mofn#97, and the second
time in two weeks that a merged report left its own backlog row behind.

**T-031 is narrowed, not done.** It now names the threshold-subject vector as
the remaining gap and cites R-0006 §3.12 and §3.13 for why.
