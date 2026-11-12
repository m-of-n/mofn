---
schema: "archdoc/v1"
id: PLAN-0004
title: "Application plan — local wallet, two domains, verdict first"
short_title: "Application plan"
description: "Whether APP-0001 is complete, and the plan that fills the gaps. Draft. Does not accept a DEC-*."
type: plan
category: product
status: draft
version: "0.3.0"
date: "2026-10-02"
updated: "2026-11-09"
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
  PLAN-0003 MD-1 records the targets (software supply chain + archives/library).
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

Follow PLAN-0003 MD-1. Do not add a third.

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

### 6.1 Private keys

**Proposed, except where it restates a constraint this plan already has.**
Keys are files. There is no keychain product and no cloud custody. Those
two lines are not a new decision. The rest is a proposal for the CLI
engine. It does not close DEC-002.

- Private keys are files under `wallet/keys`. The directory is mode `0700`.
  Each private key file is mode `0600`.
- Each private key file is encrypted at rest. The mechanism is
  passphrase-based secret-key encryption. The candidates — OpenPGP S2K
  with AEAD, or one modern KDF plus AEAD — are surveyed in R-0002
  (PR 59), the private-key section. This plan does not pick one. The
  on-disk encoding is still DEC-002.
- The engine prompts for the passphrase. The passphrase is not a
  command-line argument and it is not logged. Later, not this
  milestone: an OS keychain may store the passphrase. It does not store
  the key.
- The plaintext key exists only inside the engine, for one signature,
  and is then wiped. The CLI asks the engine. Callers do not hold the
  unlocked key.
- Hardware-backed non-exportable keys are out of scope for the CLI
  engine milestone. The private key would no longer be a file.

### 6.2 What OpenPGP already does here (#128)

**Proposed, 2026-11-05.** It reads §6.1 against OpenPGP (RFC 9580 and
GnuPG, as R-0002 §10 records them) and against wallet engine v0
(`prototype/wallet`, DL-0016). It borrows ideas only. It does not adopt the
OpenPGP packet format or generate a primitive, and it closes no DEC-*.
Whether ADR-0004 governs the key file as well as statements is not decided
here.

