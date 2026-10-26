---
schema: "archdoc/v1"
id: DECISIONS-0001
title: "Open decision register — everything waiting on a human"
short_title: "Decision register"
description: "Every open decision across both repos, ranked by what it blocks. The sponsor review list."
type: process
category: process
status: active
version: "0.3.4"
version_policy: "semver; MINOR = decisions added or closed"
date: "2026-09-22"
updated: "2026-10-25"
decision_makers:
  - role: sponsor
    id: paul-lambert
  - role: student
    id: ndewedo-newbury
    authority: >
      Delegated by the sponsor on 2026-10-25 to accept, by ADR under
      ARCH-0001 §9.2, the open decisions recorded in ARCH-0001 §7 (Tier 1 items 2 and 4b). Relayed
      verbally by ndewedo-newbury; the sponsor confirms on the PR that adds
      this entry. Does not extend to ADR-0002 (DECISIONS-0001 item 4a).
reviewers: []
needs_review: false
reviewed: false
review_note: >
  The register itself is live, not under review. Its ITEMS are what
  await a decision — that is the document's whole content.
canonical_path: project/DECISIONS-0001.md
defers_to: ARCH-0001
companion:
  - project/meetings/2026-09-28.md
agent_notes: >
  A register, not an authority. Accepting any DEC-* still requires an ADR plus
  a changelog line plus a status update in ARCH-0001 (§9.2). Nothing here
  accepts anything — and in particular MD-3 NARROWED DEC-002 without accepting
  it, so DEC-002 is still open and no code or vector may assume an encoding.
---

# Open decision register

**Checkpoint 2026-10-10.** Brought up to date with the weekly of **2026-09-28**
(`project/meetings/2026-09-28.md`), which took seven decisions — **MD-1 … MD-7** —
four of which answered items this register was still printing as open. The
register had not moved since 2026-09-23; the gap is recorded in §*What changed*
below rather than edited away.

Ordered by **what it unblocks**, not by importance.

> **`MD-1 … MD-7` are the dated decisions of 2026-09-28**; `D0 … D10` are
> semester *deliverables* (`PLAN-0003`). They were both written `D-n` until
> **2026-10-11**, when the decisions were renamed to `MD-n` — item 27, now
> closed. **Older text citing `D-3` means `MD-3`, never `D3`;** the redirect is
> in `GLOSSARY-0001`.

---

## Tier 1 — blocks the demo floor (I3, Nov 11)

