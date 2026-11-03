---
schema: "design-log/v1"
id: DL-0020
part: review
date: "2026-11-01"
---

# DL-0020 — review

**Human input so far: three instructions.** Chip said to answer as recommended,
using the records and evidence; then to add Chip as a decision maker on the
three SPECs; then, on 2026-11-03, to accept the spec diffs. Chip took the
recommendations as a whole and has not reviewed each answer below line by line.
Review of the code is pending on the PR.

## Authority

- **The delegation does not cover these.** ARCH-0001 `decision_makers` (added in
  0.1.4, unchanged in 0.1.5) gives `ndewedo-newbury` authority to accept, by ADR
  under §9.2, the open decisions in §7, excluding ADR-0002. A1, C1, C4 and the
  items below are not §7 decisions, and there is no ADR. **Nothing here relies on
  the delegation**, and it would not stretch to them.
- **What they are.** W-1 implementation decisions, taken by Chip because the
  human asked and the engine needs answers. A1 was addressed to Paul, the C-items
  were held for him, and the engine's owner is David. Any of them can be reversed
  in review.
- **Spec text: accepted 2026-11-03 by `ndewedo-newbury`.** It was proposal only
  while SPEC-0002, SPEC-0003 and SPEC-0004 named only the sponsor. Once Chip was
  added (next point), Chip accepted SPEC-0002 0.4.0, SPEC-0003 0.1.1 and
  SPEC-0004 0.2.0 on mofn#125. They stay `reviewed: false`, `needs_review: true`:
  acceptance by a decision maker is not a second reader's review, and the
  sponsor may still reverse it.
- **Added as a decision maker, 2026-11-03.** Chip then told the agent: "add me
  as a decision maker for those specs and DECISIONS-0001". SPEC-0002 0.4.1,
  SPEC-0003 0.1.2 and SPEC-0004 0.2.1 list `ndewedo-newbury` alongside the
  sponsor; DECISIONS-0001 0.4.1 extends the authority line to match. The agent
  wrote the `authority:` text to say what happened: the instruction came from
  Chip, and no sponsor confirmation is recorded. *Rejected:* wording it as a
  sponsor delegation like v0.3.4's, because nothing on record shows one. So
  Chip can now accept these diffs; the point above still describes their state
  until Chip, or the sponsor, does.
- **No DEC-* is accepted or narrowed.** DEC-001, DEC-004, DEC-005 and DEC-007
  stay open.
- **An unmet condition in the delegation.** Its text says "the sponsor confirms on
  the PR that adds this entry". mofn#116 asked him to. Its timeline shows David's
  approval and Chip's merge, and no comment or review from the sponsor. ADR-0004
  and ADR-0005 rest on that entry, so this matters beyond W-1.

## Decisions

### A1 — what each `check` line reports

**Answer.** SPEC-0004 §10.4's line meanings, plus one addition: integrity also
re-hashes the relying party's copy. Acceptance is **pass** when no template is
named. Authorization and acceptance are **not evaluated** when no verified
statement is about the file. This is what David's update of 2026-11-01 reports.

**Evidence.** SPEC-0004 is the newer document. Its Appendix A prints
`acceptance: pass # TV-4 names no template`. #65 requires `integrity FAIL` for a
changed file, and the slice's ③ shows it against the golden.

**Rejected.** APP-0001 §4's meanings: older, and they put a changed statement on
authenticity. "Not evaluated" for acceptance when no template is named: A1's own
first proposal, against Appendix A, rejected by David in DL-0016.

**Correction to the record.** A1 said no line fails for a changed file under
SPEC-0004, and DL-0016 repeats it for a subject taken from the statement. With
the subject taken from the file, §10.2 item 1 fails, so the authorization line
would fail by the letter of §10.4. The diff moves the report to integrity and
states why.

### C1 — the second codec

**Answer.** The human-review YAML form of SPEC-0002 §11, including `signed`.
This meets #65's "debug JSON/YAML codec". It is identified from DL-0016.

**Evidence.** TV-4's output equals §11.2's printed example; TV-1…8 round-trip
binary → YAML → binary byte for byte; the slice passes under it. It adds no
second signed format, as ADR-0003 D2 requires.

**Rejected.** A JSON codec: a second signed format against D2, and no spec says
how to spell one.

### C4 — the suite 1 library, and torsion keys

**Answer.** Keep PyNaCl (libsodium), including its stricter point check, and
propose that §6.3 say so: a key outside the prime-order subgroup MUST be rejected.
Identified from DL-0016 as the N-4/N-5 library choice plus the question it left.
C4's exact wording is not recoverable.

**Evidence.** DL-0016's experiment: only libsodium exposes a point check, so only
it meets N-4 without a hand-written check. New here: under a torsion key, 100 of
800 signatures pass both libraries' verify (`produced.md`), so a verifier reading
§6.3 as written and this engine disagree on one statement. A MUST closes that. An
honest key is never affected, and N-4 and N-5 keep their results.

