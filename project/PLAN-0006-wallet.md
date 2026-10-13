---
schema: "archdoc/v1"
id: PLAN-0006
title: "Wallet build plan — the decisions it bears on, the work in flight, and the order to build it in"
short_title: "Wallet build plan"
description: "How the wallet application is to be built: which open decisions it touches and must not close, which tasks and issues are already in flight, the engine/UI contract that lets both be built at once, and the decisions still owed by a human."
type: plan
category: product
status: draft
version: "0.1.0"
version_policy: "semver; MINOR = a build step or contract added or changed"
date: "2026-10-12"
updated: "2026-10-12"
decision_makers: []
reviewers: []
needs_review: true
reviewed: false
canonical_path: project/PLAN-0006-wallet.md
companion:
  - project/PLAN-0004-application-plan.md
  - project/APP-0001-application-design.md
  - project/PLAN-0003-semester-plan.md
  - research/0002-wallets/report.md
defers_to: ARCH-0001
backlog: W-1, W-2, W-3, W-4, W-5
agent_notes: >
  Execution plan only. It accepts no DEC-*, no principle, and no encoding.
  Where it recommends, the recommendation is marked as a proposal and names
  who owns the decision. §8 is the list of things a human still owes; §9 is
  the list of things already settled that keep being re-asked.
---

# Wallet build plan

**Status: draft. Nothing here accepts a `DEC-*`, a principle, or a stack.**
`APP-0001` is the behaviour sketch, `PLAN-0004` is the application plan, and
this file is the build plan underneath both: what the wallet touches that is
still open, what is already in flight, and the order that lets two people build
it in parallel instead of in series.

Read `APP-0001` §1–§2 for what a wallet *is*. It is not restated here.

---

## 1. The finding this plan exists for

**The wallet is one person's critical path, and that person is behind on three
other deliverables.** `W-1` — the engine every other wallet task calls — is due
**Oct 28**, owned by David, with **no commits** as of the 2026-10-12 weekly;
the same owner also holds D3 *context* and *mechanism* (not started, due
Oct 14) and the D5 Tier 1 extraction (0 of 7, due Oct 28). The GUI owner, who
merged roughly sixteen PRs in the same week, is scheduled **last** (I5,
Nov 26 – Dec 4).

Everything in §6 follows from one move: **freeze the engine's output contract
as fixtures before the engine exists**, so the GUI is built against golden
files rather than against David's availability. The contract is not extra
work — it is `T-045` (R-O-06 separated output) and `APP-0001` open question 3
(`--json`) pulled forward from December to **Oct 19**.

---

## 2. Decisions the wallet bears on

### 2.1 Open `DEC-*` — and where the wallet would close one by accident

The wallet is the **first implementation** of three of these. Implementation is
how an open decision gets closed without anyone deciding it.

