---
schema: "design-log/v1"
id: DL-0006
part: review
date: "2026-10-08"
---

# DL-0006 — review

## Rejected — claims already in the repository, overturned by reading the rest of the source

Both had been written into the topic answer by the session DL-0004 records, and
both were in **our** favour, which is why they survived.

1. **"DSSE's `(t, n)` multi-signature envelope already carries threshold
   semantics, so R-I-03's export target makes R-M-06 cheaper than anyone
   assumed."** Committed to `topics/canonical-encoding.yaml` and to the DSSE
   `summary.md` on 2026-10-03, and then **propagated** into
   `records/ietf/rfc-9804/distilled/design-notes.md` on 2026-10-04, where the
   R-I-03 row relied on it. **Withdrawn.** The sentence continues *"where `t` is
   application-specific"*: `t` is a verifier-side parameter supplied out of
   band, not an envelope field. `envelope.md` then settles it — multiple
   signatures are *"equivalent to separate envelopes with individual
   signatures"*. A DSSE envelope carries `n` and cannot carry `k`.

   *This is the one worth dwelling on. The refutation was not in an unread
   document — it was in the second half of the sentence the answer had already
   quoted.* The quotation stopped at the clause that supported the claim. No
   amount of further reading elsewhere would have caught it; only re-reading the
   cited line to its end did. For a project whose threshold semantics are the
   whole point, a truncated quotation produced a confident, wrong, and
   *favourable* conclusion that then spread to a second record.

   Consequence beyond the retraction: because `envelope.md` declares a
   multi-signature envelope *equivalent* to separate envelopes, an intermediary
   may legitimately split or merge them, so any threshold meaning inferred from
   signature count is not merely absent but **unsafe to infer**.

2. **"Option 3's named envelope reintroduces a global type identifier, which
   R-M-12 excludes."** Recorded as the fourth of four grounds for withdrawing
   DEC-002 option 3. **Weakened, not false.** `payloadType` is only *recommended*
   to be a media type or URI — a **SHOULD** in `protocol.md` — and
   `envelope.md` §Other data structures explicitly licenses coding it *"as a
   shorter string or enum"*, which PAE authenticates just as well. DSSE does not
   **force** a centrally allocated identifier; its default recommends one.

   *Two failures compounded: a SHOULD read as a requirement, and a conclusion
   about an envelope drawn without reading the document that defines the
   envelope.* The ground survives as the weakest of the four. The first three —
   condition (5) prohibited rather than absent, §5's mandated ordering, and the
   number algorithm being outside the cited document — stand untouched.

## Rejected — this session's own plans, before they were executed

3. **"Promoting DSSE to `distilled` will trigger FX-1 full extraction."**
   Assumed while planning, and it would have made item 3 of the audit far more
   expensive than it was. **Rejected by reading `bin/check-pr-extraction`
   instead of guessing:** `IN_SCOPE = {"rfc", "draft", "spec", "ietf"}` is keyed
   on record **type**, and DSSE is type `repo`. `bin/validate` asks only for one
   artifact plus a `README.md` indexing them. The promotion was cheap, and the
   `distilled/README.md` now says out loud that FX-1 does not apply and why,
   rather than leaving a reader to infer it from a missing `distillation` block.

