---
schema: "archdoc/v1"
id: SPEC-0003
title: "KSA Definitions — vocabularies, types, human-readable semantics, constraints and templates"
short_title: "KSA Definitions"
description: "How a key publishes what statements mean: hash-identified definitions carrying types with mandatory human-readable semantics, a fixed set of base value kinds with range algebra, declarative constraints that explain themselves, templates for issuing statements, and the rendering of a statement into a sentence."
type: specification
category: security
status: draft
version: "0.1.0"
version_policy: "semver; MAJOR = any change to hashed bytes or evaluation results; MINOR = additive registry entries; PATCH = editorial"
date: "2026-10-14"
updated: "2026-10-14"
decision_makers:
  - role: sponsor
    id: paul-lambert
reviewers: []
needs_review: true
reviewed: false
canonical_path: spec/SPEC-0003-ksa-definitions.md
companion:
  - spec/SPEC-0002-ksa-core.md
  - spec/SPEC-0005-ksa-processes.md
  - spec/ARCH-0002-key-relative-naming.md
defers_to: ARCH-0001
related_rfcs: [RFC5646, RFC5890, RFC5952, RFC8949]
---

# KSA Definitions — vocabularies, types, human-readable semantics, constraints and templates

**Specification SPEC-0003 · version 0.1.0 · draft**

## Abstract

A KSA statement assigns typed values to a target. This document specifies where
those types come from: **definitions**, published by keys and identified by the
hash of their canonical encoding. A definition carries, for every type, value,
field and constraint, the **words a person reads** — in more than one language —
together with the machine rules a verifier applies. It specifies a fixed set of
base value kinds with exact assignment, range, membership and subset rules; a
small declarative constraint language whose every rule carries its own
explanation; templates from which statements are issued; and how a statement is
rendered as a sentence. Process definitions are specified in SPEC-0005.

## Status of this document

Draft for review in the m-of-n project. Realises ARCH-0002 P1 (accepted), P3 and
P4, and ARCH-0003 §3.5–§3.6, under ADR-0003 D1 and D2.

---

## 1. Introduction

PICS (W3C, 1996) published *rating systems* — categories, permitted values and
the words a person reads — as documents separate from the labels that cited
them, so that software meeting an unfamiliar vocabulary could fetch its
description and render it correctly. That separation is the idea KSA keeps.
Three things are added:

1. **Identity by hash.** A definition is identified by the SHA-256 of its
   canonical encoding, never by a URL. A locator is only a place to fetch it;
   what is fetched is checked against the hash.
2. **Authorship by signature.** A definition is published by a signed `define`
   statement from its definer (SPEC-0002 §8.9), so whether to rely on a
   vocabulary is a trust question like any other.
3. **Machine rules beside the words.** Every type has a base kind with exact
   range algebra, and constraints are declarative, so a verifier needs no
   definition-specific code — and a definition can never ship code.

The human-readable semantics are **mandatory**. A definition whose types, values,
fields, constraints or templates lack names and descriptions does not conform
(§9).

## 2. Conventions and terminology

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when,
and only when, they appear in all capitals, as shown here.

Terms from SPEC-0002 §2 apply. In addition:

| term | meaning |
|---|---|
| **definition body** | the map of §4 that is hashed and published |
| **definer** | the key whose kid is in the body, and which signs the `define` statement |
| **entry** | one item in a definition: a type, template, panel or process |
| **base kind** | one of the fixed value kinds of §6, each with its own range algebra |
| **assignment** | a single value of a type |
| **range** | a set of values of a type, used to scope trust and delegation |
| **language map** | a map from language tags to text (§5.3) |
| **label** | a name local to a definition: `[a-z][a-z0-9-]{0,62}` |

## 3. Overview

```
 definition body (KSA-CBOR) ──SHA-256──▶ DefinitionId ◀── cited by every type-ref
        │
        ├── type   "build-provenance"  base: enum   names/short/long, values (each named and explained), constraints, review questions
        ├── type   "outcome"           base: enum
        ├── template "release-attestation"  function, target rules, attributes, max validity, sentence
        ├── panel   (SPEC-0005)
        └── process (SPEC-0005)

 define statement (SPEC-0002 §8.9) — signed by the definer, this = [4, DefinitionId]
```

