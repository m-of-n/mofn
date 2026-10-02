---
schema: "archdoc/v1"
id: PLAN-0004
title: "Application plan — local wallet, two domains, verdict first"
short_title: "Application plan"
description: "Whether APP-0001 is complete, and the plan that fills the gaps. Draft. Does not accept a DEC-*."
type: plan
category: product
status: draft
version: "0.1.0"
date: "2026-10-02"
updated: "2026-10-02"
needs_review: true
reviewed: false
canonical_path: project/PLAN-0004-application-plan.md
companion:
  - project/APP-0001-application-design.md
  - project/PLAN-0003-semester-plan.md
defers_to: ARCH-0001
---

# Application plan

**Status: draft. Nothing here is accepted.** APP-0001 remains the behaviour
sketch. This file says what is missing and how to build the wallet without
inventing architecture.

## 1. Is the application design complete?

**No.** APP-0001 v0.2 names the right product and the right verdict, and it is
not a plan you can hand to someone and have them build the October UI.

What is solid:

- The product is a **local wallet**: hold, collect, make, present, evaluate.
- Trust roots are local and unsigned.
- The product moment is the **authorization** line of a six-dimension verdict.
- The demo floor (`reduce` + `check`) and the application are the same work.
- Delegation is graph-shaped and is **not** a knowledge-graph product.

What is not solid:

- **It contradicts itself.** §0 requires a graphic UI. §5 still says "No GUI,
  no web UI, no server." The second sentence is right; the first is stale.
- **The two use cases are unnamed.** "October" and "two applications" do not
  say which domains, which claims, or which screens. PLAN-0002 already says
  personas, scenarios, and sketches cannot be written until that is settled.
  PLAN-0003 D-1 records the targets (software supply chain + archives/library).
  APP-0001 never uses them. Its only worked example is still email.
- **No screens, no on-disk layout, no owners, no dates** beyond "October" and
  "packaging last." PLAN-0003 already schedules D8 for Nov 26–Dec 4 under
  Ndewedo. APP-0001's build order does not match that calendar.
- **Open questions are still open** (§9, duplicated heading): command name,
  domain lookup, `--json`, whether the prototype encoding may ship, whether
  thresholds are in the floor. This plan does not close them.
- **Stack is unspecified**, which is correct until someone proposes one. A
  proposal is in §4. It is not a decision.

## 2. What we are building

A **local desktop wallet** over a **reduction engine**.

| layer | job | not |
|---|---|---|
| engine | keys-as-files, statements-as-files, domains-as-files, `make` / `render` / `check` / `reduce` | a server, a registry, a graph database |
| CLI | the same operations, scriptable, the demo floor | a substitute for the CS Night UI |
| graphic UI | two domains through one set of views, so a sentence is visibly rendered from the vocabulary | a dashboard of the data model |

No network. No keychain product. No revocation product. No knowledge-graph
engine. A chain of "Alice says Bob may speak about Foo" is reduced by matching
issuer to subject and intersecting tag and validity. Files plus that algorithm
are the store.

## 3. The two applications

Follow PLAN-0003 D-1. Do not add a third.

**Supply chain (primary).** A key asserts a vocabulary value about a hashed
artifact (`build-provenance` / `reproducible`). A second key signs a true
statement it is not entitled to make. `check` shows integrity and authenticity
ok, **authorization fail**, and the rendered sentence with "no standing."
That is the CS Night moment.

**Archives / library (contrast).** A statement about a record that is described
rather than treated as a software build, using the archives vocabulary. Same
screens, same engine, different domain file. If the second domain needs
type-specific UI code, the vocabulary claim has failed.

Email (Alice/Bob/Carol/Dave) stays a **schema scenario**, not a third
application. PLAN-0003 already says that.

Personas, all three required by the product spec, mapped onto those two:

| persona | does |
|---|---|
| domain author | publishes a domain file: types, values, renderings |
| issuer | holds a key, makes an attestation or a delegation |
| relying party | holds trust roots, evaluates a presented set, reads the verdict |

## 4. Proposed stack — not accepted

**Python engine + CLI first. Thin local UI later.**

A Tauri/TypeScript shell is a reasonable October/November UI **if** every
cryptographic and reduction step stays in the engine and the UI only displays
wallet state and verdicts. Do not put a knowledge graph behind that shell.
Do not start the shell before the two scenarios in §3 can be run from the CLI.

DEC-002 stays open. The prototype's reduced CBOR must not become the shipping
format by being the only thing the UI can load (APP-0001 open question 4).

## 5. Minimal UI

Five views. Nothing else for Fall 2026.

1. **Wallet** — roots, key files, collected statements. Roots are visually distinct because they are unsigned.
2. **Domain** — types and values of one domain, including the human rendering, so the vocabulary is inspectable.
3. **Make** — pick key, subject, type, value; write a statement file.
4. **Present** — choose the statement set to hand a relying party.
5. **Verdict** — six dimensions, the rendered sentence, and the limit line: this proves origin and integrity, not truth.

## 6. On disk

No database. A directory the user already has:

```
wallet/
  roots/        unsigned local decisions
  keys/         files, not a keychain
  domains/      one file per domain of discourse
  statements/   collected and made
```

An optional index may map a domain hash to a file. It is not a graph store.

## 7. Schedule

Fits PLAN-0003. Does not move D8 earlier than the floor.

| when | ships | owner | done when |
|---|---|---|---|
| by Oct 14 | one-page scenario for each §3 application, including the fail-authorization case | both | APP-0001 can name the two apps without saying "October" |
| by Oct 28 | engine contract: the §3 CLI commands, human verdict text; encoding still swappable | David | `check` on a fixture prints the six lines |
| Nov 11 (I3) | signature check inside reduction; tamper and unauthorized-key demos | David, Ndewedo | break a link; the verdict names which dimension failed |
| Nov 25 (I4) | archives domain through the same path; supply-chain mapping may land beside it | David | second domain, no new UI code |
| Dec 1–4 (I5) | the five views over that engine; package last | Ndewedo | CS Night can show both domains and the authorization fail |

Threshold subjects stay a cut, as APP-0001 already allows, unless the floor
is otherwise green. Packaging is last.

## 8. Fixes this plan expects in APP-0001

1. Delete "No GUI" or replace it with "no web UI, no server; graphic UI is in scope."
2. Name the two D-1 applications; keep email as a scenario.
3. Point the build order at PLAN-0003's dates and owners.
4. Collapse the two sections both numbered 9.

Those edits are documentation. They do not accept DEC-002 or any other open decision.
