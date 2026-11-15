---
schema: "design-log/v1"
id: DL-0046
part: review
date: "2026-11-15"
---

# DL-0046 — review

**Human verdict:** pending (PR review).

## What the human decided

- **Merge mofn#168 (W-3) now** (ndewedo-newbury, 2026-11-15), so that W-2b
  could start on the engine it depends on. Rejected: stacking W-2b on the
  open branch, and waiting.
- **The one archives vocabulary takes the demo's values,
  `reviewed · summarized · unverified`** (ndewedo-newbury, 2026-11-15).
  Rejected: DV-3's `yes · partial · no` with a separate `summarized` type,
  which was DL-0033's example, and DV-3's values alone, which drops
  `summarized` and departs from #66's list again (the reason DL-0033 rejected
  option B).

## What the agent rejected, and why

- **Editing DV-3 in place.** It would change hashed bytes that TV-21…26,
  E-5…E-7 and ARCH-0001 §2.3.2 depend on. SPEC-0002 calls that MAJOR. A new
  version is additive.
- **Keeping `archives` v1 as the demo vocabulary and regenerating it.** That
  leaves two vocabularies, which is what W-2b exists to end.
- **Making Dave's key importable as an owned persona,** so the demo could
  delegate as the definer. It would add a private-key import to `cli.py`
  (engine work, and a command that takes a secret), and W-2's rule is no
  engine change for a domain.
- **Moving ARCH-0001 §2.3.2's AR-1…AR-3 to DV-5 in this change.** ARCH-0001
  is changed by proposal only (§9.4, the `propose-arch` skill). DV-3 is still
  published and its rows are still true. Left as the next step.
- **Redrawing APP-0004's archives wireframes now.** The views are built in I5
  (Dec 1–4) by their owner. A note marks the sketches as v1.
- **Adding archives asks to SPEC-0004 Appendix A.** E-5…E-7 are not there
  either. The evaluations live in `vectors.json`.

## Found, not fixed

- **F-6 (APP-0003).** When an issuer's value is outside its delegated range,
  the authorization line does not name the hop the range came from. The
  expired case does name it. This is wording in `engine/check.py`, for its
  owner.
