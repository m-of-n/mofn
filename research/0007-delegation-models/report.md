---
schema: "archdoc/v1"
id: R-0007
title: "Who May Speak for foo.com: Delegation and Trust in X.509, S/MIME, OpenPGP and SDSI/SPKI"
short_title: "Delegation models"
description: "One email-delegation case (UC-5: Dave trusts Alice for foo.com, Alice delegates eng.foo.com to Bob, Bob attests Carol) written out in each of X.509/PKIX, S/MIME, OpenPGP, SDSI and SPKI, with both must-fail cases, then the five questions of library#14 answered against the primary sources. Evidence only — it decides nothing."
type: research
category: security
status: draft
version: "0.1.0"
date: "2026-10-26"
updated: "2026-10-26"
needs_review: true
reviewed: false
canonical_path: research/0007-delegation-models/report.md
companion:
  - research/0001-signatures-and-attestation/report.md
  - research/0002-wallets/report.md
  - research/0006-mechanism/report.md
informs: [ARCH-0001, SPEC-0003, SPEC-0004, UC-0001]
open_decisions: [DEC-004]
backlog: L-040
closes: "m-of-n/library#14"
library_pin: "library@f15fd76 + library PR for #14 (rfc-8550, sdsi-1-1 to the summary bar)"
---

# Who May Speak for foo.com
## Delegation and trust in X.509, S/MIME, OpenPGP and SDSI/SPKI

**Status: first draft. It closes library#14 as a research task and decides
nothing.** Its recommendations (§8) are proposals against ARCH-0001, SPEC-0003,
SPEC-0004 and UC-0001, offered for review.

Bibliography pinned at **`library@f15fd76`**, plus two records brought to the
summary bar for this report in the library PR that closes #14: `[@rfc-8550]`
and `[@sdsi-1-1]`. Citation keys `[@record-id]` resolve to records at that
state. Section locators (§) refer to the cited source. Every verbatim quotation
below was checked against the digest-verified source text in the library's
`.cache/`. `sources.md` lists what was read, `searches.md` lists what was
fetched, and `unverified.md` holds the claims that are **not stated as fact
below**.

This report builds on three earlier reports and does not repeat them. R-001
§4–§5 covers X.509's history, the name-constraint measurement and OpenPGP's
collapse. R-001 §9 covers capability systems. R-0002 §5.3 covers trust
signatures in wallets. Where this report corrects one of them, it says so (§7).

---

## Abstract

The sponsor's observation that started library#14 was this: *email address
assertions are already supported by X.509, S/MIME, PGP and SDSI/SPKI; the
difference is in delegation and trust models.* This report tests that
observation with one case, the project's own UC-5, written in each system's
syntax.

Three findings drive the report.

**1. Every system tested can scope a delegate to `foo.com`, except S/MIME.**
- X.509 does it with `nameConstraints`.
- OpenPGP does it with a regular expression on a trust signature.
- SPKI does it with tag intersection.
- SDSI does it by name chaining.
- S/MIME is not a fifth model. It is X.509 with a mail profile, and RFC 8550
  never mentions name constraints.

**2. The systems differ in three ways the issue's table did not ask about:**
- **What is scoped.** X.509 and OpenPGP scope *which names a delegate may
  certify*. SPKI and ours scope *what a delegate may say*. SDSI scopes nothing:
  a binding hands over the whole subtree.
- **Whether scope narrows along the whole chain.** X.509 (§6.1.4(g)) and SPKI
  (§6.3) intersect at every hop. OpenPGP defines no rule for combining scopes
  along a chain. The reference implementation, GnuPG, keeps one regular
  expression per key, and a newer trust signature *replaces* it rather than
  intersecting with it. On a reading of its source (`unverified.md` §1, not yet
  run), the relying party's scope reaches one hop and no further. Alice can
  widen Bob, and GnuPG will not notice.
- **Whether the relying party's own scope is in the format.** In X.509 it is an
  optional input to path validation (§6.1.1(h)), which conforming
  implementations "are not required to support". In OpenPGP it is a trust
  signature the relying party makes itself. In SPKI it is an unsigned ACL entry.
  In ours it is an anchor with an `about` range.

**3. The project's own claim survives in a narrower form.** "Scoped delegation
with a decentralised tagging language is poorly served by all of these" is
**false as stated** for SPKI. SPKI already had exactly that. What survives:
- Of the *deployed* systems, none scopes delegation by what may be said.
- The one deployed system that scopes by name and lets anyone delegate
  (OpenPGP) does not narrow scope along a chain in its main implementation.
- The system that had the right algebra (SPKI) never published a wire format.

The report also found a defect in our own spec: under SPEC-0003 §6.3's own
algebra, UC-5's expected answer is wrong (§2.2).

---

## 1. Question and method

### 1.1 What library#14 asks

The issue asks for a table: *how is authority delegated, where does trust
start, can delegation be scoped*, for X.509/PKIX, S/MIME, OpenPGP and
SDSI/SPKI, against ours. It then asks five questions:
1. range restriction, and whether anyone uses X.509 name constraints;
2. whether the delegation is a different object type from the assertion;
3. who decides the root;
4. what revocation is, and whether anyone runs it;
5. where each system breaks down for a group self-organising around `foo.com`
   with no external CA.

