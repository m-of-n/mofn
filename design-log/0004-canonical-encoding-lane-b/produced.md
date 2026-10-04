---
schema: "design-log/v1"
id: DL-0004
part: produced
date: "2026-10-03"
---

# DL-0004 — produced

All library output is `m-of-n/library` commit **`79c543a`** on branch
`topic/canonical-encoding`, 20 files. Nothing was written to `mofn/` except
this entry.

## The answer — six conditions in two groups

`topics/canonical-encoding.yaml`. The question was **widened** from *"what must
hold for a canonical form to be safe to sign?"* to *"…to be safe to sign, and
to derive a stable identifier from?"*, on the `close-topic` rule that evidence
pointing at a stronger claim should widen the question rather than be answered
narrowly. `bears_on` gained DEC-003, R-M-11 and R-O-03.

To be safe to **sign**: (1) the encoding is injective, not merely
deterministic; (2) the decoder rejects non-canonical input rather than
normalising it; (3) canonicalisation runs once, at authoring, on trusted input,
never during verification; (4) an authenticated type indicator names the
profile inside the signed bytes. **R-O-05 delivers (3) and (4) and assumes (1)
and (2).**

To be safe to **derive an identifier from**, two more that no candidate
encoding supplies: (5) set-valued fields carried in arrays have a defined
canonical order; (6) identity-bearing text has a declared Unicode normalisation
rule, or an explicit refusal plus rejection of unnormalised input.

**R-O-05 reaches only the first group**, because at an identifier there are no
received bytes to verify verbatim — the digest is *produced by* canonicalising.
Three such sites exist in the only code there is: `keyid()` (R-M-02),
`by_description()` (R-M-11), `domain_id()` (P4).

## `records/ietf/rfc-8785/` — FX-1 full extraction

DEC-002 option 3's own specification, previously absent from the library
entirely.

| artifact | content |
|---|---|
| `normative.md` | 91 verbatim statements, §2–§6.1 and Appendices A–I |
| `requirements.yaml` | 41 entries; 32 BCP 14 verbs matching source exactly (25 MUST, 4 MUST NOT, 2 RECOMMENDED, 1 SHOULD) |
| `schema/` | Appendix A verbatim (sha256 `c4c656fd…a909`) + 3 derived; the RFC ships no grammar of any kind |
| `messages.yaml` | 16 structures, 61 fields |
| `protocol.{md,yaml}` | 3 flows, 5 error paths |
| `examples/vectors.yaml` | 44 vectors, all 26 Appendix B rows |
| `design-notes.md` | 6 adopt / 6 adapt / 8 reject, 12 open questions, 8 source defects |

`state-machine` recorded `not_applicable` with a written reason.
`distillation.profile: full` **deliberately withheld** pending pass 3, so
`bin/check-pr-extraction` correctly still blocks the PR.

## The finding — withdraw DEC-002 option 3

Not "score it lower". The lead ground is not the obvious one:

> RFC 8949 §4.2.1 is **silent** on array element order, so a CBOR profile may
> add a bytewise rule without contradicting it. RFC 8785 §3.2.3 says array
> element order **MUST NOT be changed**.

So the canonicalisation P4's set hash needs is a **modification** of JCS, not a
subset — and under R-O-03 that is a partly invented algorithm. *Prohibited*
versus *absent* decides it; scoping the citation cannot repair it.

Supporting: §5 normatively mandates parse → locate the signature property →
verify, the inverse of R-O-05. The number algorithm is not in the cited
document at all (§3.2.2.3 delegates to ECMA-262 and points at V8 and Ryu).

**Recorded in option 3's favour**: it wins **namespace governance outright** —
the criterion proposal §3.3 says was never scored. JSON has no tag space, no
header space, and §4 reads "This document has no IANA actions."

## Other library output

- `secure-systems-lab-dsse` summarised from `background.md` and `protocol.md`
  at pinned commit `1d3370f`. Two findings: its anti-canonicalisation
  requirements are **SHOULD, not MUST**, so R-O-05 is consistent with them; and
  its **(t, n) multi-signature envelope** means the R-I-03 export target already
  carries threshold semantics, bearing on R-M-06.
- `topics/deterministic-cbor-profiles.yaml` created; CDE, `cbor-serialization`
  and dCBOR moved there. They ask about convergence, not conditions, and under
  FX-1 they made `canonical-encoding` uncloseable.
- `library#43` — `bin/_yaml.py` silently discards block scalars; 36 of 44 FX-1
  vectors read as the literal string `"|-"`, so CI over them is vacuous.
- `library#44` — derived-vs-verbatim schema filenames have drifted; the
  convention is real but undocumented in `docs/extraction.md`.

## Named but deliberately not drafted

Two `propose-arch` candidates, left for the m-of-n repo:

1. **A scope clause on R-O-05** — that it governs signed payloads, and that
   identifier derivation (DEC-003, R-M-11, P4) is constrained separately.
2. **Scoped citation under R-O-03** — that a partial adoption SHALL name the
   adopted sections and state which normative provisions are not adopted, and
   why. Needed whichever encoding wins; `rfc-8949` has the same shape at
   §4.2.3 and §5.4.

Condition (2) was routed to **ARCH-0002 P5** rather than a new R-O-07.
