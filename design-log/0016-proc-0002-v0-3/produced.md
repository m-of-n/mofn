---
schema: "design-log/v1"
id: DL-0016
part: produced
date: "2026-10-29"
---

# DL-0016 — produced

| file | what |
|---|---|
| `project/PROC-0002-multi-agent-ingestion.md` | 0.2.0 → 0.3.0; §2 stage 8 rewritten; §5 gate; §6 two rules; §8 reconciled; §9 changelog added |
| `project/BACKLOG-0001.md` | 0.12.2 → 0.12.3; the FIPS 186-5 stage 8 paragraph no longer says "generate an implementation" |

## The changes, by reason

1. **Stage 8 is a harness over a vetted library, never a primitive.** v0.2 said
   *"reference code from the spec — e.g. NIST DSS → Python or C"*. Generating
   ECDSA/EdDSA from FIPS 186-5 **is** generating a cryptographic primitive,
   which CLAUDE.md and the design-log README both forbid. The comprehension test
   the sponsor wanted survives: parameter mapping, encodings and hash choices
   are where misreadings live, and CAVP vectors catch them through a harness
   as well as through a from-scratch implementation. Encodings and wire formats
   stay in scope for agent-written code.
2. **`artifacts/` → `harness/`.** *Artifact* is normative (`ArtifactId`,
   R-M-07). No stage 8 code exists yet in either repo, so the rename breaks
   nothing.
3. **`src/` rationale.** "empty until DEC-002" was false once ADR-0004 landed;
   now cites DEC-004/DEC-005 as CLAUDE.md does.
4. **§6 gains DL-0009's two rules** — cite-or-leave-empty for
   `decision_makers`/`reviewers`/`reviewed`; fetch before reporting anything
   stale. DL-0009 said they belong in PROC-0002 "where it can bind".
5. **§8.1 closed** by MD-4; §8.2/4/6/7 point at their register rows so the
   question is answered in one place.
