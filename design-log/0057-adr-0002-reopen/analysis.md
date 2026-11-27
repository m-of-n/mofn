---
schema: "design-log/v1"
id: DL-0057
part: analysis
title: "Gap analysis — original goals and vocabulary against ARCH-0002, ADR-0002, ADR-0004…0008 and SPEC-0001…0005; a plan for one base architecture"
date: "2026-11-25"
---

# DL-0057 — gap analysis and a proposed order of work

Written for the sponsor after reopening `ADR-0002`. **It proposes; it decides
nothing.** Read against `origin/main` at `5b2e1bf` (2026-11-25).

**Limits, stated first.**

- The weekly minutes are not published, so **what the sponsor meant by "a
  richer vocabulary" can only be reconstructed from what the repository kept**.
  Where the record is thin this says so, and §10 lists what only the sponsor can
  supply.
- Several of the principles under review were **drafted from the sponsor's own
  direction of 2026-09-22** (`ARCH-0002` P2, P3, P6 quote it; `DL-0002` records
  which parts the human corrected). The reopening is therefore not only a
  question of what students or an agent wrote. It may be a question of what
  was *compressed* between that direction and the text, and §3 and §4 separate
  those readings.
- Process observations (§7) are about the shape of the process, not about any
  person's good faith.

---

## 1. Top findings

1. **P2 describes three slots; the architecture and the specification have
   six.** P2's form is *A says B has C*. `ARCH-0001` v0.1.0 gave every kind a
   `validity`; `SPEC-0002` §7.1 makes a statement `kind · suite · says · this ·
   valid · body`, with eleven kinds. **Time (validity) is in the specification
   and absent from the principle.** This is the sponsor's "time limitations"
   point, and the record supports it.
2. **The original vocabulary was narrowed in steps, each one reasonable.**
   Five kinds (`NameCert`, `AuthzCert`, `AclEntry`, `ArtifactStatement`,
   `Endorse`) became "functions over one form" (P6, `ARCH-0001` 0.2.0 §4.2).
   The SPKI 5-tuple `(issuer, subject, delegation, tag, validity)` became
   `says · this · may-delegate · about · valid`. **A delegation *bit* became an
   integer depth, and the *tag* became a typed attribute range**, while
   DEC-004 (*which tag language*) is still formally open. `ARCH-0001` R-M-10
   records the first change and its limit. Nothing records the second as a
   decision.
3. **P6 and R-M-04 contradict each other as written.** `ARCH-0002` P6: *"There is
   no distinct naming object."* `ARCH-0001` R-M-04, a Must: *"Name bindings and
   authorization bindings SHALL be distinct object kinds."* `ARCH-0001` §4.2's
   note says R-M-04 "still holds" as *functions*. **The SPEC does not follow
   P6 either:** `SPEC-0002` §7.2 has a **name target** (type 7, an SDSI compound
   name) and `SPEC-0003` §6.4 a **name base kind** (12), which `ADR-0008`
   added. The specification has a naming object. The principle says there isn't
   one.
4. **"A type is a schema" is not what the specification says.** The word
   *schema* appears in no normative sentence of `SPEC-0001`…`SPEC-0005`. A type
   there is a `type-def` inside a *definition*, identified by `(DefinitionId,
   label)` (`SPEC-0003` §5.4). *Schema* is also used for the front matter
   (`schema: archdoc/v1`), the record schema in the library and the `spec/schema/`
   directory. P3 uses a word the specification avoids and the repository
   already uses three other ways.
5. **Four documents each say they govern, and they disagree.** `CLAUDE.md`:
   `ARCH-0001` is "the source of truth". `ARCH-0002`: where it conflicts with
   `ARCH-0001` §4, "ARCH-0001 governs and this document is wrong".
   `ADR-0003` (sponsor, accepted): where a SPEC and an ARCH document differ,
   **the SPEC governs**. `ARCH-0001` §5.5 repeats the SPEC rule. The ARCH
   documents are `draft`; the SPECs are `draft`; the ADR that ranks them is
   `accepted`. A new ADR cannot be checked for consistency when the order of
   authority is itself disputed.
6. **The same words carry several senses across documents** (§5): *name*,
   *type*, *statement*, *validity/valid*, *label*, *schema*, *attestation*,
   *claim*, *domain of discourse* against *definition*, *predicate* against
   *attribute*, *principal* against *persona*. `GLOSSARY-0001` exists, but it
   was written to catch *collisions* (one word, two senses on one page). It
   defines **none** of *name*, *principal*, *validity*, *threshold*, *claim* or
   *attribute*, and its entries for *Statement*, *Type*, *Delegation* and
   *Attestation* are P2 and P3 restated.
7. **The engine implements less than the specification, and the specification
   less than the architecture** (§6). Revocation is specified for paths and for
   attestations (`SPEC-0004` §6.3 item 2, §5.2, worked Ask 2) and **the engine
   does not apply it** outside name bindings (`reduce.py` says so; answers
   report `0` revocations considered). Threshold trust statements and threshold
   anchors' own `may-delegate` are not followed (T-095). `Group`, `aliases`
   and `online_check` have no form. `review`, `approve`, `aggregate`, panels and
   processes (`SPEC-0005`) verify structurally but are not evaluated.
   **k-of-n and delegation, two original goals, are the two the demo leans
   on.**
