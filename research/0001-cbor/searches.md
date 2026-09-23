---
schema: "library-doc/v1"
id: RPT-0001-searches
title: "Searches run — CBOR research"
type: evidence
status: draft
version: "0.1.0"
date: "2026-09-22"
updated: "2026-09-22"
needs_review: true
---

# Searches

> **This file does not meet `research/README.md` rule 2.** That rule requires
> the queries to be archived verbatim. The six dimension agents recorded their
> *sources* and retrieval dates but not the *queries* that produced them, and
> that cannot be reconstructed after the fact. What follows is the part that is
> reconstructable, plus an explicit statement of the part that is not. Recorded
> as a process failure to fix on the next pass, not smoothed over — the whole
> point of `library/docs/construction.md` is that this is the failure mode.

## 1. Author-run retrievals — verbatim, reproducible

These are the queries the report's specification claims rest on. All run
2026-09-22.

```sh
# The start set: every CBOR/COSE/CDDL RFC, from the authoritative index.
curl -sS https://www.rfc-editor.org/rfc-index.txt -o rfc-index.txt
# then, over parsed entries, the inclusion filter:
#   \bCBOR\b | \bCDDL\b | Concise Binary | Concise Data Definition
#   | CBOR Object Signing | \bCOSE\b
# yield: 41 entries from 8,995 RFCs

# Draft status, revision and expiry — the check that overturned the
# secondary account of CDE and Packed CBOR.
for d in draft-ietf-cbor-serialization draft-ietf-cbor-cde \
         draft-ietf-cbor-packed draft-ietf-cbor-edn-literals \
         draft-ietf-cbor-cddl-modules draft-mcnally-deterministic-cbor; do
  curl -sS "https://datatracker.ietf.org/api/v1/doc/document/?name=$d&format=json"
done
# yield: 6/6 resolved; rev, states, stream, expires for each

# Relation checks against the source text, not against commentary.
grep -niE "obsolet|replaces|supersed" draft-ietf-cbor-serialization-08.txt
grep -ci 'cde' draft-ietf-cbor-serialization-08.txt        # -> 0
grep -ci 'cde' draft-mcnally-deterministic-cbor-18.txt     # -> 0
sed -n '/Normative References/,/Informative/p' draft-mcnally-deterministic-cbor-18.txt

# Duplicate check before ingesting anything.
grep -ril "cbor" --exclude-dir=.git .        # in library/ -> 9 pre-existing hits
```

**Yield of the backward (Wohlin) pass so far: 1 frontier entry** — the IANA
CDDL registry, cited normatively by dCBOR and not held. It is on
`library/index/frontier.md`. A full backward pass over the 51 records'
reference sections has **not** been run; `cites` is populated for one record
only.

## 2. Agent searches — not archived

Six agents ran in parallel, each given a dimension, a method rule ("every
claim carries a source URL and retrieval date; never fabricate; prefer primary
sources") and an output contract. Each wrote a `## Sources` section and a
"what I could not verify" section, both preserved in `dimensions/`.

**What is missing:** the verbatim queries, the number of results screened per
query, and the per-iteration yield. PRISMA-style reporting of what was found,
screened and excluded is therefore **not possible for the agent tier** of this
research. The dimension files record where each agent landed, not how it got
there.

## 3. Fix for the next pass

Agent prompts must require a `searches.md` fragment per dimension — query
verbatim, date, result count, how many kept — returned alongside the findings.
The contract that produced good sourcing here (URL + retrieval date on every
claim) worked; the same contract simply was not extended to queries.