It sets the bar: the claim *"is only worth making if the comparison is
honest — including where X.509 name constraints or PGP trust signatures
already do most of it."*

### 1.2 Method

1. **One case, every system.** UC-5 (`spec/UC-0001` §UC-5) is written out in
   each system's own syntax, with its two must-fail cases. A system that cannot
   reject a must-fail case is reported as such. "Cannot express" is reserved for
   a case the format has no syntax for.
2. **Primary sources only, read in full where they bear.** Six records are at
   FX-1 `profile: full` in the library: `[@rfc-2692]`, `[@rfc-2693]`,
   `[@rfc-5280]`, `[@rfc-8551]`, `[@rfc-9580]` and `[@rfc-9804]`. Two were
   brought to the summary bar for this report: `[@rfc-8550]` (S/MIME
   certificate handling, where S/MIME's trust rules actually are) and
   `[@sdsi-1-1]`. The SPKI wire syntax comes from
   `[@draft-ietf-spki-cert-structure]`, which expired and was never published.
3. **Implementation behaviour comes from code, labelled as such.** GnuPG is the
   only implementation whose behaviour this report states, and it is stated
   from its source at a recorded digest (`sources.md` §3). The source was read,
   not executed. `unverified.md` §1 records the experiment that would settle it,
   and the script is in `experiments/`.
4. **The library's `delegation-models` topic answer is the starting
   hypothesis, not the conclusion.** Where this report departs from it, it says
   so (§7.3).

---

## 2. The case

### 2.1 UC-5, as written

From `spec/UC-0001` §UC-5:

- **Personas.** Alice is trusted for the domain. Bob runs `eng.foo.com`. Carol
  is the claim subject. Dave is the relying party.
- **Precondition.** Dave's context *mail* anchors Alice about
  `mailbox ∈ [*@foo.com]`, depth 1.
- **Flow.** *Alice says trust Bob about mailbox ∈ [\*@eng.foo.com]*, then
  *Bob says key(Carol) has mailbox = carol@eng.foo.com*.
- **Expected.** **yes**.
- **Must fail.** Bob attesting `carol@bar.com` gives `no-path`. Alice
  delegating `*@bar.com` gives `widening`.

### 2.2 A defect in our own case: `*@foo.com` does not contain `eng.foo.com`

SPEC-0003 §6.3 defines an email pattern as `*@` followed by a dns-name pattern.
It states that *"`*@foo.com` matches every address at `foo.com`; `*@*.foo.com`
every address at any name below `foo.com`"*. §6.1 says a plain name *"matches
only that name"* and that `*.foo.com` does not match `foo.com`.

So under SPEC-0003's own algebra:

- `*@eng.foo.com` is **not within** `*@foo.com`. `carol@eng.foo.com` is not
  matched by `*@foo.com`.
- Under SPEC-0004 §6.3 item 4, Alice's trust statement to Bob fails the
  *within* test. The path is not followed, and UC-5's expected **yes** is in
  fact **no**.
- SPEC-0003 §6.3's own closing sentence, *"a domain owner trusted about
  `*@foo.com` may delegate `*@eng.foo.com`"*, contradicts the rule two
  sentences above it.

Under SPEC-0003, the anchor that means what UC-5 intends is
`[*@*.foo.com, *@foo.com]`, sorted bytewise as §6 requires.

This is the same trap RFC 5280 documents. In §4.2.1.10, the constraint
`"example.com"` *"is satisfied by any mail address at the host
"example.com""*, while `".example.com"` *"indicates all the Internet mail
addresses in the domain "example.com", but not Internet mail addresses on the
host "example.com""*. PKIX needs two subtrees for "foo.com and everything
under it", and so do we. RFC 5280 says so in the text. SPEC-0003 says the
opposite in its own example. The fix is proposed in §8 (P1).

**The rest of this report reads UC-5 as intended:** Dave trusts Alice for
`foo.com` and every name below it.

---

## 3. The case in each system

### 3.1 X.509 / PKIX — `[@rfc-5280]`

**Dave's anchor.** Dave configures Alice's public key as a trust anchor. RFC
5280 does not say how: *"The selection of a trust anchor is a matter of
policy"* (§6). There are three places Dave's `foo.com` scope could live:

1. **As path-validation input.** §6.1.1(h) defines `initial-permitted-subtrees`:
   *"a set of subtrees within which all subject names in every certificate in
   the certification path MUST fall"*. This is exactly Dave's scope, in-format.
   But it has two limits:
   - It is an input to *one validation run*, not a property of the anchor.
   - §6.1.1 closes: *"Conforming implementations are not required to support
     the setting of all of these inputs."*
2. **As name constraints in Alice's self-signed certificate.** §6.2 makes these
   advisory: implementations *"are free to process or ignore such
   information"*.
3. **As a trust-anchor constraint under RFC 5937** (Informational).

**Alice → Bob: a CA certificate.**

```
subject:             CN=Bob, O=foo.com eng
subjectPublicKeyInfo: <Bob's key>
basicConstraints:    critical, cA=TRUE, pathLenConstraint=0
keyUsage:            critical, keyCertSign, cRLSign
nameConstraints:     critical,
                     permitted: rfc822Name "eng.foo.com",
                                rfc822Name ".eng.foo.com"
                     excluded:  dNSName "" , iPAddress 0.0.0.0/0, ::/0, ...
```

- `pathLenConstraint=0` is X.509's depth control: no further CA may follow Bob
  (§4.2.1.9).
- The rfc822Name pair is the host-plus-subdomains split of §4.2.1.10.
- The exclusions are necessary, not decorative. Constraints *"apply only when
  the specified name form is present"*. Without them Bob can certify any DNS
  name, IP address or URI, and *"using the nameConstraints extension to
  constrain one name form ... offers no protection against use of other name
  forms"* (§8, Security Considerations).

**Bob → Carol: an end-entity certificate.** `subjectAltName: rfc822Name
carol@eng.foo.com`, `extKeyUsage: emailProtection`. RFC 5280 requires new
certificates to carry the address in `rfc822Name`, with the DN's
`emailAddress` attribute *"deprecated but permitted"* (§4.1.2.6).

**Must-fail cases.**

- **Bob certifies `carol@bar.com`: rejected.** The address is outside
  `permitted_subtrees` (§6.1.3(b)).
- **Alice widens Bob to `bar.com`: the widening certificate is accepted, but
  everything issued under it is rejected.** §6.1.4(g) *intersects* each
  certificate's permitted subtrees into the running state. Two cases:
  - If Dave supplied `initial-permitted-subtrees`, or Alice's own constraint
    sits in a certificate on the path, then `{foo.com, .foo.com} ∩ {bar.com}`
    is empty for rfc822Name. Every address Bob certifies then fails.
  - If Dave's scope lives *only* in a self-signed anchor that his library
    ignores (§6.2), there is nothing to intersect with, and `carol@bar.com`
    **validates**.

So X.509 rejects the widening case only if the relying party's scope reaches
the algorithm. The format allows that; it does not require it.

**What Bob may say.** Inside `eng.foo.com`, Bob is unrestricted. He can certify
any key for any purpose, and for any other name form not excluded.
`extKeyUsage` in a CA certificate is not processed by RFC 5280 path
validation, and the policy tree (§6.1.3(d)) constrains *policies*, not
statements.

### 3.2 S/MIME — `[@rfc-8551]`, `[@rfc-8550]`

S/MIME's row is X.509's row with a mail profile, and the documents say so:

- RFC 8551 §4: *"This specification does not cover how S/MIME agents handle
  certificates -- only what they do after a certificate has been validated or
  rejected."*
- RFC 8550 §4.2: *"Certificate, CRL, and path validation MUST be performed as
  per [RFC5280] when validating a correspondent's public key."*

RFC 8550 adds only rules about what an end-entity certificate may be used for:
- key usage MUST be critical (§4.4.2);
- EKU, if present, MUST contain `emailProtection` or `anyExtendedKeyUsage`
  (§4.4.4);
- the address goes in `rfc822Name` (§4.4.3).

**It adds nothing that delegates.** It never mentions name constraints.
Worse, §4.4 says certificates *"issued for the S/MIME environment SHOULD NOT
contain any critical extensions ... other than those listed here"*. Its list
omits name constraints, which RFC 5280 §4.2.1.10 says *"Conforming CAs MUST
mark ... as critical"*. RFC 5280's MUST should win. Still, an S/MIME profile
that reads as discouraging the one PKIX scoping mechanism that would serve
UC-5 is worth stating.

**What S/MIME adds is the last step of UC-5: checking Carol's address against
the message.** RFC 8550 §3: *"Receiving agents MUST check that the address in
the From or Sender header of a mail message matches an Internet mail address
in the signer's certificate, if mail addresses are present in the
certificate."*

The conditional matters. The same section says receivers *"MUST recognize and
accept certificates that contain no email address"*. On a mismatch, the
receiver is told to do *"some explicit alternate processing"*, not to reject.

**Who decides the root** is negative-only. Receivers *"SHOULD NOT simply trust
any self-signed certificates as valid CAs but SHOULD use some other mechanism
to determine if this is a CA that should be trusted"* (§2.3). The other
mechanism is never named.

### 3.3 OpenPGP — `[@rfc-9580]`, GnuPG

**Dave's anchor.** Dave makes a level-2 trust signature on Alice's User ID,
scoped by a regular expression:

```
gpg --quick-tsign-key <Alice-fpr> 2,full,foo.com
```

GnuPG turns the domain into the regex `<[^>]+[@.]foo.com>$`
(`g10/keyedit.c`, `parse_trustsig_string`).

- `[@.]` matches both the host and its subdomains. This is the one place in
  this report where the default covers what UC-5 means.
- The command-line path does **not** escape the `.` in the domain. The
  interactive path (`trustsig_prompt`) does. At evaluation, `sanitize_regexp`
  in `trustdb.c` escapes only `^[$()|*+?{` (`REGEXP_OPERATOR_CHARS`). Its
  comment says *"the only legal regex character is "."*", so `.` stays a
  wildcard, and the match is case-insensitive (`REG_ICASE`).
- **So a command-line trust signature over-matches.** Alice's
  `1,full,eng.foo.com` becomes `<[^>]+[@.]eng.foo.com>$`, which also matches
  `carol@eng-foo.com`, a separately registrable domain. Dave's `foo.com` regex
  likewise matches `@fooxcom`. That one is harmless only because `fooxcom` is
  not a registrable name, and the same holds for any single-label-plus-TLD
  domain. Multi-label domains are exposed. This is a source reading, and is
  in `unverified.md` §2.

On the wire this is RFC 9580 §5.2.3.21 (level 2, amount 120) plus §5.2.3.22.
Level 2 makes Alice a *"meta introducer"*. The Regular Expression subpacket
means *"Only signatures by the target key on User IDs that match the Regular
Expression ... have trust extended"*.

**Alice → Bob: a level-1 trust signature on Bob's User ID**, regex for
`eng.foo.com`. **Bob → Carol: an ordinary (level 0) certification** of
`Carol <carol@eng.foo.com>`.

**Must-fail cases.**

- **Bob certifies `carol@bar.com`: rejected.** Alice's regex is checked against
  the User IDs Bob signs.
- **Alice widens Bob to `bar.com`: RFC 9580 does not say; GnuPG, as read,
  accepts it.**
  - RFC 9580 defines a regex per signature and no rule for combining regexes
    along a chain. Trust computation is entirely the implementation's (§5.10:
    *"The format of Trust packets is defined by a given implementation"*).
  - GnuPG's `validate_one_keyblock` (`g10/trustdb.c`) checks the *signer's*
    recorded regex against the target User ID, then records the *new*
    signature's regex on the target key: *"If the trust sig contains a regexp,
    record it on the pk for the next round"*.
  - So Dave's `foo.com` regex constrains which User IDs **Alice** can make
    valid, including Bob's `bob@eng.foo.com`, which passes. Bob's onward scope
    is then **Alice's** regex alone.
  - If Alice's trust signature on Bob says `bar.com`, Bob can make
    `carol@bar.com` valid for Dave. If it carries no regex, Bob is
    unconstrained.
  - Depth is handled more carefully: the code takes the minimum of the
    signature's depth and the chain's remaining depth.

  This is a source reading, not an executed result (`unverified.md` §1). If it
  holds, **OpenPGP as deployed scopes the first hop and not the chain.**