8. **Six ADRs were accepted one question at a time; none of those six was
   reviewed by a second reader.** `ADR-0002`, `0004`, `0005`, `0006`, `0007`,
   `0008` all carry `reviewed: false`; all name one student decision maker acting
   under a verbal delegation with no written confirmation (`DL-0021`).
   `ADR-0002` §7 itself argued that a decision-maker name with no act behind it
   is "a forged provenance record in a project whose subject is provenance"
   and then, on 2026-11-06, was accepted under a verbal delegation relayed three
   days earlier. The decisions
   may well be sound. **The process gave no way to find out, and no ADR is
   required to cite a base definition it relies on.**

---

## 2. The original goals and vocabulary, as the repository records them

| source | what it says | notes |
|---|---|---|
| **Goal statement**, `PLAN-0001` §1, sponsor 2026-09-16 | *"Advances in trust, provenance, and attestation through **AI-assisted protocol design**, enabling **key-centric semantic attestations**."* | Three parts: trust/provenance/attestation; the method; **key-centric** and **semantic**. |
| `ARCH-0001` v0.1.0 §1 (first commit, `2a79b1f`, 2026-09-16) | six primary objects: principal (key or key digest); **local names relative to a naming key (SDSI)**; **authorization bound to a principal, optionally delegated, with tag intersection (SPKI)**; **threshold subjects, k of n**; signed statements about artifacts (PICS lineage); import and export | The founding list. Names, authorization, thresholds and attestations are four separate items. |
| `ARCH-0001` v0.1.0 §2.1 | G1 key-centric principals, **names not globally unique**; G2 **separate name certificates from authorization certificates**; G3 deterministic reduction (SPKI 5-tuple style); G4 k-of-n in the native model; G5 artifact statements use the **same principal and validity machinery** as rights; G6 mapping in and out; G7 versioned documents, decisions reversible until accepted | G2 and G5 pull in opposite directions; v0.1.0 kept both. |
| `ARCH-0001` v0.1.0 §4.1–§4.2 | `Principal = Key | KeyId | Name | Threshold | Group`; `Name = {issuer, labels[]}` compound SDSI; `Threshold = {k, n, members}`; `Validity = {not_before?, not_after?, online_check?}`; five kinds **each with `validity`**; `AuthzCert = {issuer, subject, delegate: bool, tag, validity}` | The 5-tuple, as built. |
| `ARCH-0001` §3.1 (still in the file) | SPKI authorization certificate is `(Issuer, Subject, Delegation, Tag, Validity)`; two 5-tuples compose when subject-of-first is issuer-of-second and delegation is permitted; **result tag and result validity are intersections** | The reduction the goals name. |
| Sponsor correction, 2026-09-22 (quoted in `ARCH-0002`, "Note — reduction is simpler") | reduction is *"simply taking a set of cryptographically signed statements and then following the chain of inference to determine if you trust the statement"*; SPKI is *"prior art we take ideas from, and fidelity to its formalism is not a goal"* | This relaxes **fidelity to the 5-tuple ceremony**. It does not say the five parts go away. |
| Sponsor direction, 2026-09-22 (`ARCH-0002` P2, P3, P6 and `DL-0002`) | P2: the statement form *A says B has C*, with constraint as one **function**; P3: *a type IS a schema* — representation, constraints, semantics, human-review tags, multilingual descriptions; P6: *"a 'name' is just a type of attested string"*; delegation scoped by **(Domain, Topic)** | `DL-0002`: the model proposed "constraints come from a speaker" as P2 and the human corrected it to the form. The example/principle confusion went both ways. |
| `ARCH-0002` P2 table, **Contract** row | *"open. The sponsor indicated a further form; not yet specified."* | **The record itself says there is at least one more form** and none is specified. |
| `ARCH-0001` v0.1.0 R-O-02, R-M-09 | short-lived validity preferred to revocation; **validity intersection** defined | **Time limits are a stated requirement from the first version.** |

**What this supports.** The sponsor's objection to P2 is consistent with the
record: the founding model had **five kinds, a validity on each, a delegation
bit, a tag, thresholds and local names**, and P2 as accepted names three slots
and six functions, one of them open. **What it does not settle** is which "more
forms" the sponsor means. Candidates in the record: the five v0.1.0 kinds, the
Contract form, the eleven KSA kinds, or something the minutes hold. See §10.

---

## 3. Trace: each original concept, down the stack

Columns: **v0.1.0** = `ARCH-0001` 2026-09-16. **ARCH now** = `ARCH-0001` 0.3.5.
**P** = `ARCH-0002` principles and `ADR-0002`. **SPEC** = `SPEC-0001`…`0005`.
**Engine** = `prototype/wallet/engine/` at `5b2e1bf`.

