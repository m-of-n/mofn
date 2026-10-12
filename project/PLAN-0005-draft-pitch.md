---
schema: "archdoc/v1"
id: PLAN-0005
title: "Draft pitch — the application and the benefit"
short_title: "Draft pitch"
description: "How to explain Key-centric Semantic Attestations to an investor or partner: the problem, the applications, the benefit, and what is real today. Draft for team guidance; not for external use until market sizing (D9) is done."
type: plan
category: strategy
status: draft
version: "0.1.0"
date: "2026-10-12"
updated: "2026-10-12"
needs_review: true
reviewed: false
canonical_path: project/PLAN-0005-draft-pitch.md
companion:
  - project/PLAN-0004-application-plan.md
  - project/APP-0001-application-design.md
  - research/0001-signatures-and-attestation/report.md
defers_to: ARCH-0001
---

# Draft pitch — the application and the benefit

> **Draft, for team guidance.** This is how we explain the project to an
> investor or partner. Every factual claim below is traced to the survey or
> the library (see *Sources*). **Market size and customer validation are not
> done yet (D9)** — do not quote a market number until they are. The commercial
> path beyond the student project is the sponsor's (T-012).

**One line:** *Signatures tell you who signed. We tell you whether they were
allowed to — in words a person can read.*

## The problem

Every software and AI system now runs on digital signatures — and signatures
answer the wrong question. A signature proves *who* signed. It does not prove
they were *allowed* to say what they signed. Attackers have learned to live in
that gap.

**The proof point is recent and real.** In **May 2026**, attackers shipped **84
npm packages carrying cryptographically valid provenance attestations** that
correctly named the builder, repository and workflow. Every standard verifier
said ✅. The industry's own write-up conceded that provenance records *what
happened*, not *whether that was good enough*.

The rest of the stack has the same shape. The supply-chain frameworks take
"who may sign" as an input — a parameter, a command-line flag, a registry
setting — and say so in their own specifications. In the web's certificate
system, the mechanism for limiting what a certificate authority may vouch for
is present on **1.8% of authorities**; any of them can vouch for any name.

## What we are building

**The missing layer: an entitlement check.** It sits on top of the signatures
people already use and answers one question —

> *Was this key allowed to make this claim, about this thing, right now?*

— and shows the answer as a readable sentence, with the chain of delegation
behind it. Concretely, a local **wallet** (PLAN-0004): it holds keys and the
user's own trust decisions, makes signed statements and delegations, and gives
a verdict on six separate lines — integrity, authenticity, names,
**authorization**, acceptance, meaning. No server, no registry, no central
certificate authority; it works offline.

## Applications, in order of market pull

### 1. Software supply chain — the beachhead
A verifier and policy layer for platform security teams, package registries
and regulated software vendors.

- **Benefit:** stops the attack class that passes every signature check today
  — a valid signature from a key with no standing to make the claim.
- **Why now:** the EU Cyber Resilience Act's vulnerability reporting obligations
  apply from **September 2026** and the full regulation from **December 2027**.
  Today's tools leave entitlement to configuration nobody audits.

### 2. AI agents acting on people's behalf — the big upside
Scoped, expiring, narrowing delegation — *"this agent may spend up to $X with
this vendor until Friday"* — verifiable at every hop and auditable back to the
person who authorised it.

- **Benefit:** answers the question no current agent framework can: *which
  human authorised this action?*
- **Why now:** three new IETF drafts in 2026 are racing to solve exactly this,
  and are reinventing a 1999 design (SPKI) without its strongest property —
  the ability to compute what a chain of delegations actually authorises.

### 3. Content provenance and AI labelling
Claims about media that render in plain language, with a place for
independent assessors such as fact-checkers.

- **Why now:** EU AI Act Article 50 applies from **2 August 2026**; California's
  AI Transparency Act from the same date.
- **The gap:** the incumbent standard (C2PA) fixes its vocabulary in the
  specification, so an unknown claim becomes an unreadable signed blob — and its
  published specifications carry **no post-quantum migration path** while
  promising that timestamped credentials stay valid indefinitely.

## Why we would win

- **Complements, does not replace.** Works over the signing infrastructure
  people already run — Sigstore, in-toto, COSE.
- **No central root.** Trust is decided locally, offline, with no vendor
  certificate authority to lock customers in.
- **Self-describing claims.** A new domain needs a published vocabulary file,
  not a software update or a standards-body vote. The same engine renders
  supply-chain and archive claims, in English and Spanish, with no
  domain-specific code.
- **The research is done properly.** A 17,000-word survey of fifty years of
  signature systems (155 citations, an original measurement) and a 438-record
  technical library with 35 standards fully extracted into requirements,
  schemas and test vectors.

## The demonstration

Built around one moment (PLAN-0004 §3): a key signs a **true** statement it is
**not entitled to make**, and the verdict reads integrity ✔, authenticity ✔,
**authorization ✘** — *"asserted by a key with no standing to say so."*
Candidate moments for CS Night: replaying the May 2026 npm attack side by side
with a standard verifier; live, expiring delegation on stage; a vocabulary the
wallet has never seen rendering correctly with no code change; a one-byte
tamper caught before anything is decoded; all of it with Wi-Fi off.

## Stage — honestly

| | |
|---|---|
| **Today** | research complete for this phase; open specification in progress; working prototype of the core engine (encoding, vocabularies, rendering, delegation reduction) |
| **Nov 11** | demo floor — delegation chain reduces, a broken link is named in English |
| **Dec 4** | public demonstration at CS Night (USF CS690) |
| **Not done** | market sizing and customer validation (D9); a packaged application (D8); signature checking inside reduction |
| **Team** | sponsored research project — two graduate students and the sponsor |

## Sources

Every claim above, and where it is established:

| claim | source |
|---|---|
| May 2026 npm attack: 84 artifacts, valid provenance | survey R-001 §8.6; library `slsa-2026-mini-shai-hulud` |
| supply-chain frameworks take authorization as an input | R-001 §8.5 |
| 1.8% of CA intermediates carry name constraints | R-001 §4.5 (original measurement, CCADB, 2026-09-26) |
| EU CRA dates | R-001 §8.4; library `eu-cra-2024-2847` |
| three 2026 IETF agent-delegation drafts; SPKI's computable meet | R-001 §9.2–§9.3 |
| EU AI Act Art 50 and CA SB 942 dates | R-001 §6.4 |
| C2PA vocabulary fixed in spec; no post-quantum path | R-001 §6.5, §10.5 |
| the CS Night moment | PLAN-0004 §3; APP-0001 §4 |
| prototype capabilities | `prototype/statements/`; APP-0001 §7–§8 |