| # | Decision | Where | Why it blocks |
|---|---|---|---|
| ~~1~~ | ~~**Does R-M-12 stand?**~~ **DECIDED 2026-09-22 — yes.** `ADR-0001`; now `ARCH-0002` P1. | ADR-0001 | closed |
| **2** | **DEC-002 — the encoding. NARROWED 2026-09-28 by MD-3 to option 5** (CBOR data model, no IANA tags, COSE export only; YAML as the human form). **Still open: a narrowing is not an acceptance, and no ADR exists.** Option 2 is retained only as the comparison fixture. See the standing note below — the library's evidence now cuts against the narrowing. | ARCH-0001 §7, proposal §3.3, mofn#8 | Everything downstream. WP1 is encoding-neutral by design, but D5 needs a target by **Oct 28**. |
| ~~3~~ | ~~**Who drives the agent lanes — students or sponsor?**~~ **ANSWERED 2026-09-28 by MD-4** — students drive, with named lanes: David #13 → option-5 encoder fixtures and #23 → D3 mechanism; Ndewedo #14 → D3 and the archives domain. The teaching reading was taken over the throughput one. | PROC-0002 §8.1 | closed |
| **4** | **Accept the proposal as ARCH-0001 v0.2.0?** DEC-007 filed, DEC-006 withdrawn, R-M-11, R-O-05, R-O-06, RFC 9943 citation. **Not on any agenda to date.** | proposal | Until accepted, ARCH-0001 still cites a draft that became an RFC in June 2026, and R-M-11/R-O-05/R-O-06 have no force — while roughly thirty library records already name them in `bears_on`. See the standing note below. |
| **4a** | **Accept `ADR-0002`?** MD-2 granted P2, P3, P5, P6 *provisionally* and said each becomes final "only through an ADR after review". `ADR-0002` has landed at `status: proposed` (#83). **Both acceptance conditions are now met:** §6(b) by `ARCH-0002` v0.7.0 carrying the amended P5 (#72), and §6(a) by the review of **2026-10-16** — v0.7.1 carries a reviewer and `reviewed: true`. **Sharpened 2026-10-14, corrected 2026-10-16:** the citation that binds is `SPEC-0003` §7.1, which cites `ARCH-0002` P5 by name *inside the Definition Publisher conformance class*; `SPEC-0002` §13.5 is the louder quote but sits in Security Considerations, which no conformance class requires. The SPECs are themselves `draft` — what is accepted is `ADR-0003`, whose consequences make them govern (ADR-0002 §6a). **What is left is a judgement, not a condition:** the reviewer wrote P5.1 and P5.2, so the sponsor accepts either P5 **as amended**, or P2/P3/P6 plus P5 **as drafted** with the two clauses held for a second reader. Then acceptance is a status flip plus a name. | ADR-0002 | `prototype/`, `APP-0001` and three answered library topics already build on P2 and P3. |
| **4b** | **The DEC-002 ADR.** Item 2's instrument. Scoring input is in `library/topics/canonical-encoding.yaml` (`status: answered`) and summarised on mofn#8. | mofn#8 | **Oct 28.** Nothing downstream of D5 can freeze until it is accepted. |

### Standing note on item 2 — `ADR-0003` D2, and what it did not do

**Added 2026-10-15.** `ADR-0003` was accepted on 2026-10-14 and its **D2** fixes
*one canonical encoding for every hashed or signed object* — the deterministic
CBOR profile of FKSA suite 1, which is MD-3's option 5. `SPEC-0002` §4 specifies
it and `spec/vectors/ksa-core/` ships vectors for it.

**D2 says in its own text that it does not accept DEC-002**, and that the
DEC-002 ADR and its fixtures still decide it. Both halves of that should be read
literally. The specifications now have an encoding and can be implemented
against; DEC-002 remains open, item 4b is still the instrument, and the evidence
below — including the post-narrowing findings that favour option 1 — is still
what that ADR must answer. What has changed is the **cost of reopening**: there
are now five SPEC documents and a vector set written against option 5's profile.

That is a fact about cost, not an argument about correctness, and it is recorded
here so a reviewer weighs it deliberately rather than discovering it later.

### Standing note on item 2 — the evidence moved after the narrowing

MD-3 was taken on **2026-09-28**. RFC 9804 reached full FX-1 extraction on
**2026-10-04**, and the `canonical-encoding` topic closed on **2026-10-08**.
The narrowing therefore predates the scoring of option 1, and three findings
bear on it. They are recorded here because a reviewer must be able to see them
without reading an issue thread.

- **Six conditions, not four.** R-O-05 delivers (3) canonicalise once at
  authoring and (4) an authenticated type indicator, and *assumes* (1)
  injectivity and (2) decoder rejection. Two further conditions — (5) a canonical
  order for set-valued fields carried in arrays, and (6) a declared Unicode
  normalisation rule — are **reachable by no candidate and stated in no document
  of ours.** They bite on the *identity* path, where divergence fails silently
  rather than as a signature mismatch.
- **Option 3 should be withdrawn rather than out-scored**, on four grounds; the
  strongest is that RFC 8785 §3.2.3 *prohibits* array reordering where RFC 8949
  §4.2.1 is *silent*, so what we need is a modification of JCS rather than a
  subset — and under R-O-03 a modification is a partly invented algorithm.
- **Option 1 is now on the right side of all four of those grounds**, and also
  wins namespace governance — the criterion the proposal §3.3 says was never
  scored, and which had been recorded as option 3's outright win. What stops it
  being a conclusion is a far poorer data model and library availability, which
  DEC-002 names as a driver.

**This does not reopen MD-3 and nobody should read it as doing so.** It is the
material the ADR must answer, and the reason the ADR is the decision rather than
the minute.

**Both condition-(2) hand-offs are now closed, and one of them moved the
evidence again.** mofn#73 ran the experiment and **the falsifier did not fire**:
canonicality is decidable by parsing alone, single pass, no re-encoding, for
*both* surviving candidates — 60 fixtures, 36 negative (DL-0007). mofn#72 then
landed the rule as `ARCH-0002` P5.1. The consequence for item 2 is narrow and
should not be overstated: condition (2) is no longer a discriminator between
options 1 and 5, because both reach it. What it does expose is a difference in
**kind** — under RFC 9804 smallest-form is in the grammar, so a conforming
reader cannot omit the check; under reduced CBOR it is a rule an implementation
must state, and one that omits it still parses every valid document. That is an
input the ADR must answer. **Conditions (5) and (6) remain open and remain the
gap**; neither is reachable by a decoder, and (5) still depends on P4.

## Tier 1 briefs — both decided 2026-09-28; the analysis is kept

### T1-A · Which target applications are **in scope for the specification**? — **CLOSED 2026-09-28 by MD-1**

**Decision: software supply chain (primary) + archives/library (contrast).**
Option (a), as recommended below. Archives/library was chosen because it lets us
make *statements about the library itself* — records, reviews, distillations —
using a corpus we already run; supply chain keeps the mapping to in-toto, SLSA
and SCITT. **Very short further scenarios, email delegation among them, are
written only as use cases that drive schema definition, not as specified
targets.** This supersedes the "two apps" framing of the September email.

The reasoning is retained because the cost argument governs any future request
to add a third target.

**The distinction.** *In scope* means the specification must be shown to work
for it: a domain of discourse, worked examples, and a section. *Cited as
motivation* means it appears in the introduction and the uptake analysis with
**no normative content**.

**Why it is not free.** Each in-scope target costs a published domain, worked
examples, and interchange mapping. Each one cited costs a paragraph.

**Why it cannot be zero.** A specification demonstrated against exactly one
domain **cannot show that the vocabulary mechanism generalises** — and that
generalisation is the entire P3/P4 claim. One target proves the machinery runs;
it does not prove the thesis.

| target | case for scoping it | cost | outcome |
|---|---|---|---|
| **Software supply chain** | Existing standards to map to (in-toto, SLSA, SCITT), so WP2/WP3 have a real target. A demo pipeline exists | moderate — mapping work already planned | **in scope** |
| **Archives / library** | **We already run one.** Non-software, so it exercises R-M-11's `description` mode. Corpus exists | near zero | **in scope** |
| AI agent attestation | Fastest-moving, least served, where the contribution lands hardest | **high — the target moves.** NIST work began Apr 2026; SCITT profile is a draft | cited as motivation |
| AI media provenance | C2PA adopters | high, crowded, standards-led | not scoped |
| Scientific data | PROV-O adjacent, weak authz today | moderate, no partner | not scoped |
| IoT onboarding | key-centric by nature | high, needs a partner | not scoped |

**Why two and not three.** Two deliberately unlike domains demonstrate
generalisation; a third adds cost without adding evidence. **AI agent
attestation is cited as motivation, not specified against** — specifying against
a target that is itself in flux would date the specification faster than
anything else in it.

### T1-B · Accept ARCH-0002 P2–P7, or hold? — **DECIDED 2026-09-28 by MD-2**

**Decision: P2, P3, P5, P6 accepted *provisionally*; P4 and P7 held.** Exactly
as recommended below. "Provisionally" is load-bearing and is MD-2's own wording:
work may build on them now, **but they are not yet normative, and each becomes
final only through an ADR after review** (`ARCH-0001` §9). That ADR is
`ADR-0002` — register item 4a.

P1 is accepted (`ADR-0001`). Accepting the rest makes them normative and
constrains DEC-002, DEC-004 and DEC-007.

| | principle | evidence today | accepting costs | rec | **outcome** |
|---|---|---|---|---|---|
| **P2** | statement form *A says B has C* | prototype: naming and attestation in one form. **Since strengthened:** the library's `artifact-statements` and `sbom` topics both find a live specification with the *A* missing — vCon is signed by whoever assembled it and never distinguishes ASSEMBLED from ASSERTED | rewrite ARCH-0001 §4.2 | accept | **provisional** |
| **P3** | a type *is* a schema | prototype renders EN/ES with **no type-specific code** | multilingual becomes a requirement | accept | **provisional** |
| **P4** | domains are hash-identified **sets** | one domain hashed in a spike | **tightens DEC-002** — canonicalisation onto the semantic critical path | hold | **held** |
| **P5** | validity checked, unknown rejected | CVE-2025-59420; vCon `critical` shows opt-in is weaker | encoder and verifier must reject | accept | **provisional** |
| **P6** | a name is an attested string | prototype: 91 bytes, same form | resolves 6a; §4.2 rewrite | accept | **provisional** |
| **P7** | authorization is a family by profile | **none — no profile written** | reframes DEC-004 | hold | **held** |

**Why P4 was held** — it carries the largest downstream cost of the six and the
least testing. One domain was hash-identified in a spike. Nobody has versioned a
domain, or had two reference each other, and those are exactly where a set-hash
gets hard. Accepting it tightens DEC-002 before DEC-002 is decided.

> **Consequence now visible.** The `canonical-encoding` answer records that
> conditions (5) and (6) are **conditional on P4** and on `Threshold` members
> being a set rather than a sequence. Holding P4 keeps them live; dropping it
> would shrink the answer to its original four conditions and restore option 3
> to contention. **P4 is therefore no longer only a semantic-layer question —
> it is an input to DEC-002.**

**Why P7 was held** — no profile exists. Accepting a principle *about* profiles
before writing one is asserting a shape we have not tested. Write the
supply-chain profile first (T1-A), then accept P7 or correct it.

## Tier 2 — shapes the work now in flight

| # | Decision | Where |
|---|---|---|
| ~~5~~ | ~~**ARCH-0002?**~~ **DECIDED 2026-09-22 — yes.** | ADR-0001 |
| ~~5a~~ | ~~**ARCH-0002 P2–P5**, all draft~~ — **superseded by MD-2** and by the T1-B outcome column above. P2, P3, P5 are provisional; P6 provisional; P4 and P7 held. | ARCH-0002 |
| **5e** | **DEC-009 — what is the contract form?** A third statement function beside attestation and delegation; the sponsor's note is incomplete. Deliberately unspecified rather than guessed. | ARCH-0002 |
| **5b** | **DEC-008 — can all processing be key-local?** Proposed: yes above a fixed core, never below it. A key that may define its own validity may define itself valid. | ARCH-0002 |
| **5c** | **Is a domain of discourse itself a statement by a key**, inheriting authorization and revocation — or a bare hashed artifact any key may cite? First composes; second allows vocabularies nobody owns. **Held with P4.** | ARCH-0002 P4 |
| **5d** | **Does DEC-007 survive?** P3 and P4 arguably *answer* it rather than constrain it. Re-state in their terms, or close as answered. **Now partly live:** MD-2 made P3 provisional, so DEC-007's premise has moved while DEC-007 has not. The library's `scitt` topic adds that RFC 9943's shape — mandatory `iss`/`sub`, opaque tagged payload — is "worth copying". | ARCH-0002 |
| 6 | **Does `locator` survive R-M-12?** Proposed as non-authoritative evidence; the strict reading excludes global locators from the native model entirely. | proposal §7 |
| 7 | **Which records get PROC-0002 stage 8** (generate code from spec)? Proposed: only where a spec defines an algorithm or wire format we intend to implement or map. | PROC-0002 §8.2 |
| 8 | **Does `versions/` hold a full record per version, or metadata plus a delta note?** | scope §7.1 |
| 9 | **Should `cites` be extracted automatically from converted PDFs, or always reviewed?** Automatic is noisy; manual does not scale. | references §5.1 |
| 10 | **Requirements extracted for every summarised record, or only where we intend to conform or map?** Extraction is expensive. | requirements §5.1 |

## Tier 2b — arising from ARCH-0002 and the retro

| # | Decision | Where |
|---|---|---|
| ~~6a~~ | ~~Five *kinds* or one *form*?~~ **ANSWERED 2026-09-22 by ARCH-0002 P6** — a name is an attested string, so the five are functions over one form. §4.3's three *procedures* stay separate; that was never about object kinds. `AclEntry` is the informative outlier: unsigned, so no speaker, so not a statement — it is the fixed floor DEC-008 needs. **`ARCH-0001` §4.2 still lists five kinds; carrying the answer into it is part of register item 4.** | ~~ARCH-0001 §4.2~~ |
| ~~6b~~ | ~~"Topic" collides~~ · ~~6c~~ ~~"Tag" collides~~ — **WITHDRAWN 2026-09-22.** Neither survives the collision test now stated in `GLOSSARY-0001`: two senses collide only when both can be live in the same context. Both are homonyms across separated repos and documents. Raising them was over-correction after three genuine collisions. | GLOSSARY-0001 |

## Tier 3 — process, decide when convenient

| # | Decision | Where |
|---|---|---|
| 11 | Who moves the submodule pin — the lane that merged, or whoever next needs it? | PROC-0003 §8.3 |
| 12 | Is three to five lanes right for four people with one reviewer? Uncalibrated. | PROC-0003 §8.2 |
| 13 | Is topic ownership exclusive? | PROC-0003 §8.4 |
| 14 | Design-log entries per record or per topic? Per record is unusable at volume. | PROC-0002 §8.6 |
| 15 | Does the adversarial agent see prior human corrections? Sharper, but risks optimising for one reviewer. | PROC-0002 §8.7 |
| 16 | Reference-extraction depth beyond 1 for a named topic? | PROC-0002 §8.4 |
| 17 | Does `usefulness` need forced re-assessment dating? | scope §7.3 |
| 18 | When does a new body directory get created (`regulator` vs `eu`/`us-federal`)? | scope §7.2 |
| 19 | Does `cited_by` belong on a record, or only in `index/`? | references §5.2 |
| 20 | Normalise `verb` SHALL → MUST? Synonymous in RFC 2119; normalising loses the source's wording. | requirements §5.3 |
| 21 | Track requirement **satisfaction** — ours against theirs? That is a conformance matrix and a much larger commitment. | requirements §5.2 |
| ~~27~~ | ~~**Rename one sense of `D-`.**~~ **DONE 2026-10-11.** Both senses were live in one `PLAN-0003` table — `D-3` the encoding decision two rows above `D3` the research reports — which is the collision test `GLOSSARY-0001` states, met exactly. Dated decisions became **`MD-n`**; `D0 … D10` kept, being the wider-used side (issue titles, the backlog `del` column). **129 citations rewritten**, 75 in `mofn` and 54 in `library` (library#65). Redirect note in `GLOSSARY-0001`. | GLOSSARY-0001 |

## Tier 4 — administrative, blocking people not work

| # | Item | State |
|---|---|---|
| 22 | **Faculty repo access.** Invite to `mlim3@usfca.edu` pending since 2026-09-16. `mlim-usfca` is an **organisation**, not a user account — the invite needs a personal GitHub login. **Name unresolved: this register and the USF address read "Mario Lim"; MD-6 and `BACKLOG-0001` T-006b read "Mario Lin".** One is wrong; confirm before re-sending. | blocked on him |
| 23 | **`enforce_admins`** is `false` on both repos. Set so a single member could bootstrap; three admins now exist, so the reason has expired. **Still off at 2026-10-05** (`BACKLOG-0001` T-006c). | ready to flip |
| 24 | **Signed commits** — `CONTRIBUTING.md` asks for them; the requirement is off so students are not blocked on key setup. | deliberate |
| 25 | **`~/cb/.claude/rules/usf-provenance.md`** written but uncommitted — `~/cb` has your in-flight manifest work. | yours to commit |
| 26 | **Shelfmark convergence** — requirements first, then schema. No data merger. | T-023, not started |
| **28** | **Wallet GUI framework — Tauri, tentative (MD-7).** Web frontend plus a Python sidecar; PySide6 is the fallback. **Confirm before GUI work begins** (`BACKLOG-0001` T-029c). | due Oct 14 |

---

## What changed in v0.3.4 — 2026-10-25

Process. **No decision added, closed, or narrowed.** The sponsor delegated
acceptance of `ARCH-0001`'s open decisions to **`ndewedo-newbury`** on
2026-10-25, offering either that or removing `decision_makers` altogether. The
field is kept and filled — here and in `ARCH-0001` v0.1.4 — because an ADR has
to name who accepted it. Consequence for item **4b**: the DEC-002 ADR (and the
DEC-003 ADR, whose inputs are in `ARCH-0001` §7 since v0.1.3) no longer waits
on the sponsor's calendar. Item **4a**, `ADR-0002`, is unchanged and still the
sponsor's.

## What changed in v0.3.3 — 2026-10-16

Editorial. **No decision added, closed, or narrowed.** Item 4a records that
`ADR-0002`'s **first** acceptance condition — MD-2's review — is now met, and
corrects the §6a citation from `SPEC-0002` §13.5 to `SPEC-0003` §7.1, which is
the one inside a conformance class. The item also records the residue the
review leaves: the reviewer authored P5.1 and P5.2, so what remains is the
sponsor's choice between accepting P5 as amended and accepting it as drafted.
**`ADR-0002` is still `proposed`** and `decision_makers` is still empty.

## What changed in v0.3.2 — 2026-10-15

Editorial. **No decision added, closed, or narrowed.** Written up on 2026-10-16:
the 0.3.2 bump landed on a rebase and its entry was missed, which is the defect
this section exists to prevent. Two changes: the standing note on item 2
recording `ADR-0003` D2 — what it fixed, that it declines DEC-002 in terms, and
that reopening now has a cost it did not have before — and the sharpening of
item 4a against `SPEC-0002` §13.5, since corrected in v0.3.3.

## What changed in v0.3.1 — 2026-10-13

Editorial. **No decision added, closed, or narrowed.** Item 4a records that
`ADR-0002`'s second acceptance condition is met and that only MD-2's review
remains; the standing note on item 2 records that mofn#73 and mofn#72 are both
closed, and what their outcome does and does not do to the DEC-002 scoring.

## What changed in v0.3.0 — 2026-10-11

Item **27 closed by doing it**: `D-1 … D-7` are now `MD-1 … MD-7` across both
repositories, with a redirect note in `GLOSSARY-0001` so older citations still
resolve. This register's own `D-n` references moved with them. Nothing else in
the register changed; the v0.2.0 account below stands as written.

## What changed in v0.2.0 — 2026-10-10

Recorded rather than edited away, because the gap is the finding: **this
register sat eighteen days behind a meeting that answered four of its items.**
MD-1's own text instructed that T1-A "be closed with this"; the action was
assigned for Sep 30 and is carried out here on Oct 10.

| item | was | now | by |
|---|---|---|---|
| Tier 1 #2 | open, undirected | **narrowed** to option 5, still open, with the post-narrowing evidence stated | MD-3 |
| Tier 1 #3 | open | **closed** — students drive, named lanes | MD-4 |
| Tier 1 #4a, #4b | absent | **added** — the two ADRs that are now the live gate | MD-2, MD-3 |
| T1-A | brief awaiting a decision | **closed** — supply chain + archives; analysis retained | MD-1 |
| T1-B | brief awaiting a decision | **decided** — P2/P3/P5/P6 provisional, P4/P7 held | MD-2 |
| Tier 2 #5a | open restatement of P2–P5 | **superseded** by MD-2 | MD-2 |
| Tier 2 #5d | open | open, **premise moved** by MD-2 and by the `scitt` topic | — |
| Tier 3 #27 | absent | **added** — the `D-` collision | this revision |
| Tier 4 #22 | "Mario Lim" asserted | **unresolved** — register and MD-6 disagree | this revision |
| Tier 4 #28 | absent | **added** — Tauri, tentative | MD-7 |

**Nothing here accepts a decision.** MD-3 narrowed DEC-002; it did not accept it,
and `CONTRIBUTING` §5 is explicit that only an ADR can. Items 4a and 4b are the
ADRs that would.

---

## What is *not* waiting on you

Decided and merged: DEC-001 (`m-of-n`) · `summary.md` primary, `distilled/` for
FX-1 extraction · stubs allowed · hierarchical `records/<body>/<id>/` ·
version folding · `usefulness` verdicts replacing caps · no record caps ·
NIST summarised not stubbed (L-011) · skills partitioned by what they act on ·
generated nav, index and crosswalk with CI staleness gates · in-scope targets
(MD-1) · lane ownership (MD-4) · survey R-001 Q6–Q9 defaults (MD-5) · project name,
instructor and due date (MD-6).

Students are unblocked: **#13** (David, namespace-governance → option-5 encoder
fixtures), **#14** (Ndewedo, canonical-encoding — **answered**, library#57),
**#23** (David, NIST set). The live student work is now **#73** (single-pass
rejecting decoder) and the D5 fixture package for **Oct 28**.