## 4. Definition body and identity

### 4.1 Body

```
definition-body = {
  1 definer:  kid,
  2 name:     text,
  3 version:  text,
  ? 4 imports: [+ DefinitionId],
  5 entries:  [+ entry]
}
entry = [ entry-type, entry-map ]
```

| entry-type | entry | specified in |
|---|---|---|
| 1 | type | §6, §5.4 |
| 2 | template | §7 |
| 3 | panel | SPEC-0005 §4 |
| 4 | process | SPEC-0005 §5 |

Every map in a definition body is closed: an unregistered key MUST cause the
definition to be rejected. Labels MUST be unique within a definition across all
entries.

### 4.2 Identity

`DefinitionId = SHA-256(KSA-CBOR(definition-body))`, using the encoding of
SPEC-0002 §4.2. A verifier that obtains a definition body MUST decode it with the
validating decoder of SPEC-0002 §4.3 and MUST recompute its DefinitionId; if the
result differs from the DefinitionId it was looking for, the body MUST be
rejected. A DefinitionId is computed, never asserted.

### 4.3 Imports

`imports` lists other definitions whose types this definition's entries refer
to. Because each is named by hash, an import cannot name a definition that does
not yet exist, so the import graph is acyclic by construction. A verifier
evaluating a definition MUST obtain every import.

### 4.4 Locators

A definition MAY be obtained from anywhere: a presentation that carries it
(SPEC-0001 §8), a wallet's cache, the library, a peer, a URL. Every such source
is a **locator**: a hint for retrieval, never an identity. Content obtained from
a locator is accepted only by §4.2.

## 5. Common structures

### 5.1 Type references inside a definition

```
local-type-ref = { ? 1 definition: DefinitionId, 2 label: label }
```

Inside a definition body, a type reference whose `definition` is absent refers
to **the enclosing definition** — a definition cannot contain its own hash. A
type reference whose `definition` is present MUST name one of the enclosing
definition's `imports`. In statements, `definition` is always present
(SPEC-0002 §7.4).

### 5.2 Labels

A label matches `[a-z][a-z0-9-]{0,62}`. Labels are local to their definer
(ARCH-0002 P1): `(DefinitionId, label)` is globally unique; the label alone is not.

### 5.3 Language maps

```
language-map = { + language-tag => text }
```

A language map's keys are language tags [RFC5646], well-formed and written in
the canonical case of RFC 5646 §2.1.1 (`en`, `es`, `zh-Hant`, `en-GB`). A
language map MUST have at least one entry. It is RECOMMENDED that every language
map include `en`. A renderer selects a language as in §10.2.

### 5.4 Type definition

```
type-def = {
  1 label:       label,
  2 base:        base-kind,                     ; §6
  3 names:       language-map,                  ; what a person calls it
  4 short:       language-map,                  ; one line, shown on a card
  ? 5 long:      language-map,                  ; what it means and when to use it
  ? 6 values:    [+ value-def],                 ; REQUIRED when base is enum
  ? 7 constraints: [+ constraint-rule],         ; §8
  8 delegation:  0 / 1 / 2,                     ; none / same / scoped
  ? 9 review:    [+ review-question],
  ? 10 examples: [+ value],
  ? 11 fields:   [+ field-def],                 ; REQUIRED when base is record
  ? 12 params:   { + uint => value }            ; base-kind parameters, §6
}
value-def       = { 1 value: text, 2 names: language-map, 3 meaning: language-map }
field-def       = { 1 name: label, 2 type: local-type-ref, 3 required: bool,
                    4 names: language-map, 5 description: language-map, ? 6 unit: text }
review-question = { 1 tag: label, 2 ask: language-map }
```

`delegation` states whether trust about this type may be delegated: `0` never;
`1` only with the same range (no narrowing is possible); `2` with a range that
narrows, under the base kind's subset rule. A trust statement that delegates a
type whose `delegation` is `0` is a type error (SPEC-0004 §6).

