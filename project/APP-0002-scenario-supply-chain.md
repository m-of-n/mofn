---
schema: "archdoc/v1"
id: APP-0002
title: "Scenario — supply chain: a release file, and a key with no standing"
short_title: "Scenario: supply chain"
description: "One-page scenario for the primary PLAN-0004 §3 application, with the define, claim and rely roles and the fail-authorization case, as wallet engine 0.4.0 runs it today. Drives APP-0004."
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
canonical_path: project/APP-0002-scenario-supply-chain.md
companion:
  - project/APP-0003-scenario-archives.md
  - project/APP-0004-five-views.md
  - project/PLAN-0004-application-plan.md
defers_to: ARCH-0001
backlog: W-2
---

# Scenario — supply chain

**Status: draft.** mofn#66 deliverable 1, for PLAN-0004 §3 (*primary*). Every
step below runs in wallet engine 0.4.0 (`prototype/wallet`), and every verdict
quoted is a pinned golden (`prototype/wallet/fixtures/golden/`). Its twin is
APP-0003. The two pages have the same headings on purpose, so a reader can
check that only the vocabulary differs.

**The question the relying party asks:** *was this release file built the way
someone I trust says it was?*

## Who

The issue calls these "three personas". PLAN-0002 §2.1 (2026-10-14) calls
them **roles**, the thing a key does in one statement. A **persona** is the
key-identified principal that plays a role, and an **archetype** is the
person behind it. These are the archetypes for this scenario, a proposal
toward PLAN-0002 GAP-1:

| role (issue's "persona") | archetype | persona: key, controller | wallet holds |
|---|---|---|---|
| **domain author** (define) | Alice, on a supply-chain standards group | `Alice (definer)`, person. Published key TV-1 | `dv-1.def` and her define statement TV-3, both public |
| **issuer** (claim) | the project's CI | `release machine`, service | its own key; signs `build-provenance = reproducible` about `release.bin` |
| a second issuer, **the fail case** | Maya, a release engineer, signing from her laptop | `key holder`, person | her own key; signs the same claim about the same file |
| **relying party** (rely) | Sam, who packages the release for a distribution | `me`, person | the two public keys, Alice's key, and Sam's own anchors |

## Setup

- **Vocabulary:** `supply-chain` v1 (DV-1). Type `build-provenance`, values
  `reproducible · attested · unverified`, template `release-attestation`.
  Its sentence reads *"{says} attests that {this} was {build-provenance}."*
  It is in English and Spanish, except that `attested` and `unverified` have
  no Spanish and fall back to English (§ Gaps).
- **Subject:** a file, named only by its SHA-256 (R-M-07).
- **Sam's anchor:** *in context `default`, I trust `release machine` to say
  build-provenance is reproducible or attested, about any file.* It is unsigned
  and local (`mofn root add`).

## Steps

| # | who | does | command |
|---|---|---|---|
| 1 | Alice | publishes DV-1 and the define statement that says it is hers | (vector TV-3; mofn has no `define` command, see APP-0003 F-1) |
| 2 | CI | makes its key and hands Sam `build.pub.stmt` | `key gen build --controller service` |
| 3 | CI | signs the claim about the file | `make --subject release.bin --type build-provenance --value reproducible` |
| 4 | Sam | knows the keys without trusting them | `key import` ×3 |
| 5 | Sam | decides whom to trust, about what | `root add "release machine" --values reproducible,attested` |
| 6 | Sam | checks what he was handed, against his own copy of the file | `check prov.stmt tv-3-define.stmt --artifact release.bin --def dv-1.def` |

**Green.** All six lines pass. Sam reads:

> release machine attests that sha-256:48dfc39586b0c4f9 was built reproducibly from published sources.

## The fail-authorization case

Maya signs **the same claim about the same file**. It may well be true, since
she ran the same reproducible build. The signature is valid and Sam holds her
key. Sam never anchored her for `build-provenance`. Excerpt of golden `unauthorized.txt`, as `demo/slice.sh` case ②′ labels it:

```
integrity      pass           every statement verified, and your file is the one described
authenticity   pass           every speaker's key is in your key store, and each envelope agrees with its statement
authorization  fail           key holder was never given the right to say this: no anchor in context default trusts it about build provenance

answer: no

key holder attests that sha-256:48dfc39586b0c4f9 was built reproducibly from published sources.
```

This is the CS Night moment (PLAN-0004 §3). The sentence is printed, because it
is what was said, and the answer is still **no**, because saying it is not
standing to say it. The limit line closes every result: *who said it and
whether they were entitled to, not that it is true.*

Other cases on the same run, all pinned: key never received → authenticity
fail; file changed → integrity fail; statement changed → integrity fail, exit 3;
vocabulary unsigned → semantics fail; checked after `valid` ends →
authorization fail (`not-valid-at-time`).

## In Spanish

`mofn --lang es check …` prints the vocabulary's words in Spanish:
*"release machine atestigua que sha-256:48dfc39586b0c4f9 fue compilado de
forma reproducible desde fuentes publicadas."* The six verdict lines keep
the engine's English frames (§ Gaps).

## Not in v0

- **Delegation.** PLAN-0002 §2.2's version, where Paul delegates to David and
  a CI key is missing a link, needs W-3 (mofn#67). Until then, Sam's anchor
  names the CI key directly. The fail case does not change: there is no path
  from Sam to Maya.
- **Review and approval** (`outcome`, kind `review`) are in DV-1 but not
  evaluated.

## Gaps this scenario exposes

1. DV-1 is missing Spanish for two values. Its bytes are hashed into the
   published vectors, so adding Spanish means a new definition version. For
   the vector owners.
2. With `--lang`, the verdict is in two languages: the engine's frames are
   English. Translating the engine's own words is not in W-2.

## Run it

`demo/slice.sh` (both codecs, against the goldens), or the walkthrough in
`prototype/wallet/README.md` § *Try it*.
