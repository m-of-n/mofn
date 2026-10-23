---
schema: "design-log/v1"
id: DL-0014
part: review
date: "2026-10-23"
---

# DL-0014 — what a human decided, and what the model rejected

**Status: human review of the output is PENDING** on the PR that carries this
entry. Written in the same change per the `DL-0001` rule. Nothing here predicts
the reviewer's verdict.

## 1. Decided by the human

- **Cross-link #110 and #112 before working either.** The model proposed it; the
  human directed it ("complete next steps for me") and, when the auto-mode
  classifier refused the external write, **posted both comments themselves**.
  The comments fix the sequencing this PR follows: #112's DEC-003 work lands
  before #110's COSE_Sign1 + CWT row, and the two stay in separate PRs.
- **"Now complete #112."** Scope was the human's; the reading of "complete" as
  *verdict per checkbox, text where text is owed* was the model's and is open to
  correction here.

## 2. Rejected by the model, and why

Recorded because the omissions are decisions, not oversights.

| considered | rejected because |
|---|---|
| **Write the DEC-002 / DEC-003 ADRs** — #112's "closed as each ADR is amended" | an agent never writes an ADR unprompted or accepts a DEC (`propose-arch`); register item 4b is the human's instrument |
| **Re-rank DEC-002's options** on `rfc-8747` cut B | the issue's framing forbids "this decision is wrong"; and for native objects `SPEC-0002` §4.3 already makes the divergence a rejection, so the cut corroborates `DECISIONS-0001`'s existing *difference in kind* rather than reversing anything. Recorded as a driver the ADR scores, not as a ranking |
| **Amend the §6 COSE_Sign1 + CWT row** with the `kid` and `cnf` rules | mofn#110's lane, per the comments the human posted. P1.1 states the rules and points at the row |
| **Edit accepted P1 in place** | P1 is accepted by `ADR-0001`; a change there needs an ADR. P1.1 is a separate `[draft]` clause, the P5 → P5.1 pattern |
| **Add the suite code to the `kid` preimage** | answers a question the DEC-003 ADR owns, and imports our own registry into the identifier (`produced.md`) |
| **Add a threshold vector to `spec/vectors/ksa-core/`** | vectors are T-031's deliverable; the ARCH text now says the vector is missing and who owns the check |
| **Bump the library pin** | mofn#113 does it. This PR cites records at `bafd536` and depends on #113 landing |
| **Put the verdict table only in the PR body** | working agreement 3; the table is here, and each verdict's text is in ARCH |

## 3. Where the model nearly went wrong

Read alone, `ARCH-0001` §7 lists four DEC-002 options and no option 5; #112's
"option 5", "MD-3" and the encoding profile live in the v0.2.0 proposal,
`DECISIONS-0001` and `SPEC-0002`. A model working from ARCH-0001 only would
have judged every #112 item a gap and proposed text `SPEC-0002` already
contains. **Most #112 items survive because `SPEC-0002` answered them first**;
the gaps are in the architecture record, not the specification. `ARCH-0001`
still does not mention option 5 or `ADR-0003` — register item 4, not touched
here.

## 4. Open for the reviewer

1. Is P1.1's import rule (*report, never adopt* a disagreeing foreign `kid`)
   right, or should a disagreement reject the import, as P5.2 rejects unknown
   DSSE exterior fields?
2. Is 0.1.3 (PATCH) right for ARCH-0001, given §7 text was added? The choice
   follows 0.1.2's precedent and keeps 0.2.0 for the proposal.
