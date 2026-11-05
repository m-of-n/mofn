---
schema: "design-log/v1"
id: DL-0012
part: review
date: "2026-10-19"
---

# DL-0012 — review

**Reviewed by the human on 2026-11-05; DL-0012 is closed.** The first session
(2026-10-19) is recorded below as it happened. The review of the results is in
the section after it.

## Session 1 (2026-10-19)

### Rejected by the human

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

The human later committed the work and opened mofn#109, which merged on
2026-10-20. Items 2 and 3 applied to that session only. The library records
and the topic `answer` are still not written.

### Chosen by the human

- **Consumers:** pycose + `in-toto-attestation`, over pycose only (no
  in-toto reader at all) and over adding the `slsa-verifier` binary (heavier).
  The cost of that choice is in the README: `in-toto-attestation` checks very
  little, so its "yes" rows say little about a strict verifier.

### Rejected by the model's own runs — passes for the wrong reason

Same lesson as DL-0007: a check that passes by accident is not evidence.

1. **`payloadType` first reported "validate() passed".** True, but
   meaningless — `in-toto-attestation` never reads the envelope, so it never
   saw the changed value. The row now says *not tested*.
2. **COSE labels 3 and 4 first reported plain "verified".** pycose keeps an
   unknown header label and ignores it. "Accepted" there means "not
   understood", so the row now says so.

## Review of the results (2026-11-05)

The model listed fourteen items for the human to accept or reject. Numbers
are the ones the human answered.

### Accepted as written

1. The `04` table (15 rows) as the evidence for mofn#13.
2. The signature never breaks; the reader does.
3. COSE breaks where pycose uses the identifier (alg label, alg value, content
   format); labels 3 and 4 are kept and ignored without an error.
4. in-toto rejects only `_type`; the `predicateType`, `sha256`, `buildType`
   and `builder.id` rows show nothing yet, because `validate()` does not check
   them.
5. The `payloadType` row stays *not tested*.
6. Key-relative names fit inside the payload; the envelope keeps registry
   identifiers. Since accepted in ADR-0004 ("COSE/DSSE for export only"); this
   table is now evidence behind it, not a guess.

### Accepted with a change

7. **The tag 18 row, reworded.** It read as if COSE required the tag. The
   rejection is pycose's choice: RFC 9052 §2 allows untagged COSE_Sign1 when
   the protocol says what the message is. README finding 3 and `produced.md`
   now say so.
8. **The placeholder stays a placeholder, with one line added.** The first
   half, SHA-256 of the raw 32-octet Ed25519 public key (RFC 8032 §5.1.2),
   equals `ADR-0005`'s `kid`. The `[kid, label]` pair form is still not
   decided. Added to the README's "Not tested" list and to `produced.md`.
9. **`01`'s docstring corrected.** It said the signature covers "the two
   headers and the payload". Only the protected header and the payload are
   signed. The human ruled it a factual error, so fixing it keeps the meaning.
   This narrows session 1's rule ("don't change original meaning"): a wrong
   fact is not meaning to be kept.

### Rejected, and why

10. **Adding a COSE `crit` row.** Rejected: `crit` is an export question, so it
    is tracked under DEC-005 instead of tested here. It stays on "Not tested",
    with that reason.
11. **Adding CWT claim rows.** Rejected: `ADR-0004` makes CWT an export-only
    concern. It stays on "Not tested", with that reason.
12. **Running `slsa-verifier`.** Rejected: it only verifies Sigstore-signed
    provenance, so on our self-signed samples it would fail at the certificate
    before reading `predicateType` or `builder.id` — a failure for the wrong
    reason. The README now gives this reason in place of "has not been run".

### Housekeeping

13. The note that mofn#109 merged on 2026-10-20 is added under session 1.
14. DL-0012 is closed: `question.md` is `status: complete`.

### Model errors in this review

- **`slsa-verifier` was first listed as a decision for the human.** The human
  asked why it could not simply be run. The real reason was technical, not a
  preference: it cannot read self-signed samples at all (item 12). The model
  should have said so the first time instead of handing it over as a choice.