**Rejected.** `cryptography`/OpenSSL: no point check. Leaving §6.3 alone with the
engine stricter: two conforming verifiers give different results. MAY reject: the
same split, allowed in writing. Dropping to a small-order check only: libsodium
exposes `is_valid_point`, not a check that stops there, so that needs a
hand-written one.

**For the sponsor.** §6.1 calls a suite "an immutable registry entry" and lists
verification rules in it. This changes suite 1's rules, which is defensible only
because the draft is `0.x`. Paul's call.

### C2, C3, C5 — not identified

**No answer, because the questions are unknown.** Searched: all of DL-0016, the
#65 comments, mofn#122 with its review and commits, `feat/wallet-engine` and
`plan/0006-wallet`, the README and code comments, `project/meetings/`, and earlier
local session transcripts. C1 and C4 are the only ones named. The `C1`–`C5` in
DL-0009 and R-0004 are other lists. DL-0016's "Open for the human" items do not
carry those labels, and mapping them across would be a guess, so they are decided
below under their own numbers. David holds the notes.

### DL-0016 open items, under their own numbers

| item | answer | evidence | rejected |
|---|---|---|---|
| **1a** target spelling | one-key map named by the target type, in §11.3 | what the codec does; TV-1…8 round-trip key, digest, statement and definition targets, and tests cover locator and description | a `type:` field in the map: longer, and §11.2's printed `{digest: …}` already has this shape |
| **1b** text that reads as `'0x…'` in a generic value | refuse to convert; the statement stays valid in binary; §11.1 notes the exception | `test_text_that_looks_like_bytes_is_refused_in_a_value`. Only generic `value` slots are affected | an escape syntax: invented, and maps are legal values, so a wrapper collides with them. Banning such text at V7: changes which binary statements are valid in order to suit a view of them. Silently reading it as bytes: the form would no longer be exact |
| **2** torsion | see C4 | | |
| **3** answer is yes only if all six lines pass | keep for v0. **No spec diff** | the only divergence from §10.2 is a key known only from an envelope `pub`, where §10.2 says yes while the authenticity line fails. Answering no is the safe side | changing §10.2 here: it changes an evaluation result, so it is Paul's. Relaxing the engine to §10.2: a yes beside a failed line |
| **4** golden ③ fixes the flip | flip that byte: first byte → `X`. No placeholder | the slice's ③ matches the golden byte for byte | a golden placeholder: a weaker comparison for no gain |
| **5** which YAML | YAML 1.2 core, restricted to what a 1.1 parser reads the same way; quote the Appendix A value | `produced.md` table. The form's rules already reject what makes the versions differ | declaring 1.1: `yes` becomes a boolean, and §11 would bless the older semantics. Plain 1.2 with a 1.2 parser: a new dependency to accept one unquoted `?`, and a 1.1 tool would still misread the same files |

Item 6 of DL-0016 was a note, not a question.

**Version numbers.** SPEC-0004's policy makes a change to an evaluation result
MAJOR. Read strictly, A1 is that: a line changes although the answer does not. But
1.0.0 would say the draft is final, and SPEC-0002 keeps "nothing is final until
its version leaves `0.x`". So 0.2.0, with the reasoning in its status section.

## Rejected for the slice

- **A second relying-party wallet for ②′.** Rejected: one wallet per role is the
  rule. Swapping one label in the comparison costs a `sed`.
- **A new golden for the key-holder.** Rejected: it would differ from
  `unauthorized.txt` only by a label, and two files then drift.
- **`pip install` or creating a venv inside the script.** Rejected: "no network".
  The script checks that its prerequisites import, and stops with a pointer.
- **Passphrase from an environment variable or argument.** Rejected: A3.
  `printf` is a shell builtin, so it shows in no process list.
- **Testing only for the word `fail`.** Rejected: the brief says compare with the
  goldens, and a grep passes a wrong sentence.
- **Trusting one wallet per role by convention.** Rejected: the two signing
  wallets are made unreadable, so sharing fails rather than goes unnoticed.

## Not decided here

- **A2 and A3** were also "please decide" and got no reply. The engine follows
  both proposals, and the slice relies on A3. The brief named A1 and C1–C5, so
  these are left open.
- **APP-0001 §3 and §4** still show the old line meanings and flags, including
  `not evaluated` for acceptance. B2 promised an update.

## Numbering

mofn#118 holds `0018`, and mofn#124 (T-031) holds `0019` and SPEC-0002 0.3.0. So
this entry is `0020` and its SPEC-0002 is 0.4.0, whichever merges first. If this
merges before mofn#124, that PR's status line conflicts with this one; the fix is
to keep both lines, in version order.