**What Bob may say.** Only "this User ID belongs to this key". OpenPGP has no
authorization field. The scope is a regex over a display string, not over a
permission (R-001 §5.2, R-0002 §5.3).

**Third axis.** The trust *amount* (partial below 120, complete at 120 and
above) has no composition rule in RFC 9580. GnuPG adds counts on top:
`--completes-needed` 1 and `--marginals-needed` 3 (R-0002 §5.3).

### 3.4 SDSI 1.1 — `[@sdsi-1-1]`

SDSI expresses UC-5 as **name resolution**. SDSI 1.1 gives email addresses a
special mapping: `Bob.Smith@penguin.microsoft.com` *"is equivalent to:
DNS!!'s com's microsoft's penguin's Bob.Smith"* (§2). A local definition of a
suffix takes precedence over the global `DNS!!` root (§5.2).

So, in our construction:

1. Dave binds `foo.com` in his own name space to Alice's key.
2. Alice binds `eng` to Bob.
3. Bob binds `carol` to Carol.
4. `carol@eng.foo.com`, evaluated in Dave's name space, resolves to Carol's
   key.

**Must-fail cases.**

- **Bob binding a `bar.com` name: cannot happen.** Bob can only define names in
  *Bob's* space. `carol@bar.com` resolves through whatever Dave has bound
  `bar.com` to (or through `DNS!!`), never through Bob. "Out of scope" is not
  a check that fails; it is a name that never reaches Bob.
