---
schema: "archdoc/v1"
id: APP-0001
title: "The application — what we are actually building for the demo"
short_title: "Application design"
description: "What the demo application does, its commands, and what a user sees. The gap PROC-0004 §6 left: it specified packaging for a thing whose behaviour was undefined."
type: design
category: product
status: draft
version: "0.1.0"
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

## 1. What it is

**`mofn` — a command-line tool that makes and checks statements.**

One binary. No service, no daemon, no account. It reads and writes files and
prints verdicts. Everything the CS Night demo shows, it does.

**Why a CLI and not a GUI:** the thesis is that legibility is a property of the
*data*, not of a UI someone hand-wrote. A CLI that renders a claim in English
from a resolved type proves that. A GUI would obscure it — a reviewer could not
tell whether the nice sentence came from the vocabulary or from the programmer.

## 2. The five things it does

| verb | what it does |
|---|---|
| `make` | create a statement — *A says B has C* — and sign it |
| `check` | verify a statement and emit a **multi-dimensional verdict** |
| `render` | print what a statement *means*, from its resolved type |
| `reduce` | compose a delegation chain and say what authority results |
| `domain` | publish, inspect and hash a domain of discourse |

Reduction is the one with no prototype behind it yet, and it is the one the
project is actually about.

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

`prototype/statements/` has statement creation, the reduced-CBOR encoding,
signing shape, subject modes, domain construction, hash-identification, range
checking and multilingual rendering — **all of it working**.

Missing, and it is the hard part: **reduction.** Delegation is represented and
not composed. That is SPKI's actual contribution and the thing the project
claims, and it has no code.

## 8. Build order

| | | why |
|---|---|---|
| 1 | **`reduce`** | the only unprototyped piece, and the one the thesis rests on |
| 2 | `check` | the verdict, over reduction |
| 3 | `render` | already works in the spike |
| 4 | `make` | already works in the spike |
| 5 | `domain` | already works in the spike |
| 6 | packaging | genuinely last |

**Reduction first, not last.** Building the easy parts first would produce
something demoable that does not demonstrate the claim.

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