`review` lists the questions a human reviewer should answer before reviewing or
approving a statement of this type. Wallets SHOULD present them as a checklist
(SPEC-0001 §7).

## 6. Base kinds

A type's base kind fixes, exactly, five things: what an **assignment** is, what
a **range** is, when a value is **in** a range, when one range is **within**
another, and what the **unbounded** range is. Every base kind is implemented by
the verifier; a definition chooses one and may constrain it (§8), but cannot
change its algebra. This is the fixed core of ARCH-0002 DEC-008: definitions are
declarative, and processing they cannot alter is what makes them safe to load
from anyone.

In every base kind, a range is written as an array and the unbounded range is
written by **omitting** `range` from an attribute range (SPEC-0002 §7.4). An
empty array is not a range and MUST be rejected. Ranges MUST be canonical as
stated for each kind, so that equal ranges have equal bytes.

| code | base kind | assignment | range | member | within |
|---|---|---|---|---|---|
| 1 | **enum** | a text equal to the `value` of one of the type's `values` | an array of distinct such texts, in the order they appear in `values` | v is an element | every element of the narrower range is an element of the wider |
| 2 | **integer** | an integer; with `params` 1 = minimum and 2 = maximum when present | `[lo, hi]` with lo ≤ hi, inclusive | lo ≤ v ≤ hi | lo₁ ≥ lo₂ and hi₁ ≤ hi₂ |
| 3 | **text** | a text; `params` 1 = maximum length in octets when present | an array of distinct texts sorted in bytewise order | equal to an element, byte-exact | subset |
| 4 | **dns-name** | a domain name, §6.1 | an array of patterns, §6.1, sorted bytewise, with no pattern within another | §6.1 | every pattern of the narrower range is within some pattern of the wider |
| 5 | **ip-prefix** | an IP address, §6.2 | an array of prefixes, §6.2, sorted, none within another | §6.2 | as dns-name |
| 6 | **digest** | `[digest-alg, bytes]` (SPEC-0002 §12.5) | an array of distinct digests, sorted by encoding | equal to an element | subset |
| 7 | **key** | a kid | an array of distinct kids, sorted | equal to an element | subset |
| 8 | **boolean** | true or false | an array of one or two distinct booleans, `false` first | an element | subset |
| 9 | **record** | a map from field names to values, as `fields` define | none — a record type's `delegation` MUST be 0 | — | — |
| 10 | **time** | a time (SPEC-0002 §4.4) | `[not-before, not-on-or-after]`, the first less than the second | nb ≤ v < noa | nb₁ ≥ nb₂ and noa₁ ≤ noa₂ |
| 11 | **email** | an address, §6.3 | an array of patterns, §6.3, sorted bytewise, none within another | §6.3 | as dns-name |

### 6.1 dns-name

An assignment is a domain name written as A-labels [RFC5890]: lowercase letters,
digits and hyphens, labels of 1–63 octets separated by `.`, no leading or
trailing `.`, total length at most 253 octets. A pattern is either a name — which
matches only that name — or `*.` followed by a name — which matches every name
with **one or more** further labels below it (`*.foo.com` matches `a.foo.com` and
`x.a.foo.com`, not `foo.com`). This is FKSA's decision for multi-label wildcards.
A name or pattern not in this form MUST be rejected, not normalised: `Foo.com`
and `foo.com.` are invalid, not equal to `foo.com`.

### 6.2 ip-prefix

An assignment is an IPv4 address in dotted-decimal form with no leading zeros,
or an IPv6 address in the canonical text form of [RFC5952]. A prefix is an
address followed by `/` and a length, with every bit beyond the length zero
(`10.1.0.0/16`, not `10.1.2.3/16`). An address is in a prefix if their first
*length* bits are equal. IPv4 and IPv6 never match each other. Non-canonical
forms MUST be rejected.

### 6.3 email

