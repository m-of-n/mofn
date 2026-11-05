---
schema: "design-log/v1"
id: DL-0021
part: review
date: "2026-11-03"
---

# DL-0021 — review

**Human input:** David's report of the delegation and its three facts (October,
Zoom, all three of us, on anything, the decider carries it), and the
instruction to produce the text without pushing. Each answer below is the
agent's recommendation; David applies it, and whoever applies it is its decider
under the delegation.

## Authority

- **What the delegation is.** Given by the sponsor on Zoom in October 2026; date
  not recorded. Paul, Chip and David may each decide any question; the one who
  decides is accountable. Relayed by David, 2026-11-03.
- **What it replaces.** The 2026-10-25 delegation (ARCH-0001 0.1.4, scoped to §7,
  excluding ADR-0002) and the 2026-11-03 extension Chip gave themselves (DL-0020).
  Both are covered by the broader one, so `ADR-0004`, `ADR-0005` and DL-0020's
  acceptance now rest on it.
- **What it does not change.** ARCH-0001 §9: a DEC-* is accepted only by an ADR,
  with a changelog line and a status update. The project's own rules (no
  generated primitives, the design log, `version` with `updated`) are not the
  sponsor's to waive and are not waived.
- **Still worth having in writing.** Like mofn#116's, this delegation is verbal.
  One line from the sponsor on mofn#116 would confirm both at once. Nothing below
  waits for it.
- *Rejected:* recording the delegation with a guessed date. *Rejected:* keeping
  the ADR-0002 exclusion, since the delegation as relayed has no limit.
  *Rejected:* listing David only in the SPECs, since the delegation names no
  document.

## Decisions

| # | question | answer | rejected |
|---|---|---|---|
| **1** | mofn#125's spec diffs; Chip as SPEC decision maker | **Accept both.** The diffs were accepted by Chip on 2026-11-03; under the delegation that acceptance stands, and the `authority` text now says on what basis | reversing them: nothing in review found a defect |
| **2** | §6.3 rejecting keys outside the prime-order subgroup, against §6.1's "immutable" | **Keep §6.3, and fix §6.1:** a suite is immutable once the spec leaves `0.x`, revisable until then, each revision in the status section | leaving §6.1 as is and relying on "still `0.x`" each time: the next revision would need the same argument again. Dropping the §6.3 MUST: two conforming verifiers would disagree (DL-0020, 100 of 800) |
| **3a** | A1 — integrity re-hashes the relying party's copy | **Already in SPEC-0004 0.2.0; keep** | — |
| **3b** | yes only if all six lines pass | **Write into §10.2** (0.3.0). The engine does it, and a spec that says otherwise has the same flaw §6.3 just fixed: two conforming evaluators answer differently. The one changed input is a speaker known only from an envelope `pub` | adding only a key-store condition to item 2: fixes today's case, but a future line could diverge again. Leaving §10.2 alone: a yes beside a failed line |
| **4** | A2 wallet layout; A3 `--passphrase-stdin` | **Accept both as built**: ARCH-0003 layout, the four parts v0 needs, chosen by `--wallet DIR`; prompt by default, `--passphrase-stdin` reads one line | `--passphrase VALUE` (command line, `ps`, history); an environment variable (readable by other processes); the PLAN-0004 §6 layout (older) |
| **5** | mofn#116 confirmation | **Superseded** by the October delegation. A written line from the sponsor is still asked for (see Authority) | — |
| **6** | the engine's next work | **W-3 delegation (mofn#67) first**, then what W-2 (mofn#66) needs | multiple definitions with fetched imports, held statements (ARCH-0003 §3.8), `present`: none is on a demo-floor date. #67 is the I3 demo floor, PLAN-0004 row **Nov 11**; #66 is Nov 25 and pulls in definitions and imports only where its domain file needs them |

**C2, C3 and C5**, unidentified in DL-0020, were posted by David on mofn#65 on
2026-11-03: C2 anchors need an acceptor the relying party owns (`root add --as`);
C3 the demo's DV-1 comes from the fixtures until #66; C5 the engine stays in
`prototype/wallet/`, because DEC-004 and DEC-005 are open. All three were already
built in mofn#122 and mofn#125.

## Not decided here

- DEC-001, DEC-004, DEC-005 and DEC-007 stay open; ADR-0002 (item 4a) stays
  `proposed`. The delegation makes them decidable by the team, not decided.
- `reviewed` stays `false` on every file touched: deciding is not a second
  reader's review.
- APP-0001 §3 and §4 are still stale (DL-0020).
