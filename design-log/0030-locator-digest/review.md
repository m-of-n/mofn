---
schema: "design-log/v1"
id: DL-0030
part: review
date: "2026-11-07"
---

# DL-0030 — review

**Human answer:** "go #144", in reply to the agent's recommendation (withdraw
type 5). The human gave no reasons of their own. The reasons below are the
agent's, and the human can reject them in PR review.

## What was rejected, and why

- **An `aliases` set** (issue option 1). `ARCH-0001` §5.5 already lists
  `aliases` as having no KSA form "until a consumer needs it". Inventing the
  form here, to rescue one target type, would decide the aliases question as a
  side effect.
- **A second target** (option 2). `this` is one target throughout `SPEC-0002`
  §7–§9 and in `SPEC-0004` §10.1's `subject`. Making it a list changes every
  kind's target rule (§8.1) to save a type nobody uses: no vector, definition or
  golden uses type 5.
- **A body field** (option 3). It would put an extension field on a closed map,
  and §7.1 says all extensibility is through attributes (`ADR-0003` D1). An
  attribute already does the job, with nothing added.
- **Keep type 5 but require a digest elsewhere** (options 1–3 in general). The
  locator would stay the *target*, which is the definitional role R-M-11
  forbids it. Requiring a digest beside it makes the digest the real subject
  anyway.
- **Loosen R-M-07 to SHOULD.** Rejected by the human in `DL-0028`; not
  reopened.

## What the agent did not do

- **`ARCH-0003` §3.7** still lists `locator(uri)` as a `Target`. It is not
  edited: its only decision maker is the sponsor, and it defers to the SPECs.
  Owed to a sponsor-approved PATCH.
- No positive vector shows a locator carried as an attribute. That needs a
  definition with a locator type, and DV-1 and DV-2 have none. Owed if a demo
  needs one.
- §13.10's description-as-URI caveat is a SHOULD on definers, not a
  verifier check. Whether `SPEC-0003` should forbid such types is open.

## Owed

- A second reader for the `SPEC-0002` §7.2 and §13.10 text.
- `ARCH-0003` §3.7 PATCH (sponsor).