| concept | v0.1.0 | ARCH now | P (ARCH-0002 / ADR-0002) | SPEC | engine | verdict |
|---|---|---|---|---|---|---|
| **Issuer / speaker** | `issuer: Principal`, must be Key or KeyId at signing | R-O-01: a `KeyId` | P2: *A*, "a key, a hash of a key, **or an alias** resolving to one" | `says` is a **kid** only; "on the wire a persona appears only as kids" | kid | **P conflicts with SPEC:** P2 lets a name speak; SPEC never does. SPEC is the narrower and safer, and P2 should follow it |
| **Subject** | `subject: Principal` (Key, KeyId, Name, **Threshold**); statements take `subjects: [ArtifactId…]` (plural) | `subject` / `this` | P2: *B*, any `ArtifactId` mode | **one** `this`, types 1 key, 2 digest, 3 statement, 4 definition, 6 description, 7 name; 5 withdrawn | same | Plural subjects → one target. A threshold is **not** a subject in the SPEC; it is a form of `trust` |
| **Statement forms** | **5 kinds**, each signed, each with validity | §4.2: five rows → KSA kinds, plus lifecycle row | P2: **one form, 6 functions** (Attestation, Delegation, Constraint, Review, Approval, **Contract open**) | **11 kinds**: key-publish, self, speaks, attestation, trust, revoke, rotate, define, review, approve, aggregate | all 11 verify; evaluated: attestation, trust, define, and revoke/rotate for name bindings only (§6) | **Three different counts (5, 6, 11) for "the forms", with no list that derives the others.** P2's functions and SPEC's kinds are not the same list: *Constraint* has no kind; *revoke*, *rotate*, *define*, *speaks*, *self*, *aggregate* have no function |
| **Validity (time)** | `{not_before?, not_after?, online_check?}` on every kind | §4.1 same; R-M-09 intersection | **not in P2.** "Validity" in P5 means *RFC 8949 data-model validity* | `valid = {not-before, not-on-or-after, issued}`; `not-on-or-after` also in `may-delegate`; **no online check** | time only; delegation expiry works (E-1…E-7); intersection of windows along a path | **P2 omits it; P5 uses the word for something else.** Same word, two senses, in one document |
| **Delegation (bit → depth)** | `delegate: bool` | R-M-10: `may_delegate {depth, ranges, allow/exclude keys, not_on_or_after}` | P2: *A says B can speak about (Domain, Topic)* | `trust` + `may-delegate`; depth counts hops; `delegation 0/1/2` per type (none/same/scoped) | depth, widening, expiry, allow/exclude all enforced | **Behaviour is richer than the principle and better specified.** RFC 2693 §4.1.4's objection to depth is recorded as a stated limit (R-M-10) |
| **Authorization tag** | `Tag`, "opaque except for defined intersection" | `attribute-range`; DEC-004 **open** | P2/P7: scope by (Domain, Topic); profile chooses tag types | `attribute-range {type-ref, range}`; base kinds in `SPEC-0003` §6, `within` defined once | enum, text, int, ip-prefix, email, … | **DEC-004 is open on paper and answered in practice** by `SPEC-0003` §6. No ADR records that |
| **Threshold k-of-n** | `Threshold {k, n, members}` is a **Principal**, usable as a subject | R-M-06 Must; `Principal` includes it | not mentioned in P1–P7 | only as **`trust` threshold form** (`this` absent, `trusts: [2* kid]`, `threshold`); keys only, no nesting; `SPEC-0001` §1.3 puts multi-speaker contracts out of scope | **anchor** thresholds work (E-11…E-19: k distinct members each attested); **threshold trust statements as hops and threshold `may-delegate` are not followed** (T-095) | **Original goal G4, partly built.** Principles are silent; the narrowing from "a principal kind" to "a trust form" happened in the SPEC without an ADR |
| **Names (SDSI)** | `Name {issuer, labels[]}`, compound; `NameCert` its own kind; G2 | §4.1 kept by decision (`DL-0028`); R-M-03, R-M-04 | **P6: "a name is an attested string"; "no distinct naming object"** | target type 7 (compound SDSI name), base kind 12 `name`; bindings need no anchor; a label bound twice is a **group**; names follow rotation (`ADR-0008`) | `names.py`: resolution, groups, rotation, revocation for bindings | **The specification and engine implement SDSI local names. P6 as worded does not describe them,** and R-M-04 contradicts P6 |
| **Group** | `Group` in `Principal` | §4.1; §5.5: **no form** | — | none; `ARCH-0001-PROPOSAL-v0.4.0` (draft) proposes a group is a key; a label bound twice is a *name group* (a different thing) | none | **"Group" now means two things** (SDSI name group, proposed enrolled group). Both undefined in the glossary |
| **Attestation / assertion** | `ArtifactStatement`, PICS analogue: issuer ≈ rating service | §4.2: `attestation (4)` about a subject | P2 function *Attestation*; P6: `ArtifactStatement` is "P2's form with a predicate type" | kind 4 `attestation`; `has: [+ attribute]` | covered-by-path evaluation | Consistent across the stack. **"Assertion"** appears twice in ARCH-0001 and twice in SPEC-0002 as a plain English word, with no definition |
| **Type / schema / definition** | `PredicateType` = a **URI** | `type-ref {definition, label}`, key-relative (P1) | **P3: a type is a schema** (representation, constraints, semantics, review tags, multilingual text) | `type-def` in a `definition`; `DefinitionId` = hash of canonical body; templates; base kinds | `definition.py` loads and renders | P3's five parts are **all present in `type-def`** (`base`, `constraints`, `names`/`short`/`long`, `review`, language maps). The *content* of P3 is built. The **word "schema"** and the **claim that a type *is* one** are what is disputed, and what the SPEC does not use |
| **Domain of discourse** | — | §2.3 notes P4 draft | **P4 (draft):** a hash-identified *set* of schemas | no such term; **definition** (`DefinitionId`) is the unit; `ARCH-0003` §3.5, `GLOSSARY` say *definition generalises domain* | one definition at a time; no sets | **P4 draft is superseded in practice by *definition***. `ADR-0007` cites P3 and P1, not P4 |
| **Revocation** | `online_check`; R-O-02 | R-O-02: representable | P2 consequences: constraints "subject to the same … revocation" | `revoke` kind; §7.1 required for paths, attestations, bindings (ADR-0003 D5) | **names only** | Spec says yes; engine says no (finding 7) |
| **"Validity is checked, never assumed"** | not in v0.1.0 | R-O-05/R-O-06 | **P5** (well-formed / valid / expected; P5.1 canonical; P5.2 interchange) | `SPEC-0002` §4.3, §5, §13.5; `SPEC-0003` §7.1 cite or restate | rejecting decoder, 60+ fixtures | **Sound, built, cited. Not objected to.** Held only because its acceptance rode on `ADR-0002` |

