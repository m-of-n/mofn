---
schema: "design-log/v1"
id: DL-0057
part: review
date: "2026-11-25"
---

# DL-0057 — review

**Human verdict so far:** the sponsor reopened the ADR and named three
objections and one process concern (question.md). Everything else here is the
agent's choice, for the reviewer.

## What the agent chose, and what it rejected

- **Status `proposed`, not `superseded` or `withdrawn`.** Nothing replaces
  P2, P3 or P6 yet, and the sponsor did not say what should. `superseded` would
  need a successor; `withdrawn` would erase an accepted ADR's record.
  *Rejected:* a new status word `reopened`. The validator and the register know
  `proposed`, `accepted`, `superseded`, `draft` and `active`; a `reopened:`
  front-matter key carries the fact without a new state.
- **`decision_makers` emptied; the old acceptance kept under
  `previous_acceptance`.** §7 of the ADR argued that a name in that field with
  no act behind it is a false provenance record. Leaving the 2026-11-06 name
  there on a `proposed` ADR would say the opposite of the status.
  *Rejected:* deleting the 2026-11-06 text. It is history, and the design log
  exists to keep it.
- **P5 left alone.** The sponsor objected to P2, P3 and P6 and to the process.
  Not to P5. But P5 was accepted by the same ADR, so its acceptance now rests
  on a `proposed` document. The agent held its standing rather than ruling
  either way, and said so in the ADR and ARCH-0002.
  *Rejected:* marking P5 `[reopened]` (it would object on the sponsor's behalf);
  marking it flatly `[accepted]` with no note (the dangling dependency would be
  invisible).
- **The other accepted ADRs were not edited.** `ADR-0006`, `ADR-0007` and
  `ADR-0008` cite P3 or P6 as accepted, and `ADR-0004` cites P5.1. An accepted
  ADR changes only by superseding, and the task said not to change their
  status. They are listed in `ADR-0002` §10.3 as flagged dependents.
  *Rejected:* adding "reopened" notes inside them, which would be edits to
  accepted decisions without a decision maker.
- **The gap analysis is in the design log, not under `project/` or `research/`.**
  `bin/validate-archdoc` admits fixed id kinds, and `bin/manifest` publishes
  every document under `project/` and `spec/` to the public site, drafts
  included. An analysis of how the project's own decision process went wrong
  should be reviewed by the sponsor before it is on the site. The design log is
  the repository's home for AI-produced analysis with its human review, and it
  is not published. *Rejected:* adding a `REVIEW` id kind to the validator for
  one document.
- **ARCH-0002 bumped MINOR (0.11.0), not PATCH.** The policy says PATCH is
  editorial. No wording changed, but the standing of three principles did.
- **No "fix" of P2, P3 or P6 text.** The agent did not propose replacement
  wording in the documents. The objection is that the base is inconsistent;
  rewording three principles one at a time repeats the cycle the sponsor
  objected to. The analysis proposes the order instead.

## For the reviewer

- Whether `ADR-0006`, `ADR-0007`, `ADR-0008` should be marked as under review
  now, by an explicit decision, rather than only listed.
- Whether the sponsor wants P5 reopened with the rest.
- Whether the plan in `analysis.md` §9 is the order of work, and who owns step 1.