An assignment is `local@domain`, where `domain` is a dns-name assignment (§6.1)
and `local` is the local part exactly as given — byte-exact, never case-folded,
since a mail system may distinguish case in it. A pattern is an address — which
matches only that address — or `*@` followed by a dns-name **pattern** (§6.1):
`*@foo.com` matches every address at `foo.com`; `*@*.foo.com` every address at
any name below `foo.com`. A pattern is within another if every address it matches
is matched by the other. Quoted local parts and comments are not supported in this
version and MUST be rejected.

This is the type behind the email-delegation scenario in UC-0001 §UC-5: a domain
owner trusted about `*@foo.com` may delegate `*@eng.foo.com`, and not
`*@bar.com`.

## 7. Templates

A template is the unit a person issues statements from.

```
template-def = {
  1 label:      label,
  2 function:   kind-code,                    ; 4 attestation, 5 trust, 9 review, 10 approve
  3 target:     { 1 types: [+ target-type], ? 2 rules: [+ constraint-rule] },
  4 attributes: [+ template-attribute],
  ? 5 max-validity: uint,                     ; seconds
  ? 6 approval: process-ref,                  ; SPEC-0005: a process that must be met
  ? 7 issuer:   { 1 topic: label },           ; the delegated topic an issuer must hold
  8 sentence:   language-map,                 ; §10
  9 names:      language-map,
  ? 10 short:   language-map
}
template-attribute = { 1 type: local-type-ref, 2 required: bool, ? 3 fixed: value, ? 4 default: value }
```

### 7.1 Conformance

A statement that names a template (SPEC-0002 §8.5) **conforms** to it if and only
if every condition below holds. Non-conformance is a rejection at the *expected*
level of ARCH-0002 P5, whatever the statement's signature or authorization
(ARCH-0003 W-17).

1. The statement's kind equals the template's `function`.
2. The statement's target type is in `target.types`, and every `target.rules`
   rule holds for the target (§8).
3. Every template attribute with `required: true` appears in the statement.
4. Every attribute in the statement is one of the template's attributes. A
   template is closed.
5. Where a template attribute has `fixed`, the statement's value equals it.
6. Every value is a valid assignment for its type, and every constraint of its
   type holds.
7. Where `max-validity` is present, the statement has both `not-before` and
   `not-on-or-after`, and their difference is at most `max-validity` seconds.

`default` is used only by the issuing interface to pre-fill a form; it has no
effect on conformance.

### 7.2 Issuing

An issuing interface lists the templates of the definitions in use in a context
(SPEC-0001 §6), generates a form from the template and its types — **with no
template-specific code** — fills the target and attributes, checks conformance
before signing, and names the template in the statement it signs.

## 8. Constraints

### 8.1 Rules

```
constraint-rule = { 1 rule: expr, 2 explain: language-map }
```

Every rule carries `explain`: the sentence a renderer shows when the rule does
not hold — "validity may not exceed 30 days", "release digests use SHA-256". A
rule without `explain` makes its definition non-conforming.

### 8.2 Expressions

An expression is an array whose first element is an operator code.

| code | form | holds when |
|---|---|---|
| 1 | `[1, path, value]` | the value at `path` equals `value` |
| 2 | `[2, path, value]` | it does not |
| 3 | `[3, path, [+ value]]` | it equals one of the listed values |
| 4–7 | `[4..7, path, int]` | it is <, ≤, >, ≥ the integer |
| 8 | `[8, path, uint]` | its length in octets (text, bytes) or elements (array) is ≤ the integer |
| 9 | `[9, [+ expr]]` | every listed expression holds |
| 10 | `[10, [+ expr]]` | at least one holds |
| 11 | `[11, expr]` | the expression does not hold |
| 12 | `[12, path]` | a value is present at `path` |
| 13 | `[13, path, range]` | the value is in `range` under its type's base kind |

A `path` is an array of field labels and array indices descending into the value
under test; the empty array is the value itself. For a template's target rules
the value under test is the target: `[0]` is its target type and `[1]`, `[2]`
its components. A path that does not resolve makes the expression false, except
under operator 11, where `[11, [12, path]]` tests absence.