| OpenPGP | §6.1 / ARCH-0003 | engine v0 | this change |
|---|---|---|---|
| Secret key encrypted with a passphrase KDF (Argon2, S2K id 4) and AEAD (usage octet 253), RFC 9580 §3.7, §5.5.3 | "encrypted at rest", candidates in R-0002 §10.1 | **done.** Argon2id + libsodium SecretBox, files 0600 and directory 0700 (`engine/store.py`) | none |
| The AEAD's additional data is the public-key packet fields (§5.5.3), so secret material moved under another key fails to decrypt | not stated | **gap.** The box authenticates the seed but not whose seed it is. A `.key` file copied under another persona with the same passphrase opened, and the mismatch was caught only later, at the post-sign verify | **fixed.** `unlock` derives the kid from the opened seed and refuses a mismatch before any signing. Test: `test_key_file_swapped_between_personas` |
| `gpg-agent` `PKSIGN`: the caller passes a key and a hash and gets a signature back, never the secret key. The cache defaults to 600 s and is capped at 7200 s (R-0002 §10.2) | "callers do not hold the unlocked key" | **met in-process.** Unlocks for one operation, no cache, seed wiped in `signer.sign` (best effort in Python) | none yet: see rule 1 |
| Primary key certifies, subkeys sign; key flags limit each key; the primary can be kept offline (GnuPG exports subkeys with a stub in place of the secret primary) | ARCH-0003 §3.2: the identity key delegates operational keys by scoped delegation; `capabilities` play the role of key flags | **absent.** v0 has no delegation (`engine/reduce.py`); W-3 (#67) adds it | rules 2–3, after W-3 |

Rules proposed for the engine:

1. **No unlocked key in the UI process.** When the GUI (W-5, #69) lands,
   it asks the engine to sign, as `PKSIGN` does, and never receives the
   seed. Default: no passphrase cache. If one is added later, it has a hard
   maximum lifetime and the wallet shows it. A cache that only resets
   when used is the gpg-agent behaviour R-0002 §10.2 calls too long.
2. **Operational keys under an identity key.** Once W-3 can reduce a
   delegation, the engine can make a key whose authority comes from an
   ordinary ARCH-0003 §3.2 delegation by the persona's identity key, with
   a narrow scope and a short expiry. This adds no new object kind, and
   ARCH-0001 R-M-10 and ARCH-0003 W-03 already cover it. CI signs with
   the operational key.
3. **The identity key may be offline.** A persona stays `owned` when its
   identity `.key` file has been moved to offline media, as long as an
   operational key is still present. The wallet signs with the operational
   keys and says that the identity key is not present. Making or renewing
   a delegation needs the identity key back.

**Compromise is handled by expiry, not revocation.** A leaked operational key
is bounded by the scope and expiry its identity key gave it (ARCH-0003 §3.2,
ARCH-0001 R-O-02). **Declined by the owner, 2026-11-05: a revocation
certificate generated with every key** (OpenPGP's practice). R-0007 P5,
escrowed revocation, is a separate proposal and stays open; this decline does
not decide it.

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

### 7.1 Schedule status, Nov 9, 2026

Verified at main `c84a0e7` (2026-11-09). This is a status reading of the dates
already in §7 and in PLAN-0001, PLAN-0002 and PLAN-0003. It does not move
those dates, and it accepts no DEC-*.

I3, the demo floor, is due 2026-11-11 — two days from this reading. The
one-hop CLI path works. Delegation, which the sponsor has required for the
floor, is not in the engine.

| item | due | owner | status | evidence |
|---|---|---|---|---|
| I1 / D1–D3: library and research reports | Oct 14 | both | done | library repo; `R-0004`, `R-0005`, `R-0006` |
| §7 one-page scenarios for each §3 application (W-2, #66, T-029a) | Oct 14 | Paul, both | behind | #66 is open; T-029a is still todo; APP-0001 still says "October" |
| GUI framework (DECISIONS-0001 item 28, T-029c) | Oct 14 | Paul confirms; Ndewedo proposes | behind | still "Tauri, tentative, PySide6 fallback"; #69 last activity 2026-10-05 |
| I2 / D4 encoding-neutral schema; D5 DEC-002 ADR | Oct 21 / Oct 28 | David, Paul | done | SPEC-0002; `ADR-0004` accepted 2026-10-25 |
| §7 engine contract: `check` prints the six-line verdict (W-1, #65) | Oct 28 | David | done | #122, #125; `prototype/wallet` |
| §7 signature check; tamper and unauthorized-key demos | Nov 11 | David, Ndewedo | done | `check.py` runs V1–V9, including the signature check, before `reduce`; `demo/slice.sh` cases ②, ③, ②′; #68 run of 2026-11-09 at `c84a0e7` was green |
| I3 / D6 / #31 / #67: delegation in the engine | Nov 11 | David (engine); Paul (rewrite #67 and #31) | behind | `reduce.py` last changed in `b7600fe` (2026-11-01) and is one hop only; #148's `test_delegation.py` uses a test-only walker; #67 still uses retired `may-speak` terms; BACKLOG T-041 and T-065 are todo |
| Issuer revocation (`ADR-0003` D5) | with the floor | David | not started | `check.py` hard-codes `revocations considered` to 0; #67 still says short expiry is the only revocation mechanism |
| W-6 / #127: menu, `--version`, `mofn run`, CI matrix | Nov 11 | David | done | #131 (`724bb4b`, 2026-11-06) |
| W-6 / #127: `release.yml`, downloads, README install | Nov 11 | Ndewedo | not started | no tags; no `.github/workflows/release.yml` |
| I4 / D7 mappings; §7 archives domain through the same path | Nov 25 | David; #66 Paul and Ndewedo | not started | I4 has not begun; #66 is still open. The Oct 14 scenario half of #66 is already behind |
| I5 / D8 five views and packaging; #69 GUI | Dec 1–4 | Ndewedo | not started | #69 unchanged since 2026-10-05 |
| #68 weekly demo slice | every Monday | Ndewedo | on track for the current cases | `weekly-slice.yml`; automated post on #68, 2026-11-09. Delegation and revocation cases wait on the engine |

David's last commit on this repo is `724bb4b` (2026-11-06, 10:25 AM PT). He
has no open pull requests.

**To recover before Nov 11:**

- **David:** put delegation in `reduce` (move E-1…E-4 off the test-only
  walker, T-065); keep sets of statements in the wallet for those paths;
  enforce issuer revocation (`ADR-0003` D5) instead of hard-coding 0.
- **Ndewedo (Chip):** add slice cases for delegation and revocation once the
  engine can run them; write `release.yml`, the downloads, and the README
  install section (#127).
- **Paul:** rewrite #67 and #31 for integer depth, `trust` / `about` /
  `may-delegate`, and issuer revocation; confirm or replace decision #28.

## 8. Fixes this plan expects in APP-0001

1. Delete "No GUI" or replace it with "no web UI, no server; graphic UI is in scope."
2. Name the two MD-1 applications; keep email as a scenario.
3. Point the build order at PLAN-0003's dates and owners.
4. Collapse the two sections both numbered 9.

Those edits are documentation. They do not accept DEC-002 or any other open decision.

## 9. Build and release

**Proposed, 2026-11-09**, except where it restates what is already in the repo
or in PLAN-0001 and PLAN-0002. It accepts no DEC-* and it does not close
decision #28.

**Current state**, verified 2026-11-09 at main `c84a0e7`. The only application
is the `mofn` Python CLI, run from a checkout (the command menu, `--version`,
and the `mofn run` guided screen). There are no releases, no tags, and no
`release.yml`. There is nothing to download.

What is automated:

- `ci.yml` runs the wallet tests on Ubuntu, macOS and Windows for every pull
  request and every push to `main`, and checks the menu and version.
- `weekly-slice.yml` runs `demo/slice.sh` offline each Monday and posts the
  result on #68.
- `pages.yml` publishes the documentation site.
- `library-update.yml` bumps the library pin hourly.

**Targets.** macOS and Linux (PLAN-0002 M6, "wallet installs from Pages").
Windows is already in the CI matrix but is not a release target unless that
is decided.

**CLI packaging (proposed).** PLAN-0001 row 10 is a single-file Python zipapp,
not an installer. The proposal is that a `release.yml` workflow builds it on
a version tag (`wallet-vX.Y.Z`, as the wallet changelog already describes),
attaches it to a GitHub Release, and links it from Pages, with checksums.
Ndewedo owns this half of #127 (`release.yml`, the downloads, the README
install section). Signing of the release files is an open item.

The wallet's runtime dependencies are `pynacl==1.5.0`, `PyYAML==6.0.2` and
`textual==8.2.8` (`prototype/wallet/requirements.txt`; `pytest` is for tests
only). PyNaCl is a native extension. A zipapp cannot bundle it portably, so
an install still needs a Python (CI uses 3.12) and at least `pip install
pynacl`, or a per-OS build that includes the wheel. How to handle that is an
open question; BACKLOG W-6 already asks for one self-contained build per OS.

**GUI.** Not started. #69 has had no activity since 2026-10-05. Decision #28
(DECISIONS-0001) — "Tauri, tentative, PySide6 fallback" — was due 2026-10-14
and is unconfirmed. The open options are Tauri, PySide6, and SwiftUI
(Mac-only). GUI packaging (a signed and notarized Mac app, and a Linux
AppImage or similar) comes after the five views, in the Dec 1–4 window, with
packaging last, per §7.

| output | platform | built by | status |
|---|---|---|---|
| CLI zipapp | macOS, Linux (Windows only if decided) | proposed `release.yml` on a `wallet-v*` tag; Ndewedo, #127 | not started |
| GUI app | Mac first; Linux if the framework is not SwiftUI | after the five views, Dec 1–4, packaging last | not started; framework (decision #28) unconfirmed |
| documentation site | Pages | `pages.yml` | in place |
| weekly slice report | posted on #68 | `weekly-slice.yml` each Monday | in place |

**Open items.** Confirm the GUI framework (decision #28). Cut a first tagged
CLI release. Decide how release files are signed. Decide whether Windows is a
release target.

## What changed in v0.3.0 — 2026-11-09

- §7.1: schedule status as of main `c84a0e7`, with evidence and a recover
  list. No dates in §7 are changed.
- §9: build and release — what CI does today, the proposed zipapp release,
  and the open items. Decision #28 is listed as open, not accepted.
