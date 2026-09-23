---
schema: "archdoc/v1"
id: APP-0001
title: "The application — what we are actually building for the demo"
short_title: "Application design"
description: "What the demo application does, its commands, and what a user sees. The gap PROC-0004 §6 left: it specified packaging for a thing whose behaviour was undefined."
type: design
category: product
status: draft
version: "0.2.0"
version_policy: "semver; MINOR = command or behaviour added"
date: "2026-09-22"
updated: "2026-09-22"
decision_makers: []
reviewers: []
needs_review: true
reviewed: false
canonical_path: project/APP-0001-application-design.md
companion:
  - project/PROC-0004-community-launch.md
defers_to: ARCH-0001
backlog: D8
---

# The application

**Status: draft.** Written because the honest answer to *"have we planned the
application?"* was **no**. `PROC-0004` §6 lists packaging, checksums, signing
and app notes — six checkboxes about shipping a thing whose *behaviour* was
never specified.

---

## 0. Correction — 2026-09-23

v0.1 said *"a CLI and not a GUI"* and argued that a GUI would obscure whether a
rendered sentence came from the vocabulary or from the programmer. **The sponsor
has since specified a graphic UI for two specific applications, in October.**
That supersedes the argument, and the argument was wrong anyway: the way to show
a rendering came from the vocabulary is to **render two unrelated domains through
one UI** — which a GUI demonstrates more convincingly than a terminal does.

v0.2 therefore specifies **a wallet application with a graphic UI**, with the CLI
retained as the scriptable surface underneath it.

## 1. What it is

**A wallet.** It holds keys, trust roots and statements; it makes attestations;
and it evaluates a set of statements to decide whether to believe a claim.

| surface | for |
|---|---|
| **graphic UI** | the two use-case applications. October |
| **CLI** | the same operations, scriptable. Already prototyped |
| **library** | the reduction and encoding underneath both |

**Why "wallet" rather than "tool":** the noun matters because it names what the
user actually has — a set of keys and a set of things other people have said,
which they carry and present. `PROC-0004` and `PLAN-0001` both under-specified
this, and the sponsor flagged it as missing on 2026-09-22.

## 2. What a wallet does

| | |
|---|---|
| **hold** | keys, and **trust roots** — *"I trust Pa for email in `*@foo.com`"* |
| **collect** | statements others have made, including ones about you |
| **make** | attestations, and delegations |
| **present** | the set of statements a relying party needs to believe a claim |
| **evaluate** | reduce a presented set against your own roots, and say why |

**Trust roots are the part that is easy to miss.** They are unsigned — nobody
said them *to* you, you decided them. That is the fixed floor: if a key could
define its own trustworthiness there would be no floor at all, and it is why
ARCH-0001's `AclEntry` has no speaker.

## 3. Commands

```sh
# domains of discourse — the PICS-like layer
mofn domain init   supply-chain --key paul.key
mofn domain add-type supply-chain build-provenance \
       --value reproducible:"built reproducibly from published sources" \
       --value attested:"built by an attested pipeline" \
       --value unverified:"origin not verified"
mofn domain id     supply-chain          # the hash that identifies the SET

# statements
mofn make  --key tool.key --subject dist/app.pyz \
           --type paul:build-provenance --claim reproducible   > prov.stmt
mofn make  --key paul.key --subject-key david.pub \
           --type paul:name --claim david                      > name.stmt
mofn make  --key paul.key --subject-key david.pub \
           --type paul:may-speak \
           --domain supply-chain --topic build-provenance      > deleg.stmt

# checking and reading
mofn check  prov.stmt --domain supply-chain
mofn render prov.stmt --lang es
mofn reduce deleg.stmt prov.stmt --ask "may david attest build-provenance?"
```

## 4. What a user sees — the verdict

`check` prints the six dimensions of `R-O-06`, separately, and then says what it
does **not** prove.

```
statement  prov.stmt
  integrity      ok    subject digest re-derives
  authenticity   ok    signature valid under key 9f2a…
  names          ok    no name chain to resolve
  authorization  FAIL  tool.key is not entitled to assert
                       paul:build-provenance about this subject
  acceptance     —     not evaluated: authorization failed
  semantics      ok    domain 2104d6d4… resolved, value in range

  "The artifact sha256:8e1c… was built reproducibly from published sources."
  — asserted by key 9f2a…, which has no standing to say so.

  This proves origin and integrity. It does not prove truth.
```

**The `authorization` line is the product.** Everything else is available
elsewhere; a valid signature from a key with no standing to make the claim is
the distinction nothing mainstream surfaces.

## 5. What it deliberately does not do

- **No key management.** Keys are files. No agent, no keychain, no rotation.
- **No network.** No fetching domains, no transparency log, no registry. A
  domain is a file you already have.
- **No revocation.** Short validity or nothing.
- **No GUI, no web UI, no server.**
- **No cryptographic primitives of our own** — a vetted library, always.

## 6. Relationship to the demo floor

**They are the same deliverable, and that is the useful finding.**

`PLAN-0001` §9's I3 floor is name resolution, reduction, thresholds and a
multi-dimensional verdict. That *is* `reduce` plus `check`. The application is
not additional work after the floor — **it is the floor, with a CLI on it.**

| demo moment | command |
|---|---|
| show a statement, read it aloud | `render` |
| verify — six dimensions green | `check` |
| tamper, the verifier names the break | `check` |
| valid but **unauthorized** key | `check` + `reduce` |
| different subject type, same code path | `render` with a second domain |

**Consequence:** D8 should not be scheduled after D6. Packaging is the only
part that is genuinely later.

## 7. What exists already

`prototype/statements/` — statement creation, reduced-CBOR encoding, signing
shape, subject modes, domains, hash-identification, range checking, multilingual
rendering, **and now reduction**.

`demo_email.py` runs the sponsor's Alice/Bob/Carol/Dave example end to end,
including the three cases that must fail. **Reduction is no longer the gap.**

## 8. The gap now

**The graphic UI, and the two use-case applications it serves.** October work,
and nothing exists for it.

Also missing: signature checking inside reduction (`reduce.py` takes statements
as given), revocation, validity windows, thresholds, and a real range language
in place of globs.

## 9. Build order

| | | why |
|---|---|---|
| 1 | ~~reduce~~ | **done** — `reduce.py`, with the email example |
| 2 | **the two use cases** | they determine what the UI must show |
| 3 | **graphic UI** | October |
| 4 | signature checking into reduction | reduction currently trusts its inputs |
| 5 | packaging | genuinely last |

**The use cases come before the UI**, not after: a UI built before knowing what
it presents ends up presenting the data model, which is exactly the failure the
PICS-like layer exists to avoid.

## 9. Open questions

1. **Is `mofn` the command name?** It matches the repo; it says nothing about
   what the tool does.
2. **Does `check` take `--domain` as a file, or resolve by hash from a search
   path?** The second is closer to how this should work and needs a lookup rule.
3. **Output format.** Human text is specified above; a `--json` verdict for
   scripting is obvious but unspecified.
4. **Does the app ship the prototype's reduced CBOR, or wait for DEC-002?**
   Shipping it makes the spike normative by accident — which is exactly what
   `prototype/` exists to prevent.
5. **Threshold subjects in `reduce` for the floor**, or v2? `PLAN-0001` §12 risk
   7 already offers the cut.
