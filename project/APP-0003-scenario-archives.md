---
schema: "archdoc/v1"
id: APP-0003
title: "Scenario — archives: a library record, and an agent that may summarise but not review"
short_title: "Scenario: archives"
description: "One-page scenario for the contrast PLAN-0004 §3 application: statements about a library record by digest, the fail-authorization case, --lang es. Same engine, different domain file. Drives APP-0004."
type: design
category: product
status: draft
version: "0.1.0"
version_policy: "semver; PATCH = editorial; MINOR = step or case added; MAJOR = a step changes"
date: "2026-11-09"
updated: "2026-11-09"
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
(*contrast*). Every step runs in wallet engine 0.4.0. The domain file,
statements and goldens are in `prototype/wallet/domains/archives/`, and
`tests/test_archives.py` runs them under both codecs. It has the same
headings as APP-0002.

**The question the relying party asks:** *has anyone I trust actually checked
this library record against its source, or has it only been summarised?*

**The claim under test:** this runs through **the same `mofn make` and
`mofn check`** as APP-0002 with **no engine code change**, only a different
domain file. Result: **it does.** The commit that adds the domain touches
nothing under `engine/` or `cli.py`. `--lang` came in the commit before it,
as engine work ndewedo-newbury allowed on 2026-11-09 (DL-0033), and it serves both domains
alike. What it took to get there is under § Findings.

## Who

These are roles, not personas, in PLAN-0002 §2.1's sense; see APP-0002 § Who.

| role (issue's "persona") | archetype | persona: key, controller | wallet holds |
|---|---|---|---|
| **domain author** (define) | Rosa, the project's librarian | `Archivist (definer)`, person. Example key, published seed | `archives.def` and her define statement |
| **issuer** (claim) | Lee, a student who read the source | `Reviewer`, person | own key; signs `record-review = reviewed` |
| a second issuer, **the fail case** | the library's ingestion agent (PROC-0002) | `ingest agent`, service | own key; signs the same `reviewed` |
| **relying party** (rely) | Tomás, a researcher citing the record, who reads Spanish | `researcher`, person | the three public keys, and Tomás's own anchors |

## Setup

- **Vocabulary:** `archives` v1. Type `record-review`, values
  `reviewed · summarized · unverified`, template `record-attestation`. Every
  name, meaning and sentence is in English and Spanish:

  | | en | es |
  |---|---|---|
  | type | Record review | Revisión del registro |
  | `reviewed` | read against its source and confirmed | cotejado con su fuente y confirmado |
  | `summarized` | summarized, but not read against its source | resumido, pero no cotejado con su fuente |
  | `unverified` | not checked against its source | no cotejado con su fuente |
  | sentence | {says} attests that the library record {this} was {record-review}. | {says} atestigua que el registro de la biblioteca {this} fue {record-review}. |

- **Subject:** the library record `w3c-prov-dm` (`record.yaml`), named only by
  its SHA-256. It is the record itself, not the W3C document it describes, and
  it is copied and frozen because the live record may change (mofn#34).
- **Tomás's anchors**, in context `library`:
  - `Reviewer` about record-review ∈ {reviewed, summarized, unverified}
  - `ingest agent` about record-review ∈ {summarized, unverified}

  The second anchor is the point. Tomás trusts the agent, but only to say
  what an agent's run can establish.

## Steps

| # | who | does | command |
|---|---|---|---|
| 1 | Rosa | publishes `archives.def` and her define statement | `domains/archives/generate.py` (finding F-1) |
| 2 | Lee, agent | each makes a key and hands Tomás the public half | `key gen` |
| 3 | Lee, agent | each signs `reviewed` about the record | `make --subject record.yaml --def archives.def --type record-review --value reviewed` |
| 4 | Tomás | knows the three keys | `key import` ×3 |
| 5 | Tomás | anchors each, with a different range | `root add … --context library --values …` ×2 |
| 6 | Tomás | checks each statement against his copy of the record | `check X.stmt archivist-define.stmt --artifact record.yaml --def archives.def --context library` |

**Green**, for Lee's statement: all six pass.

> Reviewer attests that the library record sha-256:538b22155838b2e4 was read against its source and confirmed.

## The fail-authorization case

The agent's statement says the same as Lee's. It may even be true, since the
agent did fetch the bytes and compare digests. The signature is valid, the
key is known, and the key is **anchored**, so this is a harder case than
APP-0002's. The authorization line now has to refuse on the *value*:

```
authorization  fail           ingest agent is trusted in context library, but not about record review = reviewed

answer: no

ingest agent attests that the library record sha-256:538b22155838b2e4 was read against its source and confirmed.
```

That is the project's AI-assisted-design rule (CLAUDE.md, the design log) as
a verdict. An agent may summarise, but only a person's key has standing to say
*reviewed*. If the agent signs `summarized` instead, the same anchor covers it.

## In Spanish

`mofn --lang es check agent.stmt …` (golden `agent-not-entitled-es.txt`):

```
authorization  fail           ingest agent is trusted in context library, but not about revisión del registro = revisado

ingest agent atestigua que el registro de la biblioteca sha-256:538b22155838b2e4 fue cotejado con su fuente y confirmado.
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

## Two archives vocabularies, pending reconciliation

mofn#152 (open, T-012b) adds **DV-3 `library-review`** to the published
vectors for ARCH-0001 §2.3.2. Its type is `reviewed: yes · partial · no`. It
also has `title`, `work` and `locator`, a description target, and a
delegation path (Carol → Dave → Bob). This page's `archives` v1 is what
mofn#66 specified (`record-review: reviewed · summarized · unverified`), and
it runs in engine v0, which has no delegation. They do different jobs: DV-3
is the protocol's interoperability vector, and `archives` is the domain file
the wallet demo runs today. The two are not reconciled, and both name the
same idea differently.

**Recommendation:** once #152 merges, keep DV-3 as the vector and keep
`archives` as the demo domain until W-3 (mofn#67) can run DV-3's delegation
path. Then decide whether the demo switches to DV-3. Owner: @nymble (the
issue owner), with the #152 author.

## Run it

`prototype/wallet/domains/archives/README.md` § *Run it*, or
`.venv/bin/pytest tests/test_archives.py`.