4. **"`w3c-rdf-canon-1-0` is an out-of-scope comparator — document it and move
   on."** This was the plan presented to the human and the human approved it.
   **Overturned by reading the record's own `usefulness.reason` before acting on
   it.** RDFC-1.0 canonicalises **RDF datasets**, which are unordered *sets* of
   triples — so it is a ratified algorithm for canonically ordering a set,
   including the hard blank-node case, which is precisely **condition (5)**, the
   gap the answer says no candidate supplies.

   *The first plan would have buried the one document in the library bearing on
   the gap the answer names.* It remains correct that RDFC-1.0 cannot be a
   DEC-002 candidate — it canonicalises graphs, not our tree-shaped statements —
   so it stays unowned and unread. But the answer now scopes its claim ("no
   **candidate** supplies condition (5)", not "no prior art exists") and
   **library#56** owns the follow-up. The plan was approved as written and was
   still wrong; executing it unchanged would have been the easier path.

5. **"Add an `implementations:` block to `rfc-8785` so the library-availability
   axis is measured rather than cited."** Tempting, because `rfc-8949` has a
   twelve-entry block and the asymmetry is exactly what the axis is about.
   **Rejected:** the current maintenance state, versions and audit history of
   those five libraries cannot be established from the pinned source, and
   asserting them from memory would have manufactured the very unmeasured claim
   the axis exists to expose. The answer instead cites Appendix G, states that
   four of the five implementations live in one author's repository, and says
   plainly that *on this axis we are citing the source rather than measuring*.

6. **Routing `yaml-1-2-2` and `strictyaml-why` by their `bears_on`.** Both carry
   `bears_on: DEC-002`, which would have kept them in `canonical-encoding` and
   left the topic uncloseable. **Rejected in favour of their
   `usefulness.reason`**, which says what they are actually for — *"the YAML spec
   our authored sources are written in"* and the Norway problem. YAML is not a
   DEC-002 candidate; the four options are canonical S-expressions, CBOR, JSON
   with JCS, and a dual form. They bear on DEC-002 **by analogy**, and an analogy
   is not evidence for an encoding decision. Moved to `library-construction`,
   with that reasoning written into the topic rather than into a commit message.

7. **Writing a `distilled/requirements.yaml` for DSSE.** Rejected. It would have
   invited `bin/validate`'s BCP 14 reconciliation gate on a document that
   declares no BCP 14 boilerplate at all, and would have claimed an FX-1
   artifact for a record explicitly exempt from FX-1. `normative.md` carries the
   keyword-bearing statements with locators and no counting apparatus.

8. **Amending ARCH-0002 P5, and writing the `rcbor` decode path.** Both are
   where the evidence points, and both are forbidden by #14's own *"No
   architecture document. No implementation code."* Handed off to **#72** and **#73**. The
   library PR says so, rather than leaving the omission to look like an
   oversight.

## Rejected — the instructions themselves

9. **The submodule's `library/CLAUDE.md`.** It had diverged from the standalone
   clone's copy: the **"Extracting, not touching"** amendment of 2026-10-03 was
   absent, and the FX-1 gate read *"a PR moves past stub"* rather than *"a PR
   extracts"*. Under the submodule's wording, promoting DSSE would have looked
   like it demanded full FX-1. The standalone clone's copy was used, and it
   agrees with `bin/check-pr-extraction`, which is the thing CI actually runs.
   *Two copies of the rules disagreeing, with the stale one sitting in the path
   an agent reaches first, is a live hazard rather than a tidiness problem.*

## Accepted by the human

The audit was delivered as five numbered gaps with a recommendation on each, and
the human approved all five in one instruction — *"execute with your
recommendations"* — including the recommendation that the finding be **drafted
but not posted** to #8, since #8 is assigned to others. That draft is in the
library PR thread and on #8 only when a human sends it.

**No human has reviewed the content.** `reviewed_by` is empty on every artifact
in `secure-systems-lab-dsse/distilled/`, as it is on `rfc-9804`'s and
`rfc-8785`'s. Under `docs/extraction.md` pass 4 these are readable but not
buildable-on until someone signs them. Recorded here so that the next reader of
this entry does not mistake "`status: answered`" for "reviewed".

## Retracted — a "finding" that was a stale checkout

11. **"`bin/manifest` silently drops the library Bibliography from nav."**
    Written into this entry and into the PR body as a hazard discovered while
    regenerating, with `bin/manifest:92` cited. **Retracted.** The bug was real
    and is **already fixed on `main`** — `f86d6a2`, *"fix: the nav generator's
    output depended on local state, and dropped the bibliography"* (#55,
    2026-10-01), which replaced the test on the generated
    `library/index/bibliography.md` with a test on the **generator**
    (`library/bin/reindex`), and #62 then added a CI check that fails when the
    tracked nav or `PUBLISHING.md` differs from what the generators produce.

    **The cause was mine.** This branch was created from a local `main` at
    `46634c0`, which is a genuine ancestor of `origin/main` but sits **22 commits
    behind it** and predates the fix. `git fetch` was never run before branching.
    So the generator was observed misbehaving in a checkout where it had not yet
    been repaired, and the observation was written up as a discovery.

    *The tell was in the evidence and was misread.* The entry cited, as
    corroboration, a committed chore on the unmerged `design-log-0004` branch
    titled *"and the library bibliography drops out"* — treating a second
    occurrence as confirmation that the bug was live. It was the opposite: that
    branch is **also** stale, and two stale branches agreeing is the same
    non-evidence as two agents agreeing, which `DL-0003` §review already records
    as a lesson. A fixed bug reported as live costs a reviewer the time to
    rediscover the fix.

    Three further consequences of the same stale base, all found only when the
    PR was pushed: the **DL numbering was wrong** (see `question.md`), the PR
    **conflicted** with `main` in `mkdocs.nav.yml` and `project/PUBLISHING.md`,
    and the entry **duplicated** a finding the human it was being written for had
    fixed himself a week earlier.

    **Rule taken from it:** branch from `origin/main` after a fetch, not from
    whatever `main` points at locally — and before reporting a defect in a
    generator, check whether the checkout is current. Neither the library work
    nor any finding in `produced.md` is affected: that work was done in the
    **standalone library clone**, which was current, and `bin/lib-sync --check`
    passes on the rebased branch.

## Not rejected, but flagged

**Nothing.** The `DL-0004` collision this entry previously flagged was an
artifact of the stale base and is resolved above.
