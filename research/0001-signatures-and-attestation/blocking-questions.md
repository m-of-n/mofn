# Blocking questions

Per sponsor direction: **catalogue blocking questions and move to the next item.**
Nothing here stops the survey; each is a place where the draft states an
assumption that a person must confirm.

| # | question | blocks | current assumption |
|---|---|---|---|
| Q1 | **Venue and length.** A workshop paper is ~8 pages; a journal survey is 30+. Eight areas at survey depth is closer to the latter. | final scope of §§4–10 | Writing to *thorough*, then cutting to a named target once one exists |
| Q2 | **Authorship and attribution.** Sponsor, students, and an AI-assisted method that the project claims as a contribution. How is that stated on a paper? | title block | Left as `<pending>`; an honest methods note is drafted but unattributed |
| Q3 | **Is this the CS690 D3 *mechanism* report, or separate?** `PLAN-0001` D3 already specifies a mechanism report with overlapping scope. | whether D3 is now done | Treating R-001 as a superset; D3 can cite it |
| Q4 | **How far does "extract requirements" go for X.509?** RFC 5280 has hundreds of normative statements. | area B depth | Extracting 10–20 most consequential on path validation, name constraints, revocation |
| Q5 | **Does the paper argue a position, or only classify?** A survey that merely classifies is safer; one that argues is more useful and more attackable. | §12 open problems | Classifying in §§4–10, arguing only in §12, with the argument clearly marked as ours |

## Resolved in this pass

- **Q4 is answered by the evidence rather than by a judgement call.** Area B
  extracted **43 requirements** from RFC 5280 and the CA/B Forum baseline
  requirements, each with verbatim text, section locator, RFC 2119 verb and
  actor, grouped as path validation (10), name constraints (15) and revocation
  (13+). That is the consequential set: it covers every normative statement the
  survey's §4 argument depends on. They are in `mini-reports/B-x509-pkix.md` §3
  and should seed the first distilled library record. Q4 no longer blocks.
- **Q5 resolved toward arguing.** The draft classifies in §§4–10 and argues in
  §11–§13, with every argumentative claim marked as the survey's own and
  supported by primary sources. The §11.2 findings and the §13 conclusion are
  positions, not classifications. This is the more attackable choice and the
  more useful one; §1.3 states it openly so a reviewer is not ambushed.

## New questions from this pass

| # | question | blocks | current assumption |
|---|---|---|---|
| Q6 | **Does the original measurement (§4.5) stay in a survey?** Surveys do not normally contain new measurements. It closes a real gap — no published name-constraint prevalence figure was found — but it changes the paper's genre, and a reviewer may say so. | §4.5, and how the abstract is worded | Keeping it, framed as "the literature had no answer, so we measured." Alternative: split it into a short companion measurement note and cite it. |
| Q7 | **Is the C2PA-versus-PICS finding the paper's headline, or one section among eight?** It is the sharpest result and the closest to the project's own thesis, which cuts both ways — it is also where we are least disinterested. | title, abstract emphasis | Presented as one finding of four in §11.2, not as the headline, precisely because it is the one we have an interest in. |
| Q8 | **Do we publish the mini-reports?** They are 31,000 words of verified research with their own "could not establish" sections, and they are more useful to a reader than the paper's citations alone. But they are AI-lane output, not peer-reviewed prose. | repo layout, Pages build | Committed to the repo as working papers, not linked from the published site until a person has read them. |
| Q9 | **Seven of eight lanes exhausted their search budget.** Several open items in `unverified.md` are recoverable with a fresh pass. Is that worth doing before review, or after? | whether `unverified.md` shrinks before a human reads it | Leaving it as-is for review, because the register is itself informative about method. |

**None of these block.** The draft is complete and internally consistent under
the assumptions stated in each row.
