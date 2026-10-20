---
schema: "library-doc/v1"
id: R-0006-searches
title: "Searches — mechanism"
type: evidence
status: draft
version: "0.2.0"
date: "2026-10-14"
updated: "2026-10-17"
---

# Searches

## No web searches were run for this report

`BACKLOG-0001` T-026 scopes the task as *"R-001 §2/§4, plus the RFC 8785 R-O-05
analysis in library#46"* — a synthesis of material already extracted. No new
retrieval was performed, and `research/README.md` requires this file to say so
rather than leave the absence implied.

**Nor for the v0.2.0 reconciliation pass.** §3.13 and the revisions to §3.2,
§3.9, §3.10, §3.12, §5.2, §6 and §8 were written from documents that landed on
`main` on 2026-10-14 — `ADR-0003`, `SPEC-0001`…`SPEC-0005`, `UC-0001`,
`ARCH-0003` and `spec/vectors/ksa-core/` — read in-repo at
`643fba2`. No external source was consulted and no published specification was
re-read, so every external claim in this report still rests on the extractions
below. §3.13's findings are claims about **our own documents** and are checkable
by reading them; the exact sections are cited inline so a reviewer can do that
without taking the report's word for any of it.

## v0.3.0 — library queries, not web searches

The comparative anatomy (§2.2–§2.5) was built by **querying the library at
`library@60b3284`**, not the web. No external retrieval was performed, so the
rule above still holds. These are the queries, verbatim, with their yield, run
2026-10-17 from `library/`. **The misses are the result.**

| # | query | yield | what it settled |
|---|---|---|---|
| 1 | `ls records/*/ \| grep -ciE 'pics\|dsig\|did\|vc\|verifiable\|scitt\|in-toto\|dsse\|merkle\|cose\|rdf\|spki\|sdsi'` | 31 record ids | the candidate set. A record existing is not the same as its being written up — see 7 |
| 2 | `grep -ril -- 'verifiable credential' records topics` | **0** | no VC record |
| 3 | `grep -ril -- 'vc-data-model' records topics` | **0** | no VC Data Model record |
| 4 | `grep -ril -- 'vc-jose' records topics` | **0** | no VC-JOSE-COSE record |
| 5 | `grep -ril -- 'data integrity' records topics` | 14 | **miss**: all generic security guidance (OWASP ASVS, NIST SP 800-218, ETSI, CISA, FDA); none is VC Data Integrity |
| 6 | `grep -rli 'md5' records/w3c` | **0** | no record states how a PICS label binds content |
| 7 | read `summary.md`, `record.yaml` `status`, and presence of `distilled/` for each record named in the T-026 brief §6 under SPKI, PICS, VC/DID, envelopes, Merkle | 23 stubs | which cells of §2.2 can be filled. Itemised in `sources.md` §2a and `unverified.md` |
| 8 | `grep -rl -- '#46' records topics`; `grep -ril -- 'library#46' records topics` | **0**; **0** | the RFC 8785 design notes do not cite the PR that produced them (`report.md` §3.4) |
| 9 | `grep -ril -- 'R-O-05' records topics` | 29 files | R-O-05 is analysed widely in the library, including `rfc-8785/distilled/design-notes.md`, which marks it *proposed* |

Query 7 was run by a delegated read-only pass over the records. Queries 1–6, 8
and 9 were re-run by hand afterwards so that the counts above are the ones
recorded.

**In-repo reads for §4.6–§4.7**, no retrieval: `SPEC-0003` §5.4 and §6;
`SPEC-0004` §6; `ADR-0003`; `ARCH-0001` §4–§7; `BACKLOG-0001` I3; and
`DECISIONS-0001` item 4. All read at `c0c93c3`.

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
| RFC 8949, RFC 8785, RFC 9804 extractions | each record's `distilled/` plus `record.yaml` provenance, `library@60b3284` |
| DSSE full read (2026-10-08) | `library/topics/canonical-encoding.yaml`; archive digest re-verified at the pinned commit |
| The `canonical-encoding` topic close | library#14, library#57; `design-log/0006-canonical-encoding-close/` |
| The decoder spike | mofn#73, mofn#78; `design-log/0007-rejecting-decoder-spike/` — including its own fixture list |
| R-001 §9, §11, §12 | `research/0001-signatures-and-attestation/searches.md` |
| `ADR-0003` D2, `SPEC-0002` §4/§5/§8.6, `SPEC-0003` §6/§13.4, `SPEC-0004` §6.3/§6.4, `spec/vectors/ksa-core/` — the §3.13 material | authored in-repo at `643fba2`; no retrieval |

## The one experiment this pass did not re-run

§3.10's result is quoted from the spike, not reproduced. `prototype/statements/
test_decode.py` holds 60 fixtures and is the thing to re-run; the spike's own
caveat — that `rcbor_decode.py` is **evidence rather than a component**, and
that nothing in the spike round-trips through it — is carried into `report.md`
§3.6 rather than dropped.
