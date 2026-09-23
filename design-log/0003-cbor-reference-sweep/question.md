---
schema: "design-log/v1"
id: DL-0003
title: "CBOR reference sweep — 51 library records and RPT-0001"
date: "2026-09-22"
model: "claude-opus-5"
human: paul-lambert
outcome: "library/ +51 records, 2 topics; research/0001-cbor/ (RPT-0001). No ADR — DEC-002 untouched."
status: complete
---

# DL-0003 — question

## Context supplied

`manifest/repos.yaml` and `manifest/archives.yaml`; `kb/open.md`;
`library/CLAUDE.md`, `docs/scope.md` v0.2.0, `docs/references.md`,
`schema/record.schema.yaml` v5, and the three library skills
(`ingest-reference`, `summarize`, `distill`); `mofn/CLAUDE.md`;
ARCH-0001 §7 DEC-002…DEC-005, ADR-0001, `DECISIONS-0001` tier 1–2.

## Question posed

> "use the library skills to ingest all relevant references to CBOR - stick to
> what it takes to implement a complete product . summary page to have
> bibliography and spin side research deep market analysis of products with
> CBOR , markets, applications, open source code, consortiums , specifications
> ongoing work, each of these a side agent, organize the topics and review
> resutls to package in a research report on 'CBOR'"

## How it was decomposed

Six parallel agents, one per named dimension (products, markets, applications,
open source, consortiums, specifications). Each was given the same method
contract: primary sources preferred, every claim carries a URL and a retrieval
date, never fabricate, state explicitly what could not be verified.

Ingestion was **not** delegated. The record set was built by the author from
`rfc-editor.org/rfc-index.txt` and the datatracker API so that no bibliographic
fact in the library rests on an agent's summary.

## Constraint held throughout

`mofn/CLAUDE.md`: **DEC-002 is open; do not write documents that assume a
selection.** RPT-0001 is framed as evidence and states this in its first
paragraph. No ADR was written and no DEC was marked accepted.
