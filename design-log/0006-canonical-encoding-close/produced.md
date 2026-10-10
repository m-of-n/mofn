---
schema: "design-log/v1"
id: DL-0006
part: produced
date: "2026-10-08"
---

# DL-0006 — produced

All of it in `library/`, on branch `topic/canonical-encoding-close`
(**library#57**). Nothing in `spec/`, `src/` or `prototype/` — see
`question.md` §Scope.

## In `library/`

**`secure-systems-lab-dsse` — read out and promoted.** The source archive was
re-fetched at the pinned commit and its sha256 **re-verified** against
`content.sha256` before anything was written. `envelope.md`, `envelope.proto`
and `hypothetical_signature_attack.ipynb` were read — the gap the topic note
itself had named. `status: summarized` → `distilled`, with a new `distilled/`
holding `README.md`, `normative.md` (24 verbatim statements, 9 carrying a BCP 14
keyword) and `design-notes.md` (five findings). `bears_on` gained `DEC-003`,
`R-M-02` and `R-M-12`.

**`topics/canonical-encoding.yaml` — answered.** `status: active` → `answered`.
The stale closing paragraph was replaced by eight new blocks: option 1 scored
condition by condition; two findings from option 1 that revise earlier claims;
the three-axis cost comparison for all four candidates; the DSSE retraction and
weakening; two new DSSE findings; the attack notebook's sharpening of condition
(1); the `answered` justification with its one deliberately-unread record; and
what the answer unblocks and who acts.

**Two claims corrected in place, in three files.** The `(t, n)` withdrawal
touched `topics/canonical-encoding.yaml`, the DSSE `summary.md`, and
`records/ietf/rfc-9804/distilled/design-notes.md`, whose R-I-03 row had
inherited the claim from the note.

**Topic ownership drift fixed.** `ipld-dag-cbor` and the three CBOR drafts →
`deterministic-cbor-profiles` (and `ipld-dag-cbor` added to its `records:`,
where that topic's own answer had already been discussing DAG-CBOR without
owning it). `yaml-1-2-2` and `strictyaml-why` → `library-construction`, which
gained its first two records and a written-out reason. `w3c-rdf-canon-1-0` left
`fetched` and unowned **by design**, with the reason stated in the answer.

**Three issues opened.** `library#56` — read RDFC-1.0 as the one plausible prior
art for condition (5). **#72** — the ARCH-0002 P5 clause extension, now carrying
the DSSE envelope-layer collision as a second reason. **#73** — the single-pass
rejecting decoder, with `c-sexp` recommended first because RFC 9804 makes it
~50 lines and already argues the result.

## In `mofn/`

This design-log entry, and the two handoff issues. **Nothing else** — no
`mkdocs.nav.yml`, no `project/PUBLISHING.md`.

An earlier revision of this branch carried regenerated copies of both. They are
gone: the branch was built on a `main` 22 commits stale, and on the real `main`
those files had already been fixed and are now **drift-checked by CI** (#62).
Regenerating them from the current tree produces no diff, which is the correct
outcome — this change adds a design-log entry and the nav does not list
design-log entries. `review.md` §11 records how the stale base was found and the
three other things it caused.

## The substantive findings

Ordered by how much they change, not by where they appear.

1. **The `(t, n)` envelope carries `n`, not `k`.** *Withdrawn*, see
   `review.md` §1. This is the finding with consequences: R-M-06's interchange
   story is not cheaper than assumed, under **any** DEC-002 option.
2. **Condition (1) must hold over the `(profile, bytes)` pair.** The attack
   notebook's payload is a **polyglot** — injective within CBOR, injective
   within protobuf, ambiguous across the pair. The six conditions as written
   quantify condition (1) over bytes under one profile, which is not enough.
   This makes the authenticated type indicator load-bearing rather than
   belt-and-braces, and makes **DEC-002 option 4** the candidate most exposed,
   since option 4 keeps two profiles live and asserts a bijection between them.
3. **JCS is idempotent; what fails is injectivity.** The issue's second question
   asks whether canonicalisation is idempotent, and for JCS the honest answer
   inverts the question: run it on its own output and nothing changes, but the
   first pass is lossy — Appendix B serialises 2^68 as a different integer,
   silently, with a signature that verifies. *Stable on re-application, lossy on
   application*, which is worse for condition (1) than non-idempotence, because
   non-idempotence is loud.
4. **`MUST ignore unrecognized fields` collides with ARCH-0002 P5** at the
   envelope layer — and only there, since unsupported payload *types* are
   rejected. A conforming DSSE export boundary cannot enforce P5 on the envelope
   exterior, and no document of ours says which reading holds.
5. **DSSE's `KEYID` is the exact inverse of our `KeyId`.** Unauthenticated,
   `MUST NOT` drive security decisions — against R-M-02, under which `KeyId`
   *is* the principal's name. The failure mode is a mapping table under R-I-01
   that lines the two up because they share a name.
6. **Condition (5) is not a discriminator between DEC-002 options.** From RFC
   9804's extraction: every candidate is silent on canonical set order except
   option 3, which prohibits it. What distinguishes option 3 is not the absence
   of the rule but the prohibition.
7. **Option 1 also wins namespace governance** — the criterion the v0.2.0
   proposal §3.3 says was never scored and that the note recorded as option 3's
   outright win — by the same registry-free argument, and without option 3's §5
   cost.
8. **The ranking the three cost axes produce is not the ranking the six
   conditions produce.** That disagreement is the deliverable for #8, not a
   complication in it.

## Verification run

```sh
bin/validate                   # 0 errors, 1 warning (the #45 scaffold backlog, pre-existing)
bin/check-pr-extraction main   # FX-1: every record this PR extracts is complete
bin/export && bin/reindex      # clean; neither committed
```

`bin/check-pr-extraction` reports the five topic-pointer-only records at the
**summary bar** and demands FX-1 of none of them, which is the amended
"extracting, not touching" rule behaving as intended.
