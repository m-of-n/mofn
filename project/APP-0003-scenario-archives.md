---
schema: "archdoc/v1"
id: APP-0003
title: "Scenario — archives: a library record, and an agent that may summarise but not review"
short_title: "Scenario: archives"
description: "One-page scenario for the contrast PLAN-0004 §3 application: statements about a library record by digest, the fail-authorization case, --lang es. Same engine, different domain file. Drives APP-0004."
type: design
category: product
status: draft
version: "0.2.0"
version_policy: "semver; PATCH = editorial; MINOR = step or case added; MAJOR = a step changes"
date: "2026-11-09"
updated: "2026-11-15"
decision_makers: []
reviewers: []
needs_review: true
reviewed: false
canonical_path: project/APP-0003-scenario-archives.md
companion:
  - project/APP-0002-scenario-supply-chain.md
  - project/APP-0004-five-views.md
  - project/PLAN-0004-application-plan.md
defers_to: ARCH-0001
backlog: W-2
---

# Scenario — archives / library

**Status: draft.** mofn#66 deliverables 1 and 2, for PLAN-0004 §3
(*contrast*). Every step runs in wallet engine 0.7.0. The domain file,
statements and goldens are in `prototype/wallet/domains/archives/`, and
`tests/test_archives.py` runs them under both codecs. It has the same
headings as APP-0002.

**0.2.0 (2026-11-15, W-2b, DL-0046):** one archives vocabulary. The demo
moves from its own `archives` v1 to the published **DV-5 `library-review`
v2**, which took `archives` v1's values, and the relying party now trusts the
library lead, who **delegates** (W-3). Steps 1, 4, 5 and 6 change, and a
delegation step is added. Under the version policy that is MAJOR; it stays
`0.x` because the page is a draft.

**The question the relying party asks:** *has anyone I trust actually checked
this library record against its source, or has it only been summarised?*

**The claim under test:** this runs through **the same `mofn make`,
`mofn delegate` and `mofn check`** as APP-0002 with **no engine code change**,
only a different domain file. Result: **it does.** Neither the v0 commit nor
W-2b touches anything under `engine/` or `cli.py`. `--lang` came in the
commit before v0, as engine work ndewedo-newbury allowed on 2026-11-09
(DL-0033), and it serves both domains alike. What it took to get there is
under § Findings.

## Who

These are roles, not personas, in PLAN-0002 §2.1's sense; see APP-0002 § Who.

