---
schema: "design-log/v1"
id: DL-0035
part: review
date: "2026-11-11"
---

# DL-0035 — review

**Human input:** Chip asked for the fix without choosing between the options in
mofn#157; the choices below are the agent's. Chip has not reviewed them line
by line. **Review pending:** David (engine owner, mofn#157 assignee) on the PR.
SPEC-0004 lists Chip and David as decision makers, so either can accept the
0.5.0 rules.

## F-1: sentences about another file

| option | outcome |
|---|---|
| (a) drop the sentences when no attestation is about your copy | **rejected** |
| (b) keep them, framed as being about another file | **accepted** |
| (c) put the framing inside the integrity line's sentence | **rejected** |

- *Rejected (a):* the sentence is what lets a relying party see what the
  tampered file was *supposed* to be. Dropping it hides the evidence of the
  mismatch the integrity line reports.
- *Rejected (c):* the integrity line already names both digests. The
  confusion is in the sentences block, after the answer, so the framing goes
  where the confusion is.
- *Accepted (b):* one line of framing, written into §10.4 as a MUST so the
  GUI (W-5) does the same. JSON carries `sentences_about_your_file` so a
  client does not re-derive it.

## F-2: the vacuous acceptance pass

| option | outcome |
|---|---|
| (a) keep **pass**, make the sentence say why, explain it in §10.4 | **accepted** |
| (b) make it **not evaluated** | **rejected** |
| (c) leave the wording and change nothing | **rejected** |

- *Rejected (b):* already proposed and rejected in DL-0016 and DL-0020 A1.
  "Not evaluated" in §10.4 means there was nothing to examine. A statement
  about the file that names no template *was* examined. It would also change
  a line result and Appendix A.
- *Rejected (c):* the slice notes (2026-11-01, 2026-11-09) and APP-0003 F-3
  both report that the pass reads as if a template had been met.
- *Accepted (a):* the sentence becomes "no template is named, so there is
  none to meet". No result changes.

## Versioning

- *SPEC-0004:* MINOR (0.5.0), because two MUSTs are added.
- *Wallet:* PATCH (0.4.1), wording only.
- *Rejected:* making the SPEC-0004 change PATCH as editorial. A MUST that a
  second implementation (the GUI) has to follow is not editorial.

## Not changed

- *APP-0004's sketches:* they paraphrase the verdict lines, so they were left
  as sketches rather than turned into quotes.
- *APP-0003 F-3:* left as the record of the finding.
