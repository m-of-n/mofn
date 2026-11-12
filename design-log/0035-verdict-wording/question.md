---
schema: "design-log/v1"
id: DL-0035
part: question
title: "Verdict wording: sentences about another file (F-1), the vacuous acceptance pass (F-2) — mofn#157"
date: "2026-11-11"
model: "claude-opus-5-5"
human: Ndewedo-Newbury
outcome: "SPEC-0004 0.5.0 §10.4 adds two rules about what the verdict prints; wallet 0.4.1 implements them; goldens updated. No line result, answer or exit code changes. No DEC-* touched."
status: open
---

# DL-0035 — question

## The brief

Chip (GitHub `Ndewedo-Newbury`) told the agent: *"you fix the F-1 and F-2 in
#157"*. mofn#157 was filed on 2026-11-10 by the agent for Chip, from the W-4
demo slice runs (mofn#68, DL-0029 session 2), and assigned to David, who owns
the engine. Chip took the fix over and asked the agent to make it. David
reviews.

- **F-1.** In golden ③ (`tampered`), the attestation sentence prints straight
  after `answer: no`. It is about the digest in the statement, not about the
  relying party's file, but nothing says so.
- **F-2.** `acceptance pass — no template is named` sits beside `answer: no`
  in ②, and reads as if a template was met.

## Context supplied

- mofn#157 and its options: F-1 (a) drop the sentence, (b) frame it; F-2
  (a) keep the pass and explain it, (b) make it `not evaluated`.
- SPEC-0004 §10.4 and Appendix A (`acceptance: pass # TV-4 names no
  template`).
- DL-0016 and DL-0020 A1, where "not evaluated" for acceptance with no
  template was proposed and rejected by David.
- APP-0003 finding F-3, which reports the same vacuous pass from the archives
  domain.
- `prototype/wallet/engine/check.py`, `render.py`, `screens/forms.py`, and
  the goldens.
