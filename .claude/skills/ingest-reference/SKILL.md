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
4. **`bears_on` is mandatory judgment, not a tag.** Name the `DEC-*` or `R-*`
   this document actually informs. If you cannot name one, the reference is not
   needed yet — say so and stop rather than ingesting it.
5. **`status: queued` until you have read it.** Do not set `read` or `distilled`
   because the file downloaded.
6. Typed relations only — `supersedes`, `updates`, `see_also`, `contradicts`,
   `part_of`, `implements_concept`. `contradicts` is the valuable one and the
   one everybody forgets.
7. `bin/validate && bin/export`, commit the regenerated `exports/`.

Use `--fetch` only when the digest matters. It reaches the network and writes to
`.cache/`, which is gitignored.

**Never commit the document itself.** PDF, spreadsheet, ebook: record the
`sha256` and the URL. CI rejects the bytes.

For a standards family — an IETF working group, a C2PA release line — create one
`consortium` or `hierarchy` record and point members at it with `part_of`. Do
not create forty sibling records with no parent.

Stop after ingest. Distilling is the `distill` skill and a separate judgement.