### 8.3 Evaluation

Expressions are total, bounded and side-effect free. A verifier MUST reject a
definition containing an expression nested more than 16 deep or with more than
256 nodes, and evaluation of a conforming expression always terminates. No
expression can call out, loop, read the network, or read anything except the
value under test. This keeps definitions inside ARCH-0002 DEC-008's boundary.

## 9. Conformance of a definition

A definition body conforms if and only if:

1. it decodes under SPEC-0002 §4.3 and matches the structures of this document,
   with closed maps and unique labels;
2. **every** type has `names` and `short`; every enum value has `names` and
   `meaning`; every record field has `names` and `description`; every
   constraint rule has `explain`; every template has `names` and `sentence`;
   every panel and process has the language maps SPEC-0005 requires;
3. every type reference resolves to this definition or to an import;
4. every enum type has `values`, every record type has `fields`, and a record
   type's `delegation` is 0;
5. every example is a valid assignment for its type;
6. every expression satisfies §8.3.

A verifier MUST NOT use a non-conforming definition to evaluate any statement.
A statement whose types are in a non-conforming or unobtainable definition fails
the semantics line of the verdict (SPEC-0004 §10).

## 10. Rendering

### 10.1 Sentences

A template's `sentence` is a language map of texts containing placeholders:

| placeholder | renders |
|---|---|
| `{says}` | the speaker, as SPEC-0001 §7.3 requires: the relying party's own label for the persona, or a fingerprint — never the speaker's self-asserted label alone |
| `{this}` | the target: for a digest, `sha-256:` and its first 8 octets in hex; for a key, as `{says}`; for a statement, its rendered sentence or digest |
| `{label}` | the `meaning` of the value of the attribute with that label (for enum), or the value itself |
| `{label.name}` | the `names` text of the value (for enum) |

Using TV-4 and DV-1 (SPEC-0002 Appendix A), with a relying party that labels
Alice's key "Alice":

> en: *Alice attests that sha-256:48dfc39586b0c4f9 was built reproducibly from published sources.*
>
> es: *Alice atestigua que sha-256:48dfc39586b0c4f9 fue compilado de forma reproducible desde fuentes publicadas.*

### 10.2 Language selection

A renderer selects, for each language map independently, the first of: the
reader's preferred languages in order; `en`; the lexicographically first tag
present. When the selected language is not the reader's preferred one, the
renderer MUST indicate that a fallback was used.

### 10.3 What a renderer must not do

A renderer MUST NOT present a value for which the type has no `meaning` in any
language as though it had one, and MUST NOT render a statement whose definition
is unobtainable or non-conforming as though its meaning were known: it renders
"unresolved vocabulary" with the DefinitionId.

## 11. Publication, adoption and supersession

### 11.1 Publication

A definer publishes a definition by signing a `define` statement (SPEC-0002 §8.9)
whose target is `[4, DefinitionId]` and whose `name` and `version` equal the
body's. The `define` statement's speaker MUST equal the body's `definer`.

### 11.2 Unpublished definitions

A definition with no verified `define` statement may still be cited by hash and
evaluated. It is **unattributed**: a renderer MUST say so, and no trust anchor can
make its author authoritative, because it has none (SPEC-0004 §9).

### 11.3 Supersession

A definition is never edited: any change produces a new DefinitionId. A definer
replaces a definition by publishing the new one with `supersedes` naming the old
(SPEC-0002 §8.9). Supersession is honoured only when both have the same definer.
Statements made under the old definition keep their meaning; a relying party MAY
treat a superseded definition as deprecated by policy.

## 12. Registries

Append-only and never reused, as SPEC-0002 §12.

- **Entry types** — §4.1.
- **Base kinds** — §6.
- **Expression operators** — §8.2.
- **Type-definition, template, value, field and question map keys** — §5.4, §7.

## 13. Security considerations

### 13.1 No code in definitions

A definition can choose a base kind and add
declarative constraints. It cannot change how ranges intersect, and it cannot
execute. Loading a definition from an unknown key is therefore safe; relying on
statements under it is a trust decision (SPEC-0004).