---

## 4. Where each document narrowed or contradicted the goals

### 4.1 `ARCH-0002` P1–P7 and `ADR-0002`

- **P2 narrows the vocabulary** (finding 1, 2) and **lists forms that do not
  match the SPEC's kinds**. It also gives (Domain, Topic) delegation without
  saying how that becomes `attribute-range {type-ref, range}` (the SPEC does
  this implicitly: the `DefinitionId` is the domain and the `label` the topic).
- **P3 asserts an identity ("is a schema") where the SPEC has a composition**
  (a definition *contains* type definitions). `DL-0002` shows the human's
  addition was "a type IS a schema — representation, constraints, semantics,
  human-review tags, multilingual descriptions". The five-part content survived
  into `SPEC-0003`; the identity claim is what is left to settle.
- **P6 collapses two things**: (a) *a name is **bound** by a signed statement in
  its speaker's namespace* (true, and `SPEC-0004` §5.3, `ADR-0008` say it) and
  (b) *a name is a **string*** (the text of P6, and what the sponsor rejected).
  SDSI's contribution is the **namespace relativity and chaining** (`(name fred
  sam)` is George's Fred's Sam). A string has neither. The SPEC kept both; the
  principle kept neither word. **P6 also says "`NameCert` is therefore not a *kind* of
  object"**, which G2 and R-M-04 deny.
- **P4's replacement (definition) was never decided as P4's replacement.** It
  entered through `ADR-0003` D1 (sponsor) and `SPEC-0003`. P4 remains draft and
  is cited by `ADR-0007` as context only.
- **P5 uses "validity" for a different thing than P2's missing slot** (§5).
- **`ADR-0002` §2 says accepting it "accepts no DEC-\*"**; but `ADR-0007`
  (DEC-007) and `ADR-0008` both name it as a ground. An ADR that decides
  nothing was used as the basis for two that do.

### 4.2 `ADR-0004`…`ADR-0008`

| ADR | decides | leans on | gap |
|---|---|---|---|
| **0004** DEC-002 KSA-CBOR | one deterministic CBOR profile; decoder rejects non-canonical; no IANA registry native; COSE/DSSE export only | P5.1 (named), P1 | The whole SPEC and the vector set depend on it. Its own text records that part of the evidence favoured another option and that reopening was costed. Reviewed: false. **Not touched by this reopening**, but P5.1 is cited by name |
| **0005** DEC-003 `kid` | `kid = SHA-256(suite public-key encoding)`, fixed across suites | P1, P1.1 (draft), P5.2 | Changing the hash needs a new identifier version. Low relation to the vocabulary dispute |
| **0006** DEC-001 slug | title `m-of-n`, slug `mofn` | P6 in one rejected-alternative row | The decision does not depend on P6. Only a sentence does |
| **0007** DEC-007 predicate rendering | meaning comes from a signed, hash-identified definition; one renderer | **P3 as accepted**, P1 | **Direct dependence.** Its context quotes *"`ADR-0002` accepted P3"* as a ground. The *behaviour* (one renderer, definitions with human-readable semantics) is independent of the word "schema" |
| **0008** SDSI names | name target (7), base kind 12, no-anchor bindings, groups, rotation | **P6 as accepted** (context) | **Direct dependence in its context, none in its decisions.** The decisions are SDSI, and are the best evidence that the SPEC did not take P6's "no distinct naming object" literally |

### 4.3 `SPEC-0001`…`SPEC-0005`

- **The terminology tables in `SPEC-0001` §2 and `SPEC-0002` §2 define about a
  dozen terms each and overlap on `persona` and `statement`.** Neither defines *name*,
  *attestation* or *attribute*.
- **`SPEC-0001` §1.2 lists seven design principles** (a principal is a key;
  meaning is published, hashed, readable; authority narrows; trust begins
  locally; verify the bytes first; unknown is an error; the answer explains
  itself). **That is a second list of principles, beside ARCH-0002's seven, and
  they are not the same.** Only #1 and #6 cite ARCH-0002. A reader has no rule
  for which list governs.
- **`SPEC-0001` §1.3 puts "multi-speaker contracts" out of scope**, the form
  `ARCH-0002` P2 marks *Contract — open*.
- **The SPEC set is `draft` and `reviewed: false`** while `ADR-0003` says it
  governs.
- **`SPEC-0002` TV-13's title still says "the NameCert role, ARCH-0002 P6"**,
  while `ADR-0008` says TV-13 is **not** a binding (its type is plain text,
  DV-2). The vector set itself carries both statements.

---

## 5. Definitions that conflict between documents

| term | senses found | where | fix needed |
|---|---|---|---|
| **name** | (1) SDSI compound name, `{issuer, labels[]}` — `ARCH-0001` §4.1, `SPEC-0002` §7.2 type 7; (2) "an attested string" — `ARCH-0002` P6; (3) a plain text attribute called `name` — DV-2, TV-13; (4) a **naming type** of base kind 12 — `SPEC-0003` §6.4, DV-4; (5) `self.label` (a key's own display claim) — TV-2; (6) a type's **label** — `SPEC-0003` §5.2 (same grammar as name labels) | many | One definition of *name* (SDSI), one of *name binding*, one of *label* (type label, name label and display label are three things) |
| **type** | `PredicateType` (URI, v0.1.0); `type-ref {definition, label}` (`SPEC-0002` §7.4); *a schema* (P3); `type-def` (`SPEC-0003` §5.4); "template" (a type's statement shape); "base kind" | ARCH-0001, ARCH-0002, SPEC-0003 | Say what a type is made of, once. *Schema* is not the word the SPEC uses |
| **schema** | P3's type; `schema: archdoc/v1` (front matter); library record schema; `spec/schema/`; YAML 1.2 "core schema" (`SPEC-0002` §11.3) | five senses | Reserve *schema* for one, rename the rest, or drop it from the principle |
| **statement** | the signed object `kind·suite·says·this·valid·body` (`SPEC-0002`); *A says B has C* (P2); "a claim you were handed" (reduction note); the five v0.1.0 kinds (`ARCH-0001`); `ArtifactStatement` | all | One definition of the *object* and a separate one of the *form it takes* |
| **form / kind / function** | P2 "one form, several functions"; `ARCH-0001` v0.1.0 "kinds"; `SPEC-0002` "kind" (code 1–11); P2's functions ≠ SPEC kinds (§3) | ARCH-0001 §4.2, P2, SPEC-0002 §8.1 | A single registry the other lists derive from |
| **attestation** | the basic function (P2); `attestation` kind 4; `ArtifactStatement` (renamed); the protocol name, "Key-centric Semantic **Attestations**" (KSA; #193 made the expansion consistent) | whole stack | Define *attestation* as the kind **and** say whether *assertion* is a synonym. Today it is used loosely |
| **claim** | the "C" of *A says B has C* (P2 table: "a predicate in some type"); a "claim" in the reduction note; "controller kind is a claim" (`SPEC-0004` §4.5); a *role* named `claim` (`ARCH-0003` §4) | P2, ARCH-0003, SPEC-0004 | The glossary has "Statement" and "Attestation" but not *claim* |
| **validity / valid** | (1) the **time window** (`Validity`, `valid`); (2) P5's **data-model validity** (RFC 8949 *valid*); (3) "valid at time t" (`SPEC-0002` §7.3); (4) **verified** (`SPEC-0002` §9 results) | ARCH-0001, ARCH-0002, SPEC-0002 | Two words needed. This is the likeliest to cause a real misreading of "validity is checked, never assumed" |
| **predicate / attribute** | `Predicate` and `PredicateType` (ARCH-0001 §4.1, 13 uses; ARCH-0002, 9 uses); `attribute` (24 uses in SPEC-0002, 10 in SPEC-0003, 13 in SPEC-0004; ARCH-0001 §4.1 maps one to the other) | ARCH vs SPEC | A one-line mapping in the glossary |
| **domain of discourse / definition / vocabulary** | P4 draft; `definition` (SPEC: 57 uses in SPEC-0003); `vocabulary` (10 uses in ARCH-0001); `DV-n` | ARCH-0002 vs SPEC-0003 | `GLOSSARY` already says *definition generalises domain*; P4 does not |
| **principal / persona / speaker / subject** | `Principal = Key|KeyId|Name|Threshold|Group` (ARCH-0001); *persona* "a key-identified principal" (SPEC-0001 §3.1, 63 uses in ARCH-0003); *speaker* (P2); `this` (SPEC) | all | `persona` replaced `principal` in the SPEC, but `Principal` still lists forms (name, threshold, group) that a persona is not |
| **delegation** | `delegate: bool`; `AuthzCert`; *A says B can speak about (Domain, Topic)* (P2, GLOSSARY); `trust` + `may-delegate` (SPEC-0002 §8.6); `delegation 0/1/2` on a **type** (SPEC-0003 §5.4) | ARCH, P2, SPEC | Delegation is both a *statement* (trust with may-delegate) and a *property of a type*. Say so |
| **anchor / ACL / root / Self** | `AclEntry` (unsigned); *anchor* (SPEC-0004 §4); *root*; *trust root you chose yourself* (reduction note) | ARCH, SPEC | Glossary has *Anchor*; not tied to `AclEntry`/`Self` |
| **group** | `Group` principal (unspecified); SDSI name group (`ADR-0008`); enrolled group with a steward (`ARCH-0001-PROPOSAL-v0.4.0`, draft); `Panel` (a set of keys that may speak on a topic, `GLOSSARY`) | ARCH-0001, ADR-0008, PROPOSAL, GLOSSARY | Four meanings, none named apart |
| **KSA** | *Key-centric Semantic Attestations* (current); formerly *FKSA*; "KSA-CBOR" the encoding (`ADR-0004`) | whole | Settled by the cleanup; unrelated to the sponsor's objection |

**Precedence.** `CLAUDE.md` ("ARCH-0001 is the source of truth"), `ARCH-0002`
("ARCH-0001's §4 model governs"), `ADR-0003` ("the SPEC governs") and
`ARCH-0001` §5.5 (repeats the SPEC rule) are four statements of authority. All
four are in force. §9 step 3 asks the sponsor to pick one.

---

## 6. What the engine implements

`prototype/wallet/` at `5b2e1bf` (wallet 0.11.x). 511 wallet tests pass on this
branch, run after the document edits.

| capability | spec says | engine does | evidence |
|---|---|---|---|
| Statement structure, 11 kinds | `SPEC-0002` §7–§8 | all 11 parse and verify; closed maps; reject unknown | `schema.py` `KINDS` |
| **Attestation coverage by a delegation path** | `SPEC-0004` §5.2, §6 | **yes** | E-1…E-7, E-20…E-25 |
| **Delegation: depth, widening, expiry, allow/exclude** | §6.3 | **yes, each named in the answer** (`depth`, `widening`, `not-valid-at-time`, `key-excluded`, `key-not-allowed`) | `reduce.py` `_follow`, `test_delegation.py` |
| **Thresholds, anchor form** | §6.4 | **yes**, *k* distinct members each attest, rotation-linked keys count once | E-11…E-19, `test_thresholds.py` |
| **Thresholds, trust-statement form / `may-delegate` on a threshold anchor** | §6.4 | **no** ("not followed yet", T-095) | `reduce.py` module docstring |
| **SDSI names**: bindings, compound, groups, rotation | §5.3 | **yes** | `names.py`, R-1…R-10, E-8…E-10 |
| **Revocation** | §7.1 applies to paths, attestations and bindings (ADR-0003 D5) | **bindings only.** Answers report `revocations considered: 0` | `reduce.py` docstring; `check.py` |
| Worked "Ask 2" (revoked attestation → `revoked`) | `SPEC-0004` App. A | **no vector in `evaluations`, no test** | `vectors.json` `evaluations` E-1…E-7, E-20…E-25 |
| `review`, `approve`, `aggregate` evaluation; panels, processes | `SPEC-0005` | **verify structurally only; "not supported in v0"** | `definition.py` |
| `Group`, `aliases`, `online_check` | `ARCH-0001` §4.1, §5.5 | none (§5.5 records the gap) | — |
| One renderer, no type-specific code | `ADR-0007` | **yes**, EN and ES | `render.py` |

**So:** the engine implements **names, delegation (depth, widening, expiry),
anchor thresholds, definitions and rendering**, which is most of the original
goals G1, G3, G4 (partly) and G5. **It does not implement revocation for the
things that are revoked in practice, and it does not run any of SPEC-0005.**

---

## 7. Process findings

Observations, not findings against anyone.

1. **One ADR per question, each accepted by the same decision maker.** Order:
   `ADR-0001` (P1, 2026-09-22, reviewed), `ADR-0003` (sponsor, 2026-10-14,
   reviewed), `ADR-0004`/`0005` (2026-10-25), `ADR-0002`/`0006` (2026-11-06),
   `ADR-0007` (2026-11-07), `ADR-0008` (2026-11-12). `ADR-0001` and `ADR-0003`
   are `reviewed: true`; the other six are `reviewed: false`.
2. **Authority was verbal and moved.** 2026-10-25: a delegation scoped to §7 that
   **excluded `ADR-0002`**. 2026-11-03: a broader one, relayed by the other
   student, no date, no written confirmation (`DL-0021`), that "supersedes the
   exclusion". `ADR-0002` was accepted three days later under it.
3. **The ADR recorded its own review gap and accepted it.** MD-2 required review
   before the principles became final; the v0.7.1 review happened. `ADR-0002` §9
   then accepted P5 as amended knowingly, with the decision maker as author of
   P5.1 and P5.2 and a second reader "still owed".
4. **No ADR cites a base definition**, because there is none to cite. Each ADR
   is internally careful (alternatives rejected, acceptance test, evidence).
   None can be checked against a common glossary or against the original goal
   list, so a later ADR can lean on an earlier one's wording (`ADR-0007` on
   P3; `ADR-0008` on P6) without anyone testing the wording.
5. **The principles were drafted from conversation**, and `DL-0002` is candid
   about the model's habit of taking an example for the principle. P2 and P6's
   current wording came out of exactly that kind of exchange.
6. **Three authority documents and one glossary, none ranking the others** (§5).

---

## 8. What the reopening does and does not change

**Changes:** the standing of P2, P3, P6 (not binding) and `ADR-0002` (proposed).
**Does not change:** any byte, vector, `DefinitionId`, engine result, release or
test. `SPEC-0004`, `SPEC-0005`, `prototype/wallet/` and `demo/` do not cite P2,
P3 or P6 at all; `SPEC-0002` cites P6 only in a vector title and `SPEC-0003` in
one status line and §6.4, descriptively. The demo for 2026-12-04 is not
affected.

**Dependents left alone and flagged:** `ADR-0004` (P5.1), `ADR-0005` (P5.2,
P1.1), `ADR-0006` (P6, in a rejected-alternatives row), `ADR-0007` (P3),
`ADR-0008` (P6). `ARCH-0003` cites P2 (three times), P3 (twice), P4 and P6 (once each) as a
design record and was not edited. The throwaway spike `prototype/statements/`
cites P2, P3 and P4 in docstrings, and `prototype/README.md` cites P2; they
are descriptive and were not edited.

---

## 9. Proposed order of work

The sponsor's instruction: *a consistent base architecture and definitions, not
random questions.* So: **one definitions document first, nothing accepted
against anything else until it exists.**

| # | step | output | owner | gate |
|---|---|---|---|---|
| **0** | **Stop the per-question cycle.** No new ADR cites P2, P3 or P6 as accepted; no ADR is accepted in the meantime except by the sponsor in writing. Already done for P2, P3, P6 by this change | this PR | sponsor merges | — |
| **1** | **Capture the original vocabulary from the sponsor, in one sitting.** Ask the §10 questions, record the answers verbatim in the design log. This is the one input the repository does not have | `design-log/NNNN-base-vocabulary/question.md`: the answers | sponsor (30–60 min) | before anything is written |
| **2** | **One canonical definitions document**, `GLOSSARY-0001` promoted from "collisions" to "definitions" (or a new `ARCH-0004`; sponsor chooses). Each term: definition, **source** (RFC 2693 §, PICS, sponsor direction), **where used**, **engine mapping**, status. Terms to cover first: key, kid, principal/persona, statement (object) and its *form*, kind, speaker, subject/target, claim/predicate/attribute, **validity (time) and valid (data model)**, delegation, depth, scope/range/tag, threshold, **name, name binding, label**, group, attestation, assertion, type, definition, domain of discourse, template, anchor, context, revocation, rotation | `project/GLOSSARY-0001` 1.0 or `spec/ARCH-0004` | sponsor reviews; one second reader | each term has a source or is marked *proposed* |
| **3** | **Fix the order of authority.** One sentence, in one place, agreed by the sponsor, that `CLAUDE.md`, `ARCH-0001`, `ARCH-0002`, `ADR-0003` all repeat. The usual answer is: *definitions doc → SPEC → ARCH (design record) → ADR (history)*, but that is the sponsor's call | one edit to each of the four | sponsor | step 2 complete |
| **4** | **Make citation mechanical.** An ADR's front matter carries `defines_against: [DEF-name, DEF-statement, …]`; `bin/validate-archdoc` fails an ADR that cites an undefined term or a principle that is not `accepted` | validator change, 20–30 lines | agent drafts, student reviews | step 2 |
| **5** | **Restate P2, P3, P6 against the definitions.** P2 gets every slot (`kind`, `says`, `this`, `valid`, `body`) and **one registry of forms** (the SPEC's eleven kinds, with the functions as a view over them, and *Contract* named as open). P3 either says *a type is defined by a definition* or drops "schema". P6 says *a name is a label in a key's namespace, bound by that key's signed statement*, and says what happens to R-M-04. This replaces ADR-0002 | one superseding ADR, drafted not accepted | agent drafts, **sponsor accepts** | steps 1–3 |
| **6** | **Re-read the dependents against the base.** `ADR-0004`, `0005`, `0006`, `0007`, `0008` and `SPEC-0003` §6.4: each gets a one-line verdict *consistent / amend / supersede* in `ADR-0002` §10.3's table. Expect mostly *consistent* (the decisions are about bytes and behaviour). The review is for the sentences that quote P3 and P6 | table + any amendments | sponsor or student, with second reader | step 5 |
| **7** | **Close the engine gaps the goals name.** (a) Revocation for paths and attestations, with the missing `revoked` vector and test, then the issue (SPEC-0004 §7.1 already specifies it); (b) threshold trust statements as hops (T-095) — the k-of-n goal; (c) say in the SPEC what `online_check`, `Group` and `aliases` are (drop or build); (d) SPEC-0005 evaluation of `approve`/`aggregate` | issues + one PR each | agent + student | independent of 2–6 |
| **8** | **A traceability matrix**, goal → requirement → SPEC section → vector → engine test, generated from front matter and `vectors.json`. Every Must in `ARCH-0001` §5 has a row; a blank is a visible gap | `project/` table or generated view | agent drafts | step 2 |

**Against 2026-12-04.** Steps 0, 1 and 2 (first pass), and step 7(a), fit before
CS Night and are the strongest story: *the demo's claims trace to the original
goals, and the project found and is fixing its own gaps*. Steps 3–6 and 8 are
after. Nothing in 3–6 changes what the demo shows.

---

## 10. Questions only the sponsor can answer

1. **What are the "more forms" in P2?** The five v0.1.0 kinds? The *Contract*
   form (marked open in P2)? Others from the minutes? A list, even rough.
2. **What were the "time limitations"?** The validity window
   (`not-before`/`not-on-or-after`) and `online_check`? Limits on delegation
   (`may-delegate.not-on-or-after`)? A validity on *every* statement, or only
   some?
3. **P6.** Is the objection to *"string"* (a name is more than a string), to
   *"signed/attested"* (a name is not a statement), to *"no distinct naming
   object"* (names are a separate kind, as G2 and R-M-04 say), or to all
   three? The specification already implements SDSI local names, with a name
   target and a naming base kind; does that match what you meant?
4. **P3.** Is a type not a schema, or is "schema" the wrong word for what the
   specification calls a definition (representation, constraints, semantics,
   human-review tags, multilingual descriptions)?
5. **The 5-tuple.** Is the delegation *bit* to integer *depth*, and the *tag* to
   typed *attribute range*, an acceptable change, or part of what narrowed too
   far? (R-M-10 records the first; nothing records the second.)
6. **Order of authority** (§9 step 3): definitions, SPEC, ARCH-0001, or something
   else?
7. **P5.** Held now, not objected to. Reopen with the rest, or leave?
8. **Who owns step 1?** It cannot be done without the sponsor.

---

## 11. Evidence

All paths on `origin/main` at `5b2e1bf` unless noted.

- `design-log/0002-arch-0002-cycle/review.md` — P2 and P4 were model proposals
  the human overruled; P3 and P4 additions by the human; the model's error
  pattern.
- `design-log/0021-sponsor-delegation-w1-close/` — the delegation, its exclusion
  of `ADR-0002`, "no written confirmation".
- `design-log/0024-adr-0002-accept/` — the acceptance; the decision maker was
  the P5.1/P5.2 author.
- `git show 2a79b1f:artifacts/docs/ARCH-0001-authorization-attestation.md` §4 —
  the v0.1.0 model (five kinds, `delegate: bool`, `Validity`, `Group`).
- `spec/ARCH-0001-authorization-attestation.md` §1, §2.1, §3.1, §4.1–§4.3,
  §5.1 (R-M-03, R-M-04, R-M-06, R-M-09, R-M-10), §5.5.
- `spec/ARCH-0002-key-relative-naming.md` P1–P7, the "reduction" note.
- `spec/ADR-0002`…`ADR-0008`; `spec/SPEC-0001` §1.2, §2; `SPEC-0002` §7.1–§7.3,
  §8.1, §8.5–§8.7; `SPEC-0003` §5.4, §6.4; `SPEC-0004` §5.2, §6.3, §6.4, §7.1;
  `SPEC-0005`.
- `prototype/wallet/engine/reduce.py` (module docstring), `names.py`,
  `definition.py`, `schema.py`, `check.py`.
- `spec/vectors/ksa-core/vectors.json` — 47 positive, 13 negative,
  13 `evaluations`, 10 `resolutions`, 3 `name_evaluations`, 9
  `threshold_evaluations`.
- `project/GLOSSARY-0001.md`, `project/PLAN-0001-project-plan.md` §0, §1.
- Term counts in §5 come from `grep -o -i -w` over the eight ARCH/SPEC files and
  are indicative, not exact.
