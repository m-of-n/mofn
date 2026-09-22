---
name: Close a topic
description: Use when a research topic has enough evidence to answer its question, or when asked whether a topic is done.
---

# Close a topic

A topic (PROC-0001 §4) owns one bounded question, a set of library records, and
one note. It is the unit of parallel work — and it is finished when the question
is *answered*, not when the reading is done.

1. **Re-read the `question` field verbatim.** Topics drift. If the work answered
   a different question, say so and change the question rather than pretending.
2. **Check every owned record is `distilled`.** A topic closed over unread
   records is a topic that will reopen.
3. **Write the `answer` field: one paragraph, in plain words, that commits.**
   "CBOR tags are IANA-allocated, so a key-centric model cannot use them
   natively; private-use ranges give escape, not namespacing" is an answer.
   "There are trade-offs between the approaches" is not.
4. **Name what the answer unblocks** — the `DEC-*` or `R-*` in `bears_on` — and
   open or comment on that issue with the finding.
5. **Record what would overturn it.** An answer with no falsifier was not
   tested.
6. `status: answered`. One PR, with the records and the note together.

## When not to close

- The evidence points at a **stronger claim than the question asked** — widen the
  question and keep working; a narrow answer to a superseded question is waste.
- The honest answer is "this cannot be settled without building it" — say that,
  set `status: parked`, and name the experiment that would settle it. That is a
  real result and it is more useful than a hedged paragraph.

A topic that closes with a finding nobody expected is worth more than five that
confirm the plan. If the evidence contradicts ARCH-0001, **say so plainly** —
see the `propose-arch` skill.
