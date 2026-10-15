---
schema: "library-doc/v1"
id: R-0006-searches
title: "Searches — mechanism"
type: evidence
status: draft
version: "0.1.0"
date: "2026-10-14"
updated: "2026-10-14"
---

# Searches

## No searches were run for this report

`BACKLOG-0001` T-026 scopes the task as *"R-001 §2/§4, plus the RFC 8785 R-O-05
analysis in library#46"* — a synthesis of material already extracted. No new
retrieval was performed, and `research/README.md` requires this file to say so
rather than leave the absence implied.

## Why that is less of a limitation here than in R-0005

R-0005's evidence is a survey of a moving field, so a stale retrieval date
matters. This report's evidence is **four published specifications and one
repository at a pinned commit**, all of which were read at FX-1 full-extraction
depth by the library. Specifications do not move between retrievals; RFC 8949,
RFC 8785 and RFC 9804 say today what they said when extracted.

The two places where staleness could still bite are named in `report.md`:

- **The CBOR profile drafts** (`draft-ietf-cbor-cde`,
  `draft-mcnally-deterministic-cbor`, `draft-ietf-cbor-serialization`) moved to
  topic `deterministic-cbor-profiles` on 2026-10-03 and are **not** scored
  here. They are drafts and they move.
- **The 2026 agentic drafts** in §4.3 are individual Internet-Drafts, none
  WG-adopted. Their constraint vocabularies are exactly the thing that would
  change between revisions, and §4.3's claim that the attenuating-token draft
  is "one `⊓` away" is a claim about a specific revision.

## Where the original searches are archived

| material | search record |
|---|---|
| RFC 8949, RFC 8785, RFC 9804 extractions | each record's `distilled/` plus `record.yaml` provenance, `library@f57dcbc` |
| DSSE full read (2026-10-08) | `library/topics/canonical-encoding.yaml`; archive digest re-verified at the pinned commit |
| The `canonical-encoding` topic close | library#14, library#57; `design-log/0006-canonical-encoding-close/` |
| The decoder spike | mofn#73, mofn#78; `design-log/0007-rejecting-decoder-spike/` — including its own fixture list |
| R-001 §9, §11, §12 | `research/0001-signatures-and-attestation/searches.md` |

## The one experiment this pass did not re-run

§3.10's result is quoted from the spike, not reproduced. `prototype/statements/
test_decode.py` holds 60 fixtures and is the thing to re-run; the spike's own
caveat — that `rcbor_decode.py` is **evidence rather than a component**, and
that nothing in the spike round-trips through it — is carried into `report.md`
§3.6 rather than dropped.