| | decision | how the wallet touches it | the guard |
|---|---|---|---|
| **DEC-002** | concrete encoding — narrowed to option 5 by MD-3, **not accepted** | statements are read and written from disk; a wallet that can load only one encoding *is* an encoding decision | **two codecs behind one interface**, and `demo/slice.sh` passes under both (already `W-1`'s acceptance, #65) |
| **DEC-003** | issuer/subject identifiers on the wire | the verdict prints `key 9f2a…`. Truncated-hex-of-what is a DEC-003 position | the **engine** names its KeyId profile and emits the display string; the UI renders what it is given and derives nothing |
| **DEC-004** | tag language | `reduce` intersects topics; `W-3` adds validity | ship the DEC-004 **minimum** only — opaque bytes + `bytes-equal` (`T-042`). No richer tag reaches the UI |
| **DEC-005** | envelope for `ArtifactStatement` | what a `.stmt` file *is* | native statements are files; COSE/DSSE stay **export**, out of the wallet floor (R-I-03) |
| **DEC-007** | predicate rendering — the semantic layer | **the wallet is DEC-007's only implementation.** The domain file's rendering table is what makes the sentence a sentence | renderings come from the domain file at run time; **no string in UI source describes a type or a value** |
| **DEC-008** | can all processing be key-local? | trust roots are unsigned and local — the fixed floor the question is about | roots stay unsigned, local, and **scoped to a topic**; the UI never offers "trust this key" without a topic |
| DEC-009 | the contract form | — | out of scope for the wallet |

**DEC-007 deserves its own line.** The project's claim is that a vocabulary
renders a sentence with no type-specific code. The wallet is where that claim
is either demonstrated or quietly broken, and it breaks the first time a
developer writes `if type == "build-provenance"` in a view. §7 makes that
mechanically checkable.

### 2.2 The requirement the product moment rests on is not accepted

`APP-0001` §4 calls the verdict "the six dimensions of **R-O-06**". Two things
are true and neither is recorded anywhere else:

1. **R-O-06 is not in `ARCH-0001`.** It lives in `ARCH-0001-PROPOSAL-v0.2.0`
   §6, together with R-O-05 and R-M-11. Accepting the proposal is
   `DECISIONS-0001` Tier 1 **item 4**, which the register notes is *"not on any
   agenda to date"*. Until then the wallet's headline feature cites a
   requirement with no force.
2. **R-O-06 names three results, not six** — name resolution, authorization
   reduction, statement acceptance (`ARCH-0001` §4.3). The other three lines
   (integrity, authenticity, semantics) come from `PLAN-0001` §7.4 and DEC-007.
   So **three of the six verdict lines have no requirement id at all.**

Neither blocks building. Both mean the verdict JSON contract (§5.3) is
currently the *most* normative statement of the verdict shape in the
repository, which is backwards. **Recommended:** schedule item 4 before Oct 28,
and fix the `APP-0001` §4 citation when it lands.

### 2.3 Principles — what is provisional, what is held, what that costs here

Per MD-2 and `ADR-0002` (proposed, mofn#83): **P1 accepted** (ADR-0001);
**P2, P3, P5, P6 provisional**; **P4, P7 held**.

| | principle | consequence for the build |
|---|---|---|
| **P1** | type identity is `(defining key, label)` | the Domain view shows **"defined by `<key>`"**. That is the identity. Accepted, so it is safe to build on |
| **P2** | *A says B has C* | one statement form, three functions. One `make` command, not three |
| **P3** | a type *is* a schema | the Make form is **generated from the domain file**. This is the load-bearing one for the UI |
| **P5** | validity checked, unknown rejected | the UI must have a way to display *rejected*, not just *failed*. An unknown field is a refusal, not a warning |
| **P6** | a name is an attested string | name resolution is a verdict line, not a lookup table |
| **P4** | **held** — domains are hash-identified sets | **the Domain view may not present a domain hash as the domain's identity.** `PLAN-0002` §6.5 sketch ④ does exactly that (`id 2104d6d4…`). Show the defining key (P1); a file digest may appear, labelled as a file digest |
| **P7** | **held** — authorization is a family by profile | the demo uses **one** authorization profile and says so on screen |

Register item **5c** (is a domain itself a statement by a key, or a bare hashed
artifact?) is held with P4 and is the question the Domain view would answer by
accident. Same guard: defining key, not hash-as-identity.

### 2.4 Dated decisions

| | | bears on the wallet as |
|---|---|---|
| **MD-1** | targets: software supply chain + archives/library | the two domains the UI must serve. **Email stays a schema scenario, not a third app** |
| **MD-3** | DEC-002 narrowed to option 5 | the CBOR codec is the *primary* codec; the second codec exists to prove the first is not load-bearing |
| **MD-7** | GUI framework: **Tauri, tentative** | `DECISIONS-0001` item 28 / `T-029c` — **confirm by Oct 14, before GUI work begins.** §8.1 recommends against it |

---

## 3. Work in flight

### 3.1 The `W-*` lane — issues #65–#69, parent #31 (floor) and #32 (D8)

| id | issue | owner | due | state 2026-10-12 | blocked by |
|---|---|---|---|---|---|
| **W-1** engine v0 | [#65](https://github.com/m-of-n/mofn/issues/65) | David | Oct 28 | **no commits** | nothing — it is the root |
| **W-2** second domain | [#66](https://github.com/m-of-n/mofn/issues/66) | Paul | Oct 14, then Nov 25 | scenarios not written | — |
| **W-3** delegation + expiry | [#67](https://github.com/m-of-n/mofn/issues/67) | Paul | Nov 11 | not started | W-1 |
| **W-4** weekly demo slice | [#68](https://github.com/m-of-n/mofn/issues/68) | Ndewedo | weekly | doing | W-1 for real cases |
| **W-5** Mac GUI | [#69](https://github.com/m-of-n/mofn/issues/69) | Ndewedo | Dec | framework unconfirmed | **W-1, or the §5.3 contract** |

### 3.2 `T-*` rows that are the same work seen from the other side

`BACKLOG-0001` flags the double-count and declines to resolve it. **Resolution
proposed here**, because the overlap is now costing a planning answer:

| `T-` row | | |
|---|---|---|
| `T-040` names · `T-041` 5-tuple · `T-044` acceptance · `T-045` separated output | **become pointers** to `W-1` / `W-3` | they have no issues, no dates and no owners the `W-` rows do not already have |
| `T-042` minimum tag profile | **stays** | it is a profile definition, not application work |
| `T-043` *k*-of-*n* thresholds | **stays, and leaves the wallet floor** | R-M-06 and G4 make it an engine requirement; `APP-0001` q5 and `PLAN-0001` §12 risk 7 already offer the UI cut. The GUI displays a reduced result; it does not build a threshold |
| `T-046` published test vectors | **stays** | `spec/vectors/` is a specification artifact, not a wallet file |
| `T-047` break-a-link demo · `T-055` unauthorized-key demo | **become** `W-4` slice cases | one script, run weekly, is better evidence than two demo tasks in different increments |
| `T-029a/b` scenarios + sketches | **become** `W-2` | already the same deliverable |
| `T-054` zipapp packaging · `T-060` download on Pages | **stay, last** | D8 packaging is genuinely after everything |

### 3.3 What already exists

`prototype/statements/` — statement creation, reduced-CBOR encode/decode,
signing shape, subject modes, domains, hash identification, range checking,
multilingual rendering, and reduction (`reduce.py`). `demo_email.py` runs the
Alice/Bob/Carol/Dave chain end to end including the three cases that must fail.

**`reduce.py` does not check signatures** (`APP-0001` §8). That is not a detail:
until it does, the `authorization FAIL` demo is a claim about data the verifier
took on trust. It is `W-1`'s **first** change, not its last.

`src/` contains one file, `src/mofn/__init__.py`, which `DL-0009` §2 already
lists as an unfixed defect — `CLAUDE.md` says `src/` is empty on purpose. §8.4
proposes the condition under which it legitimately stops being empty.

---

## 4. What the wallet must not do

Carried from `APP-0001` §5, `PLAN-0004` §2 and the wallet survey
(`research/0002-wallets/report.md` §7.3), because **a GUI is where each of these
gets violated by a well-meaning default**:

- **No single padlock, and no "Signature valid" headline.** The headline is the
  authorization result. GnuPG and Thunderbird both say "Good signature" for the
  trusted and the untrusted case; that collapse is the thing this product
  exists to undo.
- **No ownertrust, no marginal/full, no web of trust.** A root is "this key may
  speak on this topic", never "I trust this key".
- **No global trust list, no recognized-issuer list, no keyless OIDC identity
  as the principal.** A recognized signer with no delegation is precisely the
  failure this project shows.
- **No network in the verdict.** No registry, no transparency log fetch, no
  keyserver. The verdict must be reproducible with Wi-Fi off.
- **No "probably a FORGERY"** for an unaccepted key. The words are "no
  standing", or "not accepted".
- **No cloud custody, no keychain product, no long-lived unlocked agent, no
  passphrase on a command line.**
- **No knowledge graph, no graph database, no RDF store.** Delegation is
  graph-shaped; the operation is deterministic reduction.
- **No type-specific code in any view.**

---

## 5. How to build it

### 5.1 Three layers, two boundaries

```
  engine  (Python)   keys · statements · domains · reduce · verify · render
     │               the only thing that touches a private key or a signature
     │  ── boundary A: the codec interface  (keeps DEC-002 open)
     │  ── boundary B: the verdict contract (lets the UI be built first)
  CLI     (Python)   mofn …            — scriptable, the demo floor
  GUI     (§8.1)     Sign · Verify     — displays; computes nothing
```

**Boundary A must be a verify-then-decode boundary.** This is the one piece of
real design in this plan. R-O-05 requires the verifier to verify the signature
**over the canonical bytes before decoding**, and never to canonicalize during
verification. A codec interface shaped `object → dict → bytes` breaks that
silently, because it invites verification of a re-encoded object. The interface
is therefore:

```
encode_canonical(statement)        -> bytes      # authoring only, trusted input
verify(bytes, signature, key)      -> bool       # BEFORE any decode
decode(bytes)                      -> statement  # only after verify
digest(bytes)                      -> Digest
```

Two implementations: the prototype's reduced CBOR (MD-3's option 5) and a debug
JSON/YAML codec. The slice passes under both. **This is what keeps DEC-002 open
while the wallet is built, and it is the only thing that does.**

**Boundary B is `mofn check --format json`.** See §5.3.

### 5.2 The command surface — and the three commands `APP-0001` is missing

`APP-0001` §3 lists `domain init/add-type/id`, `make`, `check`, `render`,
`reduce`. That surface **cannot do two of the five things `APP-0001` §2 says a
wallet does**: it cannot *hold* (no `init`, no `key`, no `root`) and it cannot
*present*. `W-1` (#65) already adds the first group. Completed surface:

| | command | §2 function | source |
|---|---|---|---|
| hold | `mofn init [--wallet DIR]` · `key gen` · `key list` · `root add` · `root list` | hold | `W-1` |
| vocabulary | `domain init` · `domain add-type` · `domain id` · `domain import` | — | `APP-0001` §3 |
| make | `make` (attestation) · `make --type …:may-speak` (delegation) | make | `APP-0001` §3 |
| read | `render [--lang]` · `check [--format json]` · `reduce --ask` | evaluate | `APP-0001` §3 + §5.3 |
| present | `present --ask … -o bundle.d/` | **present** | **new; see below** |

**`present` is a gap, not an addition.** `PLAN-0004` §5 view 4 is *Present* —
"choose the statement set to hand a relying party" — and there is no engine
command under it. Minimum honest form: given a question, emit the set of
statements the reducer actually used, plus the domains they cite. It is the
output of `reduce` with the chain retained, which the engine computes anyway.

### 5.3 The verdict contract — build this first

**One artifact, due Oct 19, that unblocks everything else.** A JSON object plus
three golden files. Written and reviewed *before* the engine emits it; the
engine is then made to match, and the GUI is built against the goldens.

```json
{
  "statement": "prov.stmt",
  "dimensions": [
    {"id": "integrity",     "result": "ok",   "detail": "subject digest re-derives"},
    {"id": "authenticity",  "result": "ok",   "detail": "signature valid under 9f2a…"},
    {"id": "names",         "result": "ok",   "detail": "no name chain to resolve"},
    {"id": "authorization", "result": "fail", "detail": "9f2a… is not entitled to assert paul:build-provenance about this subject"},
    {"id": "acceptance",    "result": "n/a",  "detail": "not evaluated: authorization failed"},
    {"id": "semantics",     "result": "ok",   "detail": "domain resolved, value in range"}
  ],
  "attributes": {
    "signer": "9f2a…", "topic": "paul:build-provenance",
    "subject_digest": "sha256:8e1c…",
    "standing": [{"from": "root:paul", "to": "david", "topic": "build-provenance", "delegate": true},
                 {"from": "david", "to": "9f2a…", "status": "missing"}]
  },
  "sentence": "The artifact sha256:8e1c… was built reproducibly from published sources.",
  "limit": "This proves origin and integrity. It does not prove truth.",
  "unknowns": []
}
```

Four things this fixes at once:

1. It answers `APP-0001` open question **3** (`--json`), which the GUI forces.
2. `result` has **four** values — `ok`, `fail`, `n/a`, `rejected`. P5 requires
   *rejected* to be distinguishable from *failed*; a boolean cannot carry it.
3. `attributes` is #69's "attribute associations" — signer, topic, digest,
   standing — so the GUI requirement is satisfied by the engine, once.
4. `standing` is the chain **as reduced**, with the break named. That is the
   demo, and it is data rather than a drawing.

The three goldens are the `W-4` slice cases: green, `authorization FAIL`,
`integrity FAIL`.

### 5.4 On disk — and the `~/.mofn` vs `wallet/` conflict

`PLAN-0002` §6.4 says `~/.mofn/`; `PLAN-0004` §6 says `wallet/`. Both are
right about different things, and the demo needs the second.

**Proposed:** one layout, a *profile directory*, resolved as
`--wallet DIR` → `$MOFN_WALLET` → `~/.mofn`. `demo/slice.sh` builds a
disposable wallet under `demo/`, which it must be able to do from a clean clone.

```
<wallet>/
  roots/        unsigned local decisions — scoped to a topic, never bare
  keys/         0700; private keys 0600, encrypted at rest
  domains/      one file per domain of discourse
  statements/   collected and made
  index.json    optional: domain digest → file. Not a store, not a graph
```

### 5.5 Private keys

Carried unchanged from `PLAN-0004` §6.1 and `R-0002` §10.7: files, `0700`/`0600`,
encrypted at rest, passphrase **prompted and never an argument**, plaintext key
inside the engine for one signature then wiped, callers get a signature and not
a key. Hardware-backed keys out of scope.

**One open choice can be closed cheaply.** `PLAN-0004` §6.1 leaves the
mechanism open between OpenPGP S2K with AEAD and a modern KDF plus AEAD.
Proposed: use the vetted library's own encrypted private-key serialization
(PKCS#8 with a passphrase, via `cryptography`), and state the citation.

**Why this is not an encoding decision:** a private key file is local, is never
interchanged, and is not a statement. DEC-002 governs the statement encoding.
Nothing about this choice reaches a signature, a digest or a wire format, so it
cannot narrow DEC-002 — and it generates no primitive.

### 5.6 The GUI

Floor for Fall 2026 is **two screens** (#69): **Sign** (`PLAN-0004` view 3) and
**Verify** (view 5). Ceiling is the five views. Wallet and Domain are read-only
renderers over files and are cheap once §5.3 exists; Present needs the engine
command in §5.2.

**The view sets in the two documents do not match.** `PLAN-0004` §5 has no
Delegations view; `PLAN-0002` §6.5 sketch ③ is one. **Proposed:** the chain
lives in the **Verdict** view as `attributes.standing` — it is the product
moment and it belongs where the failure is read. A separate Delegations view is
a *making* view and stays in the ceiling.

---

## 6. Build order

Fits `PLAN-0003`. The only change to the published calendar is that the GUI
starts against fixtures in October instead of waiting for the engine.

| when | ships | owner | done when |
|---|---|---|---|
| **Oct 14** | GUI framework confirmed (§8.1) · `W-2` one-page scenario per MD-1 target incl. the fail-authorization case | Paul, Ndewedo | `T-029c` closed; `APP-0001` can name both apps without saying "October" |
| **Oct 19** | **the §5.3 verdict contract + 3 golden files**, hand-written and reviewed | David writes, Ndewedo reviews | goldens committed; both owners have signed off on the shape |
| Oct 19 → | GUI skeleton **against the goldens** — Sign and Verify, no engine | Ndewedo | Verify renders all three goldens; Sign writes a request the engine will accept |
| **Oct 28** | `W-1` engine v0: `init`, `key gen`, `root add`, `make`, `check`; **signature checking inside reduction**; two codecs | David | `demo/slice.sh` green / `authorization FAIL` / `integrity FAIL`, **under both codecs**, from a clean clone |
| **Nov 11** | `W-3` delegation + short expiry in `reduce`; `T-042` minimum tag; `T-040` names; `T-046` vectors. **The floor** | David, Ndewedo | break a link — the verdict names which dimension and which link |
| **Nov 25** | `W-2` archives domain through the same engine; `--lang es`; D7 mappings beside it | Paul, David | second domain, **no new UI code** (§7) |
| **Dec 1–4** | `W-5` GUI on the real engine; `present` if it has landed; packaging **last** | Ndewedo | GUI verdict is byte-identical to `check --format json` for all slice cases |

`W-4` runs **weekly throughout**, which is what makes slippage visible rather
than discovered.

---

## 7. Acceptance — all mechanical

Not demo moments. Checks that run in CI and fail a PR.

| # | check | what it defends |
|---|---|---|
| A1 | `demo/slice.sh` produces three verdicts from a clean clone: green, `authorization FAIL`, `integrity FAIL` | the product moment exists |
| A2 | A1 passes under **both** codecs | DEC-002 stays open (§2.1) |
| A3 | `check --format json` validates against the §5.3 schema; goldens match byte for byte | boundary B holds |
| A4 | **no domain, type or value literal appears in UI or verdict-rendering source** — a grep test over the view layer and the renderer | DEC-007 / P3 — the thesis |
| A5 | both domains render EN and ES with no code change (`PLAN-0002` M4) | the vocabulary claim generalises |
| A6 | GUI verdict equals CLI verdict for every slice case | one engine, two surfaces |
| A7 | no private key value is ever an argv element; key files are `0600`, dir `0700` | §5.5 |
| A8 | verification rejects a tampered byte **before** decode (R-O-05 ordering) | boundary A is real, not nominal |

A4 is the one most likely to be waived under pressure and is the one that must
not be: it is the difference between demonstrating the mechanism and
demonstrating a demo.

---

## 8. Decisions owed by a human

Each names the owner and the cost of not taking it. **None is taken here.**

### 8.1 GUI framework — due **Oct 14** · owner Paul · `T-029c`, register item 28

MD-7 says Tauri, tentative, with PySide6 as the fallback.

**Recommended: take the fallback.** One criterion — *how many toolchains sit
between the verdict and the screen.* Tauri is Rust + a web frontend + a Python
sidecar + IPC, which is three languages and a process boundary, for two screens
that display a JSON object and generate a form from a domain file. PySide6
imports the engine directly: no sidecar, no IPC, no second serialization of the
verdict. `PLAN-0003` already carries the risk *"wallet GUI eats I4–I5"*, and
the owner who would absorb that is the one carrying the library as well.

**What would change the recommendation:** if macOS signing and notarization for
#32 turn out materially easier for a Tauri bundle than for a Qt app, flip —
packaging is the one place Tauri's extra machinery pays. That is a half-day
spike, and it is worth running before Oct 14 rather than arguing it.

Note for either choice: Qt's licensing (LGPL) is compatible with the project's
Apache-2.0 code but is a dependency-licensing line the final report should
state, not discover.

### 8.2 Accept the v0.2.0 proposal — unscheduled · owner Paul · register item 4

R-O-05 and R-O-06 are wallet requirements with no normative force (§2.2), and
~30 library records already cite them in `bears_on`. **Recommended:** schedule
before Oct 28, so the engine contract is written against accepted text.

### 8.3 `APP-0001`'s five open questions — the GUI forces two of them

| q | recommendation | by |
|---|---|---|
| 1 · is the command `mofn`? | **yes, keep it.** Cosmetic, and the cost rises with every script and doc. Decide now or never | Oct 19 |
| 2 · `--domain` a file, or resolved by hash? | **both** — resolve from `<wallet>/domains` by digest, with a path override. **The GUI forces this**: it cannot ask for a file path per statement | Oct 28 |
| 3 · output format | **§5.3** — JSON, four-valued, with `attributes` and `standing` | **Oct 19** |
| 4 · may the prototype's CBOR ship? | **yes, as one of two codecs** (§5.1). Shipping it as the *only* codec is what makes the spike normative | Oct 28 |
| 5 · thresholds in the floor? | **engine yes, UI no** (§3.2) | Nov 11 |

### 8.4 Where the engine lives — owner Paul

`CLAUDE.md` keeps `src/` empty because *"DEC-002 is open; code now decides it by
accident."* #65 asks for a `src/` exception.

**Proposed: make the gate the property, not the date.** The reason `src/` is
closed is that code would decide DEC-002. A two-codec engine whose slice passes
under both (A2) demonstrably does not. So: the engine moves from `prototype/` to
`src/` **when A2 passes**, not when the DEC-002 ADR is accepted. Until then it
stays under `prototype/`. Separately, `src/mofn/__init__.py` should be deleted —
it is a stale file that contradicts the rule it was written under.

### 8.5 The backlog double-count — owner Paul · `BACKLOG-0001`

§3.2 proposes the resolution. Needs a yes, or a different cut; what it must not
stay is both-live, because I3 is being counted twice.

---

## 9. Already settled — stop re-asking these

Recorded so the wallet does not re-litigate them under a UI heading.

- **Two targets, not three** (MD-1). Email is a schema scenario.
- **No network, no registry, no transparency log in the verdict** (`ARCH-0001`
  NG4, `APP-0001` §5).
- **No revocation product.** Short expiry is the mechanism (`W-3`, R-O-02).
- **Keys are files.** No keychain product, no cloud custody.
- **No knowledge-graph engine** (`PLAN-0004` §2).
- **No cryptographic primitives of our own**, ever.
- **A graphic UI is in scope**; a web UI and a server are not. `APP-0001` §5
  still reads "No web UI, no server" alongside a stale "No GUI" — `PLAN-0004`
  §8 already asks for that edit and it is still owed.
- **The authorization line is the product.** Everything else in the verdict is
  available elsewhere.

---

## 10. Risks

| risk | signal it is happening | response |
|---|---|---|
| **W-1 does not start** | no commit by Oct 19 | the §5.3 contract is already the hedge — the GUI proceeds on goldens. If Oct 19 passes with no contract either, reassign the contract, not the engine |
| GUI eats I4–I5 | framework still unconfirmed after Oct 14 | take §8.1's fallback by default; two screens, not five |
| The prototype encoding becomes the format by accident | the second codec is "added later" | A2 is a CI gate from the first engine PR, not an end-state |
| Type-specific code creeps into the views | the archives domain needs "a small change" in Nov | A4 is a grep test and it fails the PR |
| The verdict shape drifts between CLI and GUI | two renderers | A6; the GUI renders the engine's JSON and formats nothing itself |
| Packaging eats December | installer work before Dec 1 | `PLAN-0001` §12 risk 10 stands: single-file zipapp, not an installer |

---

## 11. What this plan does not do

It does not accept `DEC-002`, `DEC-003`, `DEC-004`, `DEC-005`, `DEC-007`,
`DEC-008`, P4, P7, the v0.2.0 proposal, or a GUI framework. It does not edit
`APP-0001`, `PLAN-0004`, `BACKLOG-0001` or `DECISIONS-0001` — the fixes it
expects in those files are listed in §8 and §9 and belong in their own changes,
reviewed by their owners.
