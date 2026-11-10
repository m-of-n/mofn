---
schema: "archdoc/v1"
id: APP-0004
title: "The five views — sketches driven by the two scenarios"
short_title: "Five views"
description: "Wireframes of PLAN-0004 §5's five views (Wallet, Domain, Make, Present, Verdict), each drawn for both APP-0002 and APP-0003, with every element bound to the engine output or definition field it shows. Replaces PLAN-0002 §6.5's placeholders."
type: design
category: product
status: draft
version: "0.1.0"
version_policy: "semver; PATCH = editorial; MINOR = element or view added; MAJOR = a view changes"
date: "2026-11-09"
updated: "2026-11-09"
decision_makers: []
reviewers: []
needs_review: true
reviewed: false
canonical_path: project/APP-0004-five-views.md
companion:
  - project/APP-0002-scenario-supply-chain.md
  - project/APP-0003-scenario-archives.md
  - project/PLAN-0004-application-plan.md
  - project/PLAN-0002-product-spec.md
defers_to: ARCH-0001
backlog: W-2
---

# The five views

**Status: draft.** mofn#66 deliverable 3. These are text wireframes, not
visual design. They fix **what each view shows and where each element comes
from**, so the December UI (W-5, mofn#69) builds against them. A paper or
Figma pass may restyle them. It must not add an element that has no source
in the last column of a binding table.

## The rule every view follows

**No view knows a domain.** Each view is drawn twice below, for supply chain
(APP-0002) and archives (APP-0003), and the two drawings differ only in
strings. Every one of those strings comes from the definition (type and value
names, meanings, sentence) or from the relying party's own wallet (labels,
contexts). If building a view needs `if domain == …`, that is a finding
against the vocabulary claim, filed as APP-0003 did. It is not a feature.

Strings marked `«…»` come from the definition and follow the Language menu
(`--lang`). Unmarked text is the UI's own.

## ① Wallet — what I hold

Anchors are drawn apart and marked *unsigned*, because they are local
decisions and not evidence (PLAN-0004 §5).

```
┌─ Wallet ── context [ library ▾ ] ──────────────────── Language [ ES ▾ ] ─┐
│  MY ANCHORS · unsigned, mine, never sent                                  │
│    Reviewer      «Revisión del registro» ∈ «revisado · resumido · sin…»   │
│    ingest agent  «Revisión del registro» ∈ «resumido · sin verificar»     │
│  MY KEYS                                                                  │
│    researcher    person      key:9c1e…   [ Export public key ]            │
│  KEYS I KNOW · not trusted for anything by being here                     │
│    Archivist (definer)  person   key:4fae426a…  from archivist.pub.stmt   │
│    Reviewer             person   key:0176…      from reviewer.pub.stmt    │
│    ingest agent         service  key:4a8e…      from agent.pub.stmt       │
│  VOCABULARIES                                                             │
│    «archives» 1   definition:087bde13…   by Archivist (definer)           │
│  [ Import key… ]  [ Trust a key… ]                                        │
└───────────────────────────────────────────────────────────────────────────┘
```

Supply chain: the same view in context `default`, with one anchor (`release
machine` ∈ «reproducible · attested») and DV-1 in place of «archives».

| element | source |
|---|---|
| context menu | `trusts/<context>.yaml` file names |
| anchors | `root list --context C`; the type and value names from the definition (F-5: the CLI prints the label today) |
| my keys / keys I know | `key list --format json` (`yours`, `kind`, `fingerprint`, `from`) |
| vocabularies | definitions held (`root add` stores them); definer by key label |

## ② Domain — what a statement in this vocabulary can mean

The PICS-like layer: inspectable before anything is signed.

```
┌─ Vocabulary «archives» 1 ── definition:087bde13… ── by Archivist (definer)┐
│  published by its definer ✔  (define statement verified)                  │
│  TYPE  «Record review»   record-review   enum   delegation: scoped        │
│        «How far a library record was checked against its source.»         │
│    reviewed    «Reviewed»     «read against its source and confirmed»     │
│    summarized  «Summarized»   «summarized, but not read against its …»    │
│    unverified  «Unverified»   «not checked against its source»            │
│    review question: «Do the bytes that were read have the digest …?»      │
│  TEMPLATE «Record attestation»  attestation · about a digest · ≤365 days  │
│    «{says} attests that the library record {this} was {record-review}.»   │
│  RENDERINGS   en ✔ all   es ✔ all                                         │
│  [ Show as review YAML ]                    (write half: F-1, not in v0)  │
└───────────────────────────────────────────────────────────────────────────┘
```

Supply chain: DV-1, two types (`build-provenance`, `outcome`), and the
renderings row reads **es ✘ partial** (`attested`, `unverified` and all of `outcome` have no Spanish; APP-0002 gap 1). That
row is how a domain author finds the gap.

| element | source |
|---|---|
| everything | `show X.def` (SPEC-0003 Appendix A review form) |
| "published by its definer" | `check`'s semantics line, `definition.attributed` |
| renderings row | count of language-map keys per string. New, and UI-only: no engine change |

## ③ Make — say one thing, within the vocabulary

The form is generated from the chosen type. It is never hard-coded
(PLAN-0002 §6.5 rule, kept).

