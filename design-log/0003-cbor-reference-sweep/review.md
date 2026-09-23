---
schema: "design-log/v1"
id: DL-0003
part: review
date: "2026-09-22"
---

# DL-0003 — review

## Rejected — agent claims overturned against primary sources

The reason the ingestion was not delegated. Three substantive claims from the
dimension agents were checked and **found wrong**:

1. **"`draft-ietf-cbor-serialization` supersedes CDE."** Asserted by the
   specifications agent; a `supersedes` edge was written into the record on
   that basis, then withdrawn. The draft's own text never mentions CDE
   (`grep -ci cde` → 0) and makes no replacement claim. Downgraded to
   `see_also`, with the reason recorded in the record's `usefulness`.
   *An unwarranted `supersedes` edge tells a future reader a document is safe
   to ignore. That is the most damaging possible error in a reference library.*

2. **"dCBOR is layered on CDE without forking it."** Asserted independently by
   *two* agents — applications and consortiums — which is precisely why
   agreement between agents is not evidence. False at `-18`: CDE appears
   nowhere in the document, whose normative references are the IANA registries,
   IEEE 754 and RFC 2119. It narrows RFC 8949 §4.2 directly. True of earlier
   revisions, which is how the received account survives in secondary sources.

3. **"RFC 9165 and RFC 9741 update RFC 8610."** The RFC Editor index shows an
   Updates relation only for RFC 9682. Recorded as `see_also`. The
   specifications agent had itself flagged this as unconfirmed — the flag was
   correct and was resolved from the index.

Also corrected, from the agents' own cross-checking: **Matter does not use
CBOR** (it uses TLV), **in-toto/DSSE is JSON**, and **Intel TDX / AMD SEV-SNP
attestation are not CBOR**. These are recorded in RPT-0001 §7 because a survey
that repeats them is worse than no survey.

## Accepted

The six-dimension decomposition worked. The method contract — primary sources,
URL plus retrieval date on every claim, explicit "could not verify" section —
produced material that was checkable, which is what made the three rejections
possible. An agent that had merely sounded confident would have been
unfalsifiable.

The determinism divergence table (RPT-0001 §3) is the substantive finding and
survived verification intact.

## Process failure recorded

`research/README.md` rule 2 requires verbatim archiving of the queries run.
**This pass does not meet it.** The agents archived sources and retrieval dates
but not queries, and that is unrecoverable after the fact. `searches.md` says
so plainly rather than presenting the author-run commands as if they were the
whole search. The fix — extend the output contract to require a per-dimension
`searches.md` fragment — is written down there.

This is the same failure `library/docs/construction.md` was written about,
reproduced one increment later, by a method designed to prevent it.

## Outcome

**No ADR. DEC-002 remains open** and RPT-0001 states in its opening paragraph
that it selects nothing. The report supplies evidence for DEC-002, DEC-003,
DEC-005, R-M-07 and R-M-12, and names one interaction nobody has written down:
**COSE's protected header requires tag 24, so a profile that bans all tags
under R-M-12 cannot use COSE as specified.** That belongs in the DEC-005
discussion and is not resolved here.