- **Alice "widening" Bob to `bar.com`: not expressible.** Alice owns only
  names under her own key. The structure does the narrowing.

**What SDSI does not have.**

- **No scope within a subtree.** Binding `eng` to Bob gives Bob all of
  `eng.foo.com`, for every purpose.
- **Delegation of authority is a separate object.** SDSI's `Delegation-Cert`
  *"gives the delegee the authority to sign statements of certain types on
  behalf of the delegator"* (§2). Its template matches by the same structural
  rule as a Get template (§6.4), with no wildcards or ranges. So a delegation
  "for `*@eng.foo.com`" cannot be written.
- **Groups have no key.** *"No principal is authorized to speak for the
  group"* (§7).
- **`DNS!!` is a shared root.** It *"may not be re-defined"* (§5.2), and SDSI
  relies on DNS security *"which is soon to appear, we presume"* (§5.2).
  RFC 2693, which absorbed SDSI's names (§2.6), has no `!!` roots at all.

### 3.5 SPKI — `[@rfc-2693]`, `[@draft-ietf-spki-cert-structure]`

SPKI expresses UC-5 as **authorization**. An address is not a name SPKI knows
about. It is something an application encodes in a tag.

SPKI's wildcards (§6.3.1) are `(*)`, `(* set …)`, `(* prefix <byte-string>)`
and `(* range …)`. There is **no suffix form**, so `*@foo.com` cannot be
written as a string pattern. The encoding that works uses list-prefix
semantics: *"If one list is longer than the other but match at all elements
where both lists have elements, then the longer list is the result of the
intersection"* (§6.3.1). Domain labels are written root-first, as SDSI did:

```
(acl (entry (hash sha256 |Alice…|) (propagate)
            (tag (mailbox com foo))))                      ; Dave's ACL, unsigned

(cert (issuer (hash sha256 |Alice…|))
      (subject (hash sha256 |Bob…|))
      (propagate)
      (tag (mailbox com foo eng)))                         ; Alice → Bob

(cert (issuer (hash sha256 |Bob…|))
      (subject (hash sha256 |Carol…|))
      (tag (mailbox com foo eng (local carol))))           ; Bob → Carol, no propagate
```

