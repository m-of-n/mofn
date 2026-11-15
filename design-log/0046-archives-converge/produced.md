---
schema: "design-log/v1"
id: DL-0046
part: produced
date: "2026-11-15"
---

# DL-0046 — produced

No primitive. TV-38…44 are signed with `cryptography` through the existing
`spec/vectors/ksa-core/generate.py`. Nothing under `engine/` or `cli.py`
changed.

| file | change |
|---|---|
| `spec/vectors/ksa-core/generate.py`, `vectors.json`, `vectors.md` | **DV-5** `library-review` v2, definer Dave. Type `record-review` (`reviewed · summarized · unverified`, en + es, delegation scoped, review question `source`), plus DV-3's `title`, `work` and `locator`. Template `record-reviewed`: digest or description target, `record-review` required, `locator` optional, ≤ 365 days, sentence *{says} attests that {this} was {record-review}.* **TV-38** Dave's key-publish; **TV-39** define DV-5; **TV-40** Carol trusts Dave, depth 1; **TV-41** Dave → Bob ∈ {summarized, unverified}; **TV-42** Bob says `reviewed` (outside scope); **TV-43** Bob says `summarized`; **TV-44** Dave, description target. **E-20** yes, **E-21** no / `no-path` at TV-42, **E-22** yes. `vectors.json` diff has no removed line: every existing vector is byte-identical |
| `spec/SPEC-0002-ksa-core.md` | 0.10.0: Appendix A re-spliced from `vectors.md`; changelog line |
| `spec/vectors/ksa-core/README.md` | § Archives target: v2 paragraph |
| `prototype/wallet/tests/test_delegation.py` | `subject()` maps `work-v2` to TV-44, so E-20…E-22 run through `engine/reduce.py` with E-1…E-7 |
| `prototype/wallet/domains/archives/` | `archives.def` and the archivist's statements **removed**. `generate.py` now copies DV-5, TV-38 and TV-39 out of `vectors.json`, as `fixtures/sync.py` does, into `library-review.def`, `dave.pub.stmt[.yaml]`, `dave-define.stmt[.yaml]`. README rewritten |
| `prototype/wallet/tests/test_archives.py` | The relying party anchors **Library lead**, depth 1. The lead delegates `Reviewer` for all values and `ingest agent` for {summarized, unverified}, 30 days. Five goldens: `reviewed` (yes, path shown), `agent-not-entitled` (+`-es`), `agent-summarized` (yes), `reviewer-expired` (31 days on: the link is named) |
| `project/APP-0003-scenario-archives.md` | 0.2.0: § Who (definer and lead are now different keys), § Setup, § Steps (7 steps, a delegate step), the fail case, the expiry case, Spanish; § *Two archives vocabularies* is replaced by § *One archives vocabulary*; finding F-6 |
| `project/APP-0004-five-views.md` | 0.1.1: a note that the archives wireframes show v1 names until the I5 redraw |
| `project/BACKLOG-0001.md` | 0.14.1: W-2b → review |

Results: wallet `pytest` 435 passed; `demo/slice.sh` green; `generate.py --check` clean.

## Choices the human has not seen

- **DV-5 is a new definition, not an edit of DV-3.** DV-3 and TV-21…26 stay,
  as do E-5…E-7 and ARCH-0001 §2.3.2's citations of them.
- **Type label `record-review`, not `reviewed`.** With the demo's values, a
  type called `reviewed` would have a value called `reviewed`.
- **Definition name kept as `library-review`, version `2`**, as DL-0033
  proposed, so that v2 is visibly the successor of DV-3.
- **The sentence drops "the library record".** The template now also takes a
  description target, and *"the library record a described object"* reads
  wrong.
- **Dave is the definer, and a new live persona, the library lead, delegates.**
  The vectors publish Dave's seed, and `mofn` has no way to import a private
  key, so a live wallet cannot sign as Dave. Splitting the definer from the
  delegator is also the stronger demo: writing a vocabulary gives no standing
  to claim within it.
- **Numbers TV-38…44, E-20…22, DL-0046.** TV-36, TV-37, E-11…E-19 and
  DL-0041…0045 are taken by open PRs (#166, #167, #169, #170).
