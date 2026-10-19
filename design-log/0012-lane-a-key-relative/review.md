---
schema: "design-log/v1"
id: DL-0012
part: review
date: "2026-10-19"
---

# DL-0012 — review

**Human review of the results is pending.** The human has not yet read the
`04` table or the rewritten findings. Below is only what was actually decided
or rejected so far.

## Rejected by the human

1. **A rewrite of `01`'s `build_eddsa` docstring.** The plan proposed
   rewording it. The human rejected that: *"don't change original meaning …
   but can improve, don't add comment inside function, keep comment EASY to
   understand, don't use wierd vocabulary."* The docstring was tidied only
   (typo, sentence form). The same rule was applied to `04`: no comments inside
   functions, plain words.
2. **Opening a PR and touching the library repo** in this session. The issue's
   required output (library records, the `namespace-governance` topic
   `answer`) is therefore **not** in this change.
3. **Committing.** Offered a local signed-off commit; the human chose to leave
   the work uncommitted for their own review.

## Chosen by the human

- **Consumers:** pycose + `in-toto-attestation`, over pycose only (no
  in-toto reader at all) and over adding the `slsa-verifier` binary (heavier).
  The cost of that choice is in the README: `in-toto-attestation` checks very
  little, so its "yes" rows say little about a strict verifier.

## Rejected by the model's own runs — passes for the wrong reason

Same lesson as DL-0007: a check that passes by accident is not evidence.

1. **`payloadType` first reported "validate() passed".** True, but
   meaningless — `in-toto-attestation` never reads the envelope, so it never
   saw the changed value. The row now says *not tested*.
2. **COSE labels 3 and 4 first reported plain "verified".** pycose keeps an
   unknown header label and ignores it. "Accepted" there means "not
   understood", so the row now says so.

## Open for the human

- `01`'s docstring says the signature covers "the two headers and the
  payload". In COSE_Sign1 only the **protected** header is signed (with the
  payload); the unprotected header is not. The meaning was kept as instructed —
  the human should decide whether to correct it.
- Whether the "Not tested" list is enough, or `slsa-verifier` should be run
  before the topic `answer` is written.