Reduction (§6.3) chains these into one 5-tuple
`<Self, Carol, false, (mailbox com foo eng (local carol)), V>`.

**Must-fail cases.**

- **Bob issues `(mailbox com bar …)`: rejected.** `AIntersect` with
  `(mailbox com foo …)` is empty.
- **Alice widens Bob to `(mailbox com bar)`: rejected the same way.** Any
  widening is intersected away at reduction, because the ACL's tag is in
  every reduction.

**Notes.**

- `(mailbox com foo)` covers both the host and its subdomains. The tag cannot
  say "host only", because SPKI has no exclusion form.
- The meaning of the tag is entirely the application's (§6.3.1, *"Special
  semantics would require special reduction software"*).
- **SPKI is the only system here that scopes what a delegate may *say*.** A
  `(mailbox …)` tag and a `(code-signing …)` tag are different authorizations,
  and Bob holding one gives him nothing in the other.
- Depth is a boolean (`propagate`). SPKI considered integer depth and rejected
  it (§4.1.4).

### 3.6 Ours — ARCH-0001, SPEC-0003, SPEC-0004

- **Dave's anchor** is a local, unsigned anchor: `trusts: Alice`,
  `about: mailbox ∈ [*@*.foo.com, *@foo.com]`, `may-delegate: {depth: 1}`
  (SPEC-0004 §4.2; ranges corrected per §2.2).
- **Alice → Bob** is a *trust* statement about `mailbox`.
- **Bob → Carol** is an *attestation* of `mailbox = carol@eng.foo.com`.
- **Must-fail cases.** SPEC-0004 §6.3 rejects both, by the *within* test
  (item 4) and the non-widening test (item 6). It says so: *"Widening fails the
  path."*

**What differs from SPKI is not the algebra.** It is four things:

1. **Ranges are typed.** The base kinds of SPEC-0003 §6 (`email`, `dns-name`,
   `ip-prefix`, …) have a defined *within*, so the verifier knows what
   `*@eng.foo.com` means. SPKI leaves that to the application.
2. **A widening is reported as `widening`,** not intersected silently to empty.
3. **Depth is an integer** (`deleg.depth`, SPEC-0004 §6.3).
4. **The trust statement and the attestation are different types.** UC-5:
   `trust` about `mailbox` *"is not an attestation of a `mailbox`, and holding
   one never implies the other"* (emphasis on "of" in the original dropped).

Point 3 is not what ARCH-0001 R-M-10 says (§7.3).

---

## 4. The table

The issue's table, filled in, with three columns it did not ask for. "RP" is
the relying party (Dave).

| | how is authority delegated? | where does trust start? | can delegation be scoped? | scope is over | narrows along the chain? | RP's own scope in-format? | delegation is a separate object? |
|---|---|---|---|---|---|---|---|
| **X.509 / PKIX** | CA certificate: `cA`, `keyCertSign`, `pathLenConstraint` (§4.2.1.9) | a trust anchor chosen as *"a matter of policy"* (§6), in practice a root store | **yes**, `nameConstraints` (§4.2.1.10), fail-open per name form | names a delegate may certify | **yes**, intersect permitted, union excluded (§6.1.4(g)) | optional input `initial-permitted-subtrees` (§6.1.1(h)), support not required | **no**, three fields on the name-binding certificate |
| **S/MIME** | none of its own; RFC 5280 path validation (RFC 8550 §4.2) | the agent's, by "some other mechanism" (RFC 8550 §2.3) | inherits PKIX; never mentions name constraints, and discourages critical extensions it does not list (§4.4) | as PKIX | as PKIX | as PKIX | **no** |
| **OpenPGP** | trust signature, level *n* may issue *n−1*; level 2 is a *"meta introducer"* (§5.2.3.21) | the RP's own keyring and ownertrust; Trust packet format *"defined by a given implementation"* (§5.10) | **yes**, a regex over User IDs (§5.2.3.22) | names a delegate may certify | **not specified**; GnuPG keeps the latest regex per key, so first hop only (§3.3, unverified) | **yes**, the RP's own trust signature | **partly**: a subpacket on a User-ID certification |
| **SDSI 1.1** | name binding (`Cert:`), or a `Delegation-Cert` for signing authority | the verifier's own name space and ACLs, plus shared `!!` roots (§2) | **by position only**: a binding hands over the whole subtree | names, structurally | yes, by construction | yes: the RP's own bindings | **yes**: `Delegation-Cert` is distinct from `Cert:` |
| **SPKI** | 5-tuple with `propagate` (boolean) | an unsigned ACL, *"the source of empowerment"* (§1.1) | **yes**, tag intersection; `prefix`, `range`, `set`, no suffix | what a delegate may say (application-defined) | **yes**, `AIntersect` at every reduction (§6.3) | **yes**: the ACL entry's tag | **yes**: 5-tuple vs 4-tuple, *"qualitatively different"* (§6.2) |
| **ours** | trust statement with `may-delegate` (integer depth) | an unsigned local anchor, or an accepted signed statement (SPEC-0004 §4.3) | **yes**, by typed range | what a delegate may say, with typed ranges | **yes**, and widening is an error (SPEC-0004 §6.3) | **yes**: the anchor's `about` | **yes**: `trust` ≠ attestation |

