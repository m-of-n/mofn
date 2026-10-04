---
schema: "design-log/v1"
id: DL-0004
part: review
date: "2026-10-03"
---

# DL-0004 — review

## Rejected — the author model's own claims, overturned by extraction

Four. All were stated confidently to the human before the extraction ran, and
three of them would have reached the topic answer if the lane had stopped at
reading.

1. **"R-O-05 does not exist in the repository."** The model searched
   `ARCH-0001`, found §5.3 stops at R-O-04, reported the requirement absent,
   and advised the human to *ask the sponsor whether it exists on a branch*.
   It exists — `ARCH-0001-PROPOSAL-v0.2.0` §3.4 and §7, priority **M**, with
   the full argument at §3.4. **Rejected on the next turn** by reading the
   proposal file. *The failure was searching one document and concluding
   absence from the repository. The proposal is listed in `spec/` beside
   ARCH-0001 and was in the supplied context.*

2. **"JCS leaves the duplicate-key hole open."** Written into the first
   committed topic answer, as a point in favour of the reduced CBOR profile.
   **False.** RFC 8785 §3.1 requires I-JSON, under which *"JSON objects MUST
   NOT exhibit duplicate property names."* JCS closes it by constraining input.
   Corrected in `79c543a`. The *residual* problem is real but different: §5
   mandates a duplicate check that Appendix A's reference canonicaliser is
   structurally incapable of performing, because `JSON.parse` has already
   collapsed duplicates by the time it runs.

3. **"The IEEE 754 double limit disqualifies option 3."** Overstated, and the
   model had asserted it twice before the design-notes agent went field by
   field and overturned it: `Threshold.{k,n}`, digests, counters and `Validity`
   at second, millisecond or microsecond resolution all fit. The ceiling falls
   between microsecond and nanosecond time and nowhere else in the model. The
   genuine hazards were found only by extraction: Appendix B serialises
   `4430000000000000` — exactly 2^68 — as `295147905179352830000`, **a
   different integer**, silently, with a signature that verifies; and
   Appendix D's string-wrapping remedy is **itself not canonicalised**, so
   Appendix E's own example shows `"055"` becoming `"55"` under a different
   parser style. *The remedy fails the injectivity condition the answer is
   about.*

4. **"R-O-05 needs a companion rule requiring the verifier to re-encode and
   compare."** Proposed by the model as the fix for condition (2).
   **Rejected by the model's own later analysis**: re-encoding at verification
   drags the producer's canonicaliser back into the verifier, which is exactly
   what R-O-05 forbids and exactly the DSSE critique. Replaced by routing
   condition (2) to ARCH-0002 **P5**, which already obliges encoder *and*
   verifier to reject, and which the RFC 8949 extraction already uses for three
   of its fourteen open rows.

## Rejected — an agent's argument, by another agent

5. **"Reject option 3 because RFC 8785 is an Independent Submission."** The
   standing point is true — it is Informational and its BCP 14 force rests on a
   single lowercase sentence in §2 — and the author model had reached for it
   first. The design-notes agent argued explicitly that this is **the wrong
   reason**, and that the R-O-03 argument is that the number algorithm *is not
   in the cited document*: §3.2.2.3 declines to reproduce it and points at V8
   and Ryu, so citing RFC 8785 means citing three artifacts, one of them an
   edition of an annually revised standard. Accepted; the weaker argument was
   demoted in the answer.

## Rejected — 10 artifact defects, by the adversarial pass

Pass 2 did none of the extraction and was briefed to break it. It found 10 and
fixed 10. The one that matters:

> `schema/sorting.md` carried the Hebrew property name **decomposed** as
> `U+05D3 U+05BC` where §3.2.3's test vector specifies precomposed `U+FB33`.
> Wrong UTF-8 bytes, wrong UTF-16 length, and a wrong sort position.