| role (issue's "persona") | archetype | persona: key, controller | wallet holds |
|---|---|---|---|
| **domain author** (define) | the vectors' Dave | `Dave (definer)`, person. Example key, seed published in `spec/vectors` | DV-5 and his define statement (TV-38, TV-39) |
| **delegate** | Rosa, the project's librarian, who answers for its reviews | `Library lead`, person | own key; delegates `record-review` for 30 days |
| **issuer** (claim) | Lee, a student who read the source | `Reviewer`, person | own key; signs `record-review = reviewed` |
| a second issuer, **the fail case** | the library's ingestion agent (PROC-0002) | `ingest agent`, service | own key; signs the same `reviewed` |
| **relying party** (rely) | Tomás, a researcher citing the record, who reads Spanish | `researcher`, person | the four public keys, and one anchor |

Authoring the vocabulary and answering for reviews are now **different keys**.
Dave wrote what `reviewed` means; that gives him no say over who may claim it.
Tomás's trust runs to Rosa, not to Dave.

## Setup

- **Vocabulary:** DV-5 `library-review` v2. Type `record-review`, values
  `reviewed · summarized · unverified`, template `record-reviewed` (digest or
  description target). It also carries DV-3's `work`, `title` and `locator`,
  which this scenario does not use. Every name, meaning and sentence of
  `record-review` is in English and Spanish:

  | | en | es |
  |---|---|---|
  | type | Record review | Revisión del registro |
  | `reviewed` | read against its source and confirmed | cotejado con su fuente y confirmado |
  | `summarized` | summarized, but not read against its source | resumido, pero no cotejado con su fuente |
  | `unverified` | not checked against its source | no cotejado con su fuente |
  | sentence | {says} attests that {this} was {record-review}. | {says} atestigua que {this} fue {record-review}. |

- **Subject:** the library record `w3c-prov-dm` (`record.yaml`), named only by
  its SHA-256. It is the record itself, not the W3C document it describes, and
  it is copied and frozen because the live record may change (mofn#34).
- **Tomás's one anchor**, in context `library`: `Library lead` about
  record-review ∈ {reviewed, summarized, unverified}, may delegate one hop.
- **Rosa's delegations**, 30 days each:
  - `Reviewer` about record-review ∈ {reviewed, summarized, unverified}
  - `ingest agent` about record-review ∈ {summarized, unverified}

  The second delegation is the point. The library trusts the agent, but only
  to say what an agent's run can establish.

## Steps

| # | who | does | command |
|---|---|---|---|
| 1 | Dave | DV-5 and his two statements are copied from the vectors | `domains/archives/generate.py` (finding F-1) |
| 2 | Rosa, Lee, agent | each makes a key and hands the public half on | `key gen` |
| 3 | Lee, agent | each signs `reviewed` about the record | `make --subject record.yaml --def library-review.def --type record-review --value reviewed` |
| 4 | Rosa | delegates to each, with a different range, for 30 days | `delegate … --values … --valid-days 30` ×2 |
| 5 | Tomás | knows the four keys | `key import` ×4 |
| 6 | Tomás | anchors Rosa, one hop | `root add "Library lead" … --depth 1 --context library` |
| 7 | Tomás | checks each statement and its delegation against his copy of the record | `check X.stmt lead-X.stmt dave-define.stmt --artifact record.yaml --def library-review.def --context library` |

**Green**, for Lee's statement: all six pass, and the path is shown.

```
authorization  pass           Reviewer is trusted in context library about record review (reviewed, summarized, unverified), through Library lead → Reviewer
semantics      pass           library-review 2 is published by its definer, Dave (definer)

answer: yes

Reviewer attests that sha-256:538b22155838b2e4 was read against its source and confirmed.
```

## The fail-authorization case

The agent's statement says the same as Lee's. It may even be true, since the
agent did fetch the bytes and compare digests. The signature is valid, the
key is known, and the delegation to it is **valid and unexpired**, so this is
a harder case than APP-0002's. The authorization line has to refuse on the
*value*:

```
authorization  fail           ingest agent is trusted in context library, but not about record review = reviewed

answer: no

ingest agent attests that sha-256:538b22155838b2e4 was read against its source and confirmed.
```

That is the project's AI-assisted-design rule (CLAUDE.md, the design log) as
a verdict. An agent may summarise, but only a person's key has standing to say
*reviewed*. If the agent signs `summarized` instead, the same delegation
covers it (golden `agent-summarized.txt`, answer yes, *through Library lead →
ingest agent*).

**After 30 days** Lee's own chain fails too, and names the link. Short expiry
is the revocation mechanism (W-3):

```
authorization  fail           the delegation Library lead → Reviewer is broken: the delegation has expired (not-valid-at-time)
```

## In Spanish

`mofn --lang es check agent.stmt lead-agent.stmt …` (golden
`agent-not-entitled-es.txt`):

```
authorization  fail           ingest agent is trusted in context library, but not about revisión del registro = revisado

ingest agent atestigua que sha-256:538b22155838b2e4 fue cotejado con su fuente y confirmado.
```

The answer and exit code do not change.

## Findings against the vocabulary claim

None of these needed type-specific engine code. They are what *only a
different domain file* cost:

- **F-1. The domain author has no command.** `mofn` cannot publish a
  definition or sign a `define`. The archives files come from a script that
  calls the engine's existing encoder and signer. A `mofn define` belongs to
  the engine owner (#65 successor), and it is the Domain view's write half
  (APP-0004 ②).
- **F-2. `--artifact` names the subject.** For a record, the flag's name is
  wrong in two ways. It is domain-flavoured, and "artifact" is a normative
  term here (`ArtifactId`, R-M-07). `--subject`, which `make` already uses,
  would serve both domains. This is a rename and changes no behaviour.
- **F-3. "no template is named".** `make` names no template, so acceptance
  passes vacuously in both domains, while the sentence still comes from the
  template. Pre-existing (SPEC-0004 Appendix A, DL-0020 A1), and not
  archives-specific.
- **F-4. Two languages in one verdict.** `--lang` translates the vocabulary,
  not the engine's frames, so the same as APP-0002 gap 2.
- **F-5. `root add` / `root list` print the type's label (`record-review`),
  not its name**, and ignore `--lang`. Cosmetic.
- **F-6. A value outside a delegated range does not name the hop.** The
  agent's fail line says *trusted … but not about record review = reviewed*.
  It does not say that the range came from *Library lead → ingest agent*,
  as the expired case names its link. Found in W-2b; an engine wording for
  the owner of `check.py`, not archives-specific.

## One archives vocabulary

Until 0.2.0 this page ran its own `archives` v1 beside the published DV-3
`library-review` v1, and the two named the same idea differently. As decided
on 2026-11-09 (DL-0033), they converged when W-3 merged: **DV-5
`library-review` v2** has `archives` v1's values (ndewedo-newbury,
2026-11-15) and DV-3's other types. DV-3 stays published for its vectors.
`ARCH-0001` §2.3.2 still cites DV-3; moving AR-1…AR-3 to DV-5 is an ARCH
proposal of its own. The record is `design-log/0046-archives-converge/`.

## Run it

`prototype/wallet/domains/archives/README.md` § *Run it*, or
`.venv/bin/pytest tests/test_archives.py`.
