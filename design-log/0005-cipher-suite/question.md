---
schema: "design-log/v1"
id: DL-0005
title: "Cipher suite — definition and critique, before any statement schema"
date: "2026-10-02"
model: "grok"
human: "pending"
outcome: "R-0003 (research/0003-cipher-suite). No ADR. DEC-002 not touched. No code change."
status: open
---

# DL-0005 — question

## Context supplied

Paul's definition of a cipher suite, quoted in the task and repeated in
R-0003 §1. APP-0001 and PLAN-0004 on `origin/main` (`0ea374c`): local file
wallet, unsigned trust roots, short expiry as revocation, engine is files
plus reduce/check, no knowledge graph. DEC-002 open in DECISIONS-0001.
`src/` empty so code does not decide the encoding. The existing
implementation was not in the repo; it was found at
`/Users/paul/cb/projects/hpke/cipher_suite.py`.

## Question posed

Start the schema design for the wallet, attestations, and delegation
statements at the cipher suite. Critique the existing `cipher_suite.py`.
Suggest a structure. Write a definition-and-example report. Change code
only for a concrete defect or a missing function that does not close an
open decision. Do not design the full schemas. Do not close DEC-002. Do
not invent a key exchange.