---

## 5. The five questions

### 5.1 Can delegation be restricted to a range of names? Does anyone use X.509 name constraints?

**Yes, in four of the five, and the mechanisms are real.**

- X.509's is the best specified. It has a monotone intersection rule (§6.1.4(g))
  and precise mailbox, host and domain forms (§4.2.1.10).
- Its weaknesses are documented in R-001 §4.4: fail-open per name form, and new
  name forms escape old constraints, as with RFC 9598's `SmtpUTF8Mailbox`.

**Use: almost none, measured.** R-001 §4.5's measurement of Mozilla's CCADB
on 2026-09-26 found:
- **31 of 1,769** disclosed intermediates carry `nameConstraints`, and only
  **2** of those are marked critical as RFC 5280 requires;
- 29 of the 31 come from one CA family;
- **1 of 172** roots carries a positive Mozilla-applied scope.

That measurement covers the public Web PKI only. Enterprise PKI is not
measured (R-001 `unverified.md` item 1). Implementations kept failing at it:
five Go `crypto/x509` CVEs in eleven months, and OpenSSL's 2022 overflows in
the email-constraint code (R-001 §4.5).

The `delegation-models` topic recorded "nobody uses name constraints" as
supported only by secondary sources. **The library already held an original
measurement** (`[@survey-2026-nameconstraints-measurement]`, R-001's), so that
gap is closed for the Web PKI. The record itself is still a stub.

OpenPGP: no study measures how many keys carry trust signatures or regex
scoping (R-001 `unverified.md`, "Adoption rate of OpenPGP trust signatures").
This report found none either.

### 5.2 Is the delegation a different object type from the assertion?

| System | Answer |
|---|---|
| **X.509** | **No.** Delegation is `cA=TRUE` plus `keyCertSign` plus an optional `pathLenConstraint` on the same certificate that binds the CA's own name. There is nothing separate to scope, revoke or audit. ARCH-0001's interchange matrix already says *"Do not treat CA bit as AuthzCert"*. |
| **OpenPGP** | **Partly.** A trust signature is a *subpacket* inside a certification of a User ID. It cannot exist without vouching for a name. R-I-04's escape hatch ("unless an explicit profile says so") exists for exactly this case. |
| **SDSI** | **Yes**, `Delegation-Cert`, though it delegates the right to *sign*, matched by a wildcard-free template. |
| **SPKI** | **Yes, cleanly.** The 5-tuple (authorization) and the 4-tuple (name) are separate intermediate forms because they are *"qualitatively different"* (§6.2). |
| **Ours** | **Yes**, as SPKI, and one step further. The thing delegated (`trust` about a type) and the thing asserted (an attestation of that type) are distinct even when both are about `mailbox`. |

### 5.3 Who decides the root?

**In every system, the relying party, and every standard declines to say
how.**

| System | Source |
|---|---|
| X.509 | *"a matter of policy"*, delivered by *"some trustworthy out-of-band procedure"* (§6, §6.1.1(d)) |
| S/MIME | "some other mechanism" (RFC 8550 §2.3) |
| OpenPGP | a Trust packet whose format is *"defined by a given implementation"* (§5.10) |
| SPKI | an ACL that *"has no Issuer (and is not signed)"* (§1.1) |
| SDSI | the verifier's own name space, plus the `!!` roots *"bound to the same principal in every name space"* by procedures it does *"not try to describe"* (§2) |

**In practice:**
- X.509 and S/MIME roots are an **inherited bundle**: a root program, an OS
  store, or IT policy.
- OpenPGP's is a **keyring the user built**, which, after the 2019 flooding
  attack, mostly means keys fetched from a verifying directory (R-001 §5.2).
- SPKI's and ours are a **policy written down as data**.

The difference that survives is not that our root is unsigned. Every system
except SDSI's `!!` roots has an unsigned local root. **The difference is that
ours is a specified object with a scope** (SPEC-0004 §4.2). The topic answer
said this; this report confirms it.

### 5.4 What is revocation, and does anyone run it?

| System | Mechanism | Run in practice? |
|---|---|---|
| X.509 | CRLs and OCSP. *"this profile does not require the issuance of CRLs"* (§3.3). Status can end `UNDETERMINED` with no rule for what follows (§6.3.3). | Documented collapse, then replacement: soft-fail browsers, CRLSets, OCSP made optional by CA/B SC-063, Let's Encrypt ending OCSP in 2025, RFC 9608's `noRevAvail`, CRLite (R-001 §4.6). |
| S/MIME | *"All agents MUST perform revocation status checking in accordance with [RFC5280]"* (RFC 8550 §4.1), CRLs only. Every freshness rule is a SHOULD. *"The value of the CRL information in a particular context is beyond the scope of this specification but may be governed by the policies associated with particular certification paths."* | Not measured by any source the library holds. |
| OpenPGP | Self-revocation signatures. Delegated revocation (Revocation Key) is now *"deprecated. Applications MUST NOT generate such a subpacket"* (§5.2.3.23). It is replaced by **escrowed revocation** (§13.9): Alice pre-signs her own revocation and hands it to a holder. | The RFC's own reason is a deployment verdict: support for the old mechanism *"is uneven and unreliable"* (§13.9). |
| SPKI | Timed CRLs and revalidations under three rules (§5.2): the certificate names the CRL key, CRLs carry dates, and *"CRL validity date ranges must not intersect"*. This yields *"a deterministic validity computation"*. | Never deployed. |
| SDSI | No CRLs: *"signatures may be designated as needing periodic reconfirmation"* (§6.2). Key compromise is a hot-list group. | Never deployed. |
| Ours | A `revoke` statement by the original speaker, permanent, decided with whatever revocations the evaluator holds. Answers MUST state how many were considered, and short validity is RECOMMENDED (SPEC-0004 §7.1). | — |

**Two findings for us.**

1. SPEC-0004 §7.1 is the "wandering anti-matter" model SPKI ruled out
   (RFC 2693 §5.1, *"this process is non-deterministic"*). SPEC-0004 knows
   this and mitigates it by *reporting* the count rather than by SPKI's
   non-overlap rule. That is a defensible choice, but it should be recorded as
   a choice (§8, P4).
2. **Escrowed revocation (RFC 9580 §13.9)** needs nothing new in our model. It
   is a `revoke` statement signed in advance and held by someone else. The
   keyholder can *"constrain what types of revocation the preferred revoker
   can issue, by only escrowing those specific signatures"*. It is the most
   directly reusable mechanism in this comparison (§8, P5).

### 5.5 Where does each break down for a group self-organising around `foo.com` with no external CA?

Assume: the group controls `foo.com`'s DNS and mail, has no relationship with
a public CA, and its members' relying parties are each other plus outsiders
who want to check `carol@eng.foo.com`.

- **X.509/S/MIME breaks at distribution, not expressiveness.**
  - The group can run a private CA with `nameConstraints` and get UC-5 exactly
    right.
  - But every outside relying party must install the group's root.
  - Most mail clients give that root *every* name, because they ignore
    self-signed-certificate constraints (§6.2) and few expose §6.1.1(h).
  - So the group asks outsiders to trust it for the whole internet in order to
    trust it for `foo.com`. That is the same "1 of N" exposure R-001 §4.8
    describes for public CAs.
- **OpenPGP breaks at chain scope and at distribution.**
  - Inside the group, trust signatures with domain regexes work for one hop.
  - Beyond that, as read, a sub-delegate's scope is whatever its delegator
    wrote, not what the relying party granted (§3.3).
  - Outsiders have no discovery mechanism for the group's trust signatures:
    keys.openpgp.org does not publish third-party certifications (R-001 §5.2).
  - A command-line domain scope over-matches look-alike multi-label domains
    (§3.3).
- **SDSI breaks at `DNS!!`.** The group's names are reachable to outsiders only
  through the shared `DNS!!` root or a local binding each outsider must make.
  SDSI 1.1 assumed DNS security *"soon to appear"*. Within a subtree, nothing
  is scoped.
- **SPKI breaks at interoperability.** It has the algebra but no published wire
  format (the structure draft expired), no email tag profile and no deployed
  verifier. The group would be writing its own.
- **Ours** inherits SPKI's position and adds typed ranges and a wire format. It
  breaks where every system does: an outsider must still decide to anchor
  Alice. SPEC-0004 §4.4 makes that an explicit, rendered decision rather than
  an inherited bundle, which is the most a format can do.

---

## 6. The discriminators, stated plainly

1. **What scope ranges over.** In X.509 and OpenPGP it is names a delegate may
   certify. In SPKI and ours it is what a delegate may assert. In SDSI it is
   position in a name tree. Only SPKI and ours can say "Bob may speak about
   *mailboxes* in `eng.foo.com`, and about nothing else".
2. **Whether scope is monotone along the chain.** X.509, SPKI, SDSI and ours:
   yes. OpenPGP: unspecified, and per GnuPG's source, no.
3. **Whether the relying party's scope is part of the format.** In X.509 it is
   optional and per-call. In OpenPGP, SPKI, SDSI and ours it is first-class.
4. **Whether widening is detected or silently absorbed.** X.509 and SPKI absorb
   it into an empty intersection. Ours reports it.
5. **Whether delegation is a distinct object.** SPKI, SDSI and ours: yes.
   OpenPGP: as a subpacket. X.509: no.

Scoping by itself is not a discriminator. The issue's table column "can
delegation be scoped?" has the answer *yes* in every row except S/MIME.

---

## 7. The project's claim, tested

### 7.1 What is withdrawn

- **The framing "ours can scope and theirs cannot"**, which the topic answer
  already warned against. False. X.509, OpenPGP and SPKI all scope. X.509's
  mail scoping is more precise than our current spec (§2.2).
- **The framing "ours is different because the root is unsigned"**, which the
  topic answer asked #14 to retire. Every system has an unsigned local root
  (§5.3).
- **library#14's own claim, that scoped delegation with a decentralised
  tagging language is "poorly served by all of these"**, as a claim about
  everything compared. It is false for SPKI, which is exactly that.

### 7.2 What survives

- Of the *deployed* systems, **none scopes delegation by what may be said**.
  X.509 and OpenPGP scope only which names may be certified.
- Of the deployed systems that let anyone delegate without a CA (OpenPGP),
  **the reference implementation does not narrow scope along a chain** (as
  read; `unverified.md` §1).
- **The system that had the right algebra never shipped a wire format.** SPKI
  standardised its rationale (RFC 2692, RFC 2693, both Experimental) and its
  S-expression encoding 26 years later (RFC 9804), but never its certificates.
- **Typed ranges are new.** SPKI's tags are untyped byte strings and lists,
  whose meaning is the application's. SPEC-0003's base kinds give the verifier
  the *within* relation for email, DNS names and IP prefixes. That makes
  "widening" detectable and reportable rather than an empty intersection.

**The honest one-line version:** *SPKI's model, with typed ranges and a wire
format, for a domain where the deployed systems scope only names.*

### 7.3 Where this report departs from the library's `delegation-models` topic answer and from R-001

1. **R-001 §4.3** says RFC 5280's algorithm *"has no channel for the relying
   party's own scoping of a trust anchor"*. That is too strong. §6.1.1(h)/(i)
   is exactly such a channel. It is per-validation, not per-anchor, and support
   is optional. R-001's conclusion that relying-party scoping is not reliably
   available survives; the sentence does not. The error is in our wording,
   not in the RFC.
2. **The topic answer** cites `dev.gnupg.org` T6238 (*the domain restriction
   fails for a key with only an email address*). Current GnuPG `trustdb.c`
   `check_regexp` explicitly wraps a bare mailbox in angle brackets before
   matching, with a comment describing that exact case. As of the source read,
   the defect is fixed upstream. The version that fixed it was not established.
3. **The topic answer** says ARCH-0001's R-M-10 boolean is *"a choice this
   project has inherited"*. SPEC-0004 §6.3 has since moved to **integer**
   depth. So the spec now sides with X.509 and OpenPGP against SPKI §4.1.4,
   while ARCH-0001 R-M-10 still reads *"Delegation SHALL be an explicit
   boolean (or equivalent)"*. Whether an integer depth is "equivalent" is
   exactly what is in question. The text should say, and the choice should
   cite SPKI's reason for rejecting integers (§8, P3).
4. **The topic answer** treats "nobody uses name constraints" as resting on
   secondary sources. R-001 §4.5 is a primary measurement (§5.1).

---

## 8. Proposals (for review; nothing here is decided)

| # | Proposal | Against | Why |
|---|---|---|---|
| **P1** | Fix UC-5 and SPEC-0003 §6.3: Dave's anchor is `[*@*.foo.com, *@foo.com]`, Alice delegates `[*@*.eng.foo.com, *@eng.foo.com]` (or just `*@eng.foo.com` if only the host is meant), and §6.3's closing sentence is corrected. Add a vector in which `*@eng.foo.com` under `*@foo.com` is **`widening`**. | SPEC-0003, UC-0001, `spec/vectors` | §2.2: the case's expected answer contradicts the algebra. RFC 5280 §4.2.1.10 shows the host/domain split is a known trap. |
| **P2** | State, in SPEC-0004 §6.3, that scope narrowing is checked against the *whole* path, not only the previous hop, and add a vector for "Alice widens Bob, Bob attests in the widened range". | SPEC-0004 | §3.3: the deployed system that lets anyone delegate fails exactly this case. SPEC-0004 §6.3 item 4 checks `s.about` against the current `scope`, which already carries the narrowing. A vector would make that a guarantee rather than a reading. |
| **P3** | Reconcile ARCH-0001 R-M-10 (boolean) with SPEC-0004 (integer depth), and cite RFC 2693 §4.1.3–§4.1.4 for whichever is chosen. | ARCH-0001 | §7.3 item 3. |
| **P4** | Record in SPEC-0004 §7.1 that revocation is non-deterministic in SPKI's sense, and why the count-reporting mitigation was preferred over RFC 2693 §5.2's non-overlap rule. | SPEC-0004 | §5.4 |
| **P5** | Name escrowed revocation (RFC 9580 §13.9) as a supported pattern: a `revoke` signed in advance and held by a third party. | SPEC-0004 §7, R-O-02 | §5.4: it needs no new object, and it is the one revocation mechanism here whose change was motivated by deployment experience. |
| **P6** | Write the X.509 import mapping (R-I-01, R-I-05) to carry `nameConstraints` across as a *name-only* scope, never as a range over a typed attribute. Treat a CA certificate without `nameConstraints` as unscoped. | ARCH-0001 §6 | §3.1: a PKIX CA's scope is over names it may certify. Importing it as a `mailbox` trust range would grant Bob more (every purpose) than the PKIX chain did. |

---

## 9. Limits

- **GnuPG behaviour is read from source, not executed** (`unverified.md` §1).
  The chain-scoping finding is the strongest new claim in this report and the
  one most in need of the experiment in `experiments/`.
- **Other OpenPGP implementations were not examined.** Sequoia, RNP and
  OpenPGP.js may compose regexes differently. RFC 9580 permits any choice.
- **No X.509 library was tested** for §6.1.1(h) support. The report says only
  that RFC 5280 does not require it.
- **SDSI's renderings are our construction.** SDSI 1.1 has no email-delegation
  example. The SPKI tag `(mailbox com foo …)` is likewise ours: neither RFC
  2693 nor the structure draft defines an email tag.
- **S/MIME deployment** (which clients enforce RFC 8550 §3's From-address
  check, or any name constraint) is not measured by any source the library
  holds.
- **Supporting records.** Several records cited through R-001 are still stubs
  (library#45), including the measurement record itself. This report cites
  R-001 for those facts rather than the stubs.
