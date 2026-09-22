---
name: Ingest a reference
description: Use when a document needs a library record — a new source found during research, or the next item in a topic's reading list.
---

# Ingest a reference

`library/schema/record.schema.yaml` is the schema. `library/docs/construction.md`
is the method. This skill is the judgment around them.

1. **Grep `library/records/` first.** Never create a second record for the same
   document. A spec at a new version is a *new* record linked by `supersedes` —
   not an edit of the old one.
2. **Pick the narrowest type.** `rfc` and `draft` beat `ietf`; `spec` beats
   `web`. The type decides which fields a reviewer expects. `bin/ingest --list`.
3. `library/bin/ingest <type> <source> --topic <id> --bears-on <ids>`. Never
   hand-create a record directory — the adapter fills identifiers you will get
   wrong by hand.
4. **`bears_on` names the `DEC-*` or `R-*` this document informs** — when one
   applies. **When none does, ingest it anyway as a stub:** `--stub`. A
   reference that is not fully applicable is still worth recording for use
   elsewhere, and a stub is cheap. Never invent relevance to justify a record.
5. **`status` reflects what you have actually done.** `stub` = kept for later.
   `queued` = to read. Do not set `read` or `summarized` because the file
   downloaded.
6. **Set `maturity` only if you checked it.** RFC 2026 levels — `standard`,
   `best-practice`, `informational`, `experimental`, `historic`. An RFC being an
   RFC does not make it a standard. Leave unset rather than guess.
7. **Prefer a controlled tag** from `schema/tags.yaml` — subject, body, role.
8. Typed relations only — `supersedes`, `updates`, `see_also`, `contradicts`,
   `part_of`, `implements_concept`. `contradicts` is the valuable one and the
   one everybody forgets.
9. `bin/validate && bin/export`, commit the regenerated `exports/`.

Use `--fetch` only when the digest matters. It reaches the network and writes to
`.cache/`, which is gitignored.

**Never commit the document itself.** PDF, spreadsheet, ebook: record the
`sha256` and the URL. CI rejects the bytes.

For a standards family — an IETF working group, a C2PA release line — create one
`consortium` or `hierarchy` record and point members at it with `part_of`. Do
not create forty sibling records with no parent.

Stop after ingest. Writing `summary.md` is the `summarize` skill; `distilled.md`
is the `distil` skill and most records never need one.
