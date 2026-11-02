---
schema: "design-log/v1"
id: DL-0016
part: review
date: "2026-10-20"
---

# DL-0016 — review

**Human review of the code is pending.** The human has not yet read the
diff or run the slice. Below is only what was decided or rejected so far, and
by whom.

## Chosen by the human

- **Scope: engine plus a thin CLI.** Offered: engine only; engine + thin
  CLI; the whole wallet including Chip's track B; A0 only. Chose engine + thin
  CLI, so the goldens can be tested end to end without taking Chip's track.
- **Acceptance line = pass when no template is named.** SPEC-0004 Appendix A
  prints `acceptance: pass  # TV-4 names no template`. Golden ① is therefore
  six passes.
- **Show the data in the demo.** For the presentation, the human asked to see
  a statement, a definition, an envelope and an anchor. Produced `mofn show`,
  which decodes without verifying, and `mofn root list` for the anchors. The
  wallet README explains each field under "Reading the files".

## Rejected by the human

- **"not evaluated" for acceptance** (#65-c2 A1, posted to Paul on Oct 20).
  Rejected in favour of what SPEC-0004 Appendix A already says. **A1 as posted
  is now out of date on this point** and #65 needs a follow-up.
- **Pushing the branch and opening a draft PR** as the last step of the plan.
  Rejected: "don't push". The commits are local only; CLAUDE.md's "open the PR
  in the browser" step waits for the human.
- **Committing the demo guide** (`prototype/wallet/DEMO.md`, a script for
  presenting the engine live, with talking points). Rejected: "demo.md don't
  need to be committed; update readme instead". The guide stays a local file;
  what a reader of the repo needs from it went into the README: the cases and
  the line that decides each, the six lines, how to read the files, and what
  the wallet keeps.

## Rejected before this session (carried from #65-c2 and the notes)

These were decided by David and Chip in the notes and the #65 comment; the
code follows them. Recorded so the rejection lives here too.

- **A JSON second codec.** It would invent a second signed format; ADR-0003
  D2 says one canonical encoding. The second codec is the human-review YAML
  form instead (C1, still to be confirmed by Paul).
- **`--passphrase VALUE`** — on the command line, in `ps` and shell history.
- **A passphrase in an environment variable** — readable by other processes.
- **`--type paul:build-provenance`** — `paul:` needs a names layer v0 does
  not have; a type is `(DefinitionId, label)` (SPEC-0002 §7.4).
- **Merging `key import` into `root add`** — then "known but not trusted",
  the state golden ② needs, could not be reached.
- **`--domain`** — every SPEC says *definition*; the flag is `--def`.

## Rejected by the model, with the evidence

- **`cryptography` (OpenSSL) as the Ed25519 library.** It accepts the
  identity point as a key and exposes no check, so N-4 could only pass with a
  hand-written point check — a primitive, which CLAUDE.md forbids. See the
  experiment in `produced.md`.
- **Porting `prototype/statements/rcbor.py` as the encoder.** It emits
  `null`, has no ±(2^53−1) bound, and its sibling `statement.py` truncates
  hashes to 16 bytes. The encoder is `generate.py`'s instead, which is already
  the one the vectors were cross-checked with.
- **Exit 3 for an unverifiable statement.** The working notes said 3 for
  invalid *or* unverifiable in one place, and that ②b exits 1 in another. SPEC-0002 §9.1 keeps them apart:
  unverifiable "may be valid". Exit 3 is for invalid only.
- **Taking the ask's subject from the statement.** Then a tampered artifact
  fails nothing under SPEC-0004 alone. The ask is about the relying party's
  own file, `[2, 1, sha256(file)]`, which is what that party is actually
  asking; A1's integrity check follows from it.
- **Goldens that contain kids, digests or times.** Keys are generated fresh
  on every run, so a golden with a kid could never match. The text verdict
  names keys by the relying party's labels and the artifact by its fixed hash;
  the JSON form carries the digests.
- **Writing a text that looks like `'0x…'` in a YAML value.** It would read
  back as bytes. `dump` refuses it rather than write a form that does not
  round-trip (SPEC-0002 §11.1).

## Open for the human

1. **#107 has merged**, with §11 unchanged from what the codec follows. Two
   choices §11 does not state remain (target spelling `{key: '0x…'}` etc.;
   the `0x` text ambiguity above); both should be raised against SPEC-0002.
2. **libsodium is stricter than SPEC-0002 §6.3**: `is_valid_point` also
   rejects keys with a torsion component. An honest key is never affected;
   whether §6.3 should say so is a question for Paul (C4).
3. **The answer is yes only if all six lines pass.** SPEC-0004 §10.3 defines
   the answer by coverage alone; v0 also requires integrity (A1),
   authenticity and semantics. Under the default policy of §9 the results
   agree, except for a key known only from an envelope `pub` hint.
4. **Golden ③ fixes how the byte is flipped** (first byte → `X`), because the
   integrity sentence prints the tampered file's hash. Chip's slice must flip
   the same byte, or the golden needs a placeholder.
5. **SPEC-0003 Appendix A is YAML 1.2, not 1.1.** Its unquoted
   `ask: {en: Does the provenance name the expected builder?}` is refused by
   PyYAML, which the §11 strict reader is built on. `mofn show dv-1.def`
   quotes that value, and its test quotes it before comparing. Either the
   example quotes it, or §11 says which YAML version the human form is.
6. **DEC-002 and DEC-003 were accepted while this was open** (ADR-0004,
   ADR-0005, mofn#117). The engine already used KSA-CBOR and `kid` =
   SHA-256(pub), and SPEC-0002 0.2.0 changes no signed bytes, so no code
   changed on the rebase; only the README and docstrings that called them
   open. The entry was renumbered from 0014, which mofn#112 took first.

**Items 1–5 and A1, C1 and C4 are decided in DL-0020** (2026-11-01), with the
evidence and what was rejected. C2, C3 and C5 could not be identified.