**Signature-breaking, and committed inside the record that documents the
hazard** — `examples/README.md` warns about exactly this decomposition two
directories away. It is also, unplanned, the best evidence the lane produced
for condition (6): a normalising layer anywhere in a JCS pipeline breaks
signatures silently.

Also overturned: a stated "re-checkable" invariant that was simply false
(U+20AC claimed raw "in the four places the RFC prints it raw" — the RFC prints
it raw in 2, the vectors carry it in 6); a dropped `[IEEE754]` from inside
quotation marks; and three cases of extractor prose altered into or spliced
inside a `violates.rule` field that is verbatim everywhere else. That last
class is the `vCon 2026-09` splice failure, reproduced.

## Disagreement between agents, resolved mechanically

Pass 1 produced **two artifacts giving different counts** for Appendix B
Table 1 — one said 24 rows, one said 26. Neither was lying and agreement
between agents would have proved nothing either way. Resolved by parsing the
table: **26 data rows, 24 of which carry a serialization**; the NaN and
Infinity rows have an empty cell. Both figures now appear in the record and
each states which it means. *Two agents agreeing is not evidence; two agents
disagreeing is a prompt to go and count.*

## Accepted

The decomposition held. Six parallel extractors on one 984-line document was
not obviously proportionate, and it earned itself: the schema agent
brute-forced **275,145,156** name pairs to establish the exact boundary of the
UTF-16 versus code-point sorting divergence (every disagreeing pair has a
supplementary-plane character on one side and U+E000–U+FFFF on the other; no
BMP-only pair disagrees), and validated the derived number grammar against
499,848 binary64 values. Neither is a thing a reading pass produces.

The adversarial brief worked **because it named things to overturn** rather
than asking for confirmation. Every one of the five named targets came back
with a verdict, and one of them was a defect.

## Process failures recorded

**This entry was not written in the same change as the work.** Working
agreement #4 requires it; `79c543a` was committed and pushed to
`m-of-n/library` before this entry existed, and the entry lives in a separate
repository on branch `design-log-0004`. The two cannot share a commit:
`design-log/` is in `mofn/` and the output is in `library/`. The gap was
minutes rather than `DL-0001`'s week, and the prompts and rejections were still
in context — but the agreement as written is **not satisfiable** for any lane
whose output lands in the library, and that is a process defect to fix rather
than a lapse to excuse. Options: allow a cross-repo pair with the design-log
entry naming the library commit (what was done here), or move `design-log/`
into a repo that can see both.

**Three library defects were worked around before being filed.**
`bin/_yaml.py`'s block-scalar blindness was hit three separate times in this
lane — once by the author model, twice by agents — and each time the response
was a local workaround plus an in-file warning telling the next author not to
use `|` or `>`. It was only filed (`library#43`) after the verify agent
measured the blast radius: **36 of 44 FX-1 vectors read as the literal string
`"|-"`**, so CI over them is vacuous. A defect of the `U+FB33` class above
would not be caught today. *Three encounters before one issue is the finding.*

## Outcome

**No ADR. DEC-002 remains open.** The topic is `active`, not `answered`:
RFC 9804 is still `queued`, so `close-topic` step 2 is unmet and option 1
cannot be fairly scored against the six conditions.

**Decision 2 was asked about and deliberately not taken.** The human asked
whether R-O-05's scope amendment could be left untouched for now. The answer
given: yes for the acceptance of `v0.2.0`, but only because `src/` is empty by
design — that protection expires the day T-030 begins, so the scope clause must
land before implementation, not before Oct 28. **No amendment was drafted**, and
Tier 1 #4 is unchanged.

Decision 3 was taken: condition (2) extends **ARCH-0002 P5** rather than
minting R-O-07.

The lane feeds the **Oct 28 D5** package with the six-condition frame, the
option 3 withdrawal argument, and the namespace-governance point in option 3's
favour. The `propose-arch` diffs named in `produced.md` are not written.