### 13.2 Substitution

Because statements cite definitions by hash, an attacker
cannot change what a value means after the fact. An attacker can publish a
*different* definition with the same `name`; the DefinitionId differs, and the
renderer shows the definer.

### 13.3 Homographs

Labels are restricted to `[a-z0-9-]`; DNS names to A-labels;
language-map texts are presented as published. A renderer SHOULD mark text in a
script different from the reader's.

### 13.4 Range canonicality

Ranges have exactly one encoding (§6), so two
statements scoping the same set have the same bytes, and narrowing is decided by
the base kind's rules, never by comparing bytes.

### 13.5 Resource limits

A verifier MAY reject a definition body larger than
1 MiB or with more than 1024 entries.

## 14. Privacy considerations

A definition reveals its definer and its subject matter. A `speaks` statement
reveals which definitions a key uses. Neither reveals who relies on them.

## 15. References

### 15.1 Normative
[RFC2119], [RFC8174], [RFC8949] — as SPEC-0002.
- [RFC5646] Phillips, A. and M. Davis, "Tags for Identifying Languages", BCP 47, RFC 5646, September 2009.
- [RFC5890] Klensin, J., "Internationalized Domain Names for Applications (IDNA): Definitions and Document Framework", RFC 5890, August 2010.
- [RFC5952] Kawamura, S. and M. Kawashima, "A Recommendation for IPv6 Address Text Representation", RFC 5952, August 2010.
- [SPEC-0002] KSA Core.

### 15.2 Informative
- [PICS] Miller, J., Resnick, P. and D. Singer, "PICS 1.1 Rating Services and Rating Systems — and Their Machine Readable Descriptions", W3C Recommendation, October 1996.
- [FKSA] — §8–§9, schema federation and attributes.
- [ARCH-0002], [ARCH-0003].

---

## Appendix A. Example — DV-1

DV-1 is the definition in SPEC-0002 Appendix A, whose DefinitionId is
`517007656a617b3b…` (full value there). In human-review form:

```yaml
definer: '0x21fe31dfa154a261626bf854046fd2271b7bed4b6abe45aa58877ef47f9721b9'   # Alice
name: supply-chain
version: "1"
entries:
  - type:
      label: build-provenance
      base: enum
      names: {en: Build provenance, es: Procedencia de la compilación}
      short: {en: How the artifact was built., es: Cómo se compiló el artefacto.}
      values:
        - value: reproducible
          names: {en: Reproducible, es: Reproducible}
          meaning: {en: built reproducibly from published sources,
                    es: compilado de forma reproducible desde fuentes publicadas}
        - {value: attested, names: {en: Attested}, meaning: {en: built by an attested pipeline}}
        - {value: unverified, names: {en: Unverified}, meaning: {en: origin not verified}}
      delegation: scoped
      review:
        - {tag: provenance, ask: {en: Does the provenance name the expected builder?}}
  - type:
      label: outcome
      base: enum
      names: {en: Review outcome}
      short: {en: What a reviewer concluded.}
      values:
        - {value: approve, names: {en: Approve}, meaning: {en: ready to publish as built}}
        - {value: changes, names: {en: Request changes}, meaning: {en: not ready; changes needed}}
        - {value: reject,  names: {en: Reject}, meaning: {en: must not be published}}
      delegation: none
  - template:
      label: release-attestation
      function: attestation
      target: {types: [digest]}
      attributes: [{type: build-provenance, required: true}]
      max validity: 2592000          # 30 days
      sentence:
        en: "{says} attests that {this} was {build-provenance}."
        es: "{says} atestigua que {this} fue {build-provenance}."
      names: {en: Release attestation}
```

TV-5 (Carol trusts Alice about build-provenance in `[reproducible, attested]`,
delegable within `[reproducible]`) shows an enum range and its narrowing: the
delegation range is within the trust range because `reproducible` is an element
of both, and DV-1's `build-provenance` has `delegation: scoped`.
