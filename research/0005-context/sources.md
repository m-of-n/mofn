---
schema: "library-doc/v1"
id: R-0005-sources
title: "Sources consulted — context"
type: evidence
status: draft
version: "0.1.2"
date: "2026-10-14"
updated: "2026-10-17"
---

# Sources

Bibliography pinned at **`library@60b3284`**. Every `[@key]` in `report.md`
resolves to a record directory at that commit; the mapping was checked
mechanically, and **101 distinct keys resolve with zero unresolved.**

> **Corrected 2026-10-16.** This file previously said *72 distinct keys*. The
> count was wrong, not the resolution: the counting pass missed multi-key
> citations of the form `[@a; @b]`, of which `report.md` has several. Re-counted
> at the current pin by parsing every bracketed group containing `@` and
> splitting on `;` — 80 bracket groups, 109 citations, 101 distinct keys, zero
> unresolved. The pin itself moved `f57dcbc` → `60b3284` when this branch was
> rebased onto the KSA specifications.

## 1. The sourcing situation, stated plainly

**No source was retrieved over HTTP for this report.** It is a synthesis pass
over material already in the repository and the library, and `searches.md`
records the absence as a method limitation rather than a gap in the write-up.

That means this file cannot do what `R-0004-sources` does — list fresh
retrievals with digests and retrieval dates — because there were none. What it
can do, and what matters for review, is say **which prior pass each claim's
evidence comes from**, so a reviewer can go to the retrieval record rather than
to this report.

## 2. Where the evidence actually came from

| §in report.md | evidence | its retrieval record |
|---|---|---|
| §2 the narrow guarantee | R-001 §2 in full | `research/0001-signatures-and-attestation/sources.md`, `searches.md` |
| §3.1 the four incidents | R-001 §8.1, §8.6; R-0004 §3 | R-001 and `research/0004-uptake-and-applications/sources.md` |
| §3.2 statute | R-001 §8.4; R-0004 §3, §5 | as above |
| §3.3 cost of signing | R-001 §8.2; **R-0004 §3.2's npm measurement** | `research/0004-uptake-and-applications/` — the measurement is original there |
| §3.4 agentic delegation | R-001 §9.2 | R-001 |
| §4 the five axes | R-001 §3, §11.1 | R-001 |
| §5.1 X.509 | R-001 §4.1–4.9; **the 1,769-certificate measurement is R-001 §4.5's own** | R-001; `[@survey-2026-nameconstraints-measurement]` is the record of it |
| §5.2 OpenPGP | R-001 §5.2 | R-001 |
| §5.3 SDSI/SPKI | R-001 §5.3–5.7 | R-001 |
| §5.4 PICS | R-001 §6.1–6.4 | R-001 |
| §6 the two conflations | R-001 §11.3 | R-001 |
| §7 the gap | R-001 §11.4, §12 | R-001 |
| §8 the counter-argument | **R-0004 §8** | R-0004 |

## 3. Claims deliberately not made

Three things a context report is tempted to assert and this one does not,
because the primary source was not re-checked in this pass:

1. **No adoption percentage is stated in this report's own voice.** Every
   number in §3.3 and §5.1 is attributed to R-001 §4.5 or R-0004 §3, which are
   where the measurement and its method live.
2. **No claim about C2PA platform or newsroom deployment.** R-001 §6.7 records
   that those could not be established from primary sources, and R-0004 §4
   supplies what could. This report cites neither beyond what those two state.
3. **No priority claim in signature history.** R-001 §2.6's contested-attribution
   note governs, and §2.1 here is written to stay inside it.

## 4. Ingestion candidates

**None.** This pass retrieved nothing, so it generated no un-recorded source.
That is the one advantage of a synthesis pass: it cannot create bibliographic
debt.

## 5. Unverified register

**None, and the absence is deliberate rather than overlooked** (#99 §7 asks for
`unverified.md` *if anything could not be sourced primarily*).

- This pass retrieved nothing (§1), so it produced no claim of its own whose
  primary source went unchecked. Every claim routes to an upstream pass (§2),
  and those passes keep the registers:
  `research/0001-signatures-and-attestation/unverified.md` and
  `research/0004-uptake-and-applications/unverified.md`.
- The three claims this report *would* have needed a register for are
  withheld, not stated (§3).
- Checked 2026-10-17: no item in either upstream register is stated as fact in
  `report.md`. The nearest passages stay inside the caveats — the SPKI working
  group is "recorded as concluded" with no date (R-001 register §C); Rabin is
  cited without pagination (§A); OpenPGP trust signatures are described from
  the specification with no adoption figure (§C); RFC 9162 is cited beside
  RFC 6962, not as the deployed CT standard (§B).
