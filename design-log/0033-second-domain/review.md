---
schema: "design-log/v1"
id: DL-0033
part: review
date: "2026-11-09"
---

# DL-0033 — review

**Human verdict:** pending (PR review). The issue owner, @nymble, has not yet
confirmed the `--lang` decision.

## What the human decided

- **`--lang` is allowed engine work** under W-2's "zero engine code changes"
  (ndewedo-newbury, 2026-11-09). The agent kept it to one commit, separate
  from the domain, so the acceptance test stays checkable: the domain commit
  touches no engine file.

## What the human corrected

- **The agent recorded the `--lang` decision as the sponsor's.** It wrote
  "Sponsor decision" in the first commit message and "the sponsor allowed" in
  APP-0003 and the domain README, and it was wrong. The person deciding was
  the user in the session, who is not the issue owner. The agent caught this
  before pushing, reworded the commit and fixed both files. It is recorded
  because it is exactly the error the design log exists to catch:
  attribution of a decision, made up from context.

## What the agent rejected, and why

- **Adding the archives definition to `spec/vectors/ksa-core` as DV-3.**
  The agent had proposed this in its first answer. It rejected it on
  reading the vectors README ("the interoperability contract"). An
  application vocabulary is not protocol, and adding it would have reopened
  SPEC-0003 Appendix A for a domain file. Cost: `domains/archives/` is not
  covered by `fixtures/sync.py`'s "copies of published vectors" rule, and
  has its own `--check` instead.
- **Generating the domain files with `cbor2` and `cryptography`,
  independently of the engine,** as `generate.py` in the vectors does. That
  would add two dependencies to the wallet's venv. The engine's encoder is
  already checked against the published vectors, and a domain author with a
  real `mofn define` would use the engine anyway. Cost: the engine writes
  bytes it later reads, so an encoder bug that is symmetric would not show
  here. The vectors would catch it.
- **Reading `record.yaml` live from the `library/` submodule.** Its digest
  is in the goldens, and the live record changes (mofn#34). The copy is
  frozen and its source commit recorded.
- **`reviewed` meaning "read against its source by a person".** This was the
  first draft. It would make the agent's statement false, and the issue asks
  for a *true* statement the key is not entitled to make. Changed to "read
  against its source and confirmed". Who may say it is now the anchor's job,
  not the meaning's.
- **An unanchored key as the archives fail case.** That would repeat
  APP-0002. An agent that is anchored but limited to `summarized ·
  unverified` tests the range, which APP-0002 does not.
- **Translating the engine's own words under `--lang`.** That is not what
  was asked ("which language it wants to use" for the vocabulary), and it
  would mean a message catalogue in the engine. Recorded as F-4 and
  APP-0002 gap 2.
- **Accepting `--lang ES` and folding the case.** SPEC-0003 keys language
  maps in canonical case, and the definitions are checked with the same
  pattern. One rule, refused clearly (exit 2), seemed better than two.
- **Naming the archetypes after the team** (PLAN-0002 §2.2 used Paul,
  David, Ndewedo). PLAN-0002 §2.1 separates role, persona and archetype, and
  real names blur them. The archetypes are invented.
- **A Delegation view as a sixth view.** PLAN-0002 §6.5 had one. PLAN-0004
  §5 does not, and v0 has no delegation, so it is folded into Wallet and
  Verdict until W-3.
- **Paper or Figma.** The issue allows either. The agent produced text
  wireframes bound to sources, which a human can restyle, and did not claim
  to have produced visual design.

## Found, not fixed

- **A second archives vocabulary is in flight.** mofn#152 (opened the same
  evening, T-012b) adds DV-3 `library-review` (`reviewed: yes · partial ·
  no`) to the vectors. The agent found it only at the design-log number
  check: #152 holds `DL-0032`, so this entry took `0033`. It did not
  switch to DV-3, for three reasons. #66 names `record-review: reviewed ·
  summarized · unverified`. DV-3's scenario needs delegation, which engine v0
  lacks. And #152 is unmerged. APP-0003 § *Two archives vocabularies* records
  the recommendation. The agent should have looked at open PRs before
  designing the vocabulary, not after.

- **F-1** `mofn` has no `define` command, so the domain author role has no
  CLI verb. Engine owner (#65 successor).
- **F-2** `check --artifact` should be `--subject`, as in `make`:
  "artifact" is normative here, and the subject may be a record.
- **F-3** `make` names no template, so acceptance passes vacuously in both
  domains (pre-existing, DL-0020 A1).
- **F-5** `root add` / `root list` print the type label, not its name, and
  ignore `--lang`.
- **DV-1 lacks Spanish** for `attested`, `unverified` and `outcome`. Its
  bytes are in the vectors, so a fix is a new version, for the vector owners.
- **APP-0001 still does not name the two applications** (PLAN-0004 §8
  fix 2). PLAN-0004 §7's Oct 14 row lists that as "done when". Not touched
  here.