```
┌─ Sign ─────────────────────────────────────────────────────────────────────┐
│  Sign as      [ Reviewer ▾ ]          (only keys this wallet owns)         │
│  About        [ record.yaml          ] [Browse]  sha-256:538b22155838b2e4  │
│  Vocabulary   [ «archives» 1 ▾ ]   Claim [ «Record review» ▾ ]             │
│  Value        (•) «Reviewed»    «read against its source and confirmed»    │
│               ( ) «Summarized»  «summarized, but not read against its …»   │
│               ( ) «Unverified»  «not checked against its source»           │
│  Valid for    [ 30 ] days                                                  │
│  Preview  «Reviewer attests that the library record sha-256:538b…         │
│            was read against its source and confirmed.»                     │
│  Runs: mofn make --as Reviewer --subject record.yaml --def archives.def    │
│        --type record-review --value reviewed                               │
│                                                       [ Cancel ] [ Sign ]  │
└────────────────────────────────────────────────────────────────────────────┘
```

Supply chain: «supply-chain» 1, «Build provenance», three values, and the
preview *«release machine attests that sha-256:48dfc395… was built
reproducibly from published sources.»*

| element | source |
|---|---|
| sign as | owned personas (`key list`, `yours: true`) |
| claim / values | the definition's enum types and `values` |
| preview | `render.sentence` over the unsigned statement: what `make` prints after signing |
| Runs line | the argv, as `mofn run` already shows it |
| passphrase | asked by the engine at Sign, never held by the UI (PLAN-0004 §6.2 rule 1) |

## ④ Present — choose what to hand over

```
┌─ Hand over ─── for: record.yaml (sha-256:538b22155838b2e4) ────────────────┐
│  Include                                                                    │
│   [✔] reviewer.stmt          «Reviewer attests that … was read against …»   │
│   [✔] archivist-define.stmt  the vocabulary is the archivist's  (needed ✔)  │
│   [ ] agent.stmt             «ingest agent attests that … was read …»       │
│  The receiver also needs: archives.def, reviewer.pub.stmt                   │
│  Anchors are never included.                                                │
│                                            [ Copy to folder… ] [ Check… ]   │
└─────────────────────────────────────────────────────────────────────────────┘
```

Supply chain: `prov.stmt` and `tv-3-define.stmt`. "needed ✔" marks the
define statement, because semantics fails without it (the wallet README's
*vocabulary unsigned* case).

| element | source |
|---|---|
| candidate statements | statements whose `this` is the chosen subject's digest |
| "needed" | the define statement whose target is the definition the statements name |
| "also needs" | the definition and the speakers' key-publish statements |
| no anchors | SPEC-0004 §4.2 |

v0 keeps no received statements (wallet README § *What the wallet keeps*), so
until ARCH-0003 §3.8 lands, Present lists only the statements you made plus
the files you pick.

## ⑤ Verdict — the product screen

The authorization line is the point. The view is `check --format json`
drawn out. Here it shows the archives fail case in Spanish:

```
┌─ Check ── agent.stmt ── context library ── at 2026-11-09 ── Language [ ES ▾ ]┐
│  «ingest agent atestigua que el registro de la biblioteca                     │
│   sha-256:538b22155838b2e4 fue cotejado con su fuente y confirmado.»          │
│                                                                               │
│  ✔ Integrity       every statement verified; your file is the one described   │
│  ✔ Authenticity    every speaker's key is in your key store                   │
│  ✔ Names           every key is shown by your own label for it                │
│  ✘ AUTHORIZATION   ingest agent is trusted in context library, but not about  │
│                    «revisión del registro» = «revisado»                       │
│  ✔ Acceptance      no template is named                                       │
│  ✔ Semantics       archives 1 is published by its definer, Archivist          │
│                                                                               │
│  Answer: NO. Said, but not by a key with standing to say it.                  │
│  This establishes who said it and whether they were entitled to say it;       │
│  it does not establish that it is true.                                       │
│  [ Why? ]  [ Show anchors used ]                                              │
└───────────────────────────────────────────────────────────────────────────────┘
```

Supply chain fail case (APP-0002), in English: *✘ AUTHORIZATION key holder was
never given the right to say this: no anchor in context default trusts it
about «build provenance».* The rest of the screen is the same.

| element | source |
|---|---|
| sentence | `sentences[]` |
| six lines | `verdict.<line>.result`, `.sentence`. Order fixed by `render.LINES` |
| answer | `answer` |
| limit line | `limit`. Always shown, never hidden behind *Why?* |
| Why? | `because[]`: the anchor used (`path`), or the `stopped` reason code |
| Language | `--lang`. Only «…» strings change; the line frames are the engine's English (F-4) |
| not evaluated | drawn as `–`, never as ✔ (statement-changed golden) |

## Changed from PLAN-0002 §6.5's placeholders

| was | now | why |
|---|---|---|
| four sketches: Verdict, Make, Delegation, Domain browser | PLAN-0004 §5's five: Wallet, Domain, Make, Present, Verdict | §5 is the plan of record; Wallet and Present had no sketch |
| Delegation as a view | folded into Wallet (anchors) and Verdict (*Show anchors used*); a chain view waits for W-3 | v0 has no delegation (mofn#67) |
| `library-review` domain, values `yes · partial · no` | `archives` v1, `reviewed · summarized · unverified` | what the domain file defines |
| "Signed, but NOT by a key with standing" | "Said, but not by a key with standing to say it" | a signature is what passed |
| `– Acceptance not evaluated` beside ✘ Authorization | `✔ Acceptance` | the engine evaluates acceptance even when authorization fails (goldens) |
| "Semantics: value in range" | "published by its definer" | range is authorization's job; semantics is the definition obtained, conforming and attributed (SPEC-0004 §10.4) |
